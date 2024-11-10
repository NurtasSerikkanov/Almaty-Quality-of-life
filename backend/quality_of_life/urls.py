from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppealViewSet

router = DefaultRouter()
router.register(r'appeals', AppealViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Включаем все маршруты роутера
]
