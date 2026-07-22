#!/usr/bin/env python3
"""Génère les .ipynb du chapitre 14 (Démographie et croissance) via nb_kit.

Convention « stricte » : une seule cellule code par notebook, fonctions typées +
docstrings ; ``load_*()`` charge les données (série FRED en direct, ou points
embarqués pour les données ONU / Banque mondiale / valeurs calculées) puis
``build_figure(...) -> Figure`` construit la figure ; bilingue via ``LANG``.
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="14",
    title_fr="Démographie et croissance : comment la population façonne l'économie",
    title_en="Demography and Growth: How Population Shapes the Economy",
    slug_fr="demographie-et-croissance",
    slug_en="demography-and-growth",
)
DIR = "macro/14-demographie-et-croissance"


# ── Figure 01 — population active du Japon (FRED en direct) ───────────────────

DATA_1 = '''from pandas import Series

def load_working_age() -> Series:
    """Population en âge de travailler au Japon (15-64 ans), en millions, en direct de FRED.
    Japan's working-age population (15-64), in millions, live from FRED (LFWA64TTJPM647S)."""
    persons = nm.load_fred("LFWA64TTJPM647S", start="1970")
    return persons / 1_000_000

pop = load_working_age()'''

FIG_1 = '''import matplotlib.dates as mdates
import pandas as pd
from matplotlib.figure import Figure

MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
             "août", "septembre", "octobre", "novembre", "décembre"]

LABELS = {
    "fr": dict(
        title="Le Japon a perdu un actif sur six",
        sub="Population en âge de travailler au Japon, 1970-2026",
        ylab="population de 15 à 64 ans, millions",
        total="pic de la population\\nTOTALE : 2008",
        gap="13 ans d'écart",
        today="aujourd'hui"),
    "en": dict(
        title="Japan has lost one working-age adult in six",
        sub="Japan's working-age population, 1970-2026",
        ylab="population aged 15 to 64, millions",
        total="peak of the TOTAL\\npopulation: 2008",
        gap="13-year gap",
        today="today"),
}

def peak_text(peak_date, peak_val: float, lang: str) -> str:
    """Étiquette du pic de 1995 (valeur et mois lus sur la série)."""
    if lang == "fr":
        value = f"{peak_val:.1f}".replace(".", ",")
        return f"pic : {value} M\\n{MONTHS_FR[peak_date.month - 1]} {peak_date.year}"
    return f"peak: {peak_val:.1f}M\\n{peak_date:%B %Y}"

def latest_text(latest_val: float, lang: str) -> str:
    """Étiquette du dernier point (valeur du jour)."""
    if lang == "fr":
        return f"{latest_val:.1f} M".replace(".", ",") + "\\n" + LABELS["fr"]["today"]
    return f"{latest_val:.1f}M\\n{LABELS['en']['today']}"

def caption(peak_val: float, latest_val: float, lang: str) -> str:
    """Note interne dynamique : recul de la population active depuis son pic."""
    decline = (peak_val - latest_val) / peak_val * 100
    if lang == "fr":
        value = f"{decline:.1f}".replace(".", ",")
        return ("La population active culmine en 1995, TREIZE ANS avant la population totale, et a reculé de "
                f"{value} %\\ndepuis. La « stagnation » japonaise est d'abord un fait démographique. Source : Banque du Japon, FRED.")
    return ("The working-age population peaks in 1995, THIRTEEN YEARS before the total population, and has fallen "
            f"{decline:.1f}%\\nsince. Japan's « stagnation » is first a demographic fact. Source: Bank of Japan, FRED.")

