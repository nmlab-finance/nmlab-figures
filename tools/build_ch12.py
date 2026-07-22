#!/usr/bin/env python3
"""Génère les notebooks du chapitre 12 — Productivité et croissance de long terme.

Convention « strict » : une seule cellule code par notebook, fonctions typées et
documentées (``load_*()`` puis ``build_figure(...) -> Figure``), bilingue via ``LANG``.
Voir ~/cms-workspace/nmlab-figures-tools/nb_kit.py et les recettes ch18/19/20 de
build_notebooks.py (chargement FRED, aires, barres, note dynamique)."""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="12",
    title_fr="Productivité et croissance de long terme : la variable qui décide de tout",
    title_en="Productivity and Long-Run Growth: The Variable That Decides Everything",
    slug_fr="productivite-et-croissance-long-terme",
    slug_en="productivity-and-long-term-growth",
)
DIR = "macro/12-productivite-croissance-long-terme"


# ── Figure 01 — le niveau de la productivité horaire (FRED OPHNFB, en direct) ──

DATA_1 = '''from pandas import Series

def load_productivity() -> Series:
    """Production par heure travaillée du secteur privé non agricole (OPHNFB),
    indice 2017 = 100, en direct depuis FRED.
    Nonfarm business sector real output per hour of all persons, live from FRED."""
    return nm.load_fred("OPHNFB")

productivity = load_productivity()'''

FIG_1 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le grand enrichissement, heure par heure",
        sub="Production par heure, secteur privé non agricole, États-Unis",
        ylab="production par heure travaillée (indice 2017 = 100)",
        multiple="× 5,2 en une vie de travail",
        detail="ce qui prenait 1 heure en 1947\\ndemande 11 min 30 aujourd'hui",
        start="indice 22,5\\n(1947)",
        end="indice 118\\n(2025)",
        note="Une même heure de travail produit cinq fois plus qu'en 1947 — c'est toute la richesse en plus.\\n"
             "Source : BLS via FRED (OPHNFB)."),
    "en": dict(
        title="The great enrichment, hour by hour",
        sub="Output per hour, nonfarm business sector, United States",
        ylab="output per hour worked (index 2017 = 100)",
        multiple="× 5.2 in one working life",
        detail="what took 1 hour in 1947\\ntakes 11 min 30 today",
        start="index 22.5\\n(1947)",
        end="index 118\\n(2025)",
        note="One and the same hour of work produces five times more than in 1947 — that is all the added wealth.\\n"
             "Source: BLS via FRED (OPHNFB)."),
}

