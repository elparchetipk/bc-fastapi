# GUÍA RÁPIDA - SEMANA 4: BASE DE DATOS

## ⚡ Setup en 5 Minutos

### 1. Prerrequisitos

- ✅ Python 3.9+ instalado
- ✅ VS Code con extensión Python
- ✅ Conocimientos de FastAPI básico (Semanas 1-3)

### 2. Instalación Express

```bash
# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python -c "import fastapi, sqlalchemy; print('✅ Todo listo')"

# Ejecutar ejemplo
python ejemplo_main.py
```

### 3. Primer Test

```bash
# Abrir en el navegador
# http://localhost:8000 - Página principal
# http://localhost:8000/docs - Documentación interactiva
# ✅ Servidor funcionando
# ✅ Tests básicos pasando
```

## 🚀 Funcionalidades por Implementar

### Mínimo Viable (3.5 horas)

- [ ] **Modelos SQLAlchemy** (45 min)
- [ ] **CRUD Libros** (60 min)
- [ ] **CRUD Usuarios** (45 min)
- [ ] **Sistema Préstamos** (60 min)

### Testing y Documentación (2 horas)

- [ ] **Tests básicos** (60 min)
- [ ] **Validaciones** (30 min)
- [ ] **README y docs** (30 min)

## 📋 Checklist de Desarrollo

### Paso 1: Configuración (45 min)

- [ ] Crear estructura de proyecto
- [ ] Configurar SQLAlchemy + SQLite
- [ ] Definir modelos básicos (Book, User, Loan)
- [ ] Probar conexión a BD

### Paso 2: CRUD Libros (60 min)

- [ ] Endpoints POST, GET, PUT, DELETE
- [ ] Schemas Pydantic para validación
- [ ] Operaciones CRUD en base de datos
- [ ] Probar con documentación automática

### Paso 3: CRUD Usuarios (45 min)

- [ ] Endpoints similares a libros
- [ ] Validación de email único
- [ ] Restricción: no eliminar con préstamos activos
- [ ] Tests manuales básicos

### Paso 4: Sistema Préstamos (60 min)

- [ ] Modelo Loan con relaciones
- [ ] Endpoint crear préstamo
- [ ] Endpoint devolver libro
- [ ] Lógica de disponibilidad de libros
- [ ] Validación: máximo 3 préstamos por usuario

### Paso 5: Testing (60 min)

- [ ] Tests de CRUD básico
- [ ] Tests de validaciones
- [ ] Tests de reglas de negocio
- [ ] Al menos 10 tests que pasen

### Paso 6: Documentación (30 min)

- [ ] README con instrucciones
- [ ] Comentarios en código complejo
- [ ] Verificar documentación automática

## 🐛 Troubleshooting Común

### Error: "No module named 'sqlalchemy'"

**Solución:**

```bash
pip install sqlalchemy
```

### Error: "database is locked"

**Solución:**

- Cerrar todas las conexiones a la BD
- Reiniciar el servidor
- Eliminar archivo `library.db` si es necesario

### Error: "Validation error"

**Solución:**

- Verificar que todos los campos requeridos estén presentes
- Revisar tipos de datos en schemas Pydantic
- Usar la documentación automática para ver el formato correcto

### Error: "Book not available"

**Solución:**

- Verificar que `is_available = True` antes de crear préstamo
- Revisar si el libro ya está prestado a otro usuario

## 📚 Referencias Rápidas

### SQLAlchemy Basics

```python
# Definir modelo
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

# Query básica
books = db.query(Book).all()
book = db.query(Book).filter(Book.id == 1).first()
```

### Pydantic Validation

```python
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
```

### FastAPI + SQLAlchemy

```python
@app.post("/books/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    return db_book
```

## 🎯 Objetivos de la Semana

- ✅ **Integrar** SQLAlchemy con FastAPI
- ✅ **Crear** modelos relacionales básicos
- ✅ **Implementar** CRUD completo con BD
- ✅ **Aplicar** validaciones de negocio
- ✅ **Testing** básico con pytest

## 💡 Tips de Productividad

1. **Usa la documentación automática**: http://localhost:8000/docs
2. **Desarrolla paso a paso**: Una entidad completa antes de seguir
3. **Prueba frecuentemente**: Cada endpoint después de crearlo
4. **Mantén simple**: No optimices prematuramente
5. **Copia del ejemplo**: Úsalo como referencia, no lo copies completo

## ⚠️ Errores Comunes a Evitar

- ❌ No definir relaciones entre modelos
- ❌ Olvidar validar campos únicos (email, ISBN)
- ❌ No manejar libros no disponibles
- ❌ Tests que no prueban la lógica de negocio
- ❌ README sin instrucciones de instalación

¡Éxito en tu proyecto de biblioteca! 📚🚀
