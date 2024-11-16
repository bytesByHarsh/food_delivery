const Sequelize = require('sequelize');
const sequelize = require('../db');
const Driver = require('./driver');
const Orderdetail = sequelize.define('Orderdetail', {
    rest_id: {
        type: Sequelize.STRING,
        allowNull: false,
      },
    rest_address: {
       type: Sequelize.STRING,
       allowNull: false,
      },
    rest_location: {
      type: Sequelize.JSONB, // Store latitude and longitude as JSON
      allowNull: false,
      },
    delivery_distance: {
      type: Sequelize.INTEGER,
      allowNull: false,
      },
    price: {
      type: Sequelize.FLOAT,
      allowNull: false,
      },
    tip: {
      type: Sequelize.FLOAT,
      allowNull: false,
      },
    order_id: {
      type: Sequelize.STRING,
      allowNull: false,
      unique: true,
      },
    status: {
      type: Sequelize.ENUM,
      values: [
        "placed",
        "ordered",
        "accepted",
        "on_the_way",
        "reached",
        "delivered",
        "cancelled",
        "returned",
        "failed",
        ],
        defaultValue: "placed", // Default status when an order is created
        allowNull: false,
      },
    driver_id: {
      type: Sequelize.INTEGER,
      references: {
        model: Driver,
        key: 'id',
      },
      allowNull: true, // driver_id will be null until assigned
      },
      driverstatus: {
        type: Sequelize.ENUM,
        values: [
          "orderAssigned",
          "Idle",
        ],
        defaultValue: "Idle", // Default status when an order is created
        allowNull: false,
      },
      location: {
        type: Sequelize.JSONB, // Storing location as JSON object with `lat` and `long`
        allowNull: false,
        defaultValue: "None",
      },
      customer_location: {
        type: Sequelize.JSONB, // Storing as JSON object with `lat` and `long`
        allowNull: false,
        defaultValue: "None",
      },  
},
{
  tableName: 'deliverorder', // Explicitly specify table name
}
);

module.exports = Orderdetail;