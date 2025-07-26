# Práctica 30: Estrategias de Deployment

## 📋 Descripción

Domina las estrategias avanzadas de deployment para aplicaciones FastAPI, incluyendo blue-green deployments, rolling updates, canary releases y rollback automático.

## 🎯 Objetivos Específicos

- ✅ Implementar blue-green deployment
- ✅ Configurar rolling updates
- ✅ Ejecutar canary releases
- ✅ Gestionar rollbacks automáticos

## ⏱️ Tiempo Estimado: 75 minutos

---

## 📚 Conceptos Clave

### 🚀 **Estrategias de Deployment**

**Blue-Green Deployment:**

- Dos ambientes idénticos (Blue/Green)
- Cambio instantáneo de tráfico
- Rollback rápido y seguro
- Requiere doble infraestructura

**Rolling Update:**

- Actualización gradual de instancias
- Mantenimiento de disponibilidad
- Menor uso de recursos
- Control granular del proceso

**Canary Release:**

- Deployment a subset de usuarios
- Validación en producción real
- Mitigación de riesgos
- Feedback temprano

### 🏗️ **Componentes Críticos**

```yaml
# Elementos clave
Load Balancer: Distribución de tráfico
Health Checks: Validación de instancias
Monitoring: Observabilidad en tiempo real
Rollback Plan: Estrategia de reversa
```

---

## 🛠️ Desarrollo Práctico

### **Paso 1: Blue-Green Deployment**

Configuración de infrastructure as code:

```yaml
# terraform/blue-green.tf
variable "environment_color" {
  description = "Blue or Green environment"
  type        = string
  default     = "blue"
}

# Blue Environment
resource "aws_ecs_service" "fastapi_blue" {
  count           = var.environment_color == "blue" ? 1 : 0
  name            = "fastapi-blue"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.fastapi.arn
  desired_count   = 3

  load_balancer {
    target_group_arn = aws_lb_target_group.blue.arn
    container_name   = "fastapi"
    container_port   = 8000
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }
}

# Green Environment
resource "aws_ecs_service" "fastapi_green" {
  count           = var.environment_color == "green" ? 1 : 0
  name            = "fastapi-green"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.fastapi.arn
  desired_count   = 3

  load_balancer {
    target_group_arn = aws_lb_target_group.green.arn
    container_name   = "fastapi"
    container_port   = 8000
  }
}

# Load Balancer
resource "aws_lb" "main" {
  name               = "fastapi-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb.id]
  subnets           = var.public_subnets

  enable_deletion_protection = false
}

# Target Groups
resource "aws_lb_target_group" "blue" {
  name     = "fastapi-blue-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
}

resource "aws_lb_target_group" "green" {
  name     = "fastapi-green-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
}

# Listener
resource "aws_lb_listener" "main" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = var.environment_color == "blue" ? aws_lb_target_group.blue.arn : aws_lb_target_group.green.arn
  }
}
```

### **Paso 2: Script de Blue-Green Deployment**

