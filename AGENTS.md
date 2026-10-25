# AGENTS.md

## Обзор проекта

OrderFlow_Microservices — учебный монорепозиторий микросервисного e-commerce приложения на Python/FastAPI.

## Структура проекта

```
OrderFlow_Microservices/
├── pyproject.toml / poetry.lock   # единый Poetry-проект на весь репозиторий
├── docker-compose.yml             # сервисы + PostgreSQL
├── catalog_service/               # каталог товаров (наиболее полный сервис)
│   ├── app/
│   │   ├── main.py                # FastAPI app, lifespan (init_db), CORS, static
│   │   ├── config.py              # pydantic-settings
│   │   ├── database.py            # async engine, SessionLocal, Base, get_db
│   │   ├── models/                # product.py, category.py
│   │   ├── schemas/               # product.py, category.py
│   │   ├── repositories/          # product_repository.py, category_repository.py
│   │   ├── services/              # product_service.py, category_service.py
│   │   └── routers/               # product.py, category.py
│   ├── Dockerfile
│   └── .env
├── order_service/                 # заказы и корзина (в разработке)
│   ├── app/
│   │   ├── main.py                # импортирует несуществующие routers/cart.py, routers/order.py
│   │   ├── config.py, database.py
│   │   ├── models/                # order.py, order_item.py
│   │   ├── schemas/               # order.py, order_item.py, cart.py
│   │   ├── repository/            # order_repository.py, order_item_repository.py
│   │   ├── routers/               # пусто (только __init__.py)
│   │   └── services/              # пусто
│   ├── Dockerfile
│   └── .env
├── payment_service/               # заглушка (.gitkeep)
├── notification_service/          # заглушка (.gitkeep)
├── analytics_service/             # заглушка (.gitkeep)
├── frontend/                      # заглушка (.gitkeep)
└── infra/                         # заглушка (.gitkeep)
```

## Стек технологий

- **Python 3.14** (`requires-python >= 3.14`)
- **FastAPI** (0.142.x) + **Uvicorn** (0.54.x)
- **SQLAlchemy 2.1** — полностью async (`AsyncSession`, `asyncpg`)
- **PostgreSQL 16** (alpine, через docker-compose)
- **Pydantic v2** + **pydantic-settings** — схемы и конфигурация
- **asyncpg** — асинхронный драйвер Postgres
- **Poetry** — управление зависимостями (один pyproject.toml на всё монорепозиторий)
- **Docker / docker-compose** — сборка и оркестрация
- **python-dotenv**, **httpx** (межсервисные вызовы), **greenlet**

## Архитектурные соглашения

- Layered architecture внутри каждого сервиса: `routers -> services -> repositories -> models`
- Каждый сервис имеет собственную БД (pattern: `<service>_db` в compose)
- Общая база `Base` в `database.py`: `__tablename__` генерируется автоматически из имени модели (lowercase + `s`), PK — `id: int`
- `init_db()` через `Base.metadata.create_all` в lifespan-хуке (миграции Alembic пока не используются)
- Конфигурация через `pydantic-settings`, значения из `.env` каждого сервиса
- Эндпоинты `/` и `/health` присутствуют в каждом сервисе

## Известные проблемы (учитывать при работе)

- `order_service/app/main.py` импортирует несуществующие `routers/cart.py` и `routers/order.py`; `include_router(...)` — заглушки (сервис не запустится, пока роутеры не написаны)
- `order_service/static` — симлинк на `../catalog_service/static` (данные не дублируются)
- Смешаны относительные (`from ..app.`) и абсолютные (`from catalog_service.app.`) импорты

## Команды

```bash
poetry install                      # установка зависимостей
docker compose up --build           # запуск сервисов и БД
# catalog_service: http://localhost:8000, order_service: http://localhost:8001
```
