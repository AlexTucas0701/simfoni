import React from 'react';
import '../../css/Spinner.css'; // You can add your spinner styles in this file


const Spinner: React.FC = () => {
  return (
    <div className="spinner">
      <div className="spinner-circle"></div>
    </div>
  );
};

export default Spinner;
