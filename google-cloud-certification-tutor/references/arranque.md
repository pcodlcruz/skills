# Arranque de una certificación nueva

Objetivo: dejar un proyecto listo para estudiar en una sola sesión, con la guía oficial
destilada y la configuración correcta. No inventes pesos ni dominios: salen de la guía oficial.

## 1. Conseguir la guía oficial

Por orden de preferencia:

1. **PDF que aporte el usuario** (lo ideal: es la versión que él va a examinar). Léelo con Read
   (`pages`) y guárdalo en la raíz del proyecto.
2. **Página oficial de la certificación**: `https://cloud.google.com/learn/certification/<slug>`
   (p. ej. `cloud-security-engineer`, `cloud-architect`, `data-engineer`, `cloud-engineer`,
   `cloud-devops-engineer`, `cloud-network-engineer`, `cloud-database-engineer`,
   `cloud-developer`, `machine-learning-engineer`, `cloud-digital-leader`,
   `generative-ai-leader`, `data-practitioner`, `workspace-administrator`...). Léela con el
   agente `web-fetch` pidiendo: formato del examen (nº preguntas, duración, tipos, idiomas),
   enlace a la exam guide y, si la hay, a las sample questions. Los slugs cambian: si uno no
   carga, búscalo con WebSearch.
3. Si la guía tiene **versión nueva anunciada** (Google lo indica en la página: "new exam
   guide effective <fecha>"), pregunta al usuario qué fecha de examen tiene y usa la versión
   que le aplique.

## 2. Extraer dominios y pesos

- Las guías de Google numeran secciones `Section 1: ... (~25% of the exam)`. Cada sección →
  un dominio `S1..Sn`, con su peso tal cual. Si una guía no trae pesos, repártelos por nº de
  subtemas y **díselo al usuario** (es una estimación, no oficial).
- Los subtemas (`1.1`, `1.2`...) y sus viñetas van a `guia/mapa-dominios.md`, en el idioma de
  feedback, conservando los nombres de producto en inglés. Añade debajo de cada subtema una
  línea **"Servicios clave:"** — es lo que luego guía la generación de preguntas.
- Formato del examen por nivel (verifícalo siempre en la página oficial, cambia):
  | Nivel | Preguntas | Duración | Notas |
  |---|---|---|---|
  | Foundational | ~50-60 | 90 min | conceptual, poco detalle de configuración |
  | Associate | ~50-60 | 120 min | más práctico: comandos, consola, pasos |
  | Professional | ~50-60 | 120 min | escenarios, "best/LEAST/MOST", trade-offs; algunos con case studies |
  Para el simulacro usa el nº real de preguntas (si da rango, el valor bajo: 50).
- Exámenes con **case studies** (p. ej. Professional Cloud Architect, DevOps): anota los casos
  publicados en `guia/case-studies.md` (resumen de requisitos técnicos y de negocio) y reserva
  ~20-30% del simulacro a preguntas sobre ellos.

## 3. Configuración

Escribe `certificacion.json` (ver `assets/certificacion.ejemplo.json`). Campos:

| Campo | Qué es |
|---|---|
| `codigo` | Sigla corta (PCSE, PCA, ACE, PDE...) |
| `nombre`, `proveedor`, `nivel`, `url_guia` | Identificación |
| `idioma_preguntas` / `idioma_feedback` | Por defecto `en` / `es`: el examen se hace en inglés y se aprende mejor el porqué en la lengua propia. Pregunta solo si el usuario va a examinarse en otro idioma |
| `fecha_examen` | `YYYY-MM-DD` o `null`; el panel muestra la cuenta atrás |
| `examen.preguntas` / `duracion_min` / `umbral_pct` | Para el simulacro y el veredicto (umbral 70 si no hay dato oficial) |
| `dominios[]` | `{cod, nombre, peso}` |

Escríbelo primero en el scratchpad, y genera el proyecto:

```bash
python3 ~/.claude/skills/google-cloud-certification-tutor/scripts/init_proyecto.py <carpeta> <ruta>/certificacion.json
```

El script no sobrescribe nada que exista. Después rellena tú `guia/mapa-dominios.md` con los
subtemas (el script solo deja el esqueleto).

## 4. Cierre del arranque

1. `git init` si no es repo (pregunta antes), con el `.gitignore` ya generado — los datos
   personales (registro, banco, tips, estado) quedan fuera; las plantillas `*.example.*` dentro.
2. `python3 scripts/progreso.py` para comprobar que el panel sale ("sin datos aún").
3. Rellena `progreso/estado.md` (fecha de examen si la sabe, fase "diagnóstico").
4. Propón el plan (ver "Fases del plan de estudio" en SKILL.md) y ofrece la ronda de diagnóstico.
