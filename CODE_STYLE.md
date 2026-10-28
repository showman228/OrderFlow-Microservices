# Code Style Guide

This document is the mandatory standard for code in this project (Python + FastAPI microservice).
Before writing or modifying code, read it in full. If a requirement below conflicts with the user's request, say so and ask for clarification instead of silently violating the rule.

---

## 1. Stack and versions

- Python **3.12+**
- FastAPI, Pydantic **v2** (do not use v1 syntax: `validator`, `.dict()`, `class Config`)
- SQLAlchemy **2.0** (async, `select()` style, `Mapped[]`) + Alembic
- `pydantic-settings` for configuration
- `pytest` + `pytest-asyncio` + `httpx.AsyncClient` for tests
- Dependency manager: `uv` / `poetry` (use whichever is specified in `pyproject.toml`)

> Do not add new dependencies unless necessary. If a library is needed, name it and explain why.

---

## 2. General principles

1. **Readability over brevity.** Code is read more often than it is written.
2. **Explicit over implicit.** No magic, hidden side effects, or global state.
3. **One function, one responsibility.** If a function is longer than ~40 lines or does "this and that", split it.
4. **Don't reinvent the wheel.** First check whether the standard library, FastAPI, or existing project code already solves the problem.
5. **Follow existing code.** If the project already has a pattern, use it instead of introducing your own.
6. **Minimal diff.** Change only what the task requires. Do not reformat or refactor unrelated code.
7. **No dead code:** commented-out blocks, unused imports, debug `print` calls.

---

## 3. Project structure

```
app/
├── main.py                # FastAPI app creation, router registration, lifespan
├── core/
│   ├── config.py          # Settings (pydantic-settings)
│   ├── security.py        # JWT, hashing, etc.
│   └── exceptions.py      # domain exceptions + handlers
├── api/
│   ├── deps.py            # shared dependencies (Depends)
│   └── v1/
│       ├── router.py      # aggregating router for the version
│       └── endpoints/
│           ├── users.py
│           └── orders.py
├── schemas/               # Pydantic models (DTOs): requests and responses
├── models/                # SQLAlchemy models
├── repositories/          # database access (queries only)
├── services/              # business logic
├── clients/               # clients for external services (HTTP, brokers)
└── db/
    ├── base.py
    └── session.py
tests/
├── conftest.py
├── api/
├── services/
└── repositories/
alembic/
pyproject.toml
```

### Layer rules

Dependencies flow strictly one way: **endpoint → service → repository → DB**.

| Layer | Responsibilities | Must NOT do |
|---|---|---|
| `endpoints` | parse the request, call a service, build the response | business logic, direct SQL queries |
| `services` | business logic, orchestration, transactions | know anything about HTTP (`Request`, `Response`, status codes) |
| `repositories` | database queries | business rules, `HTTPException` |
| `schemas` | validation and serialization | database access |
| `models` | table definitions | business logic |

- An endpoint **never** imports SQLAlchemy models directly to run queries.
- Services do not import anything from `fastapi`.
- Repositories do not call other repositories — that is the service's job.

---

## 4. Naming

| Entity | Style | Example |
|---|---|---|
| Modules, packages | `snake_case` | `user_service.py` |
| Functions, methods, variables | `snake_case` | `get_user_by_id` |
| Classes | `PascalCase` | `UserService` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_PAGE_SIZE` |
| Private members | `_` prefix | `_build_query` |
| Pydantic schemas | suffix by purpose | `UserCreate`, `UserUpdate`, `UserRead` |
| SQLAlchemy models | singular, no suffix | `User`, `Order` |
| Repositories / services | `<Entity>Repository` / `<Entity>Service` | `UserRepository` |
| Exceptions | `Error` suffix | `UserNotFoundError` |

- Names are in English, meaningful, and unabbreviated (`user`, not `usr`; `index`, not `idx`, except for conventional `i` and `id`).
- Boolean variables start with `is_`, `has_`, `can_`, `should_`.
- Async functions are named the same way as sync ones (no `async` prefix/suffix).
- Endpoints: plural nouns in URLs (`/users`, `/orders/{order_id}`); no verbs in paths — that is what HTTP methods are for.

---

## 5. Typing

- **All** functions and methods have annotations for arguments and return values.
- Use modern syntax: `list[int]`, `dict[str, Any]`, `str | None` (not `List`, `Dict`, `Optional`).
- Avoid `Any`. If it is unavoidable, leave a comment explaining why.
- For collection inputs use abstract types (`Sequence`, `Mapping`); for outputs use concrete ones (`list`, `dict`).
- In FastAPI dependencies, use `Annotated`.

```python
# ✅ Good
async def get_user(user_id: int, repo: UserRepository) -> User | None:
    return await repo.get_by_id(user_id)

