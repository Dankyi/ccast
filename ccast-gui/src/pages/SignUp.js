import React, { Component } from "react";
import { Link } from "react-router-dom";
import Form, { form } from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";
import { isEmail } from "validator";

import AuthService from "../services/auth.service";

import './AuthForm.css';

const required = value => {
  if (!value) {
    return (
      <div className="alert alert-danger" role="alert">
        This field is required!
      </div>
    );
  }
};

// Create verifications for the variables.
const email = value => {
  if (!isEmail(value)) {
    return (
      <div className="alert alert-danger" role="alert">
        This is not a valid email.
      </div>
    );
  }
};

const vusername = value => {
  if (value.length < 3 || value.length > 20) {
    return (
      <div className="alert alert-danger" role="alert">
        The username must be between 3 and 20 characters.
      </div>
    );
  }
};

const vpassword = value => {

  if (!ValidPassword(value)) {
    return (
      <div className="alert alert-danger" role="alert">
        The password must be at least 8 characters, and contain at least one Uppercase letter, one Lowercase letter, and one number.
      </div>
    );
  }

};

const vmatchpassword = value => {
  /**if (!PasswordMatch(value)){
  return (
    <div className="alert alert-danger" role="alert">
      The provided passwords do not match.
    </div>
  );
  }*/

};



/**
 * Enforce a password policy:
  At least 8 characters long.
  At least 1 Uppercase and Lowercase letter.
  At least 1 digit.
 * @param {string} value 
 */
function ValidPassword(value)
{
  var length = 8;
  if (value.length < length) return false;

  // If the converted values are identical, then all characters are either upper or lowercase.
  if (value.toLocaleLowerCase === value || value.toLocaleUpperCase === value) return false;

  const NUMERIC_REGEX = /[0-9]/;

  return NUMERIC_REGEX.test(value);

}

/**
 * Check if the password and password confirmations match.
 * @returns whether the values are the same or not.
 */
function PasswordMatch(value)
{
  if (this.state !== undefined) {
    return this.state.password === value
  }
  console.log("State is undefined.")
  return false;
}



export default class Register extends Component {
  constructor(props) {
    super(props);
    this.handleRegister = this.handleRegister.bind(this);
    this.onChangeUsername = this.onChangeUsername.bind(this);
    this.onChangeEmail = this.onChangeEmail.bind(this);
    this.onChangePassword = this.onChangePassword.bind(this);
    this.onChangeMatchPassword = this.onChangeMatchPassword.bind(this);

    this.state = {
      username: '',
      email: '',
      password: '',
      matchPassword: '',
      successful: false,
      message: ''
    };
  }

  // Update the variables when the text inputs change.
  onChangeUsername = (e) => {
    this.setState({
      username: e.target.value
    });
  }

  onChangeEmail = (e) => {
    this.setState({
      email: e.target.value
    });
  }

  onChangePassword = (e) => {
    this.setState({
      password: e.target.value
    });
  }

  onChangeMatchPassword = (e) => {
    this.setState({
      matchPassword: e.target.value
    });
  }

  handleRegister = (e) => {
    e.preventDefault();

    this.setState({
      message: "",
      successful: false
    });

    this.form.validateAll();

    if (this.state.password !== this.state.matchPassword){
      this.setState({
        successful: false,
        message: "The provided passwords do not match."
      });
    }

    else if (this.checkBtn.context._errors.length === 0) {
      AuthService.register(
        this.state.username,
        this.state.email,
        this.state.password
      ).then(
        response => {
          this.setState({
            message: response.data.message,
            successful: true
          });
        },
        error => {
          const resMessage =
            (error.response &&
              error.response.data &&
              error.response.data.message) ||
            error.message ||
            error.toString();

          this.setState({
            successful: false,
            message: resMessage
          });
        }
      );
    }
  } 

  render() {
    return (
      <div className="AuthForm">
        <div className="card card-container">
          <img
            src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
            alt="profile-img"
            className="profile-img-card"
            
          />

          <Form
            onSubmit={this.handleRegister}
            ref={c => {
              this.form = c;
            }}
          >
            {!this.state.successful && (
              <div>
                <div className="form-group">
                  <label htmlFor="username">Username</label>
                  <Input
                    type="text"
                    className="form-control"
                    name="username"
                    value={this.state.username}
                    onChange={this.onChangeUsername}
                    validations={[required, vusername]}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <Input
                    type="text"
                    className="form-control"
                    name="email"
                    value={this.state.email}
                    onChange={this.onChangeEmail}
                    validations={[required, email]}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="password">Password</label>
                  <Input
                    type="password"
                    className="form-control"
                    name="password"
                    value={this.state.password}
                    onChange={this.onChangePassword}
                    validations={[required, vpassword]}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="matchPassword">Confirm Password</label>
                  <Input
                    type="password"
                    className="form-control"
                    name="matchPassword"
                    value={this.state.matchpassword}
                    onChange={this.onChangeMatchPassword}
                    validations={[required, vmatchpassword]}
                  />
                </div>

                <br />

                <div className="form-group">
                  <button className="btn btn-primary btn-block">Sign Up</button>
                </div>
              </div>
            )}

            {this.state.message && (
              <div className="form-group">
                <div
                  className={
                    this.state.successful
                      ? "alert alert-success"
                      : "alert alert-danger"
                  }
                  role="alert"
                >
                  {this.state.message}
                </div>
              </div>
            )}
            <CheckButton
              style={{ display: "none" }}
              ref={c => {
                this.checkBtn = c;
              }}
            />
          </Form>
        </div>


        <p>
                Already have an account? <br />

                <li><Link to="/login">Sign In</Link></li>
            </p>
      </div>
    );
  }
}