# How to Run

Execute in development environment:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Some useful links:

- [Interactive API docs: Swagger UI](http://localhost:8000/docs)
- [Alternative API docs: Redoc](http://localhost:8000/redoc)
- [OpenAPI spec](http://localhost:8000/openapi.json)