```bash
#!/bin/bash
# scripts/blue-green-deploy.sh

set -e

CURRENT_COLOR=${1:-blue}
NEW_COLOR=${2:-green}
APP_VERSION=${3:-latest}
HEALTH_CHECK_URL=${4:-http://localhost/health}

echo "🚀 Starting Blue-Green Deployment"
echo "Current: $CURRENT_COLOR -> New: $NEW_COLOR"
echo "Version: $APP_VERSION"

# Función para verificar salud del servicio
check_health() {
    local url=$1
    local max_attempts=30
    local attempt=1

    echo "🔍 Checking health at $url"

    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null; then
            echo "✅ Health check passed"
            return 0
        fi
        echo "⏳ Attempt $attempt/$max_attempts failed, retrying..."
        sleep 10
        ((attempt++))
    done

    echo "❌ Health check failed after $max_attempts attempts"
    return 1
}

# Función para deployar nueva versión
deploy_new_version() {
    echo "📦 Deploying $APP_VERSION to $NEW_COLOR environment"

    # Actualizar task definition
    aws ecs update-service \
        --cluster fastapi-cluster \
        --service "fastapi-$NEW_COLOR" \
        --task-definition "fastapi:$APP_VERSION" \
        --desired-count 3

    # Esperar que el deployment complete
    echo "⏳ Waiting for deployment to complete..."
    aws ecs wait services-stable \
        --cluster fastapi-cluster \
        --services "fastapi-$NEW_COLOR"

    echo "✅ Deployment completed"
}

# Función para cambiar tráfico
switch_traffic() {
    echo "🔄 Switching traffic to $NEW_COLOR environment"

    # Obtener ARN del target group
    NEW_TG_ARN=$(aws elbv2 describe-target-groups \
        --names "fastapi-$NEW_COLOR-tg" \
        --query 'TargetGroups[0].TargetGroupArn' \
        --output text)

    # Obtener ARN del listener
    LB_ARN=$(aws elbv2 describe-load-balancers \
        --names "fastapi-lb" \
        --query 'LoadBalancers[0].LoadBalancerArn' \
        --output text)

    LISTENER_ARN=$(aws elbv2 describe-listeners \
        --load-balancer-arn "$LB_ARN" \
        --query 'Listeners[0].ListenerArn' \
        --output text)

    # Modificar listener para apuntar al nuevo target group
    aws elbv2 modify-listener \
        --listener-arn "$LISTENER_ARN" \
        --default-actions Type=forward,TargetGroupArn="$NEW_TG_ARN"

    echo "✅ Traffic switched successfully"
}

# Función para rollback
rollback() {
    echo "🔙 Rolling back to $CURRENT_COLOR environment"

    CURRENT_TG_ARN=$(aws elbv2 describe-target-groups \
        --names "fastapi-$CURRENT_COLOR-tg" \
        --query 'TargetGroups[0].TargetGroupArn' \
        --output text)

    LB_ARN=$(aws elbv2 describe-load-balancers \
        --names "fastapi-lb" \
        --query 'LoadBalancers[0].LoadBalancerArn' \
        --output text)

    LISTENER_ARN=$(aws elbv2 describe-listeners \
        --load-balancer-arn "$LB_ARN" \
        --query 'Listeners[0].ListenerArn' \
        --output text)

    aws elbv2 modify-listener \
        --listener-arn "$LISTENER_ARN" \
        --default-actions Type=forward,TargetGroupArn="$CURRENT_TG_ARN"

    echo "✅ Rollback completed"
}

# Función principal
main() {
    # 1. Deploy nueva versión
    deploy_new_version

    # 2. Verificar salud del nuevo environment
    NEW_HEALTH_URL=$(echo $HEALTH_CHECK_URL | sed "s/$CURRENT_COLOR/$NEW_COLOR/")
    if ! check_health "$NEW_HEALTH_URL"; then
        echo "❌ New environment is unhealthy, aborting deployment"
        exit 1
    fi

    # 3. Cambiar tráfico
    switch_traffic

    # 4. Verificar que el nuevo environment maneja tráfico correctamente
    sleep 30
    if ! check_health "$HEALTH_CHECK_URL"; then
        echo "❌ New environment failed under load, rolling back"
        rollback
        exit 1
    fi

    # 5. Cleanup del environment anterior
    echo "🧹 Scaling down $CURRENT_COLOR environment"
    aws ecs update-service \
        --cluster fastapi-cluster \
        --service "fastapi-$CURRENT_COLOR" \
        --desired-count 0

    echo "🎉 Blue-Green deployment completed successfully!"
    echo "Active environment: $NEW_COLOR"
}

# Trap para rollback en caso de error
trap 'echo "❌ Deployment failed, attempting rollback..."; rollback' ERR

# Ejecutar deployment
main
```

### **Paso 3: Rolling Update con Kubernetes**

```yaml
# k8s/rolling-update.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  labels:
    app: fastapi
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 25% # Máximo 25% de pods down
      maxSurge: 25% # Máximo 25% de pods extra
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8000'
        prometheus.io/path: '/metrics'
    spec:
      containers:
        - name: fastapi
          image: mi-fastapi-app:v1.2.0
          ports:
            - containerPort: 8000
              name: http
          resources:
            requests:
              memory: '256Mi'
              cpu: '250m'
            limits:
              memory: '512Mi'
              cpu: '500m'
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 2
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: fastapi-secrets
                  key: database-url
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: fastapi-secrets
                  key: redis-url
      terminationGracePeriodSeconds: 30

---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi
  ports:
    - name: http
      port: 80
      targetPort: 8000
  type: LoadBalancer

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fastapi-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'
spec:
  tls:
    - hosts:
        - api.miapp.com
      secretName: fastapi-tls
  rules:
    - host: api.miapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: fastapi-service
                port:
                  number: 80
```

### **Paso 4: Canary Release**

