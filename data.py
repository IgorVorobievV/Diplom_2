import random, string, requests

from curl import *

def generate_email():
    email = f'igorvorobiev41{random.randint(100, 999)}@yandex.ru'
    return email

def generate_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for _ in range(length):
        password += random.choice(chars)
    return password

def generate_ingredients_list(length):
    response = requests.get(INGREDIENTS_URL)
    ingredients = [value['_id'] for value in response.json()['data'][:length]]
    return ingredients