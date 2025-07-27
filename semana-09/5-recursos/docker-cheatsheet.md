# Docker Cheatsheet - Semana 9

## 🚀 Comandos Básicos de Docker

### Gestión de Imágenes

```bash
# Descargar imagen
docker pull <imagen>:<tag>

# Listar imágenes locales
docker images
docker image ls

# Eliminar imagen
docker rmi <imagen>:<tag>
docker rmi <image_id>

# Eliminar imágenes no utilizadas
docker image prune

# Ver información detallada de una imagen
docker inspect <imagen>:<tag>

# Construir imagen desde Dockerfile
docker build -t <nombre>:<tag> .
docker build -t <nombre>:<tag> -f <dockerfile> <contexto>

# Guardar imagen a archivo
docker save -o imagen.tar <imagen>:<tag>

# Cargar imagen desde archivo
docker load -i imagen.tar
```

### Gestión de Contenedores

```bash
# Ejecutar contenedor
docker run <imagen>
docker run -d <imagen>                    # en background
docker run -it <imagen> /bin/bash        # interactivo
docker run -p 8000:8000 <imagen>         # mapear puertos
docker run -v $(pwd):/app <imagen>       # montar volumen
docker run --name <nombre> <imagen>      # asignar nombre

# Listar contenedores
docker ps                                # ejecutándose
docker ps -a                            # todos (incluidos parados)

# Parar contenedor
docker stop <container_id>
docker stop <container_name>

# Iniciar contenedor parado
docker start <container_id>

# Reiniciar contenedor
docker restart <container_id>

# Eliminar contenedor
docker rm <container_id>
docker rm -f <container_id>             # forzar eliminación

# Eliminar todos los contenedores parados
docker container prune

# Acceder a contenedor en ejecución
docker exec -it <container_id> /bin/bash
docker exec -it <container_id> sh

# Ver logs del contenedor
docker logs <container_id>
docker logs -f <container_id>           # seguimiento en tiempo real

# Ver estadísticas de recursos
docker stats
docker stats <container_id>

# Inspeccionar contenedor
docker inspect <container_id>
```

### Gestión de Volúmenes

```bash
# Crear volumen
docker volume create <nombre_volumen>

# Listar volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect <nombre_volumen>

# Eliminar volumen
docker volume rm <nombre_volumen>

# Eliminar volúmenes no utilizados
docker volume prune

# Usar volumen en contenedor
docker run -v <nombre_volumen>:/app/data <imagen>

# Bind mount (montar directorio host)
docker run -v /ruta/host:/ruta/contenedor <imagen>
docker run -v $(pwd):/app <imagen>      # directorio actual
```

### Gestión de Redes

```bash
# Listar redes
docker network ls

# Crear red
docker network create <nombre_red>
docker network create --driver bridge <nombre_red>

# Inspeccionar red
docker network inspect <nombre_red>

# Conectar contenedor a red
docker network connect <nombre_red> <container_id>

# Desconectar contenedor de red
docker network disconnect <nombre_red> <container_id>

# Eliminar red
docker network rm <nombre_red>

# Eliminar redes no utilizadas
docker network prune
```

## 🐳 Docker Compose

### Comandos Básicos

```bash
# Levantar servicios
docker-compose up
docker-compose up -d                     # en background
docker-compose up --build               # reconstruir imágenes

# Parar servicios
docker-compose down
docker-compose down -v                   # eliminar volúmenes también

# Ver servicios en ejecución
docker-compose ps

# Ver logs
docker-compose logs
docker-compose logs <servicio>
docker-compose logs -f <servicio>       # seguimiento

# Ejecutar comando en servicio
docker-compose exec <servicio> /bin/bash
docker-compose exec <servicio> <comando>

# Escalar servicios
docker-compose up --scale <servicio>=3

# Reconstruir servicios
docker-compose build
docker-compose build <servicio>

# Parar servicio específico
docker-compose stop <servicio>

# Reiniciar servicio específico
docker-compose restart <servicio>

# Eliminar servicios parados
docker-compose rm
```

### Archivo docker-compose.yml Básico

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
    volumes:
      - .:/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: dbname
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - '5432:5432'

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'

