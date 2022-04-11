import axios from "axios";

const API_URL = "http://127.0.0.1:5000/ai/";



class AiService {

  startReal(id, marketToken, marketSecret) {
    console.log("Sending Start Live Request.")

    var userData = {
      "id": id,
      "token": marketToken,
      "secret": marketSecret
    }

    return axios
      .post(API_URL + "startReal", userData)
      .then((response) => {
        return response.data;
      });
  }

  startFake(id, marketToken, marketSecret) {
    console.log("Sending Start Dummy Request.")

    var userData = {
      "id": id,
      "token": marketToken,
      "secret": marketSecret
    }

    return axios
      .post(API_URL + "startFake", userData)
      .then((response) => {
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
      .then((response) => {
        return response.data;
      });
  }

  getStatus(id) {
    console.log("Aquiring AI status. ID = ", id)

    var userData = {
      "id": id
    }

    var status = axios.post(API_URL + "status", userData)

    return status
  }

  getMarketInfo(id) {
    console.log("Getting balance for user ", id)

    var userData = {
      "id": id
    }

    return axios
      .post(API_URL + "info", userData)
      .then( (response) => {

        response = response.data.data

      console.log("Recieved the following from the API:")
      console.log(response)

      return response
    });
  }

}



export default new AiService();