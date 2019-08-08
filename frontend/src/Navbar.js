import React, { PureComponent } from 'react';

import {Navbar} from 'react-bootstrap';

export default class Head extends PureComponent {
    render() {
      return (
          <div>
            <Navbar bg="dark" variant="dark">
            <Navbar.Brand href="#home">
            <img
                alt=""
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