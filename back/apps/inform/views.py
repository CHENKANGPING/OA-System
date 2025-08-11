from rest_framework import viewsets
from .models import Inform
from .serializers import InformSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer
    
    def get_queryset(self):
        # 如果多个条件的并查，那么就需要用到Q查询
        queryset =  self.queryset.select_related('author') . prefetch_related("reads","departments").filter(Q(public = True) | Q(departments = self.request.user.department) | Q(author = self.request.user)).distinct()
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.uid == request.user.uid:
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)