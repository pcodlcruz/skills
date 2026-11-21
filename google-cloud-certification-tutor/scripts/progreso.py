#!/usr/bin/env python3
"""Panel de progreso genérico para preparar una certificación.

Lee la configuración de `certificacion.json` (raíz del proyecto) y el registro
`progreso/registro.csv` (fuente de verdad), y:
  - Imprime el panel (acierto global, por dominio, preparación ponderada,
    tendencia, zonas y subtemas a reforzar, siguientes IDs).
  - Reescribe `progreso/dashboard.md` con el mismo contenido.

Sin dependencias externas (solo stdlib). Uso, desde la raíz del proyecto:
    python3 scripts/progreso.py              # panel completo + dashboard.md
    python3 scripts/progreso.py --ids        # solo los siguientes IDs libres
    python3 scripts/progreso.py --simulacro  # reparto de preguntas de un simulacro
    python3 scripts/progreso.py --fallos     # preguntas falladas (para repaso)
    python3 scripts/progreso.py --json       # datos en JSON (dashboard HTML)
"""

import csv
import json
import os
import re
import sys
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(RAIZ, "certificacion.json")
CSV_PATH = os.path.join(RAIZ, "progreso", "registro.csv")
BANCO_PATH = os.path.join(RAIZ, "preguntas", "banco.md")
DASHBOARD_PATH = os.path.join(RAIZ, "progreso", "dashboard.md")

ULTIMAS_N = 15


def cargar_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(f"No encuentro {CONFIG_PATH}. Crea el proyecto con init_proyecto.py.")
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("examen", {})
    cfg["examen"].setdefault("preguntas", 50)
    cfg["examen"].setdefault("umbral_pct", 70)
    return cfg


def leer_registro():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return [fila for fila in csv.DictReader(f)]


def pct(a, t):
    return (100.0 * a / t) if t else 0.0


def barra(p, ancho=20):
    llenos = int(round(p / 100 * ancho))
    return "█" * llenos + "░" * (ancho - llenos)


def reparto_simulacro(dominios, total):
    """Reparte `total` preguntas según pesos (método del resto mayor)."""
    suma = sum(d["peso"] for d in dominios) or 1
    exactos = [(d["cod"], total * d["peso"] / suma) for d in dominios]
    base = {cod: int(x) for cod, x in exactos}
    faltan = total - sum(base.values())
    for cod, x in sorted(exactos, key=lambda e: e[1] - int(e[1]), reverse=True)[:faltan]:
        base[cod] += 1
    return base


def siguientes_ids(dominios, filas):
    """Siguiente número libre por dominio, mirando registro.csv y banco.md."""
    maximo = {d["cod"]: 0 for d in dominios}
    patron = re.compile(r"\b([A-Z]\d+)-(\d{3,})\b")
    textos = [f.get("id_pregunta", "") for f in filas]
    if os.path.exists(BANCO_PATH):
        with open(BANCO_PATH, encoding="utf-8") as f:
            textos += [l for l in f if l.startswith("### ")]
    for t in textos:
        for cod, num in patron.findall(t):
            if cod in maximo:
                maximo[cod] = max(maximo[cod], int(num))
    return {cod: f"{cod}-{n + 1:03d}" for cod, n in maximo.items()}


def calcular(cfg, filas):
    dominios = cfg["dominios"]
    umbral = cfg["examen"]["umbral_pct"]
    total = len(filas)
    aciertos = sum(1 for f in filas if f.get("correcta") == "1")

    por_dom = {}
    for d in dominios:
        sub = [f for f in filas if f.get("seccion") == d["cod"]]
        por_dom[d["cod"]] = (sum(1 for f in sub if f.get("correcta") == "1"), len(sub))

    peso_cub, ponderado = 0, 0.0
    for d in dominios:
        a, t = por_dom[d["cod"]]
        if t:
            ponderado += pct(a, t) * d["peso"]
            peso_cub += d["peso"]
    prep = ponderado / peso_cub if peso_cub else 0.0

    # Subtemas con fallos (para orientar tandas)
    subtemas = {}
    for f in filas:
        clave = (f.get("seccion", ""), f.get("subtema", ""))
        a, t = subtemas.get(clave, (0, 0))
        subtemas[clave] = (a + (f.get("correcta") == "1"), t + 1)
    sub_debiles = sorted(
        [(s, n, a, t) for (s, n), (a, t) in subtemas.items() if t >= 2 and pct(a, t) < umbral],
        key=lambda x: pct(x[2], x[3]),
    )

    ultimas = filas[-ULTIMAS_N:]
    # Racha actual de aciertos
    racha = 0
    for f in reversed(filas):
        if f.get("correcta") != "1":
            break
        racha += 1

    return {
        "certificacion": cfg.get("nombre", ""),
        "codigo": cfg.get("codigo", ""),
        "umbral": umbral,
        "total": total,
        "aciertos": aciertos,
        "global_pct": pct(aciertos, total),
        "por_dominio": {
            d["cod"]: {"nombre": d["nombre"], "peso": d["peso"],
                       "aciertos": por_dom[d["cod"]][0], "total": por_dom[d["cod"]][1],
                       "pct": pct(*por_dom[d["cod"]])}
            for d in dominios
        },
        "preparacion": prep,
        "peso_cubierto": peso_cub,
        "tendencia": {"aciertos": sum(1 for f in ultimas if f.get("correcta") == "1"),
                      "total": len(ultimas)},
        "racha": racha,
        "subtemas_debiles": [{"seccion": s, "subtema": n, "aciertos": a, "total": t}
                             for s, n, a, t in sub_debiles],
        "siguientes_ids": siguientes_ids(dominios, filas),
        "reparto_simulacro": reparto_simulacro(dominios, cfg["examen"]["preguntas"]),
        "fecha_examen": cfg.get("fecha_examen"),
    }


