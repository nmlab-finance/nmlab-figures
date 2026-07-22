#!/usr/bin/env python3
"""Notebooks du chapitre 11 — « La croissance économique et son poids sur vos rendements ».

Sept figures : deux séries FRED en direct (PIB réel par habitant ; part des profits),
une trajectoire de composé calculée, et quatre figures à données EMBARQUÉES (non-FRED :
Banque mondiale pour le Japon, données de Shiller / Bernstein-Arnott / Dimson-Marsh-
Staunton pour la décomposition, la dilution et le nuage des décennies). Chaque notebook =
une seule cellule code (load_*() puis build_figure(...) -> Figure), style NMLab partagé.
"""

import sys

sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit


# ═════════════════════════════════════════════════════════════════════════════
# Figure 01 — le pays qui devait dépasser l'Amérique (données embarquées)
# ═════════════════════════════════════════════════════════════════════════════

DATA_01 = '''def load_japan_share() -> tuple[list[int], list[float]]:
    """PIB du Japon en % du PIB américain, 1980-2024 (dollars courants, Banque mondiale).
    Points relevés sur la figure ; pic 1995 = 73,8 %, fin 2024 = 14,3 %.
    Japan's GDP as a share of U.S. GDP, 1980-2024 (current dollars, World Bank)."""
    years = list(range(1980, 2025))
    share = [40.5, 39.0, 35.5, 35.0, 34.5, 33.5, 44.0, 48.5, 58.5, 61.0,
             55.5, 54.5, 59.0, 65.0, 68.5, 73.8, 65.0, 56.0, 46.0, 48.5,
             49.0, 43.0, 41.0, 40.5, 41.0, 38.0, 34.5, 32.0, 35.5, 38.5,
             40.5, 40.5, 39.5, 31.5, 27.5, 25.5, 27.0, 26.0, 25.5, 25.0,
             24.5, 24.0, 21.0, 17.0, 14.3]
    return years, share

years, share = load_japan_share()'''

FIG_01 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le pays qui devait dépasser l'Amérique",
        sub="PIB du Japon rapporté à celui des États-Unis, en dollars courants",
        ylab="PIB japonais, % du PIB américain",
        krach="krach de\\n1989-1990",
        peak="1995 : 73,8 %",
        trough="2024 : 14,3 %",
        note="Le Japon culmine à près des trois quarts de l'économie américaine en 1995 — cinq ans après\\n"
             "l'éclatement de sa bulle. La croissance passée ne dit rien de la suivante. Source : Banque mondiale (NY.GDP.MKTP.CD)."),
    "en": dict(
        title="The country that was meant to overtake America",
        sub="Japan's GDP relative to that of the United States, in current dollars",
        ylab="Japanese GDP, % of U.S. GDP",
        krach="1989-1990\\ncrash",
        peak="1995: 73.8%",
        trough="2024: 14.3%",
        note="Japan peaks at nearly three-quarters of the U.S. economy in 1995 — five years after\\n"
             "its bubble burst. Past growth says nothing about the next. Source: World Bank (NY.GDP.MKTP.CD)."),
}

