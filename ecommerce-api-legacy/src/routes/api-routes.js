const express = require("express");

const { asyncHandler } = require("../middleware/async-handler");

function buildApiRoutes({ checkoutController, reportController, userController }) {
  const router = express.Router();

  router.post("/checkout", asyncHandler((req, res) => checkoutController.checkout(req, res)));
  router.get("/admin/financial-report", asyncHandler((req, res) => reportController.financialReport(req, res)));
  router.delete("/users/:id", asyncHandler((req, res) => userController.deleteUser(req, res)));

  return router;
}

module.exports = { buildApiRoutes };
