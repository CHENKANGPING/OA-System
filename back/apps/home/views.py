from rest_framework.views import APIView
from apps.inform.models import Inform, InformRead
from django.db.models import Q
from django.db.models import Prefetch
from apps.inform.serializers import InformSerializer

class LatestInformView(APIView):
    def get(self, request):
        Inform.objects.prefetch_related(Prefetch("reads",queryset=InformRead.objects.filter(user_id=self.current_user.uid)),'departments').filter(Q(public=True))| Q(departments=current_user.department)



class LatestAbsentView(APIView):
    def get(self, request):
        pass


class DepartmentStaffCountView(APIView):
    def get(self, request):
        pass