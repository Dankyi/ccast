import axios from "axios";

const API_URL = "http://127.0.0.1:5000/users/";

class AuthService {
  login(username, password) {
    return axios
      .post(API_URL + "login", {
        username,
        password
      })
      .then(response => {
        if (response.data.accessToken) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem("user");
  }

  register(username, email, password) {
    console.log("Sending Registration Request.")

    var userData = {
      "name": username,
      "email": email,
      "password" : password
    }

    var request = axios.post(API_URL, userData);

    console.log(request)

    return request
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));;
  }

  isLoggedIn(){
    const isLoggedIn = JSON.parse(localStorage.getItem('user'));
    return (isLoggedIn !== null);
  }
}

export default new AuthService();