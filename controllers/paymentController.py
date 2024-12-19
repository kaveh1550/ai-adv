const { Payment } = require('../models'); // مدل پرداخت

// ثبت پرداخت جدید
exports.createPayment = async (req, res, next) => {
  try {
    const { userId, consultationId, amount, paymentMethod, status } = req.body;
    const newPayment = await Payment.create({
      userId,
      consultationId,
      amount,
      paymentMethod,
      status
    });
    res.status(201).json({ payment: newPayment });
  } catch (err) {
    next(err);
  }
};

// دریافت تاریخچه پرداخت‌ها برای یک کاربر
exports.getPaymentsByUser = async (req, res, next) => {
  try {
    const payments = await Payment.findAll({
      where: { userId: req.params.userId }
    });
    res.status(200).json({ payments });
  } catch (err) {
    next(err);
  }
};

// دریافت تاریخچه پرداخت‌ها برای یک مشاور
exports.getPaymentsByAdvisor = async (req, res, next) => {
  try {
    const payments = await Payment.findAll({
      include: {
        model: Consultation,
        where: { advisorId: req.params.advisorId }
      }
    });
    res.status(200).json({ payments });
  } catch (err) {
    next(err);
  }
};
