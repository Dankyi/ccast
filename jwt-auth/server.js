//https://www.bezkoder.com/node-js-jwt-authentication-mysql/


const express = require("express");
const cors = require("cors");


const app = express();

// Define the port to send responses from.
var corsOptions = {
  origin: "http://localhost:8081"
};

const db = require("./app/models");
const Role = db.role;

db.sequelize.sync();

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(express.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// simple route
app.get("/", (req, res) => {
  res.json({ message: "Welcome to CCAST authentication." });
});

// routes
require('./app/routes/auth.routes')(app);
require('./app/routes/user.routes')(app);

// set port, listen for requests
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});
