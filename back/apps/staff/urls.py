from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter




app_name = 'staff'
router = DefaultRouter(trailing_slash=False)
router.register(r'staff', views.StaffViewSet, basename='staff')

urlpatterns = [
    path('departments', views.DepartmentListView.as_view(), name='departments'),
    # path('staff', views.StaffView.as_view(), name='staff_views'),
    path('active', views.ActiveStaffView.as_view(), name='active'),
    path('download', views.SraffDownloadView.as_view(), name='download'),
    path('upload', views.StaffUploadView.as_view(), name='upload'),


    path('test/celery', views.TestCeleryView.as_view(), name='test_celery'),

] + router.urls