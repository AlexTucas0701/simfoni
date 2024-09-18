import React from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';

import Home from './pages/Home';

const App: React.FC = () => {
  return (
    <div className="App">
      <Routes>
        <Route path='/' element={<Home />} />
      </Routes>
    </div>
  );
}

export default App;
