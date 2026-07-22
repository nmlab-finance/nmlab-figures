#!/usr/bin/env python3
"""Boîte à outils autonome pour générer les notebooks d'UN chapitre (parallélisable).

Un script de chapitre importe ce module, définit ``META`` + une liste ``FIGURES``,
puis appelle ``test_all(...)`` (rend les PNG pour comparaison visuelle) et
``build_all(...)`` (écrit les .ipynb dans le miroir). Chaque script travaille sur
son propre dossier et ses propres fichiers → plusieurs chapitres tournent en
parallèle sans conflit. Convention : une seule cellule code par notebook,
fonctions typées + docstrings (voir les blocs ch18/19/20 de build_notebooks.py).

Un ``FIGURES`` est une liste de dicts :
    dict(name="fig01-slug", fig_fr="Titre H1 fr", fig_en="H1 en",
         data=DATA_STR, fig=FIG_STR, live=True|False, source=("… fr", "… en"))
``META`` = dict(num="12", title_fr=…, title_en=…, slug_fr=…, slug_en=…).
"""

import json
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(TOOLS, "..", "nmlab-figures")
RAW = "https://raw.githubusercontent.com/nmlab-finance/nmlab-figures/main/nmlab_style.py"

SETUP = f'''LANG = "fr"   # "fr" ou "en" — langue des libellés / label language

# Récupère puis active le style partagé NMLab (thème sombre + police Inter).
# Fetch and activate the shared NMLab style (dark theme + Inter font).
import urllib.request

urllib.request.urlretrieve("{RAW}", "nmlab_style.py")
import nmlab_style as nm

nm.setup()'''


def intro_md(meta, fig_fr, fig_en, live=True, source=None):
    art_fr = f"https://nmlab.io/ressources/{meta['slug_fr']}"
    art_en = f"https://nmlab.io/en/ressources/{meta['slug_en']}"
    if source:                                        # données réelles non-FRED (ex. Shiller)
        run_fr = f"la figure se régénère à partir des **{source[0]}**"
        run_en = f"rebuild the figure from **{source[1]}**"
    elif live:
        run_fr = "la figure se régénère avec les **données FRED du jour**"
        run_en = "rebuild the figure with **today's FRED data**"
    else:
        run_fr = "la figure est régénérée par le code — un **schéma éditable** : changez les libellés à votre guise"
        run_en = "rebuild the figure from code — an **editable diagram**: change the labels as you like"
    return f"""# {fig_fr} · *{fig_en}*

Notebook compagnon du chapitre **{meta['num']}. {meta['title_fr']}** — [lire l'article]({art_fr}).
Companion notebook to chapter **{meta['num']}. {meta['title_en']}** — [read the article]({art_en}).

**Exécutez l'unique cellule ci-dessous** (bouton ▶ ou Ctrl+Entrée) : {run_fr}. Passez `LANG = "en"` en tête de cellule pour les libellés anglais. — Run the single cell below (▶ or Ctrl+Enter) to {run_en}; set `LANG = "en"` at the top for English labels.

Code : licence MIT · © 2026 [NMLab](https://nmlab.io) · dépôt [nmlab-finance/nmlab-figures](https://github.com/nmlab-finance/nmlab-figures)"""


def _as_cell(kind, src):
    cell = {"cell_type": kind, "metadata": {}, "source": src.splitlines(keepends=True)}
    if kind == "code":
        cell.update(execution_count=None, outputs=[])
    return cell


def build_all(meta, dir_rel, figures):
    """Écrit les .ipynb du chapitre dans le miroir ; renvoie les chemins relatifs écrits."""
    written = []
    for f in figures:
        intro = intro_md(meta, f["fig_fr"], f["fig_en"], f.get("live", True), f.get("source"))
        rel = f"{dir_rel}/{f['name']}.ipynb"
        path = os.path.join(REPO, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        nb = {
            "nbformat": 4, "nbformat_minor": 5,
            "metadata": {"colab": {"provenance": []},
                         "kernelspec": {"name": "python3", "display_name": "Python 3"},
                         "language_info": {"name": "python"}},
            "cells": [_as_cell("markdown", intro),
                      _as_cell("code", "\n\n\n".join([SETUP, f["data"], f["fig"]]))],
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(nb, fh, ensure_ascii=False, indent=1)
        written.append(rel)
        print("écrit", rel)
    return written


def test_all(figures, out_dir):
    """Rend chaque figure (fr+en) en PNG dans ``out_dir`` — pour comparaison aux WebP."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import sys
    import urllib.request as _ur
    _real = _ur.urlretrieve
    _ur.urlretrieve = (lambda url, fn=None, *a, **k:
                       (fn, None) if "nmlab_style" in str(url) else _real(url, fn, *a, **k))
    if REPO not in sys.path:
        sys.path.insert(0, REPO)
    cwd = os.getcwd()
    out_abs = os.path.abspath(out_dir)
    os.makedirs(out_abs, exist_ok=True)
    os.chdir(REPO)                                     # nmlab_style.py locale
    try:
        for f in figures:
            for lang in ("fr", "en"):
                plt.close("all")
                ns = {}
                src = "\n\n\n".join([SETUP, f["data"], f["fig"]]).replace('LANG = "fr"', f'LANG = "{lang}"', 1)
                exec(compile(src, f"{f['name']}[{lang}]", "exec"), ns)
                png = os.path.join(out_abs, f"{f['name']}-{lang}.png")
                plt.gcf().savefig(png)
                print("rendu", png)
    finally:
        os.chdir(cwd)
