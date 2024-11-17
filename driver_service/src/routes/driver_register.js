const express = require('express');
const router = express.Router();
const Driver = require('../models/driver');
const User = require('../models/user')
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
require('dotenv').config();



const JWT_SECRET = process.env.JWT_SECRET;
console.log(JWT_SECRET)
const JWT_EXPIRATION = process.env.JWT_EXPIRATION || '1h';


// Create a new user
router.post('/register', async (req, res) => {

    const{adminId,...data} = req.body
   try {
    const adminUser = await User.findByPk(adminId);

    if (!adminUser || !adminUser.isSuperuser) {
        return res.status(403).json({ error: "Permission denied: Only superusers can register drivers." });
      }


    
    const driver = await Driver.create(req.body);
    // console.log('new driver created',driver.toJSON())

    return res.status(201).json({ message:'driver registered successfully', driver});
  } catch (error) {
    console.error('Error registering driver:', error);

    if (error.name === 'SequelizeValidationError') {
      const validationErrors = error.errors.map(err => err.message);
      return res.status(400).json({ message: 'Validation errors occurred', errors: validationErrors });
    }

    res.status(500).json({ message: 'failed to create driver.' });
  }
});

router.get('/list', async (req, res) => {
    try {
      const driver = await Driver.findAll();
      return res.status(200).json({ message:'driver list', driver});
    } catch (error) {
      console.error('Error registering driver:', error);
  
      if (error.name === 'SequelizeValidationError') {
        const validationErrors = error.errors.map(err => err.message);
        return res.status(400).json({ message: 'Validation errors occurred', errors: validationErrors });
      }
  
      res.status(500).json({ message: 'failed to fetch list.' });
    }
  });

  // POST /api/drivers/login - Driver login
router.post('/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    // Find driver by email
    const driver = await Driver.findOne({ where: { email } });
    if (!driver) {
      return res.status(404).json({ message: 'Driver not found' });
    }

    // Check if password is correct
    const isPasswordValid = await bcrypt.compare(password, driver.password);
    if (!isPasswordValid) {
      return res.status(401).json({ message: 'Invalid password' });
    }

    // Generate JWT token
    console.log('JWT_SECRET:', JWT_SECRET);
    const token = jwt.sign({ id: driver.id, email: driver.email }, JWT_SECRET, { expiresIn: JWT_EXPIRATION });

    res.status(200).json({
      message: 'Login successful',
      token,
    });
  } catch (error) {
    console.error('Error logging in driver:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

module.exports = router;