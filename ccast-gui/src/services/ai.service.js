import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL + "ai/";

class AiService {

    startReal(id) {
        console.log("Sending Start Live Request.")
    
        var userData = {
          "id": id
        }
        
        return axios
          .post(API_URL + "startReal", userData)
          .then( (response) => {    
            return response.data;
          });
    }

    startFake(id) {
        console.log("Sending Start Dummy Request.")
    
        var userData = {
          "id": id
        }
        
        return axios
          .post(API_URL + "startFake", userData)
          .then( (response) => {    
            return response.data;
          });
    }

    stop(id) {
        console.log("Sending Stop Request.")
    
        var userData = {
          "id": id
        }
        
        return axios
          .post(API_URL + "stop", userData)
          .then( (response) => {    
            return response.data;
          });
    }

}

export default new AiService();