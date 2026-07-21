#!/usr/bin/env python3
"""Génère les .ipynb du dépôt nmlab-figures (source unique des cellules).

  build_notebooks.py          → écrit les .ipynb dans ../nmlab-figures/
  build_notebooks.py --test   → exécute les cellules code (fr+en), PNG dans ./out/
"""

import json
import os
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(TOOLS, "..", "nmlab-figures")
NB_DIR = "macro/18-atelier-donnees-fred"
RAW = "https://raw.githubusercontent.com/nmlab-finance/nmlab-figures/main/nmlab_style.py"

ARTICLE_FR = "https://nmlab.io/ressources/atelier-donnees-decouvrir-fred"
ARTICLE_EN = "https://nmlab.io/en/ressources/data-workshop-discovering-fred"

# ── Cellules communes ────────────────────────────────────────────────────────

def intro_md(title_fr, title_en, live=True):
    run_fr = ("la figure se régénère avec les **données FRED du jour**" if live
              else "la figure est régénérée par le code — un **schéma éditable** : changez les libellés à votre guise")
    run_en = ("rebuild the figure with **today's FRED data**" if live
              else "rebuild the figure from code — an **editable diagram**: change the labels as you like")
    return f"""# {title_fr} · *{title_en}*

Notebook compagnon du chapitre **18. Atelier données : découvrir FRED, l'entrepôt de la Réserve fédérale** — [lire l'article]({ARTICLE_FR}).
Companion notebook to chapter **18. Data Workshop: Discovering FRED** — [read the article]({ARTICLE_EN}).

**Exécutez l'unique cellule ci-dessous** (bouton ▶ ou Ctrl+Entrée) : {run_fr}. Passez `LANG = "en"` en tête de cellule pour les libellés anglais. — Run the single cell below (▶ or Ctrl+Enter) to {run_en}; set `LANG = "en"` at the top for English labels.

Code : licence MIT · © 2026 [NMLab](https://nmlab.io) · dépôt [nmlab-finance/nmlab-figures](https://github.com/nmlab-finance/nmlab-figures)"""


SETUP = f'''LANG = "fr"   # "en" → libellés anglais / English labels

# Style NMLab (thème sombre + police Inter) / NMLab style (dark theme + Inter font)
import urllib.request
urllib.request.urlretrieve("{RAW}", "nmlab_style.py")
import nmlab_style as nm
nm.setup()'''


# ── Figure 01 — croissance du catalogue FRED ─────────────────────────────────

DATA_01 = '''# Jalons du catalogue FRED — source : « The History of FRED », Federal Reserve Bank
# of St. Louis (valeurs approchées). / FRED catalog milestones (approximate).
years  = [1991, 1993, 1995, 2004, 2016, 2021, 2026]
series = [30,   300,  860,  2900, 384_000, 780_000, 845_000]'''

FIG_01 = '''L = {
    "fr": dict(
        title="De 30 séries par modem à 845 000",
        sub="Le catalogue de FRED depuis sa naissance, le 18 avril 1991",
        ylab="nombre de séries (échelle log)",
        a1991="30 séries,\\npar modem\\n(1991)",
        a2026="≈ 845 000 séries,\\n121 sources (2026)",
        note="FRED a débuté comme un serveur télématique en accès libre — 620 utilisateurs, une heure par jour. C'est\\n"
             "aujourd'hui l'entrepôt de données le plus utilisé au monde. Source : Federal Reserve Bank of St. Louis."),
    "en": dict(
        title="From 30 series by modem to 845,000",
        sub="FRED's catalog since its birth, April 18, 1991",
        ylab="number of series (log scale)",
        a1991="30 series,\\nby modem\\n(1991)",
        a2026="≈ 845,000 series,\\n121 sources (2026)",
        note="FRED began as a free dial-up bulletin board — 620 users, one hour a day. It is today the most-used data\\n"
             "warehouse in the world. Source: Federal Reserve Bank of St. Louis."),
}[LANG]

fig = nm.figure(height_px=1045)
ax = nm.axes(fig, left=0.137)
ax.plot(years, series, color=nm.COLORS["blue"], linewidth=3.6,
        marker="o", markersize=13, clip_on=False, zorder=3)
ax.set_yscale("log")
ax.set_ylim(20, 2_000_000)
ax.set_yticks([100, 1_000, 10_000, 100_000, 1_000_000])
ax.yaxis.set_major_formatter(nm.thousands(LANG))
ax.tick_params(which="minor", left=False)
ax.grid(which="minor", visible=False)
ax.set_ylabel(L["ylab"])
ax.set_xlim(1989.5, 2027.5)
ax.set_xticks(range(1990, 2030, 5))
ax.annotate(L["a2026"], xy=(2025.6, 845_000), xytext=(2010.5, 480_000),
            ha="center", va="center", fontsize=23, fontweight="bold",
            color=nm.COLORS["blue2"], linespacing=1.55,
            arrowprops=dict(arrowstyle="->", color=nm.COLORS["blue2"], lw=1.8))
ax.text(0.143, 0.22, L["a1991"], transform=ax.transAxes, fontsize=21.5,
        color=nm.COLORS["muted"], va="top", linespacing=1.4)
nm.header(fig, L["title"], L["sub"])
nm.footer(fig, L["note"])'''


