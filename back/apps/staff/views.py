
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


from apps.oaauth.models import OADepartment
from apps.oaauth.serializers import DepartmentSerializer
from .serializers import AddStaffSerializer, OAUser
from utlis.aeser import AESCipher
from django.urls import reverse
from HiiaenOAback.celery import debug_task
from .tasks import send_email_task
from django.views import View


OAUser = get_user_model()


# Create your views here.

class DepartmentListView(ListAPIView):
    queryset = OADepartment.objects.all()
    serializer_class = DepartmentSerializer


class ActiveStaffView(View):
    def get(self,request):
        token = request.GET.get('token')
        response = render(request,'active.html')
        response.set_cookie('token',token)
        return response



        




class StaffView(APIView):
    def get(self,request):
        return Response

    
    def post(self, request):
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

    def send_active_email(self,email):
        aes = AESCipher(settings.SECRET_KEY)
        token = aes.encrypt(email)
        active_path = reverse('staff:active') + "?token=" + token
        active_url = self.request.build_absolute_uri(active_path)

        # 发送一个链接 让用户点击这个链接后，跳转到激活的页面，才能激活
        message = f"请点击以下链接激活账号：{active_url}"
        subject = f'【HiiAenOA】账号激活'
        # send_mail(subject, recipient_list=[email], message=message,
        #             from_email=settings.DEFAULT_FROM_EMAIL)
        send_email_task.delay(email,subject,message)

class TestCeleryView(APIView):
    def get(self,request):
        debug_task.delay()
        return Response({"detail":"成功！"})