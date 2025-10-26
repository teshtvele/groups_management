#!/usr/bin/env python3
"""
Скрипт для быстрого запуска проекта
"""

import subprocess
import sys
import time
import os


def run_command(command, description):
    """Выполнение команды с описанием"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} - выполнено")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка при {description.lower()}: {e.stderr}")
        return False


def main():
    print("=== Запуск системы управления людьми ===")
    
    # Проверка существования файлов
    if not os.path.exists('manage.py'):
        print("Ошибка: manage.py не найден. Убедитесь, что вы находитесь в корне проекта.")
        sys.exit(1)
    
    if not os.path.exists('.env'):
        print("Создание файла конфигурации...")
        subprocess.run('cp .env.example .env', shell=True)
    
    # Запуск PostgreSQL
    print("\n1. Запуск базы данных...")
    if not run_command("docker-compose up -d", "Запуск PostgreSQL"):
        print("Попробуйте выполнить: docker-compose up -d")
        sys.exit(1)
    
    # Ожидание запуска БД
    print("Ожидание запуска базы данных...")
    time.sleep(5)
    
    # Проверка подключения к БД
    if not run_command("python manage.py check --database default", "Проверка подключения к БД"):
        print("Ошибка подключения к базе данных")
        sys.exit(1)
    
    # Миграции
    if not run_command("python manage.py migrate", "Применение миграций"):
        print("Ошибка при применении миграций")
        sys.exit(1)
    
    # Загрузка SQL скрипта
    if not run_command("python manage.py load_sql_script", "Загрузка SQL скрипта"):
        print("Предупреждение: Не удалось загрузить SQL скрипт")
    
    # Сбор статических файлов
    run_command("python manage.py collectstatic --noinput", "Сбор статических файлов")
    
    print("\n=== Система готова к работе! ===")
    print("\nДля запуска сервера выполните:")
    print("  python manage.py runserver")
    print("\nИли запустите start_server.py для автоматического запуска")


if __name__ == "__main__":
    main()
