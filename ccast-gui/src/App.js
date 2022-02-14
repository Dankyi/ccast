import React from 'react'
import { BrowserRouter } from 'react-router-dom'

import NavBar from './components/NavBar';
import "bootstrap/dist/css/bootstrap.min.css";
import Views from './pages/Views'


function App(){
        return (
                <BrowserRouter>
                <NavBar />
                <Views/>
                </BrowserRouter>
        );
    
}

export default App
