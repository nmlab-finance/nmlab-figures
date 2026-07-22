#!/usr/bin/env python3
"""Génère les notebooks du chapitre 9 — Comprendre le PIB.

Convention « strict » : une seule cellule code par notebook, fonctions typées et
documentées (``load_*()`` puis ``build_figure(...) -> Figure``), bilingue via ``LANG``.
Voir ~/cms-workspace/nmlab-figures-tools/nb_kit.py et les recettes ch18/19/20 de
build_notebooks.py (chargement FRED, aires, barres, cartes, note dynamique)."""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="9",
    title_fr="Comprendre le PIB : la mesure de la richesse produite par un pays",
    title_en="Understanding GDP: The Measure of the Wealth a Country Produces",
    slug_fr="comprendre-le-pib",
    slug_en="understanding-gdp",
)
DIR = "macro/09-comprendre-pib"


# ── Figure 01 — un siècle de PIB nominal (FRED GDPA, log, en direct) ───────────

DATA_1 = '''from pandas import Series

def load_nominal_gdp() -> Series:
    """PIB nominal annuel des États-Unis (GDPA), en dollars courants, en direct de FRED.
    U.S. annual nominal GDP (GDPA), current dollars, live from FRED."""
    return nm.load_fred("GDPA")

gdp = load_nominal_gdp()'''

FIG_1 = '''import matplotlib.ticker as mticker
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Un siècle dans une courbe",
        sub="PIB nominal des États-Unis, {a}-{b} — échelle logarithmique",
        ylab="milliards de dollars courants (échelle log)",
        kuznets="1934 — le Sénat reçoit\\nle rapport Kuznets",
        note="Source : BEA via FRED, série GDPA (dollars courants) — millésime du 15 juillet 2026.\\n"
             "Dollars courants : l'inflation explique une large part de la pente — voir le chapitre 10."),
    "en": dict(
        title="A century in one curve",
        sub="U.S. nominal GDP, {a}-{b} — log scale",
        ylab="billions of current dollars (log scale)",
        kuznets="1934 — the Senate receives\\nthe Kuznets report",
        note="Source: BEA via FRED, GDPA series (current dollars) — vintage of July 15, 2026.\\n"
             "Current dollars: inflation accounts for much of the slope — see chapter 10."),
}

def build_figure(gdp: Series, lang: str) -> Figure:
    """Un siècle de PIB nominal en échelle log, avec trois repères annotés."""
    text = LABELS[lang]
    first_date, first_val = gdp.index[0], gdp.iloc[0]
    last_date, last_val = gdp.index[-1], gdp.iloc[-1]
    k_date = gdp[gdp.index.year == 1934].index[0]
    k_val = gdp[gdp.index.year == 1934].iloc[0]
    multiple = round(last_val / first_val / 100) * 100
    if lang == "fr":
        first_lbl = f"{first_date.year} : {first_val:,.0f} Mds $".replace(",", " ")
        last_lbl = (f"{last_date.year} : {last_val:,.0f} Mds $".replace(",", " ")
                    + f"\\n(≈ {multiple:.0f} fois {first_date.year}, en dollars courants)")
    else:
        first_lbl = f"{first_date.year}: ${first_val:,.0f}bn"
        last_lbl = (f"{last_date.year}: ${last_val:,.0f}bn"
                    + f"\\n(≈ {multiple:,.0f} times {first_date.year}, in current dollars)")

    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.092)
    ax.plot(gdp.index, gdp, color=nm.COLORS["blue"], linewidth=3.2)
    ax.set_yscale("log")
    ax.set_ylim(50, 45000)
    ax.set_yticks([100, 1000, 10000])
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.yaxis.set_minor_locator(mticker.NullLocator())
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ticks = [pd.Timestamp(f"{y}-01-01") for y in (1930, 1950, 1970, 1990, 2010)]
    ticks.append(last_date)
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_title("")
    ax.annotate(text["kuznets"], xy=(k_date, k_val), xytext=(48, 168),
                textcoords="offset points", ha="left", va="center", fontsize=22,
                color=nm.COLORS["text"], linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    ax.annotate(first_lbl, xy=(first_date, first_val), xytext=(78, -46),
                textcoords="offset points", ha="left", va="center", fontsize=22,
                color=nm.COLORS["text"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    ax.annotate(last_lbl, xy=(last_date, last_val), xytext=(-548, -120),
                textcoords="offset points", ha="left", va="center", fontsize=22,
                color=nm.COLORS["text"], linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    nm.header(fig, text["title"], text["sub"].format(a=first_date.year, b=last_date.year))
    nm.footer(fig, text["note"])
    return fig

build_figure(gdp, LANG)'''


