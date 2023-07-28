from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PackDataViewSet

app_name = 'core'

router = DefaultRouter()
router.register(r'packs', PackDataViewSet, basename="pack")

urlpatterns = [
    path('', include(router.urls)),
]
