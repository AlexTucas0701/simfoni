import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import './App.css';

import Home from './pages/Home';

const App: React.FC = () => {
  return (
    <div className="App">
      <Routes>
        <Route path='/' element={<Navigate to='/user' />} />
        <Route path='/:type' element={<Home />} />
      </Routes>
    </div>
  );
}

export default App;
