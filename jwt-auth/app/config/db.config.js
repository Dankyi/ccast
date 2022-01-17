module.exports = {
    HOST: "selene.hud.ac.uk",
    USER: "ccast",
    PASSWORD: "CC12nov21cc",
    DB: "ccast",
    dialect: "mysql",
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  };