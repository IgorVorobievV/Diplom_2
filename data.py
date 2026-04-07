import random
import string

def generate_email():
    email = f'igorvorobiev41{random.randint(100, 999)}@yandex.ru'
    return email

def generate_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for _ in range(length):
        password += random.choice(chars)
    return password

right_email = 'igorvorobiev41002@yandex.ru'
right_pass = 'HT9-TTW-sJw-aHJ'

wrong_email = 'yandex.ru'
wrong_pass = 'HT9-T'