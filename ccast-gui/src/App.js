import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Main from './pages/Main'
import Login from './pages/Login'
import SignUp from './pages/SignUp'
import NavBar from './components/NavBar';

function App() {
    return (
        <div>
            <NavBar />
            <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/main" element={<Main />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
            </Routes>
        </div>
    );
}

export default App
