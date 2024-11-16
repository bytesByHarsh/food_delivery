const Sequelize = require('sequelize');
const sequelize = require('../db');
const bcrypt = require('bcrypt');

const Driver = sequelize.define('driver', {
  driver_id: {
     type: Sequelize.STRING,
     allowNull: false,
    },  
  firstName: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  lastName: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  email: {
    type: Sequelize.STRING,
    allowNull: false,
    unique: true, 
  },
  password: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  age: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  date_of_birth: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  street: {
    type: Sequelize.STRING,
    allowNull: false, 
  },
  city: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  state: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  zip_code: {
    type: Sequelize.STRING,
    allowNull: false, 
  },
  country: {
    type: Sequelize.STRING,
    allowNull: false, 
  },
  phone_number: {
    type: Sequelize.STRING,
    allowNull: false, 
  },
});

Driver.beforeCreate(async (driver) => {
  driver.password = await bcrypt.hash(driver.password, 10);
});

module.exports = Driver;