import pytest, allure, requests

from curl import *

class TestLogin:
    @allure.title('Вход под существующим пользователем')
    @allure.description('Проверка статуса 200 и success: True')  
    def test_login_existed_user_success_login(self, user_login):
        with allure.step("Извлекаем токен из фикстуры."):
            accessToken = user_login['token'][0]
        with allure.step("Копируем тело запроса из фикстуры."):
            payload = user_login['payload'].copy()
        with allure.step("Удаляем имя из запроса."):
            del payload['name']
        with allure.step("Отправляем запрос на авторизацию пользователя и сохраняем ответ в response."):
            response = requests.post(LOGIN_URL, headers={'Authorization': accessToken}, data=payload)

        assert response.status_code == 200 and '"success":true' in response.text

    @allure.title('Вход под существующим пользователем с отсутствующим логином или паролем')
    @allure.description('Проверка статуса 401 и message: email or password are incorrect')  
    @pytest.mark.parametrize('userdata', ['email', 'password'])
    def test_login_incomplete_data_error(self, user_login, userdata):
        with allure.step("Извлекаем токен из фикстуры."):
            accessToken = user_login['token'][0]
        with allure.step("Копируем тело запроса из фикстуры."):
            payload = user_login['payload'].copy()
        with allure.step(f"Удаляем {payload[userdata]} из тела запроса."):
            del payload[userdata]
        with allure.step("Отправляем запрос на авторизацию пользователя и сохраняем ответ в response."):
            response = requests.post(LOGIN_URL, headers={'Authorization': accessToken}, data=payload)

        assert response.status_code == 401 and response.text == '{"success":false,"message":"email or password are incorrect"}'

    @allure.title('Вход под существующим пользователем с неверным логином или паролем "wrongdata"')
    @allure.description('Проверка статуса 401 и message: email or password are incorrect')  
    @pytest.mark.parametrize('userdata', ['email', 'password'])
    def test_login_wrong_data_error(self, user_login, userdata):
        with allure.step("Извлекаем токен из фикстуры."):
            accessToken = user_login['token'][0]
        with allure.step("Копируем тело запроса из фикстуры."):
            payload = user_login['payload'].copy()
        with allure.step(f"Меняем {payload[userdata]} в теле запроса."):
            payload[userdata] = 'wrongdata'
        with allure.step("Отправляем запрос на авторизацию пользователя и сохраняем ответ в response."):
            response = requests.post(LOGIN_URL, headers={'Authorization': accessToken}, data=payload)

        assert response.status_code == 401 and response.text == '{"success":false,"message":"email or password are incorrect"}'