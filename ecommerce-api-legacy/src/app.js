const express = require("express");

const { settings } = require("./config/settings");
const { createDatabase, initializeDatabase } = require("./db/database");
const { UserRepository } = require("./repositories/user-repository");
const { CourseRepository } = require("./repositories/course-repository");
const { EnrollmentRepository } = require("./repositories/enrollment-repository");
const { PaymentRepository } = require("./repositories/payment-repository");
const { AuditLogRepository } = require("./repositories/audit-log-repository");
const { CheckoutService } = require("./services/checkout-service");
const { ReportService } = require("./services/report-service");
const { hashPassword } = require("./services/password-service");
const { AuditCache } = require("./services/audit-cache");
const { CheckoutController } = require("./controllers/checkout-controller");
const { ReportController } = require("./controllers/report-controller");
const { UserController } = require("./controllers/user-controller");
const { buildApiRoutes } = require("./routes/api-routes");
const { errorHandler } = require("./middleware/error-handler");

async function start() {
  const db = createDatabase();
  await initializeDatabase(db);

  const userRepository = new UserRepository(db);
  const courseRepository = new CourseRepository(db);
  const enrollmentRepository = new EnrollmentRepository(db);
  const paymentRepository = new PaymentRepository(db);
  const auditLogRepository = new AuditLogRepository(db);
  const auditCache = new AuditCache();

  const checkoutService = new CheckoutService({
    userRepository,
    courseRepository,
    enrollmentRepository,
    paymentRepository,
    auditLogRepository,
    passwordService: { hashPassword },
    auditCache,
    db,
  });
  const reportService = new ReportService({
    courseRepository,
    enrollmentRepository,
    userRepository,
    paymentRepository,
  });

  const checkoutController = new CheckoutController(checkoutService);
  const reportController = new ReportController(reportService);
  const userController = new UserController(userRepository);

  const app = express();
  app.use(express.json());
  app.use("/api", buildApiRoutes({ checkoutController, reportController, userController }));
  app.use(errorHandler);

  app.listen(settings.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${settings.port}...`);
  });
}

start().catch((error) => {
  console.error("Falha ao iniciar a aplicacao", error);
  process.exit(1);
});
