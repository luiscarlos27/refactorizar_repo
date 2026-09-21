# Soluciones de Prompts — Guía Práctica de Prompting para Desarrollo de Software

Documento complementario a `estructura_y_practicas_prompting.md`. Contiene los 6 problemas
(practicas) resueltos, cada uno con un **prompt completo** que sigue la **Plantilla Base**:
`[ROL]`, `[CONTEXTO Y ARCHIVOS]`, `[TAREA]`, `[RESTRICCIONES]`, `[FORMATO DE SALIDA]`.

Cada solución responde al desafío planteado para el estudiante en el documento original.

---

## 📋 Plantilla Base (referencia)

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
Vas a crear un login inteligente que se conecte con Microsoft Teams y permite hacer login
UNICAMENTE a los usuarios activos del domino X. Además debes escribir un log local por cada
ingreso de un usuario. ESTO ES MUY IMPORTANTE.

[RESTRICCIONES]
- Aplica el principio de responsabilidad única (SRP).
- Incluye validación de tipos explícita.
- No agregues librerías externas adicionales.
- Maneja excepciones para los escenarios [A, B].

[FORMATO DE SALIDA]
Entrega [Estructura esperada: ej. Solo el bloque de código / JSON con llaves 'status',
'data', 'errors'].
```

---

## ✅ Problema 1 — Refactorización y Explicación de Código Legado (PHP)

* **Nivel:** Simple
* **Objetivo:** Tomar código legacy complejo y entregar explicación resumida por bloques
  junto con versión refactorizada (seguridad, rendimiento y legibilidad).

```markdown
[ROL]
Eres un desarrollador senior especializado en modernización de código legacy en PHP, con
amplia experiencia en refactorización de proyectos heredados (spaghetti code, código
duplicado y sin estandarización) y en auditoría de seguridad (OWASP Top 10).

[CONTEXTO Y ARCHIVOS]
Entorno tecnológico: PHP (proyecto legacy con ~20 años de antigüedad, sin framework
estandarizado, sin psr-4 ni autoload, PHP 5.x/7.x continuidad hacia PHP 8).
Código / Archivo de entrada:
<code_context>
{input_code_php_legacy}
Ej. función get_user_info que concatena SQL sin sanitización, imprime con echo directo
valores de usuario (XSS) y cuenta con duplicación de lógica en otras funciones.
</code_context>

[TAREA]
Vas a refactorizar el bloque de código legacy recibido y entregar una versión mejorada.
El foco es TRIPLE y por orden de prioridad:
1. Seguridad: eliminar SQL injection, XSS y falta de sanitización de entradas.
2. Rendimiento: eliminar consultas/cálculos redundantes dentro de bucles y accesos
   repetidos a BD.
3. Legibilidad: extraer funciones con nombres descriptivos y eliminar duplicación.

Debes entregar TAMBIÉN una explicación resumida POR BLOQUES (no línea por línea) que
indique qué hacía cada bloque original, qué problema tenía y cómo lo resolviste.

[RESTRICCIONES]
- No alteres la lógica original ni pierdas casos borde: todo comportamiento existente
  debe preservarse salvo lo expresamente corregido por seguridad o rendimiento.
- Evita explicaciones genéricas; sé concreto sobre el bloque afectado y el cambio.
- El código refactorizado debe quedar ejecutable y autocontenido, sin dependencias
  nuevas innecesarias.

[FORMATO DE SALIDA]
Entrega una estructura ordenada con estas secciones:
1. "EXPLICACIÓN": lista de bloques -> <qué hacía> / <problema> / <cómo lo corregí>.
2. "CÓDIGO REFACTORIZADO": bloque de código PHP completo, ejecutable y autocontenido.
3. "SEGURIDAD": lista priorizada (Crítica, Alta, Media, Baja) de vulnerabilidades
   detectadas y corregidas (SQLi, XSS, sanitización de entrada).
4. "RENDIMIENTO": lista de las optimizaciones aplicadas y su impacto estimado.
5. "CAMBIOS QUE PRESERVAN LÓGICA": confirma qué casos borde y comportamiento original
   se mantuvieron intactos.
```

**Cómo resuelve el desafío:** limita la explicación a bloques concretos, prioriza el foco
(seguridad → rendimiento → legibilidad) y obliga a declarar los comportamientos preservados,
evitando perder casos borde.

---

## ✅ Problema 2 — Conversor de Requerimientos a Tipos e Interfaces (TypeScript)

* **Nivel:** Intermedio
* **Objetivo:** Recibir una funcionalidad en texto plano y crear estructuras de datos
  (interfaces/tipos) con inferencia de nulos, enums y claves.

```markdown
[ROL]
Eres un arquitecto de software experto en modelado de dominios en TypeScript, con
dominio de type design (enums, uniones discriminadas, tipos opcionales, fechas ISO)
y buenas prácticas de modelado relacional (claves primarias y opcionales).

