import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import '../styles/Appeals.css';

function Appeals() {
    const [appeals, setAppeals] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [limit, setLimit] = useState(100);

    const fetchAppeals = useCallback(() => {
        axios.get(`http://127.0.0.1:8000/api/appeals/?search=${searchTerm}&limit=${limit}`)
            .then(response => {
                console.log("Ответ от бэкенда:", response.data);
                setAppeals(response.data.results || response.data);
            })
            .catch(error => {
                console.error("Ошибка при получении данных жалоб:", error);
            });
    }, [searchTerm, limit]);

    useEffect(() => {
        fetchAppeals();
    }, [fetchAppeals]);

    const handleSearchChange = (e) => {
        setSearchTerm(e.target.value);
    };

    const handleLimitChange = (e) => {
        setLimit(Number(e.target.value));
    };

    return (
        <div className="appeals">
            <h1>Все жалобы</h1>
            <div className="controls">
                <input
                    type="text"
                    placeholder="Поиск..."
                    value={searchTerm}
                    onChange={handleSearchChange}
                />
                <select onChange={handleLimitChange} value={limit}>
                    <option value={100}>100</option>
                    <option value={200}>200</option>
                    <option value={500}>500</option>
                </select>
            </div>
            <table className="appeals-table">
                <thead>
                <tr>
                    <th>Заголовок</th>
                    <th>Описание</th>
                    <th>Дата создания</th>
                    <th>Статус</th>
                    <th>Адрес</th>
                </tr>
                </thead>
                <tbody>
                {appeals.length > 0 ? (
                    appeals.map((appeal) => (
                        <tr key={appeal.id}>
                            <td>{appeal.title}</td>
                            <td>{appeal.description}</td>
                            <td>{new Date(appeal.creation_date).toLocaleDateString()}</td>
                            <td>{appeal.status}</td>
                            <td>{appeal.address}</td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="5">Данные отсутствуют</td>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
    );
}

export default Appeals;
