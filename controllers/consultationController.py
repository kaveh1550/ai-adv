const { Consultation } = require('../models'); // مدل مشاوره

// ثبت مشاوره جدید
exports.createConsultation = async (req, res, next) => {
  try {
    const { advisorId, userId, consultationDate, status } = req.body;
    const newConsultation = await Consultation.create({
      advisorId,
      userId,
      consultationDate,
      status
    });
    res.status(201).json({ consultation: newConsultation });
  } catch (err) {
    next(err);
  }
};

// دریافت تاریخچه مشاوره‌ها برای یک کاربر
exports.getConsultationsByUser = async (req, res, next) => {
  try {
    const consultations = await Consultation.findAll({
      where: { userId: req.params.userId },
      include: ['advisor']
    });
    res.status(200).json({ consultations });
  } catch (err) {
    next(err);
  }
};

// دریافت تاریخچه مشاوره‌ها برای یک مشاور
exports.getConsultationsByAdvisor = async (req, res, next) => {
  try {
    const consultations = await Consultation.findAll({
      where: { advisorId: req.params.advisorId },
      include: ['user']
    });
    res.status(200).json({ consultations });
  } catch (err) {
    next(err);
  }
};
