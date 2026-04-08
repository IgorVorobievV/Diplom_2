import pytest, allure, requests

from curl import *
from data import *

class TestMakeOrder:
    @allure.title('Создание заказа с авторизацией и ингредиентами')
    @allure.description('Проверка статуса 200 и success: True и email авторизованного пользователя с авторизацией и 3-мя ингредиентами')
    def test_make_order_with_auth_and_with_ingredients_success_order(self, user_login):
        with allure.step("Извлекаем токен из фикстуры."):
            accessToken = user_login['token'][0]
        with allure.step("Извлекаем email из фикстуры."):
            email = user_login['payload']['email']
        with allure.step("Создаем тело запроса с ingredients."):
            payload = {"ingredients": generate_ingredients_list(3)}
        with allure.step("Отправляем запрос на создание заказа."):
            response = requests.post(ORDERS_URL, headers={'Authorization': accessToken}, data=payload)

        assert response.status_code == 200 and '"success":true' in response.text and response.json()['order']['owner']['email'] == email 

    @allure.title('Создание заказа без авторизацией и ингредиентами')
    @allure.description('Проверка статуса 200 и success: True без авторизации с 3-мя ингредиентом')  
    def test_make_order_without_auth_and_with_ingredients_success_order(self):
        with allure.step("Создаем тело запроса с ingredients."):
            payload = {"ingredients": generate_ingredients_list(3)}
        with allure.step("Отправляем запрос на создание заказа."):
            response = requests.post(ORDERS_URL, data=payload)

        assert response.status_code == 200 and '"success":true' in response.text

    @allure.title('Создание заказа с авторизацией и без ингредиентов')
    @allure.description('Проверка статуса 400, success: false и message: Ingredient ids must be provided с авторизацией и без ингредиентов')
    def test_make_order_with_auth_and_without_ingredients_error_400(self, user_login):
        with allure.step("Извлекаем токен из фикстуры."):
            accessToken = user_login['token'][0]
        with allure.step("Извлекаем email из фикстуры."):
            email = user_login['payload']['email']
        with allure.step("Создаем тело запроса с ingredients."):
            payload = {"ingredients": []}
        with allure.step("Отправляем запрос на создание заказа."):
            response = requests.post(ORDERS_URL, headers={'Authorization': accessToken}, data=payload)

        assert response.status_code == 400 and response.text == '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title('Создание заказа без авторизации и без ингредиентов')
    @allure.description('Проверка статуса 400, success: false и message: Ingredient ids must be provided без авторизации и без ингредиентов')  
    def test_make_order_without_auth_and_without_ingredients_error_400(self):
        with allure.step("Создаем тело запроса с ingredients."):
            payload = {"ingredients": []}
        with allure.step("Отправляем запрос на создание заказа."):
            response = requests.post(ORDERS_URL, data=payload)
        assert response.status_code == 400 and response.text == '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title('Создание заказа с авторизацией и неверным хешем ингредиентов')
    @allure.description('Проверка статуса 500 с авторизацией и неверным хешем ингредиентов')
    def test_make_order_with_auth_and_wrong_ingredients_error_500(self, user_login):
        with allure.step("Извлекаем токен из фикстуры."):
            accessToken = user_login['token'][0]
        with allure.step("Извлекаем email из фикстуры."):
            email = user_login['payload']['email']
        with allure.step("Создаем тело запроса с ingredients."):
            payload = {"ingredients": [generate_password(8)]}
        with allure.step("Отправляем запрос на создание заказа."):
            response = requests.post(ORDERS_URL, headers={'Authorization': accessToken}, data=payload)

        assert response.status_code == 500

    @allure.title('Создание заказа без авторизации и неверным хешем ингредиентов')
    @allure.description('Проверка статуса 500 без авторизации и неверным хешем ингредиентов')  
    def test_make_order_without_auth_and_wrong_ingredients_error_500(self):
        with allure.step("Создаем тело запроса с ingredients."):
            payload = {"ingredients": [generate_password(8)]}
        with allure.step("Отправляем запрос на создание заказа."):
            response = requests.post(ORDERS_URL, data=payload)

        assert response.status_code == 500