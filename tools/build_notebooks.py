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
RAW = "https://raw.githubusercontent.com/nmlab-finance/nmlab-figures/main/nmlab_style.py"

# Un chapitre = dossier de notebooks + méta pour la cellule d'introduction.
CHAPTERS = {
    "18": dict(
        dir="macro/18-atelier-donnees-fred",
        title_fr="Atelier données : découvrir FRED, l'entrepôt de la Réserve fédérale",
        title_en="Data Workshop: Discovering FRED, the Federal Reserve's Warehouse",
        slug_fr="atelier-donnees-decouvrir-fred",
        slug_en="data-workshop-discovering-fred"),
    "19": dict(
        dir="macro/19-premier-script-python",
        title_fr="Premier script Python : charger une série FRED et la tracer en dix lignes",
        title_en="Your First Python Script: Load a FRED Series and Plot It in Ten Lines",
        slug_fr="premier-script-python-fred",
        slug_en="first-python-script-fred"),
    "20": dict(
        dir="macro/20-croissance-deja-anticipee",
        title_fr="La croissance déjà anticipée : pourquoi elle est souvent dans les cours",
        title_en="Growth Already Anticipated: Why It's Often Already in the Price",
        slug_fr="croissance-deja-anticipee-dans-les-cours",
        slug_en="growth-already-priced-in"),
}


# ── Cellule d'introduction (markdown) ────────────────────────────────────────

def intro_md(chapter, fig_fr, fig_en, live=True, source=None):
    c = CHAPTERS[chapter]
    art_fr = f"https://nmlab.io/ressources/{c['slug_fr']}"
    art_en = f"https://nmlab.io/en/ressources/{c['slug_en']}"
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

Notebook compagnon du chapitre **{chapter}. {c['title_fr']}** — [lire l'article]({art_fr}).
Companion notebook to chapter **{chapter}. {c['title_en']}** — [read the article]({art_en}).

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


# ═════════════════════════════════════════════════════════════════════════════
# Chapitre 19 — Premier script Python
# ═════════════════════════════════════════════════════════════════════════════

# ── Figure 19.01 — PIB réel (GDPC1) en aire (FRED en direct) ──────────────────

DATA_19_01 = '''from pandas import Series

def load_gdp() -> Series:
    """PIB réel des États-Unis (GDPC1), en direct depuis FRED / U.S. real GDP, live from FRED."""
    return nm.load_fred("GDPC1")

gdp = load_gdp()'''

FIG_19_01 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Ce que produisent huit lignes de Python",
        sub="Le PIB réel des États-Unis (GDPC1), chargé depuis FRED et tracé",
        ylab="milliards de dollars de 2017"),
    "en": dict(
        title="What eight lines of Python produce",
        sub="U.S. real GDP (GDPC1), loaded from FRED and plotted",
        ylab="billions of 2017 dollars"),
}

def caption(gdp: Series, lang: str) -> str:
    """Note dynamique : le dernier point de PIB / dynamic note: the latest GDP point."""
    latest, when = gdp.iloc[-1], gdp.index[-1]
    quarter = (when.month - 1) // 3 + 1
    if lang == "fr":
        value = f"{latest:,.0f}".replace(",", " ")
        ordinal = "1ᵉʳ" if quarter == 1 else f"{quarter}ᵉ"
        return ("Aucun fichier à télécharger à la main : le script va chercher la série directement sur FRED et la dessine.\\n"
                f"Dernier point : {value} milliards au {ordinal} trimestre {when.year}. Source : BEA via FRED (GDPC1).")
    return ("Nothing to download by hand: the script fetches the series straight from FRED and draws it.\\n"
            f"Latest point: ${latest:,.0f} billion in Q{quarter} {when.year}. Source: BEA via FRED (GDPC1).")

