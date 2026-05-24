const { createDatabase, initializeDatabase } = require("./db/database");

class AppManager {
  constructor() {
    this.db = createDatabase();
  }

  async initDb() {
    await initializeDatabase(this.db);
  }
}

module.exports = AppManager;
