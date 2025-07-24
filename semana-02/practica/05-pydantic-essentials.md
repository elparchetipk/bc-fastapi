# Práctica 5: Fundamentos de Pydantic para APIs

## 🎯 Objetivo

Dominar Pydantic para crear modelos de datos robustos y validación automática en FastAPI, construyendo sobre la API de la Semana 1.

## ⏱️ Tiempo Estimado: 120 minutos

## 📋 Pre-requisitos

- ✅ API de Semana 1 funcionando
- ✅ Entorno FastAPI configurado
- ✅ Conocimiento básico de Python classes

## 🧱 ¿Qué es Pydantic?

Pydantic es la biblioteca que usa FastAPI internamente para:

- ✅ **Validación automática** de datos de entrada
- ✅ **Conversión de tipos** automática
- ✅ **Documentación automática** de esquemas
- ✅ **Serialización/deserialización** JSON

## 🚀 Paso 1: Modelos Básicos (30 min)

Vamos a evolucionar nuestra API de Semana 1 con modelos Pydantic:

```python
# Actualizar main.py con modelos
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

app = FastAPI(
    title="API con Pydantic - Semana 2",
    description="API evolucionada con validación robusta",
    version="2.0.0"
)

# Enum para categorías
class CategoriaPersona(str, Enum):
    estudiante = "estudiante"
    instructor = "instructor"
    administrador = "administrador"

# Modelo base para Persona
class PersonaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre completo")
    edad: int = Field(..., ge=18, le=120, description="Edad en años")
    email: EmailStr = Field(..., description="Email válido")
    categoria: CategoriaPersona = Field(..., description="Categoría de la persona")
    activo: bool = Field(default=True, description="Estado activo")

# Modelo para crear persona (entrada)
class PersonaCreate(PersonaBase):
    pass

# Modelo para respuesta (salida)
class PersonaResponse(PersonaBase):
    id: int = Field(..., description="ID único generado")
    timestamp: datetime = Field(..., description="Fecha de creación")

    class Config:
        # Ejemplo de respuesta en la documentación
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Ana García",
                "edad": 25,
                "email": "ana@ejemplo.com",
                "categoria": "estudiante",
                "activo": True,
                "timestamp": "2025-07-24T10:30:00"
            }
        }

# Almacenamiento temporal
personas: List[PersonaResponse] = []
```

## 🔍 Paso 2: Validación Avanzada (45 min)

```python
# Agregar más modelos con validación avanzada
from pydantic import validator, root_validator

class Curso(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    duracion_horas: int = Field(..., ge=1, le=200)
    precio: float = Field(..., ge=0, description="Precio en USD")
    instructor_id: int = Field(..., ge=1)
    tags: List[str] = Field(default=[], max_items=10)

    @validator('tags')
    def validar_tags(cls, v):
        # Convertir a lowercase y remover duplicados
        return list(set(tag.lower().strip() for tag in v if tag.strip()))

    @validator('titulo')
    def validar_titulo(cls, v):
        if any(char in v for char in ['<', '>', '&']):
            raise ValueError('Título no puede contener caracteres HTML')
        return v.strip().title()

    @root_validator
    def validar_curso_completo(cls, values):
        duracion = values.get('duracion_horas')
        precio = values.get('precio')

        # Cursos muy largos deben tener precio mínimo
        if duracion and duracion > 50 and precio and precio < 100:
            raise ValueError('Cursos de más de 50 horas deben costar al menos $100')

        return values

class CursoResponse(Curso):
    id: int
    fecha_creacion: datetime
    estudiantes_inscritos: int = Field(default=0)

# Modelo para inscripción
class Inscripcion(BaseModel):
    persona_id: int = Field(..., ge=1)
    curso_id: int = Field(..., ge=1)
    fecha_inscripcion: Optional[datetime] = Field(default_factory=datetime.now)
    notas: Optional[str] = Field(None, max_length=200)

class InscripcionResponse(Inscripcion):
    id: int
    persona: PersonaResponse
    curso: CursoResponse
```

## 📝 Paso 3: Implementar Endpoints con Modelos (30 min)