def build_figure(gdp: Series, lang: str) -> Figure:
    """PIB réel en aire remplie, sur toute la période disponible."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig, left=0.12)
    ax.fill_between(gdp.index, gdp, color=nm.COLORS["blue"], alpha=0.14)
    ax.plot(gdp.index, gdp, color=nm.COLORS["blue"], linewidth=2.9)
    ax.set_ylim(0, 26_000)
    ax.set_yticks(range(0, 26_000, 5000))
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, caption(gdp, lang))
    return fig

build_figure(gdp, LANG)'''


# ── Figure 19.02 — glissement annuel du PIB (FRED en direct) ──────────────────

DATA_19_02 = '''from pandas import Series

def load_gdp_growth() -> Series:
    """Croissance du PIB réel sur un an / real GDP year-over-year growth.
    pct_change(4) car le PIB est trimestriel / pct_change(4) since GDP is quarterly."""
    gdp = nm.load_fred("GDPC1")
    return (gdp.pct_change(4) * 100).dropna()

growth = load_gdp_growth()'''

FIG_19_02 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Une ligne de plus, une autre histoire",
        sub="La même série, transformée en glissement annuel par « pct_change »",
        ylab="croissance du PIB réel sur un an, %",
        covid="COVID : −7,5 %\\npuis +12,4 %",
        note="df.pct_change(4)*100 : une instruction, et le niveau devient un taux de croissance — krach COVID et\\n"
             "rebond compris. C'est là que le code dépasse la souris. Source : BEA via FRED (GDPC1)."),
    "en": dict(
        title="One more line, another story",
        sub="The same series, turned into year-over-year growth by « pct_change »",
        ylab="real GDP growth year over year, %",
        covid="COVID: −7.5%\\nthen +12.4%",
        note="df.pct_change(4)*100: one instruction, and the level becomes a growth rate — COVID crash and\\n"
             "rebound included. That is where code beats the mouse. Source: BEA via FRED (GDPC1)."),
}

def build_figure(growth: Series, lang: str) -> Figure:
    """Glissement annuel : ligne claire, aire bleue (>0) et rose (<0)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig)
    ax.fill_between(growth.index, growth, 0, where=growth >= 0,
                    color=nm.COLORS["blue"], alpha=0.5, interpolate=True)
    ax.fill_between(growth.index, growth, 0, where=growth < 0,
                    color=nm.COLORS["rose"], alpha=0.5, interpolate=True)
    ax.plot(growth.index, growth, color=nm.COLORS["text"], linewidth=1.6)
    ax.axhline(0, color=nm.COLORS["muted"], linewidth=1.4, alpha=0.9)
    ax.set_ylim(-10, 14)
    ax.set_yticks(range(-10, 11, 5))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    # Annotation sur le creux COVID de 2020 / annotate the 2020 COVID trough
    trough = growth.loc["2020"].idxmin()
    ax.annotate(text["covid"], xy=(trough, growth.loc[trough]), xytext=(-150, 34),
                textcoords="offset points", ha="right", va="center", fontsize=22,
                fontweight="bold", color=nm.COLORS["rose"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(growth, LANG)'''


# ── Figure 19.03 — PIB réel + bandes de récession NBER (FRED en direct) ───────

DATA_19_03 = '''from pandas import Series

def load_data() -> tuple[Series, Series]:
    """PIB réel (GDPC1) et indicateur de récession NBER (USREC), en direct de FRED.
    Real GDP and the NBER recession flag, live from FRED."""
    gdp = nm.load_fred("GDPC1")
    recessions = nm.load_fred("USREC", start=str(gdp.index[0].year))
    return gdp, recessions

gdp, recessions = load_data()'''

FIG_19_03 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Cinq lignes de plus, et le cycle apparaît",
        sub="Le PIB réel avec les récessions du NBER, ajoutées par une boucle",
        ylab="milliards de dollars de 2017",
        bands="bandes grises =\\nrécessions (NBER)",
        note="Une petite boucle sur la série USREC, un axvspan par récession, et votre graphique parle comme celui d'un\\n"
             "professionnel. Chaque récession y creuse une marche. Source : BEA et NBER via FRED (GDPC1, USREC)."),
    "en": dict(
        title="Five more lines, and the cycle appears",
        sub="U.S. real GDP with NBER recessions, added by a loop",
        ylab="billions of 2017 dollars",
        bands="grey bands =\\nrecessions (NBER)",
        note="A small loop over the USREC series, one axvspan per recession, and your chart speaks like a\\n"
             "professional's. Every recession carves a step. Source: BEA and NBER via FRED (GDPC1, USREC)."),
}

def build_figure(gdp: Series, recessions: Series, lang: str) -> Figure:
    """PIB réel ombré des récessions du NBER."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig, left=0.12)
    runs = recessions.ne(recessions.shift()).cumsum()
    for _, run in recessions.groupby(runs):
        if run.iloc[0] == 1:
            ax.axvspan(run.index[0], run.index[-1], color=nm.COLORS["edge"], alpha=0.75, linewidth=0)
    ax.plot(gdp.index, gdp, color=nm.COLORS["blue"], linewidth=2.9)
    ax.set_ylim(0, 26_000)
    ax.set_yticks(range(0, 26_000, 5000))
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.text(0.085, 0.80, text["bands"], transform=ax.transAxes, fontsize=21.5,
            color=nm.COLORS["muted"], linespacing=1.55)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(gdp, recessions, LANG)'''


# ── Figure 19.04 — l'erreur Reinhart-Rogoff (données embarquées) ──────────────

DATA_19_04 = '''def reinhart_rogoff() -> list[float]:
    """Croissance moyenne au-delà de 90 % de dette : résultat publié vs corrigé (%).
    Average growth above 90% debt: published vs corrected (Herndon, Ash & Pollin, 2013)."""
    return [-0.1, 2.2]'''

FIG_19_04 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Cinq pays oubliés, une conclusion inversée",
        sub="Croissance moyenne des pays très endettés, avant et après correction",
        ylab="croissance moyenne au-delà de 90 % de dette, %",
        cats=["résultat publié\\n(erreur Excel)", "résultat corrigé\\n(Herndon, 2013)"],
        value_labels=["−0,1 %", "+2,2 %"],
        note="Une formule Excel portant sur les lignes 30-44 au lieu de 30-49 excluait cinq pays. Corrigée, la\\n"
             "« contraction » de −0,1 % devient une croissance de +2,2 %. Source : Herndon, Ash & Pollin (2013)."),
    "en": dict(
        title="Five countries forgotten, a conclusion reversed",
        sub="Average growth of highly indebted countries, before and after correction",
        ylab="average growth above 90% debt, %",
        cats=["published result\\n(Excel error)", "corrected result\\n(Herndon, 2013)"],
        value_labels=["−0.1%", "+2.2%"],
        note="An Excel formula spanning rows 30-44 instead of 30-49 excluded five countries. Corrected, the\\n"
             "« contraction » of −0.1% becomes growth of +2.2%. Source: Herndon, Ash & Pollin (2013)."),
}