def build_figure(years: list[int], share: list[float], lang: str) -> Figure:
    """Part du PIB japonais dans le PIB américain, avec le pic de 1995 et le point de 2024."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.078)
    ax.fill_between(years, share, color=nm.COLORS["blue"], alpha=0.14)
    ax.plot(years, share, color=nm.COLORS["blue"], linewidth=3.0)
    ax.axvline(1990, color=nm.COLORS["edge"], linestyle=(0, (2, 3)), linewidth=2.0)
    ax.text(1989, 63, text["krach"], ha="right", va="center", fontsize=20,
            color=nm.COLORS["muted"], linespacing=1.4)
    ax.scatter([1995], [73.8], s=150, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(text["peak"], xy=(1995, 73.8), xytext=(1999, 73.8), ha="left", va="center",
                fontsize=25, fontweight="bold", color=nm.COLORS["rose"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["rose"], lw=1.8))
    ax.scatter([2024], [14.3], s=150, color=nm.COLORS["amber"], zorder=5)
    ax.annotate(text["trough"], xy=(2024, 14.3), xytext=(2008, 10.5), ha="left", va="center",
                fontsize=25, fontweight="bold", color=nm.COLORS["amber"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["amber"], lw=1.8))
    ax.set_ylim(0, 84)
    ax.set_yticks(range(0, 81, 10))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(1979, 2026)
    ax.set_xticks(range(1980, 2021, 10))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(years, share, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 02 — la marée invisible : PIB réel par habitant (FRED en direct)
# ═════════════════════════════════════════════════════════════════════════════

DATA_02 = '''from pandas import Series

def load_gdp_per_capita() -> Series:
    """PIB réel par habitant des États-Unis (A939RX0Q048SBEA), en direct depuis FRED.
    U.S. real GDP per capita, live from FRED (chained 2017 dollars)."""
    return nm.load_fred("A939RX0Q048SBEA")

gdppc = load_gdp_per_capita()'''

FIG_02 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import NullFormatter

LABELS = {
    "fr": dict(
        title="La marée que personne ne voit monter",
        sub="Production réelle par habitant aux États-Unis, 1947-2025",
        ylab="PIB réel par habitant, $ de 2017 (éch. log)",
        mid="+1,98 % par an\\n— invisible chaque année",
        note="Deux pour cent par an pendant près de quatre-vingts ans : personne n'a jamais eu le sentiment de vivre\\n"
             "un miracle, et le pays produit plusieurs fois plus par habitant. Source : BEA via FRED (A939RX0Q048SBEA)."),
    "en": dict(
        title="The tide no one sees rising",
        sub="Real output per capita in the United States, 1947-2025",
        ylab="real GDP per capita, 2017 $ (log scale)",
        mid="+1.98% a year\\n— invisible each year",
        note="Two percent a year for nearly eighty years: no one ever felt they were living through a miracle,\\n"
             "and the country produces several times more per capita. Source: BEA via FRED (A939RX0Q048SBEA)."),
}

def money(value: float, lang: str) -> str:
    """Montant en dollars, formaté selon la langue / dollar amount, localized."""
    if lang == "fr":
        return f"{value:,.0f} $".replace(",", " ")
    return f"${value:,.0f}"

def build_figure(gdppc: Series, lang: str) -> Figure:
    """PIB réel par habitant en échelle log ; premier et dernier points marqués."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.12)
    ax.plot(gdppc.index, gdppc, color=nm.COLORS["blue"], linewidth=2.9)
    ax.set_yscale("log")
    ax.set_ylim(12500, 82000)
    ax.set_yticks([15000, 30000, 60000])
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(which="minor", left=False)
    ax.grid(which="minor", visible=False)
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    first_x, first_y = gdppc.index[0], gdppc.iloc[0]
    last_x, last_y = gdppc.index[-1], gdppc.iloc[-1]
    ax.scatter([first_x], [first_y], s=150, color="#c9d4e7", zorder=5)
    ax.scatter([last_x], [last_y], s=170, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(money(first_y, lang), xy=(first_x, first_y), xytext=(12, -34),
                textcoords="offset points", ha="left", va="center", fontsize=24,
                fontweight="bold", color="#c9d4e7")
    ax.annotate(money(last_y, lang), xy=(last_x, last_y), xytext=(-4, 34),
                textcoords="offset points", ha="right", va="center", fontsize=25,
                fontweight="bold", color=nm.COLORS["rose"])
    ax.text(0.34, 0.30, text["mid"], transform=ax.transAxes, ha="left", va="center",
            fontsize=27, fontweight="bold", color=nm.COLORS["text"], linespacing=1.5)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(gdppc, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 03 — la puissance du composé (schéma calculé, éditable)
# ═════════════════════════════════════════════════════════════════════════════

DATA_03 = '''def load_compounding() -> tuple[list[int], list[tuple[float, list[float]]]]:
    """Trois trajectoires d'une économie base 100 sur 70 ans, à 1 %, 2 % et 3 %/an.
    La seule « donnée » est le calcul du composé : 100·(1+g)^t.
    Three paths of a base-100 economy over 70 years, at 1%, 2% and 3% a year."""
    years = list(range(0, 71))
    paths = [(rate, [100 * (1 + rate) ** t for t in years]) for rate in (0.01, 0.02, 0.03)]
    return years, paths

years, paths = load_compounding()'''

FIG_03 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Deux points de croissance, un monde d'écart",
        sub="Ce que devient une économie de base 100 selon son rythme de croissance",
        xlab="années", ylab="richesse produite, base 100",
        leg=["1 %/an", "2 %/an", "3 %/an"],
        note="Sur une vie (70 ans), 3 %/an produit près de quatre fois plus que 1 %/an. Aucune décision de politique\\n"
             "économique n'a d'effet comparable — mais l'écart ne se voit pas d'une année sur l'autre."),
    "en": dict(
        title="Two points of growth, a world apart",
        sub="What a base-100 economy becomes according to its growth rate",
        xlab="years", ylab="output produced, base 100",
        leg=["1%/yr", "2%/yr", "3%/yr"],
        note="Over a lifetime (70 years), 3%/yr produces nearly four times more than 1%/yr. No economic-policy\\n"
             "decision has a comparable effect — but the gap never shows from one year to the next."),
}

