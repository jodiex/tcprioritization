import React from 'react';
import './card-component.css';

export default class CardComponent extends React.PureComponent {
    render() {
        return (
            <div className="card">
                {this.props.children}
            </div>
        );
    }
}