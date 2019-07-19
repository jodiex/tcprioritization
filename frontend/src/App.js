import React from 'react';
import './App.css';

import NavbarComponent from './components/navbar/navbar-component';

function App() {
  return (
    <div className="App">
      <NavbarComponent/>
      <div className="App-body">
      </div>
      <div className="App-footer">
        <p>
          Made by <a className="App-link" href="www.adamwong.me">Adam Wong</a> and <a className="App-link" href="www.google.com">Alex Bakker</a> in Waterloo, Ontario
        </p>
      </div>
    </div>
  );
}

export default App;
