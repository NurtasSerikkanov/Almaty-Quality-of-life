import psycopg2
import h3.api.basic_str as h3
import json

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="openalmaty",
    user="postgres",
    password="t$hZw!Kz",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Шаг 1: Очистка существующих данных в колонках
cur.execute("""
    UPDATE appeals
    SET hexagon_id = NULL, boundary_coords = NULL
""")
conn.commit()
print("Старые данные hexagon_id и boundary_coords очищены.")

# Параметры для создания сетки хексов
center_lat, center_lon = 43.238949, 76.889709  # Координаты центра Алматы
resolution = 8  # Разрешение хексов
k_ring_radius = 15  # Увеличиваем радиус сетки, чтобы охватить весь город

# Создаем центральный хекс и сетку вокруг него
center_hex = h3.latlng_to_cell(center_lat, center_lon, resolution)
hexagons = list(h3.grid_disk(center_hex, k_ring_radius))

# Шаг 2: Сохранение новой сетки хексов в таблицу appeals
for hex_id in hexagons:
    # Получаем координаты границ для хексагона
    boundary_coords = h3.cell_to_boundary(hex_id)
    # Преобразуем координаты в формат GeoJSON: [долгота, широта]
    boundary_coords_geojson = [[lng, lat] for lat, lng in boundary_coords]

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

print("Новые данные hexagon_id и boundary_coords успешно сохранены.")