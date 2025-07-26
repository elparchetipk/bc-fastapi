# Ejercicios Prácticos - Semana 1

## 🎯 Objetivos

Aplicar todos los conceptos aprendidos en la Semana 1 mediante ejercicios prácticos progresivos.

## 📋 Requisitos Previos

- Haber completado todos los tutoriales de práctica (01-04)
- Entorno de desarrollo configurado
- FastAPI y dependencias instaladas

## 🏋️ Ejercicios

### Ejercicio 1: API de Biblioteca (Básico)

**Objetivo**: Crear una API para gestionar una biblioteca de libros.

**Requerimientos**:

- Modelo `Book` con: id, title, author, isbn, year, available
- Endpoints CRUD completos
- Validación de datos con Pydantic
- Documentación automática

**Estructura esperada**:

```
ejercicios/
├── ejercicio_01/
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
```

**Criterios de evaluación**:

- ✅ Modelo Pydantic bien definido
- ✅ Endpoints funcionando correctamente
- ✅ Validación de datos
- ✅ Manejo de errores HTTP
- ✅ Documentación clara

### Ejercicio 2: API de Tareas con Filtros (Intermedio)

**Objetivo**: Sistema de gestión de tareas con filtros avanzados.

**Requerimientos**:

- Modelo `Task` con: id, title, description, priority, status, due_date, tags
- Endpoints con filtros por: prioridad, estado, fecha, tags
- Paginación
- Búsqueda por texto
- Ordenamiento múltiple

**Funcionalidades adicionales**:

- Estadísticas de tareas
- Bulk operations (crear/actualizar múltiples)
- Validaciones personalizadas

### Ejercicio 3: API de E-commerce (Avanzado)

**Objetivo**: API completa de e-commerce con múltiples entidades relacionadas.

**Requerimientos**:

- Modelos: `User`, `Product`, `Category`, `Order`, `OrderItem`
- Relaciones entre entidades
- Sistema de autenticación básico
- Carrito de compras
- Gestión de inventario

**Funcionalidades avanzadas**:

- Cálculo de precios y descuentos
- Validaciones de negocio complejas
- Endpoints de reportes
- Middleware personalizado

## 📝 Instrucciones de Entrega

1. **Crear branch específico**:

```bash
git checkout -b semana-01-ejercicios
```

2. **Estructura de entrega**:

```
semana-01/
├── ejercicios/
│   ├── ejercicio_01_biblioteca/
│   ├── ejercicio_02_tareas/
│   └── ejercicio_03_ecommerce/
```

3. **Cada ejercicio debe incluir**:

- Código fuente completo
- README.md con instrucciones
- requirements.txt
- Ejemplos de uso (curl o requests)
- Tests básicos (opcional pero recomendado)

4. **Commit y push**:

```bash
git add .
git commit -m "feat: ejercicios semana 1 - APIs con FastAPI"
git push origin semana-01-ejercicios
```

5. **Pull Request**:

- Título: "Entrega Semana 1: Ejercicios FastAPI Básico"
- Descripción detallada de lo implementado
- Screenshots de documentación
- Mencionar cualquier desafío encontrado

## 🔍 Criterios de Evaluación

### Código (40%)

- Estructura del proyecto
- Calidad del código
- Uso correcto de FastAPI
- Modelos Pydantic bien definidos

### Funcionalidad (30%)

- Endpoints funcionando
- Validaciones implementadas
- Manejo de errores
- Casos edge cubiertos

### Documentación (20%)

- README claro
- Documentación automática
- Ejemplos de uso
- Comentarios en código

### Mejores Prácticas (10%)

- Nombres descriptivos
- Separación de responsabilidades
- Principios SOLID básicos
- Git workflow apropiado

## 🎁 Bonus Points

- **Tests automatizados** (+10 puntos)
- **Docker setup** (+5 puntos)
- **Middleware personalizado** (+5 puntos)
- **Logging configurado** (+5 puntos)
- **Variables de entorno** (+5 puntos)
- **CI/CD básico** (+10 puntos)

## 📚 Recursos de Apoyo

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [HTTP Status Codes](https://httpstatuses.com/)
- Tutoriales completados en práctica/

## ⏰ Plazos

- **Fecha límite**: Viernes de la Semana 1, 23:59
- **Revisión por pares**: Lunes de la Semana 2
- **Feedback del instructor**: Miércoles de la Semana 2

## 🤝 Ayuda y Soporte

- **Canal Discord**: #semana-01-ayuda
- **Office Hours**: Martes y Jueves 19:00-20:00
- **FAQ**: Revisar issues del repositorio

¡Éxito en tus ejercicios! 💪🚀
