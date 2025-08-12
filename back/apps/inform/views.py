from django.db.models import Q, Prefetch
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Inform, InformRead
from .serializers import InformSerializer, ReadInformSerializer


class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer

    def get_queryset(self):
        # 如果多个条件的并查，那么就需要用到Q查询
        queryset = self.queryset.select_related('author').prefetch_related(
            Prefetch('reads', queryset=InformRead.objects.filter(user_id=self.request.user.uid)),
            "departments"
        ).filter(

            Q(public=True) | Q(departments=self.request.user.department) | Q(author=self.request.user)).distinct()
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.uid == request.user.uid:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # 修复：使用正确的字段名
        data['read_count'] = InformRead.objects.filter(inform=instance).count()
        return Response(data=data)


class ReadInformView(APIView):
    def post(self, request):
        serializer = ReadInformSerializer(data=request.data)
        if serializer.is_valid():
            inform_pk = serializer.validated_data.get('inform_pk')
            try:
                inform_obj = Inform.objects.get(pk=inform_pk)
                # 检查是否已经阅读过
                if InformRead.objects.filter(inform=inform_obj, user=request.user).exists():
                    return Response({"detail": "已经阅读过了"}, status=status.HTTP_200_OK)
                else:
                    # 创建阅读记录
                    InformRead.objects.create(inform=inform_obj, user=request.user)
                    return Response({"detail": "阅读记录成功"}, status=status.HTTP_201_CREATED)
            except Inform.DoesNotExist:
                return Response({"detail":"通知不存在！"},status=status.HTTP_404_NOT_FOUND)
            except Exception as e: 
                print(f"阅读记录创建失败: {e}")
                return Response({"detail":"阅读失败！"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'detail': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)
