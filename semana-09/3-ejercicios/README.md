# Ejercicios - Semana 9: Containerización con Docker

## 📋 Información General

Esta carpeta contiene los ejercicios prácticos de la semana 9, enfocados en containerización con Docker. Los ejercicios están diseñados para ser completados durante las 6 horas de la semana y consolidar los conocimientos adquiridos en las prácticas.

## 🎯 Objetivos de los Ejercicios

- Aplicar conceptos de containerización en escenarios prácticos
- Desarrollar habilidades en creación y optimización de Dockerfiles
- Practicar orquestación multi-servicio con Docker Compose
- Implementar pipelines de CI/CD con Docker
- Configurar monitoreo y observabilidad de contenedores

## 📁 Contenido

### `ejercicios-docker.md`

Archivo principal con todos los ejercicios de la semana:

1. **Ejercicio 1**: Containerización Básica - Blog API
2. **Ejercicio 2**: Multi-container con Docker Compose - E-commerce
3. **Ejercicio 3**: Pipeline CI/CD - Task Manager
4. **Ejercicio 4**: Monitoreo y Observabilidad - Social Media API
5. **Ejercicio 5**: Optimización y Seguridad - Financial Dashboard
6. **Ejercicio Integrador**: Sistema Completo con Todas las Tecnologías

## ⏱️ Distribución de Tiempo

| Ejercicio   | Tiempo Estimado  | Dificultad | Prioridad |
| ----------- | ---------------- | ---------- | --------- |
| Ejercicio 1 | 45 min           | Básica     | Alta      |
| Ejercicio 2 | 60 min           | Intermedia | Alta      |
| Ejercicio 3 | 45 min           | Intermedia | Media     |
| Ejercicio 4 | 45 min           | Avanzada   | Media     |
| Ejercicio 5 | 30 min           | Avanzada   | Baja      |
| Integrador  | 75 min           | Avanzada   | Alta      |
| **Total**   | **300 min (5h)** | -          | -         |

## 🚀 Cómo Empezar

### Prerrequisitos

1. **Docker instalado y funcionando**:

   ```bash
   docker --version
   docker run hello-world
   ```

2. **Docker Compose disponible**:

   ```bash
   docker-compose --version
   ```

3. **Git configurado**:

   ```bash
   git --version
   ```

4. **Editor de código** (VS Code recomendado con extensión Docker)

### Estructura de Trabajo Recomendada

```
semana-09-ejercicios/
├── ejercicio-1/
│   ├── app/
│   ├── Dockerfile
│   └── README.md
├── ejercicio-2/
│   ├── backend/
│   ├── frontend/
│   ├── docker-compose.yml
│   └── README.md
├── ejercicio-3/
│   ├── .github/workflows/
│   ├── app/
│   ├── Dockerfile
│   └── README.md
└── ...
```

## 📋 Checklist de Entrega

### Para Cada Ejercicio Individual

- [ ] **Código fuente** completo y organizado
- [ ] **Dockerfile** optimizado y documentado
- [ ] **docker-compose.yml** (si aplica) con servicios configurados
- [ ] **README.md** con instrucciones de instalación y uso
- [ ] **Evidencias** de funcionamiento (capturas de pantalla o logs)
- [ ] **Comandos de validación** ejecutados exitosamente

### Para el Ejercicio Integrador

- [ ] **Arquitectura completa** implementada
- [ ] **Servicios orquestados** con Docker Compose
- [ ] **Pipeline CI/CD** configurado y funcional
- [ ] **Monitoreo** implementado con métricas visibles
- [ ] **Documentación** completa del sistema
- [ ] **Optimizaciones** de seguridad aplicadas
- [ ] **Tests** automatizados pasando

## 🎯 Criterios de Evaluación

### Ejercicios Básicos (1-2)

- **Funcionalidad** (40%): La aplicación funciona correctamente
- **Dockerfile** (30%): Optimización y mejores prácticas
- **Documentación** (20%): Instrucciones claras y completas
- **Organización** (10%): Estructura de proyecto ordenada

### Ejercicios Avanzados (3-5)

- **Implementación técnica** (35%): Corrección de la solución
- **Arquitectura** (25%): Diseño de la solución
- **Seguridad** (20%): Prácticas de seguridad aplicadas
- **Documentación** (15%): Calidad de la documentación
- **Innovación** (5%): Soluciones creativas o mejoras adicionales

### Ejercicio Integrador

- **Funcionalidad completa** (30%): Todos los componentes funcionan
- **Integración** (25%): Los servicios se comunican correctamente
- **Operaciones** (20%): CI/CD y monitoreo implementados
- **Calidad del código** (15%): Código limpio y mantenible
- **Documentación** (10%): Documentación profesional

## 🛠️ Herramientas de Apoyo

### Comandos Útiles

