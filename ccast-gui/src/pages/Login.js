import { useEffect, useState } from 'react';
import {Navigate, useNavigate, Link} from 'react-router-dom'
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";
import AuthService from '../services/auth.service';

import './AuthForm.css';


export default function Login() {

// States for registration
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [loading, setLoading] = useState(false);
const [message, setMessage] = useState('');


// States for checking the errors
const [submitted, setSubmitted] = useState(false);
const [error, setError] = useState(false);

// Handling the email change
const handleEmail = (e) => {
	setEmail(e.target.value);
	setSubmitted(false);
};

// Handling the password change
const handlePassword = (e) => {
	setPassword(e.target.value);
	setSubmitted(false);
};

// Handling the form submission
const handleSubmit = (e) => {
	// Disable the normal procedure so this code only executes.
  e.preventDefault();

  // Clear messages and set loading to true.
  setMessage("");
  setLoading(true);


  // Check that all of the provided details are valid.
  //this.form.validateAll();


    // If the login is successful:
    AuthService.login(email, password).then(
      () => {
        navigate("/ccast/profile");
        window.location.reload(false);
        
      },

      // If there was an error, get the message and set the message in the state.
      error => {
        const resMessage =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString();
 
        setLoading(false);
        setMessage(resMessage);
        errorMessage();
      }      
    );
    
    // Stop the login attempt due to invalid values.
 

};


// Showing error message if error is true
const errorMessage = () => {
	return (
	<div
		className="error"
		style={{
		display: error ? '' : 'none',
		}}>
		<h1>{message}</h1>
	</div>
	);
};

const required = value => {
  if (!value) {
    return (
      <div className="alert alert-danger" role="alert">
        This field is required!
      </div>
    );
  }
};

let navigate = useNavigate();

return (
	<div className="AuthForm">
        <div className="card card-container">
          <img
            src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
            alt="profile-img"
            className="profile-img-card"
          />

          <Form
            onSubmit={handleSubmit}
            
          >
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <Input
                type="text"
                className="form-control"
                name="email"
                value={email}
                onChange={handleEmail}
                validations={[required]}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <Input
                type="password"
                className="form-control"
                name="password"
                value={password}
                onChange={handlePassword}
                validations={[required]}
              />
            </div>

            <br />

            <div className="form-group">
              <button
                className="btn btn-primary btn-block"
                disabled={loading}
              >
                {loading && (
                  <span className="spinner-border spinner-border-sm"></span>
                )}
                <span>Login</span>
              </button>
            </div>

            {message && (
              <div className="form-group">
                <div className="alert alert-danger" role="alert">
                  {message}
                </div>
              </div>
            )}
            <CheckButton
              style={{ display: "none" }}              
            />
          </Form>
        </div>

        <p>
                Need an account? <br />

                <li><Link to="/ccast/signup">Sign Up</Link></li>
            </p>
      </div>
);
}
