import React from 'react';
import {Navbar} from 'react-bootstrap';

import './navbar-component.css';

export default class NavbarComponent extends React.PureComponent {
    render() {
        return (
          <div>
            <Navbar className="navbar" bg="dark" variant="dark">
                <Navbar.Brand>
                    <img
                        src="/logo.svg"
                        width="30"
                        height="30"
                        className="d-inline-block align-top"
                    />
                {' QA Dashboard'}
                </Navbar.Brand>
            </Navbar>
        </div>
      );
    }
  }