from src.errors import NotFoundError, ValidationError


class OrderService:
    VALID_STATUS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]

    def __init__(self, order_repository, product_repository, user_repository):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.user_repository = user_repository

    def create_order(self, payload):
        if not payload:
            raise ValidationError("Dados invalidos")
        usuario_id = payload.get("usuario_id")
        itens = payload.get("itens", [])
        if not usuario_id:
            raise ValidationError("Usuario ID e obrigatorio")
        if not self.user_repository.get_by_id(usuario_id):
            raise NotFoundError("Usuario nao encontrado")
        if not itens:
            raise ValidationError("Pedido deve ter pelo menos 1 item")

        product_ids = [item.get("produto_id") for item in itens]
        products = self.product_repository.get_by_ids(product_ids)
        enriched_items = []
        total = 0
        for item in itens:
            produto = products.get(item.get("produto_id"))
            quantidade = item.get("quantidade", 0)
            if not produto:
                raise NotFoundError(f"Produto {item.get('produto_id')} nao encontrado")
            if quantidade <= 0:
                raise ValidationError("Quantidade invalida")
            if produto["estoque"] < quantidade:
                raise ValidationError(f"Estoque insuficiente para {produto['nome']}")
            total += produto["preco"] * quantidade
            enriched_items.append(
                {
                    "produto_id": produto["id"],
                    "quantidade": quantidade,
                    "preco_unitario": produto["preco"],
                }
            )

        pedido_id = self.order_repository.create_order(usuario_id, total, enriched_items)
        return {"pedido_id": pedido_id, "total": total}

    def list_orders(self):
        return self._hydrate_orders(self.order_repository.list_all())

    def list_user_orders(self, usuario_id):
        if not self.user_repository.get_by_id(usuario_id):
            raise NotFoundError("Usuario nao encontrado")
        return self._hydrate_orders(self.order_repository.list_by_user(usuario_id))

    def update_status(self, pedido_id, novo_status):
        if novo_status not in self.VALID_STATUS:
            raise ValidationError("Status invalido")
        self.order_repository.update_status(pedido_id, novo_status)

    def sales_report(self):
        summary = self.order_repository.sales_summary()
        faturamento = summary["faturamento_bruto"]
        desconto = 0
        if faturamento > 10000:
            desconto = faturamento * 0.1
        elif faturamento > 5000:
            desconto = faturamento * 0.05
        elif faturamento > 1000:
            desconto = faturamento * 0.02
        summary["desconto_aplicavel"] = round(desconto, 2)
        summary["faturamento_bruto"] = round(faturamento, 2)
        summary["faturamento_liquido"] = round(faturamento - desconto, 2)
        total_pedidos = summary["total_pedidos"]
        summary["ticket_medio"] = round(faturamento / total_pedidos, 2) if total_pedidos else 0
        return summary

    def _hydrate_orders(self, rows):
        order_ids = [row["id"] for row in rows]
        grouped_items = self.order_repository.get_items_by_order_ids(order_ids)
        product_ids = [
            item["produto_id"]
            for items in grouped_items.values()
            for item in items
        ]
        products = self.product_repository.get_by_ids(product_ids)
        result = []
        for row in rows:
            order_items = []
            for item in grouped_items.get(row["id"], []):
                produto = products.get(item["produto_id"])
                order_items.append(
                    {
                        "produto_id": item["produto_id"],
                        "produto_nome": produto["nome"] if produto else "Desconhecido",
                        "quantidade": item["quantidade"],
                        "preco_unitario": item["preco_unitario"],
                    }
                )
            result.append(
                {
                    "id": row["id"],
                    "usuario_id": row["usuario_id"],
                    "status": row["status"],
                    "total": row["total"],
                    "criado_em": row["criado_em"],
                    "itens": order_items,
                }
            )
        return result
