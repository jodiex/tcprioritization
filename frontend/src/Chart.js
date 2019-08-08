import React, { PureComponent } from 'react';
import {
  ResponsiveContainer, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip
} from 'recharts';

const data = [
  { name: 1, impression: 100 },
  { name: 2, impression: 120 },
  { name: 3, impression: 150 },
  { name: 4, impression: 180 },
  { name: 5, impression: 200 },
  { name: 6, impression: 499 },
  { name: 7, impression: 50 },
  { name: 8, impression: 100 },
  { name: 9, impression: 200 },
  { name: 10, impression: 222 },
  { name: 11, impression: 210 },
  { name: 12, impression: 300 },
  { name: 13, impression: 50 },
  { name: 14, impression: 190 },
  { name: 15, impression: 300 },
  { name: 16, impression: 400 },
  { name: 17, impression: 200 },
  { name: 18, impression: 50 },
  { name: 19, impression: 100 },
  { name: 20, impression: 100 }
];

export default class Example extends PureComponent {
  render() {
    return (
      <div style={{ margin: '17% auto', width: '50%', height: 400 }}>
        <ResponsiveContainer style>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis dataKey="impression" />
            <Line dataKey="impression" />
            <Tooltip />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }
}
