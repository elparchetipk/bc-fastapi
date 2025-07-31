# Ejercicios Semana 8: Testing y Calidad

## 🎯 Objetivo General

Reforzar los conceptos de testing y calidad mediante ejercicios prácticos que complementan las 4 prácticas de la semana.

## ⏱️ Tiempo Estimado Total: 2-3 horas adicionales (opcional)

---

## 📋 Ejercicio 1: Completar Suite de Tests Básicos

**Tiempo:** 30-45 minutos  
**Prerequisito:** Práctica 27 completada

### Descripción

Expandir la suite de tests básicos creada en la Práctica 27 con casos adicionales.

### Tareas

1. **Agregar 3 tests más** para validación de datos
2. **Implementar tests** para códigos de error específicos (400, 404, 422)
3. **Crear tests** para endpoints GET con parámetros de consulta
4. **Verificar** que todos los tests pasen con `pytest -v`

### Entregables

- [ ] Mínimo 8 tests funcionando
- [ ] Cobertura básica de endpoints principales
- [ ] Documentación de cada test con docstrings

---

## 📋 Ejercicio 2: Mocking de Servicios Externos

**Tiempo:** 45-60 minutos  
**Prerequisito:** Práctica 28 completada

### Descripción

Practicar el uso de mocks para servicios externos como email, APIs REST, etc.

### Tareas

1. **Crear mock** para servicio de email (simulado)
2. **Implementar mock** para API externa de validación
3. **Escribir tests** que usen estos mocks
4. **Verificar** que los mocks se llamen correctamente

### Código Base Sugerido

```python
# services/email_service.py (crear)
def send_welcome_email(email: str) -> bool:
    """Servicio de email a mockear"""
    # Simular llamada externa
    return True

# services/external_api.py (crear)
import requests

def validate_user_data(data: dict) -> bool:
    """API externa a mockear"""
    response = requests.post("https://api.example.com/validate", json=data)
    return response.status_code == 200
```

### Entregables

- [ ] 2 servicios externos mockeados
- [ ] 4 tests usando mocks
- [ ] Verificación de llamadas a mocks

---

## 📋 Ejercicio 3: Mejora de Cobertura de Código

**Tiempo:** 30-45 minutos  
**Prerequisito:** Práctica 29 completada

### Descripción

Alcanzar y mantener una cobertura de código del 85%+ mediante tests adicionales.

### Tareas

1. **Ejecutar** `pytest --cov --cov-report=html`
2. **Identificar** líneas sin cobertura en el reporte HTML
3. **Escribir tests** para las líneas no cubiertas
4. **Alcanzar** mínimo 85% de cobertura

### Áreas Comunes Sin Cobertura

- Manejo de excepciones
- Validaciones de edge cases
- Funciones de utilidad
- Middlewares personalizados

### Entregables

- [ ] Cobertura ≥ 85%
- [ ] Tests para manejo de errores
- [ ] Tests para casos límite

---

## 📋 Ejercicio 4: Documentación y Scripts

**Tiempo:** 30-45 minutos  
**Prerequisito:** Práctica 30 completada

### Descripción

Mejorar la documentación del proyecto y crear scripts de automatización personalizados.

### Tareas

1. **Crear** script personalizado de testing
2. **Mejorar** documentación OpenAPI con más ejemplos
3. **Implementar** comando Make personalizado
4. **Documentar** proceso de testing en README

### Script Sugerido

```bash
#!/bin/bash
# scripts/run_quality_checks.sh

echo "🧪 Ejecutando verificaciones de calidad..."

# Linting
flake8 . || exit 1

# Formateo
black --check . || exit 1

# Tests con cobertura
pytest --cov --cov-fail-under=85 || exit 1

echo "✅ Todas las verificaciones pasaron!"
```

### Entregables

- [ ] Script de calidad personalizado
- [ ] Documentación OpenAPI mejorada
- [ ] README actualizado con proceso de testing
- [ ] Comando Make personalizado

---

## 🏆 Ejercicio Bonus: Test de Performance Básico

**Tiempo:** 45-60 minutos  
**Nivel:** Intermedio

### Descripción

Implementar tests básicos de performance para verificar tiempos de respuesta.

### Herramientas

```bash
pip install pytest-benchmark
```

### Ejemplo de Test

```python
def test_user_creation_performance(client, benchmark):
    """Test de performance para creación de usuarios"""
    user_data = {
        "name": "Performance Test",
        "email": "perf@example.com",
        "age": 25
    }

    result = benchmark(client.post, "/users", json=user_data)
    assert result.status_code == 201
```

### Entregables

- [ ] 3 tests de performance implementados
- [ ] Benchmarks de endpoints principales
- [ ] Documentación de resultados

---

## 📝 Instrucciones de Entrega

### Estructura Esperada

```
tu-proyecto/
├── tests/
│   ├── test_main.py           # Tests básicos
│   ├── test_mocking.py        # Tests con mocks
│   ├── test_coverage.py       # Tests adicionales
│   └── test_performance.py    # Tests de performance (bonus)
├── scripts/
│   └── run_quality_checks.sh  # Script personalizado
└── README.md                  # Documentación actualizada
```

### Verificación Final

```bash
# Ejecutar todos los tests
pytest -v

# Verificar cobertura
pytest --cov --cov-report=term-missing

# Ejecutar script de calidad
./scripts/run_quality_checks.sh
```

---

## 🎯 Criterios de Evaluación

| Aspecto               | Puntos | Descripción                          |
| --------------------- | ------ | ------------------------------------ |
| **Tests Básicos**     | 25%    | Ejercicio 1 completado correctamente |
| **Mocking**           | 25%    | Ejercicio 2 con mocks funcionando    |
| **Cobertura**         | 25%    | Ejercicio 3 con ≥85% cobertura       |
| **Documentación**     | 25%    | Ejercicio 4 con docs y scripts       |
| **Bonus Performance** | +10%   | Tests de performance implementados   |

---

## 📚 Recursos de Apoyo

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-mock Examples](https://pytest-mock.readthedocs.io/en/latest/usage.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)

---

💡 **Consejo**: Estos ejercicios son opcionales pero altamente recomendados para dominar testing en FastAPI.
