from rest_framework import serializers
from django.contrib.auth import get_user_model


OAUser = get_user_model()

class AddStaffSerializer(serializers.Serializer):
    realname = serializers.CharField(max_length=20,error_messages={'required':'请输入用户名'})
    email = serializers.EmailField(error_messages={'required':'请输入邮箱','invalid':'请输入正确格式的邮箱'})
    password = serializers.CharField(max_length=20,error_messages={'required':'请输入密码'})

    def validate(self,attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        if OAUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('邮箱已存在')

        if request.user.department.leader.uid != request.user.uid:
            raise serializers.ValidationError('非部门leader不能添加员工')
        return attrs