```bash
# Verificar estado de Docker
docker system df
docker system info

# Limpiar recursos no utilizados
docker system prune

# Ver logs de servicios
docker-compose logs -f [servicio]

# Validar Dockerfile
docker run --rm -i hadolint/hadolint < Dockerfile

# Analizar imagen
dive imagen:tag
```

### Scripts de Ayuda

#### Verificación de Requisitos

```bash
#!/bin/bash
# check-requirements.sh
echo "🔍 Verificando requisitos..."

# Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker: $(docker --version)"
else
    echo "❌ Docker no encontrado"
fi

# Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose: $(docker-compose --version)"
else
    echo "❌ Docker Compose no encontrado"
fi

# Git
if command -v git &> /dev/null; then
    echo "✅ Git: $(git --version)"
else
    echo "❌ Git no encontrado"
fi

echo "🏁 Verificación completada"
```

#### Template de Validación

```bash
#!/bin/bash
# validate-exercise.sh
EXERCISE_DIR=$1

echo "🧪 Validando ejercicio en $EXERCISE_DIR..."

cd $EXERCISE_DIR

# Verificar archivos requeridos
if [[ -f "Dockerfile" ]]; then
    echo "✅ Dockerfile encontrado"
    # Validar con hadolint si está disponible
    if command -v hadolint &> /dev/null; then
        hadolint Dockerfile
    fi
else
    echo "❌ Dockerfile no encontrado"
fi

if [[ -f "docker-compose.yml" ]]; then
    echo "✅ docker-compose.yml encontrado"
    docker-compose config
else
    echo "⚠️  docker-compose.yml no encontrado (puede no ser necesario)"
fi

if [[ -f "README.md" ]]; then
    echo "✅ README.md encontrado"
else
    echo "❌ README.md no encontrado"
fi

echo "🏁 Validación completada"
```

## 📚 Recursos de Apoyo

### Documentación Rápida

- [Docker Cheatsheet](../5-recursos/docker-cheatsheet.md)
- [Referencias](../5-recursos/referencias.md)
- [Herramientas Docker](../5-recursos/herramientas-docker.md)

### Videos Recomendados

- [Videos y Tutoriales](../5-recursos/videos-tutoriales.md)

### Para Debugging

1. **Logs detallados**: `docker-compose logs -f`
2. **Acceder a contenedores**: `docker exec -it <container> /bin/bash`
3. **Verificar redes**: `docker network inspect <network>`
4. **Ver recursos**: `docker stats`

## 🆘 Troubleshooting Común

### Problemas Frecuentes

#### "Port already in use"

```bash
# Encontrar proceso usando el puerto
sudo lsof -i :8000
# O cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Puerto externo diferente
```

#### "Cannot connect to Docker daemon"

```bash
# Verificar estado del servicio
sudo systemctl status docker
# Iniciar si está parado
sudo systemctl start docker
```

#### "No space left on device"

```bash
# Limpiar recursos Docker
docker system prune -a --volumes
```

#### "Permission denied"

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# Reiniciar sesión
```

### Comandos de Diagnóstico

```bash
# Estado general del sistema Docker
docker system info

# Espacio utilizado
docker system df

# Procesos en contenedores
docker stats

# Logs de Docker daemon
journalctl -u docker.service
```

## 📬 Entrega de Ejercicios

### Formato de Entrega

1. **Crear repositorio** para cada ejercicio o uno general
2. **Estructura clara** de carpetas
3. **README.md** en cada ejercicio con:
   - Descripción del ejercicio
   - Instrucciones de instalación
   - Comandos para ejecutar
   - Capturas de pantalla o evidencias
4. **Commits descriptivos** con mensajes claros

### Información a Incluir

- **Nombre del estudiante**
- **Fecha de entrega**
- **Ejercicios completados**
- **Tiempo invertido**
- **Dificultades encontradas**
- **Aprendizajes clave**

## 🎯 Siguientes Pasos

Después de completar estos ejercicios, deberías ser capaz de:

1. **Containerizar** cualquier aplicación Python/FastAPI
2. **Orquestar** múltiples servicios con Docker Compose
3. **Implementar** pipelines básicos de CI/CD
4. **Configurar** monitoreo básico de contenedores
5. **Aplicar** mejores prácticas de seguridad

### Continuando el Aprendizaje

- Explora **Kubernetes** para orquestación avanzada
- Profundiza en **security scanning** y compliance
- Aprende sobre **service mesh** y microservicios
- Investiga **serverless containers** (AWS Fargate, etc.)

---

## 💡 Consejos Finales

1. **Lee completamente** cada ejercicio antes de empezar
2. **Planifica tu tiempo** - algunos ejercicios son más largos
3. **Usa el debugging** cuando algo no funcione
4. **Documenta tus decisiones** en los README
5. **No tengas miedo** de experimentar y modificar
6. **Busca ayuda** en los recursos proporcionados

---

**¡Éxito con los ejercicios de Docker! 🐳**
