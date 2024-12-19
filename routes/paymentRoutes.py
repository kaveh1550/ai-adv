const express = require('express');
const router = express.Router();
const paymentController = require('../controllers/paymentController');

// ثبت پرداخت جدید
router.post('/', paymentController.createPayment);

// دریافت تاریخچه پرداخت‌ها برای یک کاربر
router.get('/user/:userId', paymentController.getPaymentsByUser);

// دریافت تاریخچه پرداخت‌ها برای یک مشاور
router.get('/advisor/:advisorId', paymentController.getPaymentsByAdvisor);

module.exports = router;
