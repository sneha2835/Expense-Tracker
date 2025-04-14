import requests

BASE_URL = "http://127.0.0.1:8000/api"

def authenticate(email, password):
    url = f"{BASE_URL}/auth/login/"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()  # should contain access & refresh tokens
    else:
        return None

def save_user(email, password, username):
    url = f"{BASE_URL}/auth/register/"
    payload = {
        "email": email,
        "password": password,
        "username": username
    }
    response = requests.post(url, json=payload)
    return response.status_code == 201
