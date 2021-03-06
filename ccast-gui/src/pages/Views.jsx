import React from 'react'
import { Routes, Route, Outlet, Navigate } from 'react-router-dom'
import Main from './Main'
import Login from './Login'
import SignUp from './SignUp'
import Profile from './Profile';
import authService from '../services/auth.service'

const Views = () => {
  return (
  <Routes>
    <Route path="/ccast/login" element={<Login />} />
    <Route path="/ccast/signup" element={<SignUp />} />      
    <Route path="/ccast" element={<Navigate to="/ccast/home"/>}/>      
    
    
    
    /** Protected routes (Requires user sign in to view) */
    <Route element={<ProtectedViews />}>
      <Route path="/ccast/home" element={<Main />} />    
      <Route path="/ccast/profile" element={<Profile />} />
      <Route index element={<Main />} />
    </Route>

    <Route path="/*" element={    <div><h1>ERROR 404: Page not found.</h1></div>}/>
</Routes>
  )
}

const ProtectedViews = () => 
{
  const isAuth = authService.isLoggedIn();
  return isAuth ? <Outlet /> : <Login />;
}

export default Views