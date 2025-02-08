[![Lint Check](https://github.com/Bojchenko-Konstantin/cafe_order_system/actions/workflows/lint-check.yml/badge.svg)](https://github.com/Bojchenko-Konstantin/cafe_order_system/actions/workflows/lint-check.yml)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Bojchenko-Konstantin_cafe_order_system&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Bojchenko-Konstantin_cafe_order_system)
# Система управления заказами в кафе

## Описание

Это веб-приложение на Django для управления заказами в кафе. Оно позволяет:
- Создавать, редактировать, удалять и просматривать заказы.
- Добавлять блюда из меню в заказы.
- Фильтровать заказы по статусу.
- Рассчитывать итоговую стоимость заказа.
- Управлять позициями из меню через админку.

Приложение построено с использованием принципов чистой архитектуры, что позволяет разделить код на слои: **entities**, **use cases**, **repositories**, **views**, **models** и **templates**. 
Это способствует безболезненному переходу на другой фреймворк при необходимости, обеспечивает возможность масштабирования приложения, а также значительно упрощает процесс тестирования.

---

## Архитектура проекта

Проект построен на основе **чистой архитектуры** (Clean Architecture) и разделен на следующие слои:

### 1. **Entities (Сущности)**
   - Описывают основные бизнес-объекты: `Order`, `MenuItem`, `OrderItem`.
   - Находятся в файле `entities.py`.
   - Пример:
     ```python
     @dataclass
     class MenuItem:
         name: str
         price: Decimal
     ```

### 2. **Use Cases (Сценарии использования)**
   - Содержат бизнес-логику приложения.
   - Пример: `CreateOrderUseCase`, `UpdateOrderStatusUseCase`.
   - Находятся в файле `use_cases.py`.

### 3. **Repositories (Репозитории)**
   - Обеспечивают доступ к данным (работа с базой данных).
   - Пример: `OrderRepository`.
   - Находятся в файле `repositories.py`.

### 4. **Views (Представления)**
   - Обрабатывают HTTP-запросы и возвращают ответы.
   - Используют use cases и репозитории.
   - Находятся в файле `views.py`.

### 5. **Templates (Шаблоны)**
   - Отвечают за отображение данных в веб-интерфейсе.
   - Используют Bootstrap 5 для стилизации.
   - Находятся в директории `templates/orders/`.

### 6. **Models (Модели)** 
   - Cлужат для представления структуры данных, которые приложение будет использовать.
   - Определяют, какие поля и типы данных будут храниться.
   - Находятся в файле `models.py`.

---

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Bojchenko-Konstantin/cafe_order_system.git
cd cafe_order_system
```
### 2. Установите зависимости

```bash
poetry install
```

### 3. Скройте чувствительные данные в переменных окружения

В директории `config` скопировать содержимое файла `.env.example` в файл `.env` и указать в нём актуальные настройки.

### 4. Настройте базу данных (опционально)

По умолчанию используется SQLite. Если хотите использовать PostgreSQL, измените настройки в `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Примените миграции

```bash
python manage.py migrate
```

### 6. Создайте суперпользователя (для доступа к админке)

```bash
python manage.py createsuperuser
```

### 7. Запустите сервер

```bash
python manage.py runserver
```
Перейдите по адресу `http://127.0.0.1:8000/`, чтобы открыть приложение.

---

## Запуск тестов

Тесты покрывают слои `models`, `use_cases`, `repositories` и `views`. Чтобы запустить тесты, выполните

```bash
python manage.py test orders.tests
```

## Использование админки

Перейдите в админку: `http://127.0.0.1:8000/admin/`.
Войдите с учетными данными суперпользователя.
Управляйте позициями из меню (`MenuItems`) и заказами (`Orders`) через удобный интерфейс.

### Как добавить новую позицию из меню в административной панели

Откройте раздел `MenuItems`.

Нажмите `Add MenuItem`.

Введите название и стоимость позиции из меню.
Сохраните.

### Как добавить позицию в заказ
Перейдите на страницу создания заказа: `http://127.0.0.1:8000/orders/create/`.

Выберите позицию из выпадающего списка и укажите количество.
Нажмите `Save`.

## API

Приложение предоставляет REST API для работы с заказами:

    - Получить список заказов: `GET /api/orders/`
    - Создать заказ: `POST /api/orders/`
    - Получить детали заказа: `GET /api/orders/<order_id>/`
    - Обновить заказ: `PUT /api/orders/<order_id>/`
    - Удалить заказ: `DELETE /api/orders/<order_id>/`

Пример запроса:
```bash
curl -X GET http://127.0.0.1:8000/api/orders/
```



