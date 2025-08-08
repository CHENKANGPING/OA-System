from rest_framework import serializers

from apps.inform.models import Inform
from apps.oaauth.models import OADepartment
from apps.oaauth.serializers import UserSerializer, DepartmentSerializer


class InformSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    # department_ids： 是一个包含了部门的id列表
    department_ids = serializers.ListField(write_only=True)

    class Meta:
        model = Inform
        fields = '__all__'
        read_only_fields = ('public',)

    # 重写保存Inform对象的create方法
    def create(self, validated_data):
        request = self.context["request"]
        department_ids = validated_data.pop('department_ids')
        # def toint(value):
        #     return int(value)
        department_ids = list(map(lambda value: int(value), department_ids))
        if 0 in department_ids:
            inform = Inform.objects.create(public=True, author=request.user, **validated_data)
        else:
            departments = OADepartment.objects.filter(id__in=department_ids).all()
            inform = Inform.objects.create(public=False, author=request.user, **validated_data)
            inform.departments.set(departments)
            inform.save()
        return inform

