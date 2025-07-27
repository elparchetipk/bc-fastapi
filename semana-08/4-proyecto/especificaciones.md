# Especificaciones del Proyecto Semana 8

## 🎯 Objetivo del Proyecto

Implementar una **suite completa de testing y calidad** para la API FastAPI desarrollada en las semanas anteriores, demostrando las mejores prácticas de testing en producción.

## ⏱️ Tiempo Total: 6 horas distribuidas en 4 sesiones

---

## 📋 Especificaciones Técnicas

### Requisitos Base

- ✅ **API FastAPI** funcionando (Semanas 1-7)
- ✅ **Base de datos** configurada (SQLite/PostgreSQL)
- ✅ **Autenticación JWT** implementada
- ✅ **Endpoints CRUD** completos

### Entregables del Proyecto

#### 1. Suite de Tests Automatizados (Práctica 27)

- **pytest configurado** con fixtures básicas
- **Tests para endpoints** GET, POST, PUT, DELETE
- **Tests de validación** de datos con Pydantic
- **Mínimo 10 tests** funcionando correctamente

#### 2. Tests Avanzados con Mocking (Práctica 28)

- **Fixtures avanzadas** para base de datos de prueba
- **Mocking de servicios externos** (email, APIs)
- **Tests de autenticación** JWT completos
- **Tests de integración** del flujo completo

#### 3. Análisis de Cobertura y Calidad (Práctica 29)

- **Cobertura de código ≥ 80%** medida con pytest-cov
- **Herramientas de calidad** configuradas (black, flake8, mypy)
- **Scripts de automatización** para verificaciones
- **Reporte HTML** de cobertura generado

#### 4. Documentación y CI/CD (Práctica 30)

- **Documentación OpenAPI** avanzada con ejemplos
- **GitHub Actions** para CI/CD básico
- **Makefile** con comandos de automatización
- **Health checks** y métricas básicas

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Archivos Esperada

```
mi-api-fastapi/
├── app/
│   ├── main.py              # Aplicación principal
│   ├── auth.py              # Autenticación JWT
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Modelos Pydantic
│   ├── database.py          # Configuración BD
│   └── middleware.py        # Middleware personalizado
├── tests/
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_main.py         # Tests básicos
│   ├── test_auth.py         # Tests autenticación
│   ├── test_users.py        # Tests CRUD usuarios
│   ├── test_integration.py  # Tests integración
│   └── test_performance.py  # Tests performance (bonus)
├── scripts/
│   └── quality_check.sh     # Script automatización
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions
├── docs/
│   └── api-docs.html        # Documentación estática
├── requirements.txt         # Dependencias producción
├── requirements-dev.txt     # Dependencias desarrollo
├── Makefile                 # Comandos automatización
├── pyproject.toml          # Configuración herramientas
└── README.md               # Documentación proyecto
```

---

## 🎯 Casos de Uso a Testear

### Flujo Principal: Gestión de Usuarios

1. **Registro** de nuevo usuario
2. **Login** y obtención de token JWT
3. **Consulta** de perfil propio
4. **Actualización** de datos del usuario
5. **Listado** de usuarios (admin)
6. **Eliminación** de usuario

### Casos de Error a Testear

1. **Registro** con email duplicado
2. **Login** con credenciales incorrectas
3. **Acceso** sin token de autenticación
4. **Token** expirado o inválido
5. **Validación** de datos incorrectos
6. **Operaciones** sin permisos

### Tests de Performance

1. **Tiempo de respuesta** de endpoints
2. **Carga** de múltiples requests
3. **Memory usage** durante operaciones

---

## 📊 Métricas de Calidad Objetivo

| Métrica                 | Objetivo       | Herramienta      |
| ----------------------- | -------------- | ---------------- |
| **Cobertura de Código** | ≥ 80%          | pytest-cov       |
| **Tests Unitarios**     | ≥ 15 tests     | pytest           |
| **Tests Integración**   | ≥ 5 tests      | pytest           |
| **Tiempo Respuesta**    | < 200ms        | pytest-benchmark |
| **Calidad Código**      | Sin errores    | flake8, mypy     |
| **Documentación**       | 100% endpoints | OpenAPI          |

---

## 🚀 Proceso de Desarrollo

### Fase 1: Tests Básicos (Semana 8.1)

- Configurar pytest y TestClient
- Implementar tests para endpoints principales
- Validar funcionamiento básico

### Fase 2: Tests Avanzados (Semana 8.2)

- Agregar mocking y fixtures avanzadas
- Tests de autenticación completos
- Tests de base de datos

### Fase 3: Calidad y Cobertura (Semana 8.3)

- Medir y mejorar cobertura
- Configurar herramientas de calidad
- Automatizar verificaciones

### Fase 4: Documentación y CI/CD (Semana 8.4)

- Documentación OpenAPI avanzada
- Pipeline de CI/CD con GitHub Actions
- Scripts de automatización

---

## 📝 Criterios de Evaluación

### Funcionalidad (40%)

- [ ] Suite de tests ejecutándose sin errores
- [ ] Cobertura de código ≥ 80%
- [ ] Tests para casos principales y de error
- [ ] Mocking implementado correctamente

### Calidad de Código (30%)

- [ ] Código formateado con black
- [ ] Sin errores de linting (flake8)
- [ ] Type hints verificados (mypy)
- [ ] Estructura organizada y legible

### Documentación (20%)

- [ ] README completo con instrucciones
- [ ] Documentación OpenAPI detallada
- [ ] Comments y docstrings en tests
- [ ] Scripts documentados

### Automatización (10%)

- [ ] GitHub Actions funcionando
- [ ] Makefile con comandos útiles
- [ ] Scripts de verificación
- [ ] Pre-commit hooks (bonus)

---

## 🛠️ Herramientas Requeridas

### Testing

- **pytest**: Framework principal de testing
- **httpx**: Cliente HTTP para TestClient
- **pytest-asyncio**: Soporte para código asíncrono
- **pytest-cov**: Medición de cobertura
- **pytest-mock**: Mocking avanzado

### Calidad

- **black**: Formateador de código
- **flake8**: Linting
- **mypy**: Type checking
- **isort**: Ordenamiento de imports

### Documentación

- **redoc-cli**: Documentación estática
- **mkdocs**: Documentación adicional (opcional)

### CI/CD

- **GitHub Actions**: Pipeline automatizado
- **pre-commit**: Hooks de git

---

## 🎉 Entrega Final

### Formato de Entrega

1. **Repositorio Git** con todo el código
2. **README.md** con instrucciones completas
3. **Reporte de cobertura** (HTML)
4. **Documentación OpenAPI** generada
5. **Video demo** de 5 minutos (opcional)

### Comandos de Verificación

```bash
# Instalar dependencias
make install

# Ejecutar todos los tests
make test

# Verificar calidad
make lint

# Generar reporte de cobertura
make test-cov

# Ejecutar pipeline completo
make ci
```

---

## 📚 Recursos de Apoyo

- [FastAPI Testing Tutorial](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Guide](https://coverage.readthedocs.io/)
- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

---

💡 **Nota**: Este proyecto integra todos los conocimientos de las 8 semanas, siendo el testing la culminación que asegura la calidad de todo lo desarrollado.