# ── Figure 02 — chômage + bandes de récession NBER ───────────────────────────

DATA_02 = '''import pandas as pd

# Données FRED en direct (CSV public, sans clé API) / live FRED data (no API key)
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
unrate = pd.read_csv(FRED + "UNRATE", index_col="observation_date", parse_dates=True)["UNRATE"]
usrec  = pd.read_csv(FRED + "USREC",  index_col="observation_date", parse_dates=True)["USREC"]
usrec  = usrec.loc[unrate.index.min():]   # même fenêtre que le chômage / same window
unrate.tail()'''

FIG_02 = '''L = {
    "fr": dict(
        title="Ce que vous saurez fabriquer en trois clics",
        sub="Taux de chômage américain, avec les récessions du NBER — un graphique FRED type",
        ylab="taux de chômage, %",
        bands="bandes grises =\\nrécessions (NBER)",
        note="Une série, une case « bandes de récession » à cocher, et l'histoire du cycle apparaît. Chaque pic de chômage\\n"
             "épouse une bande grise. Source : BLS et NBER via FRED (UNRATE, USREC)."),
    "en": dict(
        title="What you'll be able to make in three clicks",
        sub="U.S. unemployment rate, with NBER recessions — a typical FRED chart",
        ylab="unemployment rate, %",
        bands="grey bands =\\nrecessions (NBER)",
        note="One series, one « recession bars » box to tick, and the history of the cycle appears. Every unemployment\\n"
             "peak hugs a grey band. Source: BLS and NBER via FRED (UNRATE, USREC)."),
}[LANG]

import matplotlib.dates as mdates

fig = nm.figure(height_px=1045)
ax = nm.axes(fig)

# Chaque période contiguë où USREC == 1 devient une bande grise
# / each contiguous run of USREC == 1 becomes a grey band
runs = usrec.ne(usrec.shift()).cumsum()
for _, seg in usrec.groupby(runs):
    if seg.iloc[0] == 1:
        ax.axvspan(seg.index[0], seg.index[-1], color=nm.COLORS["edge"],
                   alpha=0.75, linewidth=0)

ax.plot(unrate.index, unrate, color=nm.COLORS["blue"], linewidth=2.9)
ax.set_ylim(0, 15.5)
ax.set_yticks(range(0, 15, 2))
ax.set_ylabel(L["ylab"])
ax.margins(x=0.012)
ax.xaxis.set_major_locator(mdates.YearLocator(10))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.text(0.085, 0.70, L["bands"], transform=ax.transAxes, fontsize=21.5,
        color=nm.COLORS["muted"], linespacing=1.55)
nm.header(fig, L["title"], L["sub"])
nm.footer(fig, L["note"])'''


# ── Figure 03 — IPC : niveau vs variation sur un an ──────────────────────────

