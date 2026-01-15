# API чатов и сообщений

## 4 конечных точек
- POST /chats/ — создать чат
- POST /chats/{id}/messages/ — отправить сообщение в чат
- GET /chats/{id} — получить чат и последние N сообщений
- DELETE /chats/{id} — удалить чат вместе со всеми сообщениями

## Разработка

```bash
uv pip install .[dev]
ruff check
ruff format --check
docker compose up db -d
python -m scripts.init_db
python -m scripts.init_random_data
python -m unittest
```
## Примените миграцию

```bash
alembic revision --autogenerate -m "make changes"
alembic upgrade head
```

## Запустить приложение в докере

- Измените переменную DB_URL
- Запустите приложение

```bash 
docker compose up
```