def build_figure(years: list[int], paths: list, lang: str) -> Figure:
    """Trois courbes de composé (1 %, 2 %, 3 %), avec leur valeur finale annotée."""
    text = LABELS[lang]
    colors = ["#c9d4e7", nm.COLORS["blue"], nm.COLORS["rose"]]
    fig = nm.figure(height_px=1083)
    ax = nm.axes(fig, bottom=0.185)
    for (rate, values), color, label in zip(paths, colors, text["leg"]):
        ax.plot(years, values, color=color, linewidth=3.6, label=label)
        ax.annotate(f"{values[-1]:.0f}", xy=(years[-1], values[-1]), xytext=(12, 0),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=27, fontweight="bold", color=color)
    ax.set_xlim(0, 76)
    ax.set_xticks(range(0, 71, 10))
    ax.set_ylim(0, 850)
    ax.set_yticks(range(0, 801, 100))
    ax.set_xlabel(text["xlab"])
    ax.set_ylabel(text["ylab"])
    ax.legend(loc="upper left", fontsize=23, labelcolor=nm.COLORS["text"], frameon=True,
              facecolor=nm.COLORS["card"], edgecolor=nm.COLORS["edge"], borderpad=0.9, handlelength=1.6)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(years, paths, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 04 — d'où vient le rendement des actions (données embarquées)
# ═════════════════════════════════════════════════════════════════════════════

DATA_04 = '''def return_decomposition() -> list[float]:
    """Décomposition du rendement réel annuel des actions américaines 1900-2024 (points/an) :
    dividende versé, croissance réelle des bénéfices, ré-évaluation du multiple.
    Decomposition of the U.S. real annual equity return 1900-2024 (points/yr)."""
    return [4.03, 1.94, 0.37]

components = return_decomposition()'''

FIG_04 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="D'où vient vraiment le rendement des actions",
        sub="Décomposition du rendement réel annuel des actions américaines, 1900-2024",
        ylab="points de rendement réel par an",
        cats=["Dividendes\\nversés", "Croissance réelle\\ndes bénéfices", "Ré-évaluation\\ndu multiple"],
        value_labels=["4,03 pt", "1,94 pt", "0,37 pt"],
        note="Près des deux tiers du rendement viennent du dividende — pas de la croissance. Le multiple\\n"
             "(PER 15,0 → 23,7 en 124 ans) n'apporte que 0,37 point. Source : données de Robert Shiller."),
    "en": dict(
        title="Where the return on stocks really comes from",
        sub="Decomposition of the U.S. real annual equity return, 1900-2024",
        ylab="points of real return per year",
        cats=["Dividends\\npaid", "Real earnings\\ngrowth", "Multiple\\nre-rating"],
        value_labels=["4.03 pt", "1.94 pt", "0.37 pt"],
        note="Nearly two-thirds of the return comes from the dividend — not from growth. The multiple\\n"
             "(P/E 15.0 → 23.7 over 124 years) adds only 0.37 point. Source: Robert Shiller's data."),
}