# ❌ Bad
async def get_user(user_id, repo):
    return await repo.get_by_id(user_id)
```

---

## 6. Formatting and imports

- Maximum line length: **100**. Quotes: double.
- Import order: standard library → third-party → local, separated by blank lines.
- Absolute imports only, from the package root (`from app.services.user import UserService`).
- `from module import *` and circular imports are forbidden. For annotations that cause a cycle, use `TYPE_CHECKING`.
- Use f-strings; do not use `%` formatting or `.format()`.
- Use `pathlib.Path`, not `os.path`.
- Use `enum.StrEnum` / `enum.IntEnum` instead of "magic" strings and numbers.

---

## 7. Async

- Everything involving I/O (DB, HTTP, files, brokers) is **`async`**.
- **Never** call blocking code inside `async def`: `time.sleep`, `requests`, a synchronous DB driver, heavy computation. For CPU-bound or unavoidably blocking calls, use `asyncio.to_thread()` / `run_in_threadpool`.
- For HTTP use `httpx.AsyncClient` (one client per application, created in `lifespan`, not per request).
- Independent parallel operations: use `asyncio.gather` or `asyncio.TaskGroup`.
- Do not create "forgotten" tasks (`asyncio.create_task` without keeping a reference and handling errors).
- All external calls must have **timeouts**.
- If an endpoint does no I/O and never `await`s, it may be a plain `def` — FastAPI will run it in a threadpool. But by default this project uses `async def`.

---

## 8. FastAPI: endpoints

- Every endpoint must define: `response_model`, `status_code`, `summary`/docstring (they end up in OpenAPI), and `tags` (at the router level).
- Use correct status codes: `201` for creation, `204` for deletion without a body, `404` for not found, `409` for conflict, `422` for validation (automatic).
- All dependencies go through `Depends` and `Annotated`. Declare type aliases for frequently used dependencies.
- Validate request parameters with `Query`, `Path`, `Body` and constraints (`ge`, `le`, `max_length`).
- List endpoints **always** have pagination (`limit`/`offset` or cursor). No "return everything".
- Endpoints are thin: no more than ~10–15 lines.

```python
# api/deps.py
SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_user_service(session: SessionDep) -> UserService:
    return UserService(UserRepository(session))

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

```python
# api/v1/endpoints/users.py
router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: UserServiceDep) -> UserRead:
    return await service.create(payload)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: Annotated[int, Path(ge=1)], service: UserServiceDep) -> UserRead:
    return await service.get(user_id)
```

---

## 9. Pydantic schemas

- Pydantic v2: `model_validate`, `model_dump`, `field_validator`, `model_validator`, `ConfigDict`.
- Separate schemas for separate purposes: `XxxBase` → `XxxCreate` / `XxxUpdate` / `XxxRead`. Do not use one schema for both input and output.
- Schemas built from ORM objects use `model_config = ConfigDict(from_attributes=True)`.
- In `XxxUpdate` all fields are optional; apply them via `model_dump(exclude_unset=True)`.
- Describe constraints in `Field(...)` (`min_length`, `ge`, `pattern`, etc.), not manually in code.
- Secrets and sensitive fields (`password`, `token`) never appear in `Read` schemas or logs. Use `SecretStr` where appropriate.

```python
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)


class UserCreate(UserBase):
    password: SecretStr = Field(min_length=8)


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
```

---

## 10. Database

