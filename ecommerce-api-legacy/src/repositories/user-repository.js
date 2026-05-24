class UserRepository {
  constructor(db) {
    this.db = db;
  }

  getByEmail(email) {
    return this.db.get("SELECT id, name, email, pass FROM users WHERE email = ?", [email]);
  }

  create(name, email, passwordHash) {
    return this.db.run("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", [name, email, passwordHash]);
  }

  async deleteWithDependencies(userId) {
    const enrollments = await this.db.all("SELECT id FROM enrollments WHERE user_id = ?", [userId]);
    const enrollmentIds = enrollments.map((item) => item.id);

    await this.db.transaction(async () => {
      if (enrollmentIds.length > 0) {
        const placeholders = enrollmentIds.map(() => "?").join(",");
        await this.db.run(`DELETE FROM payments WHERE enrollment_id IN (${placeholders})`, enrollmentIds);
      }
      await this.db.run("DELETE FROM enrollments WHERE user_id = ?", [userId]);
      await this.db.run("DELETE FROM users WHERE id = ?", [userId]);
    });
  }
}

module.exports = { UserRepository };
