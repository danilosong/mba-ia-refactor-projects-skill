const crypto = require("crypto");

function hashPassword(password) {
  return crypto.pbkdf2Sync(password, "legacy-lms-salt", 1000, 32, "sha256").toString("hex");
}

module.exports = {
  hashPassword,
};
