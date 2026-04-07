# Custom Authentication & Authorization System

**Выполнил:** Лонин Иван    
**Технологии:** Django, DRF, PostgreSQL, JWT, bcrypt

## Описание решения

Спроектирована система разграничения доступа на основе ролей и правил. 
В отличие от стандартных решений, права задаются для каждой роли на каждый бизнес-элемент 
с возможностью разделения на «свои» и «чужие» объекты.

## Схема БД 

- `accounts_user` – пользователи (email, bcrypt-хеш, активность, внешний ключ на роль)
- `access_control_role` – роли (admin, manager, user, guest)
- `access_control_businesselement` – ресурсы (users, products, orders, access_rules)
- `access_control_accessrule` – правила (read, read_all, create, update, update_all, delete, delete_all)

Почему именно так: позволяет гибко настраивать права даже для большого количества сущностей.

## Реализованные API


| Метод   | Эндпоинт | Описание | Требует аутентификации | Проверка прав |
|---------|----------|----------|------------------------|---------------|
| POST | `/api/accounts/register/` | Регистрация нового пользователя (email, пароль, имя, фамилия) | Нет | Нет |
| POST | `/api/accounts/login/` | Вход по email и паролю, возвращает JWT-токен | Нет | Нет |
| GET | `/api/accounts/profile/` | Получить данные своего профиля | Да (JWT) | Нет (только владелец) |
| PUT | `/api/accounts/profile/` | Обновить имя/фамилию | Да (JWT) | Нет (только владелец) |
| DELETE | `/api/accounts/profile/` | Мягкое удаление аккаунта (`is_active=False`) | Да (JWT) | Нет (только владелец) |
| POST | `/api/accounts/logout/` | Выход (удаление токена на клиенте) | Да (JWT) | Нет |
| GET | `/api/access/products/` | Получить список товаров (mock) | Да | `read` на `products` |
| POST | `/api/access/products/` | Создать новый товар (mock) | Да | `create` на `products` |
| GET | `/api/access/orders/` | Получить список заказов (mock) | Да | `read` на `orders` |
| GET | `/api/access/rules/` | Получить все правила доступа (только админ) | Да | `read_all` на `access_rules` |
| POST | `/api/access/rules/` | Создать/обновить правило доступа (только админ) | Да | `create` на `access_rules` |


## Примеры тестовых запросов (с реальными ответами)

# Регистрация
curl -X POST http://127.0.0.1:8000/api/accounts/register/ -H "Content-Type: application/json" -d "{\"email\":\"user@example.com\",\"password\":\"123456\",\"password2\":\"123456\",\"first_name\":\"John\",\"last_name\":\"Doe\"}"

# Логин админа
curl -X POST http://127.0.0.1:8000/api/accounts/login/ -H "Content-Type: application/json" -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"

# Получение товаров (с токеном)
curl -X GET http://127.0.0.1:8000/api/access/products/ -H "Authorization: Bearer <ваш_токен>"

# Создание правила (админ)
curl -X POST http://127.0.0.1:8000/api/access/rules/ -H "Content-Type: application/json" -H "Authorization: Bearer <токен_админа>" -d "{\"role\":\"user\",\"element\":\"products\",\"can_read\":true,\"can_create\":true}"

## Запуск проекта

- pip install -r requirements.txt

- python -m venv venv

- venv\Scripts\activate  # Windows

## Setup

```bash
# Create database in PostgreSQL
createdb -U postgres auth_db

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Seed data
python manage.py seed_data

# Run server
python manage.py runserver