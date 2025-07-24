#!/bin/bash

# Datos de las semanas del bootcamp
declare -A semanas=(
    ["02"]="FastAPI Fundamentals|Pydantic, Swagger, Validation|Task Manager API"
    ["03"]="Base de Datos y ORM|SQLAlchemy, Alembic, PostgreSQL|Task Manager con Persistencia"
    ["04"]="Docker y Containerización|Docker, Docker Compose|Task Manager Containerizado"
    ["05"]="Autenticación y Autorización|JWT, OAuth2, Security|Task Manager con Autenticación"
    ["06"]="Testing y Quality Assurance|pytest, SonarQube, Coverage|Test Suite Completo"
    ["07"]="Optimización y Performance|Caching, Monitoring, Redis|Task Manager Optimizado"
    ["08"]="Frontend Integration|React, Vite, CORS|Frontend para Task Manager"
    ["09"]="Microservices Architecture|Service Communication, API Gateway|Task Manager como Microservicios"
    ["10"]="DevOps y CI/CD|GitHub Actions, Deployment|Pipeline Completo"
    ["11"]="Proyecto Final - Desarrollo|E-Commerce API Platform|MVP funcional"
    ["12"]="Proyecto Final - Presentación|Evaluación y Cierre|Proyecto completo"
)

# Crear .gitkeep para cada semana
for semana in "${!semanas[@]}"; do
    IFS='|' read -r tema tecnologias proyecto <<< "${semanas[$semana]}"
    
    cat > "semana-$semana/.gitkeep" << EOF
# Semana $semana - $tema

## Objetivos de la Semana
Desarrollo de competencias en $tema aplicando mejores prácticas de desarrollo.

## Estructura
- \`teoria/\` - Material teórico y conceptos fundamentales
- \`practica/\` - Ejercicios prácticos guiados paso a paso
- \`ejercicios/\` - Ejercicios individuales para resolver
- \`proyecto/\` - $proyecto
- \`recursos/\` - Recursos adicionales, referencias y enlaces

## Tecnologías Principales
$tecnologias

## Entregables
- Código funcional siguiendo convenciones
- Tests implementados y pasando
- Documentación actualizada
- README específico del proyecto de semana

## Criterios de Evaluación
- Funcionamiento correcto (70%)
- Calidad del código y mejores prácticas (20%)
- Documentación y presentación (10%)
EOF
done
