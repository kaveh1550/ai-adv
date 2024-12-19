const express = require('express');
const router = express.Router();
const advisorController = require('../controllers/advisorController');

// ثبت مشاور جدید
router.post('/', advisorController.createAdvisor);

// دریافت مشاور بر اساس ID
router.get('/:id', advisorController.getAdvisorById);

// جستجو مشاوران
router.get('/search', advisorController.searchAdvisors);

module.exports = router;
