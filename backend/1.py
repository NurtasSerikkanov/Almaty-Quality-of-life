import psycopg2
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="openalmaty",
    user="postgres",
    password="t$hZw!Kz",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Загрузка GeoJSON с районами города
districts = gpd.read_file("district.geojson")
districts = districts.to_crs(epsg=4326)

# Очистка существующих данных
cur.execute("""
    UPDATE appeals
    SET district_name = NULL, district_boundary = NULL
""")
conn.commit()
print("Старые данные district_name и district_boundary очищены.")

# Перебираем районы и обновляем записи
for _, district in districts.iterrows():
    district_name = district["name"]  # Название района
    district_geometry = district["geometry"]  # Геометрия района

    # Преобразование MultiPolygon в Polygon
    if isinstance(district_geometry, MultiPolygon):
        district_geometry = list(district_geometry.geoms)[0]  # Берём первый полигон

    # Преобразуем геометрию района в формат WKT
    district_wkt = district_geometry.wkt

    # Обновляем записи в таблице appeals, которые находятся внутри данного района
    cur.execute("""
        UPDATE appeals
        SET district_name = %s, district_boundary = ST_SetSRID(ST_GeomFromText(%s), 4326)
        WHERE ST_Contains(ST_SetSRID(ST_GeomFromText(%s), 4326), location)
    """, (
        district_name,
        district_wkt,
        district_wkt
    ))
    print(f"Обновлены точки для района: {district_name}")

conn.commit()
print("Данные успешно обновлены!")

# Закрытие соединения
cur.close()
conn.close()
