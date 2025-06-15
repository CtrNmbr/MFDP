# ML Service

Проект представляет собой микросервисное приложение для обработки ML задач с использованием очередей сообщений по предсказанию фродовости транзакции.

## Структура проекта

```
.
├── app/                    # Основное приложение и Веб-интерфейс
│   ├── src/               # Исходный код
│   │   ├── api.py        # API endpoints
│   │   ├── worker.py     # Обработчик задач
│   │   ├── routes/       # Маршруты API
│   │   ├── services/     # Бизнес-логика
│   │   ├── database/     # Работа с БД
│   │   └── base/         # Ядро приложения
│   └── tests/            # Тесты
├── nginx/                 # Конфигурация NGINX
└── docker-compose.yaml    # Конфигурация Docker
```

## Компоненты системы

- **API Service (app)**: REST API сервис
- **Worker Service**: Обработчик ML задач
- **Web UI**: Пользовательский интерфейс на StreamLit
- **RabbitMQ**: Брокер сообщений
- **PostgreSQL**: База данных
- **NGINX**: Прокси-сервер

## Требования

- Docker
- Docker Compose

## Запуск проекта

1. Создайте файл с переменными окружения (за основу нужно взять шаблон .env.template):

Актуальные шаблоны смотрите в файлах .env.template

Для локальной разработки:
```bash
# app/.env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=ml-practice

JWT_SECRET_KEY=REPLACETHISSECRETINPROD

RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```
Для запуска docker-compose
```bash
# app/.env
DB_HOST=database
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=ml-practice

JWT_SECRET_KEY=REPLACETHISSECRETINPROD

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

2. Запустите сервисы:

```bash
docker-compose up -d
```

После запуска будут доступны:

- Web UI: http://localhost:8085
- API: http://localhost:80
- RabbitMQ Management: http://localhost:15672
- PostgreSQL: localhost:5432

## Масштабирование

Worker-сервис настроен на автоматическое масштабирование (2 реплики по умолчанию). Для изменения количества реплик:

```bash
docker-compose up -d --scale worker=4
```

## Мониторинг

- RabbitMQ Management UI (http://localhost:15672)
  - Login: guest
  - Password: guest
    (если не переопределено в .env)

## Разработка

Для локальной разработки можно использовать volumes:
- Код приложения монтируется в `/app`

## Тестирование

```bash
# Запуск всех тестов из контейнера app
docker-compose exec app pytest tests
```
```bash
# Запуск конкретного модуля тестов
docker-compose exec app pytest tests/api/test_ml_model_routes.py
```

```bash
# Запуск тестов с подробным выводом
docker-compose exec app pytest tests -v
```

Структура тестов:
```
tests/
├── api/                    # Тесты API endpoints
└── services/              # Тесты сервисного слоя
```

## Данные

Все данные (PostgreSQL и RabbitMQ) сохраняются в Docker volumes:
- postgres_data
- rabbitmq_data