- SQLAlchemy 2.0, declarative style with `Mapped[...]` and `mapped_column(...)`.
- Queries use `select()`, `update()`, `delete()`; do not use the legacy `session.query()`.
- The session arrives via `Depends` and is **not created** manually inside services/repositories.
- Transactions are managed at the service level (or via a unit of work), not in repositories or endpoints.
- Avoid N+1: use `selectinload` / `joinedload` explicitly.
- Any schema change is made **only via an Alembic migration**. Migrations have a meaningful message and are reversible (`downgrade`).
- Never build SQL by string concatenation — parameterized queries only.
- Every table has a primary key, `created_at`, `updated_at` (where applicable), and indexes for real queries.
- Store time in UTC with `timezone=True`. Use `datetime.now(UTC)`, not `datetime.utcnow()`.

```python
class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
```

---

## 11. Error handling

- In `services` / `repositories`, raise **domain exceptions** (subclasses of `AppError`), not `HTTPException`.
- Converting domain exceptions into HTTP responses happens in **global exception handlers** (`app.add_exception_handler`).
- No bare `except:`, and avoid `except Exception:`. Catch specific exceptions.
- Do not swallow errors silently. Either handle them meaningfully, or log and re-raise.
- When re-raising, preserve the cause: `raise DomainError(...) from exc`.
- The error response format is uniform across the service:

```json
{ "error": { "code": "user_not_found", "message": "User with id=42 not found" } }
```

```python
# core/exceptions.py
class AppError(Exception):
    code: str = "app_error"
    status_code: int = 500

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    code = "not_found"
    status_code = 404
```

---

## 12. Configuration and secrets

- All configuration goes through `pydantic-settings` (`Settings`), read from environment variables / `.env`.
- The settings object is created once and provided via `@lru_cache` and `Depends`.
- **Never hardcode**: URLs, passwords, keys, tokens, hostnames.
- `.env` is not committed. The repository contains `.env.example` without real values.
- No access to `os.environ` outside `core/config.py`.

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "my-service"
    debug: bool = False
    database_url: PostgresDsn
    jwt_secret: SecretStr


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## 13. Security

- Validate **all** external input with Pydantic.
- Passwords are stored only as hashes (`argon2` / `bcrypt`), never in plain text.
- Authorization is checked through dependencies (`Depends`), not ad hoc inside business logic.
- Do not expose internal details in errors (stack traces, SQL, file paths).
- CORS: in production, only an explicit list of allowed origins.
- Do not use `eval`, `exec`, or `pickle` on untrusted data.
- Limit request body and uploaded file sizes.

---

## 14. Testing

- Every new feature and every fixed bug comes **with a test**.
- The test structure mirrors the structure of `app/`.
- Naming: `test_<what>_<condition>_<expected result>`, e.g. `test_create_user_with_duplicate_email_returns_409`.
- Follow the **Arrange–Act–Assert** pattern; one test verifies one behavior.
- API tests use `httpx.AsyncClient` with `ASGITransport`; dependencies are replaced via `app.dependency_overrides`.
- Service tests use mocked repositories; repository tests run against a test database.
- Tests are independent of each other and of execution order.
- External services are always mocked in tests.
- For repeated data setup, use fixtures and factories instead of copy-paste.

```python
@pytest.mark.asyncio
async def test_get_user_when_not_found_returns_404(client: AsyncClient) -> None:
    response = await client.get("/api/v1/users/999")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
```

---

## 15. Prohibited

- ❌ Business logic or SQL in endpoints.
- ❌ `HTTPException` in services and repositories.
- ❌ Blocking calls (`requests`, `time.sleep`) in `async` code.
- ❌ Pydantic v1 syntax, `session.query()`, `datetime.utcnow()`.
- ❌ Bare `except:` and silently swallowed exceptions.
- ❌ Mutable default arguments (`def f(x=[])`).
- ❌ Global mutable state and module-level singletons.
- ❌ Hardcoded secrets and configuration.
- ❌ Functions without type annotations.
- ❌ Made-up library APIs: if you are unsure about a signature, say so instead of guessing.
- ❌ Unnecessary dependencies and unrelated code rewritten "while you're at it".

---

## 16. How to respond to the user

- If the task is ambiguous or context is missing, ask one specific clarifying question instead of guessing.
- Before a large change, briefly outline the plan (which files you will touch and why).
- Show code as whole files or clearly delimited fragments with a path (`app/services/user.py`), not as scraps.
- If you notice a problem in existing code that is unrelated to the task, mention it but do not fix it unless asked.
