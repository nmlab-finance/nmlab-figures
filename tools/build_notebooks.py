#!/usr/bin/env python3
"""Génère les .ipynb du dépôt nmlab-figures (source unique des cellules).

  build_notebooks.py          → écrit les .ipynb dans ../nmlab-figures/
  build_notebooks.py --test   → exécute les cellules code (fr+en), PNG dans ./out/

Convention des notebooks (style « strict ») : une seule cellule code, structurée
en fonctions typées et documentées — ``load_*()`` charge les données (série FRED
en direct, ou points embarqués pour un schéma) et ``build_figure(...) -> Figure``
construit la figure. Le module partagé ``nmlab_style`` porte le design system.
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


# ── Cellule d'introduction (markdown) ────────────────────────────────────────

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


# ── Amorce commune : récupère et active le style partagé ──────────────────────

SETUP = f'''LANG = "fr"   # "fr" ou "en" — langue des libellés / label language

# Récupère puis active le style partagé NMLab (thème sombre + police Inter).
# Fetch and activate the shared NMLab style (dark theme + Inter font).
import urllib.request

urllib.request.urlretrieve("{RAW}", "nmlab_style.py")
import nmlab_style as nm

nm.setup()'''


# ── Figure 01 — croissance du catalogue FRED (données embarquées) ─────────────

DATA_01 = '''def load_catalog() -> tuple[list[int], list[int]]:
    """Jalons du catalogue FRED (valeurs approchées) — source : « The History of FRED »,
    Federal Reserve Bank of St. Louis. / FRED catalog milestones (approximate)."""
    years = [1991, 1993, 1995, 2004, 2016, 2021, 2026]
    series_count = [30, 300, 860, 2900, 384_000, 780_000, 845_000]
    return years, series_count

years, series_count = load_catalog()'''

FIG_01 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="De 30 séries par modem à 845 000",
        sub="Le catalogue de FRED depuis sa naissance, le 18 avril 1991",
        ylab="nombre de séries (échelle log)",
        milestone_1991="30 séries,\\npar modem\\n(1991)",
        milestone_2026="≈ 845 000 séries,\\n121 sources (2026)",
        note="FRED a débuté comme un serveur télématique en accès libre — 620 utilisateurs, une heure par jour. C'est\\n"
             "aujourd'hui l'entrepôt de données le plus utilisé au monde. Source : Federal Reserve Bank of St. Louis."),
    "en": dict(
        title="From 30 series by modem to 845,000",
        sub="FRED's catalog since its birth, April 18, 1991",
        ylab="number of series (log scale)",
        milestone_1991="30 series,\\nby modem\\n(1991)",
        milestone_2026="≈ 845,000 series,\\n121 sources (2026)",
        note="FRED began as a free dial-up bulletin board — 620 users, one hour a day. It is today the most-used data\\n"
             "warehouse in the world. Source: Federal Reserve Bank of St. Louis."),
}

def build_figure(years: list[int], series_count: list[int], lang: str) -> Figure:
    """Croissance du catalogue FRED, en échelle logarithmique."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.137)
    ax.plot(years, series_count, color=nm.COLORS["blue"], linewidth=3.6,
            marker="o", markersize=13, clip_on=False, zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(20, 2_000_000)
    ax.set_yticks([100, 1_000, 10_000, 100_000, 1_000_000])
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.tick_params(which="minor", left=False)
    ax.grid(which="minor", visible=False)
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(1989.5, 2027.5)
    ax.set_xticks(range(1990, 2030, 5))
    ax.annotate(text["milestone_2026"], xy=(2025.6, 845_000), xytext=(2010.5, 480_000),
                ha="center", va="center", fontsize=23, fontweight="bold",
                color=nm.COLORS["blue2"], linespacing=1.55,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["blue2"], lw=1.8))
    ax.text(0.143, 0.22, text["milestone_1991"], transform=ax.transAxes, fontsize=21.5,
            color=nm.COLORS["muted"], va="top", linespacing=1.4)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(years, series_count, LANG)'''


# ── Figure 02 — chômage + bandes de récession NBER (FRED en direct) ───────────

DATA_02 = '''from pandas import Series

