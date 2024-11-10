from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from .models import Appeal
from .serializers import AppealSerializer

class AppealPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 500

class AppealViewSet(viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
    pagination_class = AppealPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'address']
