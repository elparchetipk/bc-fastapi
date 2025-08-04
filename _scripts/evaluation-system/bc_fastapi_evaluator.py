#!/usr/bin/env python3
"""
Script de evaluación para el bootcamp bc-fastapi
Analiza código del estudiante y genera reporte de evaluación
"""

import os
import json
import re
import sys
from pathlib import Path
from datetime import datetime

def analyze_student_code():
    """Analiza el código del estudiante"""
    analysis = {
        "files_analyzed": [],
        "total_lines": 0,
        "functions_count": 0,
        "classes_count": 0,
        "fastapi_usage": False,
        "endpoints_found": [],
        "test_files": [],
        "imports": [],
        "syntax_errors": []
    }
    
    student_path = Path('student-repo')
    if not student_path.exists():
        print("⚠️ Directorio student-repo no encontrado")
        return analysis
    
    print(f"🔍 Analizando código en {student_path}")
    
    for py_file in student_path.rglob('*.py'):
        if '.git' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_rel_path = str(py_file.relative_to(student_path))
            analysis["files_analyzed"].append(file_rel_path)
            
            # Cuenta líneas no vacías
            lines = [l for l in content.splitlines() if l.strip()]
            analysis["total_lines"] += len(lines)
            
            # Detecta FastAPI
            if 'fastapi' in content.lower() or 'FastAPI' in content:
                analysis["fastapi_usage"] = True
            
            # Busca endpoints
            patterns = [
                r'@app\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
                r'@router\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    method = match.group(1).upper()
                    path = match.group(2)
                    endpoint = f"{method} {path}"
                    if endpoint not in analysis["endpoints_found"]:
                        analysis["endpoints_found"].append(endpoint)
            
            # Cuenta funciones y clases
            analysis["functions_count"] += len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
            analysis["classes_count"] += len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
            
            # Detecta tests
            if 'test' in py_file.name.lower() or py_file.name.startswith('test_'):
                analysis["test_files"].append(file_rel_path)
            
            # Extrae imports principales
            import_lines = re.findall(r'^(?:from\s+\S+\s+)?import\s+.+', content, re.MULTILINE)
            analysis["imports"].extend(import_lines[:5])  # Primeros 5 imports
                
        except Exception as e:
            analysis["syntax_errors"].append(f"{py_file.name}: {str(e)}")
    
    print(f"✅ Análisis completado: {len(analysis['files_analyzed'])} archivos")
    return analysis

def calculate_score(analysis, week_number):
    """Calcula puntuación basada en criterios del bootcamp"""
    score = 0
    feedback = []
    improvements = []
    
    # Criterio 1: Entrega de archivos (20 pts)
    files_count = len(analysis['files_analyzed'])
    if files_count > 0:
        score += 20
        feedback.append(f"✅ {files_count} archivos Python entregados")
    else:
        improvements.append("❌ No se encontraron archivos Python")
    
    # Criterio 2: Uso de FastAPI (30 pts)
    if analysis['fastapi_usage']:
        score += 30
        feedback.append("✅ FastAPI implementado correctamente")
    else:
        improvements.append("⚠️ FastAPI no detectado - Verificar importaciones")
    
    # Criterio 3: Endpoints (25 pts)
    endpoints_count = len(analysis['endpoints_found'])
    expected_endpoints = max(2, min(5, int(week_number)))  # 2-5 según semana
    
    if endpoints_count >= expected_endpoints:
        score += 25
        feedback.append(f"✅ {endpoints_count} endpoints implementados")
    elif endpoints_count > 0:
        partial_score = int(25 * (endpoints_count / expected_endpoints))
        score += partial_score
        feedback.append(f"⚠️ {endpoints_count} endpoints (esperados: {expected_endpoints})")
        improvements.append(f"Implementar {expected_endpoints - endpoints_count} endpoints adicionales")
    else:
        improvements.append("❌ No se encontraron endpoints")
    
    # Criterio 4: Calidad del código (25 pts)
    total_lines = analysis['total_lines']
    expected_lines = max(30, int(week_number) * 15)  # Expectativa crece con semana
    
    if total_lines >= expected_lines:
        score += 25
        feedback.append("✅ Código bien desarrollado")
    elif total_lines >= expected_lines * 0.7:
        score += 20
        feedback.append("✅ Implementación básica completa")
    elif total_lines >= expected_lines * 0.4:
        score += 15
        feedback.append("⚠️ Implementación mínima")
        improvements.append(f"Expandir código (actual: {total_lines}, esperado: ~{expected_lines} líneas)")
    else:
        score += 5
        improvements.append(f"❌ Código insuficiente ({total_lines} líneas)")
    
    # Bonus por buenas prácticas
    if analysis['functions_count'] >= 3:
        score += 5
        feedback.append("✅ Buena modularización con funciones")
    
    if analysis['test_files']:
        score += 5
        feedback.append(f"✅ Tests implementados ({len(analysis['test_files'])} archivos)")
    
    # Limita score a 100
    score = min(score, 100)
    
    # Determina categoría
    if score >= 90:
        category = "Excelente"
        emoji = "🏆"
    elif score >= 80:
        category = "Satisfactorio" 
        emoji = "✅"
    elif score >= 70:
        category = "Necesita Mejora"
        emoji = "⚠️"
    else:
        category = "Insuficiente"
        emoji = "❌"
    
    return score, category, emoji, feedback, improvements

def generate_report(student_name, week_number, analysis, score, category, emoji, feedback, improvements):
    """Genera el reporte markdown de evaluación"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Encabezado
    report = f"""# 🎯 Evaluación Automática bc-fastapi

**Estudiante:** {student_name}  
**Semana:** {week_number}  
**Fecha:** {timestamp}  

---

## {emoji} Calificación: {score}/100 puntos ({category})

"""
    
    # Fortalezas
    if feedback:
        report += "### ✅ Fortalezas Identificadas:\n"
        for point in feedback:
            report += f"- {point}\n"
        report += "\n"
    
    # Mejoras
    if improvements:
        report += "### 🎯 Áreas de Mejora:\n"
        for improvement in improvements:
            report += f"- {improvement}\n"
        report += "\n"
    
    # Análisis técnico
    report += f"""### 📊 Análisis Técnico:
- **Archivos analizados:** {len(analysis['files_analyzed'])}
- **Líneas de código:** {analysis['total_lines']}
- **Funciones encontradas:** {analysis['functions_count']}
- **Clases encontradas:** {analysis['classes_count']}
- **FastAPI detectado:** {'✅ Sí' if analysis['fastapi_usage'] else '❌ No'}
- **Endpoints implementados:** {len(analysis['endpoints_found'])}

"""
    
    # Detalles de endpoints
    if analysis['endpoints_found']:
        report += "#### Endpoints encontrados:\n"
        for endpoint in analysis['endpoints_found']:
            report += f"- `{endpoint}`\n"
        report += "\n"
    
    # Archivos de test
    if analysis['test_files']:
        report += f"#### Archivos de test encontrados:\n"
        for test_file in analysis['test_files']:
            report += f"- `{test_file}`\n"
        report += "\n"
    
    # Errores de sintaxis
    if analysis['syntax_errors']:
        report += "#### ⚠️ Errores detectados:\n"
        for error in analysis['syntax_errors'][:3]:  # Máximo 3 errores
            report += f"- {error}\n"
        report += "\n"
    
    # Próximos pasos
    next_week = int(week_number) + 1
    if next_week <= 11:
        report += f"""### 📚 Próximos Pasos para Semana {next_week}:
- Revisa el material de la semana {next_week} en el repositorio principal
- Implementa las mejoras sugeridas según el feedback
- Practica con los ejercicios adicionales si están disponibles
- Participa en las discusiones del bootcamp para resolver dudas

"""
    else:
        report += """### 🎓 ¡Bootcamp Completado!
- Revisa el feedback final de tu proyecto
- Prepara tu portafolio con todos los proyectos desarrollados
- ¡Felicidades por completar el bootcamp bc-fastapi!
- Considera obtener certificaciones adicionales en FastAPI

"""
    
    # Recursos
    report += f"""### 📞 Recursos de Apoyo:
- **Repositorio principal:** https://github.com/elparchetipk/bc-fastapi
- **Material de la semana:** `/semana-{int(week_number):02d}/`
- **Documentación:** `/_docs/`
- **Guías de apoyo:** `/_docs/guides/`
- **Instructor:** Erick Granados Torres
- **Institución:** SENA - CGMLTI Regional Distrito Capital

### 💡 Consejos Generales:
- Mantén tu código organizado y bien comentado
- Usa nombres descriptivos para variables y funciones
- Implementa manejo de errores en tus endpoints
- Agrega documentación automática con FastAPI
- Practica testing para mejorar la calidad del código

---

## 🤖 Información de la Evaluación

- **Sistema:** bc-fastapi Evaluation System v2.0
- **Algoritmo:** Análisis estático + Validación de patrones FastAPI
- **Criterios evaluados:** Entrega, FastAPI, Endpoints, Calidad del código
- **Generado:** {timestamp}

---

*Sistema desarrollado específicamente para el bootcamp bc-fastapi*  
*SENA - Centro de Gestión de Mercados, Logística y TI*  
*Regional Distrito Capital*
"""
    
    return report

def generate_no_code_report(student_name, week_number):
    """Genera reporte cuando no se encuentra código"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""# ⚠️ Sin código para evaluar

**Estudiante:** {student_name}  
**Semana:** {week_number}  
**Fecha:** {timestamp}

## Problema Detectado

No se encontraron archivos Python (.py) en tu repositorio para evaluar.

### 🔍 Verifica lo siguiente:

1. **✅ Archivos con extensión .py**
   - Tu código debe estar en archivos con extensión .py
   - Evita usar .txt o otros formatos

2. **✅ Ubicación correcta**
   - Los archivos deben estar en la raíz o carpetas del repositorio
   - No dentro de carpetas ocultas o especiales

3. **✅ Rama correcta**
   - Asegúrate de hacer push a la rama correcta
   - El Pull Request debe apuntar a la rama principal

4. **✅ Permisos del repositorio**
   - El repositorio debe ser público o tener permisos de acceso
   - Verifica que el webhook funcione correctamente

### 🚀 Pasos para corregir:

1. **Crear archivo Python básico:**
```python
# main.py - Ejemplo básico para semana {week_number}
from fastapi import FastAPI

app = FastAPI(title="Mi API - Semana {week_number}")

@app.get("/")
def read_root():
    return {{"message": "¡Hola desde FastAPI!"}}

@app.get("/estudiante")
def get_estudiante():
    return {{"nombre": "{student_name}", "semana": {week_number}}}
```

2. **Hacer commit y push:**
```bash
git add main.py
git commit -m"Agregar código base semana {week_number}"
git push origin semana-{week_number}-entrega
```

3. **Verificar el Pull Request**
   - Confirma que el PR se creó correctamente
   - Revisa que los archivos aparezcan en GitHub

### 📞 Obtener Ayuda:

- **Repositorio principal:** https://github.com/elparchetipk/bc-fastapi
- **Material de referencia:** `/semana-{int(week_number):02d}/`
- **Documentación de ayuda:** `/_docs/setup/`
- **Issues del repositorio:** Para consultas técnicas específicas

### 📋 Próxima evaluación:

Una vez corrijas estos puntos, el sistema volverá a evaluar automáticamente tu código cuando:
- Hagas un nuevo push a tu rama
- Se ejecute manualmente la evaluación
- Se active el webhook configurado

---

🤖 *Evaluación automática bc-fastapi - Sistema de detección de problemas*  
📅 *Generado: {timestamp}*  
🏫 *SENA - CGMLTI Regional Distrito Capital*
"""

def main():
    """Función principal del evaluador"""
    # Obtiene parámetros del entorno
    student_name = os.getenv('STUDENT_NAME', 'Estudiante')
    week_number = os.getenv('WEEK_NUMBER', '1')
    
    print(f"🚀 bc-fastapi Evaluator v2.0")
    print(f"👤 Evaluando: {student_name}")
    print(f"📅 Semana: {week_number}")
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Analiza código del estudiante
    analysis = analyze_student_code()
    
    if len(analysis['files_analyzed']) == 0:
        print("⚠️ No se encontró código Python para evaluar")
        report = generate_no_code_report(student_name, week_number)
        
        # Datos básicos para JSON
        analysis['evaluation_score'] = 0
        analysis['evaluation_category'] = 'Sin Código'
        analysis['has_code'] = False
    else:
        print(f"📊 Código encontrado: {len(analysis['files_analyzed'])} archivos")
        
        # Calcula puntuación
        score, category, emoji, feedback, improvements = calculate_score(analysis, int(week_number))
        
        # Genera reporte
        report = generate_report(student_name, week_number, analysis, score, category, emoji, feedback, improvements)
        
        print(f"✅ Evaluación completada: {score}/100 ({category})")
        
        # Agrega datos de evaluación al análisis
        analysis['evaluation_score'] = score
        analysis['evaluation_category'] = category
        analysis['has_code'] = True
    
    # Guarda reporte markdown
    try:
        with open('evaluation_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print("💾 Reporte guardado: evaluation_report.md")
    except Exception as e:
        print(f"❌ Error guardando reporte: {e}")
        return 1
    
    # Guarda análisis en JSON
    try:
        analysis['timestamp'] = datetime.now().isoformat()
        analysis['student_name'] = student_name
        analysis['week_number'] = int(week_number)
        
        with open('analysis_result.json', 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print("💾 Análisis guardado: analysis_result.json")
    except Exception as e:
        print(f"❌ Error guardando análisis: {e}")
        return 1
    
    print("=" * 50)
    print("🎯 Evaluación completada exitosamente")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
