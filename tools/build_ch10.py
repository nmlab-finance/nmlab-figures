#!/usr/bin/env python3
"""Génère les notebooks du chapitre 10 — PIB réel et PIB nominal.

Convention « strict » : une seule cellule code par notebook, fonctions typées et
documentées (``load_*()`` puis ``build_figure(...) -> Figure``), bilingue via ``LANG``.
Voir ~/cms-workspace/nmlab-figures-tools/nb_kit.py et les recettes ch18/19/20 de
build_notebooks.py (chargement FRED, aires, barres, cartes, note dynamique)."""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="10",
    title_fr="PIB réel et PIB nominal : pourquoi corriger de l'inflation",
    title_en="Real GDP and Nominal GDP: Why Correct for Inflation",
    slug_fr="pib-reel-pib-nominal",
    slug_en="real-gdp-nominal-gdp",
)
DIR = "macro/10-pib-reel-nominal"


# ── Figure 01 — la récession invisible de 1974 (FRED GDPA/GDPCA, en direct) ────

DATA_1 = '''from pandas import Series

def load_growth() -> tuple[list[int], list[float], list[float]]:
    """Croissance annuelle du PIB américain nominal (GDPA) et réel (GDPCA), 1972-1976,
    calculée en direct depuis FRED (variation d'une année sur l'autre, en %).
    Annual growth of U.S. nominal (GDPA) and real (GDPCA) GDP, 1972-1976, live from FRED."""
    nominal = nm.load_fred("GDPA").pct_change() * 100
    real = nm.load_fred("GDPCA").pct_change() * 100
    years = list(range(1972, 1977))
    n = [round(float(nominal[nominal.index.year == y].iloc[0]), 1) for y in years]
    r = [round(float(real[real.index.year == y].iloc[0]), 1) for y in years]
    return years, n, r

years, nominal_growth, real_growth = load_growth()'''

FIG_1 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="1974 : la récession que le nominal ne voyait pas",
        sub="Croissance du PIB américain — en dollars courants et en volumes",
        ylab="croissance annuelle, %",
        legend_nom="PIB nominal (dollars courants)",
        legend_real="PIB réel (volumes)",
        recession="1974-1975 : récession",
        note="En 1974 et 1975, le PIB nominal progresse de 8 à 9 % l'an pendant que les volumes reculent :\\n"
             "toute la hausse — et davantage — n'était que des prix. Source : BEA via FRED (GDPA, GDPCA)."),
    "en": dict(
        title="1974: the recession the nominal did not see",
        sub="U.S. GDP growth — in current dollars and in volumes",
        ylab="annual growth, %",
        legend_nom="nominal GDP (current dollars)",
        legend_real="real GDP (volumes)",
        recession="1974-1975: recession",
        note="In 1974 and 1975 nominal GDP rises 8 to 9% a year while volumes shrink:\\n"
             "all the increase — and more — was nothing but prices. Source: BEA via FRED (GDPA, GDPCA)."),
}

def _pct(value: float, lang: str) -> str:
    """Étiquette de pourcentage signée, localisée (« +9,8 % » / « +9.8% »)."""
    body = f"{value:+.1f}".replace(".", ",") if lang == "fr" else f"{value:+.1f}"
    return body + (" %" if lang == "fr" else "%")

