const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const { authMiddleware } = require('../middlewares/authMiddleware');

// ثبت‌نام کاربر
router.post('/register', userController.registerUser);

// ورود کاربر
router.post('/login', userController.loginUser);

// دریافت اطلاعات کاربر (با استفاده از توکن)
router.get('/profile', authMiddleware, userController.getUserProfile);

module.exports = router;
