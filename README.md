# Автоматизация тестирования логина SauceDemo

Проект для автоматизированного тестирования функционала логина на сайте [SauceDemo](https://www.saucedemo.com/).

## Особенности

- Использование Selenium WebDriver для автоматизации браузера
- Реализация паттерна Page Object Model
- Интеграция с Allure для создания подробных отчетов
- Поддержка запуска в Docker контейнере
- 5 тестовых сценариев для проверки различных кейсов авторизации

## Тестовые сценарии

1. **Успешный логин** - стандартный пользователь
2. **Логин с неверным паролем** - проверка валидации
3. **Логин заблокированного пользователя** - проверка блокировки
4. **Логин с пустыми полями** - проверка обязательных полей
5. **Логин пользователя с проблемами производительности** - проверка работы при задержках

## Структура проекта

- `pages/` - Page Object классы
- `tests/` - тестовые сценарии
- `utils/` - вспомогательные утилиты
- `conftest.py` - фикстуры pytest
- `requirements.txt` - зависимости Python
- `Dockerfile` - конфигурация Docker
- `docker-compose.yml` - конфигурация Docker Compose

## Быстрый старт

### Локальная установка

1. Установите Python 3.10+
2. Установите зависимости: `pip install -r requirements.txt`
3. Установите Allure:
   - Windows: Скачайте с [официального сайта](https://github.com/allure-framework/allure2/releases)
   - macOS: `brew install allure`
   - Linux: `sudo apt-add-repository ppa:qameta/allure && sudo apt update && sudo apt install allure`
4. Запустите тесты: `pytest --alluredir=allure-results`
5. Просмотрите отчет: `allure serve allure-results`

### Запуск в Docker

1. Соберите образ: `docker build -t saucedemo-tests .`
2. Запустите тесты: `docker run --rm saucedemo-tests`

### Использование Docker Compose

1. Запустите: `docker-compose up --build`
2. Для просмотра отчета: `allure serve allure-results`

## Тестовые данные

| Пользователь | Пароль | Ожидаемый результат |
|--------------|--------|---------------------|
| standard_user | secret_sauce | Успешный вход |
| standard_user | wrong_password | Ошибка авторизации |
| locked_out_user | secret_sauce | Ошибка блокировки |
| (пусто) | (пусто) | Ошибка валидации |
| performance_glitch_user | secret_sauce | Успешный вход с задержкой |

## Генерация отчетов

Проект использует Allure для создания детальных отчетов. После запуска тестов:

```bash
# Генерация отчета
allure generate allure-results -o allure-report --clean

# Открытие отчета в браузере
allure open allure-report# saucedemo-test-automation