```yaml
# k8s/canary-release.yaml
# Deployment principal (90% tráfico)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-stable
  labels:
    app: fastapi
    version: stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: fastapi
      version: stable
  template:
    metadata:
      labels:
        app: fastapi
        version: stable
    spec:
      containers:
        - name: fastapi
          image: mi-fastapi-app:v1.1.0
          ports:
            - containerPort: 8000

---
# Deployment canary (10% tráfico)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-canary
  labels:
    app: fastapi
    version: canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
      version: canary
  template:
    metadata:
      labels:
        app: fastapi
        version: canary
    spec:
      containers:
        - name: fastapi
          image: mi-fastapi-app:v1.2.0 # Nueva versión
          ports:
            - containerPort: 8000

---
# Service que balancea entre stable y canary
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi # Selecciona ambos deployments
  ports:
    - port: 80
      targetPort: 8000
```

### **Paso 5: Script de Canary Release Automatizado**

```python
#!/usr/bin/env python3
# scripts/canary_release.py

import subprocess
import time
import sys
import json
import requests
from typing import Dict, List

class CanaryReleaseManager:
    """Gestor de canary releases automatizado."""

    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self.stable_deployment = "fastapi-stable"
        self.canary_deployment = "fastapi-canary"
        self.service_name = "fastapi-service"

    def deploy_canary(self, image: str, canary_percentage: int = 10):
        """Deployar versión canary."""
        print(f"🚀 Deploying canary version: {image}")

        # Calcular replicas
        total_replicas = self.get_total_replicas()
        canary_replicas = max(1, int(total_replicas * canary_percentage / 100))
        stable_replicas = total_replicas - canary_replicas

        print(f"📊 Traffic split: {100-canary_percentage}% stable, {canary_percentage}% canary")
        print(f"🔢 Replicas: {stable_replicas} stable, {canary_replicas} canary")

        # Actualizar deployments
        self.update_deployment(self.canary_deployment, image, canary_replicas)
        self.update_deployment(self.stable_deployment, None, stable_replicas)

        # Esperar que los pods estén listos
        self.wait_for_rollout(self.canary_deployment)

    def get_total_replicas(self) -> int:
        """Obtener número total de replicas."""
        cmd = f"kubectl get deployment {self.stable_deployment} -n {self.namespace} -o jsonpath='{{.spec.replicas}}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return int(result.stdout.strip()) if result.stdout.strip() else 10

    def update_deployment(self, deployment: str, image: str = None, replicas: int = None):
        """Actualizar deployment."""
        if replicas is not None:
            cmd = f"kubectl scale deployment {deployment} --replicas={replicas} -n {self.namespace}"
            subprocess.run(cmd, shell=True, check=True)

        if image:
            cmd = f"kubectl set image deployment/{deployment} fastapi={image} -n {self.namespace}"
            subprocess.run(cmd, shell=True, check=True)

    def wait_for_rollout(self, deployment: str):
        """Esperar que el rollout complete."""
        print(f"⏳ Waiting for {deployment} rollout...")
        cmd = f"kubectl rollout status deployment/{deployment} -n {self.namespace} --timeout=300s"
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {deployment} rollout completed")

    def monitor_metrics(self, duration_minutes: int = 10) -> Dict:
        """Monitorear métricas durante el canary."""
        print(f"📊 Monitoring metrics for {duration_minutes} minutes...")

        metrics = {
            "error_rate": [],
            "response_time": [],
            "total_requests": 0
        }

        for minute in range(duration_minutes):
            print(f"📈 Minute {minute + 1}/{duration_minutes}")

            # Aquí integrarías con tu sistema de métricas (Prometheus, etc.)
            # Por simplicidad, usamos requests directos
            error_rate = self.check_error_rate()
            response_time = self.check_response_time()

            metrics["error_rate"].append(error_rate)
            metrics["response_time"].append(response_time)
            metrics["total_requests"] += 100  # Ejemplo

            print(f"   Error rate: {error_rate}%")
            print(f"   Avg response time: {response_time}ms")

            time.sleep(60)  # Esperar 1 minuto

        return metrics

    def check_error_rate(self) -> float:
        """Verificar tasa de errores."""
        try:
            # Ejemplo con endpoint de métricas
            response = requests.get("http://your-app.com/metrics", timeout=5)
            # Parsear métricas de Prometheus o similar
            return 0.5  # Ejemplo: 0.5% error rate
        except:
            return 100.0  # Si no podemos conectar, asumir 100% error

    def check_response_time(self) -> float:
        """Verificar tiempo de respuesta."""
        try:
            start_time = time.time()
            response = requests.get("http://your-app.com/health", timeout=5)
            end_time = time.time()
            return (end_time - start_time) * 1000  # En millisegundos
        except:
            return 5000.0  # 5 segundos si hay error

    def analyze_metrics(self, metrics: Dict) -> bool:
        """Analizar métricas para decidir si promover o rollback."""
        avg_error_rate = sum(metrics["error_rate"]) / len(metrics["error_rate"])
        avg_response_time = sum(metrics["response_time"]) / len(metrics["response_time"])

        print(f"📊 Metrics Analysis:")
        print(f"   Average error rate: {avg_error_rate:.2f}%")
        print(f"   Average response time: {avg_response_time:.2f}ms")
        print(f"   Total requests: {metrics['total_requests']}")

        # Criterios de éxito
        success_criteria = [
            avg_error_rate < 1.0,  # Menos del 1% de errores
            avg_response_time < 2000,  # Menos de 2 segundos
            metrics["total_requests"] > 500  # Suficientes requests para validar
        ]

        return all(success_criteria)

    def promote_canary(self):
        """Promover canary a producción."""
        print("🎉 Promoting canary to production...")

        # Obtener imagen de canary
        cmd = f"kubectl get deployment {self.canary_deployment} -n {self.namespace} -o jsonpath='{{.spec.template.spec.containers[0].image}}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        canary_image = result.stdout.strip()

        # Actualizar stable deployment
        self.update_deployment(self.stable_deployment, canary_image, self.get_total_replicas())
        self.wait_for_rollout(self.stable_deployment)

        # Escalar canary a 0
        self.update_deployment(self.canary_deployment, None, 0)

        print("✅ Canary promoted successfully!")

    def rollback_canary(self):
        """Rollback del canary."""
        print("🔙 Rolling back canary...")

        # Escalar canary a 0
        self.update_deployment(self.canary_deployment, None, 0)

        # Restaurar stable deployment a todas las replicas
        self.update_deployment(self.stable_deployment, None, self.get_total_replicas())

        print("✅ Canary rolled back successfully!")

def main():
    """Función principal."""
    if len(sys.argv) < 3:
        print("Usage: python canary_release.py <image> <canary_percentage>")
        sys.exit(1)

    image = sys.argv[1]
    canary_percentage = int(sys.argv[2])

    manager = CanaryReleaseManager()

    try:
        # 1. Deploy canary
        manager.deploy_canary(image, canary_percentage)

        # 2. Monitor metrics
        metrics = manager.monitor_metrics(10)  # 10 minutos

        # 3. Analyze and decide
        if manager.analyze_metrics(metrics):
            manager.promote_canary()
        else:
            manager.rollback_canary()
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error during canary release: {e}")
        manager.rollback_canary()
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 🔨 Ejercicios Prácticos

### **Ejercicio 1: Simular Blue-Green Local**

```bash
# Usar Docker Compose para simular blue-green
# docker-compose.blue-green.yml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-blue.conf:/etc/nginx/nginx.conf
    depends_on:
      - blue-app

  blue-app:
    image: mi-fastapi-app:v1.0
    environment:
      - COLOR=blue
    deploy:
      replicas: 3

  green-app:
    image: mi-fastapi-app:v1.1
    environment:
      - COLOR=green
    deploy:
      replicas: 3

