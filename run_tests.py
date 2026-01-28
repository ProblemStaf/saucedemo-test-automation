#!/usr/bin/env python3
import subprocess
import sys

def run_tests():
    """Запуск тестов без Allure"""
    # Команда для запуска pytest без Allure
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_login.py",
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    print(f"Запуск команды: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Ошибка при запуске тестов: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())