# Referencias y Recursos - Semana 8

## 📚 Documentación Oficial

### FastAPI Testing

- [FastAPI Testing Tutorial](https://fastapi.tiangolo.com/tutorial/testing/) - Tutorial oficial de testing
- [Advanced Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/) - Testing avanzado con dependencias
- [Testing WebSockets](https://fastapi.tiangolo.com/advanced/websockets/#testing-websockets) - Testing de WebSockets

### pytest

- [pytest Documentation](https://docs.pytest.org/) - Documentación completa
- [pytest Fixtures](https://docs.pytest.org/en/latest/how.html#fixtures) - Guía de fixtures
- [pytest Parametrize](https://docs.pytest.org/en/latest/parametrize.html) - Tests parametrizados
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - Testing asíncrono

### Cobertura de Código

- [Coverage.py](https://coverage.readthedocs.io/) - Documentación de coverage
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Plugin pytest para coverage
- [Codecov](https://about.codecov.io/blog/python-code-coverage-using-github-actions-and-codecov/) - Integración con CI/CD

---

## 🛠️ Herramientas y Librerías

### Testing Framework

- **pytest** - Framework principal de testing para Python
- **httpx** - Cliente HTTP moderno para APIs
- **pytest-asyncio** - Soporte para testing de código asíncrono
- **pytest-mock** - Wrapper para unittest.mock
- **faker** - Generación de datos falsos para tests

### Calidad de Código

- **black** - Formateador automático de código Python
- **flake8** - Linter para verificar estilo PEP 8
- **mypy** - Type checker estático
- **isort** - Ordenamiento automático de imports
- **pre-commit** - Hooks de Git para calidad

### Mocking y Testing

- **pytest-mock** - Mocking avanzado
- **responses** - Mock para requests HTTP
- **freezegun** - Mock para fechas y tiempo
- **pytest-benchmark** - Performance testing

---

## 📖 Artículos y Tutoriales

### Testing Best Practices

- [Python Testing Best Practices](https://realpython.com/python-testing/) - Real Python
- [FastAPI Testing Guide](https://testdriven.io/blog/fastapi-crud/) - Test-Driven Development
- [API Testing with Python](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/) - Arrange-Act-Assert Pattern

### Mocking y Fixtures

- [Python Mocking Tutorial](https://realpython.com/python-mock-library/) - unittest.mock
- [pytest Fixtures Guide](https://realpython.com/pytest-python-testing/#fixtures) - Fixtures avanzadas
- [Database Testing](https://testdriven.io/blog/testing-databases-with-pytest/) - Testing con bases de datos

### CI/CD y Automatización

- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python) - CI/CD oficial
- [Python CI/CD Best Practices](https://sourcery.ai/blog/python-best-practices/) - Mejores prácticas
- [Docker for Testing](https://testdriven.io/blog/dockerizing-fastapi-with-postgres-uvicorn-and-traefik/) - Containers en testing

---

## 🎥 Videos y Cursos

### YouTube Tutorials

- [FastAPI Testing Tutorial](https://www.youtube.com/results?search_query=fastapi+testing+tutorial) - Tutoriales en video
- [pytest Complete Guide](https://www.youtube.com/results?search_query=pytest+python+testing) - Guías completas de pytest
- [Python Testing Strategies](https://www.youtube.com/results?search_query=python+testing+strategies) - Estrategias de testing

### Cursos Online

- [Test-Driven Development with Python](https://www.obeythetestinggoat.com/) - TDD completo
- [Python Testing 101](https://realpython.com/courses/python-testing-101/) - Real Python Course
- [FastAPI Course](https://www.udemy.com/topic/fastapi/) - Cursos completos de FastAPI

---

## 🔧 Configuraciones y Templates

### pytest.ini Example

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --strict-config
    --verbose
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
```

### GitHub Actions Template

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Test with pytest
        run: pytest
```

### Makefile Template

```makefile
.PHONY: test test-cov lint format install clean

test:
	pytest -v

test-cov:
	pytest --cov --cov-report=html

lint:
	flake8 . && mypy . && black --check . && isort --check-only .

format:
	black . && isort .

install:
	pip install -r requirements-dev.txt

clean:
	find . -type d -name __pycache__ -delete
	rm -rf htmlcov/ .pytest_cache/ .coverage
```

---

## 📊 Benchmarks y Métricas

### Performance Targets

- **Response Time**: < 200ms para endpoints simples
- **Throughput**: > 100 requests/second
- **Memory Usage**: < 100MB para aplicación básica
- **Test Coverage**: > 80% líneas de código

### Testing Metrics

- **Test Execution Time**: < 30 segundos para suite completa
- **Test Reliability**: 99%+ success rate
- **Coverage**: 80%+ líneas cubiertas
- **Test Maintainability**: Tests simples y legibles

---

## 🚨 Troubleshooting Común

### Problemas Frecuentes

#### 1. Tests Lentos

```python
# Problema: Base de datos real en tests
# Solución: Base de datos en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
```

#### 2. Import Errors

```python
# Problema: Imports relativos
# Solución: Configurar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

#### 3. Async Tests

```python
# Problema: Tests async no funcionan
# Solución: Usar pytest-asyncio
@pytest.mark.asyncio
async def test_async_endpoint():
    pass
```

#### 4. Mock no Funciona

```python
# Problema: Mock no se aplica
# Solución: Verificar ruta del import
mocker.patch('app.main.external_service')  # Correcto
mocker.patch('external_service')  # Incorrecto
```

### Comandos de Debug

```bash
# Ejecutar tests con output detallado
pytest -v -s

# Ejecutar test específico
pytest tests/test_main.py::test_specific -v

# Debug con pdb
pytest --pdb

# Mostrar cobertura línea por línea
pytest --cov --cov-report=term-missing
```

---

## 🎯 Checklist de Calidad

### Pre-commit Checklist

- [ ] Tests pasan localmente
- [ ] Cobertura > 80%
- [ ] Sin errores de linting
- [ ] Código formateado
- [ ] Imports ordenados
- [ ] Type hints agregados
- [ ] Documentación actualizada

### Code Review Checklist

- [ ] Tests comprensibles
- [ ] Casos edge cubiertos
- [ ] Mocks usados apropiadamente
- [ ] Fixtures bien organizadas
- [ ] Assertions específicas
- [ ] Cleanup adecuado
- [ ] Performance aceptable

---

## 🤝 Comunidad y Soporte

### Foros y Discusiones

- [FastAPI Discussions](https://github.com/tiangolo/fastapi/discussions) - Foro oficial
- [pytest Discussions](https://github.com/pytest-dev/pytest/discussions) - Preguntas pytest
- [Stack Overflow](https://stackoverflow.com/questions/tagged/fastapi+testing) - Q&A
- [Reddit r/FastAPI](https://www.reddit.com/r/FastAPI/) - Comunidad Reddit

### Discord y Chat

- [FastAPI Discord](https://discord.gg/VQjSZaeJmf) - Chat en tiempo real
- [Python Discord](https://discord.gg/python) - Comunidad Python general

---

## 📅 Roadmap de Aprendizaje

### Nivel Básico (Semana 8)

1. ✅ Configurar pytest
2. ✅ Tests básicos de endpoints
3. ✅ Fixtures simples
4. ✅ Cobertura básica

### Nivel Intermedio (Post-Bootcamp)

1. 🔄 Tests de performance
2. 🔄 Mocking avanzado
3. 🔄 Tests de integración
4. 🔄 Continuous testing

### Nivel Avanzado (Futuro)

1. 🚀 Property-based testing
2. 🚀 Mutation testing
3. 🚀 Load testing
4. 🚀 Contract testing

---

💡 **Tip**: Mantén esta referencia como bookmark para consulta rápida durante el desarrollo.
