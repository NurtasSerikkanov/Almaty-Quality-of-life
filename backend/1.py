import json
from shapely.geometry import shape

# Загрузите данные из GeoJSON файла
with open("/Users/nurtasserikkanov/Desktop/export.geojson", "r") as f:
    geojson_data = json.load(f)

# Преобразуем в объект Shapely и затем в WKT
almaty_shape = shape(geojson_data["features"][0]["geometry"])
almaty_wkt = almaty_shape.wkt

# Сохраняем данные WKT в файл
with open("almaty_boundary.wkt", "w") as wkt_file:
    wkt_file.write(almaty_wkt)

print("Граница Алматы в формате WKT сохранена в файл almaty_boundary.wkt")
