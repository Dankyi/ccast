import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Main from './Main'
import Login from './Login'
import SignUp from './SignUp'
import User from './User'
import Profile from './Profile';

function Views() {
  return (
  <Routes>
    <Route path="/" element={<Main />} />
    <Route path="/main" element={<Main />} />
    <Route path="/login" element={<Login />} />
    <Route path="/signup" element={<SignUp />} />
    <Route path="/user" element={<User />} />
    <Route path="/profile" element={<Profile />} />

    <Route index element={<Main />} />
</Routes>
  )
}

export default Views