# ── Figure 02 — la valeur ajoutée, étage par étage (schéma) ───────────────────

DATA_2 = '''def value_chain(lang: str) -> dict:
    """Les libellés localisés de la chaîne blé → farine → baguette et de ses encarts.
    Localized labels of the wheat → flour → baguette chain and its call-outs."""
    if lang == "fr":
        return dict(
            stages=["L'agriculteur\\nvend le blé\\n0,20 €",
                    "Le meunier\\nvend la farine\\n0,60 €",
                    "Le boulanger\\nvend la baguette\\n1,50 €"],
            va=["valeur ajoutée : 0,20 €", "valeur ajoutée : 0,40 €", "valeur ajoutée : 0,90 €"],
            sum_line="PIB = 0,20 + 0,40 + 0,90 = 1,50 €   —   exactement le prix du produit final",
            trap="Additionner les ventes (0,20 + 0,60 + 1,50 = 2,30 €) compterait le blé trois fois : double compte")
    return dict(
        stages=["The farmer\\nsells the wheat\\n€0.20",
                "The miller\\nsells the flour\\n€0.60",
                "The baker\\nsells the baguette\\n€1.50"],
        va=["value added: €0.20", "value added: €0.40", "value added: €0.90"],
        sum_line="GDP = 0.20 + 0.40 + 0.90 = €1.50   —   exactly the price of the final product",
        trap="Adding up all sales (0.20 + 0.60 + 1.50 = €2.30) would count the wheat three times: double counting")

chain = value_chain(LANG)'''

FIG_2 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="La valeur ajoutée, étage par étage",
               sub="du blé à la baguette : ce que chaque étage ajoute — et rien d'autre",
               note="Exemple stylisé (sans consommations intermédiaires pour l'agriculteur)."),
    "en": dict(title="Value added, stage by stage",
               sub="from wheat to baguette: what each stage adds — and nothing else",
               note="Stylized example (no intermediate inputs for the farmer)."),
}