```python
# Almacenamiento temporal extendido
cursos: List[CursoResponse] = []
inscripciones: List[InscripcionResponse] = []

# Endpoints para personas (mejorados)
@app.post("/personas", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def crear_persona(persona: PersonaCreate):
    """Crear nueva persona con validación completa"""
    # Verificar email único
    for p in personas:
        if p.email == persona.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {persona.email} ya está registrado"
            )

    nueva_persona = PersonaResponse(
        id=len(personas) + 1,
        timestamp=datetime.now(),
        **persona.dict()
    )
    personas.append(nueva_persona)
    return nueva_persona

@app.get("/personas", response_model=List[PersonaResponse])
def listar_personas(
    categoria: Optional[CategoriaPersona] = None,
    activo: bool = True,
    limit: int = Field(default=10, ge=1, le=100)
):
    """Listar personas con filtros opcionales"""
    resultado = [p for p in personas if p.activo == activo]

    if categoria:
        resultado = [p for p in resultado if p.categoria == categoria]

    return resultado[:limit]

@app.get("/personas/{persona_id}", response_model=PersonaResponse)
def obtener_persona(persona_id: int = Field(..., ge=1)):
    """Obtener persona por ID"""
    for persona in personas:
        if persona.id == persona_id:
            return persona

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Persona con ID {persona_id} no encontrada"
    )

# Endpoints para cursos
@app.post("/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def crear_curso(curso: Curso):
    """Crear nuevo curso con validación automática"""
    # Verificar que instructor existe
    instructor = next((p for p in personas if p.id == curso.instructor_id), None)
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Instructor con ID {curso.instructor_id} no encontrado"
        )

    if instructor.categoria != CategoriaPersona.instructor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo personas con categoría 'instructor' pueden crear cursos"
        )

    nuevo_curso = CursoResponse(
        id=len(cursos) + 1,
        fecha_creacion=datetime.now(),
        **curso.dict()
    )
    cursos.append(nuevo_curso)
    return nuevo_curso

@app.get("/cursos", response_model=List[CursoResponse])
def listar_cursos(
    instructor_id: Optional[int] = None,
    precio_max: Optional[float] = Field(None, ge=0),
    duracion_min: Optional[int] = Field(None, ge=1)
):
    """Listar cursos con filtros"""
    resultado = cursos.copy()

    if instructor_id:
        resultado = [c for c in resultado if c.instructor_id == instructor_id]

    if precio_max is not None:
        resultado = [c for c in resultado if c.precio <= precio_max]

    if duracion_min is not None:
        resultado = [c for c in resultado if c.duracion_horas >= duracion_min]

    return resultado
```

## 🔗 Paso 4: Relaciones y Operaciones Complejas (15 min)

```python
@app.post("/inscripciones", response_model=InscripcionResponse)
def inscribir_persona(inscripcion: Inscripcion):
    """Inscribir persona a curso"""
    # Verificar que persona existe
    persona = next((p for p in personas if p.id == inscripcion.persona_id), None)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )

    # Verificar que curso existe
    curso = next((c for c in cursos if c.id == inscripcion.curso_id), None)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )

    # Verificar inscripción duplicada
    for insc in inscripciones:
        if insc.persona_id == inscripcion.persona_id and insc.curso_id == inscripcion.curso_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Persona ya está inscrita en este curso"
            )

    nueva_inscripcion = InscripcionResponse(
        id=len(inscripciones) + 1,
        persona=persona,
        curso=curso,
        **inscripcion.dict()
    )
    inscripciones.append(nueva_inscripcion)

    # Actualizar contador de estudiantes en curso
    curso.estudiantes_inscritos += 1

    return nueva_inscripcion

@app.get("/inscripciones/{persona_id}", response_model=List[InscripcionResponse])
def obtener_inscripciones_persona(persona_id: int):
    """Obtener todas las inscripciones de una persona"""
    resultado = [insc for insc in inscripciones if insc.persona_id == persona_id]
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron inscripciones para esta persona"
        )
    return resultado
```

## ✅ Verificación y Testing (20 min)