volumes:
  postgres_data:

networks:
  default:
    driver: bridge
```

## 📦 Dockerfile Patterns

### Dockerfile FastAPI Básico

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile Optimizado (Multi-stage)

```dockerfile
# Build stage
FROM python:3.13-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.13-slim

RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Variables de Entorno

### En docker run

```bash
# Pasar variable individual
docker run -e VARIABLE=valor <imagen>

# Pasar archivo de variables
docker run --env-file .env <imagen>

# Variables múltiples
docker run -e VAR1=val1 -e VAR2=val2 <imagen>
```

### En docker-compose.yml

```yaml
services:
  app:
    image: mi-app
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql://localhost/db
    env_file:
      - .env
      - .env.production
```

## 🧹 Limpieza del Sistema

```bash
# Eliminar containers, networks, images y build cache
docker system prune

# Eliminar todo (incluyendo volúmenes)
docker system prune -a --volumes

# Ver uso de espacio
docker system df

# Eliminar imágenes no utilizadas
docker image prune

# Eliminar contenedores parados
docker container prune

# Eliminar volúmenes no utilizados
docker volume prune

# Eliminar redes no utilizadas
docker network prune
```

## 🔍 Debugging y Troubleshooting

```bash
# Ver procesos dentro del contenedor
docker exec <container> ps aux

# Ver uso de recursos en tiempo real
docker stats <container>

# Inspeccionar cambios en el filesystem
docker diff <container>

# Copiar archivos desde/hacia contenedor
docker cp <container>:/path/file.txt ./file.txt
docker cp ./file.txt <container>:/path/

# Ver información del daemon Docker
docker info

# Ver eventos en tiempo real
docker events

# Verificar conectividad de red
docker exec <container> ping <otro_container>
docker exec <container> nslookup <servicio>
```

## 🏷️ Tags y Registry

```bash
# Etiquetar imagen
docker tag <imagen_local> <usuario>/<repo>:<tag>

# Subir imagen a registry
docker push <usuario>/<repo>:<tag>

# Descargar imagen específica
docker pull <usuario>/<repo>:<tag>

# Login en registry
docker login
docker login <registry_url>

# Logout
docker logout
```

## 🔒 Seguridad

```bash
# Ejecutar como usuario no-root
docker run -u 1000:1000 <imagen>

# Solo lectura
docker run --read-only <imagen>

# Limitar recursos
docker run --memory="256m" --cpus="1.5" <imagen>

# Escanear vulnerabilidades (si tienes docker scan)
docker scan <imagen>

# Verificar imagen firmada
docker trust inspect <imagen>
```

## 📊 Monitoring

```bash
# Exportar métricas
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Ver logs con timestamps
docker logs --timestamps <container>

# Filtrar logs por fecha
docker logs --since 2023-01-01T10:00:00 <container>

# Healthcheck manual
docker exec <container> curl -f http://localhost:8000/health
```

## ⚡ Tips y Trucos

### Aliases Útiles

```bash
# Agregar a ~/.bashrc o ~/.zshrc
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias drmi='docker rmi'
alias dexec='docker exec -it'
alias dlogs='docker logs -f'
alias dclean='docker system prune -f'

# Docker Compose aliases
alias dc='docker-compose'
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'
alias dcps='docker-compose ps'
alias dclogs='docker-compose logs -f'
```

### Scripts Útiles

```bash
#!/bin/bash
# stop_all_containers.sh
docker stop $(docker ps -q)

#!/bin/bash
# remove_dangling_images.sh
docker rmi $(docker images -f "dangling=true" -q)

#!/bin/bash
# backup_volume.sh
docker run --rm -v $1:/data -v $(pwd):/backup alpine tar czf /backup/$1.tar.gz /data
```

---

## 🚨 Comandos de Emergencia

```bash
# Parar todos los contenedores
docker stop $(docker ps -q)

# Eliminar todos los contenedores
docker rm $(docker ps -a -q)

# Eliminar todas las imágenes
docker rmi $(docker images -q)

# Reset completo de Docker
docker system prune -a --volumes --force
```

---

_Cheatsheet actualizado para la Semana 9 del Bootcamp FastAPI_