def build_figure(chain: dict, lang: str) -> Figure:
    """Schéma : trois étages reliés par des flèches, leurs valeurs ajoutées, deux bandeaux."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 430, 126, 102
    centers = [x0 + i * (card_w + gap) + card_w / 2 for i in range(3)]

    # Étages (cartes bleues) et flèches de liaison
    top_top, top_bot = 760, 513
    for cx, label in zip(centers, chain["stages"]):
        nm.card(ax, cx - card_w / 2, top_bot, card_w, top_top - top_bot,
                edge=nm.COLORS["blue"], lw=2.6, radius=22)
        for k, line in enumerate(label.split("\\n")):
            ax.text(cx, (top_top + top_bot) / 2 + 46 - k * 46, line, ha="center", va="center",
                    fontsize=28, color=nm.COLORS["text"])
    for i in range(2):
        x_from = centers[i] + card_w / 2 + 10
        x_to = centers[i + 1] - card_w / 2 - 10
        ax.annotate("", xy=(x_to, (top_top + top_bot) / 2), xytext=(x_from, (top_top + top_bot) / 2),
                    arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["blue"], lw=3.0,
                                    mutation_scale=26))

    # Encarts « valeur ajoutée » (cartes discrètes)
    va_top, va_bot = 485, 399
    for cx, label in zip(centers, chain["va"]):
        nm.card(ax, cx - card_w / 2, va_bot, card_w, va_top - va_bot,
                edge=nm.COLORS["edge"], lw=2.0, radius=18)
        ax.text(cx, (va_top + va_bot) / 2, label, ha="center", va="center",
                fontsize=25, color=nm.COLORS["muted"])

    # Bandeau bleu (la somme) et bandeau rose (le double compte)
    band_x, band_w = x0, centers[-1] + card_w / 2 - x0
    nm.card(ax, band_x, 228, band_w, 100, edge=nm.COLORS["blue"], lw=2.6, radius=22)
    ax.text(band_x + band_w / 2, 278, text_sum(chain), ha="center", va="center",
            fontsize=29, fontweight="bold", color=nm.COLORS["text"])
    nm.card(ax, band_x, 90, band_w, 100, edge=nm.COLORS["rose"], lw=2.6, radius=22)
    ax.text(band_x + band_w / 2, 140, chain["trap"], ha="center", va="center",
            fontsize=23, color=nm.COLORS["rose"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

def text_sum(chain: dict) -> str:
    """Le texte du bandeau de somme (défini à part pour la lisibilité)."""
    return chain["sum_line"]

build_figure(chain, LANG)'''


# ── Figure 03 — trois routes, un même sommet (schéma en colonnes) ─────────────

DATA_3 = '''def approaches(lang: str) -> list:
    """Les trois routes du PIB, chaque colonne = (titre, [(libellé, couleur, poids)…]).
    The three roads to GDP, each column = (title, [(label, color, weight)…])."""
    blue, rose, edge = nm.COLORS["blue"], nm.COLORS["rose"], nm.COLORS["edge"]
    if lang == "fr":
        return [
            ("PRODUCTION", [("+ impôts nets\\nsur les produits", edge, 0.24),
                            ("Somme des\\nvaleurs ajoutées", blue, 0.76)]),
            ("DÉPENSE", [("Solde extérieur X − M (±)", rose, 0.19),
                         ("Dépense publique G", blue, 0.23),
                         ("Investissement I", blue, 0.23),
                         ("Consommation C", blue, 0.35)]),
            ("REVENU", [("Impôts nets de\\nsubventions", edge, 0.24),
                        ("Profits et\\nrevenus mixtes", blue, 0.37),
                        ("Salaires", blue, 0.39)]),
        ]
    return [
        ("OUTPUT", [("+ net taxes\\non products", edge, 0.24),
                    ("Sum of\\nvalue added", blue, 0.76)]),
        ("EXPENDITURE", [("External balance X − M (±)", rose, 0.19),
                         ("Government G", blue, 0.23),
                         ("Investment I", blue, 0.23),
                         ("Consumption C", blue, 0.35)]),
        ("INCOME", [("Taxes net of\\nsubsidies", edge, 0.24),
                    ("Profits and\\nmixed income", blue, 0.37),
                    ("Wages", blue, 0.39)]),
    ]

columns = approaches(LANG)'''

FIG_3 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Trois routes, un même sommet",
               sub="ce qui est produit = ce qui est dépensé = ce qui est gagné",
               banner="trois découpages, un même total — à l'écart statistique près",
               note="Les instituts confrontent les trois approches pour caler leurs comptes."),
    "en": dict(title="Three roads, one summit",
               sub="what is produced = what is spent = what is earned",
               banner="three ways to slice it, one and the same total — up to a statistical discrepancy",
               note="Statistical offices confront the three approaches to pin their accounts down."),
}

def build_figure(columns: list, lang: str) -> Figure:
    """Schéma : trois colonnes de même hauteur, découpées en segments empilés."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1007)
    ax = nm.blank_axes(fig)

    col_w, gap, x0 = 455, 101, 90
    y_top, y_bot = 613, 152
    inner_gap = 12
    centers = [x0 + i * (col_w + gap) + col_w / 2 for i in range(3)]

    for cx, (title, segments) in zip(centers, columns):
        total_w = sum(w for _, _, w in segments)
        usable = (y_top - y_bot) - inner_gap * (len(segments) - 1)
        cursor = y_top
        for label, color, weight in segments:
            h = usable * weight / total_w
            nm.card(ax, cx - col_w / 2, cursor - h, col_w, h, edge=color, lw=2.4, radius=18)
            for k, line in enumerate(label.split("\\n")):
                n = len(label.split("\\n"))
                ax.text(cx, cursor - h / 2 + (n - 1) * 24 - k * 48, line,
                        ha="center", va="center", fontsize=26, color=nm.COLORS["text"])
            cursor -= h + inner_gap
        ax.text(cx, 92, title, ha="center", va="center", fontsize=30,
                fontweight="bold", color=nm.COLORS["muted"])

    ax.plot([x0, centers[-1] + col_w / 2], [y_top + 22, y_top + 22],
            linestyle=(0, (7, 6)), color=nm.COLORS["muted"], lw=1.6)
    ax.text(centers[1], y_top + 62, text["banner"], ha="center", va="center",
            fontsize=25, color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(columns, LANG)'''


# ── Figure 04 — pour 100 dollars de PIB (FRED, barres horizontales, en direct) ─

DATA_4 = '''from pandas import Series

def load_weights() -> list[float]:
    """Poids moyens 2025 de C, I, G et (X − M) dans le PIB américain, en % (FRED, en direct).
    2025 average weights of C, I, G and net exports in U.S. GDP, live from FRED."""
    gdp = nm.load_fred("GDP")
    g25 = gdp[gdp.index.year == 2025]
    weights = []
    for code in ("PCEC", "GPDI", "GCE", "NETEXP"):
        s = nm.load_fred(code)
        s25 = s[s.index.year == 2025]
        n = min(len(s25), len(g25))
        weights.append(float((s25.values[:n] / g25.values[:n] * 100).mean()))
    return weights

weights = load_weights()'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Pour 100 dollars de PIB américain",
        sub="poids moyen de chaque poste de la dépense en 2025",
        cats=["Consommation des ménages (C)", "Investissement privé (I)",
              "Dépenses et invest. publics (G)", "Exportations nettes (X − M)"],
        hint="les quatre postes se somment à 100 %",
        note="Sources : BEA via FRED (PCEC, GPDI, GCE, NETEXP, GDP), moyenne des quatre trimestres de 2025."),
    "en": dict(
        title="For every 100 dollars of U.S. GDP",
        sub="average weight of each spending block in 2025",
        cats=["Household consumption (C)", "Private investment (I)",
              "Government purchases (G)", "Net exports (X − M)"],
        hint="the four blocks sum to 100%",
        note="Sources: BEA via FRED (PCEC, GPDI, GCE, NETEXP, GDP), average of the four quarters of 2025."),
}

