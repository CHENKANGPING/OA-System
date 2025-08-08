from rest_framework.routers import DefaultRouter
from . import views

app_name = 'inform'

router = DefaultRouter(trailing_slash=False)
router.register('inform',views.InformViewSet,basename='inform')

urlpatterns = [] +router.urls