Crear archivo `test_models.py` para probar los modelos:

```python
#!/usr/bin/env python3
"""
Testing básico de modelos Pydantic
"""

from pydantic import ValidationError
import pytest
from main import PersonaCreate, Curso, CategoriaPersona

def test_persona_valida():
    """Test persona con datos válidos"""
    persona = PersonaCreate(
        nombre="Ana García",
        edad=25,
        email="ana@ejemplo.com",
        categoria=CategoriaPersona.estudiante
    )
    assert persona.nombre == "Ana García"
    assert persona.edad == 25
    assert persona.activo == True  # default

def test_persona_email_invalido():
    """Test validación de email"""
    with pytest.raises(ValidationError) as exc:
        PersonaCreate(
            nombre="Ana",
            edad=25,
            email="email-invalido",
            categoria=CategoriaPersona.estudiante
        )
    assert "value is not a valid email address" in str(exc.value)

def test_curso_validacion_precio():
    """Test validación de curso largo y barato"""
    with pytest.raises(ValidationError) as exc:
        Curso(
            titulo="Curso Muy Largo",
            duracion_horas=100,
            precio=50,  # Muy barato para curso largo
            instructor_id=1
        )
    assert "deben costar al menos $100" in str(exc.value)

def test_curso_tags_duplicados():
    """Test limpieza de tags duplicados"""
    curso = Curso(
        titulo="Curso de Python",
        duracion_horas=20,
        precio=200,
        instructor_id=1,
        tags=["python", "PYTHON", "  Python  ", "api"]
    )
    assert curso.tags == ["python", "api"]  # duplicados removidos

if __name__ == "__main__":
    print("🧪 Ejecutando tests de modelos...")

    try:
        test_persona_valida()
        print("✅ Test persona válida: PASS")

        test_persona_email_invalido()
        print("✅ Test email inválido: PASS")

        test_curso_validacion_precio()
        print("✅ Test validación precio: PASS")

        test_curso_tags_duplicados()
        print("✅ Test tags duplicados: PASS")

        print("\n🎉 Todos los tests pasaron!")

    except Exception as e:
        print(f"❌ Error en tests: {e}")
```

## 🎯 Objetivos Logrados

Al finalizar esta práctica, habrás implementado:

- ✅ **Modelos Pydantic robustos** con validación automática
- ✅ **Validators personalizados** para lógica de negocio
- ✅ **Response models** para documentación clara
- ✅ **Enums** para valores predefinidos
- ✅ **Relaciones básicas** entre modelos
- ✅ **Testing de modelos** para verificar validación

## 🔍 Puntos Clave de Pydantic

### **Field() para Validación Avanzada**

```python
# Ejemplo completo de Field()
precio: float = Field(
    ...,                    # Required
    ge=0,                   # Mayor o igual a 0
    le=10000,              # Menor o igual a 10000
    description="Precio en USD",
    example=299.99
)
```

### **Validators para Lógica Custom**

```python
@validator('email')
def email_debe_ser_corporativo(cls, v):
    if not v.endswith('@empresa.com'):
        raise ValueError('Email debe ser corporativo')
    return v
```

### **Config para Comportamiento**

```python
class Config:
    # Validar asignaciones
    validate_assignment = True
    # Permitir población por nombre de atributo
    allow_population_by_field_name = True
    # Ejemplo para documentación
    schema_extra = {"example": {...}}
```

## 🚀 Próximos Pasos

1. **Inmediato**: Testa todos los endpoints con los nuevos modelos
2. **Siguiente bloque**: Async/await para operaciones más eficientes
3. **Semana 3**: Conectar estos modelos a una base de datos real

## 📝 Entregable de Este Bloque

- **Archivo `main.py`** con todos los modelos Pydantic implementados
- **Al menos 8-10 endpoints** usando response_model
- **Validación funcionando** correctamente
- **Tests básicos** pasando (opcional pero recomendado)

---

**💡 Tip**: Pydantic hace que FastAPI genere documentación automática increíble. Visita `/docs` para ver cómo se ve tu API ahora!
