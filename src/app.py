# src/app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Data dummy
items = [
    {"id": "ITM001", "name": "Laptop Dell", "category": "Electronics", "quantity": 10, "price": 15000000},
    {"id": "ITM002", "name": "Mouse Logitech", "category": "Electronics", "quantity": 25, "price": 350000},
    {"id": "ITM003", "name": "Keyboard Mechanical", "category": "Electronics", "quantity": 15, "price": 750000}
]

@app.route('/')
def home():
    return {"message": "Welcome to TechNova Inventory API", "status": "running"}

@app.route('/health')
def health():
    return {"status": "healthy", "service": "inventory-api", "version": "1.0.0"}

@app.route('/api/items', methods=['GET'])
def get_items():
    return {"items": items, "total": len(items), "status": "success"}

@app.route('/api/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return {"item": item, "status": "success"}
    return {"error": "Item not found", "status": "error"}, 404

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    
    if not data or not all(k in data for k in ("name", "category", "quantity", "price")):
        return {"error": "Missing required fields", "status": "error"}, 400
    
    new_item = {
        "id": f"ITM{len(items)+1:03d}",
        "name": data["name"],
        "category": data["category"],
        "quantity": data["quantity"],
        "price": data["price"]
    }
    items.append(new_item)
    return {"item": new_item, "status": "created"}, 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
