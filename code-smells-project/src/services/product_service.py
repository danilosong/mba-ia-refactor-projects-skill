from src.errors import NotFoundError, ValidationError


class ProductService:
    VALID_CATEGORIES = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]

    def __init__(self, product_repository):
        self.product_repository = product_repository

    def list_products(self):
        return self.product_repository.list_all()

    def get_product(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundError("Produto nao encontrado")
        return product

    def create_product(self, payload):
        data = self._validate_payload(payload)
        product_id = self.product_repository.create(**data)
        return {"id": product_id}

    def update_product(self, product_id, payload):
        self.get_product(product_id)
        data = self._validate_payload(payload)
        self.product_repository.update(product_id, **data)

    def delete_product(self, product_id):
        self.get_product(product_id)
        self.product_repository.delete(product_id)

    def search_products(self, termo, categoria, preco_min, preco_max):
        return self.product_repository.search(termo, categoria, preco_min, preco_max)

    def _validate_payload(self, payload):
        if not payload:
            raise ValidationError("Dados invalidos")
        for field in ["nome", "preco", "estoque"]:
            if field not in payload:
                raise ValidationError(f"{field.capitalize()} e obrigatorio")

        nome = payload["nome"].strip()
        descricao = payload.get("descricao", "").strip()
        categoria = payload.get("categoria", "geral")
        preco = payload["preco"]
        estoque = payload["estoque"]

        if len(nome) < 2:
            raise ValidationError("Nome muito curto")
        if len(nome) > 200:
            raise ValidationError("Nome muito longo")
        if preco < 0:
            raise ValidationError("Preco nao pode ser negativo")
        if estoque < 0:
            raise ValidationError("Estoque nao pode ser negativo")
        if categoria not in self.VALID_CATEGORIES:
            raise ValidationError("Categoria invalida")

        return {
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "estoque": estoque,
            "categoria": categoria,
        }
