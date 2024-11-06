from rest_framework import viewsets
from .models import Appeal
from .serializers import AppealSerializer

class AppealViewSet(viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
