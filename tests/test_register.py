import pytest, allure, requests

from curl import *

class TestRegister:
    @allure.title('Cоздать уникального пользователя')
    @allure.description('Проверка статуса 200 и success: True')  
    def test_register_original_user_success_register(self, user_registration):
        with allure.step("Отправляем запрос на создание пользователя и сохраняем ответ в response."):
            response = requests.post(REGISTER_URL, data=user_registration["payload"])
        with allure.step("Сохраняем accessToken из ответа."):
            accessToken = response.json().get("accessToken")
        with allure.step("Сохраняем success из ответа."):
            success = response.json().get("success")
        with allure.step("Передаем accessToken в фикстуру."):
            user_registration["token"].append(accessToken)
        assert response.status_code == 200 and success == True

    @allure.title('Создать пользователя, который уже зарегистрирован')
    @allure.description('Проверка статуса 403 и ответ с success: False и message: User alredy exists') 
    def test_register_registered_user_error(self, user_registration):
        with allure.step("Отправляем запрос на создание пользователя."):
            requests.post(REGISTER_URL, data=user_registration["payload"])
        with allure.step("Отправляем такой же запрос на создание пользователя и сохраняем ответ в response."):
            response = requests.post(REGISTER_URL, data=user_registration["payload"])
        with allure.step("Сохраняем accessToken из ответа."):
            accessToken = response.json().get("accessToken")
        with allure.step("Передаем accessToken в фикстуру."):
            user_registration["token"].append(accessToken)
        assert response.status_code == 403 and response.text == '{"success":false,"message":"User already exists"}'

    @allure.title('Создать пользователя и не заполнить одно из обязательных полей')
    @allure.description('Проверка статуса 403 и ответ с success: False и message: Email, password and name are required fields') 
    @pytest.mark.parametrize('data', ['email', 'password', 'name'])
    def test_register_incomplete_data_error(self, user_registration, data):
        with allure.step("Копируем тело запроса из фикстуры."):
            payload = user_registration["payload"].copy()
        with allure.step(f"Удаляем {payload[data]} из тела запроса."):
            del payload[data]
        with allure.step("Отправляем запрос на создание пользователя и сохраняем ответ в response."):
            response = requests.post(REGISTER_URL, data=payload)
        with allure.step("Сохраняем accessToken из ответа."):
            accessToken = response.json().get("accessToken")
        with allure.step("Передаем accessToken в фикстуру."):
            user_registration["token"].append(accessToken)
        assert response.status_code == 403 and response.text == '{"success":false,"message":"Email, password and name are required fields"}'