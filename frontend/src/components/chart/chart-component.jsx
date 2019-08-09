import React from 'react';
import Axios from 'axios';

import './chart-component.css';

import {
  ResponsiveContainer, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip
} from 'recharts';


export default class ChartComponent extends React.PureComponent {
  constructor(props){
    super(props);
    this.state = { data: null };
  }
  componentWillMount() {
    Axios.get('http://localhost:5000/tests')
    .then((response) => {
      this.setState({data : response.data});
    });
  }

  render() {
    return (
      <div className="chart">
        {
          (() => {
            if (this.state.data) {
              return (
                <div className="chart">
                  <ResponsiveContainer style>
                    <LineChart data={this.state.data}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis dataKey="impression" />
                      <Line className="line" dataKey="impression" />
                      <Tooltip />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              );
            } else {
              return (
                <p>Waiting for data...</p>
              )
            }
          })()
        }
      </div>
    );
  }
}
