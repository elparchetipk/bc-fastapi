# Recursos Adicionales - Semana 11

## 📚 Referencias Técnicas

### 🛠️ Documentación Oficial

#### Backend - FastAPI y Python

- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Documentación completa de FastAPI
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/) - ORM y Core
- [Pydantic V2 Documentation](https://docs.pydantic.dev/2.5/) - Validación de datos
- [Alembic Documentation](https://alembic.sqlalchemy.org/) - Migraciones de base de datos
- [Pytest Documentation](https://docs.pytest.org/) - Framework de testing
- [Redis Python Documentation](https://redis-py.readthedocs.io/) - Cliente Redis

#### Frontend - React y TypeScript

- [React Documentation](https://react.dev/) - Documentación oficial de React
- [TypeScript Handbook](https://www.typescriptlang.org/docs/) - Guía completa de TypeScript
- [Tailwind CSS Documentation](https://tailwindcss.com/docs) - Framework CSS
- [React Router Documentation](https://reactrouter.com/) - Enrutamiento SPA
- [Axios Documentation](https://axios-http.com/docs/intro) - Cliente HTTP
- [Vite Documentation](https://vitejs.dev/guide/) - Build tool moderno

#### DevOps y Deployment

- [Docker Documentation](https://docs.docker.com/) - Containerización
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Orquestación
- [nginx Documentation](https://nginx.org/en/docs/) - Servidor web
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - CI/CD
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Base de datos

### 📖 Libros y Guías Recomendadas

#### Desarrollo Web Full-Stack

- "Building Modern Web Applications with FastAPI" - Practical guide
- "Learning React" - Alex Banks & Eve Porcello
- "TypeScript in 50 Lessons" - Stefan Baumgartner
- "Effective Python" - Brett Slatkin
- "Clean Code" - Robert C. Martin

#### Arquitectura y Patrones

- "Clean Architecture" - Robert C. Martin
- "Building Microservices" - Sam Newman
- "Patterns of Enterprise Application Architecture" - Martin Fowler
- "Domain-Driven Design" - Eric Evans

#### DevOps y Deployment

- "Docker Deep Dive" - Nigel Poulton
- "The DevOps Handbook" - Gene Kim et al.
- "Site Reliability Engineering" - Google

## 🎯 Cheatsheets y Referencias Rápidas

### FastAPI Quick Reference

#### Dependencias y Autenticación

```python
# Dependency injection
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validar token
    return user

@app.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"user": user}

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/data")
@limiter.limit("10/minute")
async def get_data(request: Request):
    return {"data": "limited"}
```

#### WebSockets

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

#### Background Tasks

```python
from fastapi import BackgroundTasks

def send_notification(email: str, message: str):
    # Enviar email en background
    pass

@app.post("/send-notification/")
async def create_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_notification, email, "Welcome!")
    return {"message": "Notification sent"}
```

### React + TypeScript Quick Reference

#### Hooks Básicos

```typescript
import { useState, useEffect, useContext } from 'react';

// State Hook
const [count, setCount] = useState<number>(0);

// Effect Hook
useEffect(() => {
  // Side effect
  return () => {
    // Cleanup
  };
}, [dependency]);

// Custom Hook
function useAPI<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading };
}
```

#### Componentes con TypeScript

```typescript
interface Props {
  title: string;
  children?: React.ReactNode;
  onClick?: () => void;
}

const Button: React.FC<Props> = ({ title, children, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
      {title}
      {children}
    </button>
  );
};

export default Button;
```

#### Manejo de Formularios

```typescript
import { useForm } from 'react-hook-form';

interface FormData {
  email: string;
  password: string;
}

const LoginForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>();

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('email', { required: 'Email is required' })}
        type="email"
        placeholder="Email"
      />
      {errors.email && <span>{errors.email.message}</span>}

      <input
        {...register('password', { required: 'Password is required' })}
        type="password"
        placeholder="Password"
      />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  );
};
```

### Docker Quick Reference

#### Dockerfile para FastAPI

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Dockerfile para React

```dockerfile
# Build stage
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

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - '3000:80'
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'

volumes:
  postgres_data:
```

## 💡 Tips de Presentación

### 🎤 Estructura de Presentación Exitosa

#### Slide 1-2: Introducción

- **Título del proyecto** y tu nombre
- **Problema que resuelve** (1 frase)
- **Demo en 30 segundos** (overview rápido)

#### Slide 3-5: Arquitectura Técnica

- **Diagrama de arquitectura** simple
- **Stack tecnológico** con logos
- **Decisiones técnicas** clave (2-3 máximo)

#### Slide 6-12: Demo en Vivo

- **Usuario flow completo** (registro → login → usar app)
- **Funcionalidades principales** (3-4 máximo)
- **Código destacado** (1-2 snippets importantes)

#### Slide 13-15: Desafíos y Aprendizajes

- **Mayor desafío técnico** y cómo lo resolviste
- **Tecnología nueva** que aprendiste
- **Próximos pasos** si tuvieras más tiempo

### 🎥 Tips para Demo en Vivo

#### Preparación

- **Ensaya 3+ veces** el demo completo
- **Ten datos de prueba** listos
- **Backup plan**: video grabado como alternativa
- **Browser limpio**: tabs cerrados, zoom apropiado

#### Durante el Demo

- **Narra mientras haces**: explica cada acción
- **Muestra errores handled**: validaciones, 404s, etc.
- **Destaca features técnicas**: real-time, validaciones, etc.
- **Mantén ritmo**: no te quedes en una pantalla más de 30s

#### Si algo falla

- **Mantén la calma**: "Esta es una buena oportunidad para mostrar..."
- **Cambia al backup**: video o screenshots
- **Explica qué haría**: "Aquí normalmente veríamos..."

### 📊 Consejos de Presentación

#### Comunicación Efectiva

- **Habla claro y pausado**: especialmente términos técnicos
- **Usa ejemplos concretos**: "Como pueden ver aquí..."
- **Interactúa con audiencia**: "¿Alguien ha usado...?"
- **Mantén contacto visual**: no leas slides

#### Manejo del Tiempo

- **15 min total**: 2 intro + 8 demo + 3 técnico + 2 cierre
- **Practica con timer**: sé realista con los tiempos
- **Ten backup slides**: por si vas rápido
- **Prioriza demo**: mejor demo corto que explicación larga

#### Manejo de Preguntas

- **Escucha completamente** antes de responder
- **Si no sabes algo**: "No implementé eso, pero investigaría..."
- **Redirige técnicas complejas**: "Sería interesante explorar..."
- **Agradece las preguntas**: "Excelente pregunta..."

## 🎨 Ejemplos de Portfolio

### 🌟 Proyecto Destacado en GitHub

#### README que Impresiona

````markdown
# 🚀 NombreDelProyecto

> Una breve descripción que venda el proyecto en una línea

![Demo GIF](assets/demo.gif)

## ✨ Features Principales

- 🔐 **Autenticación JWT** con roles y permisos
- ⚡ **Real-time updates** con WebSockets
- 🎨 **UI/UX moderno** con Tailwind CSS
- 🧪 **Testing completo** (coverage >85%)
- 🐳 **Docker ready** para deployment

## 🛠️ Tech Stack

**Backend:** FastAPI • SQLAlchemy • PostgreSQL • Redis  
**Frontend:** React • TypeScript • Tailwind CSS  
**DevOps:** Docker • nginx • GitHub Actions

## 🚀 Quick Start

\```bash

# Clone and run with Docker

git clone https://github.com/user/project
cd project
docker-compose up -d

# Open http://localhost:3000

\```

## 📸 Screenshots

| Dashboard                          | User Profile                   | Real-time Chat           |
| ---------------------------------- | ------------------------------ | ------------------------ |
| ![Dashboard](assets/dashboard.png) | ![Profile](assets/profile.png) | ![Chat](assets/chat.png) |

## 🏗️ Architecture

![Architecture Diagram](assets/architecture.png)

## 📖 API Documentation

Interactive docs available at `/docs` when running locally.

### Key Endpoints

\```
POST /auth/login # User authentication
GET /users/me # Current user profile
POST /items # Create new item
GET /ws # WebSocket connection
\```

## 🧪 Testing

\```bash

# Backend tests

cd backend && pytest --cov=app

# Frontend tests

cd frontend && npm test
\```

## 🚀 Deployment

Deployed on: [Heroku/Railway/DigitalOcean]  
Live demo: [https://project-demo.com](https://project-demo.com)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Tu Nombre**

- GitHub: [@tu-username](https://github.com/tu-username)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)
- Email: tu.email@ejemplo.com

---

⭐ Star this repo if you found it helpful!
````

### 📱 Portfolio Personal

#### Sección de Proyectos

```html
<section class="projects">
  <div class="project-card featured">
    <img
      src="project1-demo.gif"
      alt="Proyecto 1 Demo" />
    <div class="project-info">
      <h3>Sistema de Gestión FastAPI</h3>
      <p>
        Aplicación full-stack con React + FastAPI para gestión de inventario
      </p>
      <div class="tech-stack">
        <span>FastAPI</span>
        <span>React</span>
        <span>PostgreSQL</span>
        <span>Docker</span>
      </div>
      <div class="project-links">
        <a
          href="https://github.com/user/proyecto"
          target="_blank"
          >GitHub</a
        >
        <a
          href="https://proyecto-demo.com"
          target="_blank"
          >Live Demo</a
        >
      </div>
    </div>
  </div>
</section>
```

#### Métricas que Impresionan

- **Código limpio**: "90%+ cobertura de tests"
- **Performance**: "< 200ms response time"
- **UX**: "Mobile-first responsive design"
- **DevOps**: "Automated CI/CD pipeline"
- **Security**: "JWT auth + rate limiting"

## 📞 Recursos de Soporte

### 🆘 Troubleshooting Común

#### Backend Issues

```bash
# Database connection errors
docker-compose down
docker-compose up -d db
docker-compose logs db

# Migration issues
alembic stamp head
alembic revision --autogenerate -m "fix"
alembic upgrade head

# Permission errors
sudo chown -R $USER:$USER .
chmod +x scripts/*.sh
```

#### Frontend Issues

```bash
# Node modules issues
rm -rf node_modules package-lock.json
npm install

# Build issues
npm run clean
npm run build

# Port conflicts
netstat -nlp | grep :3000
kill -9 <PID>
```

#### Docker Issues

```bash
# Clean up Docker
docker system prune -a
docker-compose down -v
docker-compose up --build

# Check logs
docker-compose logs backend
docker-compose logs frontend
```

### 🎓 Canales de Ayuda

#### Durante el Desarrollo

- **Slack del bootcamp**: #semana-11-proyectos
- **Sesiones de mentoría**: Martes y Jueves 16-18h
- **GitHub Issues**: Plantillas de bugs/features
- **Documentation**: Wiki del repositorio

#### Para la Presentación

- **Ensayos grupales**: Lunes 15-17h
- **Feedback peers**: Intercambio de reviews
- **Tech talk practice**: Miércoles 14-15h

### 📚 Recursos Extra

#### Inspiración de Proyectos

- [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi)
- [React Projects](https://github.com/sahandghavidel/React-Projects)
- [Full Stack Open](https://fullstackopen.com/)

#### Tools Útiles

- [JWT.io](https://jwt.io/) - Debug JWT tokens
- [Swagger Editor](https://editor.swagger.io/) - API design
- [Excalidraw](https://excalidraw.com/) - Diagramas
- [Carbon](https://carbon.now.sh/) - Code screenshots
- [Shields.io](https://shields.io/) - README badges

---

**¡Éxito con tu proyecto final! 🚀**

_Recuerda: Un gran proyecto + una gran presentación = oportunidades increíbles_
