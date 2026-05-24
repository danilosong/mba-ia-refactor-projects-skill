const settings = {
  port: Number(process.env.PORT || 3000),
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "sandbox-gateway-key",
  smtpUser: process.env.SMTP_USER || "no-reply@example.com",
};

module.exports = { settings };
