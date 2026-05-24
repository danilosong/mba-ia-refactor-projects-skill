class AuditCache {
  constructor() {
    this.entries = new Map();
  }

  save(key, value) {
    this.entries.set(key, value);
  }
}

module.exports = {
  AuditCache,
};
