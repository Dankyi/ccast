import React from 'react'
import {Link} from 'react-router-dom'


function Login() {
    return (
        <div className='Login'>
            <h1> LOGIN </h1>
            <li><Link to="/signup">Sign Up</Link></li>

        </div>
    )
}

export default Login
