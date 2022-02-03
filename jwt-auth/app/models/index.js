const config = require("../config/db.config.js");

const Sequelize = require("sequelize");
const sequelize = new Sequelize(
  config.DB,
  config.USER,
  config.PASSWORD,
  {
    host: config.HOST,
    dialect: config.dialect,
    operatorsAliases: false,

    pool: {
      max: config.pool.max,
      min: config.pool.min,
      acquire: config.pool.acquire,
      idle: config.pool.idle
    }
  }
);

const db = {};

db.Sequelize = Sequelize;
db.sequelize = sequelize;

db.user = require("../models/user.model.js")(sequelize, Sequelize);
db.role = require("../models/role.model.js")(sequelize, Sequelize);

// Create empty junction table to remove timestamp generation.
var userRoles = sequelize.define('user_roles', {}, {  timestamps: false});

// Define belongsToMany to solve Many-to-Many database issues.

db.role.belongsToMany(db.user, {
  through: userRoles,
  foreignKey: "roleId",
  otherKey: "userId"
});
db.user.belongsToMany(db.role, {
  through: userRoles,
  foreignKey: "userId",
  otherKey: "roleId",
});

db.ROLES = ["user", "admin", "moderator"];

module.exports = db;