def build_figure(components: list[float], lang: str) -> Figure:
    """Trois barres colorées : dividende, croissance des bénéfices, ré-évaluation."""
    text = LABELS[lang]
    fig = nm.figure(height_px=988)
    ax = nm.axes(fig, bottom=0.24)
    ax.grid(axis="x", visible=False)
    positions = range(len(components))
    colors = [nm.COLORS["blue"], nm.COLORS["amber"], nm.COLORS["rose"]]
    ax.bar(positions, components, width=0.62, color=colors, zorder=3)
    ax.set_ylim(0, 4.6)
    ax.set_yticks(range(0, 5))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 2.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, components, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 14), textcoords="offset points",
                    ha="center", va="bottom", fontsize=30, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(components, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 05 — la dilution (données embarquées, barres + flèche)
# ═════════════════════════════════════════════════════════════════════════════

DATA_05 = '''def dilution_gap() -> list[float]:
    """Croissance réelle annuelle 1929-2023 : PIB réel (l'économie) vs bénéfice réel
    par action (l'actionnaire), en % — l'écart est la dilution.
    Real annual growth 1929-2023: real GDP vs real earnings per share (%)."""
    return [3.19, 2.22]

bars = dilution_gap()'''

FIG_05 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le gâteau grossit, mais on redécoupe les parts",
        sub="Croissance de l'économie et croissance du bénéfice par action, 1929-2023",
        ylab="croissance réelle, %/an",
        cats=["PIB réel\\n(l'économie)", "Bénéfices réels par action\\n(l'actionnaire)"],
        value_labels=["3,19 %/an", "2,22 %/an"],
        gap="dilution\\n0,96 point/an",
        note="L'économie a crû d'un point de plus par an que le bénéfice par action : l'écart part aux entreprises\\n"
             "nouvelles et aux actions nouvellement émises. Sources : BEA, données de Robert Shiller."),
    "en": dict(
        title="The pie grows, but the slices are recut",
        sub="Growth of the economy and growth of earnings per share, 1929-2023",
        ylab="real growth, %/yr",
        cats=["Real GDP\\n(the economy)", "Real earnings per share\\n(the shareholder)"],
        value_labels=["3.19%/yr", "2.22%/yr"],
        gap="dilution\\n0.96 point/yr",
        note="The economy grew a point a year more than earnings per share: the gap goes to new firms\\n"
             "and newly issued shares. Sources: BEA, Robert Shiller's data."),
}

