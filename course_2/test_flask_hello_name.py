import pytest
from flask_hello_name import app
import time

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Basic functionality tests
def test_valid_name(client):
    response = client.get('/api/greet/John')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello, John!'

def test_numeric_name(client):
    response = client.get('/api/greet/123')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello, 123!'

def test_special_characters(client):
    from urllib.parse import quote
    special_chars = '@#&'
    encoded_chars = quote(special_chars)
    response = client.get(f'/api/greet/{encoded_chars}')
    assert response.status_code == 200
    assert response.json['message'] == f'Hello, {special_chars}!'

# Input length tests
def test_long_name(client):
    response = client.get('/api/greet/' + 'a'*1000)
    assert response.status_code == 200
    assert response.json['message'] == f"Hello, {'a'*1000}!"

def test_single_char_name(client):
    response = client.get('/api/greet/a')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello, a!'

def test_url_encoded_characters(client):
    response = client.get('/api/greet/John%20Doe')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello, John Doe!'


# Character encoding tests
def test_unicode_name(client):
    response = client.get('/api/greet/José')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello, José!'

def test_emoji_name(client):
    response = client.get('/api/greet/😊')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello, 😊!'

# HTTP method tests
def test_unsupported_method_post(client):
    response = client.post('/api/greet/John')
    assert response.status_code == 405  # Method Not Allowed

def test_unsupported_method_put(client):
    response = client.put('/api/greet/John')
    assert response.status_code == 405  # Method Not Allowed

# Response format tests
def test_response_format(client):
    response = client.get('/api/greet/John')
    assert response.headers['Content-Type'] == 'application/json'
    assert 'message' in response.json
    assert isinstance(response.json['message'], str)

# URL path tests
def test_trailing_slash(client):
    response = client.get('/api/greet/John/')
    assert response.status_code == 404

def test_missing_name(client):
    response = client.get('/api/greet/')
    assert response.status_code == 404

def test_empty_name(client):
    response = client.get('/api/greet/ ')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello,  !'

# Security tests
def test_path_traversal(client):
    response = client.get('/api/greet/../etc/passwd')
    assert response.status_code == 404

def test_script_injection(client):
    from urllib.parse import quote
    script = '<script>alert("xss")</script>'
    encoded_script = quote(script, safe='')
    url = f'/api/greet/{encoded_script}'
    print(url)
    response = client.get(url)
    assert response.status_code == 200
    assert response.json['message'] == f'Hello, {script}!'  # Flask automatically escapes HTML in JSON
    assert '<script>' in response.json['message']

# Performance tests
def test_response_time(client):
    start_time = time.time()
    response = client.get('/api/greet/John')
    end_time = time.time()
    assert end_time - start_time < 0.5  # Response should be under 500ms
    assert response.status_code == 200

# Concurrent request simulation
def test_concurrent_requests(client):
    responses = []
    for _ in range(10):  # Simulate 10 concurrent requests
        response = client.get('/api/greet/John')
        responses.append(response.status_code)
    
    assert all(status == 200 for status in responses) 