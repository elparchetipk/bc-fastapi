# Rúbrica de Evaluación - Semana 6: Testing y Calidad

⏰ **Evaluación de 6 horas de trabajo**  
🎯 **Enfoque en testing práctico y aplicable**  
📊 **Puntuación total: 100 puntos**

---

## 📊 Distribución de Puntuación

| Componente                  | Peso | Puntos | Descripción                   |
| --------------------------- | ---- | ------ | ----------------------------- |
| **Setup y Configuración**   | 15%  | 15 pts | Ambiente de testing completo  |
| **Tests de Autenticación**  | 25%  | 25 pts | Testing de sistema de auth    |
| **Tests de Endpoints CRUD** | 25%  | 25 pts | Testing de funcionalidad core |
| **Coverage y Calidad**      | 20%  | 20 pts | Cobertura y organización      |
| **Integración y E2E**       | 15%  | 15 pts | Tests de flujos completos     |

**Total: 100 puntos**

---

## 🎯 Criterios Detallados de Evaluación

### **1. Setup y Configuración (15 puntos)**

#### **Excelente (13-15 puntos)**

- ✅ **pytest** instalado y configurado correctamente
- ✅ **pytest.ini** con configuraciones avanzadas (marcadores, coverage, etc.)
- ✅ **.coveragerc** configurado con exclusiones apropiadas
- ✅ **Estructura tests/** bien organizada (fixtures, helpers, etc.)
- ✅ **conftest.py** con fixtures base reutilizables
- ✅ **requirements-dev.txt** completo con todas las dependencias
- ✅ **Scripts de automatización** (run_tests.sh o similar)

#### **Bueno (10-12 puntos)**

- ✅ pytest instalado y funcionando
- ✅ pytest.ini básico presente
- ✅ .coveragerc configurado
- ✅ Estructura tests/ organizada
- ✅ conftest.py con fixtures básicas
- ⚠️ requirements-dev.txt presente pero básico

#### **Suficiente (7-9 puntos)**

- ✅ pytest funcionando
- ⚠️ Configuración mínima
- ⚠️ Estructura básica de tests
- ⚠️ Fixtures básicas presentes
- ❌ Falta documentación o scripts

#### **Insuficiente (0-6 puntos)**

- ❌ Setup incompleto o no funcional
- ❌ Configuración ausente o incorrecta
- ❌ Estructura desorganizada

---

### **2. Tests de Autenticación (25 puntos)**

#### **Excelente (22-25 puntos)**

- ✅ **Tests de registro** (exitoso, email duplicado, validaciones)
- ✅ **Tests de login** (credenciales válidas/inválidas, casos edge)
- ✅ **Tests de JWT** (generación, verificación, expiración)
- ✅ **Tests de autorización** (endpoints protegidos, roles)
- ✅ **Fixtures para auth** (usuarios, tokens, headers)
- ✅ **Parametrización** para múltiples casos
- ✅ **Tests de seguridad** (aislamiento, permisos)
- ✅ **Manejo de errores** auth apropiado

#### **Bueno (18-21 puntos)**

- ✅ Tests básicos de registro y login
- ✅ Tests de JWT funcionando
- ✅ Tests de endpoints protegidos
- ✅ Fixtures de auth básicas
- ⚠️ Algunos casos edge faltantes
- ⚠️ Parametrización limitada

#### **Suficiente (14-17 puntos)**

- ✅ Tests mínimos de auth funcionando
- ⚠️ Coverage básico de login/registro
- ⚠️ Fixtures simples
- ❌ Faltan casos de error importantes

#### **Insuficiente (0-13 puntos)**

- ❌ Tests de auth incompletos o no funcionan
- ❌ Fixtures ausentes o incorrectas
- ❌ No cubre casos críticos

---

### **3. Tests de Endpoints CRUD (25 puntos)**

#### **Excelente (22-25 puntos)**

- ✅ **Tests CREATE** (éxito, validaciones, auth requerida)
- ✅ **Tests READ** (por ID, listas, paginación, filtros)
- ✅ **Tests UPDATE** (actualización completa/parcial, permisos)
- ✅ **Tests DELETE** (eliminación exitosa, verificación)
- ✅ **Tests de validación** (campos requeridos, límites)
- ✅ **Tests de autorización** (solo propietario puede modificar)
- ✅ **Tests de casos edge** (recursos inexistentes, límites)
- ✅ **Organización clara** por endpoint o funcionalidad

#### **Bueno (18-21 puntos)**

- ✅ Tests para operaciones CRUD principales
- ✅ Tests de validación básicos
- ✅ Tests de autorización presentes
- ⚠️ Algunos casos edge faltantes
- ⚠️ Organización mejorable

#### **Suficiente (14-17 puntos)**

- ✅ Tests básicos de CRUD funcionando
- ⚠️ Validaciones mínimas cubiertas
- ⚠️ Autorización básica
- ❌ Faltan tests de casos importantes

#### **Insuficiente (0-13 puntos)**

- ❌ Tests CRUD incompletos
- ❌ No valida casos críticos
- ❌ Autorización no probada

---

### **4. Coverage y Calidad (20 puntos)**

#### **Excelente (18-20 puntos)**

- ✅ **Coverage >85%** en módulos críticos (auth, core)
- ✅ **Coverage >80%** general del proyecto
- ✅ **Tests para casos edge** y manejo de errores
- ✅ **Tests de funciones utilitarias** (password hashing, JWT)
- ✅ **Organización profesional** (tests agrupados lógicamente)
- ✅ **Nomenclatura clara** de tests
- ✅ **Fixtures eficientes** y reutilizables
- ✅ **Documentación** de strategy de testing

#### **Bueno (14-17 puntos)**

- ✅ Coverage 75-85% general
- ✅ Tests de casos importantes
- ✅ Organización clara
- ⚠️ Algunas funciones sin cubrir
- ⚠️ Documentación básica

#### **Suficiente (10-13 puntos)**

- ⚠️ Coverage 65-75%
- ⚠️ Tests básicos funcionando
- ⚠️ Organización mejorable
- ❌ Gaps importantes en coverage

#### **Insuficiente (0-9 puntos)**

- ❌ Coverage <65%
- ❌ Tests desorganizados o de baja calidad
- ❌ Gaps críticos sin cubrir

---

### **5. Integración y E2E (15 puntos)**

#### **Excelente (13-15 puntos)**

- ✅ **Tests de workflow completo** (registro → login → operaciones)
- ✅ **Tests de aislamiento** entre usuarios
- ✅ **Tests de integración** real con DB
- ✅ **Tests de casos de uso** reales
- ✅ **Performance testing** básico
- ✅ **Tests de concurrencia** (si aplica)
- ✅ **Cleanup automático** entre tests

#### **Bueno (10-12 puntos)**

- ✅ Tests de workflows principales
- ✅ Tests de aislamiento básicos
- ✅ Integración con DB funcionando
- ⚠️ Tests E2E limitados

#### **Suficiente (7-9 puntos)**

- ✅ Algunos tests de integración
- ⚠️ Workflows básicos cubiertos
- ⚠️ Cleanup funcionando

#### **Insuficiente (0-6 puntos)**

- ❌ Tests de integración ausentes o no funcionan
- ❌ No verifica workflows completos

---

## 🎖️ Escalas de Calificación

### **Puntuación Final**

| Rango      | Calificación     | Descripción                     |
| ---------- | ---------------- | ------------------------------- |
| **90-100** | **Excelente**    | Dominio profesional de testing  |
| **80-89**  | **Bueno**        | Sólido conocimiento de testing  |
| **70-79**  | **Suficiente**   | Testing básico implementado     |
| **60-69**  | **Insuficiente** | Conocimiento limitado           |
| **<60**    | **No aprobado**  | Requiere refuerzo significativo |

### **Competencias Clave Evaluadas**

| Competencia             | Peso       | Descripción                           |
| ----------------------- | ---------- | ------------------------------------- |
| **Testing Setup**       | ⭐⭐⭐     | Configuración profesional de ambiente |
| **Test Implementation** | ⭐⭐⭐⭐⭐ | Implementación efectiva de tests      |
| **Coverage Analysis**   | ⭐⭐⭐⭐   | Análisis y optimización de cobertura  |
| **Code Quality**        | ⭐⭐⭐⭐   | Organización y calidad del código     |
| **Integration Testing** | ⭐⭐⭐     | Testing de workflows completos        |

---

## 📋 Checklist de Entrega

### **Archivos Requeridos**

- [ ] **`tests/`** - Carpeta completa con todos los tests
- [ ] **`conftest.py`** - Configuración central de pytest
- [ ] **`pytest.ini`** - Configuración de pytest
- [ ] **`.coveragerc`** - Configuración de coverage
- [ ] **`requirements-dev.txt`** - Dependencias de desarrollo
- [ ] **`README_TESTING.md`** - Documentación de tests

### **Evidencias de Funcionamiento**

- [ ] **Screenshot del coverage report** (HTML o terminal)
- [ ] **Output de pytest** mostrando tests pasando
- [ ] **Ejemplo de test fallando** y mensaje de error claro
- [ ] **Demostración de fixtures** funcionando

### **Documentación**

- [ ] **Explicación de strategy** de testing adoptada
- [ ] **Justificación de fixtures** utilizadas
- [ ] **Descripción de casos edge** considerados
- [ ] **Instrucciones para ejecutar** los tests

---

## 🚨 Criterios de Aprobación

### **Mínimos Obligatorios (para pasar la semana)**

1. ✅ **Tests funcionando** - pytest ejecuta sin errores críticos
2. ✅ **Coverage >70%** - Cobertura mínima aceptable
3. ✅ **Tests de auth** - Login/registro funcionando
4. ✅ **Tests de CRUD** - Operaciones básicas cubiertas
5. ✅ **Fixtures básicas** - Usuarios y auth funcionando

### **Criterios de Excelencia (para destacar)**

1. 🌟 **Coverage >90%** en módulos críticos
2. 🌟 **Tests parametrizados** para múltiples casos
3. 🌟 **Performance testing** incluido
4. 🌟 **CI/CD configurado** (GitHub Actions)
5. 🌟 **Documentación completa** de testing strategy

---

## 💡 Consejos para Maximizar Puntuación

### **Enfoque en Calidad**

1. **Prioriza coverage inteligente** - mejor 85% bien hecho que 95% superficial
2. **Casos edge importantes** - tests de error son valiosos
3. **Nomenclatura descriptiva** - `test_should_return_404_when_user_not_found`
4. **Fixtures reutilizables** - invierte tiempo en fixtures de calidad

### **Organización Profesional**

1. **Agrupa tests lógicamente** - por funcionalidad o endpoint
2. **Separa unit vs integration** - estructura clara
3. **Documenta decisiones** - explica por qué hiciste ciertas elecciones
4. **Cleanup automático** - tests independientes y repetibles

### **Demostración de Dominio**

1. **Casos complejos** - aislamiento entre usuarios, autenticación
2. **Manejo de errores** - tests que verifican errores apropiados
3. **Performance awareness** - al menos un test de performance
4. **Tools integration** - muestra conocimiento de herramientas

---

## 🎯 Objetivos de Aprendizaje Verificados

Al completar satisfactoriamente esta evaluación, el estudiante habrá demostrado:

- ✅ **Configurar** ambiente profesional de testing con pytest
- ✅ **Implementar** tests robustos para autenticación y seguridad
- ✅ **Crear** suite completa de tests CRUD con validaciones
- ✅ **Medir** y optimizar coverage de código efectivamente
- ✅ **Organizar** tests de manera profesional y mantenible
- ✅ **Integrar** testing en workflow de desarrollo
- ✅ **Documentar** estrategia y decisiones de testing

---

## ❓ Preguntas para Evaluación Oral (Opcional)

### **Conceptuales**

1. **¿Cuál es la diferencia entre unit, integration y E2E tests?**
2. **¿Por qué es importante el aislamiento entre tests?**
3. **¿Cómo decides qué nivel de coverage es apropiado?**

### **Prácticas**

1. **¿Cómo testearías un endpoint que envía emails?**
2. **¿Qué estrategia usas para testear autenticación?**
3. **¿Cómo manejas datos de testing vs producción?**

### **Arquitectura**

1. **¿Cómo organizas fixtures para proyectos grandes?**
2. **¿Qué tools adicionales integrarías para CI/CD?**
3. **¿Cómo balanceas velocidad vs completeness en tests?**

---

¡Esta rúbrica asegura evaluación objetiva y constructiva del aprendizaje de testing! 📊✅
