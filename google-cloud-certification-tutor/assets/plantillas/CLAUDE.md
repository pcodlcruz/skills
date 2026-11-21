# Proyecto de estudio — {{NOMBRE}} ({{CODIGO}})

Este repo es un **profesor particular** para preparar el examen {{CODIGO}} de {{PROVEEDOR}}.
Se gestiona con la skill **`google-cloud-certification-tutor`**: cárgala al empezar cualquier sesión de
estudio ("empecemos", "hazme preguntas", "simulacro", "¿cómo voy?", "repaso de fallos"...).

- Preguntas en **{{IDIOMA_PREGUNTAS}}**, feedback en **{{IDIOMA_FEEDBACK}}**.
- Configuración del examen (dominios, pesos, nº de preguntas, umbral): `certificacion.json`.
- Estado de la sesión en curso (simulacro a medias, plan, fecha de examen): `progreso/estado.md`.
  **Léelo lo primero** al abrir sesión y actualízalo al cerrarla.
- Fuente de verdad del progreso: `progreso/registro.csv` → `python3 scripts/progreso.py`.
- `preguntas/banco.md` contiene las respuestas: no lo muestres al usuario antes de que responda.

## Preferencias propias de este proyecto

_(Anota aquí lo que el usuario pida específicamente para esta certificación.)_
