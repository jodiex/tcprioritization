import React from 'react';
import './home-page.css';

import CardComponent from '../../components/card/card-component';
import ChartComponent from '../../components/chart/chart-component';
import Navbar from '../../components/navbar/navbar-component';


export default class HomePage extends React.PureComponent {
    render() {
        return (
            <div className='fullpage'>
                <Navbar />
                <CardComponent>
                    <ChartComponent/>
                </CardComponent>
            </div>
        );
    }
}