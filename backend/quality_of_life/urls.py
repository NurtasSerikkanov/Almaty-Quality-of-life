from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppealViewSet, hexagon_data

router = DefaultRouter()
router.register(r'appeals', AppealViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hexagon-data/', hexagon_data, name='hexagon_data'),
]
