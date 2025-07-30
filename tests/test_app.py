# tests/test_app.py
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_get_items(client):
    response = client.get('/api/items')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert len(data['items']) >= 0

def test_create_item(client):
    new_item = {
        "name": "Test Item",
        "category": "Test Category", 
        "quantity": 5,
        "price": 100000
    }
    response = client.post('/api/items', json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data['item']['name'] == new_item['name']

def test_get_single_item(client):
    response = client.get('/api/items/ITM001')
    assert response.status_code == 200
    data = response.get_json()
    assert data['item']['id'] == 'ITM001'

def test_item_not_found(client):
    response = client.get('/api/items/ITM999')
    assert response.status_code == 404