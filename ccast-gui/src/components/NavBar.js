import React from "react";
import {
    Nav,
    NavLogo,
    NavLink,
    Bars,
    NavMenu,
    NavBtn,
    NavBtnLink
} from "./NavbarElement";

const Navbar = () => {
    return (
        <>
           <Nav className="navbar">
            <NavLogo to="/">
            <img src={"https://images.ctfassets.net/23aumh6u8s0i/3vCAkDy9os54mkVdD09lps/2b5386b4302f7ce38c4f6a69d6379dc0/reactjs"} width={85} height={85}/>
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
        </>
    );
};
export default Navbar;