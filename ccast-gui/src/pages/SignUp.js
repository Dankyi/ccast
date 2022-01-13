import React, { useRef, useState, useEffect } from 'react'
import { FaCheck, FaFontAwesome, FaInfoCircle, FaTimes } from 'react-icons/fa';
import { Link } from 'react-router-dom'

import './SignUp.css';
import axios from '../api/axios';

const USER_REGEX = /^[a-zA-Z][a-zA-Z0-9-_]{3,23}$/;
const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$/;

const REGISTER_URL = '/register';

const SignUp = () => {

    const userRef = useRef();
    const errRef = useRef();

    const [username, setUserName] = useState('');
    const [validName, setValidName] = useState(false);
    const [userFocus, setUserFocus] = useState(false);

    const [password, setPassword] = useState('');
    const [validPassword, setValidPassword] = useState(false);
    const [passwordFocus, setPasswordFocus] = useState(false);

    const [matchPassword, setMatchPassword] = useState('');
    const [validMatch, setValidMatch] = useState(false);
    const [matchFocus, setMatchFocus] = useState(false);

    const [errMsg, setErrorMsg] = useState('');
    const [success, setSuccess] = useState(false);

    // Set the initial focus to the username field.
    useEffect(() => {
        userRef.current.focus();
    }, [])

    // Validate the username when the value changes.
    useEffect(() => {
        const result = USER_REGEX.test(username);
        console.log(result);
        console.log(username);
        setValidName(result);
    }, [username])

    // Validate the password when the value changes.
    useEffect(() => {
        const result = PWD_REGEX.test(password);
        console.log(result);
        console.log(password);
        setValidPassword(result);
        const match = password === matchPassword;
        setValidMatch(match);
    }, [password, matchPassword])

    // Remove error messages when the text fields change.
    useEffect(() => {
        setErrorMsg('');
    }, [username, password, matchPassword])

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Catch any last minute issues.
        const v1 = USER_REGEX.test(username);
        const v2 = PWD_REGEX.test(password);
        if (!v1 || !v2){
            setErrorMsg ("Invalid Entry");
            return;
        }

        try{
            const response = await axios.post(
                REGISTER_URL, 
                JSON.stringify({username, password}),
                {
                    headers: {'Content-Type' : 'application/json'},
                    withCredentials: true
                }
            );
            console.log(response.data);
            setSuccess(true);
        }
        catch (err) 
        { 

            if(!err?.response){setErrorMsg('No Server Response.');}
            else if (err.response?.status === 409){setErrorMsg('Username Taken.')}
            else if (err.response?.status === 400){setErrorMsg('Missing Username or Password.')}
            else if (err.response?.status === 401){setErrorMsg('Incorrect Username or Password.')}
            else{setErrorMsg('Login Failed.')}
            errRef.current.focus();
        }
    }

    return (
        <section className='SignUp'>

            <p ref={errRef} className={errMsg ? "errmsg" :
                "offscreen"} aria-live="assertive">{errMsg}
            </p>

            <h1> Sign Up </h1>

            <form onSubmit={handleSubmit}>
                <label htmlFor='username'>
                    Username:
                    <span className={validName ? "valid" : "hide"}>
                    <FaFontAwesome icon = {FaCheck}/>
                    </span>
                    <span className={validName || !username ? "hide" : "invalid"}>
                        <FaFontAwesome icon={FaTimes}/>
                    </span>
                    <input
                        type="text"
                        id="username"
                        ref={userRef}
                        autocomplete="off"
                        onChange={e => setUserName(e.target.value)}
                        value={username}
                        required
                        aria-invalid={validName ? "false" : "true"}
                        aria-describedby="uidnote"
                        onFocus={() => setUserFocus(true)}
                        onBlur={() => setUserFocus(false)}
                    />
                </label>

                <p id='uidnote' className={userFocus && username && !validName ? "instructions" : "offscreen"}>
                    <FaInfoCircle icon = {FaInfoCircle}/> <br />
                4 to 24 characters.<br />
                Must begin with a letter.<br />
                Letters, Numbers, Underscores, Hyphens, are allowed.
                </p>

                <label htmlFor='password'>
                    Password:
                    <span className={validPassword ? "valid" : "hide"}>
                    <FaFontAwesome icon = {FaCheck}/>
                    </span>
                    <span className={validPassword || !password ? "hide" : "invalid"}>
                        <FaFontAwesome icon={FaTimes}/>
                    </span>
                    <input
                        type="password"
                        id="password"
                        onChange={e => setPassword(e.target.value)}
                        value={password}
                        required
                        aria-invalid={validPassword ? "false" : "true"}
                        aria-describedby="passwordnote"
                        onFocus={() => setPasswordFocus(true)}
                        onBlur={() => setPasswordFocus(false)}
                    />
                </label>

                <p id='passwordnote' className={passwordFocus && password && !validPassword ? "instructions" : "offscreen"}>
                    <FaInfoCircle icon = {FaInfoCircle}/> <br />
                8 to 24 characters.<br />
                Must include at least one Uppercase, Lowercase, Number, and Special character.<br />
                
                </p>

                <label htmlFor='matchPassword'>
                    Confirm Password:
                    <span className={validMatch && matchPassword ? "valid" : "hide"}>
                    <FaFontAwesome icon = {FaCheck}/>
                    </span>
                    <span className={validMatch || !matchPassword ? "hide" : "invalid"}>
                        <FaFontAwesome icon={FaTimes}/>
                    </span>
                    <input
                        type="password"
                        id="matchPassword"
                        onChange={e => setMatchPassword(e.target.value)}
                        value={matchPassword}
                        required
                        aria-invalid={validMatch ? "false" : "true"}
                        aria-describedby="matchnote"
                        onFocus={() => setMatchFocus(true)}
                        onBlur={() => setMatchFocus(false)}
                    />
                </label>

                <p id='matchnote' className={matchFocus && !validMatch? "instructions" : "offscreen"}>
                    <FaInfoCircle icon = {FaInfoCircle}/> <br />
                Must match the first password input.
                
                </p>

                <div>
                    <button disabled={!validName || !validPassword || !validMatch ? true : false}>Sign Up</button>
                </div>
            </form>

            <p>
                Already have an account? <br />
                <li><Link to="/login">Login</Link></li>
            </p>

        </section>
    )
}

export default SignUp
