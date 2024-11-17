import psycopg2
import h3.api.basic_str as h3
import json
from shapely.geometry import Polygon, shape, Point
import geopandas as gpd

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="openalmaty",
    user="postgres",
    password="t$hZw!Kz",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Очистка существующих данных
cur.execute("""
    UPDATE appeals
    SET hexagon_id = NULL, boundary_coords = NULL
""")
conn.commit()
print("Старые данные hexagon_id и boundary_coords очищены.")

# Загрузка границ города из GeoJSON
boundary = gpd.read_file("export.geojson")  # Укажите путь к вашему файлу с границами города
city_boundary = boundary.unary_union  # Объединяем в одну границу, если их несколько

# Параметры для создания сетки хексов
center_lat, center_lon = 43.238949, 76.889709  # Координаты центра Алматы
resolution = 8  # Разрешение хексов
k_ring_radius = 15  # Радиус генерации хексов вокруг центра

# Генерация сетки хексов с использованием H3
center_hex = h3.latlng_to_cell(center_lat, center_lon, resolution)
hexagons = list(h3.grid_disk(center_hex, k_ring_radius))

# Фильтрация хексов, выходящих за границы города
filtered_hexagons = []
for hex_id in hexagons:
    # Получаем координаты границ хексагона
    boundary_coords = h3.cell_to_boundary(hex_id)  # Убираем geo_json
    boundary_coords = [(lng, lat) for lat, lng in boundary_coords]  # Преобразуем в формат GeoJSON-like
    hex_polygon = Polygon(boundary_coords)

    # Проверяем пересечение с границами города
    if city_boundary.contains(hex_polygon.centroid) or city_boundary.intersects(hex_polygon):
        filtered_hexagons.append((hex_id, boundary_coords))

print(f"Количество хексов внутри границ: {len(filtered_hexagons)}")

# Сохранение хексов в базу данных
for hex_id, boundary_coords in filtered_hexagons:
    boundary_coords_geojson = [[lng, lat] for lng, lat in boundary_coords]

    # Добавляем первую точку в конец списка, чтобы замкнуть полигон
    if boundary_coords_geojson[0] != boundary_coords_geojson[-1]:
        boundary_coords_geojson.append(boundary_coords_geojson[0])

    # Формируем строку координат в формате POLYGON
    polygon_wkt = f"POLYGON(({', '.join([f'{lng} {lat}' for lng, lat in boundary_coords_geojson])}))"

    # Обновляем записи в таблице appeals для записей, попадающих в данный хекс
    cur.execute("""
        UPDATE appeals
        SET hexagon_id = %s, boundary_coords = %s
        WHERE ST_Contains(
            ST_SetSRID(ST_GeomFromText(%s), 4326), 
            location
        )
    """, (hex_id, json.dumps(boundary_coords_geojson), polygon_wkt))

conn.commit()

# Закрытие соединения
cur.close()
conn.close()

print("Хексы успешно сохранены в базе данных.")
