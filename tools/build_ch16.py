#!/usr/bin/env python3
"""Génère les notebooks Colab du chapitre 16 — Épargne et investissement.

Importe nb_kit, définit META + FIGURES (une cellule code par figure : load_*/
build_figure typés), rend les PNG (test_all) et écrit les .ipynb (build_all).
Blocs DATA_*/FIG_* dans le style « strict » des chapitres 18/19/20.
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="16",
    title_fr="Épargne et investissement : les deux moteurs du financement de l'économie",
    title_en="Saving and Investment: The Two Engines Financing the Economy",
    slug_fr="epargne-et-investissement",
    slug_en="saving-and-investment",
)
DIR = "macro/16-epargne-investissement"


# ── Figure 01 — taux d'épargne des ménages (PSAVERT, FRED en direct) ──────────

DATA_1 = '''from pandas import Series

def load_saving_rate() -> Series:
    """Taux d'épargne des ménages américains (PSAVERT), en direct depuis FRED.
    U.S. personal saving rate, live from FRED."""
    return nm.load_fred("PSAVERT")

saving = load_saving_rate()'''

FIG_1 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="L'épargne des ménages américains, sur soixante ans",
        sub="Part du revenu disponible mise de côté chaque mois",
        ylab="taux d'épargne des ménages, % du revenu",
        mean="moyenne longue : 8,4 %",
        covid="31,8 % — avril 2020",
        today="3,0 %\\naujourd'hui",
        note="À 3 % aujourd'hui, deux fois et demie sous sa moyenne de long terme. Le bond de 2020 : de l'épargne forcée,\\n"
             "vite dépensée. Source : BEA via FRED (PSAVERT)."),
    "en": dict(
        title="American household saving, over sixty years",
        sub="Share of disposable income set aside each month",
        ylab="household saving rate, % of income",
        mean="long-run average: 8.4%",
        covid="31.8% — April 2020",
        today="3.0%\\ntoday",
        note="At 3% today, two and a half times below its long-run average. The 2020 spike was forced saving,\\n"
             "quickly spent. Source: BEA via FRED (PSAVERT)."),
}

def build_figure(saving: Series, lang: str) -> Figure:
    """Taux d'épargne mensuel, sa moyenne longue (8,4 %) et les deux extrêmes (2020, aujourd'hui)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig)
    ax.plot(saving.index, saving, color=nm.COLORS["blue"], linewidth=2.2)
    ax.axhline(8.4, color=nm.COLORS["muted"], linestyle=(0, (7, 5)), linewidth=2.2, alpha=0.9)
    ax.set_ylim(0, 35)
    ax.set_yticks(range(0, 36, 5))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.012)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.text(0.05, 0.265, text["mean"], transform=ax.transAxes, fontsize=21.5,
            fontweight="bold", color=nm.COLORS["muted"], va="center")
    # Pic COVID (avril 2020) / COVID peak
    peak_date = saving.loc["2020"].idxmax()
    peak = saving.loc[peak_date]
    ax.scatter([peak_date], [peak], s=95, color=nm.COLORS["amber"], zorder=5)
    ax.annotate(text["covid"], xy=(peak_date, peak), xytext=(-45, -30),
                textcoords="offset points", ha="right", va="center", fontsize=22,
                fontweight="bold", color=nm.COLORS["amber"],
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["amber"], lw=1.8))
    # Dernier point / latest point
    last_date, last = saving.index[-1], saving.iloc[-1]
    ax.scatter([last_date], [last], s=95, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(text["today"], xy=(last_date, last), xytext=(-62, 52),
                textcoords="offset points", ha="center", va="center", fontsize=22,
                fontweight="bold", color=nm.COLORS["rose"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(saving, LANG)'''


# ── Figure 02 — taux d'épargne par tranche de patrimoine (embarqué) ───────────

DATA_2 = '''def saving_by_bracket() -> list[float]:
    """Taux d'épargne par tranche de patrimoine aux États-Unis (1983-2019), en % du revenu
    disponible — d'après Mian, Straub & Sufi (2025) : top 1 %, 9 % suivants, 51e-90e, moitié du bas.
    U.S. saving rate by wealth bracket (share of disposable income)."""
    return [42, 20, 12, 0.5]

rates = saving_by_bracket()'''

FIG_2 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="L'épargne, c'est les riches",
        sub="Taux d'épargne par tranche de patrimoine, États-Unis, 1983-2019",
        ylab="taux d'épargne, % du revenu disponible",
        cats=["Top 1 %", "Les 9 %\\nsuivants", "51e-90e\\npercentile", "Les 50 %\\ndu bas"],
        value_labels=[">40 %", "20 %", "12 %", "≈ 0 %"],
        note="Le 1 % le plus riche épargne plus de 40 % de son revenu ; la moitié du bas, rien. Ce « glut des riches »,\\n"
             "aussi grand que celui de la Chine, a financé la dette du milieu — pas l'investissement. Source : Mian, Straub & Sufi (2025)."),
    "en": dict(
        title="Saving is a phenomenon of the rich",
        sub="Saving rate by wealth bracket, United States, 1983-2019",
        ylab="saving rate, % of disposable income",
        cats=["Top 1%", "Next 9%", "51st-90th\\npercentile", "Bottom 50%"],
        value_labels=[">40%", "20%", "12%", "≈ 0%"],
        note="The richest 1% save more than 40% of their income; the bottom half, nothing. This « glut of the rich »,\\n"
             "as large as China's, financed the middle's debt — not investment. Source: Mian, Straub & Sufi (2025)."),
}

def build_figure(rates: list[float], lang: str) -> Figure:
    """Quatre barres : le taux d'épargne s'effondre du sommet vers le bas de la distribution."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, bottom=0.24)
    ax.grid(axis="x", visible=False)
    positions = range(len(rates))
    colors = [nm.COLORS["rose"], nm.COLORS["blue"], nm.COLORS["blue"], nm.COLORS["blue"]]
    ax.bar(positions, rates, width=0.62, color=colors, zorder=3)
    ax.set_ylim(0, 46)
    ax.set_yticks(range(0, 41, 10))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 3.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, rate, label in zip(positions, rates, text["value_labels"]):
        ax.annotate(label, (pos, rate), xytext=(0, 14), textcoords="offset points",
                    ha="center", va="bottom", fontsize=30, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(rates, LANG)'''


# ── Figure 03 — la chute du taux neutre (embarqué) ────────────────────────────

DATA_3 = '''def neutral_rate_fall() -> list[float]:
    """Baisse du taux d'intérêt neutre sur une génération, en points de base : taux neutre
    observé vs composante « secteur privé » seule — d'après Rachel & Summers (2019).
    Fall of the neutral rate over a generation, in basis points."""
    return [300, 700]

fall = neutral_rate_fall()'''

FIG_3 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le prix du temps s'est effondré",
        sub="De combien le taux d'intérêt naturel a baissé en une génération",
        ylab="baisse du taux neutre sur une génération, points de base",
        cats=["taux neutre\\n(observé)", "composante privée\\nseule"],
        value_labels=["au moins\\n−300 pb", "jusqu'à\\n−700 pb"],
        note="Le taux neutre observé a baissé d'au moins 300 points de base ; en retirant l'effet des dettes publiques et\\n"
             "des retraites, la composante privée chute jusqu'à 700 points. Source : Rachel & Summers (2019)."),
    "en": dict(
        title="The price of time collapsed",
        sub="How much the natural rate of interest fell in one generation",
        ylab="fall of the neutral rate over a generation, basis points",
        cats=["neutral rate\\n(observed)", "private component\\nalone"],
        value_labels=["at least\\n−300 bp", "up to\\n−700 bp"],
        note="The observed neutral rate fell by at least 300 basis points; stripping out the effect of public debts and\\n"
             "pensions, the private component drops by up to 700 points. Source: Rachel & Summers (2019)."),
}

def build_figure(fall: list[float], lang: str) -> Figure:
    """Deux barres : la chute du taux neutre observé (bleu) vs sa composante privée seule (rose)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.10, bottom=0.24)
    ax.grid(axis="x", visible=False)
    positions = range(len(fall))
    ax.bar(positions, fall, width=0.55, color=[nm.COLORS["blue"], nm.COLORS["rose"]], zorder=3)
    ax.set_ylim(0, 850)
    ax.set_yticks(range(0, 801, 100))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, fall, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 16), textcoords="offset points",
                    ha="center", va="bottom", fontsize=28, fontweight="bold",
                    color=nm.COLORS["text"], linespacing=1.5)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(fall, LANG)'''


# ── Figure 04 — investissement UE vs États-Unis (embarqué, barres groupées) ───

DATA_4 = '''def investment_shares() -> tuple[list[float], list[float]]:
    """Investissement en % du PIB (2025), UE vs États-Unis, sur deux postes : logement et
    immatériel (brevets, logiciels, R&D). Sources : Eurostat, BEA.
    Investment as a share of GDP (2025), EU vs U.S., housing and intangibles."""
    eu = [5.0, 4.4]
    us = [3.9, 6.8]
    return eu, us

eu, us = investment_shares()'''

FIG_4 = '''from matplotlib.figure import Figure
from matplotlib.patches import Patch

LABELS = {
    "fr": dict(
        title="L'Europe investit autant — mais pas la même chose",
        sub="Deux postes où l'UE et les États-Unis divergent, 2025",
        ylab="investissement, % du PIB (2025)",
        cats=["Logement", "Immatériel (brevets,\\nlogiciels, R&D)"],
        eu_labels=["5,0 %", "4,4 %"], us_labels=["3,9 %", "6,8 %"],
        legend_eu="Union européenne — total 21,4 %",
        legend_us="États-Unis — total 21,3 %",
        note="Le taux d'investissement TOTAL est quasi identique (21,4 % vs 21,3 %). L'écart n'est pas un niveau, c'est\\n"
             "une composition : l'Europe met plus dans la pierre, l'Amérique bien plus dans l'immatériel. Sources : Eurostat, BEA."),
    "en": dict(
        title="Europe invests as much — but not in the same thing",
        sub="Two items where the EU and the United States diverge, 2025",
        ylab="investment, % of GDP (2025)",
        cats=["Housing", "Intangibles (patents,\\nsoftware, R&D)"],
        eu_labels=["5.0%", "4.4%"], us_labels=["3.9%", "6.8%"],
        legend_eu="European Union — total 21.4%",
        legend_us="United States — total 21.3%",
        note="The TOTAL investment rate is near identical (21.4% vs 21.3%). The gap is not a level, it is a\\n"
             "composition: Europe puts more into bricks, America far more into intangibles. Sources: Eurostat, BEA."),
}

def build_figure(eu: list[float], us: list[float], lang: str) -> Figure:
    """Barres groupées : deux postes d'investissement (logement, immatériel), UE vs États-Unis."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.axes(fig, bottom=0.20)
    ax.grid(axis="x", visible=False)
    groups = range(len(eu))
    width = 0.4
    eu_pos = [g - width / 2 for g in groups]
    us_pos = [g + width / 2 for g in groups]
    ax.bar(eu_pos, eu, width=width, color=nm.COLORS["amber"], zorder=3)
    ax.bar(us_pos, us, width=width, color=nm.COLORS["blue"], zorder=3)
    ax.set_ylim(0, 8.3)
    ax.set_yticks(range(0, 9))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(groups))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(eu_pos, eu, text["eu_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 12), textcoords="offset points",
                    ha="center", va="bottom", fontsize=25, fontweight="bold", color=nm.COLORS["amber"])
    for pos, value, label in zip(us_pos, us, text["us_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 12), textcoords="offset points",
                    ha="center", va="bottom", fontsize=25, fontweight="bold", color=nm.COLORS["blue"])
    handles = [Patch(facecolor=nm.COLORS["amber"], label=text["legend_eu"]),
               Patch(facecolor=nm.COLORS["blue"], label=text["legend_us"])]
    legend = ax.legend(handles=handles, loc="upper left", fontsize=21, frameon=True,
                       handlelength=1.1, handleheight=1.1, borderpad=0.9, labelspacing=0.6)
    legend.get_frame().set_facecolor(nm.COLORS["card"])
    legend.get_frame().set_edgecolor(nm.COLORS["edge"])
    for txt in legend.get_texts():
        txt.set_color(nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(eu, us, LANG)'''


# ── Figure 05 — le besoin d'investissement de l'Europe (embarqué) ─────────────

DATA_5 = '''def europe_investment_need() -> list[float]:
    """Besoin d'investissement annuel supplémentaire de l'UE, en milliards d'euros : chiffrage
    du rapport Draghi (sept. 2024) puis de la BCE (juillet 2025).
    EU additional annual investment need, in billions of euros."""
    return [775, 1200]

need = europe_investment_need()'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le besoin d'investissement de l'Europe, revu à la hausse",
        sub="L'investissement supplémentaire annuel jugé nécessaire pour l'UE",
        ylab="besoin d'investissement annuel supplémentaire de l'UE, Md€",
        cats=["Draghi\\nsept. 2024", "BCE\\njuillet 2025"],
        value_labels=["750-800 Md€", "~1 200 Md€"],
        note="Du rapport Draghi (sept. 2024) au chiffrage de la BCE (juillet 2025), le besoin passe de 750-800 à près de\\n"
             "1 200 milliards par an. L'épargne européenne existe — c'est sa transformation qui manque. Sources : Draghi, BCE."),
    "en": dict(
        title="Europe's investment need, revised upward",
        sub="The additional annual investment judged necessary for the EU",
        ylab="EU additional annual investment need, €bn",
        cats=["Draghi\\nSep. 2024", "ECB\\nJuly 2025"],
        value_labels=["€750-800bn", "~€1,200bn"],
        note="From the Draghi report (Sep. 2024) to the ECB's estimate (July 2025), the need rises from 750-800 to nearly\\n"
             "1,200 billion a year. European saving exists — what is missing is its transformation. Sources: Draghi, ECB."),
}

def build_figure(need: list[float], lang: str) -> Figure:
    """Deux barres : le besoin d'investissement de l'UE, du rapport Draghi au chiffrage de la BCE."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.11, bottom=0.24)
    ax.grid(axis="x", visible=False)
    positions = range(len(need))
    ax.bar(positions, need, width=0.55, color=["#c9d4e7", nm.COLORS["amber"]], zorder=3)
    ax.set_ylim(0, 1500)
    ax.set_yticks(range(0, 1401, 200))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, need, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 16), textcoords="offset points",
                    ha="center", va="bottom", fontsize=30, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(need, LANG)'''


FIGURES = [
    dict(name="fig01-taux-epargne",
         fig_fr="L'épargne des ménages américains, sur soixante ans",
         fig_en="American household saving, over sixty years",
         live=True, data=DATA_1, fig=FIG_1),
    dict(name="fig02-glut-des-riches",
         fig_fr="L'épargne, c'est les riches",
         fig_en="Saving is a phenomenon of the rich",
         live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-chute-taux-naturel",
         fig_fr="Le prix du temps s'est effondré",
         fig_en="The price of time collapsed",
         live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-investissement-ue-us",
         fig_fr="L'Europe investit autant — mais pas la même chose",
         fig_en="Europe invests as much — but not in the same thing",
         live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-besoin-invest-europe",
         fig_fr="Le besoin d'investissement de l'Europe, revu à la hausse",
         fig_en="Europe's investment need, revised upward",
         live=False, data=DATA_5, fig=FIG_5),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out16")
    nb_kit.build_all(META, DIR, FIGURES)
