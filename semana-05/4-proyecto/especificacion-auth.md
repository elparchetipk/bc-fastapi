# 🏪 Proyecto: E-commerce con Autenticación Completa

## 📝 Información General

**Duración:** 4-6 horas de desarrollo + tiempo adicional para pulir  
**Tipo:** Proyecto integrador individual  
**Entrega:** Vía GitHub con CI/CD funcional  
**Peso:** 15% de la calificación total del bootcamp

---

## 🎯 Objetivo

Desarrollar un **sistema de e-commerce básico** que integre todos los conceptos de autenticación y autorización aprendidos en la semana, incluyendo JWT, roles, protección de endpoints y buenas prácticas de seguridad.

---

## 🏗️ Arquitectura del Proyecto

### **Estructura de Directorios**

```
proyecto-ecommerce-auth/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app principal
│   ├── config.py              # Configuración y settings
│   ├── database.py            # Conexión a base de datos
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # Modelo User
│   │   ├── product.py        # Modelo Product
│   │   ├── order.py          # Modelo Order
│   │   └── audit.py          # Modelo AuditLog
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py           # Pydantic schemas User
│   │   ├── product.py        # Pydantic schemas Product
│   │   ├── order.py          # Pydantic schemas Order
│   │   └── auth.py           # Pydantic schemas Auth
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Lógica de autenticación
│   │   ├── user_service.py   # Lógica de usuarios
│   │   ├── product_service.py # Lógica de productos
│   │   └── order_service.py  # Lógica de órdenes
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # Endpoints de auth
│   │   ├── users.py          # Endpoints de usuarios
│   │   ├── products.py       # Endpoints de productos
│   │   └── orders.py         # Endpoints de órdenes
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py # Middleware de auth
│   │   └── rate_limit.py     # Rate limiting
│   └── utils/
│       ├── __init__.py
│       ├── security.py       # Utilidades de seguridad
│       ├── dependencies.py   # Dependency injection
│       └── permissions.py    # Sistema de permisos
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Configuración pytest
│   ├── test_auth.py          # Tests de autenticación
│   ├── test_users.py         # Tests de usuarios
│   ├── test_products.py      # Tests de productos
│   └── test_orders.py        # Tests de órdenes
├── requirements.txt          # Dependencias
├── .env.example             # Variables de entorno ejemplo
├── .gitignore               # Git ignore
├── README.md                # Documentación
├── docker-compose.yml       # Docker para desarrollo
└── pytest.ini              # Configuración pytest
```

---

## 👥 Roles y Permisos del Sistema

### **Roles Definidos**

| Role         | Descripción        | Permisos                                                |
| ------------ | ------------------ | ------------------------------------------------------- |
| **customer** | Cliente regular    | Ver productos, crear órdenes propias, ver perfil propio |
| **employee** | Empleado de tienda | Todo lo de customer + gestionar inventario              |
| **manager**  | Gerente de tienda  | Todo lo de employee + gestionar empleados               |
| **admin**    | Administrador      | Acceso completo al sistema                              |

### **Matriz de Permisos por Endpoint**

| Endpoint                | customer     | employee     | manager        | admin |
| ----------------------- | ------------ | ------------ | -------------- | ----- |
| `GET /products`         | ✅           | ✅           | ✅             | ✅    |
| `POST /products`        | ❌           | ✅           | ✅             | ✅    |
| `PUT /products/{id}`    | ❌           | ✅           | ✅             | ✅    |
| `DELETE /products/{id}` | ❌           | ❌           | ✅             | ✅    |
| `GET /orders`           | Solo propias | Solo propias | Todas          | Todas |
| `POST /orders`          | ✅           | ✅           | ✅             | ✅    |
| `PUT /orders/{id}`      | Solo propias | Todas        | Todas          | Todas |
| `GET /users`            | Solo propio  | Solo propio  | Empleados      | Todos |
| `POST /users`           | ❌           | ❌           | Solo empleados | Todos |
| `PUT /users/{id}`       | Solo propio  | Solo propio  | Empleados      | Todos |
| `DELETE /users/{id}`    | ❌           | ❌           | Solo empleados | Todos |

---

## 📊 Modelos de Base de Datos

### **User Model**

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum

class UserRole(enum.Enum):
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    orders = relationship("Order", back_populates="customer")
    audit_logs = relationship("AuditLog", back_populates="user")