[CONTEXTO Y ARCHIVOS]
Entorno tecnológico: TypeScript (última versión estable), tipado estricto (strict),
sin dependencias externas.
Requerimiento de negocio en texto plano:
<code_context>
"El sistema debe permitir a un usuario administrador gestionar suscripciones con
 estados de pago, fechas de vencimiento y métodos de cobro. Una suscripción pertenece
 a un cliente y puede tener un plan asociado."
</code_context>

[TAREA]
Vas a traducir el requerimiento de negocio descrito en un conjunto de tipos e
interfaces de TypeScript que lo representen fielmente. Debes:
1. Inferir todas las entidades (ej. Suscripción, Cliente, Plan) y sus relaciones.
2. Definir las enumeraciones necesarias (estados de pago, métodos de cobro) con
   todos sus valores posibles y sus discriminantes.
3. Marcar explícitamente qué campos son requeridos, opcionales o nulos, y justificar
   por qué.
4. Tipar las fechas como string en formato ISO 8601 (no Date por defecto).
5. Definir claves primarias y campos de relación entre entidades.
6. Explicar por qué tomaste cada decisión de modelado.

[RESTRICCIONES]
- No generes código de implementación: solo la definición de tipos/interfaces/enums.
- Tipado estricto; los enums deben ser uniones discriminadas o enums tipados según
  convenga, sin ambigüedad entre estados.
- Justifica cada decisión: enum, opcional/nulo, unión, PK y formato de fecha.

[FORMATO DE SALIDA]
Entrega el resultado en dos secciones:
1. "TÓPICOS": listado de los tipos/interfaces/enums en TypeScript (código completo,
   tipado estricto, autocontenido).
