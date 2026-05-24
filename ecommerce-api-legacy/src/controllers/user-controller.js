class UserController {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }

  async deleteUser(req, res) {
    await this.userRepository.deleteWithDependencies(req.params.id);
    res.send("Usuario deletado com matriculas e pagamentos removidos.");
  }
}

module.exports = { UserController };
