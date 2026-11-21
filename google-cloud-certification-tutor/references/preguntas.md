# Cómo escribir preguntas tipo examen

Lo que hace que el entrenamiento sirva: que las preguntas se parezcan al examen real **y**
que no se puedan acertar por patrones ajenos al contenido.

## Anatomía de una pregunta

```
### S3-014 · Managing encryption at rest · multi · alta        ← solo en banco.md

A healthcare company stores ... [escenario de 3-6 frases: empresa, situación, restricción
de negocio, requisito técnico]. The security team requires that ... [requisito exacto].
What should you do? (Choose two.)

A. ...
B. ...
C. ...
D. ...
E. ...
```

- **Escenario realista**, no definiciones. Empresa + contexto + una o dos restricciones
  (coste, plazo, "existing workloads", "without downtime", región, regulación).
- **Pregunta final estilo Google**: "What should you do?", "Which approach should you
  recommend?", "What is the MOST cost-effective way to...", "(Choose two.)".
- 4 opciones en `single`, 5 en `multi`. En `multi` indica siempre cuántas: "(Choose two.)".
- Opciones de **longitud y estilo parecidos**: la correcta no puede ser la más larga ni la
  única con detalle técnico.
- Las opciones van en **texto plano: nunca negrita, cursiva ni código resaltado** en una sola
  opción (delata la respuesta). Si usas `code` para nombres de constraint/flag, úsalo en todas.
- Al presentar la pregunta al usuario **no muestres el ID, el subtema ni la dificultad**: solo
  "Pregunta N/M · Dominio (S3)" si ayuda a orientarse. El subtema da pistas.

## Posición de la correcta

Antes de fijar el orden, mira las letras correctas de las 3-4 preguntas anteriores de la sesión
y **no repitas** la misma letra seguida. En un simulacro, la distribución A/B/C/D(/E) debe
quedar aproximadamente uniforme. (Lección real: varias B seguidas en un simulacro → el usuario
lo notó y el simulacro perdió valor.)

## Calibración de dificultad

Por defecto `alta` en Professional, `media/alta` en Associate, `media` en Foundational. Lo que
sube el nivel de verdad (calibrado contra el examen real):

1. **Dos opciones técnicamente válidas**, y el enunciado decide con "LEAST disruption",
   "MOST cost-effective", "minimal operational overhead", "without changing application code".
2. **Detalle fino dentro del mismo servicio**: el constraint exacto de Org Policy, el rol
   predefinido concreto, la sintaxis de la condición, el valor por defecto, qué hace y qué NO
   hace una feature (p. ej. "rotar una clave no re-cifra los datos").
3. **Distractores que fusionan dos conceptos casi correctos** en una opción: servicio correcto +
   comportamiento falso, o mecanismo correcto aplicado en el nivel/lugar equivocado.
4. **Más `multi`** (~30-40% de las preguntas): las dos correctas cubren **requisitos distintos**
   del enunciado; un distractor resuelve lo mismo que una correcta, por otra vía.
5. **Escenarios que cruzan dos dominios** (p. ej. red + IAM, datos + cumplimiento).
6. El **verbo manda**: prevent / detect / discover / remediate / contain / approve / audit.
   Ofrece siempre como distractor el control del verbo vecino.

No subas el nivel con trucos de lectura (dobles negaciones, enunciados ambiguos): el examen
real es exigente en contenido, no tramposo en redacción. Si al revisar ves que hay dos
respuestas defendibles, reescribe la pregunta antes de lanzarla.

## Catálogo de trampas (patrones de error reales)

Úsalo para construir distractores **y** para diagnosticar fallos en el feedback. Cuando el
usuario caiga en uno, nómbralo (ayuda a reconocerlo la próxima vez).

| Código | Trampa | Cómo se ve |
|---|---|---|
| 🅐 | **Detectivo vs preventivo** (el verbo) | Piden "prevent/block/approve before" y la opción ofrece el control que solo registra o alerta |
| 🅑 | **Herramienta correcta, pregunta equivocada** | El servicio es del área correcta, pero responde a otra pregunta (descubrir vs proteger, analizar vs explicar por qué) |
| 🅒 | **Justificación falsa dentro de una opción plausible** | "Usa X, porque X hace Y" — X está bien, Y es falso. Lee cada opción en dos mitades |
| 🅓 | **Alcance demasiado amplio o parche operativo** | Borrar/desactivar todo, script reactivo o cron cuando hay un control nativo, aplicar en org cuando bastaba un proyecto |
| 🅔 | **Lo más completo vs lo mínimo pedido** | Producto "premium" que lo cubre todo frente al control único que pide el requisito con "least disruption" |
| 🅕 | **Remediar vs contener** | Piden "contain immediately / reversible" y la opción repara de fondo (lento, irreversible) |
| 🅖 | **Conceptos gemelos** | Pares que el examen confunde a propósito (en GCP: labels vs tags, private vs restricted VIP, Access Transparency vs Approval, IAM Conditions vs Deny, FPE vs determinista...) |
| 🅗 | **Modelo de herencia/resolución equivocado** | Aplicar la regla de un sistema a otro (deny gana / nearest node gana / reemplaza vs fusiona) |
| 🅘 | **No retroactivo** | La política se aplica a recursos nuevos; la opción asume que arregla lo existente |
| 🅙 | **Multi: dos correctas que resuelven lo mismo** | Si tus dos elegidas cubren el mismo requisito, una sobra y falta otra |

Añade al `estado.md` del proyecto los patrones propios que vayan apareciendo, y los gemelos
específicos de cada certificación.

## Fuentes de realismo

- Las **sample questions oficiales** de la certificación marcan el tono. Úsalas para calibrar
  (léelas tú), pero no las copies como preguntas propias.
- **No reproduzcas preguntas de dumps** (ExamTopics, etc.) ni preguntas reales filtradas: viola
  los términos del examen y no enseña. Crear preguntas originales del mismo estilo sí.
- Contenido técnico: si un detalle fino no lo tienes claro al 100% (valor por defecto, nombre
  exacto de un constraint, si una feature sigue en preview), verifícalo antes de usarlo como
  clave de una pregunta (ver "Verificación" en SKILL.md). Una pregunta con la clave mal enseña
  lo contrario.

## Repaso de fallos (modo)

- Pregunta nueva sobre **el mismo concepto** que se falló, con escenario distinto: no repitas
  el enunciado literal (se acierta de memoria y no mide nada).
- Prioriza `python3 scripts/progreso.py --fallos` + los "subtemas con fallos recurrentes" del panel.
