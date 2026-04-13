import pytest, allure, requests

from curl import *
from data import *

@pytest.fixture # фикстура, которая содает пользователя и удаляет его после теста
def user_registration():

    with allure.step("Создаем пустой список token для передачи в тест и возврата с accessToken."):
        token = list()

    with allure.step("Генерируем email, пароль и имя пользователя и сохраняем в переменную тела запроса payload."):
        payload = {"email": generate_email(), "password": generate_password(8), "name": generate_password(6)}

    with allure.step("Собираем все в data для передачи в тест."):
        data = {"payload": payload, "token": token}

    with allure.step("Передаем тело запроса в тест."):
        yield data
    
    try:
        with allure.step("Отпраляем запрос на удаление пользователя."):
            requests.delete(USER_URL, headers={'Authorization': token[0]}, data=payload)

    except Exception as e:
        pass

@pytest.fixture # фикстура, которая содает пользователя и удаляет его после теста
def user_login():

    with allure.step("Создаем пустой список token для передачи в тест и возврата с accessToken."):
        token = list()

    with allure.step("Генерируем email, пароль и имя пользователя и сохраняем в переменную тела запроса payload."):
        payload = {"email": generate_email(), "password": generate_password(8), "name": generate_password(6)}

    with allure.step("Собираем все в data для передачи в тест."):
        data = {"payload": payload, "token": token}

    with allure.step("Отправляем запрос на создание пользователя и сохраняем ответ в response."):
        response = requests.post(REGISTER_URL, data=payload)

    with allure.step("Сохраняем accessToken из ответа."):
        accessToken = response.json().get("accessToken")
        data["token"].append(accessToken)

    with allure.step("Передаем тело запроса в тест."):
        yield data
    
    try:
        with allure.step("Отпраляем запрос на удаление пользователя."):
            requests.delete(USER_URL, headers={'Authorization': accessToken}, data=payload)

    except Exception as e:
        pass