DATA_03 = '''import pandas as pd

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
cpi = pd.read_csv(FRED + "CPIAUCSL", index_col="observation_date", parse_dates=True)["CPIAUCSL"]

# « Variation sur un an » : la transformation qui change un niveau en inflation
# / "Change from year ago": the transformation that turns a level into inflation
infl = (cpi / cpi.shift(12) - 1) * 100

cpi, infl = cpi.loc["1995":], infl.loc["1995":]
print(f"Dernier point / latest: {infl.index[-1]:%Y-%m} → {infl.iloc[-1]:.1f} %")'''

FIG_03 = '''MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]
last, when = infl.iloc[-1], infl.index[-1]
last_fr = f"{last:.1f}".replace(".", ",")   # 3.5 → « 3,5 » pour la note française

L = {
    "fr": dict(
        title="La même série, deux histoires",
        sub="Un menu déroulant transforme un niveau en taux d'inflation",
        y1="« Niveau »", y2="« Variation sur un an », %",
        lab1="l'indice des prix (IPC)", target="cible 2 %",
        note="Le même indice des prix, vu comme « Niveau » (en haut) puis comme « Variation sur un an » (en bas) : c'est\\n"
             f"ainsi qu'on lit l'inflation, à {last_fr} % en {MOIS[when.month - 1]} {when.year} (dernier point). "
             "Source : BLS via FRED (CPIAUCSL)."),
    "en": dict(
        title="The same series, two stories",
        sub="One dropdown turns a level into an inflation rate",
        y1="« Level »", y2="« Change from year ago », %",
        lab1="the price index (CPI)", target="2% target",
        note="The same price index, seen as « Level » (top) then as « Change from year ago » (bottom): that is how you\\n"
             f"read inflation, at {last:.1f}% in {when:%B %Y} (latest point). Source: BLS via FRED (CPIAUCSL)."),
}[LANG]

import matplotlib.dates as mdates

fig = nm.figure(height_px=1140)
ax1 = fig.add_axes([0.075, 0.553, 0.907, 0.225])
ax2 = fig.add_axes([0.075, 0.140, 0.907, 0.307])

ax1.plot(cpi.index, cpi, color=nm.COLORS["blue"], linewidth=3.2)
ax1.set_ylabel(L["y1"])
ax1.set_yticks([200, 300])
ax1.text(0.065, 0.80, L["lab1"], transform=ax1.transAxes, fontsize=21.5,
         color=nm.COLORS["muted"])
ax1.tick_params(labelbottom=False)

ax2.plot(infl.index, infl, color=nm.COLORS["rose"], linewidth=3.2)
ax2.axhline(2, color=nm.COLORS["amber"], linestyle=(0, (6, 4)), linewidth=2.6)
ax2.axhline(0, color=nm.COLORS["muted"], linewidth=1.6, alpha=0.9)
ax2.set_ylabel(L["y2"])
ax2.set_yticks(range(-2, 9, 2))
ax2.text(0.065, 0.80, L["target"], transform=ax2.transAxes, fontsize=21.5,
         fontweight="bold", color=nm.COLORS["amber"])

for ax in (ax1, ax2):
    ax.set_xlim(cpi.index[0], cpi.index[-1])
    ax.margins(x=0.012)
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

nm.header(fig, L["title"], L["sub"])
nm.footer(fig, L["note"])'''


# ── Figure 04 — la trousse de départ (schéma) ────────────────────────────────

DATA_04 = '''# Les sept codes de la trousse de départ (fixes) / the seven starter-kit codes
CODES = ["GDPC1", "CPIAUCSL", "UNRATE", "PAYEMS", "FEDFUNDS", "DGS10", "USREC"]'''