def build_figure(values: list[float], lang: str) -> Figure:
    """Deux barres : le résultat publié (erroné) contre le résultat corrigé."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.axes(fig, bottom=0.24)
    ax.grid(axis="x", visible=False)
    positions = range(len(values))
    ax.bar(positions, values, width=0.55, color=[nm.COLORS["rose"], nm.COLORS["blue"]], zorder=3)
    ax.axhline(0, color=nm.COLORS["text"], linewidth=1.6, alpha=0.85)
    ax.set_ylim(-1.3, 3.2)
    ax.set_yticks(range(-1, 4))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    for pos, value, label in zip(positions, values, text["value_labels"]):
        above = value >= 0
        ax.annotate(label, (pos, value), xytext=(0, 14 if above else -14),
                    textcoords="offset points", ha="center", va="bottom" if above else "top",
                    fontsize=34, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(reinhart_rogoff(), LANG)'''


# ── Figure 19.05 — pourquoi coder : trois pouvoirs (schéma) ───────────────────

DATA_19_05 = '''def powers(lang: str) -> list[tuple[str, str, list[str]]]:
    """Les trois pouvoirs du clavier : (nom, couleur, lignes), localisés.
    The three powers of the keyboard: (name, color, lines), localized."""
    if lang == "fr":
        return [
            ("Reproductibilité", nm.COLORS["blue"],
             ["un script se relit,", "se corrige, se partage —", "un clic ne laisse rien"]),
            ("Échelle", nm.COLORS["amber"],
             ["cent graphiques", "au lieu d'un,", "recalculés chaque matin"]),
            ("Puissance", nm.COLORS["rose"],
             ["la donnée en mémoire,", "tout le calcul", "du monde s'ouvre"]),
        ]
    return [
        ("Reproducibility", nm.COLORS["blue"],
         ["a script is re-read,", "fixed and shared —", "a click leaves nothing"]),
        ("Scale", nm.COLORS["amber"],
         ["a hundred charts", "instead of one,", "recomputed every morning"]),
        ("Power", nm.COLORS["rose"],
         ["the data in memory,", "all the computation", "in the world opens up"]),
    ]'''

FIG_19_05 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Pourquoi coder, après la souris",
               sub="Trois pouvoirs que le clavier seul apporte"),
    "en": dict(title="Why code, after the mouse",
               sub="Three powers the keyboard alone brings"),
}

def build_figure(cards: list[tuple[str, str, list[str]]], lang: str) -> Figure:
    """Schéma : trois cartes colorées (un pouvoir par carte)."""
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

build_figure(powers(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Chapitre 20 — La croissance déjà anticipée
# ═════════════════════════════════════════════════════════════════════════════

# ── Chargeur partagé des données de Robert Shiller (CAPE) ─────────────────────

SHILLER_DATA = '''import io
import urllib.request
import pandas as pd
from pandas import DataFrame

SHILLER_URL = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"

def load_shiller() -> DataFrame:
    """Données historiques de Robert Shiller (ie_data.xls) : CAPE mensuel et rendement
    réel des actions sur 10 ans (colonnes précalculées par Shiller), depuis 1871.
    Robert Shiller's historical data: monthly CAPE and the 10-year real stock return."""
    try:                                              # moteur .xls (préinstallé sur Colab)
        import xlrd  # noqa: F401
    except ModuleNotFoundError:
        import subprocess, sys
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "xlrd"], check=True)
    raw = urllib.request.urlopen(SHILLER_URL, timeout=60).read()
    sheet = pd.read_excel(io.BytesIO(raw), sheet_name="Data", header=7, engine="xlrd")
    df = pd.DataFrame({
        "year":  pd.to_numeric(sheet.iloc[:, 5], errors="coerce"),          # année décimale
        "cape":  pd.to_numeric(sheet.iloc[:, 12], errors="coerce"),         # CAPE (P/E10)
        "ret10": pd.to_numeric(sheet.iloc[:, 19], errors="coerce") * 100,   # rendement réel 10 ans, %
    })
    return df.dropna(subset=["year"])

