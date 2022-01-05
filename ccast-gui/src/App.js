import React from 'react'
import {Routes, Route} from 'react-router-dom'
import Main from './Main'
import Login from './Login'
import NavBar from './components/NavBar';

function App() {
    return (
      <div>
          <NavBar/>
        <Routes>
          <Route path="/" element={<Main />} />  
          <Route path="/main" element={<Main />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    );
  }

export default App
