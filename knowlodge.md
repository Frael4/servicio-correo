## Pytest

Manera correcta de ejecutar un test en archivos con rutas largas

```python -m pytest tests\test_connection_db.py```

Ejecutar un test con Logs de información, Ex:

```pytest --log-cli-level=INFO tests\test_connection_db.py```

Ejecutar unico test de un archivo test, Ex:

```pytest --log-cli-level=INFO tests\test_connection_db.py::test_existed_connections```