def pct(value: float, lang: str) -> str:
    """Étiquette de pourcentage à une décimale, localisée."""
    sign = "−" if value < 0 else ""
    body = f"{abs(value):.1f}".replace(".", ",") if lang == "fr" else f"{abs(value):.1f}"
    return f"{sign}{body} %" if lang == "fr" else f"{sign}{body}%"

def build_figure(weights: list[float], lang: str) -> Figure:
    """Barres horizontales : C, I, G en bleu, exportations nettes en rose (négatif)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=988)
    ax = nm.axes(fig, left=0.315, right=0.965, bottom=0.14)
    ax.grid(axis="y", visible=False)
    positions = [3, 2, 1, 0]
    colors = [nm.COLORS["blue"], nm.COLORS["blue"], nm.COLORS["blue"], nm.COLORS["rose"]]
    ax.barh(positions, weights, height=0.62, color=colors, zorder=3)
    ax.axvline(0, color=nm.COLORS["muted"], linewidth=1.4, alpha=0.9)
    ax.set_xlim(-6, 78)
    ax.set_xticks(range(0, 71, 10))
    ax.set_ylim(-0.7, 3.7)
    ax.set_yticks(positions)
    ax.set_yticklabels(text["cats"], fontsize=24, color=nm.COLORS["text"])
    ax.tick_params(axis="y", length=0)
    for pos, value in zip(positions, weights):
        colour = nm.COLORS["rose"] if value < 0 else nm.COLORS["text"]
        ax.text(value + 1.3 if value >= 0 else 1.3, pos, pct(value, lang),
                va="center", ha="left", fontsize=26, fontweight="bold", color=colour)
    ax.text(77, 0.6, text["hint"], ha="right", va="center", fontsize=23,
            fontstyle="italic", color=nm.COLORS["muted"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(weights, LANG)'''


# ── Figure 05 — un même PIB, trois lectures (FRED GDPC1, barres groupées) ──────

DATA_5 = '''from pandas import DataFrame

def load_readings() -> DataFrame:
    """Les cinq derniers trimestres du PIB réel (GDPC1) lus de trois façons, en % (FRED, direct).
    The last five quarters of real GDP read three ways, in %, live from FRED."""
    gdp = nm.load_fred("GDPC1")
    qoq = gdp.pct_change(1) * 100
    annualized = ((1 + gdp.pct_change(1)) ** 4 - 1) * 100
    yoy = gdp.pct_change(4) * 100
    table = DataFrame({"qoq": qoq, "annualized": annualized, "yoy": yoy}).dropna().tail(5)
    return table

readings = load_readings()'''

FIG_5 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Un même PIB, trois vitesses de lecture",
        sub="PIB réel américain : la même réalité, trois conventions d'affichage",
        ylab="%",
        legend=["variation t/t", "rythme annualisé", "glissement sur un an"],
        note="Le rythme annualisé ≈ la variation trimestrielle composée sur quatre trimestres (convention américaine).\\n"
             "Source : BEA via FRED (GDPC1) — millésime du 15 juillet 2026."),
    "en": dict(
        title="One GDP, three reading speeds",
        sub="U.S. real GDP: the same reality under three display conventions",
        ylab="%",
        legend=["quarter-on-quarter", "annualized pace", "year-over-year"],
        note="The annualized pace ≈ the quarterly change compounded over four quarters (U.S. convention).\\n"
             "Source: BEA via FRED (GDPC1) — vintage of July 15, 2026."),
}

def quarter_labels(index, lang: str) -> list[str]:
    """Étiquettes de trimestre localisées (T1 2025 / Q1 2025)."""
    prefix = "T" if lang == "fr" else "Q"
    return [f"{prefix}{(d.month - 1) // 3 + 1} {d.year}" for d in index]

def num(value: float, lang: str) -> str:
    """Nombre à une décimale, signe « − », virgule décimale en français."""
    sign = "−" if value < 0 else ""
    body = f"{abs(value):.1f}".replace(".", ",") if lang == "fr" else f"{abs(value):.1f}"
    return f"{sign}{body}"

def build_figure(readings: "DataFrame", lang: str) -> Figure:
    """Barres groupées par trimestre : variation t/t, rythme annualisé, glissement annuel."""
    text = LABELS[lang]
    light = "#a7c4e2"
    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig, bottom=0.14)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(readings))
    width = 0.27
    series = [("qoq", light), ("annualized", nm.COLORS["blue"]), ("yoy", nm.COLORS["rose"])]
    for (col, colour), label, offset in zip(series, text["legend"], (-width, 0, width)):
        values = readings[col].values
        ax.bar(x + offset, values, width, color=colour, label=label, zorder=3)
        for xi, v in zip(x + offset, values):
            above = v >= 0
            ax.annotate(num(v, lang), (xi, v), xytext=(0, 8 if above else -8),
                        textcoords="offset points", ha="center",
                        va="bottom" if above else "top", fontsize=20, fontweight="bold",
                        color=nm.COLORS["text"] if above else nm.COLORS["rose"])
    ax.axhline(0, color=nm.COLORS["muted"], linewidth=1.4, alpha=0.9)
    ax.set_ylim(-1.4, 5.4)
    ax.set_yticks(range(-1, 6))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, len(readings) - 0.4)
    ax.set_xticks(x)
    ax.set_xticklabels(quarter_labels(readings.index, lang), fontsize=23, color=nm.COLORS["muted"])
    ax.tick_params(axis="x", length=0)
    ax.legend(loc="upper left", frameon=False, fontsize=23, labelcolor=nm.COLORS["text"],
              handlelength=1.1, handleheight=1.1, borderaxespad=0.9)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(readings, LANG)'''


# ── Figure 06 — deux classements, deux histoires (FMI, embarqué) ──────────────

DATA_6 = '''def imf_rankings(lang: str) -> dict:
    """PIB total et PIB par habitant 2024 (FMI, WEO avril 2026), valeurs lues, non-FRED.
    Total GDP and GDP per capita 2024 (IMF WEO), read-off values, not on FRED."""
    if lang == "fr":
        total = [("États-Unis", 29298), ("Chine", 18945), ("Allemagne", 4684),
                 ("Japon", 4190), ("Inde", 3761), ("France", 3161)]
        per_capita = [("États-Unis", 86173), ("Allemagne", 56087), ("France", 46054),
                      ("Japon", 33820), ("Chine", 13453), ("Inde", 2592)]
    else:
        total = [("United States", 29298), ("China", 18945), ("Germany", 4684),
                 ("Japan", 4190), ("India", 3761), ("France", 3161)]
        per_capita = [("United States", 86173), ("Germany", 56087), ("France", 46054),
                      ("Japan", 33820), ("China", 13453), ("India", 2592)]
    return dict(total=total, per_capita=per_capita)

rankings = imf_rankings(LANG)'''

FIG_6 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Deux classements, deux histoires",
        sub="le poids économique n'est pas le niveau de vie",
        left="PIB 2024, en milliards de dollars",
        right="PIB par habitant 2024, en dollars",
        note="Source : FMI, base World Economic Outlook, avril 2026 — année 2024, dollars courants.\\n"
             "En parité de pouvoir d'achat (PPA), la Chine dépasse les États-Unis depuis le milieu des années 2010."),
    "en": dict(
        title="Two rankings, two stories",
        sub="economic weight is not living standards",
        left="GDP 2024, billions of dollars",
        right="GDP per person 2024, dollars",
        note="Source: IMF, World Economic Outlook database, April 2026 — year 2024, current dollars.\\n"
             "In purchasing-power-parity (PPP) terms, China has been ahead of the United States since the mid-2010s."),
}

def group(value: float, lang: str) -> str:
    """Grand nombre avec séparateur de milliers localisé."""
    return f"{value:,.0f}".replace(",", " ") if lang == "fr" else f"{value:,.0f}"

def build_figure(rankings: dict, lang: str) -> Figure:
    """Deux panneaux à barres horizontales : PIB total (bleu) et PIB par habitant (rose)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)

    def panel(rect: list, title: str, rows: list, colour: str) -> None:
        ax = fig.add_axes(rect)
        names = [n for n, _ in rows]
        values = [v for _, v in rows]
        positions = list(range(len(values)))
        ax.barh(positions, values, height=0.62, color=colour, zorder=3)
        ax.invert_yaxis()
        ax.set_yticks(positions)
        ax.set_yticklabels(names, fontsize=23, color=nm.COLORS["text"])
        ax.set_xlim(0, max(values) * 1.32)
        ax.set_xticks([])
        ax.tick_params(axis="y", length=0)
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(nm.COLORS["edge"])
            spine.set_linewidth(1.5)
        for pos, value in zip(positions, values):
            ax.text(value + max(values) * 0.02, pos, group(value, lang),
                    va="center", ha="left", fontsize=23, color=nm.COLORS["text"])
        ax.set_title(title, color=nm.COLORS["muted"], fontsize=25, pad=20)

    panel([0.13, 0.155, 0.35, 0.55], text["left"], rankings["total"], nm.COLORS["blue"])
    panel([0.60, 0.155, 0.35, 0.55], text["right"], rankings["per_capita"], nm.COLORS["rose"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(rankings, LANG)'''


# ── Figure 07 — l'œil du PIB : dans / hors du champ (schéma deux colonnes) ─────

DATA_7 = '''def scope(lang: str) -> tuple:
    """Deux colonnes : (en-tête, couleur, cinq cartes) pour ce qui est dans / hors du PIB.
    Two columns: (header, color, five cards) for what is inside / outside GDP."""
    if lang == "fr":
        inside = ("DANS LE PIB", nm.COLORS["blue"],
                  ["Production vendue :\\nbiens et services marchands",
                   "Services publics\\n(comptés à leur coût)",
                   "Loyers « imputés » aux\\npropriétaires occupants",
                   "Investissement, y compris\\nR&D et logiciels",
                   "Économie souterraine :\\nestimée (drogue incluse, UE)"])
        outside = ("HORS DU PIB", nm.COLORS["rose"],
                   ["Travail domestique\\net bénévolat",
                    "Ventes d'occasion\\n(hors marge du revendeur)",
                    "Plus-values boursières\\net immobilières",
                    "Loisir, temps libre,\\nservices numériques gratuits",
                    "Épuisement de la nature\\n(jamais déduit)"])
    else:
        inside = ("INSIDE GDP", nm.COLORS["blue"],
                  ["Marketed output:\\ngoods and services sold",
                   "Public services\\n(counted at cost)",
                   "Rents “imputed” to\\nowner-occupiers",
                   "Investment, including\\nR&D and software",
                   "Underground economy:\\nestimated (drugs included, EU)"])
        outside = ("OUTSIDE GDP", nm.COLORS["rose"],
                   ["Housework\\nand volunteering",
                    "Second-hand sales\\n(net of dealer margins)",
                    "Capital gains on stocks\\nand housing",
                    "Leisure, free time,\\nfree digital services",
                    "Depletion of nature\\n(never deducted)"])
    return inside, outside

columns = scope(LANG)'''

FIG_7 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="L'œil du PIB",
               sub="la « frontière de la production » : ce qui entre dans le compte, ce qui reste dehors",
               note="Frontière fixée par les normes internationales des comptes nationaux (SNA, SEC) pour rester comparable."),
    "en": dict(title="GDP's field of vision",
               sub="the “production boundary”: what makes it into the account, what stays out",
               note="The boundary is set by international national-accounts standards (SNA, ESA) to stay comparable."),
}

def build_figure(columns: tuple, lang: str) -> Figure:
    """Schéma : deux colonnes coiffées d'un onglet, cinq cartes empilées chacune."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    ax = nm.blank_axes(fig)

    col_w = 740
    x0 = [105, 902]
    card_h, gap, first_top = 112, 29, 846
    for (name, colour, cards), x in zip(columns, x0):
        cx = x + col_w / 2
        # onglet d'en-tête
        head_w = 430
        nm.card(ax, cx - head_w / 2, 852, head_w, 63, edge=colour, lw=2.6, radius=18)
        ax.text(cx, 883, name, ha="center", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["text"])
        for i, label in enumerate(cards):
            top = first_top - i * (card_h + gap)
            nm.card(ax, x, top - card_h, col_w, card_h, edge=colour, lw=2.4, radius=18)
            lines = label.split("\\n")
            for k, line in enumerate(lines):
                ax.text(cx, top - card_h / 2 + (len(lines) - 1) * 22 - k * 44, line,
                        ha="center", va="center", fontsize=26, color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(columns, LANG)'''


# ── Figure 08 — la part des profits dans le PIB (FRED CP/GDP, en direct) ───────

DATA_8 = '''from pandas import Series

def load_profit_share() -> Series:
    """Profits des sociétés américaines après impôt (CP) en % du PIB (GDP), en direct de FRED.
    U.S. after-tax corporate profits as a share of GDP, live from FRED."""
    profits = nm.load_fred("CP")
    gdp = nm.load_fred("GDP")
    return (profits / gdp * 100).dropna()

share = load_profit_share()'''

FIG_8 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La part des profits dans le gâteau",
        sub="profits des sociétés américaines après impôt, en % du PIB",
        ylab="% du PIB",
        note="Sources : BEA via FRED (CP, GDP) — millésime du 15 juillet 2026.\\n"
             "Les profits suivent le PIB nominal de loin : leur part oscille du simple au triple selon les décennies."),
    "en": dict(
        title="Profits' slice of the pie",
        sub="U.S. after-tax corporate profits, as a share of GDP",
        ylab="% of GDP",
        note="Sources: BEA via FRED (CP, GDP) — vintage of July 15, 2026.\\n"
             "Profits track nominal GDP only loosely: their share swings threefold across decades."),
}