def build_figure(years: list[int], nominal: list[float], real: list[float], lang: str) -> Figure:
    """Barres groupées par année : PIB nominal (bleu) et PIB réel (rose), bande de récession 1974-75."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.axes(fig, bottom=0.16)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(years))
    width = 0.38
    ax.axvspan(1.5, 3.5, color=nm.COLORS["rose"], alpha=0.09, zorder=0)
    ax.bar(x - width / 2, nominal, width, color=nm.COLORS["blue"], label=text["legend_nom"], zorder=3)
    ax.bar(x + width / 2, real, width, color=nm.COLORS["rose"], label=text["legend_real"], zorder=3)
    ax.axhline(0, color=nm.COLORS["text"], lw=1.8, zorder=4)
    ax.set_ylim(-2.5, 16)
    ax.set_yticks(range(0, 16, 5))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, len(years) - 0.4)
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years], fontsize=24, color=nm.COLORS["muted"])
    ax.tick_params(axis="x", length=0)
    for pos, value in zip(x - width / 2, nominal):
        ax.annotate(_pct(value, lang), (pos, value), xytext=(0, 10), textcoords="offset points",
                    ha="center", va="bottom", fontsize=22, fontweight="bold", color=nm.COLORS["blue"])
    for pos, value in zip(x + width / 2, real):
        off, va = ((0, 10), "bottom") if value >= 0 else ((0, -12), "top")
        ax.annotate(_pct(value, lang), (pos, value), xytext=off, textcoords="offset points",
                    ha="center", va=va, fontsize=22, fontweight="bold", color=nm.COLORS["rose"])
    ax.text(2.5, 14.6, text["recession"], ha="center", va="center",
            fontsize=24, fontweight="bold", color=nm.COLORS["rose"])
    ax.legend(loc="upper left", frameon=False, fontsize=22, labelcolor=nm.COLORS["text"],
              handlelength=1.1, handleheight=1.1, borderaxespad=0.9)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(years, nominal_growth, real_growth, LANG)'''


# ── Figure 02 — un même « +5 % », trois économies (barres empilées, embarqué) ──

DATA_2 = '''def load_decompositions() -> tuple[list[float], list[float]]:
    """Trois lectures stylisées d'une même croissance nominale de +5 % : volumes (croissance
    réelle) et prix (inflation), en points de croissance. Exemple pédagogique, aucune source.
    Three stylized reads of the same +5% nominal growth: volumes and prices, in growth points."""
    volumes = [0.0, 3.0, -2.0]
    prices = [5.0, 2.0, 7.0]
    return volumes, prices

volumes, prices = load_decompositions()'''

FIG_2 = '''import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Patch

LABELS = {
    "fr": dict(
        title="Un même « +5 % nominal », trois économies différentes",
        sub="Croissance nominale ≈ croissance des volumes + hausse des prix",
        ylab="points de croissance",
        legend_vol="volumes (croissance réelle)",
        legend_price="prix (inflation)",
        cats=["Stagnation habillée", "Croissance saine", "Récession masquée"],
        nominal_line="croissance nominale affichée : +5 %",
        note="Le chiffre nominal additionne les volumes et les prix : il peut habiller une stagnation,\\n"
             "ou masquer une récession. Seule la décomposition dit laquelle. Exemple stylisé."),
    "en": dict(
        title="One « +5% nominal », three different economies",
        sub="Nominal growth ≈ volume growth + price rise",
        ylab="growth points",
        legend_vol="volumes (real growth)",
        legend_price="prices (inflation)",
        cats=["Dressed-up stagnation", "Healthy growth", "Hidden recession"],
        nominal_line="displayed nominal growth: +5%",
        note="The nominal figure adds volumes and prices: it can dress up a stagnation,\\n"
             "or hide a recession. Only the decomposition tells which. Stylized example."),
}

def _pct(value: float, lang: str) -> str:
    body = f"{value:+.1f}".replace(".", ",") if lang == "fr" else f"{value:+.1f}"
    return body + (" %" if lang == "fr" else "%")

def build_figure(volumes: list[float], prices: list[float], lang: str) -> Figure:
    """Barres empilées : volumes (bleu, depuis 0) et prix (rose, empilé sur les volumes positifs)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, bottom=0.135)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(volumes))
    width = 0.5
    for xi, vol, pr in zip(x, volumes, prices):
        ax.bar(xi, vol, width, color=nm.COLORS["blue"], zorder=3)
        ax.bar(xi, pr, width, bottom=max(vol, 0.0), color=nm.COLORS["rose"], zorder=3)
    ax.axhline(5, color=nm.COLORS["text"], lw=2.2, linestyle=(0, (8, 6)), zorder=5)
    ax.axhline(0, color=nm.COLORS["text"], lw=1.6, zorder=4)
    ax.text(-0.44, 5.35, text["nominal_line"], ha="left", va="bottom",
            fontsize=21, color=nm.COLORS["text"])
    for xi, vol, pr in zip(x, volumes, prices):
        base = max(vol, 0.0)
        ax.text(xi, base + pr / 2, _pct(pr, lang), ha="center", va="center",
                fontsize=26, fontweight="bold", color=nm.COLORS["bg"])
        if vol > 0:
            ax.text(xi, vol / 2, _pct(vol, lang), ha="center", va="center",
                    fontsize=26, fontweight="bold", color=nm.COLORS["bg"])
        elif vol < 0:
            ax.annotate(_pct(vol, lang), (xi, vol), xytext=(0, -12), textcoords="offset points",
                        ha="center", va="top", fontsize=26, fontweight="bold", color=nm.COLORS["blue"])
    ax.set_ylim(-3.5, 8.5)
    ax.set_yticks(range(-2, 9, 2))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, len(volumes) - 0.4)
    ax.set_xticks(x)
    ax.set_xticklabels(text["cats"], fontsize=23, color=nm.COLORS["muted"])
    ax.tick_params(axis="x", length=0)
    handles = [Patch(color=nm.COLORS["blue"], label=text["legend_vol"]),
               Patch(color=nm.COLORS["rose"], label=text["legend_price"])]
    ax.legend(handles=handles, loc="upper left", frameon=False, fontsize=22,
              labelcolor=nm.COLORS["text"], handlelength=1.1, handleheight=1.1, borderaxespad=0.9)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(volumes, prices, LANG)'''


# ── Figure 03 — un siècle de PIB (FRED GDPA/GDPCA, log, en direct) ────────────

DATA_3 = '''from pandas import Series