FIG_04 = '''L = {
    "fr": dict(
        title="La trousse de départ du macro-observateur",
        sub="Sept codes FRED à mettre en favori — l'essentiel d'une économie",
        desc=["PIB réel", "indice des prix \\u2192 inflation", "taux de chômage",
              "emploi salarié non agricole", "taux directeur de la Fed",
              "taux à 10 ans", "récessions (NBER)"]),
    "en": dict(
        title="The macro-watcher's starter kit",
        sub="Seven FRED codes to bookmark — the essentials of an economy",
        desc=["real GDP", "price index \\u2192 inflation", "unemployment rate",
              "nonfarm payroll employment", "Fed policy rate",
              "10-year yield", "recessions (NBER)"]),
}[LANG]

fig = nm.figure(height_px=1140)
ax = nm.blank_axes(fig)

TOP, CH, GAP = 930, 96, 26            # haut du 1er encadré, hauteur, écart (px)
CARD_X, CARD_W = 100, 470
for i, (code, desc) in enumerate(zip(CODES, L["desc"])):
    top = TOP - i * (CH + GAP)
    nm.card(ax, CARD_X, top - CH, CARD_W, CH, edge=nm.COLORS["blue"])
    ax.text(CARD_X + CARD_W / 2, top - CH / 2, code, ha="center", va="center",
            family="monospace", fontsize=30, fontweight="bold", color=nm.COLORS["blue"])
    ax.text(640, top - CH / 2, desc, ha="left", va="center",
            fontsize=29, color=nm.COLORS["text"])

nm.header(fig, L["title"], L["sub"])
nm.footer(fig)'''


# ── Figure 05 — les cousins de FRED (schéma) ─────────────────────────────────

DATA_05 = '''# Schéma : rien à charger (les entrées vivent dans la cellule figure)
# Diagram: nothing to load (entries live in the figure cell)'''

FIG_05 = '''L = {
    "fr": dict(
        title="FRED n'est pas seul : ses cousins",
        sub="Où trouver les données quand elles ne sont pas américaines",
        cards=[
            ("Famille FRED", nm.COLORS["blue"],
             ["ALFRED — les millésimes", "FRASER — les archives", "API + module Excel"]),
            ("Europe", nm.COLORS["amber"],
             ["Eurostat Data Browser", "Portail de données BCE", "INSEE (BDM) \\u00b7 Webstat"]),
            ("International", nm.COLORS["rose"],
             ["OECD Data Explorer", "Banque mondiale", "FMI (Data Portal)"]),
        ]),
    "en": dict(
        title="FRED is not alone: its cousins",
        sub="Where to find the data when it isn't American",
        cards=[
            ("FRED family", nm.COLORS["blue"],
             ["ALFRED — the vintages", "FRASER — the archives", "API + Excel add-in"]),
            ("Europe", nm.COLORS["amber"],
             ["Eurostat Data Browser", "ECB Data Portal", "INSEE (BDM) \\u00b7 Webstat"]),
            ("International", nm.COLORS["rose"],
             ["OECD Data Explorer", "World Bank Open Data", "IMF Data Portal"]),
        ]),
}[LANG]

fig = nm.figure(height_px=1007)
ax = nm.blank_axes(fig)

CARD_W, GAP, X0 = 486, 94, 55
TOP, BOTTOM = 737, 177               # bords haut / bas des cartes (px)
for i, (name, color, lines) in enumerate(L["cards"]):
    x = X0 + i * (CARD_W + GAP)
    cx = x + CARD_W / 2
    nm.card(ax, x, BOTTOM, CARD_W, TOP - BOTTOM, edge=color, lw=2.6, radius=24)
    ax.text(cx, TOP - 58, name, ha="center", va="center",
            fontsize=31, fontweight="bold", color=color)
    for j, line in enumerate(lines):
        ax.text(cx, 495 - j * 47, line, ha="center", va="center",
                fontsize=26, color=nm.COLORS["text"])

nm.header(fig, L["title"], L["sub"])
nm.footer(fig)'''


# ── Gabarit pour les prochaines figures ──────────────────────────────────────

TEMPLATE_MD = """# Gabarit de figure NMLab · *NMLab figure template*

Copiez ce notebook pour créer une nouvelle figure. Une seule cellule code, trois sections : **1)** style, **2)** données, **3)** figure.
Copy this notebook to create a new figure. A single code cell, three sections: **1)** style, **2)** data, **3)** figure.

Code : licence MIT · © 2026 [NMLab](https://nmlab.io)"""

