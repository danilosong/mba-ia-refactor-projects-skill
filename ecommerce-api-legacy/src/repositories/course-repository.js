class CourseRepository {
  constructor(db) {
    this.db = db;
  }

  getActiveCourseById(courseId) {
    return this.db.get("SELECT id, title, price, active FROM courses WHERE id = ? AND active = 1", [courseId]);
  }

  listCourses() {
    return this.db.all("SELECT id, title, price, active FROM courses ORDER BY id");
  }
}

module.exports = { CourseRepository };