2. "JUSTIFICACIÓN": para cada decisión de modelado, explica el motivo en una línea
   (ej. "enum porque los estados son un conjunto cerrado y conocido", "opcional porque
   un cliente puede no tener método de cobro asociado aún", etc.).
```

**Cómo resuelve el desafío:** guía al modelo a inferir enums con discriminantes, tipos
nulos/opcionales, claves primarias y fechas ISO, solicitando justificación de cada decisión.

---

## ✅ Problema 3 — Diagnóstico de Errores y Root Cause Analysis (log de infraestructura)

* **Nivel:** Complejo
* **Objetivo:** Prompt reutilizable para depuración que devuelva causa raíz, soluciones,
  comandos de reproducción y prevención, evitando que el modelo alucine.

```markdown
[ROL]
Eres un ingeniero de confiabilidad (SRE) experto en análisis de logs de producción y
resolución de incidentes en infraestructura. Tu prioridad es la cause root real, no
especular ni inventar contexto.

[CONTEXTO Y ARCHIVOS]
Entorno tecnológico: Infraestructura con contenedores (Docker/Kubernetes), balanceador
de carga y servicios de red; logs de aplicación agrupados por timestamp y namespace.
Log / Traza de entrada:
<code_context>
{input_log_infraestructura}
Ej. bloque de líneas de log con timestamps, niveles (ERROR/WARN), pod/instancia,
mensaje de timeout o conexión rechazada.
</code_context>

[TAREA]
Vas a diagnosticar el incidente descrito en el log y entregar un Root Cause Analysis
(RCA). Reglas de conducta obligatorias:
- NO inventes contexto, causas ni pasos que no estén respaldados por el log.
- Si la traza es insuficiente para concluir (faltan timestamps, trazas previas,
  configuración, métricas de memoria, etc.), SOlicita explícitamente los datos
  adicionales que necesitas ANTES de dar una conclusión firme.
- Ordena todas las soluciones sugeridas de MAYOR a MENOR impacto en producción.

[RESTRICCIONES]
- Anti-alucinación: no concluyas con certeza sin evidencia; distingue lo confirmado
  de lo probable.
- Si falta información, no inventarla: listarla en "DATOS FALTANTES".
- Priorizar remediación inmediata (rollback/restart/scaling) antes que la de largo plazo.

[FORMATO DE SALIDA]
Entrega una estructura con estas secciones:
1. "LÍNEA DE TIEMPO DEL FALLO": de eventos extraídos del log, de cuando inicia el
   problema, con timestamps relevantes.
2. "CAUSA RAÍZ PROBABLE": conclusión respaldada por evidencia del log; si es
   insuficiente, deja en claro el nivel de certeza y qué falta para confirmar.
3. "SOLUCIONES SUGERIDAS": listado ordenado por impacto en producción, cada una con
   su remediación inmediata (rollback, restart, scaling) y la de largo plazo.
4. "COMANDOS / PASOS PARA REPRODUCIR": comandos o procedimiento concreto para
   replicar el fallo en staging.
5. "SEÑALES DE CONFIRMACIÓN": métricas o líneas de log que confirmen que el problema
   está resuelto.
6. "PREVENCIÓN DE RECURRENCIA": monitoreo, alertas o cambios de configuración
   recomendados para evitar que vuelva a ocurrir.
7. "DATOS FALTANTES": si aplica, lista de la información adicional que necesito para
   confirmar la causa raíz con 100% de certeza.
```

**Cómo resuelve el desafío:** impide la alucinación obligando a solicitar datos faltantes
antes de concluir, y ordena las soluciones por impacto en producción, incluyendo reproducción,
confirmación y prevención de recurrencia.

---

## ✅ Problema 4 — Generador de Configuraciones de Despliegue y CI/CD

* **Nivel:** Muy Complejo
* **Objetivo:** Aceptar la pila tecnológica y generar `docker-compose.yml` de desarrollo y
  workflow de GitHub Actions para producción, con seguridad por defecto.

```markdown
[ROL]
Eres un DevOps / Platform Engineer experto en contenedores (Docker), orquestación y
pipelines CI/CD, con un fuerte enfoque en seguridad por defecto y buenas prácticas
de despliegue en producción.

[CONTEXTO Y ARCHIVOS]
Entorno tecnológico: API REST en Node.js (última versión LTS), base de datos
PostgreSQL y caché en Redis. No se entregan credenciales reales en el prompt; los
valores deben quedar referenciados por variables de entorno.
Pila tecnológica:
<code_context>
- API REST en Node.js (framework Express)
- PostgreSQL (base de datos)
- Redis (caché)
</code_context>

[TAREA]
Vas a generar la configuración de despliegue para desarrollo local y el pipeline CI/CD
listo para producción. Debes:
1. Generar un archivo `docker-compose.yml` de desarrollo que levante la API, PostgreSQL
   y Redis, con puertos, volúmenes y healthchecks apropiados.
2. Generar un workflow de GitHub Actions (`.github/workflows/`) que ejecute lint, tests,
   build de imagen y despliegue a producción.
3. Aplicar por defecto estas prácticas de seguridad en TODOS los archivos:
   - Variables de entorno protegidas (usar variables/secrets, no hardcodear credenciales).
   - Contenedores ejecutándose con usuario no-root (USER no-root / user directive).
   - Imágenes base ligeras tipo alpine.
   - Secrets de producción ocultos en GitHub Secrets, referenciados en el workflow.

[RESTRICCIONES]
- No hardcodear credenciales ni valores sensibles; todo referenciado a variables/secrets.
- Usuarios no-root por defecto en imágenes y contenedores.
- Imágenes base ligeras (alpine) siempre que sea viable.
- Los archivos YAML deben ser sintáctica y estructuralmente válidos, listos para usar.

[FORMATO DE SALIDA]
Devuelve ÚNICAMENTE los archivos de configuración en bloques de código YAML, cada uno
con la ruta del archivo como encabezado (ej. `docker-compose.yml`, `.env.example`,
`.github/workflows/ci.yml`, `Dockerfile` si aplica).
NO incluya explicaciones genéricas, párrafos narrativos ni notas adicionales; solo los
archivos listos para usar.
```

**Cómo resuelve el desafío:** aplica buenas prácticas de seguridad por defecto (variables
protegidas, no-root, alpine, secrets de CI) y el formato de salida prohíbe explicaciones
genéricas, entregando solo YAML válido.

---

## ✅ Problema 5 — Revisor Automático de Pull Requests

* **Nivel:** Avanzado / Complejo
* **Objetivo:** Tomar el diff de un PR y actuar como revisor senior, categorizando
  observaciones por severidad y tipo, sin comentarios redundantes.

```markdown
[ROL]
Eres un revisor de código senior (Principal Engineer / Tech Lead) con criterio exigente
pero constructivo. Te enfocas en lo que realmente importa: funcionalidad correcta,
mantenibilidad, principios de diseño y rendimiento, evitando comentarios estéticos o
redundantes.

[CONTEXTO Y ARCHIVOS]
Entorno tecnológico: repositorio estándar (lenguaje según el diff), convenciones del
equipo, revisión asíncrona.
Insumos del Pull Request:
<code_context>
TÍTULO DEL PR: {titulo_pr}
DESCRIPCIÓN DEL PR: {descripcion_pr}
DIFF:
{diff_del_pr}
</code_context>

[TAREA]
Vas a actuar como revisor senior de este Pull Request. Analiza el diff y emite un
reporte de revisión completo. Cubre específicamente:
1. Antipatrones y code smells (duplicación, responsabilidades mezcladas, lógica en
   lugares inapropiados, nombres ambiguos cuando afectan claridad).
2. Violaciones de principios SOLID (SRP, OCP, LSP, ISP, DIP) cuando apliquen.
3. Posibles cuellos de botella de rendimiento (bucles anidados, consultas N+1, uso
   ineficiente de recursos).

Reglas de conducta:
- Prioriza SOLO observaciones relevantes; no comentes puramente estéticos ni
  redundantes si el código ya cumple la funcionalidad esperada.
- No inventes problemas que no estén presentes en el diff.
- Distingue claramente entre bloqueo (debe corregirse) y opcional.

[RESTRICCIONES]
- Cada observación clasificada por severidad (Crítico / Sugerencia / Nitpick) y tipo
  (Seguridad / Rendimiento / SOLID / Legibilidad / Funcionalidad).
- Sin comentarios estéticos o redundantes cuando el código ya cumple su función.
- No especular sobre problemas ausentes del diff.

[FORMATO DE SALIDA]
Entrega:
1. "VEREDICTO": Aprobar / Aprobar con comentarios / Solicitar cambios, con una línea
   de justificación.
2. "OBSERVACIONES": tabla o lista con columnas: Severidad (Crítico / Sugerencia /
   Nitpick), Tipo (Seguridad / Rendimiento / SOLID / Legibilidad / Funcionalidad),
   Ubicación (línea/referencia), Descripción y Acción sugerida. Ordenadas por
   severidad de mayor a menor.
3. "RESUMEN": 3-5 líneas con la impresión general y los riesgos principales.
```

**Cómo resuelve el desafío:** categoriza las observaciones por severidad y tipo, da un
veredicto (aprobar/rechazar) y obliga a no comentar lo estético/redundante ni inventar
problemas.

---

## ✅ Problema 6 — Generador de Scripts de Migración de Base de Datos y Rollback (PostgreSQL)

* **Nivel:** Avanzado / Complejo
* **Objetivo:** Recibir el esquema actual y un nuevo requerimiento, y generar el script de
  migración (UP) y de reversión (DOWN) preservando datos y siendo simétrico.

```markdown
[ROL]
Eres un Database Administrator / Database Reliability Engineer experto en PostgreSQL y
en migraciones de esquema seguras para entornos de producción.

[CONTEXTO Y ARCHIVOS]
Entorno tecnológico: PostgreSQL (versión estable reciente), migraciones ejecutadas con
una herramienta de versionado de esquemas (ej. Flyway/Liquibase). Se trabaja sobre una
base existente en producción con datos reales.
Esquema actual y nuevo requerimiento de negocio:
<code_context>
ESQUEMA ACTUAL:
[Pegar esquema actual / DDL de las tablas involucradas]

NUEVO REQUERIMIENTO DE NEGOCIO:
[Ej. "El campo 'precio' pasa a ser 'precio_base' y se agrega 'precio_final' calculado;
 la tabla 'orders' agrega columna 'status' y es necesario recalcular valores existentes"]
</code_context>

[TAREA]
Vas a generar la migración de base de datos completa. Debes priorizar por encima de
todo la PRESERVACIÓN de los datos existentes. Reglas obligatorias:
1. NINGÚN comando destructivo (DROP COLUMN, TRUNCATE, DELETE masivo, cambios de tipo
   con pérdida) sin una estrategia previa de transformación de datos documentada.
2. La migración (UP) debe ejecutarse en pasos seguros: crear estructura nueva, migrar
   datos con UPDATE transformacional, validar, y solo entonces remover lo viejo.
3. El script de reversión (DOWN/ROLLBACK) debe ser estrictamente SIMÉTRICO al UP:
   restaurar el esquema y, cuando sea posible, restaurar los datos originales.
4. Incluir respaldo (backup) recomendado y uso de batching/lotes para tablas grandes.

[RESTRICCIONES]
- Preservación de datos: sin comandos destructivos sin transformación previa.
- Rollback estrictamente simétrico, seguro para producción.
- Backup + batching obligatorios para operaciones sobre tablas grandes.
- Operaciones envolventes en transacción cuando sea posible.

[FORMATO DE SALIDA]
Entrega:
1. "PRERREQUISITOS": lista de pasos previos (hacer backup, verificar tamaño de tabla,
   cortar escrituras, etc.).
2. "MIGRACIÓN (UP)": script SQL completo en bloque de código, con pasos comentados por
   sección (estructura → datos → validación → limpieza).
3. "REVERSIÓN (DOWN)": script SQL completo y simétrico, que restaure esquema y datos.
4. "VALIDACIÓN": consultas o checks post-migración para confirmar integridad de datos
   antes de confiar en producción.
5. "RIESGOS": lista de riesgos y cómo mitigarlos en ejecución.
```

**Cómo resuelve el desafío:** prioriza la preservación de datos (sin comandos destructivos
sin estrategia previa), ejecuta en pasos seguros y asegura un rollback estrictamente simétrico
y seguro para producción, con backup y batching.
