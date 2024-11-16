const express = require('express');
//const Order = require('../models/accept_order');
const authenticate = require('../middleware/authenticate'); // Middleware to check if the driver is logged in
const Orderdetail = require('../models/Orderdetail');
const router = express.Router();
//const DriverAssign = require('../models/assign_driver');


// POST /api/orders - Create a new order
router.post('/create', async (req, res) => {
  try {
    // Extract data from the request body
    const { rest_id, rest_address, rest_location, delivery_distance, price, tip, order_id } = req.body;

    // Create a new order in the database
    const order = await Orderdetail.create({
      rest_id,
      rest_address,
      rest_location,
      delivery_distance,
      price,
      tip,
      order_id,
    });

    // Respond with the newly created order
    res.status(201).json({
      message: 'ok',
      order,
    });
  } catch (error) {
    console.error('Error assigning driver:', error);
    res.status(500).json({
      message: 'Failed to assign driver',
      error: error.message,
    });
  }
});

router.get('/list', async (req, res) => {
    try {
      const driver = await Orderdetail.findAll();
      return res.status(200).json({ message:'Order list', driver});
    } catch (error) {
      console.error('Error registering driver:', error);
  
      if (error.name === 'SequelizeValidationError') {
        const validationErrors = error.errors.map(err => err.message);
        return res.status(400).json({ message: 'Validation errors occurred', errors: validationErrors });
      }
  
      res.status(500).json({ message: 'failed to fetch list.' });
    }
  });

// PUT /api/orders/:orderId/accept - Accept an order
router.put('/:orderId/accept', authenticate, async (req, res) => {
  const { orderId } = req.params;
  const {driverId} = req.body; 

  try {
    // Find the order by ID
    const order = await Orderdetail.findOne({
      where: {
        order_id: orderId, // Column name should match the field in your database schema
      },
    }
    ); 

    if (!order) {
      return res.status(404).json({ message: 'Order not found' });
    }

    

    // Check if the order is already accepted or completed
    if (order.status == 'accepted') {
      return res.status(400).json({ message: 'Order has already been accepted' });
    }

    // Update order status to "accepted" and assign the driver
    order.status = 'accepted';
    order.driver_id = driverId;
    order.driverstatus = 'orderAssigned';
    await order.save();

    res.status(200).json({
      message: 'Order accepted successfully',
      order,
    });
  } catch (error) {
    console.error('Error accepting order:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

const getDistanceFromLatLonInKm = (lat1, lon1, lat2, lon2) => {
    const R = 6371; // Radius of the Earth in km
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  router.put('/:orderId/check-location', authenticate, async (req, res) => {
    const { orderId } = req.params;
    const { lat, long } = req.body; // Driver's current location
    const driverId = req.driverId; // Set in authenticate middleware
  
    try {
      // Find the order by ID
      const order = await Orderdetail.findOne({
        where: {
          order_id: orderId, // Column name should match the field in your database schema
        },
      }); 
      if (!order) {
        return res.status(404).json({ message: 'Order not found' });
      }
  
      // Check if the order is already received
      if (order.status === "received") {
        return res.status(400).json({ message: 'Order has already been received by a driver' });
      }
  
      // Calculate the distance between driver location and order location
      const distance = getDistanceFromLatLonInKm(lat, long, order.location.lat, order.location.long);
      const maxDistance = 5; // Acceptable distance in km (e.g., within 500 meters)
  
      if (distance > maxDistance) {
        return res.status(400).json({ message: 'Driver is not at the required location' });
      }
  
      // Update order status and assign driver
      order.status = 'received';
      order.driver_id = driverId;
      await order.save();
  
      res.status(200).json({
        message: 'Order received by driver',
        order,
      });
    } catch (error) {
      console.error('Error checking driver location:', error);
      res.status(500).json({ message: 'Internal server error' });
    }
  });

  // PUT /api/orders/:orderId/deliver - Check if driver is at customer location and deliver order
// router.put('/:orderId/deliver', authenticate, async (req, res) => {
//     const { orderId } = req.params;
//     const { lat, long } = req.body; // Driver's current location
//     const driverId = req.driverId; // Set in authenticate middleware
  
//     try {
//       // Find the order by ID
//       const order = await Order.findByPk(orderId);
//       if (!order) {
//         return res.status(404).json({ message: 'Order not found' });
//       }
  
//       // Verify the order is assigned to this driver and is not already delivered
//       if (order.driver_id !== driverId) {
//         return res.status(403).json({ message: 'Unauthorized: This order is not assigned to you' });
//       }
//       if (order.status === 'delivered') {
//         return res.status(400).json({ message: 'Order has already been delivered' });
//       }
  
//       // Calculate distance between driver's current location and customer location
//       const distance = getDistanceFromLatLonInKm(lat, long, order.customer_location.lat, order.customer_location.long);
//       const maxDistance = 0.5; // Acceptable distance in km (e.g., within 500 meters)
  
//       if (distance > maxDistance) {
//         return res.status(400).json({ message: 'Driver is not at the customer location' });
//       }
  
//       // Update order status to "delivered"
//       order.status = 'delivered';
//       DriverAssign.assign = 0;
//       await order.save();
  
//       res.status(200).json({
//         message: 'Order successfully delivered',
//         order,
//       });
//     } catch (error) {
//       console.error('Error delivering order:', error);
//       res.status(500).json({ message: 'Internal server error' });
//     }
//   });

  router.put('/:orderId/orderstatus', authenticate, async (req, res) => {
    const { orderId } = req.params;
    const {driverId,status} = req.body;
    console.log(driverId)
    console.log(status)
    //const status = req.status 
    try {
      // Update the status where both order_id and driver_id match
      const orderstatus = await Orderdetail.findOne(
         // Fields to update
        { 
          where: {
            order_id: orderId, // Match the order ID
            driver_id: driverId, // Match the driver ID
          },
        }
      );
      if(status == 'delivered'){
        orderstatus.driverstatus = 'Idle'
        orderstatus.status = status
      }
      orderstatus.status = status;
      await orderstatus.save();
      res.status(200).json({
        message: '`Order ID ${orderId} status updated successfully!`',
        orderstatus,
      });
    
    } catch (error) {
      console.error('Error updating order status:', error.message);
    }
  });

    

module.exports = router;