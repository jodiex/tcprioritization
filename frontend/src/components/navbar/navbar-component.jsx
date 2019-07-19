import React from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';

import './navbar-component.css';

class NavbarComponent extends React.Component {
    render() {
        return (
            <Navbar className="Navbar" bg="dark" variant="dark" expand="lg">
                <Navbar.Brand href="#home">Dashboard</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav" className="Navbar-elements">
                    <Nav >
                        <Nav.Link href="#home">Home</Nav.Link>
                        <Nav.Link href="#link">Link</Nav.Link>
                        <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                            <NavDropdown.Item href="#action/3.1">Log In Stuff</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.2">General Navigation</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default NavbarComponent;