def load_gdp() -> tuple[Series, Series]:
    """PIB américain nominal (GDPA, dollars courants) et réel (GDPCA, dollars chaînés de 2017),
    séries annuelles depuis 1929, en direct depuis FRED.
    U.S. nominal (GDPA) and real (GDPCA) GDP, annual since 1929, live from FRED."""
    return nm.load_fred("GDPA"), nm.load_fred("GDPCA")

nominal, real = load_gdp()'''

FIG_3 = '''import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import NullFormatter
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Un siècle de PIB américain : deux courbes, deux histoires",
        sub="Avant l'année de base, le réel est au-dessus ; après, en dessous — l'écart, ce sont les prix",
        ylab="milliards de dollars, échelle log",
        legend_nom="PIB nominal (dollars courants)",
        legend_real="PIB réel (dollars chaînés de 2017)",
        base="2017 : année de base\\nnominal = réel",
        start_nom="1929 : 105 Mds courants",
        start_real="aux prix de 2017 : 1 191 Mds",
        note="En dollars courants, le PIB de 1929 vaut 105 milliards ; aux prix de 2017, 1 191 milliards.\\n"
             "La pente bleue mélange volumes et prix ; la rouge ne garde que les volumes. Source : BEA via FRED."),
    "en": dict(
        title="A century of U.S. GDP: two curves, two stories",
        sub="Before the base year, real sits above; after, below — the gap is prices",
        ylab="billions of dollars, log scale",
        legend_nom="nominal GDP (current dollars)",
        legend_real="real GDP (chained 2017 dollars)",
        base="2017: base year\\nnominal = real",
        start_nom="1929: $105bn current",
        start_real="at 2017 prices: $1,191bn",
        note="In current dollars, 1929 GDP is worth 105 billion; at 2017 prices, 1,191 billion.\\n"
             "The blue slope mixes volumes and prices; the red keeps only volumes. Source: BEA via FRED."),
}

def _at(series: Series, year: int):
    """Renvoie (date, valeur) du premier point de l'année ``year``."""
    mask = series.index.year == year
    return series.index[mask][0], float(series[mask].iloc[0])