def build_figure(pop: Series, lang: str) -> Figure:
    """Population active du Japon, avec le pic de 1995 et le dernier point."""
    text = LABELS[lang]
    peak_date, peak_val = pop.idxmax(), pop.max()
    latest_date, latest_val = pop.index[-1], pop.iloc[-1]

    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.088)
    ax.plot(pop.index, pop, color=nm.COLORS["blue"], linewidth=2.9)

    # Repère du pic de la population TOTALE (2008), treize ans après.
    total_x = pd.Timestamp("2008-01-01")
    peak_x = pd.Timestamp("1995-03-01")
    ax.axvline(total_x, color=nm.COLORS["muted"], linestyle=(0, (2, 4)), linewidth=1.8, alpha=0.9)
    ax.text(pd.Timestamp("2008-10-01"), 71.0, text["total"], fontsize=20,
            color=nm.COLORS["muted"], va="center", ha="left", linespacing=1.4)
    ax.annotate("", xy=(total_x, 71.5), xytext=(peak_x, 71.5),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["text"], lw=1.8))
    ax.text(pd.Timestamp("2001-09-01"), 72.5, text["gap"], fontsize=22, fontweight="bold",
            color=nm.COLORS["text"], ha="center", va="bottom")

    # Pic de la population active (rose) et dernier point (ambre).
    ax.scatter([peak_date], [peak_val], s=130, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(peak_text(peak_date, peak_val, lang), xy=(peak_date, peak_val),
                xytext=(pd.Timestamp("1979-01-01"), 86.6), fontsize=22, fontweight="bold",
                color=nm.COLORS["rose"], ha="left", va="center", linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    ax.scatter([latest_date], [latest_val], s=130, color=nm.COLORS["amber"], zorder=5)
    ax.annotate(latest_text(latest_val, lang), xy=(latest_date, latest_val),
                xytext=(pd.Timestamp("2015-06-01"), 80.3), fontsize=22, fontweight="bold",
                color=nm.COLORS["amber"], ha="left", va="center", linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["amber"], lw=1.8))

    ax.set_ylim(69, 91)
    ax.set_yticks(range(70, 91, 5))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(pd.Timestamp("1969-06-01"), pd.Timestamp("2027-06-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, caption(peak_val, latest_val, lang))
    return fig

build_figure(pop, LANG)'''


# ── Figure 02 — vitesse du vieillissement (données embarquées) ────────────────

DATA_2 = '''def load_ageing_speed(lang: str) -> tuple[list[str], list[int]]:
    """Années pour passer de 7 % à 14 % de personnes de 65 ans et plus, par pays.
    Years to go from 7% to 14% elderly, by country (Cabinet Office ; World Bank data)."""
    countries = {
        "fr": ["France", "Suède", "Royaume-Uni", "Allemagne", "Japon", "Corée du Sud"],
        "en": ["France", "Sweden", "United Kingdom", "Germany", "Japan", "South Korea"],
    }
    years = [115, 85, 47, 40, 24, 18]
    return countries[lang], years'''

FIG_2 = '''from matplotlib.figure import Figure

GREY_BLUE = "#96a5c3"

LABELS = {
    "fr": dict(
        title="Le vieillissement n'est pas un niveau, c'est une vitesse",
        sub="Durée du passage de 7 % à 14 % de personnes âgées",
        xlab="années pour passer de 7 % à 14 % de personnes de 65 ans et plus",
        unit="ans",
        note="Le Japon a mis 24 ans à faire ce que la France a mis 115 ans à faire. Mais son record est déjà battu :\\n"
             "la Corée du Sud l'a fait en 18 ans. Sources : Cabinet Office japonais ; calcul sur données Banque mondiale."),
    "en": dict(
        title="Ageing is not a level, it is a speed",
        sub="Time taken to go from 7% to 14% of elderly people",
        xlab="years to go from 7% to 14% of people aged 65 and over",
        unit="yrs",
        note="Japan took 24 years to do what France took 115 years to do. But its record is already broken:\\n"
             "South Korea did it in 18 years. Sources: Japan's Cabinet Office; author's calculation on World Bank data."),
}

def build_figure(countries: list[str], years: list[int], lang: str) -> Figure:
    """Barres horizontales : durée du vieillissement par pays, Japon et Corée mis en avant."""
    text = LABELS[lang]
    colors = [GREY_BLUE] * 4 + [nm.COLORS["rose"], nm.COLORS["amber"]]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.15, bottom=0.22)
    ax.grid(axis="y", visible=False)
    positions = list(range(len(countries)))
    ax.barh(positions, years, height=0.6, color=colors, zorder=3)
    ax.invert_yaxis()                                 # France en haut / France on top
    ax.set_yticks(positions)
    ax.set_yticklabels(countries, fontsize=23, color=nm.COLORS["muted"])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 134)
    ax.set_xticks(range(0, 121, 20))
    ax.set_xlabel(text["xlab"])
    for pos, value in zip(positions, years):
        ax.annotate(f"{value} {text['unit']}", (value, pos), xytext=(12, 0),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=28, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(*load_ageing_speed(LANG), LANG)'''


# ── Figure 03 — le bon dénominateur (données embarquées) ─────────────────────

DATA_3 = '''def load_denominator() -> tuple[list[float], list[float]]:
    """Croissance annuelle 1991-2019, Japon et États-Unis, selon trois dénominateurs :
    PIB total, par habitant, par personne en âge de travailler.
    Annual 1991-2019 growth, Japan and the U.S., by three denominators
    (Fernández-Villaverde, Ventura & Yao, 2025, table 1)."""
    japan = [0.83, 0.76, 1.39]
    usa = [2.58, 1.63, 1.65]
    return japan, usa

japan, usa = load_denominator()'''

FIG_3 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Tout dépend du dénominateur",
        sub="Croissance japonaise et américaine selon ce qu'on rapporte, 1991-2019",
        ylab="croissance annuelle 1991-2019, %",
        cats=["PIB\\ntotal", "PIB par\\nhabitant", "PIB par personne\\nen âge de travailler"],
        japan="Japon", usa="États-Unis",
        gaps=["écart 1,75", "écart 0,87", "écart 0,26"],
        note="Le même Japon paraît en panne (1,75 point de retard sur le PIB total) ou presque à parité\\n"
             "(0,26 point par actif). Source : Fernández-Villaverde, Ventura & Yao (2025), tableau 1."),
    "en": dict(
        title="It all depends on the denominator",
        sub="Japanese and U.S. growth by what you divide by, 1991-2019",
        ylab="annual growth 1991-2019, %",
        cats=["total\\nGDP", "GDP per\\ncapita", "GDP per\\nworking-age person"],
        japan="Japan", usa="United States",
        gaps=["gap 1.75", "gap 0.87", "gap 0.26"],
        note="The same Japan looks stalled (1.75 points behind on total GDP) or nearly level\\n"
             "(0.26 points per working-age adult). Source: Fernández-Villaverde, Ventura & Yao (2025), table 1."),
}

def fmt(value: float, lang: str) -> str:
    """Deux décimales, virgule décimale en français."""
    return f"{value:.2f}".replace(".", ",") if lang == "fr" else f"{value:.2f}"

def build_figure(japan: list[float], usa: list[float], lang: str) -> Figure:
    """Barres groupées : Japon (rose) contre États-Unis (bleu), trois dénominateurs, avec écarts."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, bottom=0.20)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(japan))
    width = 0.38
    ax.bar(x - width / 2, japan, width=width, color=nm.COLORS["rose"], zorder=3, label=text["japan"])
    ax.bar(x + width / 2, usa, width=width, color=nm.COLORS["blue"], zorder=3, label=text["usa"])
    ax.set_ylim(0, 3.5)
    ax.set_yticks([i / 2 for i in range(8)])
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 2.6)
    ax.set_xticks(list(x))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)

    for xi, jv, uv in zip(x, japan, usa):
        ax.annotate(fmt(jv, lang), (xi - width / 2, jv), xytext=(0, 10), textcoords="offset points",
                    ha="center", va="bottom", fontsize=27, fontweight="bold", color=nm.COLORS["rose"])
        ax.annotate(fmt(uv, lang), (xi + width / 2, uv), xytext=(0, 10), textcoords="offset points",
                    ha="center", va="bottom", fontsize=27, fontweight="bold", color=nm.COLORS["blue2"])

    # Flèche d'écart (ambre) entre les deux barres de chaque groupe.
    for xi, jv, uv, glabel in zip(x, japan, usa, text["gaps"]):
        ax.annotate("", xy=(xi, uv), xytext=(xi, jv),
                    arrowprops=dict(arrowstyle="<->", color=nm.COLORS["amber"], lw=1.8))
        small = uv - jv < 0.5                          # écart trop court pour porter le texte
        lx = xi - 0.09 if small else xi
        ly = max(jv, uv) + 0.30 if small else jv + 0.7 * (uv - jv)
        ax.text(lx, ly, glabel, ha="center", va="center", fontsize=21, fontweight="bold",
                color=nm.COLORS["amber"],
                bbox=dict(boxstyle="round,pad=0.14", fc=nm.COLORS["bg"], ec="none"))

    ax.legend(loc="upper left", fontsize=21, frameon=False, labelcolor=nm.COLORS["text"], handlelength=1.3)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(japan, usa, LANG)'''


# ── Figure 04 — le dividende n'est pas automatique (données embarquées) ───────

DATA_4 = '''def load_dividend() -> tuple[list[float], list[float]]:
    """Coup de pouce démographique (points/an) et croissance obtenue du PIB par habitant (%/an) :
    Asie de l'Est contre Amérique latine.
    Demographic boost and achieved GDP-per-capita growth: East Asia vs Latin America
    (Bloom & Williamson 1998 ; Bloom, Canning & Sevilla 2003)."""
    boost = [1.6, 1.1]
    growth = [6.8, 0.7]
    return boost, growth

boost, growth = load_dividend()'''

FIG_4 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le même cadeau, deux destins",
        sub="Coup de pouce démographique et croissance effectivement obtenue",
        ylab="points de croissance annuelle",
        cats=["Asie de l'Est", "Amérique latine"],
        boost="coup de pouce démographique", growth="croissance du PIB par habitant",
        boost_labels=["1,6 pt", "1,1 pt"], growth_labels=["6,8 %", "0,7 %"],
        note="L'Amérique latine a reçu un coup de pouce démographique proche de celui de l'Asie — et a crû huit fois\\n"
             "moins vite. La démographie ouvre une fenêtre ; elle ne la traverse pas à votre place. Sources : Bloom &\\n"
             "Williamson (1998) ; Bloom, Canning & Sevilla (2003)."),
    "en": dict(
        title="The same gift, two destinies",
        sub="The demographic boost and the growth actually obtained",
        ylab="points of annual growth",
        cats=["East Asia", "Latin America"],
        boost="demographic boost", growth="GDP-per-capita growth",
        boost_labels=["1.6 pt", "1.1 pt"], growth_labels=["6.8%", "0.7%"],
        note="Latin America got a demographic boost close to Asia's — and grew eight times more slowly. Demography\\n"
             "opens a window; it does not climb through it for you. Sources: Bloom & Williamson (1998); Bloom,\\n"
             "Canning & Sevilla (2003)."),
}

