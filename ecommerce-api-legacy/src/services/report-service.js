class ReportService {
  constructor({ courseRepository, enrollmentRepository, userRepository, paymentRepository }) {
    this.courseRepository = courseRepository;
    this.enrollmentRepository = enrollmentRepository;
    this.userRepository = userRepository;
    this.paymentRepository = paymentRepository;
  }

  async financialReport() {
    const courses = await this.courseRepository.listCourses();
    const report = [];

    for (const course of courses) {
      const enrollments = await this.enrollmentRepository.listByCourse(course.id);
      const students = [];
      let revenue = 0;

      for (const enrollment of enrollments) {
        const user = await this.userRepository.db.get("SELECT name, email FROM users WHERE id = ?", [enrollment.user_id]);
        const payment = await this.paymentRepository.getByEnrollmentId(enrollment.id);
        if (payment && payment.status === "PAID") {
          revenue += payment.amount;
        }
        students.push({
          student: user ? user.name : "Unknown",
          paid: payment ? payment.amount : 0,
        });
      }

      report.push({
        course: course.title,
        revenue,
        students,
      });
    }

    return report;
  }
}

module.exports = { ReportService };
