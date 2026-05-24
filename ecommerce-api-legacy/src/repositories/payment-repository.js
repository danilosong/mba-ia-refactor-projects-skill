class PaymentRepository {
  constructor(db) {
    this.db = db;
  }

  create(enrollmentId, amount, status) {
    return this.db.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [
      enrollmentId,
      amount,
      status,
    ]);
  }

  getByEnrollmentId(enrollmentId) {
    return this.db.get("SELECT amount, status FROM payments WHERE enrollment_id = ?", [enrollmentId]);
  }
}

module.exports = { PaymentRepository };
