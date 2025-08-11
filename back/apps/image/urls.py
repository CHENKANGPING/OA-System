from django.urls import path
from .import views

app_name = 'image'

urlpatterns = [
    path('upload',views.UploadImageAPIView.as_view(),name='upload'),

]
