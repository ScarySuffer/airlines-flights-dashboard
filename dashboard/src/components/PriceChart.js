import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Dummy sample data, replace with real data later
const data = [
  { day: 'Mon', price: 4000 },
  { day: 'Tue', price: 3000 },
  { day: 'Wed', price: 2000 },
  { day: 'Thu', price: 2780 },
  { day: 'Fri', price: 1890 },
  { day: 'Sat', price: 2390 },
  { day: 'Sun', price: 3490 },
];

function PriceChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="day" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default PriceChart;
