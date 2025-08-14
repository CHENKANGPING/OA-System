from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import exceptions  
from HiiaenOAback.celery import debug_task
from apps.oaauth.models import OADepartment, UserStatusChoices
from apps.oaauth.serializers import DepartmentSerializer, UserSerializer

from utlis.aeser import AESCipher
from .serializers import AddStaffSerializer, OAUser, ActiveStaffSerializer
from .tasks import send_email_task
from urllib import parse
from .paginations import StaffListPagination


OAUser = get_user_model()

aes = AESCipher(settings.SECRET_KEY)


# Create your views here.

class DepartmentListView(ListAPIView):
    queryset = OADepartment.objects.all()
    serializer_class = DepartmentSerializer


class ActiveStaffView(View):
    def get(self, request):
        token = request.GET.get('token')
        response = render(request, 'active.html')
        response.set_cookie('token', token)
        return response

    def post(self, request):
        try:
            token = request.COOKIES.get('token')
            email = aes.decrypt(token)
            serializer = ActiveStaffSerializer(data=request.POST)
            if serializer.is_valid():
                from_email = serializer.validated_data.get('email')
                user = serializer.validated_data.get('user')
                if email != from_email:
                    return JsonResponse({"code": 400, "message": "邮箱错误"})
                user.status = UserStatusChoices.ACTIVED
                user.save()
                return JsonResponse({"code": 200, "message": ""})
            else:
                detail = list(serializer.errors.values())[0][0]
                return JsonResponse({"code": 400, "message": detail})
        except Exception as e:
            return JsonResponse({"code": 400, "message": "token错误！"})


class StaffViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin
                ):
    queryset = OAUser.objects.all()
    pagination_class = StaffListPagination

    
    def get_serializer_class(self):
        if self.request.method in ['GET', 'PUT']:

            return UserSerializer
        else:
            return AddStaffSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.department.name != '董事会':
            if user.uid !=user.department.leader.uid:
                raise exceptions.PermissionDenied()
            else:
                queryset = queryset.filter(department_id=user.department_id)
        return queryset.order_by("-date_joined").all()


    def post(self, request, *args, **kwargs):
        serializer = AddStaffSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            realname = serializer.validated_data['realname']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = OAUser.objects.create_user(realname=realname, email=email, password=password)

            department = request.user.department
            user.department = department
            user.save()

            self.send_active_email(email)

            # 添加成功响应
            return Response(data={'detail': '员工添加成功，激活邮件已发送'}, status=status.HTTP_201_CREATED)

        else:
            return Response(data={'detail': list(serializer.errors.values())[0][0]},
                            status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    
    
    

    def send_active_email(self, email):
        token = aes.encrypt(email)
        active_path = reverse('staff:active') + "?" + parse.urlencode({'token': token})

        active_url = self.request.build_absolute_uri(active_path)

        # 发送一个链接 让用户点击这个链接后，跳转到激活的页面，才能激活
        message = f"请点击以下链接激活账号：{active_url}"
        subject = f'【HiiAenOA】账号激活'
        # send_mail(subject, recipient_list=[email], message=message,
        #             from_email=settings.DEFAULT_FROM_EMAIL)
        send_email_task.delay(email, subject, message)


class TestCeleryView(APIView):
    def get(self, request):
        debug_task.delay()
        return Response({"detail": "成功！"})
