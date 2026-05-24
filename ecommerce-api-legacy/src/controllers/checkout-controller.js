class CheckoutController {
  constructor(checkoutService) {
    this.checkoutService = checkoutService;
  }

  async checkout(req, res) {
    const result = await this.checkoutService.checkout(req.body || {});
    const response = {
      msg: result.msg,
      enrollment_id: result.enrollment_id,
    };
    res.status(200).json(response);
  }
}

module.exports = { CheckoutController };
