import React from 'react';
import '../styles/Home.css';

function Home(){
    return (
        <div className='home'>
            <h1>Мониторинг качества жизни в районах Алматы</h1>
            <div className='map-placeholder'> [Карта будет здесь]</div>
            <div className='statistics'>
                <p>Общее количество жалоб:</p>
                <p>Количество благодарностей:</p>
                <p>Запросы и обращения:</p>
                <p>Количество заявлений:</p>
            </div>
        </div>
    );
}

export default Home;