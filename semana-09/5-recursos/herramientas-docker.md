# Herramientas Útiles para Docker - Semana 9

## 🖥️ Interfaces Gráficas (GUI)

### Docker Desktop

- **Plataforma**: Windows, macOS, Linux
- **Descripción**: Interfaz oficial de Docker con GUI completa
- **Características**:
  - Gestión visual de contenedores e imágenes
  - Integración con VS Code
  - Kubernetes integrado
  - Dashboard de recursos
- **URL**: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

### Portainer

- **Plataforma**: Web-based (multi-plataforma)
- **Descripción**: Interfaz web para gestión de Docker
- **Instalación**:
  ```bash
  docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer-ce
  ```
- **Características**:
  - Dashboard completo
  - Gestión de stacks (Compose)
  - Control de acceso
  - Templates predefinidos
- **URL**: [https://www.portainer.io/](https://www.portainer.io/)

### Lazydocker

- **Plataforma**: Terminal UI (Linux, macOS, Windows)
- **Descripción**: Interfaz de terminal simple y efectiva
- **Instalación**:

  ```bash
  # Con curl
  curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash

  # Con Homebrew (macOS)
  brew install lazydocker
  ```

- **Características**:
  - Navegación con teclado
  - Vista de logs en tiempo real
  - Gestión rápida de contenedores
- **URL**: [https://github.com/jesseduffield/lazydocker](https://github.com/jesseduffield/lazydocker)

## 🔧 Herramientas de Línea de Comandos

### ctop

- **Descripción**: Top-like para contenedores Docker
- **Instalación**:

  ```bash
  # Linux
  sudo wget https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 -O /usr/local/bin/ctop
  sudo chmod +x /usr/local/bin/ctop

  # macOS
  brew install ctop
  ```

- **Uso**: `ctop`
- **Características**:
  - Monitoreo en tiempo real
  - Métricas de CPU, memoria, red
  - Interfaz interactiva

### dive

- **Descripción**: Analiza capas de imágenes Docker
- **Instalación**:

  ```bash
  # Linux
  wget https://github.com/wagoodman/dive/releases/download/v0.10.0/dive_0.10.0_linux_amd64.deb
  sudo apt install ./dive_0.10.0_linux_amd64.deb

  # macOS
  brew install dive
  ```

- **Uso**: `dive <imagen>:<tag>`
- **Características**:
  - Explora capas de imágenes
  - Identifica archivos duplicados
  - Optimización de tamaño

### docker-compose-viz

- **Descripción**: Visualiza arquitectura de Docker Compose
- **Instalación**:
  ```bash
  docker run --rm -it --name dcv -v $(pwd):/input pmsipilot/docker-compose-viz render -m image docker-compose.yml
  ```
- **Características**:
  - Genera diagramas de arquitectura
  - Formato PNG/SVG
  - Visualización de dependencias

## 🏗️ Herramientas de Desarrollo

### VS Code Extensions

#### Docker Extension

- **ID**: `ms-azuretools.vscode-docker`
- **Características**:
  - Syntax highlighting para Dockerfiles
  - Comandos Docker integrados
  - IntelliSense para Docker Compose
  - Debug de contenedores

#### Remote - Containers

- **ID**: `ms-vscode-remote.remote-containers`
- **Características**:
  - Desarrollo dentro de contenedores
  - Entornos consistentes
  - Integración completa con VS Code

### Dockerfile Generator

- **URL**: [https://dockerfile-generator.netlify.app/](https://dockerfile-generator.netlify.app/)
- **Descripción**: Generador online de Dockerfiles
- **Características**:
  - Múltiples lenguajes soportados
  - Best practices incluidas
  - Configuración personalizable

## 🔍 Herramientas de Análisis y Debug

### Hadolint

- **Descripción**: Linter para Dockerfiles
- **Instalación**:

  ```bash
  # Como contenedor Docker
  docker run --rm -i hadolint/hadolint < Dockerfile

  # Local
  brew install hadolint  # macOS
  ```

- **Características**:
  - Detecta errores comunes
  - Sugiere mejores prácticas
  - Integración con CI/CD

### Docker Bench Security

- **Descripción**: Script de auditoría de seguridad
- **Instalación**:
  ```bash
  git clone https://github.com/docker/docker-bench-security.git
  cd docker-bench-security
  sudo sh docker-bench-security.sh
  ```
- **Características**:
  - Auditoría completa de seguridad
  - Basado en CIS Benchmark
  - Reportes detallados

### Trivy

- **Descripción**: Escáner de vulnerabilidades
- **Instalación**:
  ```bash
  # Como contenedor
  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image <imagen>
  ```
- **Características**:
  - Escanea vulnerabilidades en imágenes
  - Detecta secrets en código
  - Integración con CI/CD

## 🚀 Herramientas de Deployment

### Watchtower

- **Descripción**: Actualización automática de contenedores
- **Instalación**:
  ```bash
  docker run -d \
    --name watchtower \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower
  ```
- **Características**:
  - Actualiza contenedores automáticamente
  - Monitorea registros de imágenes
  - Notificaciones configurables

### Traefik

- **Descripción**: Proxy reverso y load balancer
- **Características**:
  - Auto-discovery de servicios
  - Configuración automática
  - SSL/TLS automático con Let's Encrypt

### Docker Swarm

- **Descripción**: Orquestador nativo de Docker
- **Comandos básicos**:

  ```bash
  # Inicializar swarm
  docker swarm init

  # Desplegar stack
  docker stack deploy -c docker-compose.yml myapp
  ```

## 📊 Herramientas de Monitoreo

### cAdvisor

- **Descripción**: Monitoreo de contenedores
- **Instalación**:
  ```bash
  docker run \
    --volume=/:/rootfs:ro \
    --volume=/var/run:/var/run:ro \
    --volume=/sys:/sys:ro \
    --volume=/var/lib/docker/:/var/lib/docker:ro \
    --publish=8080:8080 \
    --detach=true \
    --name=cadvisor \
    gcr.io/cadvisor/cadvisor:latest
  ```
- **Características**:
  - Métricas de recursos en tiempo real
  - Interfaz web
  - Integración con Prometheus

### Docker Stats Exporter

- **Descripción**: Exporta métricas para Prometheus
- **Instalación**:
  ```bash
  docker run -d \
    --name docker-stats-exporter \
    -p 9417:9417 \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    sebkl/docker-stats-exporter
  ```

### Grafana Dashboards

- **Docker Dashboard ID**: 893
- **Container Dashboard ID**: 179
- **URL**: [https://grafana.com/grafana/dashboards/](https://grafana.com/grafana/dashboards/)

## 🔐 Herramientas de Seguridad

### Notary

- **Descripción**: Firma digital de imágenes
- **Características**:
  - Verificación de integridad
  - Content trust
  - Cadena de custodia

### Falco

- **Descripción**: Detección de anomalías en runtime
- **Características**:
  - Monitoreo de comportamiento
  - Alertas en tiempo real
  - Integración con Kubernetes

### Anchore Engine

- **Descripción**: Análisis de seguridad de imágenes
- **Características**:
  - Escaneo de vulnerabilidades
  - Políticas de compliance
  - Reportes detallados

## 🎯 Herramientas de Testing

### Container Structure Test

- **Descripción**: Testing de estructura de contenedores
- **Instalación**:
  ```bash
  # Download binary
  curl -LO https://storage.googleapis.com/container-structure-test/latest/container-structure-test-linux-amd64
  chmod +x container-structure-test-linux-amd64
  ```
- **Uso**:
  ```bash
  ./container-structure-test test --image myimage:latest --config config.yaml
  ```

### Goss

- **Descripción**: Testing rápido de infraestructura
- **Características**:
  - Validación de servicios
  - Testing de configuración
  - Integración con Docker

## 🔄 Herramientas de CI/CD

### GitHub Actions - Docker

#### Build and Push Action

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: user/app:latest
```

#### Security Scanning Action

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'user/app:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'
```

### GitLab CI Templates

- **Docker Build Template**: Disponible en GitLab CI/CD templates
- **Security Scanning**: Integrado en GitLab Ultimate

## 🌐 Registros y Repositorios

### Docker Hub Alternatives

#### GitHub Container Registry

```bash
# Login
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin

# Tag and push
docker tag myapp ghcr.io/username/myapp:latest
docker push ghcr.io/username/myapp:latest
```

#### Amazon ECR

```bash
# Login
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com

# Push
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/myapp:latest
```

## 📱 Aplicaciones Móviles

### Docker Mobile Apps

- **Docker Desktop**: Control básico desde móvil
- **Portainer**: App web responsive
- **SSH/Terminal Apps**: Para acceso remoto

## 🛠️ Herramientas de Desarrollo Local

### Docker Compose Overrides

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  app:
    volumes:
      - .:/app
    ports:
      - '8000:8000'
    environment:
      - DEBUG=true
```

### Make Commands

```makefile
# Makefile
.PHONY: build run stop clean

build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker system prune -f
```

## 📋 Scripts Útiles

### Container Health Check

```bash
#!/bin/bash
# health-check.sh
CONTAINER_NAME=$1
STATUS=$(docker inspect --format='{{.State.Health.Status}}' $CONTAINER_NAME)
if [ "$STATUS" = "healthy" ]; then
    echo "✅ $CONTAINER_NAME is healthy"
    exit 0
else
    echo "❌ $CONTAINER_NAME is $STATUS"
    exit 1
fi
```

### Backup Script

```bash
#!/bin/bash
# backup-volumes.sh
VOLUME_NAME=$1
BACKUP_PATH=$2
docker run --rm -v $VOLUME_NAME:/data -v $BACKUP_PATH:/backup alpine tar czf /backup/backup-$(date +%Y%m%d-%H%M%S).tar.gz /data
```

### Container Cleanup

```bash
#!/bin/bash
# cleanup.sh
echo "🧹 Cleaning up Docker system..."
docker container prune -f
docker image prune -f
docker volume prune -f
docker network prune -f
echo "✅ Cleanup completed!"
```

---

## 🎯 Recomendaciones de Uso

### Para Principiantes

1. Empieza con **Docker Desktop** o **Portainer**
2. Usa **VS Code con extensión Docker**
3. Instala **Lazydocker** para terminal

### Para Desarrollo

1. **VS Code Remote Containers**
2. **docker-compose.override.yml**
3. **Hadolint** para linting

### Para Producción

1. **Trivy** para security scanning
2. **cAdvisor + Prometheus + Grafana** para monitoring
3. **Traefik** para load balancing

### Para DevOps

1. **Docker Bench Security**
2. **Watchtower** para actualizaciones
3. **GitHub Actions** para CI/CD

---

**Herramientas actualizadas para la Semana 9 del Bootcamp FastAPI**