def load_data() -> tuple[Series, Series]:
    """Taux de chômage (UNRATE) et indicateur de récession NBER (USREC), en direct de FRED.
    Unemployment rate and NBER recession flag, live from FRED."""
    unemployment = nm.load_fred("UNRATE")
    recessions = nm.load_fred("USREC", start=str(unemployment.index[0].year))
    return unemployment, recessions

unemployment, recessions = load_data()'''

FIG_02 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
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
}

def build_figure(unemployment: Series, recessions: Series, lang: str) -> Figure:
    """Chômage sur toute la période, ombré des récessions du NBER."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig)

    # Ombrer chaque période de récession (suites contiguës où USREC == 1).
    # Shade each recession (contiguous runs where USREC == 1).
    runs = recessions.ne(recessions.shift()).cumsum()
    for _, run in recessions.groupby(runs):
        if run.iloc[0] == 1:
            ax.axvspan(run.index[0], run.index[-1], color=nm.COLORS["edge"], alpha=0.75, linewidth=0)

    ax.plot(unemployment.index, unemployment, color=nm.COLORS["blue"], linewidth=2.9)
    ax.set_ylim(0, 15.5)
    ax.set_yticks(range(0, 15, 2))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.012)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.text(0.085, 0.70, text["bands"], transform=ax.transAxes, fontsize=21.5,
            color=nm.COLORS["muted"], linespacing=1.55)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(unemployment, recessions, LANG)'''


# ── Figure 03 — IPC : niveau vs variation sur un an (FRED en direct) ──────────

DATA_03 = '''from pandas import Series

def load_prices() -> tuple[Series, Series]:
    """Indice des prix (IPC) et son glissement annuel — l'inflation — depuis 1995.
    Consumer price index and its year-over-year change (inflation), since 1995."""
    cpi = nm.load_fred("CPIAUCSL").loc["1995":]
    inflation = (cpi / cpi.shift(12) - 1) * 100
    return cpi, inflation

cpi, inflation = load_prices()
print(f"Dernier point / latest: {inflation.index[-1]:%Y-%m} → {inflation.iloc[-1]:.1f} %")'''

FIG_03 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
             "août", "septembre", "octobre", "novembre", "décembre"]

LABELS = {
    "fr": dict(
        title="La même série, deux histoires",
        sub="Un menu déroulant transforme un niveau en taux d'inflation",
        y1="« Niveau »", y2="« Variation sur un an », %",
        cpi_label="l'indice des prix (IPC)", target="cible 2 %"),
    "en": dict(
        title="The same series, two stories",
        sub="One dropdown turns a level into an inflation rate",
        y1="« Level »", y2="« Change from year ago », %",
        cpi_label="the price index (CPI)", target="2% target"),
}

def caption(inflation: Series, lang: str) -> str:
    """Note interne dynamique : le dernier point d'inflation, dans la langue voulue."""
    latest, when = inflation.iloc[-1], inflation.index[-1]
    if lang == "fr":
        value = f"{latest:.1f}".replace(".", ",")
        return ("Le même indice des prix, vu comme « Niveau » (en haut) puis comme « Variation sur un an » (en bas) : c'est\\n"
                f"ainsi qu'on lit l'inflation, à {value} % en {MONTHS_FR[when.month - 1]} {when.year} (dernier point). Source : BLS via FRED (CPIAUCSL).")
    return ("The same price index, seen as « Level » (top) then as « Change from year ago » (bottom): that is how you\\n"
            f"read inflation, at {latest:.1f}% in {when:%B %Y} (latest point). Source: BLS via FRED (CPIAUCSL).")

