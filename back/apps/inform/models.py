from apps.oaauth.models import OAUser,OADepartment
from django.db import models

# Create your models here.
class Inform(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    # 如果前端上传的departments中包含了0 比如[0] 那么就认为这个通知时所有部门可见
    public = models.BooleanField(default=False)
    author = models.ForeignKey(OAUser, on_delete=models.CASCADE,related_name='informs',related_query_name='informs')
    # departments：序列化的时候用，前端上传部门id 我们通过department_ids来获取
    departments = models.ManyToManyField(OADepartment,related_name='informs',related_query_name='informs')

    class Meta:
        ordering = ['-create_time']


class InformRead(models.Model):
    inform = models.ForeignKey(Inform,on_delete=models.CASCADE,related_name='reads',related_query_name='reads')
    user = models.ForeignKey(OAUser,on_delete=models.CASCADE,related_name='reads',related_query_name='reads')
    read_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # infrom 和 user 组合的数据，必须是唯一的
        unique_together = ('inform', 'user')