def build_figure(boost: list[float], growth: list[float], lang: str) -> Figure:
    """Barres groupées : coup de pouce démographique (ambre) et croissance obtenue (bleu)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, bottom=0.26)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(boost))
    width = 0.38
    ax.bar(x - width / 2, boost, width=width, color=nm.COLORS["amber"], zorder=3, label=text["boost"])
    ax.bar(x + width / 2, growth, width=width, color=nm.COLORS["blue"], zorder=3, label=text["growth"])
    ax.set_ylim(0, 8)
    ax.set_yticks(range(0, 9))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(x))
    ax.set_xticklabels(text["cats"], fontsize=24, color=nm.COLORS["muted"])
    ax.tick_params(axis="x", length=0)
    for xi, value, label in zip(x, boost, text["boost_labels"]):
        ax.annotate(label, (xi - width / 2, value), xytext=(0, 10), textcoords="offset points",
                    ha="center", va="bottom", fontsize=28, fontweight="bold", color=nm.COLORS["amber"])
    for xi, value, label in zip(x, growth, text["growth_labels"]):
        ax.annotate(label, (xi + width / 2, value), xytext=(0, 10), textcoords="offset points",
                    ha="center", va="bottom", fontsize=28, fontweight="bold", color=nm.COLORS["blue2"])
    ax.legend(loc="upper right", fontsize=21, frameon=False, labelcolor=nm.COLORS["text"], handlelength=1.3)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(boost, growth, LANG)'''


# ── Figure 05 — où souffle le vent (données embarquées) ───────────────────────

DATA_5 = '''def load_population() -> tuple[list[float], list[float]]:
    """Population (milliards) en 2024 et 2100 : Afrique subsaharienne et monde entier.
    Population (billions) in 2024 and 2100: sub-Saharan Africa and the whole world
    (United Nations, World Population Prospects 2024)."""
    y2024 = [1.24, 8.16]
    y2100 = [3.35, 10.18]
    return y2024, y2100

y2024, y2100 = load_population()'''

FIG_5 = '''import numpy as np
from matplotlib.figure import Figure

GREY_BLUE = "#96a5c3"

LABELS = {
    "fr": dict(
        title="Le seul moteur démographique qui reste",
        sub="Population de l'Afrique subsaharienne et du monde, 2024 et 2100",
        ylab="population, milliards",
        cats=["Afrique\\nsubsaharienne", "Monde\\n(total)"],
        y2024="2024", y2100="2100", unit="Md",
        annot=["L'Afrique subsaharienne ajoute 2,11 Md", "Le monde entier n'ajoute que 2,02 Md"],
        note="L'Afrique subsaharienne apporte PLUS DE 100 % de la croissance nette de la population mondiale d'ici\\n"
             "2100 : elle croît davantage que le monde entier, parce que le reste se contracte. Source : ONU, WPP 2024."),
    "en": dict(
        title="The only demographic engine left",
        sub="Population of sub-Saharan Africa and of the world, 2024 and 2100",
        ylab="population, billions",
        cats=["Sub-Saharan\\nAfrica", "World\\n(total)"],
        y2024="2024", y2100="2100", unit="bn",
        annot=["Sub-Saharan Africa adds 2.11 bn", "The whole world adds only 2.02 bn"],
        note="Sub-Saharan Africa contributes MORE THAN 100% of the net growth of the world's population by\\n"
             "2100: it grows by more than the whole world, because the rest is contracting. Source: UN, WPP 2024."),
}

def fmt(value: float, unit: str, lang: str) -> str:
    """Deux décimales + unité, virgule décimale en français."""
    number = f"{value:.2f}".replace(".", ",") if lang == "fr" else f"{value:.2f}"
    return f"{number} {unit}"

def build_figure(y2024: list[float], y2100: list[float], lang: str) -> Figure:
    """Barres groupées 2024 (gris-bleu) vs 2100 (bleu), pour l'Afrique et le monde."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, bottom=0.25)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(y2024))
    width = 0.40
    ax.bar(x - width / 2, y2024, width=width, color=GREY_BLUE, zorder=3, label=text["y2024"])
    ax.bar(x + width / 2, y2100, width=width, color=nm.COLORS["blue"], zorder=3, label=text["y2100"])
    ax.set_ylim(0, 11)
    ax.set_yticks(range(0, 11, 2))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(x))
    ax.set_xticklabels(text["cats"], fontsize=24, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for xi, value in zip(x, y2024):
        ax.annotate(fmt(value, text["unit"], lang), (xi - width / 2, value), xytext=(0, 10),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=26, fontweight="bold", color=nm.COLORS["text"])
    for xi, value in zip(x, y2100):
        ax.annotate(fmt(value, text["unit"], lang), (xi + width / 2, value), xytext=(0, 10),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=26, fontweight="bold", color=nm.COLORS["blue2"])
    ax.text(0.5, 0.64, text["annot"][0], transform=ax.transAxes, ha="center", va="center",
            fontsize=24, fontweight="bold", color=nm.COLORS["amber"])
    ax.text(0.5, 0.565, text["annot"][1], transform=ax.transAxes, ha="center", va="center",
            fontsize=24, fontweight="bold", color=nm.COLORS["amber"])
    ax.legend(loc="upper left", fontsize=21, frameon=False, labelcolor=nm.COLORS["text"], handlelength=1.3)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(y2024, y2100, LANG)'''


# ── Assemblage ───────────────────────────────────────────────────────────────

FIGURES = [
    dict(name="fig01-japon-population-active",
         fig_fr="Le Japon a perdu un actif sur six",
         fig_en="Japan has lost one working-age adult in six",
         live=True, data=DATA_1, fig=FIG_1),
    dict(name="fig02-vitesse-vieillissement",
         fig_fr="Le vieillissement n'est pas un niveau, c'est une vitesse",
         fig_en="Ageing is not a level, it is a speed",
         live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-japon-denominateur",
         fig_fr="Tout dépend du dénominateur",
         fig_en="It all depends on the denominator",
         live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-dividende-non-automatique",
         fig_fr="Le même cadeau, deux destins",
         fig_en="The same gift, two destinies",
         live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-ou-souffle-le-vent",
         fig_fr="Le seul moteur démographique qui reste",
         fig_en="The only demographic engine left",
         live=False, data=DATA_5, fig=FIG_5),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "/home/claudeagent/cms-workspace/nmlab-figures-tools/out14")
    nb_kit.build_all(META, DIR, FIGURES)
