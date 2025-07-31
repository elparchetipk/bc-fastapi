# Ejercicios - Semana 11: Proyecto Final

⏰ **Tiempo disponible:** Según progreso individual  
🎯 **Dificultad:** Integrador  
📋 **Objetivo:** Refinar y personalizar el proyecto final

## 🎯 Propósito de los Ejercicios

Estos ejercicios están diseñados para que los estudiantes:

1. ✅ **Personalicen su proyecto** con características únicas
2. ✅ **Profundicen en aspectos específicos** según su interés
3. ✅ **Optimicen el rendimiento** de la aplicación
4. ✅ **Agreguen valor diferencial** a su portfolio
5. ✅ **Preparen variaciones** para demostrar versatilidad

## 📋 Ejercicios Propuestos

### **Ejercicio 1: Personalización Visual**

#### **Objetivo:** Hacer el proyecto único visualmente

**Tareas:**

1. **Cambiar el tema de colores** de la aplicación
2. **Agregar logo personalizado** y branding
3. **Customizar componentes** con estilos únicos
4. **Implementar modo oscuro/claro**

**Entregables:**

- Aplicación con identidad visual propia
- Documentación de decisiones de diseño

---

### **Ejercicio 2: Funcionalidades Adicionales**

#### **Objetivo:** Agregar características que demuestren creatividad técnica

**Opciones (elegir 1-2):**

#### **2A: Sistema de Comentarios**

```typescript
// Agregar comentarios a las tareas
interface TaskComment {
  id: number;
  task_id: number;
  user_id: number;
  content: string;
  created_at: string;
  user: User;
}
```

#### **2B: Filtros Avanzados**

```typescript
// Filtros por fecha, prioridad, usuario
interface TaskFilters {
  status?: TaskStatus[];
  priority?: TaskPriority[];
  assignee_id?: number;
  date_range?: {
    start: string;
    end: string;
  };
  search?: string;
}
```

#### **2C: Notificaciones Push**

```python
# Backend: Agregar notificaciones por email
from fastapi_mail import FastMail, MessageSchema

async def send_task_notification(user_email: str, task: Task):
    message = MessageSchema(
        subject="New Task Assigned",
        recipients=[user_email],
        body=f"You have been assigned to task: {task.title}"
    )
    await FastMail.send_message(message)
```

**Entregables:**

- Funcionalidad implementada y funcionando
- Tests para la nueva característica
- Documentación de la feature

---

### **Ejercicio 3: Optimización de Performance**

#### **Objetivo:** Demostrar conocimiento de optimización

**Tareas:**

1. **Implementar paginación** en el listado de tareas
2. **Agregar caching** con Redis para consultas frecuentes
3. **Optimizar queries** de base de datos
4. **Implementar lazy loading** en el frontend

#### **3A: Paginación Backend**

```python
# app/schemas/common.py
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    total_pages: int

# app/api/v1/tasks.py
@router.get("/", response_model=PaginatedResponse)
async def get_tasks(
    page: int = 1,
    per_page: int = 10,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.get_paginated_tasks(
        user_id=current_user.id,
        page=page,
        per_page=per_page
    )
```

#### **3B: Caching con Redis**

```python
# app/services/cache_service.py
import redis
import json
from typing import Optional

class CacheService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get_user_tasks_cache(self, user_id: int) -> Optional[List[dict]]:
        cached = self.redis.get(f"user_tasks:{user_id}")
        if cached:
            return json.loads(cached)
        return None

    async def set_user_tasks_cache(self, user_id: int, tasks: List[dict], ttl: int = 300):
        self.redis.setex(
            f"user_tasks:{user_id}",
            ttl,
            json.dumps(tasks, default=str)
        )
```

**Entregables:**

- Mediciones de performance antes/después
- Implementación de optimizaciones
- Documentación de mejoras

---

### **Ejercicio 4: Testing Avanzado**

#### **Objetivo:** Demostrar dominio de testing comprehensivo

**Tareas:**

1. **Alcanzar 100% de coverage** en módulos críticos
2. **Implementar integration tests** end-to-end
3. **Agregar performance tests**
4. **Configurar testing automatizado** con GitHub Actions

#### **4A: Integration Tests**

```python
# tests/test_integration.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_complete_task_workflow():
    """Test completo: registro -> login -> crear tarea -> actualizar -> eliminar"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Registro
        register_response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "testpass123"
        })
        assert register_response.status_code == 201

        # Login
        login_response = await client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "testpass123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Crear tarea
        task_response = await client.post("/api/v1/tasks/",
            json={"title": "Test Task", "priority": "medium"},
            headers=headers
        )
        assert task_response.status_code == 201
        task_id = task_response.json()["id"]

        # Actualizar estado
        update_response = await client.put(f"/api/v1/tasks/{task_id}/status",
            json={"status": "completed"},
            headers=headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "completed"
```

