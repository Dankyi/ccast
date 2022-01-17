import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Main from './pages/Main'
import Login from './pages/Login'
import SignUp from './pages/SignUp'
import User from './pages/User'
import NavBar from './components/NavBar';
import "bootstrap/dist/css/bootstrap.min.css";


function App() {

    return (
        <div>
            <NavBar />
            <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/main" element={<Main />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/user" element={<User />} />
            </Routes>
        </div>
    );
}

export default App
