const sqlite3 = require("sqlite3").verbose();

function createDatabase() {
  const raw = new sqlite3.Database(":memory:");

  return {
    raw,
    run(sql, params = []) {
      return new Promise((resolve, reject) => {
        raw.run(sql, params, function onRun(err) {
          if (err) {
            reject(err);
            return;
          }
          resolve({ lastID: this.lastID, changes: this.changes });
        });
      });
    },
    get(sql, params = []) {
      return new Promise((resolve, reject) => {
        raw.get(sql, params, (err, row) => {
          if (err) {
            reject(err);
            return;
          }
          resolve(row || null);
        });
      });
    },
    all(sql, params = []) {
      return new Promise((resolve, reject) => {
        raw.all(sql, params, (err, rows) => {
          if (err) {
            reject(err);
            return;
          }
          resolve(rows || []);
        });
      });
    },
    async transaction(work) {
      await this.run("BEGIN");
      try {
        const result = await work();
        await this.run("COMMIT");
        return result;
      } catch (error) {
        await this.run("ROLLBACK");
        throw error;
      }
    },
  };
}

async function initializeDatabase(db) {
  await db.run("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, pass TEXT)");
  await db.run("CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)");
  await db.run("CREATE TABLE enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)");
  await db.run("CREATE TABLE payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)");
  await db.run("CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)");

  await db.run("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", [
    "Leonan",
    "leonan@fullcycle.com.br",
    "123",
  ]);
  await db.run("INSERT INTO courses (title, price, active) VALUES (?, ?, ?)", [
    "Clean Architecture",
    997.0,
    1,
  ]);
  await db.run("INSERT INTO courses (title, price, active) VALUES (?, ?, ?)", [
    "Docker",
    497.0,
    1,
  ]);
  await db.run("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [1, 1]);
  await db.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [1, 997.0, "PAID"]);
}

module.exports = {
  createDatabase,
  initializeDatabase,
};
