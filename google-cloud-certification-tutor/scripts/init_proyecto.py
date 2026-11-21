#!/usr/bin/env python3
"""Crea la estructura de un proyecto de estudio para una certificación.

Uso:
    python3 init_proyecto.py <carpeta_destino> <certificacion.json>

- Copia `certificacion.json` a la raíz del proyecto.
- Crea guia/, preguntas/, progreso/, scripts/ y las plantillas (README, CLAUDE.md,
  banco, tips, estado, registro, .gitignore, esqueleto de mapa de dominios).
- Copia progreso.py y md2pdf.py en scripts/ del proyecto (así se ejecutan por ruta
  relativa dentro del directorio de trabajo, sin prompts de permiso).
- NUNCA sobrescribe un archivo existente: los que ya existen se listan como "omitido".
"""

import json
import os
import shutil
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANTILLAS = os.path.join(SKILL_DIR, "assets", "plantillas")

CABECERA_CSV = "fecha,id_pregunta,seccion,subtema,dificultad,tipo,correcta,elegida\n"

IDIOMAS = {"en": "inglés", "es": "español", "fr": "francés", "de": "alemán",
           "pt": "portugués", "it": "italiano", "ja": "japonés"}


def validar(cfg):
    for campo in ("codigo", "nombre", "dominios"):
        if campo not in cfg:
            sys.exit(f"certificacion.json: falta el campo '{campo}'")
    cods = [d["cod"] for d in cfg["dominios"]]
    if len(set(cods)) != len(cods):
        sys.exit("certificacion.json: códigos de dominio repetidos")
    suma = sum(d["peso"] for d in cfg["dominios"])
    if not 95 <= suma <= 105:
        print(f"⚠️  Los pesos suman {suma}% (se esperaba ~100%). Revísalos.")


def variables(cfg):
    ex = cfg.get("examen", {})
    filas = "\n".join(f"| {d['cod']} | {d['nombre']} | ~{d['peso']}% |" for d in cfg["dominios"])
    esqueleto = "\n\n---\n\n".join(
        f"## {d['cod']} — {d['nombre']} (~{d['peso']}%)\n\n_(subtemas y servicios clave de la guía oficial)_"
        for d in cfg["dominios"])
    tips = "\n\n".join(f"## {d['cod']} — {d['nombre']}\n" for d in cfg["dominios"])
    return {
        "{{CODIGO}}": cfg["codigo"],
        "{{NOMBRE}}": cfg["nombre"],
        "{{PROVEEDOR}}": cfg.get("proveedor", "Google Cloud"),
        "{{IDIOMA_PREGUNTAS}}": IDIOMAS.get(cfg.get("idioma_preguntas", "en"), cfg.get("idioma_preguntas", "en")),
        "{{IDIOMA_FEEDBACK}}": IDIOMAS.get(cfg.get("idioma_feedback", "es"), cfg.get("idioma_feedback", "es")),
        "{{N_PREGUNTAS}}": str(ex.get("preguntas", 50)),
        "{{DURACION}}": str(ex.get("duracion_min", 120)),
        "{{UMBRAL}}": str(ex.get("umbral_pct", 70)),
        "{{URL_GUIA}}": cfg.get("url_guia", "") or "_(pendiente)_",
        "{{TABLA_DOMINIOS}}": "| Cód | Dominio | Peso |\n|-----|---------|------|\n" + filas,
        "{{ESQUELETO_DOMINIOS}}": esqueleto,
        "{{SECCIONES_TIPS}}": tips,
        "{{EJEMPLO_ID}}": cfg["dominios"][0]["cod"] + "-001",
    }


def render(nombre_plantilla, vars_):
    with open(os.path.join(PLANTILLAS, nombre_plantilla), encoding="utf-8") as f:
        texto = f.read()
    for k, v in vars_.items():
        texto = texto.replace(k, v)
    return texto


def escribir(ruta, contenido, creados, omitidos):
    if os.path.exists(ruta):
        omitidos.append(ruta)
        return
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    creados.append(ruta)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    destino = os.path.abspath(sys.argv[1])
    with open(sys.argv[2], encoding="utf-8") as f:
        cfg = json.load(f)
    validar(cfg)
    v = variables(cfg)
    creados, omitidos = [], []
    j = lambda *p: os.path.join(destino, *p)

    escribir(j("certificacion.json"), json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", creados, omitidos)
    escribir(j("README.md"), render("README.md", v), creados, omitidos)
    escribir(j("CLAUDE.md"), render("CLAUDE.md", v), creados, omitidos)
    escribir(j(".gitignore"), render("gitignore", v), creados, omitidos)
    escribir(j("guia", "mapa-dominios.md"), render("mapa-dominios.md", v), creados, omitidos)
    escribir(j("guia", "tips.md"), render("tips.md", v), creados, omitidos)
    escribir(j("preguntas", "banco.md"), render("banco.md", v), creados, omitidos)
    escribir(j("preguntas", "banco.example.md"), render("banco.md", v), creados, omitidos)
    escribir(j("progreso", "registro.csv"), CABECERA_CSV, creados, omitidos)
    escribir(j("progreso", "registro.example.csv"), CABECERA_CSV, creados, omitidos)
    escribir(j("progreso", "estado.md"), render("estado.md", v), creados, omitidos)

    for script in ("progreso.py", "md2pdf.py"):
        dst = j("scripts", script)
        if os.path.exists(dst):
            omitidos.append(dst)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(SKILL_DIR, "scripts", script), dst)
            creados.append(dst)

    print(f"Proyecto: {destino}")
    for r in creados:
        print(f"  + {os.path.relpath(r, destino)}")
    for r in omitidos:
        print(f"  = {os.path.relpath(r, destino)} (ya existía, omitido)")


if __name__ == "__main__":
    main()
