import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import '../styles/Home.css';
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = 'pk.eyJ1IjoibnVydGFzIiwiYSI6ImNtM2Jzejd1ZTFpczkyanNjMms2djc3MG8ifQ.fNSvd6RJ_-bJo_NHsSLunQ';

function Home() {
    const mapContainer = useRef(null);
    const mapRef = useRef(null);
    const [isFullscreen, setIsFullscreen] = useState(false);

<<<<<<< HEAD
    // Начальные координаты центра и зум
=======
>>>>>>> bc08205 (upd)
    const initialCenter = [76.885, 43.238];
    const initialZoom = 11;

    useEffect(() => {
        const map = new mapboxgl.Map({
            container: mapContainer.current,
<<<<<<< HEAD
            style: 'mapbox://styles/mapbox/streets-v11', // Новый стиль карты
=======
            style: 'mapbox://styles/mapbox/streets-v11',
>>>>>>> bc08205 (upd)
            center: initialCenter,
            zoom: initialZoom,
        });

        mapRef.current = map;

        map.on('load', () => {
            console.log("Карта загружена");

            fetch('http://127.0.0.1:8000/api/hexagon-data/', {
                mode: 'cors'
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Данные хексов получены:", data);

<<<<<<< HEAD
                    // Добавляем данные хексов в качестве источника
=======
>>>>>>> bc08205 (upd)
                    map.addSource('hexagons-source', {
                        type: 'geojson',
                        data: data,
                    });

<<<<<<< HEAD
                    // Добавляем слой заливки гексагонов с динамическим цветом на основе количества жалоб
=======
                    // Слой для заливки всех хексов, включая пустые
>>>>>>> bc08205 (upd)
                    map.addLayer({
                        id: 'hexagons-layer-fill',
                        type: 'fill',
                        source: 'hexagons-source',
                        paint: {
<<<<<<< HEAD
                            // Условие для цвета заливки в зависимости от количества жалоб
                            'fill-color': [
                                'interpolate',
                                ['linear'],
                                ['get', 'complaints'], // Количество жалоб
                                0, '#FFEDA0',   // минимальное значение — светлый цвет
                                30, '#FEB24C',  // среднее значение — более насыщенный цвет
                                100, '#F03B20'   // максимальное значение — самый насыщенный цвет
=======
                            'fill-color': [
                                'case',
                                ['>', ['get', 'total_requests'], 0],
                                [
                                    'interpolate',
                                    ['linear'],
                                    ['get', 'total_requests'],
                                    0, '#FFEDA0',   // Низкие значения
                                    30, '#FEB24C',  // Средние значения
                                    100, '#F03B20'  // Высокие значения
                                ],
                                '#f2f2f2' // Цвет для пустых хексов
>>>>>>> bc08205 (upd)
                            ],
                            'fill-opacity': 0.6,
                        },
                    });

<<<<<<< HEAD
                    // Добавляем слой границ гексагонов
=======
                    // Слой для границ хексов
>>>>>>> bc08205 (upd)
                    map.addLayer({
                        id: 'hexagons-layer-borders',
                        type: 'line',
                        source: 'hexagons-source',
                        paint: {
                            'line-color': '#FF8C00',
                            'line-width': 1,
                        },
                    });

<<<<<<< HEAD
                    // Добавляем обработчик кликов по гексагону
                    map.on('click', 'hexagons-layer-fill', (e) => {
                        const properties = e.features[0].properties;

                        // Формируем содержимое всплывающего окна
                        const popupContent = `
                            <strong>Hexagon ID: ${properties.hexagon_id}</strong><br>
=======
                    // Обработчик клика на хекс
                    map.on('click', 'hexagons-layer-fill', (e) => {
                        const properties = e.features[0].properties;

                        const popupContent = `
                            <strong>Hexagon ID: ${properties.hexagon_id}</strong><br>
                            Всего запросов: ${properties.total_requests || 0}<br>
>>>>>>> bc08205 (upd)
                            Жалобы: ${properties.complaints || 0}<br>
                            Запросы: ${properties.requests || 0}<br>
                            Предложения: ${properties.suggestions || 0}<br>
                            Отзывы: ${properties.responses || 0}<br>
                            Другие: ${properties.others || 0}<br>
                            Благодарности: ${properties.gratitudes || 0}<br>
                            Сообщения: ${properties.messages || 0}
                        `;

<<<<<<< HEAD
                        // Показ всплывающего окна
=======
>>>>>>> bc08205 (upd)
                        new mapboxgl.Popup()
                            .setLngLat(e.lngLat)
                            .setHTML(popupContent)
                            .addTo(map);
<<<<<<< HEAD

                        // Автоматическое приближение к хексагону
                        const coordinates = e.features[0].geometry.coordinates[0][0];
                        map.flyTo({
                            center: coordinates,
                            zoom: 14, // Уровень зума для приближения
                        });
                    });

                    // Изменяем курсор при наведении на гексагон
=======
                    });

                    // Изменяем курсор при наведении на хекс
>>>>>>> bc08205 (upd)
                    map.on('mouseenter', 'hexagons-layer-fill', () => {
                        map.getCanvas().style.cursor = 'pointer';
                    });

                    map.on('mouseleave', 'hexagons-layer-fill', () => {
                        map.getCanvas().style.cursor = '';
                    });
                })
                .catch(error => console.error("Ошибка загрузки данных хексов:", error));
        });

        return () => map.remove();
    }, []);

    const toggleFullscreen = () => {
        setIsFullscreen(!isFullscreen);
    };

<<<<<<< HEAD
    // Функция для сброса карты к начальному масштабу и центру
=======
>>>>>>> bc08205 (upd)
    const resetMap = () => {
        if (mapRef.current) {
            mapRef.current.flyTo({ center: initialCenter, zoom: initialZoom });
        }
    };

    return (
        <div className={`home ${isFullscreen ? 'fullscreen' : ''}`}>
            <h1>Мониторинг качества жизни в районах Алматы</h1>
            <div ref={mapContainer} className="home-map-container"></div>
            <button className="fullscreen-btn" onClick={toggleFullscreen}>
                {isFullscreen ? 'Обычный экран' : 'Во весь экран'}
            </button>
            <button className="reset-btn" onClick={resetMap}>Сброс</button>
        </div>
    );
}

export default Home;