# Script para cambiar configuración
switch_to_green() {
    cp nginx-green.conf nginx.conf
    docker-compose restart nginx
}
```

### **Ejercicio 2: Rolling Update Manual**

```bash
#!/bin/bash
# Simular rolling update manual

TOTAL_INSTANCES=6
NEW_IMAGE="mi-fastapi-app:v1.2"

for i in $(seq 1 $TOTAL_INSTANCES); do
    echo "Updating instance $i/$TOTAL_INSTANCES"

    # Parar instancia antigua
    docker stop "fastapi-$i" || true
    docker rm "fastapi-$i" || true

    # Iniciar nueva instancia
    docker run -d --name "fastapi-$i" \
        -p $((8000 + i)):8000 \
        $NEW_IMAGE

    # Verificar que está saludable
    sleep 10
    curl -f "http://localhost:$((8000 + i))/health" || {
        echo "Instance $i failed health check"
        exit 1
    }

    echo "Instance $i updated successfully"
    sleep 5  # Pausa entre actualizaciones
done

echo "Rolling update completed!"
```

### **Ejercicio 3: Feature Flags para Canary**

```python
# app/core/feature_flags.py
import os
import random
from typing import Dict, Any

class FeatureFlags:
    """Sistema de feature flags para canary releases."""

    def __init__(self):
        self.flags = {
            "new_algorithm": {
                "enabled": os.getenv("FEATURE_NEW_ALGORITHM", "false").lower() == "true",
                "rollout_percentage": int(os.getenv("NEW_ALGORITHM_ROLLOUT", "0"))
            },
            "enhanced_ui": {
                "enabled": os.getenv("FEATURE_ENHANCED_UI", "false").lower() == "true",
                "rollout_percentage": int(os.getenv("ENHANCED_UI_ROLLOUT", "0"))
            }
        }

    def is_enabled(self, flag_name: str, user_id: str = None) -> bool:
        """Verificar si un feature flag está habilitado para un usuario."""
        if flag_name not in self.flags:
            return False

        flag = self.flags[flag_name]

        if not flag["enabled"]:
            return False

        # Si no hay rollout percentage, está habilitado para todos
        if flag["rollout_percentage"] >= 100:
            return True

        if flag["rollout_percentage"] <= 0:
            return False

        # Usar hash del user_id para determinismo
        if user_id:
            user_hash = hash(user_id) % 100
            return user_hash < flag["rollout_percentage"]

        # Fallback a random para usuarios anónimos
        return random.randint(1, 100) <= flag["rollout_percentage"]

