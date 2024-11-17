import React from 'react';
import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom';
import Home from './components/Home';
import Analytics from './components/Analytics';
import About from './components/About';
import Appeals from './components/Appeals';
import './App.css';

function App() {
  return (
      <Router>
        <div className="app">
          <nav className="sidebar">
            <h2>Анализ городской среды</h2>
            <NavLink to="/" className="nav-link">Главная</NavLink>
            <NavLink to="/analytics" className="nav-link">Аналитика</NavLink>
            <NavLink to="/appeals" className="nav-link">Все запросы</NavLink>  {/* Новый пункт меню */}
            <NavLink to="/about" className="nav-link">О проекте</NavLink>
          </nav>
          <main className="content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/appeals" element={<Appeals />} />  {/* Новый маршрут */}
              <Route path="/about" element={<About />} />
            </Routes>
          </main>
        </div>
      </Router>
  );
}

export default App;