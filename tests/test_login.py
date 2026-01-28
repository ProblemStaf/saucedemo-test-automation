import pytest
import allure
from pages.login_page import LoginPage


@allure.feature("Авторизация")
@allure.story("Проверка логина на сайте SauceDemo")
class TestLogin:

    @allure.title("Тест 1: Успешная авторизация с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка успешного входа стандартного пользователя")
    def test_successful_login(self, driver):
        """Тест успешного логина стандартного пользователя"""
        login_page = LoginPage(driver)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Проверить загрузку страницы"):
            assert login_page.is_page_loaded(), "Страница логина не загрузилась"
            
        with allure.step("3. Выполнить логин с валидными данными"):
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("4. Проверить переход на страницу инвентаря"):
            assert login_page.is_inventory_page_loaded(), "Страница инвентаря не загрузилась"
            
        with allure.step("5. Проверить URL страницы"):
            current_url = login_page.get_current_url()
            assert current_url, "URL не определен"
            assert "inventory" in current_url, f"Некорректный URL: {current_url}"
            
        with allure.step("6. Проверить заголовок страницы"):
            page_title = login_page.get_page_title()
            assert page_title == "Swag Labs", f"Некорректный заголовок: {page_title}"

    @allure.title("Тест 2: Авторизация с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка логина с неверным паролем")
    def test_invalid_password_login(self, driver):
        """Тест логина с неверным паролем"""
        login_page = LoginPage(driver)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Выполнить логин с неверным паролем"):
            login_page.login("standard_user", "wrong_password")
            
        with allure.step("3. Проверить сообщение об ошибке"):
            assert login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
            
            error_message = login_page.get_error_message()
            assert error_message, "Сообщение об ошибке не получено"
            
            expected_message = "Epic sadface: Username and password do not match any user in this service"
            assert error_message == expected_message, \
                f"Ожидалось: '{expected_message}', получено: '{error_message}'"
            
        with allure.step("4. Проверить, что остались на странице логина"):
            current_url = login_page.get_current_url()
            assert current_url == "https://www.saucedemo.com/", \
                f"Произошел переход на другую страницу: {current_url}"

    @allure.title("Тест 3: Авторизация заблокированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка логина заблокированного пользователя")
    def test_locked_out_user_login(self, driver):
        """Тест логина заблокированного пользователя"""
        login_page = LoginPage(driver)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Выполнить логин заблокированного пользователя"):
            login_page.login("locked_out_user", "secret_sauce")
            
        with allure.step("3. Проверить сообщение об ошибке"):
            assert login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
            
            error_message = login_page.get_error_message()
            assert error_message, "Сообщение об ошибке не получено"
            
            expected_message = "Epic sadface: Sorry, this user has been locked out."
            assert error_message == expected_message, \
                f"Ожидалось: '{expected_message}', получено: '{error_message}'"
            
        with allure.step("4. Проверить возможность закрыть ошибку"):
            login_page.close_error_message()
            assert not login_page.is_error_displayed(), "Сообщение об ошибке не закрылось"

    @allure.title("Тест 4: Авторизация с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка логина с пустыми полями")
    def test_empty_fields_login(self, driver):
        """Тест логина с пустыми полями"""
        login_page = LoginPage(driver)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Нажать кнопку логина без ввода данных"):
            login_page.click_login()
            
        with allure.step("3. Проверить сообщение об ошибке"):
            assert login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
            
            error_message = login_page.get_error_message()
            assert error_message, "Сообщение об ошибке не получено"
            
            expected_message = "Epic sadface: Username is required"
            assert error_message == expected_message, \
                f"Ожидалось: '{expected_message}', получено: '{error_message}'"

    @allure.title("Тест 5: Авторизация пользователя с проблемами производительности")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка логина пользователя performance_glitch_user с задержками")
    def test_performance_glitch_user_login(self, driver):
        """Тест логина пользователя с задержками"""
        login_page = LoginPage(driver)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Проверить загрузку страницы логина"):
            assert login_page.is_page_loaded(), "Страница логина не загрузилась"
            
        with allure.step("3. Выполнить логин пользователя performance_glitch_user"):
            login_page.login("performance_glitch_user", "secret_sauce")
            
        with allure.step("4. Проверить загрузку страницы инвентаря (с увеличенным таймаутом)"):
            # Увеличиваем таймаут для пользователя с проблемами производительности
            assert login_page.is_inventory_page_loaded(timeout=30), \
                "Страница инвентаря не загрузилась в течение 30 секунд"
            
        with allure.step("5. Проверить корректный URL"):
            current_url = login_page.get_current_url()
            assert current_url, "URL не определен"
            assert "inventory" in current_url, f"Некорректный URL: {current_url}"
            
        with allure.step("6. Проверить наличие элементов на странице инвентаря"):
            # Проверяем, что основные элементы отображаются
            assert login_page.driver.find_element(*LoginPage.INVENTORY_CONTAINER).is_displayed()
            assert login_page.driver.find_element(*LoginPage.PRODUCTS_TITLE).is_displayed()
            assert login_page.driver.find_element(*LoginPage.SHOPPING_CART).is_displayed()