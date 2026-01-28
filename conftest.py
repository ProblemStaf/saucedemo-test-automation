import pytest
import allure
import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import tempfile


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия драйвера Firefox"""
    
    # Создаем временную директорию для профиля Firefox
    profile_dir = tempfile.mkdtemp()
    
    # Настройки Firefox
    firefox_options = FirefoxOptions()
    
    # Headless режим для CI/CD
    if os.getenv("HEADLESS", "true").lower() == "true":
        firefox_options.add_argument("--headless")
    
    # Дополнительные настройки
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")
    firefox_options.add_argument(f"--profile={profile_dir}")
    
    # Отключаем логи
    firefox_options.set_preference("devtools.console.stdout.content", True)
    firefox_options.set_preference("dom.webdriver.enabled", False)
    firefox_options.set_preference('useAutomationExtension', False)
    
    try:
        # Используем webdriver-manager для автоматического управления драйвером
        service = FirefoxService(GeckoDriverManager().install())
        driver_instance = webdriver.Firefox(service=service, options=firefox_options)
        
        # Настройки времени ожидания
        driver_instance.implicitly_wait(10)
        driver_instance.set_page_load_timeout(30)
        
        yield driver_instance
        
    except Exception as e:
        print(f"Ошибка при создании драйвера: {e}")
        pytest.skip(f"Не удалось создать драйвер Firefox: {e}")
    
    finally:
        # Закрываем драйвер после теста
        if 'driver_instance' in locals():
            try:
                driver_instance.quit()
            except:  # noqa: E722
                pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении теста"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver_fixture = item.funcargs.get('driver')
        if driver_fixture:
            try:
                # Создаем скриншот в памяти и прикрепляем к Allure
                screenshot = driver_fixture.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")