def build_figure(share: Series, lang: str) -> Figure:
    """Part des profits dans le PIB : ligne bleue, moyenne en pointillés, creux et pic annotés."""
    text = LABELS[lang]
    mean = share.mean()
    min_date, min_val = share.idxmin(), share.min()
    last_date, last_val = share.index[-1], share.iloc[-1]
    last_q = (last_date.month - 1) // 3 + 1
    if lang == "fr":
        mean_lbl = f"moyenne {share.index[0].year}-{last_date.year} : {mean:.1f} %".replace(".", ",")
        min_lbl = f"{min_date.year} : {min_val:.1f} %".replace(".", ",")
        prefix = "début" if last_q <= 2 else "fin"
        last_lbl = f"{prefix} {last_date.year} : {last_val:.1f} %".replace(".", ",")
    else:
        mean_lbl = f"{share.index[0].year}-{last_date.year} average: {mean:.1f}%"
        min_lbl = f"{min_date.year}: {min_val:.1f}%"
        prefix = "early" if last_q <= 2 else "late"
        last_lbl = f"{prefix} {last_date.year}: {last_val:.1f}%"

    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig, left=0.082)
    ax.axhline(mean, color=nm.COLORS["muted"], linewidth=1.8, linestyle=(0, (7, 6)))
    ax.plot(share.index, share, color=nm.COLORS["blue"], linewidth=2.6)
    ax.set_ylim(2, 14)
    ax.set_yticks(range(2, 15, 2))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.text(share.index[-1], mean + 0.25, mean_lbl, ha="right", va="bottom",
            fontsize=21, color=nm.COLORS["muted"])
    ax.annotate(min_lbl, xy=(min_date, min_val), xytext=(70, -46),
                textcoords="offset points", ha="left", va="center", fontsize=22,
                color=nm.COLORS["text"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    ax.annotate(last_lbl, xy=(last_date, last_val), xytext=(-6, 72),
                textcoords="offset points", ha="right", va="center", fontsize=22,
                color=nm.COLORS["text"],
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(share, LANG)'''


# ── Assemblage ───────────────────────────────────────────────────────────────

FIGURES = [
    dict(name="fig01-pib-siecle", fig_fr="Un siècle dans une courbe",
         fig_en="A century in one curve", live=True, data=DATA_1, fig=FIG_1),
    dict(name="fig02-valeur-ajoutee", fig_fr="La valeur ajoutée, étage par étage",
         fig_en="Value added, stage by stage", live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-trois-approches", fig_fr="Trois routes, un même sommet",
         fig_en="Three roads, one summit", live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-cent-dollars", fig_fr="Pour 100 dollars de PIB américain",
         fig_en="For every 100 dollars of U.S. GDP", live=True, data=DATA_4, fig=FIG_4),
    dict(name="fig05-trois-lectures", fig_fr="Un même PIB, trois vitesses de lecture",
         fig_en="One GDP, three reading speeds", live=True, data=DATA_5, fig=FIG_5),
    dict(name="fig06-comparer-pays", fig_fr="Deux classements, deux histoires",
         fig_en="Two rankings, two stories", live=False, data=DATA_6, fig=FIG_6),
    dict(name="fig07-champ-hors-champ", fig_fr="L'œil du PIB",
         fig_en="GDP's field of vision", live=False, data=DATA_7, fig=FIG_7),
    dict(name="fig08-part-profits", fig_fr="La part des profits dans le gâteau",
         fig_en="Profits' slice of the pie", live=True, data=DATA_8, fig=FIG_8),
]

if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "/home/claudeagent/cms-workspace/out9")
    nb_kit.build_all(META, DIR, FIGURES)
