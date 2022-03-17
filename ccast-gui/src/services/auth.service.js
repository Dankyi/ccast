import axios from "axios";

const API_URL = "http://127.0.0.1:5000/users/";

class AuthService {
  login(email, password) {
    console.log("Sending Login Request.")

    console.log(API_URL)

    var userData = {
      "email": email,
      "password" : password
    }
    
    return axios
      .post(API_URL + "login", userData)
      .then( (response) => {
        console.log("Within the .then() method")
        if (response.data.data.accessToken) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem("user");
    window.location.reload(false);
  }

  register(name, email, password) {
    console.log("Sending Registration Request.")

    var userData = {
      "name": name,
      "email": email,
      "password" : password
    }

    var request = axios.post(API_URL, userData);

    console.log(request)

    return request
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));
  }

  isLoggedIn(){
    const isLoggedIn = JSON.parse(localStorage.getItem('user'));
    return (isLoggedIn !== null);
  }
}

export default new AuthService();