# Práctica 28: GitHub Actions CI/CD

## 📋 Descripción

Implementa pipelines de CI/CD completos usando GitHub Actions para automatizar testing, building, y deployment de aplicaciones FastAPI.

## 🎯 Objetivos Específicos

- ✅ Configurar workflows de GitHub Actions
- ✅ Implementar CI con testing automático
- ✅ Automatizar build y push de imágenes Docker
- ✅ Configurar deployment automático a producción

## ⏱️ Tiempo Estimado: 75 minutos

---

## 📚 Conceptos Clave

### 🔄 **¿Qué es CI/CD?**

**Continuous Integration (CI):**

- Integración automática de cambios
- Testing automático en cada commit
- Detección temprana de errores
- Builds consistentes y reproducibles

**Continuous Deployment (CD):**

- Deployment automático a staging/producción
- Rollback automático en caso de errores
- Versionado automático
- Monitoreo post-deployment

### 🛠️ **GitHub Actions Components**

```yaml
# Estructura básica
name: Nombre del workflow
on: Eventos que lo disparan
jobs: Trabajos a ejecutar
  job-name:
    runs-on: Entorno de ejecución
    steps: Pasos individuales
      - name: Nombre del paso
        uses: Acción a usar
        with: Parámetros
        run: Comandos a ejecutar
```

---

## 🛠️ Desarrollo Práctico

### **Paso 1: Workflow Básico de CI**

Crea el archivo `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'
  POETRY_VERSION: '1.6.1'

jobs:
  test:
    name: Test & Quality Checks
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Cache Poetry
        uses: actions/cache@v3
        with:
          path: ~/.local
          key: poetry-${{ runner.os }}-${{ env.POETRY_VERSION }}

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: ${{ env.POETRY_VERSION }}
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ env.PYTHON_VERSION }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install dependencies
        run: poetry install

      - name: Run linting
        run: |
          poetry run black --check .
          poetry run isort --check-only .
          poetry run flake8 .

      - name: Run type checking
        run: poetry run mypy .

      - name: Run security checks
        run: poetry run bandit -r app/

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: |
          poetry run pytest \
            --cov=app \
            --cov-report=xml \
            --cov-report=html \
            --junitxml=pytest.xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: |
            pytest.xml
            htmlcov/
```

### **Paso 2: Workflow de Build Docker**

Crea `.github/workflows/docker.yml`:

```yaml
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    name: Build & Push Docker Image
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
```

### **Paso 3: Workflow de Deployment**

Crea `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy:
    name: Deploy to ${{ github.event.inputs.environment || 'production' }}
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment || 'production' }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.28.0'

      - name: Configure AWS credentials
        if: env.DEPLOY_TARGET == 'aws'
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Deploy to Kubernetes
        env:
          KUBE_CONFIG: ${{ secrets.KUBE_CONFIG }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          echo "$KUBE_CONFIG" | base64 -d > kubeconfig.yml
          export KUBECONFIG=kubeconfig.yml

          # Actualizar imagen en deployment
          kubectl set image deployment/fastapi-app \
            fastapi-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }}

          # Esperar rollout
          kubectl rollout status deployment/fastapi-app --timeout=300s

      - name: Run smoke tests
        run: |
          # Esperar a que el servicio esté disponible
          sleep 30

          # Health check
          curl -f ${{ secrets.APP_URL }}/health || exit 1

          # API tests básicos
          curl -f ${{ secrets.APP_URL }}/docs || exit 1

      - name: Notify deployment
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#deployments'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### **Paso 4: Workflow de Release**

Crea `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install semantic-release
        run: |
          npm install -g semantic-release
          npm install -g @semantic-release/changelog
          npm install -g @semantic-release/git

      - name: Create release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: semantic-release

      - name: Generate changelog
        id: changelog
        uses: metcalfc/changelog-generator@v4.1.0
        with:
          myToken: ${{ secrets.GITHUB_TOKEN }}

      - name: Create GitHub Release
        if: steps.changelog.outputs.changelog != ''
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ steps.changelog.outputs.tag }}
          release_name: Release ${{ steps.changelog.outputs.tag }}
          body: ${{ steps.changelog.outputs.changelog }}
          draft: false
          prerelease: false
```

### **Paso 5: Configuración de Secrets**

En Settings > Secrets and variables > Actions:

```bash
# Docker/Registry
DOCKER_USERNAME=tu-usuario
DOCKER_PASSWORD=tu-token

# AWS (si usas AWS)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=abc123...
AWS_REGION=us-east-1

# Kubernetes
KUBE_CONFIG=base64-encoded-kubeconfig