shiller = load_shiller()'''


# ── Figure 20.01 — le paradoxe BRIC (schéma à deux cartes) ────────────────────

DATA_20_01 = '''def bric_cards(lang: str) -> list[tuple[str, str, list[list[str]]]]:
    """Les deux volets du paradoxe BRIC : (titre, couleur, paragraphes), localisés.
    The two sides of the BRIC paradox: (title, color, paragraphs), localized."""
    if lang == "fr":
        return [
            ("La croissance promise", nm.COLORS["blue"],
             [["Brésil, Russie,", "Inde, Chine"],
              ["une décennie de", "croissance record"],
              ["la promesse tenue"]]),
            ("Le fonds BRIC", nm.COLORS["rose"],
             [["depuis 2010"],
              ["− 88 %", "de valeur"],
              ["fermé en octobre 2015"]]),
        ]
    return [
        ("The promised growth", nm.COLORS["blue"],
         [["Brazil, Russia,", "India, China"],
          ["a decade of", "record growth"],
          ["the promise kept"]]),
        ("The BRIC fund", nm.COLORS["rose"],
         [["since 2010"],
          ["− 88%", "in value"],
          ["closed in October 2015"]]),
    ]'''

FIG_20_01 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La croissance était réelle. L'investissement, un désastre.",
        sub="Le paradoxe BRIC : tenir sa promesse de croissance ne fait pas gagner d'argent",
        note="Les BRIC ont tenu leur promesse de croissance — et le fonds censé en profiter a perdu près de 88 % avant\\n"
             "de fermer. La croissance connue était déjà dans les prix. Sources : Goldman Sachs ; Bloomberg (2015)."),
    "en": dict(
        title="The growth was real. The investment, a disaster.",
        sub="The BRIC paradox: keeping your growth promise does not make you money",
        note="The BRICs kept their growth promise — and the fund meant to profit lost nearly 88% before\\n"
             "closing. The known growth was already in the price. Sources: Goldman Sachs; Bloomberg (2015)."),
}

def draw_cards(ax, cards, top, bottom):
    """Deux cartes en regard : titre coloré puis paragraphes centrés."""
    card_w, gap, x0 = 720, 88, 108
    for i, (name, color, paras) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        nm.card(ax, x, bottom, card_w, top - bottom, edge=color, lw=2.6, radius=26)
        ax.text(cx, top - 62, name, ha="center", va="center",
                fontsize=31, fontweight="bold", color=color)
        y = top - 158
        for para in paras:
            for line in para:
                ax.text(cx, y, line, ha="center", va="center",
                        fontsize=27, color=nm.COLORS["text"])
                y -= 42
            y -= 40

def build_figure(cards: list, lang: str) -> Figure:
    """Schéma : la croissance promise (bleu) face au fonds BRIC (rose)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.blank_axes(fig)
    draw_cards(ax, cards, top=742, bottom=298)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(bric_cards(LANG), LANG)'''


