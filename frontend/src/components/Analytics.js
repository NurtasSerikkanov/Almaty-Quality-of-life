import React, { useState } from 'react';
import '../styles/Analytics.css';
// import { Bar } from 'react-chartjs-2';

function Analytics() {
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [type, setType] = useState('');

  // const data = {
  //   labels: ['Район 1', 'Район 2', 'Район 3', 'Район 4'],
  //   datasets: [
  //     {
  //       label: 'Количество',
  //       data: [12, 19, 3, 5],
  //       backgroundColor: '#4f6475'
  //     }
  //   ]
  // };

  const handleFilterChange = () => {

  };

  return (
      <div className="analytics">
        <h1>Аналитика по районам</h1>

        <div className="filters">
          <select value={year} onChange={(e) => setYear(e.target.value)}>
            <option value="">Выберите год</option>
            <option value="2022">2022</option>
            <option value="2023">2023</option>
          </select>

          <select value={month} onChange={(e) => setMonth(e.target.value)}>
            <option value="">Выберите месяц</option>
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
            <option value="">Выберите тип</option>
            <option value="запрос">Запрос</option>
            <option value="заявление">Заявление</option>
            <option value="жалоба">Жалоба</option>
            <option value="благодарность">Благодарность</option>
          </select>

          <button onClick={handleFilterChange}>Применить фильтры</button>
        </div>

        <div className="map-placeholder">[Карта будет здесь]</div>

        {/* <div className="chart">
        {data && data.datasets && data.datasets[0].data ? (
          <Bar data={data} options={{ responsive: true, maintainAspectRatio: false }} />
        ) : (
          <p>Загрузка данных...</p>
        )}
      </div> */}
      </div>
  );
}

export default Analytics;