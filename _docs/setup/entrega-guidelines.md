# Reglas de Entrega - Bootcamp bc-fastapi

## 🎯 Principio Fundamental

**TODOS los entregables deben ser exclusivamente a través de GitHub**

No se aceptan entregas por:

- ❌ Email
- ❌ Drives compartidos
- ❌ USB o medios físicos
- ❌ Otras plataformas de código
- ❌ Archivos ZIP enviados directamente

## 📋 Proceso de Entrega Obligatorio

### 1. Repositorio Personal

Cada aprendiz debe tener:

```
github.com/[username]/bc-fastapi-[apellido]
```

**Ejemplo**: `github.com/juan-perez/bc-fastapi-perez`

### 2. Estructura de Entrega por Semana

```
bc-fastapi-[apellido]/
├── semana-01/
│   ├── proyecto/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── ejercicios/
│   └── reflexiones.md
├── semana-02/
└── ...
```

### 3. Pull Request para Cada Entrega

- **Rama específica**: `semana-XX-entrega`
- **PR hacia main** con descripción completa
- **Auto-asignación** del PR
- **Labels apropiados**: `semana-XX`, `entrega`, `ready-for-review`

### 4. Checklist de Entrega

Cada PR debe incluir:

- [ ] ✅ Código funcional sin errores
- [ ] ✅ Tests implementados y pasando
- [ ] ✅ README.md con instrucciones claras
- [ ] ✅ Documentación de API (si aplica)
- [ ] ✅ Dockerfile funcional (a partir semana 4)
- [ ] ✅ CI/CD pipeline verde
- [ ] ✅ Code coverage > 80%
- [ ] ✅ Convenciones de nomenclatura aplicadas

## ⏰ Calendario de Entregas

### Deadlines Estrictos

- **Código completo**: Viernes 11:59 PM
- **Pull Request**: Sábado 11:59 PM
- **Presentación**: Siguiente miércoles/jueves/sábado

### Proceso de Review

1. **Auto-review**: Aprendiz revisa su propio código
2. **Peer review**: Compañero asignado revisa
3. **Instructor review**: Evaluación final
4. **Feedback**: Comentarios específicos en GitHub

## 📊 Sistema de Evaluación

### Criterios Técnicos (70%)

#### Funcionalidad (25%)

- ✅ Todos los requisitos implementados
- ✅ Aplicación ejecuta sin errores
- ✅ Edge cases manejados apropiadamente
- ✅ Performance aceptable

#### Calidad de Código (25%)

- ✅ Nomenclatura en inglés aplicada
- ✅ Clean code principles
- ✅ Separation of concerns
- ✅ No código duplicado (DRY)

#### Testing (10%)

- ✅ Unit tests implementados
- ✅ Integration tests (cuando aplique)
- ✅ Code coverage > 80%
- ✅ Tests documentados

#### Documentación (10%)

- ✅ README completo y claro
- ✅ Docstrings en funciones críticas
- ✅ API documentation
- ✅ Setup instructions funcionan

### Criterios Profesionales (20%)

#### Git Workflow (10%)

- ✅ Commits descriptivos y frecuentes
- ✅ Branch naming conventions
- ✅ PR descriptions completas
- ✅ Git history limpio

#### CI/CD Implementation (10%)

- ✅ Pipeline configurado correctamente
- ✅ Automated testing funcionando
- ✅ Quality gates implementados
- ✅ Deployment ready (semanas avanzadas)

### Criterios Actitudinales (10%)

#### Participación (5%)

- ✅ Contribución a discussions
- ✅ Code reviews a compañeros
- ✅ Preguntas constructivas
- ✅ Ayuda a otros aprendices

#### Crecimiento Continuo (5%)

- ✅ Aplicación de feedback previo
- ✅ Mejora progresiva semana a semana
- ✅ Iniciativa en aprendizaje
- ✅ Experimentación apropiada

## 🚨 Políticas de Penalización

### Entregas Tardías

- **1-24 horas tarde**: -10%
- **1-2 días tarde**: -25%
- **2-3 días tarde**: -50%
- **Más de 3 días**: No aceptada (0 puntos)

### Violaciones de Calidad

- **No seguir nomenclatura**: -15%
- **Tests faltantes**: -20%
- **CI/CD roto**: -25%
- **README inexistente/incompleto**: -10%
- **Código no funcional**: -50%

### Violaciones de Proceso

