import { useEffect, useState } from 'react';
import { Navigate, useNavigate, Link } from 'react-router-dom'
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";
import AuthService from '../services/auth.service';

import './AuthForm.css';


export default function Profile() {

  let navigate = useNavigate();

  // States for registration
  const [currentUser, setCurrentUser] = useState('');
  const [token, setToken] = useState('');
  const [secret, setSecret] = useState('');

  // Handling the email change
  const handleToken = (e) => {
    setToken(e.target.value);
  };

  // Handling the password change
  const handleSecret = (e) => {
    setSecret(e.target.value);
  };

  // Handling the form submission
  const handleSubmit = (e) => {
    // Disable the normal procedure so this code only executes.
    e.preventDefault();


    if (token !== undefined && secret !== undefined) {
      AuthService.setTokens(currentUser.email, token, secret).then(
        () => {
          navigate("/ccast/home");
          window.location.reload(false);

        },

        // If there was an error, get the message and set the message in the state.
        error => { }
      );
    }
  }


  useEffect(() => {
    // Get the current user when the page loads.
    setCurrentUser(AuthService.getCurrentUser().data);
    if (currentUser.marketToken !== undefined) {
      setToken(currentUser.marketToken);
    }

  }, []);

  const toMarket = (e) => {
    window.location.replace('https://ftx.com/settings/api');
    window.location.reload();
  }

  const required = value => {
    if (!value) {
      return (
        <div className="alert alert-danger" role="alert">
          This field is required!
        </div>
      );
    }
  };

  if (currentUser === undefined) return (
    <div className='container'>
      <h1> No Profile Information in local storage. </h1>
      <p> How did you get here? </p>
    </div>
  );



  return (
    <div className="AuthForm">
      <div className="card card-container">


        <Form
          onSubmit={handleSubmit}

        >

          <div className='form-group'>
            <p>
              <strong>Name:</strong>{" "}
              {currentUser.name}
            </p>
            <p>
              <strong>Email:</strong>{" "}
              {currentUser.email}
            </p>
          </div>

          <div className="form-group">
            <label htmlFor="token">Auth Token</label>
            <Input
              type="text"
              className="form-control"
              name="email"
              value={token}
              onChange={handleToken}
              validations={[required]}
            />
          </div>

          <div className="form-group">
            <label htmlFor="secret">Secret Key</label>
            <Input
              type="password"
              className="form-control"
              name="secret"
              value={secret}
              onChange={handleSecret}
              validations={[required]}
            />
          </div>

          <br />

          <div className="form-group">
            <button
              className="btn btn-primary btn-block"
            >
              <span>Save Changes</span>
            </button>
          </div>

          <CheckButton
            style={{ display: "none" }}
          />
        </Form>

      </div>
      
      <p>
        Need a key? <br />
        <li><a href="https://ftx.com/settings/api">Visit FTX to generate one.</a></li>
      </p>

    </div>
  );
}
