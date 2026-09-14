import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

// Dummy data for the MVP Demo
const data = [
  { day: 'Mon', target: 4000, predicted: 4100 },
  { day: 'Tue', target: 4000, predicted: 3950 },
  { day: 'Wed', target: 4000, predicted: 4200 },
  { day: 'Thu', target: 4000, predicted: 3800 },
  { day: 'Fri', target: 4000, predicted: 2500 }, // Simulate a drop here!
  { day: 'Sat', target: 4000, predicted: 2700 },
  { day: 'Sun', target: 4000, predicted: 3900 },
];

const ChartPanel = () => {
  return (
    <div className="w-full h-64 mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          {/* Subtle grid lines for the dark theme */}
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
          <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} tickLine={false} />
          <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
          
          {/* Custom dark-mode tooltip on hover */}
          <Tooltip 
            contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569', color: '#f8fafc' }}
            itemStyle={{ color: '#e2e8f0' }}
          />
          <Legend wrapperStyle={{ paddingTop: '10px' }} />
          
          {/* The Data Lines */}
          <Line 
            type="monotone" 
            dataKey="target" 
            name="Target Output (Tons)" 
            stroke="#64748b" 
            strokeWidth={2} 
            strokeDasharray="5 5" 
            dot={false} 
          />
          <Line 
            type="monotone" 
            dataKey="predicted" 
            name="AI Forecast" 
            stroke="#3b82f6" 
            strokeWidth={3} 
            activeDot={{ r: 8 }} 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartPanel;