# Uso en endpoints
from fastapi import Request, Depends

feature_flags = FeatureFlags()

@app.get("/api/data")
async def get_data(request: Request):
    user_id = request.headers.get("X-User-ID")

    if feature_flags.is_enabled("new_algorithm", user_id):
        return new_algorithm_response()
    else:
        return legacy_algorithm_response()
```

---

## 🎯 Mejores Prácticas

### **📋 Deployment Strategy Selection**

1. **Blue-Green**: Para cambios críticos con rollback rápido
2. **Rolling Update**: Para actualizaciones graduales sin downtime
3. **Canary**: Para validación de features con usuarios reales
4. **Feature Flags**: Para control granular de features

### **🔧 Automation Best Practices**

```bash
# Pipeline de deployment automatizado
stages:
  - validate      # Tests, linting, security
  - build         # Build imagen, push registry
  - deploy-canary # Deploy 5% canary
  - monitor       # Monitor por 10 minutos
  - promote       # Promote o rollback basado en métricas
  - cleanup       # Cleanup recursos antiguos
```

### **🛡️ Safety Measures**

```yaml
# Health checks robustos
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2

# Resource limits
resources:
  requests:
    memory: '256Mi'
    cpu: '250m'
  limits:
    memory: '512Mi'
    cpu: '500m'
```

---

## ✅ Checklist de Validación

### **🚀 Blue-Green Setup**

- [ ] Dos ambientes idénticos configurados
- [ ] Load balancer con switch automático
- [ ] Health checks funcionando
- [ ] Rollback plan documentado

### **🔄 Rolling Update**

- [ ] Strategy configurada apropiadamente
- [ ] maxUnavailable y maxSurge definidos
- [ ] Readiness probes configurados
- [ ] Monitoring durante rollout

### **🐦 Canary Release**

- [ ] Traffic splitting configurado
- [ ] Métricas de monitoreo definidas
- [ ] Criterios de éxito establecidos
- [ ] Rollback automático implementado

### **📊 Monitoring**

- [ ] Métricas de deployment disponibles
- [ ] Alertas configuradas
- [ ] Logs centralizados
- [ ] Dashboard de observabilidad

---

## 📚 Recursos Adicionales

### **🔗 Enlaces Útiles**

- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [AWS Blue/Green Deployments](https://docs.aws.amazon.com/whitepapers/latest/blue-green-deployments/welcome.html)
- [Canary Releases](https://martinfowler.com/bliki/CanaryRelease.html)

### **🛠️ Herramientas**

- **Argo Rollouts**: Advanced deployment strategies
- **Flagger**: Progressive delivery operator
- **Istio**: Service mesh with traffic management
- **Jenkins X**: GitOps with preview environments

---

## 🚀 Entregables

1. **Blue-green deployment** configurado y testado
2. **Rolling update strategy** implementada
3. **Canary release pipeline** automatizado
4. **Monitoring y alerting** para deployments

## ⏭️ Próximos Pasos

Con estas estrategias de deployment dominas el arte de llevar aplicaciones a producción de manera segura y eficiente. El siguiente nivel incluye advanced topics como **service mesh**, **chaos engineering**, y **multi-region deployments**.
