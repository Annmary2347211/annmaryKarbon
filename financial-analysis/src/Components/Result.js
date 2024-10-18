import React from 'react';
import './Result.css'; // Ensure this CSS file exists

function Result({ results }) {
  return (
    <div className="result-container">
      <h2>Results</h2>
      <p>TOTAL REVENUE 5CR FLAG Rule 1: {results.flags.TOTAL_REVENUE_5CR_FLAG}</p>
      <p>BORROWING TO REVENUE FLAG-Rule 2: {results.flags.BORROWING_TO_REVENUE_FLAG}</p>
      <p>ISCR FLAG Rule 3: {results.flags.ISCR_FLAG}</p>
    </div>
  );
}

export default Result;
