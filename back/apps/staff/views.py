import email
import json
from datetime import datetime
from urllib import parse

import pandas as pd
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework import exceptions
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from HiiaenOAback.celery import debug_task
from apps.oaauth.models import OADepartment, UserStatusChoices
from apps.oaauth.serializers import DepartmentSerializer, UserSerializer
from utlis.aeser import AESCipher
from .paginations import StaffListPagination
from .serializers import AddStaffSerializer, OAUser, ActiveStaffSerializer, StaffUploadSerializer
from .tasks import send_email_task

OAUser = get_user_model()

aes = AESCipher(settings.SECRET_KEY)


def send_active_email(request, email):
    token = aes.encrypt(email)
    active_path = reverse('staff:active') + "?" + parse.urlencode({'token': token})

    active_url = request.build_absolute_uri(active_path)

    # 发送一个链接 让用户点击这个链接后，跳转到激活的页面，才能激活
    message = f"请点击以下链接激活账号：{active_url}"
    subject = f'【HiiAenOA】账号激活'
    # send_mail(subject, recipient_list=[email], message=message,
    #             from_email=settings.DEFAULT_FROM_EMAIL)
    send_email_task.delay(email, subject, message)


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
        department_id = self.request.query_params.get('department_id')
        realname = self.request.query_params.get('realname')
        date_joined = self.request.query_params.getlist('date_joined')

        queryset = self.queryset
        user = self.request.user
        if user.department.name != '董事会':
            if user.uid != user.department.leader.uid:
                raise exceptions.PermissionDenied()
            else:
                queryset = queryset.filter(department_id=user.department_id)
        else:
            if department_id:
                queryset = queryset.filter(department_id=department_id)

        if realname:
            queryset = queryset.filter(realname__contains=realname)

        if date_joined:
            try:
                start_date = datetime.strptime(date_joined[0], '%Y-%m-%d')
                end_date = datetime.strptime(date_joined[1], '%Y-%m-%d')
                queryset = queryset.filter(date_joined__range=(start_date, end_date))
            except Exception:
                pass
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

            send_active_email(request, email)

            # 添加成功响应
            return Response(data={'detail': '员工添加成功，激活邮件已发送'}, status=status.HTTP_201_CREATED)

        else:
            return Response(data={'detail': list(serializer.errors.values())[0][0]},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class SraffDownloadView(APIView):
    def get(self, request):
        pks = request.query_params.get('pks')
        try:
            pks = json.loads(pks)
        except Exception:
            return Response({"detail": "员工参数错误！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_user = request.user
            queryset = OAUser.objects
            if current_user.department.name != '董事会':
                if current_user.uid != current_user.department.leader.uid:
                    return Response({"detail": "您没有权限下载！"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    queryset = queryset.filter(department_id=current_user.department_id)
            queryset = queryset.filter(pk__in=pks)
            result = queryset.values('realname', 'email', 'department__name', 'date_joined', 'status')
            staff_df = pd.DataFrame(list(result))
            staff_df = staff_df.rename(columns={"realname": "姓名",
                                                "email": "邮箱",
                                                "department__name": "部门",
                                                "date_joined": "入职日期",
                                                "status": "状态"})
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                staff_df.to_excel(writer, sheet_name='员工信息', index=False)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="员工信息.xlsx"'
            return response
        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StaffUploadView(APIView):
    def post(self, request):
        serializer = StaffUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data.get('file')
            current_user = request.user
            if current_user.department.name != '董事会' or current_user.uid != current_user.department.leader.uid:
                return Response({"detail": "您没有权限上传！"}, status=status.HTTP_403_FORBIDDEN)

            # 读取 Excel（如果你已按扩展名选择 engine，这里保持你的实现）
            staff_df = pd.read_excel(file)
            # 新增：校验必须列是否存在
            required_cols = {'姓名', '邮箱', '部门'}
            if not required_cols.issubset(set(map(str, staff_df.columns))):
                return Response({"detail": "请检查文件中邮箱、姓名、部门列是否存在"}, status=status.HTTP_400_BAD_REQUEST)

            users = []
            for index, row in staff_df.iterrows():
                if current_user.department.name != '董事会':
                    department = current_user.department
                else:
                    try:
                        dept_name = str(row['部门']).strip()
                        department = OADepartment.objects.filter(name=dept_name).first()
                        if not department:
                            return Response({"detail": f"{dept_name}部门不存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    except Exception:
                        return Response({"detail": "部门列不存在"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    email = row['邮箱']
                    realname = row['姓名']
                    password = "111111"
                    user = OAUser(realname=realname, email=email, department=department,
                                  status=UserStatusChoices.UNACTIVE)
                    user.set_password(password)
                    users.append(user)
                except Exception:
                    return Response({"detail": "请检查文件中邮箱、姓名、部门列是否存在"},
                                    status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    OAUser.objects.bulk_create(users)
            except Exception:
                return Response({"detail": "员工数据添加错误！"}, status=status.HTTP_400_BAD_REQUEST)

            for user in users:
                send_active_email(request, user.email)
            return Response({"detail": "员工数据添加成功！"}, status=status.HTTP_201_CREATED)


        else:
            detail = list(serializer.errors.values())[0][0]
            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)


class TestCeleryView(APIView):
    def get(self, request):
        debug_task.delay()
        return Response({"detail": "成功！"})
