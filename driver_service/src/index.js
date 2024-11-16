// src/index.js

require('dotenv').config();
const express = require('express');
//const orderdetialroutes= require('./routes/order_created')
const userRoutes = require('./routes/user');
const driverRoutes = require('./routes/driver_register');
//const authRoutes = require('./routes/auth');
const orderRoutes = require('./routes/accept_order');
//const driverAssignRoutes = require('./routes/')
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

// import swagger ui module and swagger json file

const swaggerDocument = require('../swagger/swagger.json');



const app = express();



app.use(express.json());

// add route for swagger document API
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));





app.use('/api/v1/users', userRoutes);

app.use('/api/v1/driver', driverRoutes);

//app.use('/api/drivers', authRoutes);

app.use('/api/v1/orders', orderRoutes);

//app.use('/api/driver-assignments', driverAssignRoutes);

//app.use('/api/order', orderdetialroutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});