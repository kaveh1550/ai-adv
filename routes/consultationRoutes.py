const express = require('express');
const router = express.Router();
const consultationController = require('../controllers/consultationController');

// ثبت مشاوره جدید
router.post('/', consultationController.createConsultation);

// دریافت تاریخچه مشاوره‌ها برای یک کاربر
router.get('/user/:userId', consultationController.getConsultationsByUser);

// دریافت تاریخچه مشاوره‌ها برای یک مشاور
router.get('/advisor/:advisorId', consultationController.getConsultationsByAdvisor);

module.exports = router;
