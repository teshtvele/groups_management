#!/usr/bin/env python3
"""
Скрипт для запуска Django сервера с автоматической проверкой
"""

import subprocess
import sys
import webbrowser
import time


def main():
    print("=== Запуск Django сервера ===")
    
    try:
        # Запуск сервера
        print("Запуск сервера на http://127.0.0.1:8000...")
        print("Для остановки нажмите Ctrl+C")
        print("\nЛоги сервера:")
        print("-" * 50)
        
        # Открываем браузер через 2 секунды
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open('http://127.0.0.1:8000')
            except:
                pass
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Запуск Django сервера
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
        
    except KeyboardInterrupt:
        print("\n\nСервер остановлен")
    except subprocess.CalledProcessError as e:
        print(f"\nОшибка запуска сервера: {e}")
        print("\nПроверьте:")
        print("1. Установлены ли зависимости: pip install -r requirements.txt")
        print("2. Запущена ли база данных: docker-compose up -d")
        print("3. Применены ли миграции: python manage.py migrate")
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
