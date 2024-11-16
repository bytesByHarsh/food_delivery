require('dotenv').config();
const jwt = require('jsonwebtoken');
//const JWT_SECRET = "your_secret_key";


const JWT_SECRET = process.env.JWT_SECRET;
console.log("authorize",JWT_SECRET)

function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // 'Bearer <token>'

  if (!token) {
    return res.status(401).json({ message: 'Access denied. No token provided.' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded; // Attach decoded user info to the request object
    next(); // Pass to the next middleware/route handler
  } catch (error) {
    console.error('Token verification error:', error);
    res.status(403).json({ message: 'Invalid token.' });
  }
}
// 

module.exports = authenticateToken;