#### **4B: GitHub Actions CI/CD**

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest-cov

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app tests/ --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
```

**Entregables:**

- Tests con 100% coverage en módulos críticos
- CI/CD pipeline funcionando
- Reports de testing automatizados

---

### **Ejercicio 5: Deployment Avanzado**

#### **Objetivo:** Preparar para deployment real en producción

**Tareas:**

1. **Configurar deployment** en un cloud provider
2. **Implementar HTTPS** con certificados SSL
3. **Configurar monitoreo** básico
4. **Optimizar Docker images** para producción

#### **5A: Deployment en la Nube**

**Opciones (elegir una):**

- **Heroku**: Para deployment simple
- **DigitalOcean**: Para control de infraestructura
- **AWS/Railway**: Para experiencia enterprise

#### **5B: Docker Optimizado**

```dockerfile
# Frontend Dockerfile optimizado
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

# Optimizaciones de seguridad
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Entregables:**

- Aplicación desplegada y accesible públicamente
- URL de producción funcionando
- Documentación de deployment

---

### **Ejercicio 6: Personalización de Portfolio**

#### **Objetivo:** Crear variaciones para diferentes tipos de roles

**Tareas:**

1. **Adaptar el proyecto** para diferentes audiencias
2. **Crear versiones especializadas** del README
3. **Preparar demos específicos** por área de interés

#### **6A: Versión Backend-Focused**

```markdown
# TaskFlow API - Backend Engineering Portfolio

## 🎯 Backend Architecture Excellence

This project showcases advanced backend engineering skills:

### API Design & Performance

- **Sub-200ms response times** with optimized database queries
- **RESTful architecture** following OpenAPI specifications
- **Async/await patterns** for concurrent request handling
- **Database indexing strategy** for scalable performance

### Advanced Features Implemented

- **JWT Authentication** with refresh token rotation
- **WebSocket real-time** communication with connection pooling
- **Background task processing** with Celery integration
- **Caching strategy** with Redis for high-traffic scenarios
```

#### **6B: Versión Full-Stack**

```markdown
# TaskFlow - Full-Stack Development Portfolio

## 🚀 End-to-End Application Development

Demonstrates complete software development lifecycle:

### Technical Stack Mastery

- **Backend**: FastAPI + PostgreSQL + Redis
- **Frontend**: React + TypeScript + Tailwind CSS
- **DevOps**: Docker + CI/CD + Cloud Deployment
- **Testing**: 95% coverage with integration tests
```

**Entregables:**

- Múltiples versiones del portfolio
- READMEs especializados por audiencia
- Demos adaptados a diferentes roles

---

## 🎯 Guía de Selección de Ejercicios

### **Para estudiantes enfocados en Backend:**

- Ejercicio 2C (Notificaciones)
- Ejercicio 3 (Performance)
- Ejercicio 4 (Testing Avanzado)

### **Para estudiantes enfocados en Frontend:**

- Ejercicio 1 (Personalización Visual)
- Ejercicio 2A o 2B (Features UI)
- Ejercicio 6 (Portfolio)

### **Para estudiantes enfocados en DevOps:**

- Ejercicio 3 (Performance)
- Ejercicio 4B (CI/CD)
- Ejercicio 5 (Deployment)

### **Para maximizar empleabilidad:**

- Ejercicio 1 + 2A + 6 (Portfolio diferenciado)

## 📚 Recursos de Apoyo

### **Herramientas de Optimización**

- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Performance auditing
- [Pytest-benchmark](https://pytest-benchmark.readthedocs.io/) - Performance testing
- [Redis Insights](https://redislabs.com/redis-enterprise/redis-insight/) - Cache monitoring

### **Deployment Platforms**

- [Heroku](https://heroku.com) - Simple deployment
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform/) - Managed containers
- [Railway](https://railway.app) - Modern deployment platform

### **Monitoring y Analytics**

- [Sentry](https://sentry.io) - Error tracking
- [DataDog](https://www.datadoghq.com) - Application monitoring
- [Google Analytics](https://analytics.google.com) - User analytics

---

## 🎯 Criterios de Evaluación

### **Calidad Técnica (40%)**

- Implementación correcta y funcional
- Código limpio y bien estructurado
- Manejo apropiado de errores
- Performance optimizado

### **Creatividad e Innovación (30%)**

- Características únicas implementadas
- Soluciones creativas a problemas
- Valor agregado al proyecto base
- Diferenciación competitiva

### **Documentación (20%)**

- Explicación clara de las mejoras
- Instrucciones de uso actualizadas
- Justificación de decisiones técnicas
- Portfolio bien presentado

### **Impacto en Portfolio (10%)**

- Mejora la empleabilidad
- Demuestra skills específicos
- Adaptado a objetivos profesionales
- Narrativa coherente del proyecto

---

## 💡 Consejos para el Éxito

### **Enfoque en Calidad sobre Cantidad**

- Es mejor implementar 1-2 ejercicios muy bien que muchos mediocres
- Documenta cada decisión técnica
- Prueba exhaustivamente cada nueva feature

### **Piensa en el Mercado Laboral**

- ¿Qué tipo de rol quieres conseguir?
- ¿Qué skills son más demandados en tu área?
- ¿Cómo puedes diferenciarte de otros candidatos?

### **Prepara Múltiples Narrativas**

- Ten versiones del proyecto para diferentes audiencias
- Prepara explicaciones técnicas de diferentes profundidades
- Documenta el proceso de desarrollo y decisiones

---

**🎯 Estos ejercicios transformarán tu proyecto base en un portfolio diferenciado que destaque en el mercado laboral.**
