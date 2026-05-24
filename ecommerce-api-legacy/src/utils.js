const { settings } = require("./config/settings");
const { AuditCache } = require("./services/audit-cache");
const { hashPassword } = require("./services/password-service");

const globalCache = new AuditCache();

function logAndCache(key, data) {
  globalCache.save(key, data);
}

module.exports = {
  config: settings,
  logAndCache,
  badCrypto: hashPassword,
  globalCache,
  totalRevenue: 0,
};
