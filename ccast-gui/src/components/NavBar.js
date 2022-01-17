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

import logo from './resources/IconIdeas1.PNG'

const Navbar = () => {  
    
    
    
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
                    <NavLink to="/settings" activeStyle>
                        Settings
                    </NavLink>
                </NavMenu>
            </Nav>
    );
};
export default Navbar;