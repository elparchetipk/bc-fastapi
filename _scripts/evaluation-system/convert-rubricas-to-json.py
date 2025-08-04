# evaluation-system/scripts/convert-rubricas-to-json.py
"""
Convierte las rúbricas existentes del bootcamp bc-fastapi a formato JSON
procesable por el sistema de evaluación automática.

Este script preserva toda la riqueza pedagógica de las rúbricas existentes
mientras las hace procesables por IA.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any
import yaml

class RubricConverter:
    """Conversor de rúbricas markdown a JSON estructurado"""
    
    def __init__(self, bootcamp_path: str):
        self.bootcamp_path = Path(bootcamp_path)
        self.output_path = self.bootcamp_path / "evaluation-system" / "rubrics"
        
        # Asegura que existe el directorio de salida
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    def extract_rubric_from_markdown(self, md_file: Path) -> Dict[str, Any]:
        """Extrae información de rúbrica desde archivo markdown"""
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extrae información básica de la semana
        week_match = re.search(r'semana[- ](\d+)', md_file.parent.name, re.IGNORECASE)
        week_number = int(week_match.group(1)) if week_match else 0
        
        # Extrae título de la rúbrica
        title_match = re.search(r'# (.+)', content)
        title = title_match.group(1) if title_match else f"Semana {week_number}"
        
        # Estructura base de la rúbrica
        rubric = {
            "week_number": week_number,
            "title": title,
            "total_points": 100,
            "evaluation_components": {},
            "grading_scale": {
                "excelente": {"range": "90-100", "description": "Supera expectativas"},
                "satisfactorio": {"range": "80-89", "description": "Cumple requisitos completamente"},
                "necesita_mejora": {"range": "70-79", "description": "Cumple parcialmente"},
                "insuficiente": {"range": "0-69", "description": "No cumple requisitos mínimos"}
            },
            "specific_requirements": {},
            "evaluation_prompts": [],
            "automated_checks": []
        }
        
        # Extrae componentes de evaluación
        components = self._extract_evaluation_components(content)
        if components:
            rubric["evaluation_components"] = components
            
        # Extrae requisitos específicos
        requirements = self._extract_specific_requirements(content, week_number)
        if requirements:
            rubric["specific_requirements"] = requirements
            
        # Extrae checks automatizables
        automated_checks = self._extract_automated_checks(content, week_number)
        if automated_checks:
            rubric["automated_checks"] = automated_checks
            
        # Genera prompts de evaluación específicos
        prompts = self._generate_evaluation_prompts(content, week_number)
        if prompts:
            rubric["evaluation_prompts"] = prompts
            
        return rubric
    
    def _extract_evaluation_components(self, content: str) -> Dict[str, Any]:
        """Extrae componentes de evaluación con sus pesos"""
        components = {}
        
        # Patrones para encontrar distribución de puntos
        patterns = [
            r'\*\*(.+?)\*\*.*?(\d+)%.*?(\d+)\s*pts?',  # **Componente** 25% 25 pts
            r'\|\s*(.+?)\s*\|\s*(\d+)%\s*\|\s*(\d+)\s*pts?',  # | Componente | 25% | 25 pts |
            r'(\w+(?:\s+\w+)*)\s*\((\d+)%.*?(\d+)\s*puntos?\)',  # Componente (25% - 25 puntos)
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                component_name = match.group(1).strip()
                weight = int(match.group(2))
                points = int(match.group(3))
                
                # Limpia el nombre del componente
                component_name = re.sub(r'[^\w\s]', '', component_name).strip()
                component_key = component_name.lower().replace(' ', '_')
                
                components[component_key] = {
                    "name": component_name,
                    "weight": weight,
                    "points": points,
                    "description": self._extract_component_description(content, component_name)
                }
        
        return components
    
    def _extract_component_description(self, content: str, component_name: str) -> str:
        """Extrae descripción de un componente específico"""
        # Busca la descripción cerca del nombre del componente
        pattern = rf'{re.escape(component_name)}.*?[:\-]\s*(.+?)(?:\n|$)'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def _extract_specific_requirements(self, content: str, week_number: int) -> Dict[str, Any]:
        """Extrae requisitos específicos de la semana"""
        requirements = {}
        
        # Mapeo de requisitos comunes por semana basado en el bootcamp
        week_requirements_map = {
            1: {
                "fastapi_setup": {
                    "description": "Configuración inicial de FastAPI",
                    "criteria": [
                        "FastAPI correctamente importado",
                        "Aplicación inicializada con FastAPI()",
                        "Primer endpoint GET funcional",
                        "Documentación automática accesible"
                    ]
                },
                "environment_setup": {
                    "description": "Configuración del entorno de desarrollo",
                    "criteria": [
                        "Entorno virtual creado",
                        "requirements.txt presente",
                        "Estructura de proyecto apropiada"
                    ]
                }
            },
            3: {
                "pydantic_models": {
                    "description": "Implementación de modelos Pydantic",
                    "criteria": [
                        "Al menos 2 modelos Pydantic definidos",
                        "Validaciones implementadas",
                        "Request/Response models usados"
                    ]
                }
            },
            8: {
                "testing_suite": {
                    "description": "Suite de testing completa",
                    "criteria": [
                        "Test coverage >90% en endpoints principales",
                        "Tests unitarios implementados",
                        "Tests de integración funcionales",
                        "Fixtures apropiadas"
                    ]
                }
            }
        }
        
        # Usa mapeo específico si existe, sino extrae del contenido
        if week_number in week_requirements_map:
            requirements = week_requirements_map[week_number]
        
        # También extrae requisitos del contenido markdown
        checklist_pattern = r'- \[ \] (.+)'
        checklist_items = re.findall(checklist_pattern, content)
        
        if checklist_items:
            requirements["checklist_items"] = {
                "description": "Elementos obligatorios del checklist",
                "criteria": checklist_items
            }
        
        return requirements
    
    def _extract_automated_checks(self, content: str, week_number: int) -> List[Dict[str, Any]]:
        """Extrae checks que pueden ser automatizados"""
        checks = []
        
        # Checks básicos que siempre se pueden automatizar
        basic_checks = [
            {
                "type": "file_exists",
                "target": "main.py",
                "description": "Verifica que existe archivo principal",
                "weight": 5
            },
            {
                "type": "syntax_check",
                "target": "*.py",
                "description": "Verifica sintaxis Python correcta",
                "weight": 10
            },
            {
                "type": "imports_check",
                "target": "fastapi",
                "description": "Verifica importación de FastAPI",
                "weight": 5
            }
        ]
        
        # Checks específicos por semana
        week_specific_checks = {
            1: [
                {
                    "type": "fastapi_app_creation",
                    "pattern": r"app\s*=\s*FastAPI\(",
                    "description": "Verifica creación de app FastAPI",
                    "weight": 15
                }
            ],
            3: [
                {
                    "type": "pydantic_models",
                    "pattern": r"class\s+\w+\s*\(\s*BaseModel\s*\):",
                    "description": "Verifica definición de modelos Pydantic",
                    "weight": 20
                }
            ],
            8: [
                {
                    "type": "test_coverage",
                    "command": "pytest --cov=src/",
                    "threshold": 80,
                    "description": "Verifica cobertura de tests",
                    "weight": 25
                }
            ]
        }
        
        checks.extend(basic_checks)
        
        if week_number in week_specific_checks:
            checks.extend(week_specific_checks[week_number])
        
        return checks
    
    def _generate_evaluation_prompts(self, content: str, week_number: int) -> List[str]:
        """Genera prompts específicos para evaluación con IA"""
        
        base_prompt = f"""Eres un instructor senior de FastAPI evaluando una entrega de la semana {week_number} del bootcamp bc-fastapi.