```

### **Product Model**

```python
class ProductCategory(enum.Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    SPORTS = "sports"
    HOME = "home"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relaciones
    order_items = relationship("OrderItem", back_populates="product")
    creator = relationship("User")
```

### **Order Model**

```python
class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    customer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
```

---

## 🔐 Funcionalidades de Autenticación

### **1. Registro de Usuario**

- **Endpoint:** `POST /auth/register`
- **Validaciones:** Email único, password fuerte, username único
- **Proceso:** Hash de password, rol por defecto customer, envío de email de verificación (simulado)

### **2. Login de Usuario**

- **Endpoint:** `POST /auth/login`
- **Proceso:** Verificación de credenciales, generación de JWT, logging de auditoría
- **Response:** Access token + refresh token

### **3. Refresh Token**

- **Endpoint:** `POST /auth/refresh`
- **Proceso:** Validación de refresh token, generación de nuevo access token

### **4. Logout**

- **Endpoint:** `POST /auth/logout`
- **Proceso:** Invalidación de tokens, logging de auditoría

### **5. Profile Management**

- **Endpoint:** `GET/PUT /auth/profile`
- **Proceso:** Ver/actualizar perfil propio, cambio de password

---

## 🛡️ Sistema de Protección

### **Dependency Injection para Auth**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    """Obtiene el usuario actual del token JWT"""
    # Implementación completa requerida

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Verifica que el usuario esté activo"""
    # Implementación completa requerida

def require_role(allowed_roles: List[UserRole]):
    """Decorator para requerir roles específicos"""
    # Implementación completa requerida
```

### **Rate Limiting**

- **Login:** Máximo 5 intentos por IP en 15 minutos
- **API calls:** Máximo 100 requests por usuario por hora
- **Public endpoints:** Máximo 10 requests por IP por minuto

### **Audit Logging**

Registrar todos los eventos importantes:

- Login exitoso/fallido
- Cambios de permisos
- Acceso a datos sensibles
- Operaciones CRUD importantes

---

## 🎯 Funcionalidades Requeridas

### **🔥 Funcionalidades Obligatorias (Mínimo para aprobar)**

#### **Autenticación Básica**

1. ✅ **Registro** - Endpoint funcional con validaciones
2. ✅ **Login** - Autenticación con JWT
3. ✅ **Logout** - Invalidación de token
4. ✅ **Profile** - Ver y editar perfil propio

#### **Gestión de Productos**

5. ✅ **Listar productos** - GET /products (público)
6. ✅ **Ver producto** - GET /products/{id} (público)
7. ✅ **Crear producto** - POST /products (employee+)
8. ✅ **Actualizar producto** - PUT /products/{id} (employee+)

#### **Gestión de Órdenes**

9. ✅ **Crear orden** - POST /orders (autenticado)
10. ✅ **Ver órdenes propias** - GET /orders (customer: solo propias)
11. ✅ **Ver orden específica** - GET /orders/{id} (con permisos)

#### **Sistema de Permisos**

12. ✅ **Roles básicos** - customer, employee, manager, admin
13. ✅ **Protección de endpoints** - Middleware de autenticación
14. ✅ **Validación de permisos** - Por rol y recurso

### **⭐ Funcionalidades Avanzadas (Para destacar)**

#### **Seguridad Avanzada**

15. ⭐ **Refresh tokens** - Sistema de renovación de tokens
16. ⭐ **Rate limiting** - Prevención de ataques
17. ⭐ **Audit logging** - Registro de eventos de seguridad
18. ⭐ **Password validation** - Validaciones robustas

#### **Gestión Avanzada**

19. ⭐ **Gestión de usuarios** - CRUD para managers/admins
20. ⭐ **Inventario** - Control de stock en órdenes
21. ⭐ **Filtros avanzados** - Búsqueda de productos por categoría/precio
22. ⭐ **Estadísticas** - Dashboard básico para managers

#### **DevOps y Testing**

23. ⭐ **Test coverage > 80%** - Tests completos
24. ⭐ **Docker setup** - Containerización
25. ⭐ **CI/CD pipeline** - GitHub Actions
26. ⭐ **API documentation** - Swagger docs completo

---

## 📋 Especificaciones Técnicas

### **Dependencies Requeridas**

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic[email]==2.5.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
python-dotenv==1.0.0
```

### **Variables de Entorno**

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/ecommerce_db

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=development
DEBUG=true

# Rate Limiting
LOGIN_RATE_LIMIT=5
API_RATE_LIMIT=100
PUBLIC_RATE_LIMIT=10
```

### **Docker Setup**

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/ecommerce
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 🧪 Testing Requirements

### **Coverage Mínima**

- **Autenticación:** 90%+ coverage
- **Endpoints protegidos:** 85%+ coverage
- **Modelos y schemas:** 80%+ coverage
- **Servicios:** 85%+ coverage

### **Tipos de Tests**

```python
# Estructura de tests requerida
tests/
├── unit/
│   ├── test_auth_service.py
│   ├── test_user_service.py
│   └── test_permissions.py
├── integration/
│   ├── test_auth_endpoints.py
│   ├── test_product_endpoints.py
│   └── test_order_endpoints.py
├── security/
│   ├── test_rate_limiting.py
│   ├── test_jwt_security.py
│   └── test_permission_matrix.py
└── e2e/
    └── test_user_journey.py
```

---

## 📤 Entregables

### **📁 Repository Structure**

```
tu-username/ecommerce-auth-bootcamp/
├── 📁 Código fuente completo
├── 📄 README.md detallado
├── 📄 API documentation (Swagger)
├── 📄 Test results y coverage report
├── 📁 Docker setup funcional
└── 📁 CI/CD pipeline configurado
```

### **📝 Documentación Requerida**

#### **README.md debe incluir:**

1. **Descripción del proyecto**
2. **Instrucciones de instalación**
3. **Uso de la API** con ejemplos
4. **Arquitectura y decisiones técnicas**
5. **Cobertura de tests**
6. **Deployment instructions**

#### **API Documentation:**

- **Swagger docs** completo y actualizado
- **Ejemplos de requests/responses**
- **Códigos de error** documentados
- **Autenticación** claramente explicada

---

## 🎯 Criterios de Evaluación

### **📊 Distribución de Puntos (100 puntos total)**

| Categoría              | Puntos | Descripción                        |
| ---------------------- | ------ | ---------------------------------- |
| **Funcionalidad Core** | 40 pts | Auth básico + CRUD + permisos      |
| **Arquitectura**       | 20 pts | Estructura, separación de concerns |
| **Seguridad**          | 20 pts | JWT, hashing, rate limiting, audit |
| **Testing**            | 10 pts | Coverage, tipos de tests           |
| **Documentación**      | 10 pts | README, API docs, comments         |

### **🏆 Niveles de Logro**

#### **Excelente (90-100 pts)**

- ✅ Todas las funcionalidades obligatorias
- ✅ Al menos 4 funcionalidades avanzadas
- ✅ Test coverage > 85%
- ✅ Documentación completa
- ✅ CI/CD funcionando
- ✅ Buenas prácticas de seguridad

#### **Proficiente (75-89 pts)**

- ✅ Todas las funcionalidades obligatorias
- ✅ Al menos 2 funcionalidades avanzadas
- ✅ Test coverage > 70%
- ✅ Documentación básica completa
- ⚠️ CI/CD parcial

#### **En Desarrollo (60-74 pts)**

- ✅ Funcionalidades obligatorias básicas
- ⚠️ Funcionalidades avanzadas limitadas
- ⚠️ Test coverage > 50%
- ⚠️ Documentación incompleta
- ❌ Sin CI/CD

#### **Insuficiente (< 60 pts)**

- ❌ Funcionalidades obligatorias incompletas
- ❌ Sin funcionalidades avanzadas
- ❌ Test coverage < 50%
- ❌ Documentación insuficiente

---

## 🚀 Deployment

### **Opciones de Deployment**

1. **Heroku** (más simple)
2. **Railway** (recomendado)
3. **DigitalOcean App Platform**
4. **AWS/GCP** (más avanzado)

### **Deployment Checklist**

- [ ] Variables de entorno configuradas
- [ ] Base de datos en production
- [ ] Secrets seguros (no hardcoded)
- [ ] HTTPS habilitado
- [ ] Health checks funcionando
- [ ] Logs configurados

---

## 📅 Timeline Sugerido

### **Día 1-2: Setup y Autenticación**

- ✅ Setup del proyecto y estructura
- ✅ Modelos de base de datos
- ✅ Autenticación básica (register/login)
- ✅ Tests de autenticación

### **Día 3-4: Core Features**

- ✅ CRUD de productos
- ✅ Sistema de órdenes básico
- ✅ Sistema de permisos
- ✅ Tests de funcionalidad

### **Día 5-6: Seguridad y Polish**

- ✅ Funcionalidades avanzadas elegidas
- ✅ Rate limiting y audit
- ✅ Documentación completa
- ✅ CI/CD y deployment

### **Día 7: Testing y Entrega**

- ✅ Testing final completo
- ✅ Documentación final
- ✅ Video demo (opcional)
- ✅ Entrega en GitHub

---

## 🆘 Soporte y Recursos

### **🔗 Enlaces Útiles**

- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- [Pytest FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)

### **🆘 Soporte Técnico**

- **GitHub Issues** con label `proyecto-semana-5`
- **Code review** disponible vía pull requests
- **Office hours** según calendario del bootcamp

---

## 📋 Checklist Final

### **Pre-entrega**

- [ ] Todas las funcionalidades obligatorias implementadas
- [ ] Tests pasando con coverage adecuado
- [ ] Documentación completa
- [ ] Repository limpio y organizado
- [ ] CI/CD configurado

### **Entrega**

- [ ] Pull request creado a tiempo
- [ ] README.md actualizado
- [ ] Video demo grabado (opcional)
- [ ] Issues cerrados
- [ ] Feedback incorporado

---

**🎯 ¡Este proyecto es tu oportunidad de demostrar todo lo aprendido sobre seguridad en APIs! Tómate el tiempo necesario para hacerlo bien y no dudes en pedir ayuda cuando la necesites.**