def render(cfg, d):
    L = [f"# 📊 Progreso — {d['codigo'] or d['certificacion']}", "",
         f"_Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M')}_", ""]
    if d["fecha_examen"]:
        try:
            dias = (datetime.strptime(d["fecha_examen"], "%Y-%m-%d") - datetime.now()).days + 1
            L += [f"🗓️ Examen: **{d['fecha_examen']}** ({dias} días)", ""]
        except ValueError:
            pass

    if d["total"] == 0:
        L += ["**Sin datos aún.** Responde tu primera ronda para empezar a medir.", "",
              "| Cód | Dominio | Peso |", "|-----|---------|------|"]
        L += [f"| {c} | {v['nombre']} | {v['peso']}% |" for c, v in d["por_dominio"].items()]
        return "\n".join(L)

    g, u = d["global_pct"], d["umbral"]
    L += [f"## Global: **{d['aciertos']}/{d['total']} = {g:.1f}%**", "", f"`{barra(g)}` {g:.1f}%", "",
          "## Acierto por dominio", "",
          "| Cód | Dominio | Peso | Respondidas | Acierto | | Estado |",
          "|-----|---------|------|-------------|---------|--|--------|"]
    for c, v in d["por_dominio"].items():
        if v["total"] == 0:
            L.append(f"| {c} | {v['nombre']} | {v['peso']}% | 0 | — | | ⚪ sin datos |")
        else:
            estado = "🟢 OK" if v["pct"] >= u else "🔴 reforzar"
            L.append(f"| {c} | {v['nombre']} | {v['peso']}% | {v['aciertos']}/{v['total']} | "
                     f"{v['pct']:.0f}% | `{barra(v['pct'], 12)}` | {estado} |")
    L.append("")

    p = d["preparacion"]
    nota = f" _(solo {d['peso_cubierto']}% del temario con datos)_" if d["peso_cubierto"] < 100 else ""
    veredicto = "✅ en zona de aprobado" if p >= u else "⚠️ aún por debajo del objetivo"
    L += [f"## Preparación estimada (ponderada): **{p:.1f}%** — {veredicto}{nota}", "",
          f"> Umbral orientativo: ~{u}%. Con margen real conviene estar ≥ {min(u + 15, 95)}% antes del examen.", ""]

    t = d["tendencia"]
    L += [f"## Tendencia (últimas {t['total']}): {t['aciertos']}/{t['total']} = "
          f"{pct(t['aciertos'], t['total']):.0f}% · racha actual: {d['racha']} ✅", ""]

    L += ["## 🎯 Zonas a reforzar", ""]
    debiles = sorted([(c, v) for c, v in d["por_dominio"].items() if v["total"] and v["pct"] < u],
                     key=lambda x: x[1]["pct"])
    if debiles:
        L += [f"- **{c} {v['nombre']}** — {v['pct']:.0f}%" for c, v in debiles]
    else:
        # Sin dominios bajo umbral: señala el más flojo para seguir subiendo
        con_datos = [(c, v) for c, v in d["por_dominio"].items() if v["total"]]
        c, v = min(con_datos, key=lambda x: x[1]["pct"])
        L.append(f"Ningún dominio bajo el umbral. El más flojo: **{c} {v['nombre']}** ({v['pct']:.0f}%).")
    if d["subtemas_debiles"]:
        L += ["", "**Subtemas con fallos recurrentes** (≥2 preguntas, bajo umbral):", ""]
        L += [f"- {s['seccion']} · {s['subtema']} — {s['aciertos']}/{s['total']}"
              for s in d["subtemas_debiles"][:8]]
    L.append("")

    ids = ", ".join(d["siguientes_ids"].values())
    rep = " · ".join(f"{c} {n}" for c, n in d["reparto_simulacro"].items())
    L += [f"**Siguientes IDs:** {ids}", "",
          f"**Reparto de un simulacro de {cfg['examen']['preguntas']}:** {rep}"]
    return "\n".join(L)


def main():
    cfg = cargar_config()
    filas = leer_registro()
    datos = calcular(cfg, filas)
    args = set(sys.argv[1:])

    if "--json" in args:
        print(json.dumps(datos, ensure_ascii=False, indent=2))
        return
    if "--ids" in args:
        print(", ".join(datos["siguientes_ids"].values()))
        return
    if "--simulacro" in args:
        print(" · ".join(f"{c} {n}" for c, n in datos["reparto_simulacro"].items()))
        return
    if "--fallos" in args:
        fallos = [f for f in filas if f.get("correcta") == "0"]
        for f in fallos:
            print(f"{f['fecha']}  {f['id_pregunta']:<8} {f['seccion']}  elegida {f.get('elegida', ''):<6} {f['subtema']}")
        print(f"\nTotal falladas: {len(fallos)}")
        return

    salida = render(cfg, datos)
    print(salida)
    os.makedirs(os.path.dirname(DASHBOARD_PATH), exist_ok=True)
    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(salida + "\n")


if __name__ == "__main__":
    main()
