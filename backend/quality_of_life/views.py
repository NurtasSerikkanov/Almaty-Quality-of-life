from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from .models import Appeal
from .serializers import AppealSerializer
from django.http import JsonResponse
from django.db import connection
import h3
import json

class AppealPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 500

class AppealViewSet(viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
    pagination_class = AppealPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'address']


def hexagon_data(request):
    with connection.cursor() as cursor:
        # Выполняем SQL-запрос для подсчета типов обращений по каждому hexagon_id
        cursor.execute("""
            SELECT 
                a.hexagon_id, 
                a.boundary_coords,
                SUM(CASE WHEN kind_of_appeal_id = 1 THEN 1 ELSE 0 END) AS appeals,
                SUM(CASE WHEN kind_of_appeal_id = 2 THEN 1 ELSE 0 END) AS requests,
                SUM(CASE WHEN kind_of_appeal_id = 3 THEN 1 ELSE 0 END) AS suggestions,
                SUM(CASE WHEN kind_of_appeal_id = 4 THEN 1 ELSE 0 END) AS responses,
                SUM(CASE WHEN kind_of_appeal_id = 5 THEN 1 ELSE 0 END) AS complaints,
                SUM(CASE WHEN kind_of_appeal_id = 6 THEN 1 ELSE 0 END) AS others,
                SUM(CASE WHEN kind_of_appeal_id = 7 THEN 1 ELSE 0 END) AS gratitudes,
                SUM(CASE WHEN kind_of_appeal_id = 8 THEN 1 ELSE 0 END) AS messages
            FROM appeals AS a
            LEFT JOIN additional_attributes AS aa ON a.id = aa.appeal_id
            WHERE boundary_coords IS NOT NULL
            GROUP BY a.hexagon_id, a.boundary_coords
        """)
        rows = cursor.fetchall()

    # Формирование GeoJSON-структуры с подсчетом типов обращений
    features = []
    for row in rows:
        (
            hexagon_id,
            boundary_coords,
            appeals_count,
            requests_count,
            suggestions_count,
            responses_count,
            complaints_count,
            others_count,
            gratitudes_count,
            messages_count
        ) = row
        boundary_coords_json = json.loads(boundary_coords)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [boundary_coords_json]
            },
            "properties": {
                "hexagon_id": hexagon_id,
                "total_requests": appeals_count + requests_count + suggestions_count +
                                  responses_count + complaints_count + others_count +
                                  gratitudes_count + messages_count,
                "appeals": appeals_count,
                "requests": requests_count,
                "suggestions": suggestions_count,
                "responses": responses_count,
                "complaints": complaints_count,
                "others": others_count,
                "gratitudes": gratitudes_count,
                "messages": messages_count
            },
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return JsonResponse(geojson)

