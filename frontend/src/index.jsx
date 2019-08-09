import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import ChartComponent from './components/chart/chart-component';

import * as serviceWorker from './serviceWorker';

const total = (
<div>
    <ChartComponent />
</div>
);

ReactDOM.render(total, document.getElementById('root'));
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
