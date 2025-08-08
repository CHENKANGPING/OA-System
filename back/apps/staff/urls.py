from django.urls import path

from apps.staff.views import DepartmentListView

app_name = 'staff'

urlpatterns = [
    path('departments', DepartmentListView.as_view(), name='departments'),
]