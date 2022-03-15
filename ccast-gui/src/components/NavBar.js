import React, { useState } from "react";
import {
    Nav,
    NavLogo,
    NavLink,
    Bars,
    NavMenu,
    NavBtn,
    NavBtnLink
} from "./NavbarElement";
import authService from "../services/auth.service";

import logo from './resources/IconIdeas1.PNG'

// Update the navbar when the local storage changes.


function Navbar()
{
    var isAuth = authService.isLoggedIn();
    //console.log(isAuth);
  return isAuth ? <UserNavbar /> : <DefaultNavbar />;
};


const DefaultNavbar = () => 
{ 

    return (
        
        <Nav className="navbar">
        <NavLogo to="/ccast/home">
            <img src={logo} width={175} height={85} />
        </NavLogo>

        <Bars />

        <NavMenu>
            <NavLink to="/ccast/home" activeStyle>
                Home
            </NavLink>
            <NavLink to="/ccast/login" activeStyle>
                Login
            </NavLink>
        </NavMenu>
    </Nav>
    );

}

const UserNavbar = () => 
{ 

    return (
        
        <Nav className="navbar">
        <NavLogo to="/ccast/home">
            <img src={logo} width={175} height={85} />
        </NavLogo>

        <Bars />

        <NavMenu>
            <NavLink to="/ccast/home" activeStyle>
                Home
            </NavLink>
            <NavLink to="/ccast/profile" activeStyle>
                Profile
            </NavLink>
            <NavBtn onClick={authService.logout}>
                Log Out
            </NavBtn>
        </NavMenu>
    </Nav>
    );

}

export default Navbar;