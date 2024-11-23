import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import '../styles/Home.css';
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = 'pk.eyJ1IjoibnVydGFzIiwiYSI6ImNtM2Jzejd1ZTFpczkyanNjMms2djc3MG8ifQ.fNSvd6RJ_-bJo_NHsSLunQ';

function Home() {
    const mapContainer = useRef(null);
    const mapRef = useRef(null);
    const [selectedType, setSelectedType] = useState('all');
    const [isFullscreen, setIsFullscreen] = useState(false);

    const initialCenter = [76.885, 43.238];
    const initialZoom = 11;

    useEffect(() => {
        // Инициализация карты
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: initialCenter,
            zoom: initialZoom,
        });

        mapRef.current = map;

        map.on('load', () => {
            console.log("Карта загружена");

            // Загрузка данных из API
            fetchDataAndUpdateMap(map);
        });

        return () => map.remove();
    }, []);

    // Загрузка данных и обновление карты
    const fetchDataAndUpdateMap = (map) => {
        fetch('http://127.0.0.1:8000/api/hexagon-data/', {
            mode: 'cors'
        })
            .then(response => response.json())
            .then(data => {
                console.log("Данные хексов получены:", data);

                const layerId = 'hexagons-layer-fill';

                if (map.getLayer(layerId)) {
                    map.removeLayer(layerId);
                }
                if (map.getSource('hexagons-source')) {
                    map.removeSource('hexagons-source');
                }

                // Обновление источника или добавление нового
                const source = map.getSource('hexagons-source');
                if (source) {
                    source.setData(data); // Принудительно обновляем источник
                } else {
                    map.addSource('hexagons-source', {
                        type: 'geojson',
                        data: data,
                    });
                }

                map.addLayer({
                    id: 'hexagons-layer-fill',
                    type: 'fill',
                    source: 'hexagons-source',
                    paint: {
                        'fill-color': [
                            'case',
                            ['==', selectedType, 'all'],
                            [
                                'interpolate',
                                ['linear'],
                                ['get', 'total_requests'],
                                0, 'rgba(255,255,255,0.45)',
                                1, 'rgba(103,236,50,0.5)',
                                10, 'rgba(241, 194, 50,0.5)',
                                100, 'rgba(253,114,14,0.5)',
                                1000, 'rgba(243,2,2,0.5)'
                            ],
                            [
                                'interpolate',
                                ['linear'],
                                ['get', selectedType],
                                0, 'rgba(255,255,255,0.45)',
                                1, 'rgba(103,236,50,0.5)',
                                10, 'rgba(241, 194, 50,0.5)',
                                100, 'rgba(253,114,14,0.5)',
                                1000, 'rgba(243,2,2,0.5)'
                            ]
                        ],
                        'fill-opacity': 0.8,
                        'fill-outline-color': 'rgba(151, 161, 169, 0.6)',
                    },
                });

                // Удаление и добавление слоя границ
                if (map.getLayer('hexagons-layer-borders')) {
                    map.removeLayer('hexagons-layer-borders');
                }
                map.addLayer({
                    id: 'hexagons-layer-borders',
                    type: 'line',
                    source: 'hexagons-source',
                    paint: {
                        'line-color': '#101010',
                        'line-width': 1,
                    },
                });

                // Обработчик кликов по гексагону
                map.on('click', 'hexagons-layer-fill', (e) => {
                    const properties = e.features[0].properties;

                    // console.log('Данные для попапа:', properties); // Проверьте, совпадают ли данные

                    const popupContent = `
                        <strong>Hexagon ID: ${properties.hexagon_id}</strong><br>
                        Всего запросов: ${properties.total_requests || 0}<br>
                        Заявление: ${properties.appeals || 0}<br>
                        Жалобы: ${properties.complaints || 0}<br>
                        Запросы: ${properties.requests || 0}<br>
                        Предложения: ${properties.suggestions || 0}<br>
                        Отзывы: ${properties.responses || 0}<br>
                        Другие: ${properties.others || 0}<br>
                        Благодарности: ${properties.gratitudes || 0}<br>
                        Сообщения: ${properties.messages || 0}
                    `;

                    new mapboxgl.Popup()
                        .setLngLat(e.lngLat)
                        .setHTML(popupContent)
                        .addTo(map);

                    const [lng, lat] = e.features[0].geometry.coordinates[0][0];
                    map.flyTo({
                        center: [lng, lat],
                        zoom: 14,
                        speed: 1.5,
                        curve: 1,
                        essential: true,
                    });
                });
            })
            .catch(error => console.error("Ошибка загрузки данных хексов:", error));
    };

    // Обработчик выбора типа
    const handleTypeChange = (event) => {
        setSelectedType(event.target.value);

        // Принудительное обновление карты при изменении типа
        if (mapRef.current) {
            fetchDataAndUpdateMap(mapRef.current);
        }
    };

    const toggleFullscreen = () => {
        const mapContainerElement = mapContainer.current;

        if (!isFullscreen) {
            if (mapContainerElement.requestFullscreen) {
                mapContainerElement.requestFullscreen();
            } else if (mapContainerElement.webkitRequestFullscreen) {
                mapContainerElement.webkitRequestFullscreen();
            } else if (mapContainerElement.mozRequestFullScreen) {
                mapContainerElement.mozRequestFullScreen();
            } else if (mapContainerElement.msRequestFullscreen) {
                mapContainerElement.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }
        setIsFullscreen(!isFullscreen);
    };

    const resetMap = () => {
        if (mapRef.current) {
            mapRef.current.flyTo({ center: initialCenter, zoom: initialZoom });
        }
    };

    return (
        <div className={`home ${isFullscreen ? 'fullscreen' : ''}`}>
            <h1>Мониторинг качества жизни в районах Алматы</h1>
            <label htmlFor="request-type">Выберите тип запроса:</label>
            <select id="request-type" onChange={handleTypeChange}>
                <option value="all">Все</option>
                <option value="appeals">Заявление</option>ё
                <option value="complaints">Жалобы</option>
                <option value="requests">Запросы</option>
                <option value="suggestions">Предложения</option>
                <option value="responses">Отзывы</option>
                <option value="others">Другие</option>
                <option value="gratitudes">Благодарности</option>
                <option value="messages">Сообщения</option>
            </select>
            <div ref={mapContainer} className="home-map-container">
                <button className="fullscreen-btn" onClick={toggleFullscreen}>
                    {isFullscreen ? 'Обычный экран' : 'Во весь экран'}
                </button>
                <button className="reset-btn" onClick={resetMap}>Сброс</button>
            </div>
        </div>
    );
}

export default Home;
