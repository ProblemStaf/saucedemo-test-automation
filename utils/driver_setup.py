import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_driver():
    """Получить драйвер для тестирования"""
    browser = os.getenv("BROWSER", "firefox").lower()
    
    if browser == "chrome":
        try:
            options = ChromeOptions()
            options.add_argument("--headless")  # Добавляем headless для Chrome
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e:
            print(f"Ошибка при запуске Chrome: {e}")
            print("Переключаемся на Firefox...")
    
    # По умолчанию используем Firefox
    options = FirefoxOptions()
    options.add_argument("--headless")  # Добавляем headless для Firefox
    
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    # Настройки
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    
    return driver