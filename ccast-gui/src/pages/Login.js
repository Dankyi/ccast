import React, { useRef, useState, useEffect, useContext } from 'react'
import { Link } from 'react-router-dom'

import './Login.css';
import AuthContext from "./../context/AuthProvider"
import axios from './../api/axios';

const LOGiN_URL = '/auth';

export default function Login({ setToken }) {
    const { setAuth } = useContext(AuthContext);

    const [username, setUserName] = useState('');
    const [password, setPassword] = useState('');
    const [errMsg, setErrorMsg] = useState('');

    const userRef = useRef();
    const errRef = useRef();

    // Set the initial focus to the username field.
    useEffect(() => {
        userRef.current.focus();
    }, [])

    // Remove any error message when the username or password changes.
    useEffect(() => {
        setErrorMsg('');
    }, [username, password])

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post(LOGiN_URL,
                JSON.stringify({ username, password }),
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true
                }
            );

            const accessToken = response?.data?.accessToken;
            const roles = response?.data?.roles;
            setAuth(username, password, roles, accessToken)
            setUserName('');
            setPassword('');
        }
        catch (err) 
        { 

            if(!err?.response){setErrorMsg('No Server Response.');}
            else if (err.response?.status === 400){setErrorMsg('Missing Username or Password.')}
            else if (err.response?.status === 401){setErrorMsg('Incorrect Username or Password.')}
            else{setErrorMsg('Login Failed.')}
            errRef.current.focus();
        }

    }


    return (
        <section className='Login'>
            <p ref={errRef} className={errMsg ? "errmsg" :
                "offscreen"} aria-live="assertive">{errMsg}
            </p>

            <h1> LOGIN </h1>

            <form onSubmit={handleSubmit}>
                <label>
                    <p>Username</p>
                    <input
                        type="text"
                        id="username"
                        ref={userRef}
                        autocomplete="off"
                        onChange={e => setUserName(e.target.value)}
                        value={username}
                    />
                </label>
                <label>
                    <p>Password</p>
                    <input
                        type="password"
                        id="password"
                        onChange={e => setPassword(e.target.value)}
                        value={password}
                    />
                </label>
                <div>
                    <button type="submit">Submit</button>
                </div>
            </form>

            <p>
                Need an account? <br />

                <li><Link to="/signup">Sign Up</Link></li>
            </p>

        </section>
    )
}