def build_figure(nominal: Series, real: Series, lang: str) -> Figure:
    """Deux courbes en échelle log, 1929-2025, avec l'année de base 2017 et les points extrêmes."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    ax = nm.axes(fig, left=0.088)
    ax.plot(nominal.index, nominal, color=nm.COLORS["blue"], lw=3.2, label=text["legend_nom"], zorder=3)
    ax.plot(real.index, real, color=nm.COLORS["rose"], lw=3.2, label=text["legend_real"], zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(48, 42000)
    ax.set_yticks([100, 1000, 10000, 30000])
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(pd.Timestamp("1926-01-01"), pd.Timestamp("2033-01-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator(20))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    d29_dip, v29_dip = _at(nominal, 1933)
    d29_real, v29_real = _at(real, 1929)
    ax.annotate(text["start_nom"], xy=(d29_dip, v29_dip), xytext=(90, 34), textcoords="offset points",
                ha="left", va="center", fontsize=21, color=nm.COLORS["blue"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    ax.annotate(text["start_real"], xy=(d29_real, v29_real), xytext=(88, -18), textcoords="offset points",
                ha="left", va="center", fontsize=21, color=nm.COLORS["rose"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))

    d17, v17 = _at(nominal, 2017)
    ax.scatter([d17], [v17], s=150, color=nm.COLORS["text"], zorder=6)
    ax.annotate(text["base"], xy=(d17, v17), xytext=(-46, 92), textcoords="offset points",
                ha="center", va="center", fontsize=22, color=nm.COLORS["text"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=1.5))

    fmt = nm.thousands(lang)
    ax.annotate(fmt(nominal.iloc[-1], None), xy=(nominal.index[-1], nominal.iloc[-1]),
                xytext=(10, 4), textcoords="offset points", ha="left", va="center",
                fontsize=25, fontweight="bold", color=nm.COLORS["blue"])
    ax.annotate(fmt(real.iloc[-1], None), xy=(real.index[-1], real.iloc[-1]),
                xytext=(10, -2), textcoords="offset points", ha="left", va="center",
                fontsize=25, fontweight="bold", color=nm.COLORS["rose"])

    ax.legend(loc="lower right", frameon=False, fontsize=21, labelcolor=nm.COLORS["text"],
              handlelength=1.6, borderaxespad=1.2)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(nominal, real, LANG)'''


# ── Figure 04 — « en volume », mais aux prix de quelle année ? (cartes) ────────

DATA_4 = '''def toy_economy(lang: str) -> dict:
    """Contenu localisé du schéma « économie-jouet » à deux produits (baguettes, ordinateurs) :
    les deux cartes d'état du haut et les trois cartes-réponses du bas.
    Localized content of the two-good toy-economy diagram (two state cards, three answer cards)."""
    if lang == "fr":
        return dict(
            top=[("Année 1", ["100 baguettes à 1,00 €", "10 ordinateurs à 1 000 €", "PIB nominal : 10 100 €"]),
                 ("Dix ans plus tard", ["100 baguettes à 1,50 €", "25 ordinateurs à 480 €", "PIB nominal : 12 150 €"])],
            question="De combien les volumes ont-ils augmenté ?",
            answers=[("Aux prix de l'an 1", "+148,5 %", "(l'ordinateur pèse\\nson vieux prix fort)", nm.COLORS["blue"]),
                     ("Aux prix de l'an 10", "+145,5 %", "(l'ordinateur pèse\\nson prix effondré)", nm.COLORS["blue"]),
                     ("Indice chaîné", "≈ +147 %", "(base re-choisie\\nchaque année)", nm.COLORS["amber"])])
    return dict(
        top=[("Year 1", ["100 baguettes at €1.00", "10 computers at €1,000", "Nominal GDP: €10,100"]),
             ("Ten years later", ["100 baguettes at €1.50", "25 computers at €480", "Nominal GDP: €12,150"])],
        question="By how much did volumes rise?",
        answers=[("At year-1 prices", "+148.5%", "(the computer carries\\nits high old price)", nm.COLORS["blue"]),
                 ("At year-10 prices", "+145.5%", "(the computer carries\\nits collapsed price)", nm.COLORS["blue"]),
                 ("Chained index", "≈ +147%", "(base re-picked\\neach year)", nm.COLORS["amber"])])

economy = toy_economy(LANG)'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="« En volume », oui — mais aux prix de quelle année ?",
        sub="Économie-jouet à deux produits : la réponse dépend de l'année des prix figés",
        note="Deux bases, deux réponses : l'indice chaîné tranche en re-basant chaque année, puis en\\n"
             "enchaînant les maillons. Les États-Unis chaînent depuis 1996, l'Europe depuis les années 2000."),
    "en": dict(
        title="« In volume », yes — but at which year's prices?",
        sub="Two-good toy economy: the answer depends on which year's prices you freeze",
        note="Two bases, two answers: the chained index settles it by re-basing every year, then\\n"
             "linking the segments. The U.S. has chained since 1996, Europe since the 2000s."),
}

def build_figure(economy: dict, lang: str) -> Figure:
    """Schéma en cartes : deux états de l'économie (haut) puis trois réponses selon la base (bas)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1178)
    ax = nm.blank_axes(fig)
    cx_mid = nm.WIDTH_PX / 2

    top_y, top_h = 648, 300
    tops = [(95, 760), (892, 760)]
    for (cx, cw), (title, lines) in zip(tops, economy["top"]):
        nm.card(ax, cx, top_y, cw, top_h, edge=nm.COLORS["edge"], lw=2.4, radius=20)
        ax.text(cx + cw / 2, top_y + top_h - 62, title, ha="center", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        for i, line in enumerate(lines):
            ax.text(cx + cw / 2, top_y + top_h - 150 - i * 60, line, ha="center", va="center",
                    fontsize=25, color=nm.COLORS["text"])
    ax.annotate("", xy=(888, top_y + top_h / 2), xytext=(859, top_y + top_h / 2),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["text"], lw=2.6, mutation_scale=26))

    ax.text(cx_mid, 548, economy["question"], ha="center", va="center",
            fontsize=30, fontweight="bold", color=nm.COLORS["text"])

    bot_y, bot_h = 150, 300
    bots = [(78, 500), (624, 500), (1170, 500)]
    for (cx, cw), (title, value, detail, color) in zip(bots, economy["answers"]):
        nm.card(ax, cx, bot_y, cw, bot_h, edge=color, lw=2.6, radius=20)
        ax.text(cx + cw / 2, bot_y + bot_h - 66, title, ha="center", va="center",
                fontsize=27, fontweight="bold", color=color)
        ax.text(cx + cw / 2, bot_y + bot_h - 150, value, ha="center", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        ax.text(cx + cw / 2, bot_y + 78, detail, ha="center", va="center",
                fontsize=22, color=nm.COLORS["muted"], linespacing=1.5)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(economy, LANG)'''


# ── Figure 05 — Japon : nominal plat, volumes en hausse (FRED, en direct) ──────

DATA_5 = '''from pandas import Series

def load_japan() -> tuple[Series, Series]:
    """PIB nominal (JPNNGDP) et réel (JPNRGDPEXP) du Japon, trimestriels, en direct depuis FRED,
    ramenés en base 100 = moyenne 1995.
    Japan nominal and real GDP, quarterly, live from FRED, indexed to 100 = 1995 average."""
    nominal = nm.load_fred("JPNNGDP")
    real = nm.load_fred("JPNRGDPEXP")
    nominal = nominal / nominal[nominal.index.year == 1995].mean() * 100
    real = real / real[real.index.year == 1995].mean() * 100
    return nominal, real

japan_nominal, japan_real = load_japan()'''

FIG_5 = '''import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Japon : vingt ans de nominal plat, des volumes en hausse",
        sub="PIB nominal et PIB réel du Japon, base 100 = moyenne 1995, données trimestrielles",
        ylab="indice, base 100 en 1995",
        legend_nom="PIB nominal", legend_real="PIB réel",
        base_line="niveau de 1995 = 100",
        ann_real="2015 : réel +18,5 %",
        ann_nom="2015 : nominal +3,5 %\\ndepuis 1995",
        ann_2022="2022- : l'inflation revient,\\nle nominal décolle",
        note="La déflation inverse l'illusion : le nominal sous-estime l'activité. En 2025, le niveau des prix\\n"
             "du PIB japonais dépasse celui de 1995 de moins de 1 %. Source : Cabinet Office via FRED."),
    "en": dict(
        title="Japan: twenty years of flat nominal, rising volumes",
        sub="Japan's nominal and real GDP, indexed to 100 = 1995 average, quarterly data",
        ylab="index, 1995 = 100",
        legend_nom="nominal GDP", legend_real="real GDP",
        base_line="1995 level = 100",
        ann_real="2015: real +18.5%",
        ann_nom="2015: nominal +3.5%\\nsince 1995",
        ann_2022="2022-: inflation returns,\\nthe nominal takes off",
        note="Deflation flips the illusion: the nominal understates activity. In 2025, Japan's GDP price level\\n"
             "stands less than 1% above its 1995 level. Source: Cabinet Office via FRED."),
}

