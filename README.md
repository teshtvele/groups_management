# Система управления людишками с персистентностью

Django-приложение для управления записями о людях с автоматической дедубликацией и поддержкой персистентности.

### REST API
- `POST /api/persons/` - создание человека
- `GET /api/persons/list/` - список всех людей
- `GET /api/persons/search/` - поиск в витрине
- `GET /api/persons/{group_id}/as-of/` - состояние на момент времени

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск базы данных

```bash
docker-compose up -d
```

### 3. Применение миграций

```bash
.venv/bin/python manage.py migrate                
```

### 4. Загрузка SQL скрипта с функциями

```bash
.venv/bin/python manage.py load_sql_script
```

### 5. Создание суперпользователя

```bash
.venv/bin/python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
.venv/bin/python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

## Использование

### Веб-интерфейс
- `/` - главная страница
- `/create/` - форма добавления человека
- `/list/` - список всех людей с поиском
- `/admin/` - админ-панель Django

## Структура базы данных

### Основные таблицы
- `person_group` - группы людей для дедубликации
- `person` - текущие записи о людях
- `person_history` - история изменений
- `change_set` - наборы изменений (коммиты)
