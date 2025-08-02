import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer,
} from 'recharts';

const AvgDurationChart = ({ data }) => {
  // Calculate average duration per airline
  const avgDurationData = Object.entries(
    data.reduce((acc, flight) => {
      if (!acc[flight.airline]) acc[flight.airline] = { total: 0, count: 0 };
      acc[flight.airline].total += flight.duration;
      acc[flight.airline].count += 1;
      return acc;
    }, {})
  ).map(([airline, { total, count }]) => ({
    airline,
    avgDuration: parseFloat((total / count).toFixed(2)),
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        data={avgDurationData}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="airline" />
        <YAxis label={{ value: 'Avg Duration (hrs)', angle: -90, position: 'insideLeft' }} />
        <Tooltip />
        <Bar dataKey="avgDuration" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default AvgDurationChart;
