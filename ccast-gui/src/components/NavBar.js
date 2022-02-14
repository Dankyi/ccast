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

const Navbar = () => {  
    
    const isLoggedIn = authService.getCurrentUser();
    console.log(isLoggedIn);
    
    if (isLoggedIn === null)
    return <DefaultNavbar />;
    else return <UserNavbar />;
    
};

const DefaultNavbar = () => 
{ 

    return (
        
        <Nav className="navbar">
        <NavLogo to="/">
            <img src={logo} width={175} height={85} />
        </NavLogo>

        <Bars />

        <NavMenu>
            <NavLink to="/" activeStyle>
                Home
            </NavLink>
            <NavLink to="/login" activeStyle>
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
        <NavLogo to="/">
            <img src={logo} width={175} height={85} />
        </NavLogo>

        <Bars />

        <NavMenu>
            <NavLink to="/" activeStyle>
                Home
            </NavLink>
            <NavLink to="/profile" activeStyle>
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