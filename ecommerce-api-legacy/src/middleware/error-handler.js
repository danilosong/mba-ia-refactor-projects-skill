const { AppError } = require("../errors");

function errorHandler(error, req, res, next) {
  if (error instanceof AppError) {
    res.status(error.statusCode).send(error.message);
    return;
  }

  res.status(500).send("Erro interno");
}

module.exports = { errorHandler };
