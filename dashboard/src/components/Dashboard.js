import React, { useState, useEffect } from 'react';
import FlightsTable from './FlightsTable';
import AvgDurationChart from './AvgDurationChart';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const [flightsData, setFlightsData] = useState([]);

  useEffect(() => {
    fetch('/data/flights.json')
      .then(res => res.json())
      .then(data => setFlightsData(data))
      .catch(err => console.error('Failed to load flights data', err));
  }, []);

  return (
    <div className="dashboard-container">
      <h1>Flights Dashboard</h1>
      {/* Show FlightsTable only if data loaded */}
      {flightsData.length > 0 ? (
        <>
          <FlightsTable data={flightsData} />
          <h2>Average Flight Duration per Airline</h2>
          <AvgDurationChart data={flightsData} />
        </>
      ) : (
        <p>Loading flight data...</p>
      )}
    </div>
  );
};

export default Dashboard;
