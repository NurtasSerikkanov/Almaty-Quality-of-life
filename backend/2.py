import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import numpy as np

# Загрузите границу города Алматы (ваш файл с границей в GeoJSON или WKT)
boundary = gpd.read_file("export.geojson")  # Замените на ваш файл

# Получение границ как объекта Polygon
city_boundary = boundary.unary_union  # Если в GeoJSON несколько полигонов

# Установите параметры для размера хексагонов
hex_size = 0.005  # Уменьшаем размер стороны шестиугольника

# Функция для генерации сетки хексагонов
def create_hex_grid(polygon, hex_size):
    minx, miny, maxx, maxy = polygon.bounds
    x_start = minx
    y_start = miny
    x_end = maxx
    y_end = maxy
    width = 2 * hex_size
    height = 3 ** 0.5 * hex_size

    x_offsets = np.arange(x_start, x_end + width, width * 0.75)
    y_offsets = np.arange(y_start, y_end + height, height)

    hexagons = []
    for x in x_offsets:
        for i, y in enumerate(y_offsets):
            # Сдвиг для четных рядов
            x_offset = x + (0.5 * width if i % 2 else 0)
            hexagon = Polygon([
                (x_offset + hex_size * np.cos(angle), y + hex_size * np.sin(angle))
                for angle in np.linspace(0, 2 * np.pi, 7)
            ])
            # Проверяем пересечение с границей
            if polygon.contains(hexagon.centroid):  # Проверка на попадание центра внутрь границы
                hexagons.append(hexagon)

    return gpd.GeoDataFrame({'geometry': hexagons})

# Генерация сетки хексов
hex_grid = create_hex_grid(city_boundary, hex_size)

# Визуализация
fig, ax = plt.subplots(figsize=(10, 10))
boundary.plot(ax=ax, color='none', edgecolor='red', linewidth=1)
hex_grid.plot(ax=ax, color='blue', edgecolor='white', alpha=0.7)
plt.show()

# Сохранение хексагонов в файл GeoJSON (по необходимости)
hex_grid.to_file("dense_hexagons.geojson", driver="GeoJSON")