- **Entrega fuera de GitHub**: No aceptada
- **No usar PR process**: -30%
- **Commits sin descripción**: -5% por commit
- **Plagio detectado**: 0 puntos + reporte académico

## 🏆 Sistema de Reconocimiento

### Badges en GitHub

- 🌟 **Perfect Delivery**: Entrega perfecta sin observaciones
- ⚡ **Early Bird**: Entregado 24h antes del deadline
- 🧪 **Testing Champion**: Coverage > 95%
- 📚 **Documentation Hero**: Documentación excepcional
- 🔧 **CI/CD Master**: Pipeline impecable
- 🤝 **Code Reviewer**: Excelentes reviews a compañeros

### Leaderboard Semanal

Ranking público basado en:

- Calidad de entrega
- Tiempo de entrega
- Contribución a la comunidad
- Mejora continua

## 📝 Templates de Entrega

### README.md Template

````markdown
# Semana XX - [Nombre del Proyecto]

## Descripción

Breve descripción del proyecto desarrollado.

## Objetivos Logrados

- [ ] Objetivo 1
- [ ] Objetivo 2
- [ ] Objetivo 3

## Tecnologías Utilizadas

- FastAPI
- PostgreSQL
- Docker
- [Otras tecnologías]

## Setup Instructions

```bash
# Clonar repositorio
git clone [repo-url]

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
uvicorn main:app --reload
```
````

## API Endpoints

- `GET /` - Descripción
- `POST /users` - Descripción
- [Otros endpoints]

## Testing

```bash
# Ejecutar tests
pytest

# Coverage report
pytest --cov=src/
```

## Reflexiones de Aprendizaje

### Desafíos Encontrados

[Descripción de dificultades y cómo se resolvieron]

### Nuevos Conocimientos

[Lo que se aprendió durante la semana]

### Próximos Pasos

[Qué se mejorará o implementará próximamente]

````

### Pull Request Template
```markdown
## Entrega Semana XX

### Resumen
Descripción breve de lo implementado esta semana.

### Checklist de Entrega
- [ ] Código funcional sin errores
- [ ] Tests implementados (coverage > 80%)
- [ ] README.md actualizado
- [ ] Convenciones de nomenclatura aplicadas
- [ ] CI/CD pipeline verde
- [ ] Dockerfile funcional (si aplica)

### Objetivos Completados
- [x] Objetivo 1: Descripción
- [x] Objetivo 2: Descripción
- [ ] Objetivo 3: En progreso (razón)

### Desafíos y Soluciones
**Desafío**: [Descripción del problema]
**Solución**: [Cómo se resolvió]

### Screenshots (si aplica)
[Capturas de pantalla de la aplicación funcionando]

### Testing Evidence
[Capturas del coverage report y tests pasando]

### Próximos Pasos
[Qué se planea mejorar o implementar]

---
**Ready for Review**: ✅
**Estimación de tiempo de review**: 30 minutos
````

## 🔄 Proceso de Feedback

### Timeline de Review

1. **Entrega**: Viernes 11:59 PM
2. **Peer Review**: Sábado-Domingo
3. **Instructor Review**: Lunes-Martes
4. **Feedback Delivery**: Miércoles antes de clase
5. **Discussion**: Durante la clase

### Tipos de Feedback

- **Inline Comments**: Comentarios específicos en código
- **PR Review**: Evaluación general del pull request
- **Issue Creation**: Para mejoras futuras
- **1:1 Sessions**: Para casos que requieren discusión profunda

### Aplicación de Feedback

- **Immediate**: Correcciones críticas
- **Next Delivery**: Mejoras para siguiente semana
- **Long-term**: Objetivos de crecimiento a largo plazo

## 📊 Métricas de Seguimiento

### Por Aprendiz

- Tiempo promedio de entrega
- Calidad score promedio
- Evolución semana a semana
- Participación en code reviews

### Por Cohorte

- Porcentaje de entregas a tiempo
- Distribución de calificaciones
- Tendencias de mejora
- Colaboración inter-aprendices

## 🎯 Objetivo Final

Al finalizar el bootcamp, cada aprendiz tendrá:

- **Portfolio completo** en GitHub con 12 proyectos profesionales
- **Historial de commits** que demuestra progresión y disciplina
- **Experiencia real** en code reviews y colaboración
- **Competencias industriales** en Git/GitHub y CI/CD
- **Red profesional** construida a través de colaboración

**Recordatorio**: GitHub será tu carta de presentación profesional. Cada commit cuenta.
