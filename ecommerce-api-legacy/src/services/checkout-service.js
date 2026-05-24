const { settings } = require("../config/settings");
const { PAYMENT_STATUS } = require("../config/constants");
const { NotFoundError, ValidationError } = require("../errors");

class CheckoutService {
  constructor({ userRepository, courseRepository, enrollmentRepository, paymentRepository, auditLogRepository, passwordService, auditCache, db }) {
    this.userRepository = userRepository;
    this.courseRepository = courseRepository;
    this.enrollmentRepository = enrollmentRepository;
    this.paymentRepository = paymentRepository;
    this.auditLogRepository = auditLogRepository;
    this.passwordService = passwordService;
    this.auditCache = auditCache;
    this.db = db;
  }

  async checkout(payload) {
    const customerName = payload.usr;
    const email = payload.eml;
    const password = payload.pwd || "123456";
    const courseId = payload.c_id;
    const card = payload.card;

    if (!customerName || !email || !courseId || !card) {
      throw new ValidationError("Bad Request");
    }

    const course = await this.courseRepository.getActiveCourseById(courseId);
    if (!course) {
      throw new NotFoundError("Curso nao encontrado");
    }

    const status = String(card).startsWith("4") ? PAYMENT_STATUS.PAID : PAYMENT_STATUS.DENIED;
    if (status === PAYMENT_STATUS.DENIED) {
      throw new ValidationError("Pagamento recusado");
    }

    const existingUser = await this.userRepository.getByEmail(email);
    const userId = existingUser ? existingUser.id : (await this.userRepository.create(customerName, email, this.passwordService.hashPassword(password))).lastID;

    const result = await this.db.transaction(async () => {
      const enrollment = await this.enrollmentRepository.create(userId, courseId);
      await this.paymentRepository.create(enrollment.lastID, course.price, status);
      await this.auditLogRepository.create(`Checkout curso ${courseId} por ${userId}`);
      return { enrollmentId: enrollment.lastID, courseTitle: course.title };
    });

    this.auditCache.save(`last_checkout_${userId}`, result.courseTitle);
    return {
      msg: "Sucesso",
      enrollment_id: result.enrollmentId,
      gateway: settings.paymentGatewayKey,
    };
  }
}

module.exports = { CheckoutService };
