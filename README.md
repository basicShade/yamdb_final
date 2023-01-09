# api_yamdb    <img src="https://github.com/basicshade/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg" />
* ~~Главная страница: http://basicshade.ddns.net/api/v1/~~
* ~~Документация: http://basicshade.ddns.net/redoc/~~


### Описание
api_yamdb - учебный командный проект по созданию web API с использованием Django REST Framework. Данное API предоставляет досутуп к базе данных произведений искусства, разделенных по категориям. Модель позволяет добавлять к произведениям обзоры и оставлять комментарии к обзорам. Эндпоинты настроены на CRUD запросы к основной модели произведений и к модели пользователя (в кастомизированной модели пользователь получает права доступа к тем или иным эндпоинтам в зависимости от его роли). Для аутентификации используется SimpleJWT токен. Реализована процедура автоматического запуска тестов и развертывания приложения с использованием сервиса GitHub Actions.

### Используемые технологии
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" /> <img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white" /> <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" />

    - Python 3.7
    - Django 2.2.16
    - Django REST framework 3.12.4
    - Simple JWT 4.7.2
    - Gunicorn 20.0.4
    - Docker 4.6.1


### Запуск проекта ⚙️
1. В терминале клонировать репозиторий и перейти в папку infra:
    ```
    git clone git@github.com:basicShade/api_yamdb.git
    cd api_yamdb/infra/
    ```
2. В папке infra создать .env файл по шаблону 🔒
    ```
    DB_ENGINE=...
    DB_NAME=...
    POSTGRES_USER=...
    POSTGRES_PASSWORD=...
    DB_HOST=...
    DB_PORT=...
    SECRET_KEY=...
    ```

3. Запустить docker-compose:
    ```
    docker-compose -p api_yamdb up --build -d
    ```

4. Выполнить миграции, загрузить статику и данные, создать суперпользователя:
    ```
    docker-compose -p api_yamdb exec web python manage.py migrate --run-syncdb
    docker-compose -p api_yamdb exec web python manage.py collectstatic --no-input
    docker-compose -p api_yamdb exec web python manage.py load_data
    docker-compose -p api_yamdb exec web python manage.py createsuperuser
    ```

После запуска сервера начните с главной страницы: http://127.0.0.1/api/v1

Redoc документация будет доступна по ссылке: http://127.0.0.1/redoc/


### Планы по доработке
Настроить API для работы с изображениями

### Авторы
```
Студенты факультета Бэкенд. Когорта №40. Команда 23.
    - Вагурин Максим
    - Кирилл Клепиков
    - Орлов Алексей
```