# ── Figure 20.02 — la croissance facturée d'avance (modèle de Gordon) ─────────

DATA_20_02 = '''def gordon_prices() -> list[float]:
    """Modèle de Gordon : Prix = dividende / (rendement exigé − croissance).
    Deux entreprises, même dividende (1 €), même rendement exigé (8 %),
    croissances attendues de 2 % et 6 %. / Gordon (1956): Price = D / (r − g)."""
    dividend, required = 1.0, 0.08
    return [dividend / (required - g) for g in (0.02, 0.06)]

prices = gordon_prices()'''

FIG_20_02 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La croissance espérée est facturée d'avance",
        sub="Deux entreprises, même dividende — mais un prix d'entrée qui triple",
        ylab="prix payé pour 1 € de dividende",
        banner="même dividende (1 €), même rendement exigé (8 %)",
        cats=["Entreprise A\\ncroissance +2 %", "Entreprise B\\ncroissance +6 %"],
        value_labels=["17 €", "50 €"],
        note="Si les deux tiennent exactement leur promesse, l'investisseur touche 8 % dans les deux cas : le pari de\\n"
             "croissance n'a rien rapporté de plus, il a seulement fait payer 3× plus cher. Modèle de Gordon (1956)."),
    "en": dict(
        title="Expected growth is billed upfront",
        sub="Two firms, same dividend — but an entry price that triples",
        ylab="price paid for €1 of dividend",
        banner="same dividend (€1), same required return (8%)",
        cats=["Firm A\\ngrowth +2%", "Firm B\\ngrowth +6%"],
        value_labels=["€17", "€50"],
        note="If both keep their promise exactly, the investor earns 8% in each case: the growth bet returned\\n"
             "nothing extra, it only made you pay 3× more. Gordon model (1956)."),
}