def build_figure(bars: list[float], lang: str) -> Figure:
    """Deux barres (PIB vs BPA) et une flèche mesurant la dilution."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1083)
    ax = nm.axes(fig, bottom=0.24)
    ax.grid(axis="x", visible=False)
    positions = range(len(bars))
    colors = [nm.COLORS["blue"], nm.COLORS["rose"]]
    ax.bar(positions, bars, width=0.5, color=colors, zorder=3)
    ax.set_ylim(0, 3.7)
    ax.set_yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.65, 2.2)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, bars, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 14), textcoords="offset points",
                    ha="center", va="bottom", fontsize=30, fontweight="bold", color=nm.COLORS["text"])
    ax.annotate("", xy=(1.5, bars[0]), xytext=(1.5, bars[1]),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["amber"], lw=2.6))
    ax.text(1.62, (bars[0] + bars[1]) / 2, text["gap"], ha="left", va="center",
            fontsize=25, fontweight="bold", color=nm.COLORS["amber"], linespacing=1.45)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(bars, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 06 — neuf décennies : le lien introuvable (nuage embarqué)
# ═════════════════════════════════════════════════════════════════════════════

DATA_06 = '''def decade_points() -> list[tuple[str, float, float, float, float]]:
    """Neuf décennies américaines : (décennie, croissance du PIB réel %/an,
    rendement réel des actions %/an, décalage x du libellé, décalage y du libellé).
    Points relevés sur la figure. / Nine U.S. decades read off the figure."""
    return [
        ("1930s", 1.0, 2.1, 0.0, -1.6),
        ("1940s", 5.6, 3.4, 0.0, 1.5),
        ("1950s", 4.2, 16.6, 0.0, 1.5),
        ("1960s", 4.5, 5.1, 0.0, 1.5),
        ("1970s", 3.2, -1.4, 0.0, -1.6),
        ("1980s", 3.1, 11.5, -0.2, 1.5),
        ("1990s", 3.2, 14.6, 0.12, 1.5),
        ("2000s", 1.9, -3.1, 0.0, 1.5),
        ("2010s", 2.4, 11.3, -0.15, 1.5),
    ]

points = decade_points()'''

FIG_06 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Neuf décennies américaines : le lien introuvable",
        sub="Croissance du PIB réel et rendement réel des actions, par décennie",
        xlab="croissance du PIB réel de la décennie, %/an",
        ylab="rendement réel des actions, %/an",
        corr="corrélation : 0,24",
        note="Les années 1930 cumulent la plus faible croissance et un rendement réel positif ; les années 1940,\\n"
             "la plus forte croissance et un rendement médiocre. Sources : BEA, données de Robert Shiller."),
    "en": dict(
        title="Nine American decades: the missing link",
        sub="Real GDP growth and real equity returns, by decade",
        xlab="real GDP growth of the decade, %/yr",
        ylab="real equity return, %/yr",
        corr="correlation: 0.24",
        note="The 1930s combine the weakest growth with a positive real return; the 1940s, the strongest\\n"
             "growth with a mediocre return. Sources: BEA, Robert Shiller's data."),
}

def build_figure(points: list, lang: str) -> Figure:
    """Nuage des neuf décennies (croissance vs rendement) et sa droite de régression."""
    text = LABELS[lang]
    x = np.array([p[1] for p in points])
    y = np.array([p[2] for p in points])
    fig = nm.figure(height_px=1121)
    ax = nm.axes(fig, left=0.078, bottom=0.19)
    ax.axhline(0, color=nm.COLORS["muted"], linestyle=(0, (1, 4)), linewidth=1.6, alpha=0.9)
    ax.scatter(x, y, s=340, color=nm.COLORS["blue"], zorder=3, linewidths=0)
    for name, gx, ry, dx, dy in points:
        ax.text(gx + dx, ry + dy, name, ha="center", va="center", fontsize=23,
                fontweight="bold", color=nm.COLORS["text"])
    slope, intercept = np.polyfit(x, y, 1)
    line_x = np.array([0.6, 6.0])
    ax.plot(line_x, intercept + slope * line_x, color=nm.COLORS["rose"],
            linestyle=(0, (6, 4)), linewidth=3.4, label=text["corr"])
    ax.set_xlim(0.5, 6.2)
    ax.set_xticks(range(1, 7))
    ax.set_ylim(-4.5, 19)
    ax.set_yticks([-2.5, 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5])
    ax.set_xlabel(text["xlab"])
    ax.set_ylabel(text["ylab"])
    ax.legend(loc="lower right", fontsize=23, labelcolor=nm.COLORS["text"], frameon=True,
              facecolor=nm.COLORS["card"], edgecolor=nm.COLORS["edge"], borderpad=0.8, handlelength=2.2)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(points, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 07 — la part des profits (FRED en direct : CPATAX / GDP)
# ═════════════════════════════════════════════════════════════════════════════

DATA_07 = '''from pandas import Series

def load_profit_share() -> Series:
    """Part des profits des sociétés après impôt (IVA et CCAdj inclus) dans le PIB,
    en direct depuis FRED : CPATAX (profits après impôt) rapporté à GDP (PIB nominal), en %.
    U.S. after-tax corporate profit share of GDP, live from FRED (CPATAX over GDP)."""
    profits = nm.load_fred("CPATAX")
    gdp = nm.load_fred("GDP")
    return (profits / gdp * 100).dropna()

share = load_profit_share()'''

FIG_07 = '''import matplotlib.dates as mdates
import pandas as pd
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="L'hypothèse qui ne tient plus",
        sub="Part des profits des sociétés américaines après impôt dans le PIB",
        ylab="profits après impôt, % du PIB",
        pre="moyenne {a}-1999 : {v} %",
        post="moyenne depuis 2000 : {v} %",
        record="record : {v} %",
        note="Toute la mécanique de la dilution suppose cette part STABLE. Elle est passée d'environ 6 % à 9 % en\\n"
             "moyenne depuis 2000, record fin 2025. Source : BEA via FRED (CPATAX — IVA et CCAdj inclus ; GDP)."),
    "en": dict(
        title="The assumption that no longer holds",
        sub="U.S. after-tax corporate profit share of GDP",
        ylab="after-tax profits, % of GDP",
        pre="average {a}-1999: {v}%",
        post="average since 2000: {v}%",
        record="record: {v}%",
        note="The whole dilution mechanism assumes this share is STABLE. It rose from about 6% to 9% on average\\n"
             "since 2000, a record in late 2025. Source: BEA via FRED (CPATAX — incl. IVA and CCAdj; GDP)."),
}

def num(value: float, lang: str, dec: int = 1) -> str:
    """Nombre localisé (virgule décimale en français) / localized number."""
    s = f"{value:.{dec}f}"
    return s.replace(".", ",") if lang == "fr" else s

def build_figure(share: Series, lang: str) -> Figure:
    """Part des profits (trimestrielle) avec les moyennes avant/après 2000 et le record."""
    text = LABELS[lang]
    split = pd.Timestamp("2000-01-01")
    pre, post = share.loc[:"1999"], share.loc["2000":]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig)
    ax.plot(share.index, share, color=nm.COLORS["blue"], linewidth=2.0)
    ax.plot([share.index[0], split], [pre.mean(), pre.mean()],
            color=nm.COLORS["text"], linestyle=(0, (7, 5)), linewidth=2.4)
    ax.plot([split, share.index[-1]], [post.mean(), post.mean()],
            color=nm.COLORS["rose"], linestyle=(0, (7, 5)), linewidth=2.4)
    ax.set_ylim(2, 12.6)
    ax.set_yticks(range(2, 13, 2))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.text(0.03, 0.94, text["pre"].format(a=share.index[0].year, v=num(pre.mean(), lang)),
            transform=ax.transAxes, fontsize=23, fontweight="bold", color=nm.COLORS["text"], va="top")
    ax.text(0.03, 0.865, text["post"].format(v=num(post.mean(), lang)),
            transform=ax.transAxes, fontsize=23, fontweight="bold", color=nm.COLORS["rose"], va="top")
    last_x, last_y = share.index[-1], share.iloc[-1]
    ax.annotate(text["record"].format(v=num(last_y, lang, 2)),
                xy=(last_x, last_y), xytext=(-260, 30), textcoords="offset points",
                ha="left", va="center", fontsize=25, fontweight="bold", color=nm.COLORS["amber"],
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["amber"], lw=1.8,
                                connectionstyle="arc3,rad=-0.3"))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(share, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Assemblage
# ═════════════════════════════════════════════════════════════════════════════

META = dict(
    num="11",
    title_fr="La croissance économique et son poids sur vos rendements de long terme",
    title_en="Economic Growth and What It Is Worth to Your Long-Term Returns",
    slug_fr="croissance-economique-rendements-long-terme",
    slug_en="economic-growth-long-term-returns",
)
DIR = "macro/11-croissance-rendements"

FIGURES = [
    dict(name="fig01-japon-etats-unis",
         fig_fr="Le pays qui devait dépasser l'Amérique",
         fig_en="The country that was meant to overtake America",
         live=False, data=DATA_01, fig=FIG_01),
    dict(name="fig02-maree-invisible",
         fig_fr="La marée que personne ne voit monter",
         fig_en="The tide no one sees rising",
         live=True, data=DATA_02, fig=FIG_02),
    dict(name="fig03-puissance-compose",
         fig_fr="Deux points de croissance, un monde d'écart",
         fig_en="Two points of growth, a world apart",
         live=False, data=DATA_03, fig=FIG_03),
    dict(name="fig04-origine-rendement",
         fig_fr="D'où vient vraiment le rendement des actions",
         fig_en="Where the return on stocks really comes from",
         live=False, data=DATA_04, fig=FIG_04),
    dict(name="fig05-dilution",
         fig_fr="Le gâteau grossit, mais on redécoupe les parts",
         fig_en="The pie grows, but the slices are recut",
         live=False, data=DATA_05, fig=FIG_05),
    dict(name="fig06-decennies-croissance-rendement",
         fig_fr="Neuf décennies américaines : le lien introuvable",
         fig_en="Nine American decades: the missing link",
         live=False, data=DATA_06, fig=FIG_06),
    dict(name="fig07-part-profits",
         fig_fr="L'hypothèse qui ne tient plus",
         fig_en="The assumption that no longer holds",
         live=True, data=DATA_07, fig=FIG_07),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out11")
    nb_kit.build_all(META, DIR, FIGURES)
