# Refactor Playbook

Use these transformation patterns during Phase 3.

## 1. Hardcoded config to settings module

Before:

```python
app.config["SECRET_KEY"] = "hardcoded"
```

After:

```python
class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
```

## 2. Raw route logic to controller

Before:

```python
@bp.post("/items")
def create_item():
    # parse, validate, save, respond
```

After:

```python
@bp.post("/items")
def create_item():
    return item_controller.create_item()
```

## 3. Controller business rules to service

Before:

```python
total = 0
for item in items:
    total += item.price * item.qty
```

After:

```python
order = order_service.create_order(payload)
```

## 4. Concatenated SQL to parameterized query

Before:

```python
cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
```

After:

```python
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## 5. Query-in-loop to bulk fetch

Before:

```python
for order in orders:
    product = repo.get_product(order.product_id)
```

After:

```python
products = repo.get_products_by_ids(product_ids)
```

## 6. Weak password hashing to standard library primitive

Before:

```python
password_hash = hashlib.md5(password.encode()).hexdigest()
```

After:

```python
password_hash = generate_password_hash(password)
```

## 7. Global mutable cache to scoped service dependency

Before:

```js
let globalCache = {};
```

After:

```js
class AuditCache {
  constructor() {
    this.entries = new Map();
  }
}
```

## 8. Monolithic manager to routes + controller + service + repository

Before:

```js
class AppManager {
  initDb() {}
  setupRoutes(app) {}
}
```

After:

```js
app.use('/api', buildRoutes({ checkoutController, reportController }));
```

## 9. Broad except to domain-aware error mapping

Before:

```python
except:
    return {"error": "Erro"}, 500
```

After:

```python
except ValidationError as exc:
    return jsonify({"error": str(exc)}), 400
```

## 10. Fat health endpoint to safe diagnostic response

Before:

```python
return {"debug": True, "secret_key": "..."}
```

After:

```python
return {"status": "ok", "database": "connected"}
```