def build_figure(cpi: Series, inflation: Series, lang: str) -> Figure:
    """Deux panneaux : le niveau de l'IPC (haut) puis sa variation annuelle (bas)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    top = fig.add_axes([0.075, 0.553, 0.907, 0.225])
    bottom = fig.add_axes([0.075, 0.140, 0.907, 0.307])

    top.plot(cpi.index, cpi, color=nm.COLORS["blue"], linewidth=3.2)
    top.set_ylabel(text["y1"])
    top.set_yticks([200, 300])
    top.text(0.065, 0.80, text["cpi_label"], transform=top.transAxes, fontsize=21.5, color=nm.COLORS["muted"])
    top.tick_params(labelbottom=False)

    bottom.plot(inflation.index, inflation, color=nm.COLORS["rose"], linewidth=3.2)
    bottom.axhline(2, color=nm.COLORS["amber"], linestyle=(0, (6, 4)), linewidth=2.6)
    bottom.axhline(0, color=nm.COLORS["muted"], linewidth=1.6, alpha=0.9)
    bottom.set_ylabel(text["y2"])
    bottom.set_yticks(range(-2, 9, 2))
    bottom.text(0.065, 0.80, text["target"], transform=bottom.transAxes, fontsize=21.5,
                fontweight="bold", color=nm.COLORS["amber"])

    for ax in (top, bottom):
        ax.set_xlim(cpi.index[0], cpi.index[-1])
        ax.margins(x=0.012)
        ax.xaxis.set_major_locator(mdates.YearLocator(5))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, caption(inflation, lang))
    return fig

build_figure(cpi, inflation, LANG)'''


# ── Figure 04 — la trousse de départ (schéma) ────────────────────────────────

DATA_04 = '''def starter_kit(lang: str) -> list[tuple[str, str]]:
    """Les sept codes FRED de la trousse de départ et leur description localisée.
    The seven starter-kit FRED codes with their localized description."""
    codes = ["GDPC1", "CPIAUCSL", "UNRATE", "PAYEMS", "FEDFUNDS", "DGS10", "USREC"]
    descriptions = {
        "fr": ["PIB réel", "indice des prix → inflation", "taux de chômage",
               "emploi salarié non agricole", "taux directeur de la Fed",
               "taux à 10 ans", "récessions (NBER)"],
        "en": ["real GDP", "price index → inflation", "unemployment rate",
               "nonfarm payroll employment", "Fed policy rate",
               "10-year yield", "recessions (NBER)"],
    }
    return list(zip(codes, descriptions[lang]))'''

FIG_04 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="La trousse de départ du macro-observateur",
               sub="Sept codes FRED à mettre en favori — l'essentiel d'une économie"),
    "en": dict(title="The macro-watcher's starter kit",
               sub="Seven FRED codes to bookmark — the essentials of an economy"),
}

def build_figure(rows: list[tuple[str, str]], lang: str) -> Figure:
    """Schéma : sept encadrés « code → description »."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    ax = nm.blank_axes(fig)

    top, card_h, gap = 930, 96, 26          # haut du 1er encadré, hauteur, écart (px)
    card_x, card_w = 100, 470
    for i, (code, description) in enumerate(rows):
        card_top = top - i * (card_h + gap)
        nm.card(ax, card_x, card_top - card_h, card_w, card_h, edge=nm.COLORS["blue"])
        ax.text(card_x + card_w / 2, card_top - card_h / 2, code, ha="center", va="center",
                family="monospace", fontsize=30, fontweight="bold", color=nm.COLORS["blue"])
        ax.text(640, card_top - card_h / 2, description, ha="left", va="center",
                fontsize=29, color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig)
    return fig