TEMPLATE_DATA = '''import pandas as pd

# Données de démonstration — remplacez par un vrai chargement (ex. CSV FRED) :
#   pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDPC1",
#               index_col="observation_date", parse_dates=True)
demo = pd.Series([2.1, 2.4, 2.9, 2.6, 3.1, 3.6, 3.4, 3.9],
                 index=pd.date_range("2019", periods=8, freq="YS"))'''

TEMPLATE_FIG = '''L = {
    "fr": dict(title="Titre de la figure", sub="Sous-titre explicatif",
               ylab="unité, %", note="Note interne : lecture de la figure. Source : à préciser."),
    "en": dict(title="Figure title", sub="Explanatory subtitle",
               ylab="unit, %", note="Internal note: how to read the figure. Source: to fill in."),
}[LANG]

fig = nm.figure(height_px=1045)      # 1045 = simple ; 1140 = deux panneaux
ax = nm.axes(fig)
ax.plot(demo.index, demo, color=nm.COLORS["blue"])
ax.set_ylabel(L["ylab"])
nm.header(fig, L["title"], L["sub"])
nm.footer(fig, L["note"])'''


# ── Assemblage ───────────────────────────────────────────────────────────────

NOTEBOOKS = {
    "templates/template-figure.ipynb": (
        TEMPLATE_MD,
        [SETUP, TEMPLATE_DATA, TEMPLATE_FIG],
    ),
    "fig01-croissance-fred.ipynb": (
        intro_md("De 30 séries par modem à 845 000", "From 30 series by modem to 845,000"),
        [SETUP, DATA_01, FIG_01],
    ),
    "fig02-recession-bands.ipynb": (
        intro_md("Ce que vous saurez fabriquer en trois clics",
                 "What you'll be able to make in three clicks"),
        [SETUP, DATA_02, FIG_02],
    ),
    "fig03-transformations.ipynb": (
        intro_md("La même série, deux histoires", "The same series, two stories"),
        [SETUP, DATA_03, FIG_03],
    ),
    "fig04-trousse-depart.ipynb": (
        intro_md("La trousse de départ du macro-observateur",
                 "The macro-watcher's starter kit", live=False),
        [SETUP, DATA_04, FIG_04],
    ),
    "fig05-cousins-fred.ipynb": (
        intro_md("FRED n'est pas seul : ses cousins", "FRED is not alone: its cousins",
                 live=False),
        [SETUP, DATA_05, FIG_05],
    ),
}


def as_cell(kind, src):
    cell = {"cell_type": kind, "metadata": {}, "source": src.splitlines(keepends=True)}
    if kind == "code":
        cell.update(execution_count=None, outputs=[])
    return cell


def build():
    for name, (intro, codes) in NOTEBOOKS.items():
        rel = name if "/" in name else f"{NB_DIR}/{name}"
        path = os.path.join(REPO, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        nb = {
            "nbformat": 4, "nbformat_minor": 5,
            "metadata": {
                "colab": {"provenance": []},
                "kernelspec": {"name": "python3", "display_name": "Python 3"},
                "language_info": {"name": "python"},
            },
            "cells": [as_cell("markdown", intro),
                      as_cell("code", "\n\n\n".join(codes))],   # une seule cellule code
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print("écrit", path)


def test():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import urllib.request as _ur
    _real = _ur.urlretrieve
    _ur.urlretrieve = (lambda url, fn=None, *a, **k:
                       (fn, None) if "nmlab_style" in str(url) else _real(url, fn, *a, **k))
    os.chdir(REPO)                                     # nmlab_style.py locale
    sys.path.insert(0, REPO)
    out = os.path.join(TOOLS, "out")
    os.makedirs(out, exist_ok=True)
    for name, (_, codes) in NOTEBOOKS.items():
        for lang in ("fr", "en"):
            plt.close("all")
            ns = {}
            src = "\n\n\n".join(codes).replace('LANG = "fr"', f'LANG = "{lang}"', 1)
            exec(compile(src, f"{name}[{lang}]", "exec"), ns)
            base = os.path.basename(name)
            png = os.path.join(out, base.replace(".ipynb", f"-{lang}.png"))
            plt.gcf().savefig(png)
            print("rendu", png)


if __name__ == "__main__":
    test() if "--test" in sys.argv else build()
