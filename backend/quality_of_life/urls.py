
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppealViewSet

router = DefaultRouter()
router.register(r'appeals', AppealViewSet)

urlpatterns = router.urls