build_figure(starter_kit(LANG), LANG)'''


# ── Figure 05 — les cousins de FRED (schéma) ─────────────────────────────────

DATA_05 = '''def cousins(lang: str) -> list[tuple[str, str, list[str]]]:
    """Les trois familles de « cousins » de FRED : (nom, couleur, entrées), localisées.
    The three families of FRED cousins: (name, color, entries), localized."""
    if lang == "fr":
        return [
            ("Famille FRED", nm.COLORS["blue"],
             ["ALFRED — les millésimes", "FRASER — les archives", "API + module Excel"]),
            ("Europe", nm.COLORS["amber"],
             ["Eurostat Data Browser", "Portail de données BCE", "INSEE (BDM) · Webstat"]),
            ("International", nm.COLORS["rose"],
             ["OECD Data Explorer", "Banque mondiale", "FMI (Data Portal)"]),
        ]
    return [
        ("FRED family", nm.COLORS["blue"],
         ["ALFRED — the vintages", "FRASER — the archives", "API + Excel add-in"]),
        ("Europe", nm.COLORS["amber"],
         ["Eurostat Data Browser", "ECB Data Portal", "INSEE (BDM) · Webstat"]),
        ("International", nm.COLORS["rose"],
         ["OECD Data Explorer", "World Bank Open Data", "IMF Data Portal"]),
    ]'''

FIG_05 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="FRED n'est pas seul : ses cousins",
               sub="Où trouver les données quand elles ne sont pas américaines"),
    "en": dict(title="FRED is not alone: its cousins",
               sub="Where to find the data when it isn't American"),
}

def build_figure(cards: list[tuple[str, str, list[str]]], lang: str) -> Figure:
    """Schéma : trois cartes régionales (famille FRED, Europe, international)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1007)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 486, 94, 55
    top, bottom = 737, 177                  # bords haut / bas des cartes (px)
    for i, (name, color, lines) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        center_x = x + card_w / 2
        nm.card(ax, x, bottom, card_w, top - bottom, edge=color, lw=2.6, radius=24)
        ax.text(center_x, top - 58, name, ha="center", va="center",
                fontsize=31, fontweight="bold", color=color)
        for j, line in enumerate(lines):
            ax.text(center_x, 495 - j * 47, line, ha="center", va="center",
                    fontsize=26, color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig)
    return fig

build_figure(cousins(LANG), LANG)'''


# ── Gabarit pour les prochaines figures ──────────────────────────────────────

TEMPLATE_MD = """# Gabarit de figure NMLab · *NMLab figure template*

Copiez ce notebook pour créer une figure. Une seule cellule code : ``load_data()`` (série FRED en direct
ou points embarqués) puis ``build_figure(...) -> Figure``.
Copy this notebook to create a figure. A single code cell: ``load_data()`` (a live FRED series or embedded
points) then ``build_figure(...) -> Figure``.

Code : licence MIT · © 2026 [NMLab](https://nmlab.io)"""

TEMPLATE_DATA = '''import pandas as pd
from pandas import Series

def load_data() -> Series:
    """Charge les données de la figure. Pour une série FRED en direct :
    Load the figure's data. For a live FRED series:
        return nm.load_fred("GDPC1", start="2000")
    Pour une figure non-FRED, embarquez les points ici (schéma éditable).
    For a non-FRED figure, embed the points here (editable diagram)."""
    return pd.Series([2.1, 2.4, 2.9, 2.6, 3.1, 3.6, 3.4, 3.9],
                     index=pd.date_range("2019", periods=8, freq="YS"))'''

TEMPLATE_FIG = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Titre de la figure", sub="Sous-titre explicatif",
               ylab="unité, %", note="Note interne : lecture de la figure. Source : à préciser."),
    "en": dict(title="Figure title", sub="Explanatory subtitle",
               ylab="unit, %", note="Internal note: how to read the figure. Source: to fill in."),
}

def build_figure(data: Series, lang: str) -> Figure:
    """Construit la figure dans la langue voulue."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)      # 1045 = simple ; 1140 = deux panneaux
    ax = nm.axes(fig)
    ax.plot(data.index, data, color=nm.COLORS["blue"])
    ax.set_ylabel(text["ylab"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(load_data(), LANG)'''


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
