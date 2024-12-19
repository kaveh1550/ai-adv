const { Advisor } = require('../models'); // مدل مشاور

// ثبت مشاور جدید
exports.createAdvisor = async (req, res, next) => {
  try {
    const { name, expertise, experience, rating } = req.body;
    const newAdvisor = await Advisor.create({
      name,
      expertise,
      experience,
      rating
    });
    res.status(201).json({ advisor: newAdvisor });
  } catch (err) {
    next(err);
  }
};

// دریافت اطلاعات مشاور بر اساس ID
exports.getAdvisorById = async (req, res, next) => {
  try {
    const advisor = await Advisor.findByPk(req.params.id);
    if (!advisor) {
      return res.status(404).json({ message: 'مشاور پیدا نشد' });
    }
    res.status(200).json({ advisor });
  } catch (err) {
    next(err);
  }
};

// جستجو و فیلتر مشاوران
exports.searchAdvisors = async (req, res, next) => {
  try {
    const { expertise, rating } = req.query;
    const advisors = await Advisor.findAll({
      where: {
        expertise: expertise || { [Op.ne]: null },
        rating: { [Op.gte]: rating || 0 }
      }
    });
    res.status(200).json({ advisors });
  } catch (err) {
    next(err);
  }
};
