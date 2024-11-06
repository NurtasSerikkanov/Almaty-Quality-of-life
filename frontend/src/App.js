import React from 'react';
import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom';
import Home from './components/Home';
import Analytics from './components/Analytics';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <h2>Анализ городской среды</h2>
          <NavLink to="/" className="nav-link">Главная</NavLink>
          <NavLink to="/analytics" className="nav-link">Аналитика</NavLink>
          <NavLink to="/about" className="nav-link">О проекте</NavLink>
        </nav>
        <main className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analytics" element={<Analytics />} />
            {/* Здесь можно добавить другие страницы */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;