CONTEXTO DEL BOOTCAMP:
- Bootcamp de 11 semanas de FastAPI con enfoque en calidad total
- Cada semana tiene 6 horas exactas de contenido estructurado
- Énfasis en mejores prácticas y desarrollo profesional
- Estudiantes son Tecnólogos en Desarrollo de Software (III trimestre)

OBJETIVOS SEMANA {week_number}:"""

        # Extrae objetivos del contenido si están disponibles
        objectives_pattern = r'objetivos?[:\-]\s*(.+?)(?:\n\n|\n#|$)'
        objectives_match = re.search(objectives_pattern, content, re.IGNORECASE | re.DOTALL)
        
        if objectives_match:
            objectives_text = objectives_match.group(1).strip()
            base_prompt += f"\n{objectives_text}"
        
        prompts = [
            base_prompt + """

INSTRUCCIONES DE EVALUACIÓN:
1. Analiza el código entregado contra los criterios específicos de esta semana
2. Proporciona feedback constructivo y específico en español
3. Mantén un tono motivador pero profesional
4. Enfócate en el crecimiento del estudiante
5. Sugiere próximos pasos concretos

FORMATO DE RESPUESTA:
Usa el formato de rúbrica existente del bootcamp, adaptándolo con ejemplos específicos del código analizado."""
        ]
        
        return prompts
    
    def convert_all_rubrics(self) -> Dict[str, str]:
        """Convierte todas las rúbricas encontradas en el bootcamp"""
        converted_files = {}
        
        # Busca archivos de rúbricas en cada semana
        for week_dir in self.bootcamp_path.glob("semana-*"):
            if week_dir.is_dir():
                # Busca archivo de rúbrica
                rubric_files = list(week_dir.glob("*RUBRICA*.md")) + list(week_dir.glob("*rubrica*.md"))
                
                if rubric_files:
                    rubric_file = rubric_files[0]  # Toma el primero si hay varios
                    
                    try:
                        # Convierte la rúbrica
                        rubric_data = self.extract_rubric_from_markdown(rubric_file)
                        
                        # Guarda como JSON
                        week_number = rubric_data["week_number"]
                        output_file = self.output_path / f"week-{week_number:02d}.json"
                        
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(rubric_data, f, indent=2, ensure_ascii=False)
                        
                        converted_files[str(week_dir)] = str(output_file)
                        print(f"✅ Convertida rúbrica de {week_dir.name} -> {output_file.name}")
                        
                    except Exception as e:
                        print(f"❌ Error convirtiendo {rubric_file}: {e}")
                else:
                    print(f"⚠️ No se encontró rúbrica en {week_dir.name}")
        
        # Crea rúbrica global combinada
        self._create_global_rubric()
        
        return converted_files
    
    def _create_global_rubric(self):
        """Crea una rúbrica global que combina elementos comunes"""
        global_rubric = {
            "bootcamp_info": {
                "name": "Bootcamp bc-fastapi",
                "duration_weeks": 11,
                "weekly_hours": 6,
                "target_audience": "Tecnólogos en Desarrollo de Software (III trimestre)"
            },
            "global_criteria": {
                "functionality": {
                    "weight": 40,
                    "description": "Código funciona correctamente según especificaciones"
                },
                "code_quality": {
                    "weight": 30,
                    "description": "Aplicación de mejores prácticas y estándares"
                },
                "documentation": {
                    "weight": 15,
                    "description": "README, comentarios y claridad del código"
                },
                "professionalism": {
                    "weight": 15,
                    "description": "Git workflow, entrega y presentación"
                }
            },
            "grading_philosophy": {
                "approach": "Constructivo y orientado al crecimiento",
                "language": "Español, tono profesional pero motivador",
                "focus": "Feedback específico con ejemplos de mejora"
            },
            "automated_evaluation_config": {
                "ai_model": "codellama:7b-instruct",
                "max_tokens": 1500,
                "temperature": 0.3,
                "evaluation_timeout_minutes": 15
            }
        }
        
        output_file = self.output_path / "global-rubric.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(global_rubric, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Creada rúbrica global: {output_file.name}")

def main():
    """Función principal del conversor"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Convierte rúbricas bc-fastapi a JSON")
    parser.add_argument("bootcamp_path", help="Ruta al directorio del bootcamp bc-fastapi")
    parser.add_argument("--output", help="Directorio de salida personalizado")
    
    args = parser.parse_args()
    
    print("🚀 Iniciando conversión de rúbricas bc-fastapi...")
    print(f"📂 Directorio bootcamp: {args.bootcamp_path}")
    
    converter = RubricConverter(args.bootcamp_path)
    
    if args.output:
        converter.output_path = Path(args.output)
        converter.output_path.mkdir(parents=True, exist_ok=True)
    
    converted = converter.convert_all_rubrics()
    
    print(f"\n📊 Conversión completada:")
    print(f"   📁 Archivos convertidos: {len(converted)}")
    print(f"   📍 Directorio salida: {converter.output_path}")
    print(f"   📋 Archivos JSON generados:")
    
    for json_file in converter.output_path.glob("*.json"):
        print(f"      • {json_file.name}")
    
    print("\n✅ Rúbricas listas para sistema de evaluación automática!")

if __name__ == "__main__":
    main()