def build_figure(productivity: Series, lang: str) -> Figure:
    """Niveau de la productivité horaire depuis 1947, tracé en aire remplie."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.092)
    ax.fill_between(productivity.index, productivity, color=nm.COLORS["blue"], alpha=0.14)
    ax.plot(productivity.index, productivity, color=nm.COLORS["blue"], linewidth=3.4)
    first_date, first_val = productivity.index[0], productivity.iloc[0]
    last_date, last_val = productivity.index[-1], productivity.iloc[-1]
    ax.scatter([first_date, last_date], [first_val, last_val],
               s=110, color=nm.COLORS["blue"], zorder=5, clip_on=False)
    ax.set_ylim(0, 125)
    ax.set_yticks(range(0, 121, 20))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.text(0.055, 0.90, text["multiple"], transform=ax.transAxes, fontsize=26,
            fontweight="bold", color=nm.COLORS["text"], va="top")
    ax.text(0.055, 0.79, text["detail"], transform=ax.transAxes, fontsize=21.5,
            color=nm.COLORS["muted"], va="top", linespacing=1.5)
    ax.annotate(text["start"], xy=(first_date, first_val), xytext=(72, 92),
                textcoords="offset points", ha="center", va="center", fontsize=21,
                color=nm.COLORS["muted"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=1.6))
    ax.annotate(text["end"], xy=(last_date, last_val), xytext=(-150, -10),
                textcoords="offset points", ha="center", va="center", fontsize=23,
                fontweight="bold", color=nm.COLORS["blue2"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["blue2"], lw=1.8))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(productivity, LANG)'''


# ── Figure 02 — les vagues de la productivité (barres groupées, embarqué) ──────

DATA_2 = '''def load_waves() -> tuple[list[float], list[float]]:
    """Croissance annuelle moyenne (%) de la productivité horaire et de la PTF, par période
    (valeurs publiées, calculées sur les séries OPHNFB et MFPNFBS de FRED).
    Average annual growth (%) of labor productivity and TFP, by era."""
    labor = [2.8, 1.44, 3.0, 1.46, 2.18]
    tfp = [1.88, 0.30, 1.51, 0.53, 1.04]
    return labor, tfp

labor, tfp = load_waves()'''

FIG_2 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Les vagues de la productivité",
        sub="Croissance par période — et le trou noir de 1973-1995",
        ylab="croissance annuelle moyenne, %",
        legend_labor="productivité horaire",
        legend_tfp="productivité globale (PTF)",
        cats=["Âge d'or\\n1948-73", "Ralentissement\\n1973-95", "Boom info.\\n1995-05",
              "2ᵉ ralentiss.\\n2005-19", "Reprise ?\\n2019-25"],
        labor_labels=["2,8 %", "1,4 %", "3,0 %", "1,5 %", "2,2 %"],
        tfp_labels=["1,88 %", "0,30 %", "1,51 %", "0,53 %", "1,04 %"],
        note="La PTF (l'efficacité pure) s'effondre à 0,3 %/an en 1973-95 : le « paradoxe de Solow », l'informatique\\n"
             "partout sauf dans les chiffres. Puis le rebond de 1995-2005. Source : BLS via FRED (OPHNFB, MFPNFBS)."),
    "en": dict(
        title="The waves of productivity",
        sub="Growth by era — and the black hole of 1973-1995",
        ylab="average annual growth, %",
        legend_labor="labor productivity",
        legend_tfp="total factor productivity (TFP)",
        cats=["Golden age\\n1948-73", "Slowdown\\n1973-95", "IT boom\\n1995-05",
              "2nd slowdown\\n2005-19", "Recovery?\\n2019-25"],
        labor_labels=["2.8%", "1.4%", "3.0%", "1.5%", "2.2%"],
        tfp_labels=["1.88%", "0.30%", "1.51%", "0.53%", "1.04%"],
        note="TFP (pure efficiency) collapses to 0.3%/yr in 1973-95: the « Solow paradox », computers everywhere\\n"
             "but in the numbers. Then the 1995-2005 rebound. Source: BLS via FRED (OPHNFB, MFPNFBS)."),
}

def build_figure(labor: list[float], tfp: list[float], lang: str) -> Figure:
    """Barres groupées par période : productivité horaire (bleu) et PTF (orange)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1083)
    ax = nm.axes(fig, bottom=0.22)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(labor))
    width = 0.38
    ax.bar(x - width / 2, labor, width, color=nm.COLORS["blue"],
           label=text["legend_labor"], zorder=3)
    ax.bar(x + width / 2, tfp, width, color=nm.COLORS["amber"],
           label=text["legend_tfp"], zorder=3)
    ax.set_ylim(0, 3.5)
    ax.set_yticks([i / 2 for i in range(8)])
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, len(labor) - 0.4)
    ax.set_xticks(x)
    ax.set_xticklabels(text["cats"], fontsize=20, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(x - width / 2, labor, text["labor_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 10), textcoords="offset points",
                    ha="center", va="bottom", fontsize=22, fontweight="bold", color=nm.COLORS["blue"])
    for pos, value, label in zip(x + width / 2, tfp, text["tfp_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 10), textcoords="offset points",
                    ha="center", va="bottom", fontsize=22, fontweight="bold", color=nm.COLORS["amber"])
    ax.legend(loc="upper right", frameon=False, fontsize=22, labelcolor=nm.COLORS["text"],
              handlelength=1.1, handleheight=1.1, borderaxespad=0.8)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(labor, tfp, LANG)'''


# ── Figure 03 — le demi-point qui change une vie (deux courbes composées) ──────

DATA_3 = '''def load_paths() -> tuple[list[int], list[float], list[float]]:
    """Deux trajectoires de niveau de vie sur 25 ans (base 100), composées à 2,8 %/an
    (âge d'or) et 1,44 %/an (ralentissement).
    Two 25-year living-standard paths (base 100), compounded at 2.8%/yr and 1.44%/yr."""
    years = list(range(26))
    golden = [100 * 1.028 ** t for t in years]
    slow = [100 * 1.0144 ** t for t in years]
    return years, golden, slow

years, golden, slow = load_paths()'''

FIG_3 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Pourquoi un demi-point change une vie",
        sub="Deux économies sur une génération (25 ans)",
        ylab="niveau de vie (départ = 100)",
        xlab="années",
        legend_golden="2,8 %/an (âge d'or)",
        legend_slow="1,44 %/an (ralentissement)",
        mult_golden="× 1,99",
        mult_slow="× 1,43",
        gap="+ 39 %\\nde revenu",
        note="Un écart de 1,4 point de croissance annuelle — le prix du ralentissement — laisse une génération\\n"
             "39 % plus pauvre. C'est pourquoi la productivité est « presque tout » (Krugman)."),
    "en": dict(
        title="Why half a point changes a life",
        sub="Two economies over one generation (25 years)",
        ylab="living standard (start = 100)",
        xlab="years",
        legend_golden="2.8%/yr (golden age)",
        legend_slow="1.44%/yr (slowdown)",
        mult_golden="× 1.99",
        mult_slow="× 1.43",
        gap="+ 39%\\nin income",
        note="A gap of 1.4 points of annual growth — the price of the slowdown — leaves a generation\\n"
             "39% poorer. That is why productivity is « almost everything » (Krugman)."),
}

def build_figure(years: list[int], golden: list[float], slow: list[float], lang: str) -> Figure:
    """Deux courbes composées sur 25 ans, l'aire entre elles et l'écart final de 39 %."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, bottom=0.20)
    ax.fill_between(years, golden, slow, color=nm.COLORS["edge"], alpha=0.55, zorder=1)
    ax.plot(years, golden, color=nm.COLORS["amber"], linewidth=3.6, label=text["legend_golden"], zorder=3)
    ax.plot(years, slow, color=nm.COLORS["blue"], linewidth=3.6, label=text["legend_slow"], zorder=3)
    ax.scatter([25], [golden[-1]], s=150, color=nm.COLORS["amber"], zorder=5)
    ax.scatter([25], [slow[-1]], s=150, color=nm.COLORS["blue"], zorder=5)
    ax.set_xlim(0, 27.5)
    ax.set_xticks(range(0, 26, 5))
    ax.set_ylim(98, 205)
    ax.set_yticks(range(100, 201, 20))
    ax.set_ylabel(text["ylab"])
    ax.set_xlabel(text["xlab"])
    ax.annotate(text["mult_golden"], xy=(25, golden[-1]), xytext=(12, 0),
                textcoords="offset points", ha="left", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["amber"])
    ax.annotate(text["mult_slow"], xy=(25, slow[-1]), xytext=(12, 0),
                textcoords="offset points", ha="left", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["blue"])
    ax.annotate("", xy=(25, golden[-1]), xytext=(25, slow[-1]),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["text"], lw=1.8))
    ax.text(21.3, (golden[-1] + slow[-1]) / 2, text["gap"], ha="center", va="center",
            fontsize=24, fontweight="bold", color=nm.COLORS["text"], linespacing=1.5)
    ax.legend(loc="upper left", frameon=False, fontsize=22, labelcolor=nm.COLORS["text"],
              handlelength=1.6, borderaxespad=1.0)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(years, golden, slow, LANG)'''


# ── Figure 04 — la leçon de la dynamo (deux barres, embarqué) ─────────────────

DATA_4 = '''def load_electrification() -> list[float]:
    """Part de la force motrice des usines américaines électrifiée : < 5 % en 1899,
    ~53 % dans les années 1920 (Paul David, 1990).
    Share of U.S. factory mechanical drive electrified: <5% in 1899, ~53% by the 1920s."""
    return [4.0, 53.0]

electrification = load_electrification()'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La leçon de la dynamo",
        sub="Il a fallu quarante ans pour que l'électricité paie",
        ylab="part de la force motrice des usines électrifiée, %",
        cats=["1899", "années 1920"],
        value_labels=["< 5 %", "53 %"],
        span="≈ 40 ans",
        note="La première centrale d'Edison ouvre en 1882 ; il faut attendre les années 1920 pour que la moitié des usines\\n"
             "soit électrifiée — et que la productivité décolle. Toute technologie générale met une génération. Source : Paul David (1990)."),
    "en": dict(
        title="The lesson of the dynamo",
        sub="It took forty years for electricity to pay off",
        ylab="share of factory mechanical drive electrified, %",
        cats=["1899", "1920s"],
        value_labels=["< 5%", "53%"],
        span="≈ 40 years",
        note="Edison's first power station opens in 1882; it takes until the 1920s for half of factories to be\\n"
             "electrified — and for productivity to take off. Every general technology takes a generation. Source: Paul David (1990)."),
}

def build_figure(values: list[float], lang: str) -> Figure:
    """Deux barres : électrification des usines en 1899 (gris) puis dans les années 1920 (bleu)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig, bottom=0.14)
    ax.grid(axis="x", visible=False)
    positions = range(len(values))
    ax.bar(positions, values, width=0.5, color=["#c9d4e7", nm.COLORS["blue"]], zorder=3)
    ax.set_ylim(0, 70)
    ax.set_yticks(range(0, 71, 10))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=25, color=nm.COLORS["muted"])
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, values, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 14), textcoords="offset points",
                    ha="center", va="bottom", fontsize=32, fontweight="bold", color=nm.COLORS["text"])
    ax.annotate("", xy=(1, 60), xytext=(0, 60),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["amber"], lw=3.0))
    ax.text(0.5, 62.5, text["span"], ha="center", va="bottom", fontsize=30,
            fontweight="bold", color=nm.COLORS["amber"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(electrification, LANG)'''


# ── Figure 05 — les idées plus dures à trouver (deux barres, embarqué) ────────

DATA_5 = '''def load_research_effort() -> list[float]:
    """Chercheurs nécessaires pour tenir la loi de Moore, base 1970 = 1 : × 18 aujourd'hui
    (Bloom, Jones, Van Reenen & Webb, 2020).
    Researchers needed to sustain Moore's Law, base 1970 = 1: ×18 today."""
    return [1.0, 18.0]

research_effort = load_research_effort()'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Les idées deviennent plus dures à trouver",
        sub="Le nombre de chercheurs pour tenir le doublement des puces",
        ylab="chercheurs nécessaires pour maintenir\\nla loi de Moore (base 1970 = 1)",
        cats=["début\\ndes années 1970", "aujourd'hui"],
        value_labels=["× 1", "× 18"],
        note="Pour maintenir la loi de Moore, il faut dix-huit fois plus de chercheurs qu'au début des années 1970. À l'échelle\\n"
             "de l'économie, la productivité de la recherche baisse de 5,3 %/an. Source : Bloom, Jones, Van Reenen & Webb (2020)."),
    "en": dict(
        title="Ideas are getting harder to find",
        sub="The number of researchers needed to sustain the doubling of chips",
        ylab="researchers needed to sustain\\nMoore's Law (base 1970 = 1)",
        cats=["early\\n1970s", "today"],
        value_labels=["× 1", "× 18"],
        note="To sustain Moore's Law, it takes eighteen times more researchers than in the early 1970s. Across the\\n"
             "economy, research productivity falls by 5.3%/yr. Source: Bloom, Jones, Van Reenen & Webb (2020)."),
}

def build_figure(values: list[float], lang: str) -> Figure:
    """Deux barres : effort de recherche au début des années 1970 (×1) puis aujourd'hui (×18)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig, left=0.11, bottom=0.21)
    ax.grid(axis="x", visible=False)
    positions = range(len(values))
    ax.bar(positions, values, width=0.5, color=["#c9d4e7", nm.COLORS["rose"]], zorder=3)
    ax.set_ylim(0, 20)
    ax.set_yticks([i * 2.5 for i in range(9)])
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=25, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, values, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 14), textcoords="offset points",
                    ha="center", va="bottom", fontsize=34, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(research_effort, LANG)'''


# ── Figure 06 — qui récolte les gains (barre horizontale, embarqué) ───────────

DATA_6 = '''def load_split() -> tuple[float, float]:
    """Répartition de la valeur sociale d'une innovation : ~2,2 % à l'innovateur,
    97,8 % aux consommateurs (Nordhaus, 2004).
    Split of an innovation's social value: ~2.2% to the innovator, 97.8% to consumers."""
    innovator = 2.2
    return innovator, 100 - innovator

innovator, consumers = load_split()'''

FIG_6 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Qui récolte les gains de l'innovation",
        sub="Sur 100 de valeur créée, la part que l'inventeur capte",
        xlab="répartition de la valeur sociale créée par une innovation, %",
        keeps="l'innovateur ne garde\\nque 2,2 %",
        innovator_label="2,2 %",
        consumers_label="97,8 % → les consommateurs",
        note="L'innovateur ne capte qu'environ 2,2 % de la valeur qu'il crée ; le reste va aux consommateurs, en prix plus\\n"
             "bas et produits meilleurs. Le progrès se dilue dans le niveau de vie. Source : Nordhaus (2004)."),
    "en": dict(
        title="Who reaps the gains of innovation",
        sub="Out of 100 of value created, the share the inventor captures",
        xlab="split of the social value created by an innovation, %",
        keeps="the innovator keeps\\nonly 2.2%",
        innovator_label="2.2%",
        consumers_label="97.8% → the consumers",
        note="The innovator captures only about 2.2% of the value it creates; the rest goes to consumers, in lower\\n"
             "prices and better products. Progress dilutes into the standard of living. Source: Nordhaus (2004)."),
}

def build_figure(innovator: float, consumers: float, lang: str) -> Figure:
    """Barre horizontale : la part captée par l'innovateur (orange) face aux consommateurs (bleu)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=988)
    ax = nm.axes(fig, bottom=0.20)
    ax.grid(axis="y", visible=False)
    ax.barh([0], [innovator], height=0.5, color=nm.COLORS["amber"], zorder=3)
    ax.barh([0], [consumers], left=innovator, height=0.5, color=nm.COLORS["blue"], zorder=3)
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 20))
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_xlabel(text["xlab"])
    ax.text(innovator + 1.6, 0, text["innovator_label"], ha="left", va="center",
            fontsize=26, fontweight="bold", color=nm.COLORS["bg"])
    ax.text(innovator + consumers / 2, 0, text["consumers_label"], ha="center", va="center",
            fontsize=30, fontweight="bold", color=nm.COLORS["bg"])
    ax.annotate(text["keeps"], xy=(innovator, 0.26), xytext=(11, 0.72),
                ha="center", va="center", fontsize=24, fontweight="bold",
                color=nm.COLORS["amber"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["amber"], lw=1.8))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(innovator, consumers, LANG)'''


# ── Assemblage ───────────────────────────────────────────────────────────────

FIGURES = [
    dict(name="fig01-niveau-productivite", fig_fr="Le grand enrichissement, heure par heure",
         fig_en="The great enrichment, hour by hour", live=True, data=DATA_1, fig=FIG_1),
    dict(name="fig02-vagues-productivite", fig_fr="Les vagues de la productivité",
         fig_en="The waves of productivity", live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-demi-point-generation", fig_fr="Pourquoi un demi-point change une vie",
         fig_en="Why half a point changes a life", live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-dynamo", fig_fr="La leçon de la dynamo",
         fig_en="The lesson of the dynamo", live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-idees-dures", fig_fr="Les idées deviennent plus dures à trouver",
         fig_en="Ideas are getting harder to find", live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-qui-recolte", fig_fr="Qui récolte les gains de l'innovation",
         fig_en="Who reaps the gains of innovation", live=False, data=DATA_6, fig=FIG_6),
]

if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "/home/claudeagent/cms-workspace/nmlab-figures-tools/out12")
    nb_kit.build_all(META, DIR, FIGURES)
