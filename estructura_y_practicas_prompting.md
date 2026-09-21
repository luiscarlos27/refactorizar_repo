# Guía Práctica de Prompting para Desarrollo de Software

---

## 📋 Plantilla Base: Estructura de Prompt

```markdown
[ROL]
Eres un desarrollador de software experto en Python 3.9, PHP 8 y .NET Y.

[CONTEXTO Y ARCHIVOS]
Entorno tecnológico: [Ej. Node.js 20, TypeScript, Jest]
Código / Archivo de entrada:
<code_context>
[Pegar código o variable {input_code}]
</code_context>

[TAREA]
Vas a crear un login inteligente que se conecte con Microsoft Teams y permite hacer login UNICAMENTE a los usuarios activos del domino X. Además debes escribir un log local por cada ingreso de un usuario. ESTO ES MUY IMPORTANTE.

[RESTRICCIONES]
- Aplica el principio de responsabilidad única (SRP).
- Incluye validación de tipos explícita.
- No agregues librerías externas adicionales.
- Maneja excepciones para los escenarios [A, B].

[FORMATO DE SALIDA]
Entrega [Estructura esperada: ej. Solo el bloque de código / JSON con llaves 'status', 'data', 'errors'].
```

---

## 🛠️ Prácticas de Prompting

---

### 1. Refactorización y Explicación de Código Legado
* **Nivel:** Simple  
* **Objetivo:** Redactar un prompt que tome un bloque de código complejo o poco claro (ej. una expresión regular gigante, una consulta SQL anidada o un script de Shell) y entregue una explicación paso a paso junto con una versión refactorizada y legible.
* **Desafío para el estudiante:** Estructurar el prompt para que el modelo limite la explicación a puntos concretos y entregue el código optimizado sin alterar la lógica original ni perder casos borde.

---

### 2. Conversor de Requerimientos a Tipos e Interfaces
* **Nivel:** Intermedio  
* **Objetivo:** Diseñar un prompt que reciba la descripción en texto plano de una funcionalidad (ej. *"El sistema debe permitir a un usuario administrador gestionar suscripciones con estados de pago, fechas de vencimiento y métodos de cobro"*) y cree las estructuras de datos (interfaces de TypeScript, dataclasses de Python o structs de Go).
* **Desafío para el estudiante:** Guiar al LLM para que infiera tipos nulos, enumeraciones (enums), claves primarias y opcionales, solicitando además explicaciones de por qué tomó cada decisión de modelado.

---

### 3. Diagnóstico de Errores y Root Cause Analysis
* **Nivel:** Complejo  
* **Objetivo:** Crear un prompt reutilizable para depuración donde el desarrollador pegue un stack trace o un log de producción críptico y el modelo responda con la causa raíz probable, soluciones sugeridas y comandos para reproducir el fallo.
* **Desafío para el estudiante:** Evitar que el modelo invente contexto (alucine), obligándolo a solicitar más datos si la traza es insuficiente y a ordenar las soluciones de mayor a menor probabilidad de éxito.

---

### 4. Generador de Configuraciones de Despliegue y CI/CD
* **Nivel:** Muy Complejo  
* **Objetivo:** Construir un prompt que acepte la pila tecnológica de un proyecto (ej. *"API REST en Node.js, base de datos PostgreSQL y caché en Redis"*) y genere el archivo `docker-compose.yml` de desarrollo o un workflow de GitHub Actions listo para producción.
* **Desafío para el estudiante:** Restringir el prompt para que aplique buenas prácticas de seguridad por defecto (variables de entorno protegidas, usuarios no-root, imágenes alpine ligeras) y entregue un YAML sintácticamente perfecto sin explicaciones genéricas adicionales.

---

### 5. Revisor Automático de Pull Requests
* **Nivel:** Avanzado / Complejo  
* **Objetivo:** Diseñar un prompt que tome el diff de un commit o Pull Request y actúe como un revisor de código senior, identificando antipatrones (*code smells*), violaciones de principios SOLID y posibles cuellos de botella de rendimiento.
* **Desafío para el estudiante:** Configurar el prompt para que categorice las observaciones por severidad (*Crítico*, *Sugerencia*, *Nitpick*) y evite hacer comentarios puramente estéticos o redundantes si el código ya cumple con la funcionalidad.

---

### 6. Generador de Scripts de Migración de Base de Datos y Rollback
* **Nivel:** Avanzado / Complejo  
* **Objetivo:** Construir un prompt que reciba el esquema actual de una base de datos junto con un nuevo requerimiento de negocio, y genere tanto el script SQL de migración (UP) como el script de reversión (DOWN/ROLLBACK).
* **Desafío para el estudiante:** Obligar al modelo a priorizar la preservación de datos existentes (evitando comandos destructivos sin una estrategia previa de transformación) y garantizar que las operaciones de reversión sean estrictamente simétricas y seguras para producción.