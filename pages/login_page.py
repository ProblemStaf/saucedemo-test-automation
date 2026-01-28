from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure


class LoginPage:
    """Page Object для страницы логина SauceDemo"""
    
    # Локаторы элементов
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_BUTTON = (By.CLASS_NAME, "error-button")
    LOGO = (By.CLASS_NAME, "login_logo")
    BOT_COLUMN = (By.CLASS_NAME, "bot_column")
    
    # Локаторы для страницы инвентаря (после успешного логина)
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    SHOPPING_CART = (By.CLASS_NAME, "shopping_cart_link")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    @allure.step("Открыть страницу логина")
    def open(self):
        """Открыть страницу логина"""
        self.driver.get("https://www.saucedemo.com/")
        return self
        
    @allure.step("Проверить загрузку страницы логина")
    def is_page_loaded(self):
        """Проверить, загрузилась ли страница"""
        try:
            self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
            self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
            self.wait.until(EC.presence_of_element_located(self.LOGIN_BUTTON))
            return True
        except TimeoutException:
            return False
            
    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username):
        """Ввести имя пользователя"""
        element = self.wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT))
        element.clear()
        element.send_keys(username)
        return self
        
    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password):
        """Ввести пароль"""
        element = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        element.clear()
        element.send_keys(password)
        return self
        
    @allure.step("Нажать кнопку входа")
    def click_login(self):
        """Нажать кнопку входа"""
        element = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        element.click()
        return self
        
    @allure.step("Выполнить логин с именем: {username} и паролем: {password}")
    def login(self, username, password):
        """Выполнить полный процесс логина"""
        return (self.enter_username(username)
                   .enter_password(password)
                   .click_login())
        
    @allure.step("Получить текст сообщения об ошибке")
    def get_error_message(self):
        """Получить текст сообщения об ошибке"""
        try:
            # Даем время для появления ошибки
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            element = self.driver.find_element(*self.ERROR_MESSAGE)
            return element.text
        except (TimeoutException, NoSuchElementException):
            return None
            
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url
        
    @allure.step("Проверить загрузку страницы инвентаря")
    def is_inventory_page_loaded(self, timeout=15):
        """Проверить, загрузилась ли страница инвентаря после успешного логина"""
        try:
            # Используем несколько критериев для надежности
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.INVENTORY_CONTAINER)
            )
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PRODUCTS_TITLE)
            )
            
            # Также проверяем URL
            current_url = self.driver.current_url
            if current_url and "inventory" in current_url:
                return True
            
            # Дополнительная проверка по тексту
            title_element = self.driver.find_element(*self.PRODUCTS_TITLE)
            if title_element.text == "Products":
                return True
                
            return False
        except (TimeoutException, NoSuchElementException):
            return False
    
    @allure.step("Проверить наличие ошибки авторизации")
    def is_error_displayed(self):
        """Проверить, отображается ли сообщение об ошибке"""
        try:
            error_element = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_element.is_displayed()
        except NoSuchElementException:
            return False
    
    @allure.step("Получить заголовок страницы")
    def get_page_title(self):
        """Получить заголовок страницы"""
        return self.driver.title
    
    @allure.step("Закрыть сообщение об ошибке")
    def close_error_message(self):
        """Закрыть сообщение об ошибке"""
        try:
            error_button = self.driver.find_element(*self.ERROR_BUTTON)
            error_button.click()
            return True
        except NoSuchElementException:
            return False