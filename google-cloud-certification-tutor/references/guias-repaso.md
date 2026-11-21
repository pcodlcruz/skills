# Documentos de repaso

Tres documentos, con propósitos distintos. Todos en el idioma de feedback, en `guia/`, y con
versión PDF (`python3 scripts/md2pdf.py guia/<archivo>.md`) para leer fuera del ordenador.

## 1. `tips.md` — se alimenta solo, pregunta a pregunta

- Cada feedback termina con un **📌 Tip**: una regla corta, reutilizable, que sirva para la
  *siguiente* pregunta del tema, no un resumen de esta.
- Tras cada pregunta, añade el tip (con Edit) bajo el dominio que toca. Si se falló, márcalo
  `_(fallada)_`. Si viene de un test externo (sample oficial), `_(sample oficial)_`.
- Formato: `- **Regla en negrita** — matiz, y por qué el distractor típico no vale.`
- No dupliques: si ya hay un tip del mismo concepto, amplíalo en vez de añadir otro.

## 2. `repaso-fallos.md` — bajo demanda o tras cada simulacro

La **anatomía de por qué se falló**, no más preguntas. Estructura que funcionó:

```
# 🔁 Repaso de fallos — <CÓDIGO>
_Generado: fecha · cubre N fallos entre X e Y_

§1 · Patrones de error      ← agrupa los fallos por trampa (catálogo de preguntas.md).
                              "Tus N fallos no son N huecos distintos: son K patrones."
                              Tabla "verbo del enunciado → lo que pide → lo que NO vale".
§2 · Fichas por pregunta    ← una por fallo:
     ### `S1-006` · subtema · fecha · elegiste C,D — correcta **A,C**
     escenario resumido · por qué tu opción parecía buena · qué la invalida ·
     la regla a automatizar
§3 · Autotest rápido        ← tabla "pregunta corta | respuesta" (tapa la columna derecha)
§4 · Qué hacer en la próxima sesión  ← 2-3 hábitos concretos de lectura del enunciado
§5 · Certificación del contenido     ← ver abajo
```

Tras cada simulacro nuevo, añade una sección nueva (`§6 · Simulacro N`) en vez de reescribir:
el usuario valora ver la evolución.

## 3. `repaso-tips.md` — consolidado para el sprint final

Cuando `tips.md` pasa de ~100 tips o quedan ~2 semanas para el examen:

- **Fichas temáticas sin duplicados**: cada tema reúne lo que estaba en 2-5 tips sueltos.
- Leyenda: ⚠️ = tema fallado alguna vez · 🔧 = corregido contra la doc · **Señal →** la frase
  del enunciado que dispara la respuesta.
- **§1 Correcciones**: al consolidar aparecen contradicciones entre tips antiguos. Verifica
  cada una y pon tabla "el tip antiguo decía | lo correcto". Corrige también `tips.md` y `banco.md`.
- **§2 Reglas transversales** (sirven en todos los dominios: prevenir vs detectar, no
  retroactividad, modelos de herencia, mínimo privilegio, least overhead...).
- Luego un bloque por dominio y un **checklist final** para el día antes.

## Certificación del contenido (verificación contra la doc oficial)

Todo documento de repaso se verifica antes de darlo por bueno, con el MCP
`google-developer-knowledge` (`search_documents` / `answer_query`) o, si no está, la
documentación oficial vía web. Sección final con tres bloques:

- **✅ Confirmado** — tabla "afirmación | fuente (ruta de la doc)".
- **🆕 Matices que añadió la doc** — lo que no estaba y conviene saber.
- **⚠️ Correcciones** — afirmación falsa del material, cita de la doc, qué cambia (la respuesta
  de la pregunta o solo el porqué), y dónde se corrigió.

Si una corrección cambia la respuesta correcta de una pregunta ya registrada, corrige
`banco.md` y la fila de `registro.csv` (avisando al usuario), porque cambia su estadística.
