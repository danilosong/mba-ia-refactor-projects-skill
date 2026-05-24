class EnrollmentRepository {
  constructor(db) {
    this.db = db;
  }

  create(userId, courseId) {
    return this.db.run("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [userId, courseId]);
  }

  listByCourse(courseId) {
    return this.db.all("SELECT id, user_id, course_id FROM enrollments WHERE course_id = ?", [courseId]);
  }
}

module.exports = { EnrollmentRepository };
