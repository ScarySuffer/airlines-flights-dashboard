import React, { useState, useEffect } from 'react';
import '../styles/FlightsTable.css';

const FlightsTable = ({ data }) => {
  const [flights, setFlights] = useState(data);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [filterText, setFilterText] = useState('');

  useEffect(() => {
    let filteredData = data;

    if (filterText) {
      filteredData = data.filter(flight =>
        flight.airline.toLowerCase().includes(filterText.toLowerCase()) ||
        flight.source_city.toLowerCase().includes(filterText.toLowerCase()) ||
        flight.destination_city.toLowerCase().includes(filterText.toLowerCase())
      );
    }

    if (sortConfig.key) {
      filteredData = [...filteredData].sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }

    setFlights(filteredData);
  }, [data, sortConfig, filterText]);

  const requestSort = key => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIndicator = key => {
    if (sortConfig.key === key) {
      return sortConfig.direction === 'asc' ? ' ↑' : ' ↓';
    }
    return '';
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Filter by Airline, Source, or Destination"
        value={filterText}
        onChange={e => setFilterText(e.target.value)}
        style={{ marginBottom: '10px', padding: '5px', width: '300px' }}
      />
      <table border="1" cellPadding="8" cellSpacing="0" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {['airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class', 'duration', 'days_left', 'price'].map(key => (
              <th
                key={key}
                onClick={() => requestSort(key)}
                role="button"
                tabIndex={0}
                onKeyPress={e => { if (e.key === 'Enter') requestSort(key); }}
                style={{ cursor: 'pointer', userSelect: 'none' }}
              >
                {key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}{getSortIndicator(key)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {flights.map((flight, index) => (
            <tr key={index}>
              <td>{flight.airline}</td>
              <td>{flight.flight}</td>
              <td>{flight.source_city}</td>
              <td>{flight.departure_time}</td>
              <td>{flight.stops}</td>
              <td>{flight.arrival_time}</td>
              <td>{flight.destination_city}</td>
              <td>{flight.class}</td>
              <td>{flight.duration}</td>
              <td>{flight.days_left}</td>
              <td>{flight.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FlightsTable;