def _at(series: Series, year: int, quarter_index: int = 0):
    """(date, valeur) d'un trimestre d'une année donnée."""
    mask = series.index.year == year
    return series.index[mask][quarter_index], float(series[mask].iloc[quarter_index])

def build_figure(nominal: Series, real: Series, lang: str) -> Figure:
    """Deux courbes trimestrielles en base 100 (1995) : nominal (bleu) plat, réel (rose) en hausse."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    ax = nm.axes(fig, left=0.072)
    ax.axhline(100, color=nm.COLORS["muted"], linestyle="--", lw=1.6, zorder=1)
    line_real, = ax.plot(real.index, real, color=nm.COLORS["rose"], lw=2.6, label=text["legend_real"], zorder=3)
    line_nom, = ax.plot(nominal.index, nominal, color=nm.COLORS["blue"], lw=2.6, label=text["legend_nom"], zorder=4)
    ax.set_ylim(87, 133)
    ax.set_yticks(range(90, 131, 10))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(pd.Timestamp("1993-06-01"), pd.Timestamp("2026-09-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.text(pd.Timestamp("2007-06-01"), 101.4, text["base_line"], ha="left", va="bottom",
            fontsize=20, color=nm.COLORS["muted"])

    d_real, v_real = _at(real, 2015)
    ax.annotate(text["ann_real"], xy=(d_real, v_real), xytext=(pd.Timestamp("2004-01-01"), 124),
                ha="left", va="center", fontsize=22, color=nm.COLORS["rose"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["rose"], lw=1.4))
    d_nom, v_nom = _at(nominal, 2015)
    ax.annotate(text["ann_nom"], xy=(d_nom, v_nom), xytext=(pd.Timestamp("2007-06-01"), 90),
                ha="center", va="center", fontsize=22, color=nm.COLORS["blue"], linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["blue"], lw=1.4))
    d_22, v_22 = _at(nominal, 2023)
    ax.annotate(text["ann_2022"], xy=(d_22, v_22), xytext=(pd.Timestamp("2015-06-01"), 130),
                ha="left", va="center", fontsize=22, color=nm.COLORS["blue"], linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["blue"], lw=1.4))

    ax.legend(handles=[line_nom, line_real], loc="upper left", frameon=False, fontsize=23,
              labelcolor=nm.COLORS["text"], handlelength=1.6, borderaxespad=1.0)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(japan_nominal, japan_real, LANG)'''


# ── Figure 06 — la dette qui fond (FRED GFDGDPA188S, aire, en direct) ─────────

DATA_6 = '''from pandas import Series

def load_debt() -> Series:
    """Dette fédérale américaine brute en % du PIB (GFDGDPA188S), série annuelle depuis 1939,
    en direct depuis FRED.
    U.S. gross federal debt as % of GDP, annual since 1939, live from FRED."""
    return nm.load_fred("GFDGDPA188S")

debt = load_debt()'''

FIG_6 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La dette ne se rembourse pas toujours : parfois, elle fond",
        sub="Dette fédérale américaine en % du PIB — un ratio nominal sur un PIB nominal",
        ylab="dette fédérale brute, % du PIB",
        ann_1946="1946 : 119 %", ann_1974="1974 : 31 %", ann_2025="2025 : 121 %",
        mid="divisée par quatre en trente ans,\\nsans grands excédents : le PIB\\nnominal courait plus vite",
        note="Le numérateur (la dette) est figé en dollars d'époque ; le dénominateur (PIB nominal) gonfle\\n"
             "avec les volumes ET les prix. L'inflation rembourse en silence. Source : OMB via FRED."),
    "en": dict(
        title="Debt is not always repaid: sometimes it melts",
        sub="U.S. federal debt as % of GDP — a nominal ratio over a nominal GDP",
        ylab="gross federal debt, % of GDP",
        ann_1946="1946: 119%", ann_1974="1974: 31%", ann_2025="2025: 121%",
        mid="cut by four in thirty years,\\nwith no big surpluses: nominal\\nGDP was running faster",
        note="The numerator (the debt) is frozen in the dollars of its era; the denominator (nominal GDP)\\n"
             "swells with volumes AND prices. Inflation repays in silence. Source: OMB via FRED."),
}

def _at(series: Series, year: int):
    mask = series.index.year == year
    return series.index[mask][0], float(series[mask].iloc[0])

def build_figure(debt: Series, lang: str) -> Figure:
    """Aire remplie du ratio dette/PIB, 1939-2025, avec les jalons 1946, 1974 et 2025."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    ax = nm.axes(fig, left=0.078)
    ax.fill_between(debt.index, debt, color=nm.COLORS["blue"], alpha=0.16, zorder=1)
    ax.plot(debt.index, debt, color=nm.COLORS["blue"], lw=3.2, zorder=3)
    ax.set_ylim(0, 145)
    ax.set_yticks(range(0, 141, 20))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.02)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    d46, v46 = _at(debt, 1946)
    ax.scatter([d46], [v46], s=130, color=nm.COLORS["text"], zorder=5)
    ax.annotate(text["ann_1946"], xy=(d46, v46), xytext=(58, 14), textcoords="offset points",
                ha="left", va="center", fontsize=24, fontweight="bold", color=nm.COLORS["text"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    d74, v74 = _at(debt, 1974)
    ax.scatter([d74], [v74], s=130, color=nm.COLORS["text"], zorder=5)
    ax.annotate(text["ann_1974"], xy=(d74, v74), xytext=(0, -78), textcoords="offset points",
                ha="center", va="center", fontsize=24, fontweight="bold", color=nm.COLORS["text"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    d25, v25 = _at(debt, 2025)
    ax.scatter([d25], [v25], s=130, color=nm.COLORS["text"], zorder=5)
    ax.annotate(text["ann_2025"], xy=(d25, v25), xytext=(-30, 46), textcoords="offset points",
                ha="center", va="center", fontsize=24, fontweight="bold", color=nm.COLORS["text"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))

    ax.text(0.30, 0.44, text["mid"], transform=ax.transAxes, ha="center", va="center",
            fontsize=23, color=nm.COLORS["text"], linespacing=1.5)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(debt, LANG)'''


# ── Figure 07 — l'épargnant nominal/réel (intérêts composés, embarqué) ────────

DATA_7 = '''def load_savings() -> dict:
    """Trajectoires de 100 € placés à 6 %/an sur 25 ans : valeur nominale et pouvoir d'achat
    sous 2 %, 5 % et 8 % d'inflation (intérêts composés, aucune source externe).
    €100 invested at 6%/yr for 25 years: nominal value and purchasing power under 2/5/8% inflation."""
    years = list(range(26))
    nominal = [100 * 1.06 ** t for t in years]
    real = {infl: [100 * 1.06 ** t / (1 + infl) ** t for t in years] for infl in (0.02, 0.05, 0.08)}
    return dict(years=years, nominal=nominal, real=real)

savings = load_savings()'''

FIG_7 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le relevé affichera 429 € dans les quatre cas",
        sub="100 € placés à 6 % par an pendant 25 ans, selon l'inflation traversée",
        xlab="années", ylab="euros",
        legend_nom="valeur nominale (le relevé)",
        legend_i2="pouvoir d'achat, inflation 2 %",
        legend_i5="pouvoir d'achat, inflation 5 %",
        legend_i8="pouvoir d'achat, inflation 8 %",
        base="mise de départ : 100 €",
        note="À 8 % d'inflation, le placement qui « rapporte » 6 % appauvrit : 63 € de pouvoir d'achat\\n"
             "au bout de 25 ans. Rendement réel ≈ rendement nominal moins inflation."),
    "en": dict(
        title="The statement will read €429 in all four cases",
        sub="€100 invested at 6% a year for 25 years, by the inflation you live through",
        xlab="years", ylab="euros",
        legend_nom="nominal value (the statement)",
        legend_i2="purchasing power, 2% inflation",
        legend_i5="purchasing power, 5% inflation",
        legend_i8="purchasing power, 8% inflation",
        base="starting stake: €100",
        note="At 8% inflation, an investment that « pays » 6% makes you poorer: €63 of purchasing power\\n"
             "after 25 years. Real return ≈ nominal return minus inflation."),
}

def _eur(value: float, lang: str) -> str:
    return f"{value:.0f} €" if lang == "fr" else f"€{value:.0f}"

def build_figure(savings: dict, lang: str) -> Figure:
    """Une courbe nominale (bleu) et trois courbes de pouvoir d'achat (2/5/8 %) sur 25 ans."""
    text = LABELS[lang]
    years = savings["years"]
    nominal = savings["nominal"]
    real = savings["real"]
    fig = nm.figure(height_px=1140)
    ax = nm.axes(fig, left=0.075, bottom=0.155)

    ax.axhline(100, color=nm.COLORS["muted"], linestyle=":", lw=1.6, zorder=1)
    ax.text(13, 108, text["base"], ha="center", va="bottom", fontsize=20, color=nm.COLORS["muted"])

    ax.plot(years, nominal, color=nm.COLORS["blue"], lw=3.4, zorder=6, label=text["legend_nom"])
    ax.plot(years, real[0.02], color=nm.COLORS["text"], lw=3.0, dashes=(6, 4), zorder=4, label=text["legend_i2"])
    ax.plot(years, real[0.05], color=nm.COLORS["amber"], lw=3.0, dashes=(9, 5), zorder=4, label=text["legend_i5"])
    ax.plot(years, real[0.08], color=nm.COLORS["rose"], lw=3.0, zorder=5, label=text["legend_i8"])

    ends = [(nominal, nm.COLORS["blue"]), (real[0.02], nm.COLORS["text"]),
            (real[0.05], nm.COLORS["amber"]), (real[0.08], nm.COLORS["rose"])]
    for serie, color in ends:
        ax.annotate(_eur(serie[-1], lang), xy=(years[-1], serie[-1]), xytext=(10, 0),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=23, fontweight="bold", color=color)

    ax.set_xlim(0, 29)
    ax.set_ylim(0, 445)
    ax.set_xticks(range(0, 26, 5))
    ax.set_yticks(range(0, 401, 100))
    ax.set_xlabel(text["xlab"])
    ax.set_ylabel(text["ylab"])
    ax.legend(loc="upper left", frameon=False, fontsize=21, labelcolor=nm.COLORS["text"],
              handlelength=2.2, borderaxespad=1.0)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(savings, LANG)'''


# ── Figure 08 — cinq réflexes réel/nominal (cartes empilées) ──────────────────

DATA_8 = '''def reflexes(lang: str) -> list[tuple[str, str, str]]:
    """Les cinq réflexes de lecture réel/nominal : (titre, sous-titre, couleur du liseré).
    Bleu = ce qui est réel / la méthode ; rose = les pièges du nominal.
    The five real/nominal reading reflexes: (title, subtitle, edge color)."""
    if lang == "fr":
        return [
            ("Les gros titres de croissance sont réels",
             "les niveaux (« 30 762 milliards ») et les ratios (dette/PIB), eux, sont nominaux", nm.COLORS["blue"]),
            ("Sous forte inflation, le nominal ne dit plus rien",
             "Turquie 2022 : +106 % en nominal, +5,4 % en volume — tout le reste est prix", nm.COLORS["rose"]),
            ("Comparer deux dates, c'est comparer en réel",
             "ou déflater soi-même : valeur nominale divisée par un indice de prix", nm.COLORS["blue"]),
            ("Vos rendements aussi sont nominaux",
             "soustrayez l'inflation avant de vous réjouir — 6 % sous 8 % d'inflation appauvrit", nm.COLORS["rose"]),
            ("Un « réel » dépend de son déflateur",
             "PIB, IPC, PCE : paniers différents, réponses différentes — module 4", nm.COLORS["blue"]),
        ]
    return [
        ("Headline growth numbers are real",
         "levels (« 30,762 billion ») and ratios (debt/GDP), though, are nominal", nm.COLORS["blue"]),
        ("Under high inflation, the nominal says nothing",
         "Turkey 2022: +106% nominal, +5.4% in volume — all the rest is prices", nm.COLORS["rose"]),
        ("Comparing two dates means comparing in real terms",
         "or deflate yourself: nominal value divided by a price index", nm.COLORS["blue"]),
        ("Your returns are nominal too",
         "subtract inflation before celebrating — 6% under 8% inflation impoverishes", nm.COLORS["rose"]),
        ("A « real » depends on its deflator",
         "GDP, CPI, PCE: different baskets, different answers — module 4", nm.COLORS["blue"]),
    ]

rows = reflexes(LANG)'''

FIG_8 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Cinq réflexes devant un chiffre en euros ou en dollars",
        sub="La première question ne change jamais : réel ou nominal ?",
        note="À coller au-dessus de l'écran : un chiffre sans son déflateur est une opinion sur les prix."),
    "en": dict(
        title="Five reflexes in front of a figure in euros or dollars",
        sub="The first question never changes: real or nominal?",
        note="Tape it above your screen: a figure without its deflator is an opinion about prices."),
}

def build_figure(rows: list[tuple[str, str, str]], lang: str) -> Figure:
    """Cinq cartes empilées, liseré alterné (bleu/rose) : titre en gras + précision en dessous."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1216)
    ax = nm.blank_axes(fig)
    cx = nm.WIDTH_PX / 2
    card_x, card_w = 90, 1567
    card_h, gap, top_edge0 = 150, 27, 962
    for i, (title, subtitle, color) in enumerate(rows):
        top_edge = top_edge0 - i * (card_h + gap)
        y = top_edge - card_h
        nm.card(ax, card_x, y, card_w, card_h, edge=color, lw=2.6, radius=18)
        ax.text(cx, y + card_h * 0.62, title, ha="center", va="center",
                fontsize=29, fontweight="bold", color=color)
        ax.text(cx, y + card_h * 0.27, subtitle, ha="center", va="center",
                fontsize=23, color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(rows, LANG)'''


# ── Assemblage ───────────────────────────────────────────────────────────────

FIGURES = [
    dict(name="fig01-recession-invisible", live=True, data=DATA_1, fig=FIG_1,
         fig_fr="1974 : la récession que le nominal ne voyait pas",
         fig_en="1974: the recession the nominal did not see"),
    dict(name="fig02-prix-volumes", live=False, data=DATA_2, fig=FIG_2,
         fig_fr="Un même « +5 % nominal », trois économies différentes",
         fig_en="One « +5% nominal », three different economies"),
    dict(name="fig03-siecle-nominal-reel", live=True, data=DATA_3, fig=FIG_3,
         fig_fr="Un siècle de PIB américain : deux courbes, deux histoires",
         fig_en="A century of U.S. GDP: two curves, two stories"),
    dict(name="fig04-fabrique-pib-reel", live=False, data=DATA_4, fig=FIG_4,
         fig_fr="« En volume », oui — mais aux prix de quelle année ?",
         fig_en="« In volume », yes — but at which year's prices?"),
    dict(name="fig05-japon-nominal-reel", live=True, data=DATA_5, fig=FIG_5,
         fig_fr="Japon : vingt ans de nominal plat, des volumes en hausse",
         fig_en="Japan: twenty years of flat nominal, rising volumes"),
    dict(name="fig06-dette-nominal", live=True, data=DATA_6, fig=FIG_6,
         fig_fr="La dette ne se rembourse pas toujours : parfois, elle fond",
         fig_en="Debt is not always repaid: sometimes it melts"),
    dict(name="fig07-epargnant-nominal-reel", live=False, data=DATA_7, fig=FIG_7,
         fig_fr="Le relevé affichera 429 € dans les quatre cas",
         fig_en="The statement will read €429 in all four cases"),
    dict(name="fig08-reflexes", live=False, data=DATA_8, fig=FIG_8,
         fig_fr="Cinq réflexes devant un chiffre en euros ou en dollars",
         fig_en="Five reflexes in front of a figure in euros or dollars"),
]

if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "/home/claudeagent/cms-workspace/out10")
    nb_kit.build_all(META, DIR, FIGURES)
