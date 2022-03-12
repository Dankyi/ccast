import React, { useState, useEffect } from 'react'
import { BrowserRouter } from 'react-router-dom'

import NavBar from './components/NavBar';
import "bootstrap/dist/css/bootstrap.min.css";
import Views from './pages/Views'



function App(){

    const [currentTime, setCurrentTime] = useState(0);
  
    useEffect(() => {
      fetch('/api/time').then(res => res.json()).then(data => {
        setCurrentTime(data.time);
      });
    }, []);

        return (
                <BrowserRouter>
                <NavBar />
                <p>The current time is {currentTime}.</p>
                <Views/>
                </BrowserRouter>
        );
    
}

export default App
