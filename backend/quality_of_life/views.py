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
        # Получение всех уникальных hexagon_id
        cursor.execute("""
            SELECT DISTINCT hexagon_id, boundary_coords 
            FROM appeals 
            WHERE boundary_coords IS NOT NULL
        """)
        all_hexes = cursor.fetchall()

        # Подсчёт обращений по типам
        cursor.execute("""
            SELECT 
                a.hexagon_id,
                COUNT(*) AS total_requests,
                SUM(CASE WHEN aa.kind_of_appeal_id = 1 THEN 1 ELSE 0 END) AS appeals,
                SUM(CASE WHEN aa.kind_of_appeal_id = 2 THEN 1 ELSE 0 END) AS requests,
                SUM(CASE WHEN aa.kind_of_appeal_id = 3 THEN 1 ELSE 0 END) AS suggestions,
                SUM(CASE WHEN aa.kind_of_appeal_id = 4 THEN 1 ELSE 0 END) AS responses,
                SUM(CASE WHEN aa.kind_of_appeal_id = 5 THEN 1 ELSE 0 END) AS complaints,
                SUM(CASE WHEN aa.kind_of_appeal_id = 6 THEN 1 ELSE 0 END) AS others,
                SUM(CASE WHEN aa.kind_of_appeal_id = 7 THEN 1 ELSE 0 END) AS gratitudes,
                SUM(CASE WHEN aa.kind_of_appeal_id = 8 THEN 1 ELSE 0 END) AS messages
            FROM appeals AS a
            LEFT JOIN additional_attributes AS aa ON a.id = aa.appeal_id
            GROUP BY a.hexagon_id;
        """)
        rows = cursor.fetchall()

    # Создаём карту хексов с данными
    data_map = {row[0]: row[1:] for row in rows}

    # Формируем GeoJSON
    features = []
    for hex_id, boundary_coords in all_hexes:
        boundary_coords_json = json.loads(boundary_coords)

        if hex_id in data_map:
            # Данные существуют
            (
                total_requests,
                appeals_count,
                requests_count,
                suggestions_count,
                responses_count,
                complaints_count,
                others_count,
                gratitudes_count,
                messages_count
            ) = data_map[hex_id]
        else:
            # Пустой хекс
            total_requests = 0
            appeals_count = 0
            requests_count = 0
            suggestions_count = 0
            responses_count = 0
            complaints_count = 0
            others_count = 0
            gratitudes_count = 0
            messages_count = 0

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [boundary_coords_json]
            },
            "properties": {
                "hexagon_id": hex_id,
                "total_requests": total_requests,
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


def district_data(request):
    """
    Эндпоинт для данных о районах с поддержкой фильтрации по годам и месяцам.
    """
    year = request.GET.get('year')
    month = request.GET.get('month')

    query = """
        SELECT
            district_name,
            ST_AsGeoJSON(district_boundary) AS boundary,
            COUNT(*) AS total_requests,
            SUM(CASE WHEN aa.kind_of_appeal_id = 1 THEN 1 ELSE 0 END) AS complaints,
            SUM(CASE WHEN aa.kind_of_appeal_id = 7 THEN 1 ELSE 0 END) AS gratitudes,
            SUM(CASE WHEN aa.kind_of_appeal_id = 2 THEN 1 ELSE 0 END) AS requests,
            SUM(CASE WHEN aa.kind_of_appeal_id = 3 THEN 1 ELSE 0 END) AS suggestions,
            SUM(CASE WHEN aa.kind_of_appeal_id = 4 THEN 1 ELSE 0 END) AS responses
        FROM appeals AS a
        LEFT JOIN additional_attributes AS aa ON a.id = aa.appeal_id
        WHERE district_boundary IS NOT NULL
    """

    # Фильтры по year и month
    if year:
        query += f" AND EXTRACT(YEAR FROM a.creation_date) = {year}"
    if month:
        query += f" AND EXTRACT(MONTH FROM a.creation_date) = {month}"

    query += " GROUP BY district_name, district_boundary"

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Формирование GeoJSON
    features = []
    for row in rows:
        (
            district_name,
            boundary_geojson,
            total_requests,
            complaints,
            gratitudes,
            requests,
            suggestions,
            responses
        ) = row

        boundary_coords = json.loads(boundary_geojson)

        feature = {
            "type": "Feature",
            "geometry": boundary_coords,
            "properties": {
                "district_name": district_name,
                "total_requests": total_requests,
                "complaints": complaints,
                "gratitudes": gratitudes,
                "requests": requests,
                "suggestions": suggestions,
                "responses": responses
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return JsonResponse(geojson)