# Application
APP_URL=https://mi-app.com
DATABASE_URL=postgresql://...

# Notifications
SLACK_WEBHOOK=https://hooks.slack.com/...
```

---

## 🔨 Ejercicios Prácticos

### **Ejercicio 1: Setup Básico**

```bash
# 1. Crear estructura de directorios
mkdir -p .github/workflows

# 2. Crear workflow básico
cat > .github/workflows/test.yml << 'EOF'
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
EOF

# 3. Commit y push
git add .github/workflows/test.yml
git commit -m "Add basic CI workflow"
git push
```

### **Ejercicio 2: Matrix Testing**

```yaml
# .github/workflows/matrix.yml
name: Matrix Testing

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
        exclude:
          - os: windows-latest
            python-version: '3.9'

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest
```

### **Ejercicio 3: Conditional Deployments**

```yaml
# .github/workflows/conditional.yml
name: Conditional Deploy

on:
  push:
    branches: [main, develop]

jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: echo "Deploying to staging..."

  deploy-production:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: echo "Deploying to production..."
```

---

## 📊 Monitoreo y Análisis

### **Dashboard de Métricas**

```yaml
# .github/workflows/metrics.yml
name: Metrics Collection

on:
  schedule:
    - cron: '0 0 * * *' # Daily at midnight

jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Collect deployment frequency
        run: |
          gh api repos/${{ github.repository }}/deployments \
            --jq '.[] | select(.created_at > "2023-01-01") | .created_at' \
            | wc -l > deployment_frequency.txt

      - name: Collect lead time
        run: |
          # Tiempo promedio entre commit y deployment
          gh api repos/${{ github.repository }}/commits \
            --jq '.[] | .commit.author.date' \
            | head -10 > lead_times.txt

      - name: Upload metrics
        uses: actions/upload-artifact@v3
        with:
          name: metrics
          path: |
            deployment_frequency.txt
            lead_times.txt
```

### **Análisis de Seguridad**

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run CodeQL Analysis
        uses: github/codeql-action/init@v2
        with:
          languages: python

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2

      - name: Run Snyk Security Scan
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

---

## 🎯 Mejores Prácticas

### **📋 Workflow Organization**

1. **Un workflow por propósito**: CI, CD, Security, Release
2. **Nombres descriptivos**: `ci.yml`, `deploy-production.yml`
3. **Documentación inline**: Comentarios en YAML
4. **Reutilización**: Composite actions para lógica común

### **🔧 Performance Optimization**

```yaml
# Optimizaciones comunes
strategy:
  fail-fast: false  # No parar todos los jobs si uno falla
  matrix:
    include:
      - os: ubuntu-latest
        cache-key: ubuntu

# Cache dependencies
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# Parallel jobs cuando sea posible
jobs:
  test:
    # ...
  lint:
    # ...
  security:
    # ...
```

### **🛡️ Seguridad**

```yaml
# Permisos mínimos
permissions:
  contents: read
  packages: write

# Secrets en environment
environment: production
# En lugar de secrets globales

# Validación de inputs
if: github.event.inputs.environment == 'production'
```

---

## ✅ Checklist de Validación

### **🔄 CI Setup**

- [ ] Workflow de CI configurado
- [ ] Tests ejecutándose automáticamente
- [ ] Linting y type checking
- [ ] Coverage reports generados

### **🐳 Docker Integration**

- [ ] Build automático de imágenes
- [ ] Push a registry configurado
- [ ] Vulnerability scanning activo
- [ ] Multi-platform builds (opcional)

### **🚀 Deployment**

- [ ] Deployment automático configurado
- [ ] Environments (staging/production)
- [ ] Rollback capabilities
- [ ] Health checks post-deployment

### **📊 Monitoring**

- [ ] Workflow status visible
- [ ] Notifications configuradas
- [ ] Metrics collection
- [ ] Error alerting

---

## 📚 Recursos Adicionales

### **🔗 Enlaces Útiles**

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Marketplace Actions](https://github.com/marketplace?type=actions)
- [Workflow Syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)

### **🛠️ Herramientas**

- **Act**: Testing workflows locally
- **GitHub CLI**: Workflow management
- **Nektos/act**: Local GitHub Actions
- **Action Lint**: Workflow validation

---

## 🚀 Entregables

1. **Workflows completos** (CI, CD, Security)
2. **Configuración de secrets** y environments
3. **Documentation** de procesos
4. **Monitoring setup** básico

## ⏭️ Próximos Pasos

En la siguiente práctica configuraremos **entornos de producción** y **variables de entorno** para deployment seguro.
