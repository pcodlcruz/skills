# 🎓 Profesor particular — {{NOMBRE}} ({{CODIGO}})

Sistema de estudio para preparar y aprobar el examen **{{NOMBRE}}** de {{PROVEEDOR}}.
Claude actúa como profesor (skill `google-cloud-certification-tutor`): te lanza preguntas tipo examen en
**{{IDIOMA_PREGUNTAS}}**, te da feedback en **{{IDIOMA_FEEDBACK}}** y lleva el registro de tu progreso.

## 🚀 Cómo empezar una sesión

Abre Claude Code en esta carpeta y di algo como:

- `"Empecemos"` / `"Hazme preguntas"` → ronda (te pregunto tamaño y dominio).
- `"Repasemos <dominio o tema>"` → tanda enfocada.
- `"Simulacro completo"` → {{N_PREGUNTAS}} preguntas ponderadas como el examen real.
- `"Repaso de fallos"` → vuelve sobre lo que fallaste, o genera la guía de fallos.
- `"¿Cómo voy?"` → panel de progreso. `"Dashboard visual"` → dashboard HTML.
- `"Genera los PDF"` → tips y repaso en PDF para leer fuera.

> **Tras clonar el repo** (tus datos están en `.gitignore`):
> ```bash
> cp progreso/registro.example.csv progreso/registro.csv
> cp preguntas/banco.example.md preguntas/banco.md
> ```

## 🗂️ Estructura

```
├── certificacion.json        # Dominios, pesos, nº de preguntas, umbral, idiomas
├── guia/
│   ├── mapa-dominios.md      # La guía oficial destilada: dominios, subtemas, servicios
│   ├── tips.md               # Un tip por pregunta, agrupados por dominio
│   ├── repaso-fallos.md      # Anatomía de los fallos y patrones de trampa (bajo demanda)
│   └── repaso-tips.md        # Tips consolidados y verificados (sprint final)
├── preguntas/banco.md        # Todas las preguntas usadas + respuesta + explicación
├── progreso/
│   ├── registro.csv          # Fuente de verdad: 1 fila por respuesta
│   ├── estado.md             # Dónde lo dejamos (simulacro en curso, plan, fecha examen)
│   └── dashboard.md          # Panel legible (lo regenera el script)
└── scripts/
    ├── progreso.py           # Panel: global, por dominio, ponderado, tendencia, siguientes IDs
    └── md2pdf.py             # Guías .md → PDF
```

## 📊 Progreso

```bash
python3 scripts/progreso.py              # panel completo
python3 scripts/progreso.py --fallos     # lista de falladas
python3 scripts/progreso.py --simulacro  # reparto de un simulacro por pesos
```

## 🎯 Dominios del examen

{{TABLA_DOMINIOS}}

Detalle en [`guia/mapa-dominios.md`](guia/mapa-dominios.md). Guía oficial: {{URL_GUIA}}

## 📝 Sobre el examen

- ~{{N_PREGUNTAS}} preguntas · {{DURACION}} min · opción única y selección múltiple.
- Basado en escenarios: hay que elegir la **mejor** solución, no solo una válida.
- Umbral orientativo: ~{{UMBRAL}}% (Google no publica la nota de corte).
