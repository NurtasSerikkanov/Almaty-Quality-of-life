import React, { useEffect, useState, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import { Bar } from 'react-chartjs-2';
import '../styles/Analytics.css';
import 'mapbox-gl/dist/mapbox-gl.css';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

mapboxgl.accessToken = 'pk.eyJ1IjoibnVydGFzIiwiYSI6ImNtM2Jzejd1ZTFpczkyanNjMms2djc3MG8ifQ.fNSvd6RJ_-bJo_NHsSLunQ';

function Analytics() {
  const mapContainer = useRef(null);
  const mapRef = useRef(null);

  const [year, setYear] = useState('all');
  const [month, setMonth] = useState('all');
  const [type, setType] = useState('total_requests');
  const [districtsData, setDistrictsData] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const initialCenter = [76.885, 43.238];
  const initialZoom = 11;

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: initialCenter,
      zoom: initialZoom,
    });

    mapRef.current = map;

    map.on('load', () => {
      fetchDataAndRenderMap();

      map.on('click', 'districts-layer-fill', (e) => {
        const properties = e.features[0].properties;

        const popupContent = `
          <strong>${properties.district_name}</strong><br>
          Всего запросов: ${properties.total_requests || 0}<br>
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
      });
    });

    return () => map.remove();
  }, []);

  const fetchDataAndRenderMap = () => {
    const queryParams = new URLSearchParams();
    if (year !== 'all') queryParams.append('year', year);
    if (month !== 'all') queryParams.append('month', month);

    fetch(`http://127.0.0.1:8000/api/district-data/?${queryParams.toString()}`)
        .then((response) => response.json())
        .then((data) => {
          setDistrictsData(data);
          updateChartData(data);

          if (mapRef.current.getSource('districts-source')) {
            mapRef.current.getSource('districts-source').setData(data);
          } else {
            mapRef.current.addSource('districts-source', {
              type: 'geojson',
              data: data,
            });

            mapRef.current.addLayer({
              id: 'districts-layer-fill',
              type: 'fill',
              source: 'districts-source',
              paint: {
                'fill-color': [
                  'interpolate',
                  ['linear'],
                  ['get', type],
                  0, 'rgba(255,255,255,0.45)',
                  1, 'rgba(103,236,50,0.5)',
                  10, 'rgba(241, 194, 50,0.5)',
                  100, 'rgba(253,114,14,0.5)',
                  1000, 'rgba(243,2,2,0.5)',
                ],
                'fill-outline-color': 'rgba(151, 161, 169, 0.6)',
                'fill-opacity': 0.8,
              },
            });

            mapRef.current.addLayer({
              id: 'districts-layer-borders',
              type: 'line',
              source: 'districts-source',
              paint: {
                'line-color': '#333',
                'line-width': 1,
              },
            });
          }
        })
        .catch((error) => console.error('Ошибка загрузки данных районов:', error));
  };

  const updateChartData = (data) => {
    if (!data || !data.features) return;

    const labels = data.features.map((feature) => feature.properties.district_name);
    const values = data.features.map((feature) => feature.properties[type]);

    setChartData({
      labels,
      datasets: [
        {
          label: 'Количество запросов',
          data: values,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    });
  };

  const applyFilters = () => {
    fetchDataAndRenderMap();
  };

  const toggleFullscreen = () => {
    const mapContainerElement = mapContainer.current;

    if (!isFullscreen) {
      if (mapContainerElement.requestFullscreen) {
        mapContainerElement.requestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
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
      <div className="analytics">
        <h1>Аналитика по районам</h1>

        <div className="filters">
          <select value={year} onChange={(e) => setYear(e.target.value)}>
            <option value="all">Все годы</option>
            <option value="2017">2017</option>
            <option value="2018">2018</option>
            <option value="2019">2019</option>
            <option value="2020">2020</option>
            <option value="2021">2021</option>
            <option value="2022">2022</option>
            <option value="2023">2023</option>
            <option value="2024">2024</option>
          </select>

          <select value={month} onChange={(e) => setMonth(e.target.value)}>
            <option value="all">Все месяцы</option>
            <option value="1">Январь</option>
            <option value="2">Февраль</option>
            <option value="3">Март</option>
            <option value="4">Апрель</option>
            <option value="5">Май</option>
            <option value="6">Июнь</option>
            <option value="7">Июль</option>
            <option value="8">Август</option>
            <option value="9">Сентябрь</option>
            <option value="10">Октябрь</option>
            <option value="11">Ноябрь</option>
            <option value="12">Декабрь</option>
          </select>

          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="total_requests">Все запросы</option>
            <option value="complaints">Жалобы</option>
            <option value="requests">Запросы</option>
            <option value="suggestions">Предложения</option>
            <option value="responses">Отзывы</option>
            <option value="others">Другие</option>
            <option value="gratitudes">Благодарности</option>
          </select>

          <button onClick={applyFilters}>Применить фильтры</button>
        </div>

        <div ref={mapContainer} className="map-container">
          <button className="fullscreen-btn" onClick={toggleFullscreen}>
            {isFullscreen ? 'Обычный экран' : 'Во весь экран'}
          </button>
          <button className="reset-btn" onClick={resetMap}>Сброс</button>
        </div>

        <div className="chart-container">
          {chartData ? (
              <Bar
                  key={type}
                  data={chartData}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: { display: true },
                      title: { display: true, text: 'Анализ запросов по районам' },
                    },
                    scales: { y: { beginAtZero: true } },
                  }}
              />
          ) : (
              <p>Загрузка данных для графика...</p>
          )}
        </div>
      </div>
  );
}

export default Analytics;
