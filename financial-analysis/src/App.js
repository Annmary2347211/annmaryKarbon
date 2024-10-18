import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Header from './Components/Header';
import Result from './Components/Result';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const navigate = useNavigate(); // Use useNavigate instead of useHistory

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('https://annmarykarbon.onrender.com/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setResults(result);
      navigate('/result'); // Navigate to results page using navigate
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={
            <>
              <h1>Model</h1>
              <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button className="btn" type="submit">Submit</button>
              </form>
            </>
          } />
          <Route path="/result" element={results && <Result results={results} />} />
        </Routes>
      </main>
      
    </div>
  );
}

export default App;