def build_figure(prices: list[float], lang: str) -> Figure:
    """Deux barres : le prix d'entrée facturé pour une croissance attendue faible vs forte."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1121)
    ax = nm.axes(fig, left=0.10, bottom=0.20)
    ax.grid(axis="x", visible=False)
    positions = range(len(prices))
    ax.bar(positions, prices, width=0.62, color=["#c9d4e7", nm.COLORS["blue"]], zorder=3)
    ax.set_ylim(0, 62)
    ax.set_yticks(range(0, 61, 10))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, price, label in zip(positions, prices, text["value_labels"]):
        ax.annotate(label, (pos, price), xytext=(0, 16), textcoords="offset points",
                    ha="center", va="bottom", fontsize=38, fontweight="bold", color=nm.COLORS["text"])
    ax.text(0.5, 0.965, text["banner"], transform=ax.transAxes, ha="center", va="top",
            fontsize=24, fontweight="bold", color=nm.COLORS["amber"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(prices, LANG)'''


# ── Figure 20.03 — CAPE de départ vs rendement à 10 ans (Shiller en direct) ───

FIG_20_03 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Plus vous payez cher, moins vous gagnez",
        sub="Valorisation de départ et rendement réel des 10 années suivantes, États-Unis, 1881-2024",
        xlab="CAPE au départ (valorisation)",
        ylab="rendement réel des 10 années suivantes, %/an",
        today="aujourd'hui\\n≈ 35-40",
        expect="rendement réel attendu\\n≈ 0 %/an",
        corr="corrélation ≈ −0,5",
        note="Chaque point : un mois depuis 1881. La valorisation de départ « explique » environ un quart du rendement\\n"
             "à dix ans — modeste, mais le signe est sans appel. Source : données de Robert Shiller (CAPE)."),
    "en": dict(
        title="The more you pay, the less you earn",
        sub="Starting valuation and real return over the next 10 years, United States, 1881-2024",
        xlab="starting CAPE (valuation)",
        ylab="real return over the next 10 years, %/yr",
        today="today\\n≈ 35-40",
        expect="expected real return\\n≈ 0%/yr",
        corr="correlation ≈ −0.5",
        note="Each dot: one month since 1881. The starting valuation « explains » about a quarter of the ten-year\\n"
             "return — modest, but the sign is unmistakable. Source: Robert Shiller's data (CAPE)."),
}

def build_figure(shiller: "DataFrame", lang: str) -> Figure:
    """Nuage CAPE de départ vs rendement réel à 10 ans, avec droite de régression."""
    text = LABELS[lang]
    pts = shiller.dropna(subset=["cape", "ret10"])
    x, y = pts["cape"].to_numpy(), pts["ret10"].to_numpy()

    fig = nm.figure(height_px=1083)
    ax = nm.axes(fig, left=0.078, bottom=0.155)
    ax.axvspan(35, 41, color=nm.COLORS["rose"], alpha=0.12, linewidth=0)
    ax.axhline(0, color=nm.COLORS["blue2"], linewidth=1.6, alpha=0.85)
    ax.scatter(x, y, s=12, color=nm.COLORS["blue"], alpha=0.32, linewidths=0, zorder=2)
    slope, intercept = np.polyfit(x, y, 1)
    line_x = np.array([5, 45])
    ax.plot(line_x, intercept + slope * line_x, color=nm.COLORS["amber"], linewidth=4.2, zorder=3)
    ax.set_xlim(4, 46)
    ax.set_xticks(range(5, 46, 5))
    ax.set_ylim(-11, 21)
    ax.set_yticks(range(-10, 21, 5))
    ax.set_xlabel(text["xlab"])
    ax.set_ylabel(text["ylab"])
    ax.text(38, 16.6, text["today"], ha="center", va="center", fontsize=22,
            fontweight="bold", color=nm.COLORS["rose"], linespacing=1.5)
    ax.annotate(text["expect"], xy=(37, intercept + slope * 37), xytext=(30.5, -6.6),
                ha="center", va="center", fontsize=21, color=nm.COLORS["rose"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    ax.text(13, -7.3, text["corr"], ha="center", va="center", fontsize=25,
            fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(shiller, LANG)'''


# ── Figure 20.04 — le CAPE de Shiller depuis 1881 (Shiller en direct) ─────────

FIG_20_04 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le futur est déjà, en grande partie, dans les cours",
        sub="Valorisation des actions américaines depuis 1881 (CAPE de Shiller)",
        ylab="CAPE (P/E ajusté du cycle)",
        mean="moyenne longue : 17,5",
        today="aujourd'hui : ~35-40\\n(97ᵉ centile de l'histoire)",
        note="À plus du double de sa moyenne longue, la valorisation n'a été dépassée qu'en 1929, 2000 et 2021.\\n"
             "Elle dit à quel point l'optimisme est déjà payé. Source : données de Robert Shiller."),
    "en": dict(
        title="The future is already, largely, in the price",
        sub="Valuation of U.S. equities since 1881 (Shiller CAPE)",
        ylab="CAPE (cyclically adjusted P/E)",
        mean="long-run average: 17.5",
        today="today: ~35-40\\n(97th percentile of history)",
        note="At more than twice its long-run average, valuation has been exceeded only in 1929, 2000 and 2021.\\n"
             "It says how much optimism is already paid for. Source: Robert Shiller's data."),
}

def build_figure(shiller: "DataFrame", lang: str) -> Figure:
    """Le CAPE de Shiller mensuel depuis 1881, sa moyenne longue et les pics de 1929/2000/2021."""
    text = LABELS[lang]
    s = shiller.dropna(subset=["cape"])
    year, cape = s["year"].to_numpy(), s["cape"].to_numpy()

    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.072)
    ax.plot(year, cape, color=nm.COLORS["blue"], linewidth=1.9)
    ax.axhline(17.5, color=nm.COLORS["text"], linestyle=(0, (7, 5)), linewidth=2.2, alpha=0.9)
    ax.set_ylim(0, 47)
    ax.set_yticks(range(0, 41, 10))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(1876, 2030)
    ax.set_xticks(range(1880, 2021, 20))
    ax.text(1891, 19.4, text["mean"], fontsize=21, fontweight="bold", color=nm.COLORS["text"])
    for yr, label in [(1929, "1929"), (2000, "2000"), (2021, "2021")]:
        peak = cape[(year >= yr - 1.3) & (year <= yr + 1.3)].max()
        ax.annotate(label, xy=(yr, peak), xytext=(0, 30), textcoords="offset points",
                    ha="center", va="bottom", fontsize=22, color=nm.COLORS["text"],
                    arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    ax.scatter([year[-1]], [cape[-1]], s=95, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(text["today"], xy=(year[-1], cape[-1]), xytext=(1966, 39.2),
                ha="center", va="center", fontsize=21, fontweight="bold",
                color=nm.COLORS["rose"], linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["rose"], lw=1.8))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(shiller, LANG)'''


# ── Figure 20.05 — la récession attendue (schéma à deux cartes) ───────────────

DATA_20_05 = '''def recession_cards(lang: str) -> list[tuple[str, str, list[list[str]]]]:
    """Les deux volets de la surprise 2023 : (titre, couleur, paragraphes), localisés.
    The two sides of the 2023 surprise: (title, color, paragraphs), localized."""
    if lang == "fr":
        return [
            ("Ce que le consensus prévoyait", nm.COLORS["rose"],
             [["Octobre 2022"],
              ["100 %", "de probabilité de", "récession sous un an", "(modèle Bloomberg Economics)"]]),
            ("Ce qui s'est passé", nm.COLORS["blue"],
             [["Année 2023"],
              ["+ 26 %", "rendement total du", "S&P 500", "(dividendes réinvestis)"]]),
        ]
    return [
        ("What the consensus expected", nm.COLORS["rose"],
         [["October 2022"],
          ["100%", "probability of", "recession within a year", "(Bloomberg Economics model)"]]),
        ("What actually happened", nm.COLORS["blue"],
         [["Year 2023"],
          ["+26%", "total return of the", "S&P 500", "(dividends reinvested)"]]),
    ]'''

FIG_20_05 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La récession que tout le monde attendait",
        sub="Le consensus était unanime. Le marché a fait l'inverse.",
        note="Quand tout le monde attend déjà le pire, le pire est dans les cours : il suffit qu'il n'arrive pas pour que\\n"
             "le marché s'envole. Sources : Bloomberg Economics (17 oct. 2022) ; rendement total S&P 500 2023."),
    "en": dict(
        title="The recession everyone was expecting",
        sub="The consensus was unanimous. The market did the opposite.",
        note="When everyone already expects the worst, the worst is in the price: it need only fail to arrive for the\\n"
             "market to soar. Sources: Bloomberg Economics (Oct. 17, 2022); S&P 500 total return 2023."),
}

def draw_cards(ax, cards, top, bottom):
    """Deux cartes en regard : titre coloré puis paragraphes centrés."""
    card_w, gap, x0 = 720, 88, 108
    for i, (name, color, paras) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        nm.card(ax, x, bottom, card_w, top - bottom, edge=color, lw=2.6, radius=26)
        ax.text(cx, top - 62, name, ha="center", va="center",
                fontsize=30, fontweight="bold", color=color)
        y = top - 158
        for para in paras:
            for line in para:
                ax.text(cx, y, line, ha="center", va="center",
                        fontsize=26, color=nm.COLORS["text"])
                y -= 42
            y -= 40

def build_figure(cards: list, lang: str) -> Figure:
    """Schéma : ce que le consensus prévoyait (rose) face à ce qui s'est passé (bleu)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.blank_axes(fig)
    draw_cards(ax, cards, top=752, bottom=300)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(recession_cards(LANG), LANG)'''


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

DIR_18 = CHAPTERS["18"]["dir"]
DIR_19 = CHAPTERS["19"]["dir"]
DIR_20 = CHAPTERS["20"]["dir"]

SHILLER_SRC = ("données de Robert Shiller (CAPE)", "Robert Shiller's data (CAPE)")

NOTEBOOKS = {
    "templates/template-figure.ipynb": (
        TEMPLATE_MD,
        [SETUP, TEMPLATE_DATA, TEMPLATE_FIG],
    ),
    # ── Chapitre 18 — Atelier données : découvrir FRED ───────────────────────
    f"{DIR_18}/fig01-croissance-fred.ipynb": (
        intro_md("18", "De 30 séries par modem à 845 000", "From 30 series by modem to 845,000"),
        [SETUP, DATA_01, FIG_01],
    ),
    f"{DIR_18}/fig02-recession-bands.ipynb": (
        intro_md("18", "Ce que vous saurez fabriquer en trois clics",
                 "What you'll be able to make in three clicks"),
        [SETUP, DATA_02, FIG_02],
    ),
    f"{DIR_18}/fig03-transformations.ipynb": (
        intro_md("18", "La même série, deux histoires", "The same series, two stories"),
        [SETUP, DATA_03, FIG_03],
    ),
    f"{DIR_18}/fig04-trousse-depart.ipynb": (
        intro_md("18", "La trousse de départ du macro-observateur",
                 "The macro-watcher's starter kit", live=False),
        [SETUP, DATA_04, FIG_04],
    ),
    f"{DIR_18}/fig05-cousins-fred.ipynb": (
        intro_md("18", "FRED n'est pas seul : ses cousins", "FRED is not alone: its cousins",
                 live=False),
        [SETUP, DATA_05, FIG_05],
    ),
    # ── Chapitre 19 — Premier script Python ──────────────────────────────────
    f"{DIR_19}/fig01-pib-reel.ipynb": (
        intro_md("19", "Ce que produisent huit lignes de Python",
                 "What eight lines of Python produce"),
        [SETUP, DATA_19_01, FIG_19_01],
    ),
    f"{DIR_19}/fig02-glissement-annuel.ipynb": (
        intro_md("19", "Une ligne de plus, une autre histoire", "One more line, another story"),
        [SETUP, DATA_19_02, FIG_19_02],
    ),
    f"{DIR_19}/fig03-bandes-recession.ipynb": (
        intro_md("19", "Cinq lignes de plus, et le cycle apparaît",
                 "Five more lines, and the cycle appears"),
        [SETUP, DATA_19_03, FIG_19_03],
    ),
    f"{DIR_19}/fig04-reinhart-rogoff.ipynb": (
        intro_md("19", "Cinq pays oubliés, une conclusion inversée",
                 "Five countries forgotten, a conclusion reversed", live=False),
        [SETUP, DATA_19_04, FIG_19_04],
    ),
    f"{DIR_19}/fig05-pourquoi-coder.ipynb": (
        intro_md("19", "Pourquoi coder, après la souris", "Why code, after the mouse",
                 live=False),
        [SETUP, DATA_19_05, FIG_19_05],
    ),
    # ── Chapitre 20 — La croissance déjà anticipée ───────────────────────────
    f"{DIR_20}/fig01-paradoxe-bric.ipynb": (
        intro_md("20", "La croissance était réelle. L'investissement, un désastre.",
                 "The growth was real. The investment, a disaster.", live=False),
        [SETUP, DATA_20_01, FIG_20_01],
    ),
    f"{DIR_20}/fig02-croissance-facturee.ipynb": (
        intro_md("20", "La croissance espérée est facturée d'avance",
                 "Expected growth is billed upfront", live=False),
        [SETUP, DATA_20_02, FIG_20_02],
    ),
    f"{DIR_20}/fig03-cape-rendement.ipynb": (
        intro_md("20", "Plus vous payez cher, moins vous gagnez",
                 "The more you pay, the less you earn", source=SHILLER_SRC),
        [SETUP, SHILLER_DATA, FIG_20_03],
    ),
    f"{DIR_20}/fig04-cape-histoire.ipynb": (
        intro_md("20", "Le futur est déjà, en grande partie, dans les cours",
                 "The future is already, largely, in the price", source=SHILLER_SRC),
        [SETUP, SHILLER_DATA, FIG_20_04],
    ),
    f"{DIR_20}/fig05-recession-attendue.ipynb": (
        intro_md("20", "La récession que tout le monde attendait",
                 "The recession everyone was expecting", live=False),
        [SETUP, DATA_20_05, FIG_20_05],
    ),
}


def as_cell(kind, src):
    cell = {"cell_type": kind, "metadata": {}, "source": src.splitlines(keepends=True)}
    if kind == "code":
        cell.update(execution_count=None, outputs=[])
    return cell


def build():
    for name, (intro, codes) in NOTEBOOKS.items():
        path = os.path.join(REPO, name)
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
