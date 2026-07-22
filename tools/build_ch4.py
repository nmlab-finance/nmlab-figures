#!/usr/bin/env python3
"""Génère les notebooks du chapitre 4 — Les grandes variables macro (panorama).

Deux figures de données FRED en direct (fig03 croissance/bénéfices, fig06 fil rouge
inflation/Fed → live=True) ; les neuf autres sont des schémas ou un diagramme
illustratif à valeurs EMBARQUÉES (live=False). Convention « strict » : une seule
cellule code, fonctions typées + docstrings — load_*() puis build_figure(...) -> Figure ;
LABELS={"fr":…,"en":…} ; LANG.
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit


META = dict(
    num="4",
    title_fr="Les grandes variables macro qui font bouger vos placements : un panorama",
    title_en="The Big Macro Variables That Move Your Investments: A Panorama",
    slug_fr="les-grandes-variables-macro-qui-font-bouger-vos-placements",
    slug_en="the-big-macro-variables-that-move-your-investments",
)
DIR = "macro/04-grandes-variables-macro"


# ── Figure 01 — « les bonnes nouvelles sont de mauvaises nouvelles » (schéma) ──

DATA_1 = '''def reasoning_chain(lang: str) -> list[str]:
    """Les six maillons du raisonnement de marché, dans l'ordre, localisés.
    The six links of the market's chain of reasoning, in order, localized."""
    if lang == "fr":
        return ["Rapport sur l'emploi\\nexcellent", "L'économie\\nchauffe",
                "Salaires et prix\\naccélèrent", "La banque centrale\\ndevra durcir",
                "Les taux\\nmontent", "Les prix d'actifs\\nbaissent"]
    return ["Excellent\\njobs report", "The economy\\nruns hot",
            "Wages and prices\\naccelerate", "The central bank\\nwill tighten",
            "Rates\\nrise", "Asset prices\\nfall"]'''

FIG_1 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="« Les bonnes nouvelles sont de mauvaises nouvelles »",
        sub="Le raisonnement que le marché déroule en quelques secondes",
        note="La vigueur de l'économie réelle compte moins que ce qu'elle implique pour le loyer de l'argent :\\n"
             "scène rejouée presque chaque mois en 2022-2023."),
    "en": dict(
        title="« Good news is bad news »",
        sub="The chain of reasoning the market unspools in seconds",
        note="The vigor of the real economy counts less than what it implies for the rent of money:\\n"
             "a scene replayed almost every month in 2022-2023."),
}

def build_figure(steps: list[str], lang: str) -> Figure:
    """Schéma en chaîne : six encadrés reliés par des flèches, en zigzag sur deux rangées."""
    text = LABELS[lang]
    fig = nm.figure(height_px=988)
    ax = nm.blank_axes(fig)
    card_w, card_h = 470, 132
    xs = [105, 680, 1255]
    top_y, bot_y = 720, 430                 # ordonnée du HAUT de chaque encadré (px)
    layout = [(xs[0], top_y), (xs[1], top_y), (xs[2], top_y),
              (xs[2], bot_y), (xs[1], bot_y), (xs[0], bot_y)]
    borders = [nm.COLORS["blue"], nm.COLORS["edge"], nm.COLORS["edge"],
               nm.COLORS["edge"], nm.COLORS["edge"], nm.COLORS["rose"]]
    for label, (x, ytop), border in zip(steps, layout, borders):
        nm.card(ax, x, ytop - card_h, card_w, card_h, edge=border, lw=2.6, radius=20)
        ax.text(x + card_w / 2, ytop - card_h / 2, label, ha="center", va="center",
                fontsize=26, fontweight="bold", color=nm.COLORS["text"], linespacing=1.25)

    def arrow(p, q):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(
            arrowstyle="-|>", color=nm.COLORS["muted"], lw=2.6, shrinkA=4, shrinkB=4))

    arrow((xs[0] + card_w, top_y - card_h / 2), (xs[1], top_y - card_h / 2))
    arrow((xs[1] + card_w, top_y - card_h / 2), (xs[2], top_y - card_h / 2))
    arrow((xs[2] + card_w / 2, top_y - card_h), (xs[2] + card_w / 2, bot_y))
    arrow((xs[2], bot_y - card_h / 2), (xs[1] + card_w, bot_y - card_h / 2))
    arrow((xs[1], bot_y - card_h / 2), (xs[0] + card_w, bot_y - card_h / 2))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(reasoning_chain(LANG), LANG)'''


# ── Figure 02 — le tableau de bord : la fraction + six cadrans (schéma) ────────

DATA_2 = '''def dashboard_cards(lang: str) -> list[tuple[str, str]]:
    """Les six cadrans (titre, description) dans l'ordre de lecture, localisés.
    The six dials (title, description) in reading order, localized."""
    if lang == "fr":
        return [
            ("Croissance (PIB)", "plus d'activité \\u2192 plus de ventes et de bénéfices"),
            ("Emploi & salaires", "revenus et consommation\\u2026 mais aussi salaires"),
            ("Inflation", "érode les revenus fixes et réveille les taux"),
            ("Banque centrale", "fixe le loyer de l'argent à court terme"),
            ("Taux d'intérêt", "le taux d'actualisation de toutes les promesses"),
            ("Change & pétrole", "inflation importée, coûts, bénéfices étrangers"),
        ]
    return [
        ("Growth (GDP)", "more activity \\u2192 more sales and profits"),
        ("Employment & wages", "income and consumption\\u2026 but also wages"),
        ("Inflation", "erodes fixed incomes and wakes the rates"),
        ("Central bank", "sets the short-term rent of money"),
        ("Interest rates", "the discount rate of every promise"),
        ("Exchange rate & oil", "imported inflation, costs, foreign profits"),
    ]'''

FIG_2 = '''from matplotlib.figure import Figure

# Structure identique fr/en : (bordure, étage touché) pour chaque cadran.
STRUCT = [("blue", "haut"), ("blue", "both"), ("rose", "both"),
          ("rose", "bas"), ("rose", "bas"), ("blue", "both")]

LABELS = {
    "fr": dict(
        title="Six cadrans qui commandent le prix de vos actifs",
        sub="Chaque variable agit sur l'un des deux étages de la fraction \\u2014 ou sur les deux",
        price="Prix d'un actif  =", num="Revenus futurs attendus", den="Taux d'actualisation",
        top="\\u2190 l'étage du haut", bottom="\\u2190 l'étage du bas",
        haut_full="\\u2192 l'étage du haut", bas_full="\\u2192 l'étage du bas",
        haut_short="\\u2192 le haut", bas_short="\\u2026et le bas"),
    "en": dict(
        title="Six dials that command the price of your assets",
        sub="Each variable acts on one of the two floors of the fraction \\u2014 or on both",
        price="Price of an asset  =", num="Expected future income", den="Discount rate",
        top="\\u2190 the top floor", bottom="\\u2190 the bottom floor",
        haut_full="\\u2192 the top floor", bas_full="\\u2192 the bottom floor",
        haut_short="\\u2192 the top", bas_short="\\u2026and the bottom"),
}

def build_figure(cards: list[tuple[str, str]], lang: str) -> Figure:
    """Schéma : la fraction du prix en tête, puis six cadrans (2 colonnes × 3 rangées)."""
    text = LABELS[lang]
    palette = {"blue": nm.COLORS["blue"], "rose": nm.COLORS["rose"]}
    fig = nm.figure(height_px=1182)
    ax = nm.blank_axes(fig)

    # La fraction, en tête.
    ax.text(560, 985, text["price"], ha="right", va="center", fontsize=30, color=nm.COLORS["text"])
    ax.text(800, 1023, text["num"], ha="center", va="center", fontsize=27,
            fontweight="bold", color=nm.COLORS["blue2"])
    ax.plot([592, 1008], [988, 988], color=nm.COLORS["text"], lw=2.4)
    ax.text(800, 951, text["den"], ha="center", va="center", fontsize=27,
            fontweight="bold", color=nm.COLORS["rose"])
    ax.text(1085, 1023, text["top"], ha="left", va="center", fontsize=22, color=nm.COLORS["muted"])
    ax.text(1085, 951, text["bottom"], ha="left", va="center", fontsize=22, color=nm.COLORS["muted"])

    col_x = [90, 865]
    card_w, card_h = 720, 185
    row_top = [830, 617, 404]
    for i, ((title, desc), (border, floor)) in enumerate(zip(cards, STRUCT)):
        col, row = i % 2, i // 2
        x, top = col_x[col], row_top[row]
        color = palette[border]
        nm.card(ax, x, top - card_h, card_w, card_h, edge=color, lw=2.6, radius=22)
        ax.text(x + 42, top - 48, title, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        ax.text(x + 42, top - 108, desc, ha="left", va="center",
                fontsize=21.5, color=nm.COLORS["muted"])
        if floor == "haut":
            ax.text(x + 42, top - 158, text["haut_full"], ha="left", va="center",
                    fontsize=22, fontweight="bold", color=nm.COLORS["blue2"])
        elif floor == "bas":
            ax.text(x + 42, top - 158, text["bas_full"], ha="left", va="center",
                    fontsize=22, fontweight="bold", color=nm.COLORS["rose"])
        else:
            ax.text(x + 42, top - 158, text["haut_short"], ha="left", va="center",
                    fontsize=22, fontweight="bold", color=nm.COLORS["blue2"])
            ax.text(x + 300, top - 158, text["bas_short"], ha="left", va="center",
                    fontsize=22, fontweight="bold", color=nm.COLORS["rose"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig)
    return fig

build_figure(dashboard_cards(LANG), LANG)'''


# ── Figure 03 — la croissance nourrit les bénéfices (FRED en direct) ──────────

DATA_3 = '''from pandas import Series

def load_data() -> tuple[Series, Series, Series]:
    """PIB nominal (GDP) et bénéfices des entreprises après impôts (CP), trimestriels,
    plus l'indicateur de récession NBER (USREC) — en direct de FRED, depuis 1990.
    Nominal GDP, after-tax corporate profits and the NBER recession flag, live from FRED."""
    gdp = nm.load_fred("GDP", start="1990")
    profits = nm.load_fred("CP", start="1990")
    recessions = nm.load_fred("USREC", start="1990")
    return gdp, profits, recessions

gdp, profits, recessions = load_data()'''

FIG_3 = '''import matplotlib.dates as mdates
from pandas import Series
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La croissance nourrit les bénéfices",
        sub="États-Unis, 1990-2025 : PIB et bénéfices des entreprises, base 100 en 1990",
        ylab="indice, base 100 en 1990",
        legend=["PIB (nominal)", "bénéfices des entreprises"],
        note="Les bénéfices amplifient les cycles de l'activité, mais en épousent la pente. Bandes : récessions\\n"
             "NBER. Source : BEA et NBER via FRED (GDP, CP, USREC)."),
    "en": dict(
        title="Growth feeds profits",
        sub="United States, 1990-2025: GDP and corporate profits, indexed to 100 in 1990",
        ylab="index, 100 = 1990",
        legend=["GDP (nominal)", "corporate profits"],
        note="Profits amplify the cycles of activity but follow its slope. Bands: NBER recessions.\\n"
             "Source: BEA and NBER via FRED (GDP, CP, USREC)."),
}

def build_figure(gdp: Series, profits: Series, recessions: Series, lang: str) -> Figure:
    """Deux séries en base 100 (PIB nominal et bénéfices), ombrées des récessions du NBER."""
    text = LABELS[lang]
    g = gdp / gdp.iloc[0] * 100
    p = profits / profits.iloc[0] * 100
    fig = nm.figure(height_px=1102)
    ax = nm.axes(fig, left=0.088, right=0.9)

    runs = recessions.ne(recessions.shift()).cumsum()
    for _, run in recessions.groupby(runs):
        if run.iloc[0] == 1:
            ax.axvspan(run.index[0], run.index[-1], color=nm.COLORS["edge"], alpha=0.75, linewidth=0)

    ax.plot(g.index, g, color=nm.COLORS["blue"], linewidth=2.9, label=text["legend"][0])
    ax.plot(p.index, p, color=nm.COLORS["rose"], linewidth=2.9, label=text["legend"][1])
    ax.set_ylim(60, 1520)
    ax.set_yticks(range(200, 1401, 200))
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    for series, color in ((p, nm.COLORS["rose"]), (g, nm.COLORS["blue"])):
        mult = series.iloc[-1] / 100
        label = (f"× {mult:.1f}".replace(".", ",") if lang == "fr" else f"× {mult:.1f}")
        ax.annotate(label, xy=(series.index[-1], series.iloc[-1]), xytext=(14, 0),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=28, fontweight="bold", color=color)

    leg = ax.legend(loc="upper left", frameon=True, fontsize=22, labelcolor=nm.COLORS["text"],
                    handlelength=1.6, borderpad=0.9)
    leg.get_frame().set_facecolor(nm.COLORS["card"])
    leg.get_frame().set_edgecolor(nm.COLORS["edge"])
    leg.get_frame().set_linewidth(1.4)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(gdp, profits, recessions, LANG)'''


# ── Figure 04 — l'inflation à double visage (schéma à deux cartes + bandeau) ───

DATA_4 = '''def inflation_cards(lang: str) -> list[tuple[str, str, list[list[str]]]]:
    """Les deux visages de l'inflation : (titre, couleur, puces), localisés ; chaque puce
    est une liste de lignes. The two faces of inflation: (title, color, bullets), localized."""
    if lang == "fr":
        return [
            ("Le voleur silencieux", "blue",
             [["\\u00b7 érode tout revenu fixé à l'avance :", "coupons, loyers, livrets, rentes"],
              ["\\u00b7 à 5 % d'inflation, un placement à 3 %", "appauvrit : rendement réel \\u22122 %"]]),
            ("Le déclencheur de la riposte", "rose",
             [["\\u00b7 la variable que la banque centrale", "s'est juré de dompter (cible ~2 %)"],
              ["\\u00b7 au-delà : riposte des taux \\u2014 tout le", "bas de la fraction tremble"]]),
        ]
    return [
        ("The silent thief", "blue",
         [["\\u00b7 erodes any income fixed in advance:", "coupons, rents, savings, annuities"],
          ["\\u00b7 at 5% inflation, a 3% investment", "impoverishes: real return \\u22122%"]]),
        ("The trigger of the response", "rose",
         [["\\u00b7 the variable the central bank", "has sworn to tame (target ~2%)"],
          ["\\u00b7 beyond it: the rate response \\u2014", "the whole bottom of the fraction trembles"]]),
    ]'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="L'inflation, à double visage",
        sub="Deux canaux distincts vers vos placements",
        banner="2022 : près de 9 % aux États-Unis, plus de 10 % en zone euro \\u2014\\nactions et obligations en baisse ensemble",
        note="Modérée et stable, une compagne discrète ; forte et instable, un poison pour presque tout ce que vous\\n"
             "possédez \\u2014 le nominal n'est pas le réel (Fisher)."),
    "en": dict(
        title="Inflation, a double face",
        sub="Two distinct channels to your investments",
        banner="2022: nearly 9% in the U.S., over 10% in the euro area \\u2014\\nstocks and bonds falling together",
        note="Moderate and stable, a discreet companion; high and unstable, a poison for almost everything you own\\n"
             "\\u2014 nominal is not real (Fisher)."),
}

def build_figure(cards: list, lang: str) -> Figure:
    """Schéma : deux cartes (voleur silencieux vs déclencheur) puis un bandeau « 2022 »."""
    text = LABELS[lang]
    palette = {"blue": nm.COLORS["blue"], "rose": nm.COLORS["rose"]}
    fig = nm.figure(height_px=1064)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 760, 90, 105
    top, bottom = 850, 430
    for i, (title, color, bullets) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        nm.card(ax, x, bottom, card_w, top - bottom, edge=palette[color], lw=2.6, radius=24)
        ax.text(x + 55, top - 68, title, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        y = top - 168
        for para in bullets:
            for j, line in enumerate(para):
                ax.text(x + 55, y, line, ha="left", va="center", fontsize=23,
                        color=nm.COLORS["text"] if j == 0 else nm.COLORS["muted"])
                y -= 52
            y -= 34

    nm.card(ax, x0, 268, 2 * card_w + gap, 108, edge=nm.COLORS["edge"], lw=2.2, radius=20)
    ax.text(nm.WIDTH_PX / 2, 322, text["banner"], ha="center", va="center",
            fontsize=25, fontweight="bold", color=nm.COLORS["text"], linespacing=1.4)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(inflation_cards(LANG), LANG)'''


# ── Figure 05 — la gravité des taux (barres illustratives, valeurs embarquées) ─

DATA_5 = '''def rate_impacts() -> list[float]:
    """Impact indicatif (ordre de grandeur) d'une hausse de 1 point de taux sur le prix,
    en %, par échéance : obligation 2 ans, 10 ans, 30 ans, action de croissance.
    Valeurs ILLUSTRATIVES, non des données de marché. Indicative, illustrative values."""
    return [-2.0, -8.0, -25.0, -32.0]

impacts = rate_impacts()'''

FIG_5 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="La gravité des taux",
        sub="Ordre de grandeur : impact d'une hausse de 1 point de taux sur le prix",
        cats=["Obligation\\n2 ans", "Obligation\\n10 ans", "Obligation\\n30 ans", "Action de\\ncroissance"],
        value_labels=["\\u22122 %", "\\u22128 %", "\\u221220 à \\u221230 %"],
        growth="forte, non\\nchiffrable",
        note="Plus les revenus promis sont lointains, plus leur valeur d'aujourd'hui plie sous le taux qui les\\n"
             "actualise : c'est la duration, la « prise au vent » face aux taux. Ordres de grandeur."),
    "en": dict(
        title="The gravity of rates",
        sub="Order of magnitude: impact of a 1-point rate rise on price",
        cats=["2-year\\nbond", "10-year\\nbond", "30-year\\nbond", "Growth\\nstock"],
        value_labels=["\\u22122%", "\\u22128%", "\\u221220 to \\u221230%"],
        growth="large, not\\nquantifiable",
        note="The further off the promised income, the more its present value bends under the discounting rate:\\n"
             "that is duration, the « exposure to the wind » of rates. Orders of magnitude."),
}

def build_figure(impacts: list[float], lang: str) -> Figure:
    """Quatre barres négatives : obligations 2/10/30 ans (pleines) et action de croissance (hachurée)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.10, bottom=0.20)
    ax.grid(axis="x", visible=False)
    positions = range(len(impacts))
    for pos, value in zip(positions, impacts):
        if pos == len(impacts) - 1:                   # action de croissance : hachurée
            ax.bar(pos, value, width=0.6, color=nm.COLORS["bg"], edgecolor=nm.COLORS["rose"],
                   hatch="///", linewidth=2.2, zorder=3)
        else:
            ax.bar(pos, value, width=0.6, color=nm.COLORS["rose"], zorder=3)
    ax.axhline(0, color=nm.COLORS["muted"], linewidth=1.6, alpha=0.9)
    ax.set_ylim(-42, 3)
    ax.set_yticks([0, -10, -20, -30, -40])
    sign = " %" if lang == "fr" else "%"
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}{sign}".replace("-", "\\u2212")))
    ax.set_xlim(-0.6, 3.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=22, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, impacts, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, -14), textcoords="offset points",
                    ha="center", va="top", fontsize=30, fontweight="bold", color=nm.COLORS["text"])
    ax.annotate(text["growth"], (len(impacts) - 1, impacts[-1]), xytext=(0, -14),
                textcoords="offset points", ha="center", va="top",
                fontsize=26, fontweight="bold", color=nm.COLORS["text"], linespacing=1.4)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(impacts, LANG)'''


# ── Figure 06 — le fil rouge 2020-2025 (FRED en direct) ───────────────────────

DATA_6 = '''from pandas import Series

def load_data() -> tuple[Series, Series]:
    """Inflation américaine sur un an (IPC, CPIAUCSL) et borne haute du taux directeur
    de la Fed (DFEDTARU), en direct de FRED, depuis 2019.
    U.S. year-on-year inflation (CPI) and the Fed policy-rate upper bound, live from FRED."""
    cpi = nm.load_fred("CPIAUCSL", start="2018")
    inflation = (cpi.pct_change(12) * 100).loc["2019":]
    fedrate = nm.load_fred("DFEDTARU", start="2019")
    return inflation, fedrate

inflation, fedrate = load_data()'''

FIG_6 = '''import matplotlib.dates as mdates
import pandas as pd
from pandas import Series
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="Le fil rouge 2020-2025 : l'inflation s'envole, la Fed la poursuit",
        sub="États-Unis, 2019-2025 \\u2014 inflation sur un an et borne haute du taux directeur",
        infl="inflation américaine\\n(prix à la consommation,\\nsur un an)",
        fed="taux directeur\\nde la Fed",
        peak="pic : \\u2248 9 %\\njuin 2022", covid="COVID : taux ramenés\\nprès de 0 %",
        hike="premier relèvement\\nmars 2022", plateau="sommet : 5,25-5,50 %\\njuillet 2023",
        cut="première baisse\\nsept. 2024", target="cible d'inflation : 2 %",
        note="Source : Bureau of Labor Statistics et Réserve fédérale, via FRED (séries CPIAUCSL et DFEDTARU)."),
    "en": dict(
        title="The running thread 2020-2025: inflation soars, the Fed gives chase",
        sub="United States, 2019-2025 \\u2014 year-on-year inflation and the policy-rate upper bound",
        infl="U.S. inflation\\n(consumer prices,\\nyear on year)",
        fed="Fed policy\\nrate",
        peak="peak: \\u2248 9%\\nJune 2022", covid="COVID: rates cut\\nto near 0%",
        hike="first hike\\nMarch 2022", plateau="peak: 5.25-5.50%\\nJuly 2023",
        cut="first cut\\nSept. 2024", target="inflation target: 2%",
        note="Source: Bureau of Labor Statistics and Federal Reserve, via FRED (series CPIAUCSL and DFEDTARU)."),
}

def build_figure(inflation: Series, fedrate: Series, lang: str) -> Figure:
    """Inflation (rose) et taux directeur en escalier (bleu), avec les jalons du cycle 2020-2025."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1225)
    ax = nm.axes(fig)
    ax.axhline(2, color=nm.COLORS["amber"], linestyle=(0, (6, 4)), linewidth=2.2)
    ax.plot(fedrate.index, fedrate, color=nm.COLORS["blue"], linewidth=3.0, drawstyle="steps-post")
    ax.plot(inflation.index, inflation, color=nm.COLORS["rose"], linewidth=3.0)
    ax.set_ylim(-0.4, 10.8)
    ax.set_yticks(range(0, 11, 2))
    fmt = " %" if lang == "fr" else "%"
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}{fmt}"))
    ax.set_xlim(pd.Timestamp("2019-01-01"), pd.Timestamp("2026-06-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.text(pd.Timestamp("2021-01-15"), 8.1, text["infl"], fontsize=21.5, fontweight="bold",
            color=nm.COLORS["rose"], va="center", linespacing=1.4)
    ax.text(pd.Timestamp("2019-02-01"), 3.15, text["fed"], fontsize=21.5, fontweight="bold",
            color=nm.COLORS["blue"], va="center", linespacing=1.4)
    ax.text(ax.get_xlim()[1], 2.35, text["target"], fontsize=20, color=nm.COLORS["muted"],
            ha="right", va="bottom")

    peak_date = inflation.loc["2022"].idxmax()
    peak_val = float(inflation.loc[peak_date])
    ax.scatter([peak_date], [peak_val], s=95, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(text["peak"], xy=(peak_date, peak_val), xytext=(peak_date, 10.4),
                ha="center", va="top", fontsize=20, color=nm.COLORS["text"], linespacing=1.4)

    covid_date = fedrate.loc["2020"].idxmin()
    ax.scatter([covid_date], [float(fedrate.loc[covid_date])], s=85, color=nm.COLORS["blue"], zorder=5)
    ax.annotate(text["covid"], xy=(covid_date, float(fedrate.loc[covid_date])),
                xytext=(covid_date, -0.15), ha="center", va="top",
                fontsize=20, color=nm.COLORS["text"], linespacing=1.4)

    hike_date = pd.Timestamp("2022-03-17")
    ax.scatter([hike_date], [float(fedrate.asof(hike_date))], s=85, color=nm.COLORS["blue"], zorder=5)
    ax.annotate(text["hike"], xy=(hike_date, float(fedrate.asof(hike_date))),
                xytext=(pd.Timestamp("2021-10-01"), 1.35), ha="center", va="center",
                fontsize=20, color=nm.COLORS["text"], linespacing=1.4)

    ax.text(pd.Timestamp("2023-08-01"), 6.15, text["plateau"], fontsize=20,
            color=nm.COLORS["text"], ha="center", va="center", linespacing=1.4)

    cut_date = pd.Timestamp("2024-09-18")
    ax.scatter([cut_date], [float(fedrate.asof(cut_date))], s=85, color=nm.COLORS["blue"], zorder=5)
    ax.annotate(text["cut"], xy=(cut_date, float(fedrate.asof(cut_date))),
                xytext=(pd.Timestamp("2025-02-01"), 6.4), ha="center", va="center",
                fontsize=20, color=nm.COLORS["text"], linespacing=1.4)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(inflation, fedrate, LANG)'''


# ── Figure 07 — une même nouvelle, deux canaux opposés (schéma) ───────────────

DATA_7 = '''def two_channels(lang: str) -> tuple[str, str, list, list]:
    """Le rapport (titre, sous-titre) et les deux canaux (titre, couleur, lignes), localisés.
    The report (title, subtitle) and the two channels (title, color, lines), localized."""
    if lang == "fr":
        head = ("Rapport sur l'emploi bien plus fort que prévu", "beaucoup d'embauches, chômage en baisse")
        left = ("Canal des bénéfices \\u2014 l'étage du haut", "blue",
                ["plus d'emplois \\u2192 plus de revenus", "plus de revenus \\u2192 plus de consommation",
                 "plus de ventes \\u2192 bénéfices en hausse", "le haut de la fraction monte",
                 "\\u2192 pousse les actions à la HAUSSE"])
        right = ("Canal des taux \\u2014 l'étage du bas", "rose",
                 ["marché du travail tendu \\u2192 salaires en hausse", "salaires \\u2192 pressions sur l'inflation",
                  "la banque centrale durcit (ou baisse plus tard)", "le bas de la fraction monte",
                  "\\u2192 pousse les actions à la BAISSE"])
        return head, left, right, ["fr"]
    head = ("Jobs report far stronger than expected", "lots of hiring, unemployment falling")
    left = ("Profit channel \\u2014 the top floor", "blue",
            ["more jobs \\u2192 more income", "more income \\u2192 more consumption",
             "more sales \\u2192 profits rise", "the top of the fraction rises",
             "\\u2192 pushes stocks UP"])
    right = ("Rate channel \\u2014 the bottom floor", "rose",
             ["tight labor market \\u2192 wages rise", "wages \\u2192 pressure on inflation",
              "the central bank tightens (or cuts later)", "the bottom of the fraction rises",
              "\\u2192 pushes stocks DOWN"])
    return head, left, right, ["en"]'''

FIG_7 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Une même nouvelle, deux canaux opposés",
               sub="Pourquoi une bonne nouvelle économique peut faire baisser la Bourse",
               note="Le verdict dépend du régime : quand la peur dominante est l'inflation (2022), le canal des taux\\n"
                    "l'emporte \\u2014 la bonne nouvelle devient mauvaise. Quand la peur dominante est la récession,\\n"
                    "le canal des bénéfices reprend le dessus."),
    "en": dict(title="One news, two opposite channels",
               sub="Why good economic news can send the stock market down",
               note="The verdict depends on the regime: when the dominant fear is inflation (2022), the rate channel\\n"
                    "wins \\u2014 the good news becomes bad. When the dominant fear is recession, the profit channel\\n"
                    "takes over again."),
}

def draw_channel(ax, x, w, top, bottom, title, color, lines):
    """Une carte-canal : titre coloré, quatre lignes de mécanisme, puis la conclusion colorée."""
    nm.card(ax, x, bottom, w, top - bottom, edge=color, lw=2.6, radius=24)
    ax.text(x + 55, top - 62, title, ha="left", va="center", fontsize=27, fontweight="bold", color=color)
    y = top - 150
    for line in lines[:-1]:
        ax.text(x + 55, y, line, ha="left", va="center", fontsize=22.5, color=nm.COLORS["text"])
        y -= 62
    ax.text(x + 55, y - 20, lines[-1], ha="left", va="center", fontsize=25, fontweight="bold", color=color)

def build_figure(payload: tuple, lang: str) -> Figure:
    """Schéma : un rapport en tête, deux flèches, puis les canaux bénéfices (haut) et taux (bas)."""
    text = LABELS[lang]
    head, left, right, _ = payload
    palette = {"blue": nm.COLORS["blue"], "rose": nm.COLORS["rose"]}
    fig = nm.figure(height_px=1182)
    ax = nm.blank_axes(fig)

    hx, hw, htop, hbot = 460, 830, 1000, 878
    nm.card(ax, hx, hbot, hw, htop - hbot, edge=nm.COLORS["edge"], lw=2.4, radius=20)
    ax.text(hx + hw / 2, htop - 44, head[0], ha="center", va="center",
            fontsize=27, fontweight="bold", color=nm.COLORS["text"])
    ax.text(hx + hw / 2, htop - 92, head[1], ha="center", va="center",
            fontsize=21, color=nm.COLORS["muted"])

    card_w, top, bottom = 780, 812, 250
    lx, rx = 90, 880
    ax.annotate("", xy=(lx + card_w / 2 + 40, top + 6), xytext=(hx + hw / 2 - 70, hbot - 4),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["muted"], lw=2.6))
    ax.annotate("", xy=(rx + card_w / 2 - 40, top + 6), xytext=(hx + hw / 2 + 70, hbot - 4),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["muted"], lw=2.6))

    draw_channel(ax, lx, card_w, top, bottom, left[0], palette[left[1]], left[2])
    draw_channel(ax, rx, card_w, top, bottom, right[0], palette[right[1]], right[2])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(two_channels(LANG), LANG)'''


# ── Figure 08 — le monde extérieur : change et pétrole (schéma à deux cartes) ──

DATA_8 = '''def outside_cards(lang: str) -> list[tuple[str, str, list[list[str]]]]:
    """Les deux cadrans extérieurs : (titre, couleur, puces), localisés ; chaque puce est
    une liste de lignes. The two outside dials: (title, color, bullets), localized."""
    if lang == "fr":
        return [
            ("Le change", "blue",
             [["\\u00b7 monnaie faible \\u2192 inflation importée"],
              ["\\u00b7 monnaie faible \\u2192 exportateurs dopés"],
              ["\\u00b7 la valeur de vos avoirs à l'étranger :", "Wall Street +10 % et dollar \\u221210 %",
               "= année blanche sans couverture"]]),
            ("Le pétrole", "rose",
             [["\\u00b7 coût de production diffus : transport,", "plastiques, engrais, électricité"],
              ["\\u00b7 et panier direct : pompe, chauffage"],
              ["\\u00b7 choc pétrolier : inflation vers le haut", "ET activité vers le bas"]]),
        ]
    return [
        ("The exchange rate", "blue",
         [["\\u00b7 weak currency \\u2192 imported inflation"],
          ["\\u00b7 weak currency \\u2192 exporters boosted"],
          ["\\u00b7 the value of your foreign holdings:", "Wall Street +10% and dollar \\u221210%",
           "= a wasted year unhedged"]]),
        ("Oil", "rose",
         [["\\u00b7 a diffuse production cost: transport,", "plastics, fertilizer, electricity"],
          ["\\u00b7 and the direct basket: pump, heating"],
          ["\\u00b7 oil shock: inflation up", "AND activity down"]]),
    ]'''

FIG_8 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Le monde extérieur : deux cadrans", sub="Aucune économie n'est une île",
               note="Détenir des actions américaines, c'est empiler deux paris \\u2014 les entreprises et le dollar ;\\n"
                    "et les grands chocs pétroliers cumulent les deux maux, comme en 1973 ou en 2022."),
    "en": dict(title="The outside world: two dials", sub="No economy is an island",
               note="Holding U.S. stocks is stacking two bets \\u2014 the companies and the dollar; and the great oil\\n"
                    "shocks combine both evils, as in 1973 or 2022."),
}

def build_figure(cards: list, lang: str) -> Figure:
    """Schéma : deux cartes à puces (le change, le pétrole)."""
    text = LABELS[lang]
    palette = {"blue": nm.COLORS["blue"], "rose": nm.COLORS["rose"]}
    fig = nm.figure(height_px=1064)
    ax = nm.blank_axes(fig)
    card_w, gap, x0 = 760, 90, 105
    top, bottom = 830, 290
    for i, (title, color, bullets) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        nm.card(ax, x, bottom, card_w, top - bottom, edge=palette[color], lw=2.6, radius=24)
        ax.text(x + 55, top - 68, title, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        y = top - 168
        for para in bullets:
            for j, line in enumerate(para):
                ax.text(x + 55, y, line, ha="left", va="center", fontsize=23,
                        color=nm.COLORS["text"] if j == 0 else nm.COLORS["muted"])
                y -= 50
            y -= 30
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(outside_cards(LANG), LANG)'''


# ── Figure 09 — la boucle des six cadrans (schéma circulaire) ─────────────────

DATA_9 = '''def loop_nodes(lang: str) -> list[tuple[str, str]]:
    """Les six cadrans en boucle, dans le sens horaire depuis le haut : (libellé, couleur).
    The six dials in a clockwise loop from the top: (label, color), localized."""
    if lang == "fr":
        labels = ["Croissance", "Emploi", "Salaires", "Inflation", "Banque\\ncentrale", "Taux"]
    else:
        labels = ["Growth", "Employment", "Wages", "Inflation", "Central\\nbank", "Rates"]
    colors = ["blue", "blue", "blue", "rose", "blue", "blue"]
    return list(zip(labels, colors))'''

FIG_9 = '''import math
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch

LABELS = {
    "fr": dict(title="Aucun cadran ne se lit seul", sub="La boucle qui relie les six variables",
               center="un seul mécanisme,\\nsix angles de vue",
               note="« La croissance accélère » n'est ni bon ni mauvais en soi : tout dépend de l'inflation, donc de la\\n"
                    "banque centrale. Ce sont les combinaisons qui font le climat \\u2014 Goldilocks ou stagflation."),
    "en": dict(title="No dial is read alone", sub="The loop that ties the six variables together",
               center="one mechanism,\\nsix angles of view",
               note="« Growth is accelerating » is neither good nor bad in itself: everything depends on inflation, hence\\n"
                    "on the central bank. It is the combinations that make the climate \\u2014 Goldilocks or stagflation."),
}

def build_figure(nodes: list[tuple[str, str]], lang: str) -> Figure:
    """Schéma : six cadrans disposés en ellipse, reliés par des flèches courbes dans le sens horaire."""
    text = LABELS[lang]
    palette = {"blue": nm.COLORS["blue"], "rose": nm.COLORS["rose"]}
    fig = nm.figure(height_px=1178)
    ax = nm.blank_axes(fig)
    cx, cy, rx, ry = 873, 545, 470, 325
    angles = [90, 30, -30, -90, -150, 150]            # sens horaire depuis le haut
    centers = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in angles]
    cw, ch = 250, 128

    for (label, color), (px, py) in zip(nodes, centers):
        nm.card(ax, px - cw / 2, py - ch / 2, cw, ch, edge=palette[color], lw=2.6, radius=20)
        ax.text(px, py, label, ha="center", va="center", fontsize=25,
                fontweight="bold", color=nm.COLORS["text"], linespacing=1.15)

    for i in range(len(centers)):
        p = centers[i]
        q = centers[(i + 1) % len(centers)]
        ax.add_patch(FancyArrowPatch(p, q, connectionstyle="arc3,rad=-0.22", arrowstyle="-|>",
                                     mutation_scale=24, color=nm.COLORS["muted"], lw=2.4,
                                     shrinkA=95, shrinkB=95))
    ax.text(cx, cy, text["center"], ha="center", va="center", fontsize=23,
            style="italic", color=nm.COLORS["muted"], linespacing=1.4)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(loop_nodes(LANG), LANG)'''


# ── Figure 10 — la surprise, pas le niveau (schéma à deux droites graduées) ────

DATA_10 = '''def surprise_panels(lang: str) -> list[dict]:
    """Deux rapports imaginaires : structure (consensus, publié, couleur, sens) + textes localisés.
    Two imaginary reports: structure (consensus, published, color, direction) + localized text."""
    if lang == "fr":
        panels = [
            dict(title="Rapport A \\u2014 un « bon » chiffre qui déçoit",
                 subtitle="250 000 emplois créés : solide dans l'absolu\\u2026",
                 cons_label="consensus\\n300 k", pub_label="publié\\n250 k",
                 concl="sous les attentes \\u2192 le prix BAISSE"),
            dict(title="Rapport B \\u2014 un chiffre médiocre qui soulage",
                 subtitle="80 000 emplois créés : faible dans l'absolu\\u2026",
                 cons_label="consensus\\n30 k", pub_label="publié\\n80 k",
                 concl="au-dessus des attentes \\u2192 le prix MONTE"),
        ]
    else:
        panels = [
            dict(title="Report A \\u2014 a « good » number that disappoints",
                 subtitle="250,000 jobs created: solid in absolute terms\\u2026",
                 cons_label="consensus\\n300k", pub_label="published\\n250k",
                 concl="below expectations \\u2192 the price FALLS"),
            dict(title="Report B \\u2014 a mediocre number that relieves",
                 subtitle="80,000 jobs created: weak in absolute terms\\u2026",
                 cons_label="consensus\\n30k", pub_label="published\\n80k",
                 concl="above expectations \\u2192 the price RISES"),
        ]
    struct = [dict(consensus=300, published=250, color="rose", direction="down"),
              dict(consensus=30, published=80, color="blue", direction="up")]
    for p, s in zip(panels, struct):
        p.update(s)
    return panels'''

FIG_10 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Ce qui fait bouger les prix : l'écart au consensus, pas le niveau",
               sub="Deux rapports sur l'emploi imaginaires \\u2014 créations d'emplois mensuelles, en milliers",
               note="Le niveau finit par compter \\u2014 il façonne les bénéfices sur la durée ; mais la réaction du jour\\n"
                    "se joue sur la surprise, car ce qui était attendu est déjà dans les prix."),
    "en": dict(title="What moves prices: the gap to consensus, not the level",
               sub="Two imaginary jobs reports \\u2014 monthly job creation, in thousands",
               note="The level ends up mattering \\u2014 it shapes profits over time; but the day's reaction turns on\\n"
                    "the surprise, for what was expected is already in the price."),
}

def build_figure(panels: list[dict], lang: str) -> Figure:
    """Schéma : deux droites graduées où le prix réagit à l'écart publié-consensus, pas au niveau."""
    text = LABELS[lang]
    palette = {"blue": nm.COLORS["blue"], "rose": nm.COLORS["rose"]}
    fig = nm.figure(height_px=880)
    ax = nm.blank_axes(fig)
    regions = [(160, 820), (940, 1600)]
    vmax, line_y = 380.0, 405
    for (x0, x1), p in zip(regions, panels):
        cx = (x0 + x1) / 2
        color = palette[p["color"]]

        def X(v, x0=x0, x1=x1):
            return x0 + (v / vmax) * (x1 - x0)

        ax.text(cx, 640, p["title"], ha="center", va="center",
                fontsize=24, fontweight="bold", color=nm.COLORS["text"])
        ax.text(cx, 578, p["subtitle"], ha="center", va="center", fontsize=20, color=nm.COLORS["muted"])

        ax.plot([X(0), X(vmax)], [line_y, line_y], color=nm.COLORS["edge"], lw=2.6, solid_capstyle="round")
        for t in (0, 100, 200, 300):
            ax.plot([X(t), X(t)], [line_y - 10, line_y + 10], color=nm.COLORS["edge"], lw=2.0)
            ax.text(X(t), line_y - 40, str(t), ha="center", va="top", fontsize=19, color=nm.COLORS["muted"])

        ax.scatter([X(p["consensus"])], [line_y], s=280, facecolors=nm.COLORS["bg"],
                   edgecolors=nm.COLORS["text"], linewidths=2.6, zorder=4)
        ax.text(X(p["consensus"]), line_y + 66, p["cons_label"], ha="center", va="bottom",
                fontsize=20, color=nm.COLORS["text"], linespacing=1.3)
        ax.scatter([X(p["published"])], [line_y], s=280, color=color, zorder=5)
        ax.annotate("", xy=(X(p["consensus"]), line_y + 34), xytext=(X(p["published"]), line_y + 34),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=2.2))
        ax.text(X(p["published"]), line_y - 70, p["pub_label"], ha="center", va="top",
                fontsize=20, fontweight="bold", color=color, linespacing=1.3)

        marker = "^" if p["direction"] == "up" else "v"
        ax.scatter([x1 - 50], [line_y - 95], s=560, marker=marker, color=color, zorder=5)
        ax.text(cx, 165, p["concl"], ha="center", va="center", fontsize=23, fontweight="bold", color=color)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(surprise_panels(LANG), LANG)'''


# ── Figure 11 — trois réflexes à emporter (schéma à trois cartes numérotées) ──

DATA_11 = '''def reflex_cards(lang: str) -> list[tuple[str, str, str, list[str]]]:
    """Les trois réflexes : (numéro, couleur, titre, lignes de texte), localisés.
    The three reflexes: (number, color, title, text lines), localized."""
    if lang == "fr":
        return [
            ("1", "blue", "La fraction d'abord",
             ["quel étage la nouvelle", "touche-t-elle \\u2014 le haut,", "le bas, les deux ? quel",
              "effet domine aujourd'hui ?"]),
            ("2", "blue", "Surprise \\u2260 niveau",
             ["la surprise fait la séance ;", "le niveau et la durée font", "les rendements des années"]),
            ("3", "rose", "Jamais un cadran seul",
             ["six organes d'un même", "corps \\u2014 au centre, la banque", "centrale, dont la réaction",
              "fait partie du jeu"]),
        ]
    return [
        ("1", "blue", "The fraction first",
         ["which floor does the news", "touch \\u2014 the top, the bottom,", "both? which effect",
          "dominates today?"]),
        ("2", "blue", "Surprise \\u2260 level",
         ["the surprise makes the", "session; the level and its", "duration make the years' returns"]),
        ("3", "rose", "Never one dial alone",
         ["six organs of one body \\u2014", "at the center, the central", "bank, whose reaction is",
          "part of the game"]),
    ]'''

FIG_11 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Trois réflexes à emporter", sub="Ils serviront à chaque chapitre du parcours",
               note="Un chiffre identique peut être bon une année et mauvais la suivante :\\n"
                    "ce n'est pas le chiffre qui a changé, c'est le régime."),
    "en": dict(title="Three reflexes to carry away", sub="They will serve in every chapter of the journey",
               note="An identical number can be good one year and bad the next:\\n"
                    "it is not the number that changed, it is the regime."),
}

def build_figure(cards: list, lang: str) -> Figure:
    """Schéma : trois cartes numérotées (la fraction, surprise vs niveau, jamais un cadran seul)."""
    text = LABELS[lang]
    palette = {"blue": nm.COLORS["blue"], "rose": nm.COLORS["rose"]}
    fig = nm.figure(height_px=966)
    ax = nm.blank_axes(fig)
    card_w, gap, x0 = 505, 56, 92
    top, bottom = 730, 250
    for i, (num, color, title, lines) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        c = palette[color]
        nm.card(ax, x, bottom, card_w, top - bottom, edge=c, lw=2.6, radius=24)
        ax.text(x + 42, top - 70, num, ha="left", va="center", fontsize=31, fontweight="bold", color=c)
        ax.text(x + 90, top - 70, title, ha="left", va="center",
                fontsize=25, fontweight="bold", color=nm.COLORS["text"])
        y = top - 160
        for line in lines:
            ax.text(x + 45, y, line, ha="left", va="center", fontsize=22, color=nm.COLORS["muted"])
            y -= 52
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(reflex_cards(LANG), LANG)'''


# ── Assemblage ───────────────────────────────────────────────────────────────

FIGURES = [
    dict(name="fig01-bonnes-mauvaises-nouvelles",
         fig_fr="« Les bonnes nouvelles sont de mauvaises nouvelles »",
         fig_en="« Good news is bad news »", live=False, data=DATA_1, fig=FIG_1),
    dict(name="fig02-tableau-bord-macro",
         fig_fr="Six cadrans qui commandent le prix de vos actifs",
         fig_en="Six dials that command the price of your assets", live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-croissance-benefices",
         fig_fr="La croissance nourrit les bénéfices",
         fig_en="Growth feeds profits", live=True, data=DATA_3, fig=FIG_3),
    dict(name="fig04-inflation-double-visage",
         fig_fr="L'inflation, à double visage",
         fig_en="Inflation, a double face", live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-gravite-des-taux",
         fig_fr="La gravité des taux",
         fig_en="The gravity of rates", live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-inflation-taux-fed",
         fig_fr="Le fil rouge 2020-2025 : l'inflation s'envole, la Fed la poursuit",
         fig_en="The running thread 2020-2025: inflation soars, the Fed gives chase",
         live=True, data=DATA_6, fig=FIG_6),
    dict(name="fig07-nouvelle-deux-canaux",
         fig_fr="Une même nouvelle, deux canaux opposés",
         fig_en="One news, two opposite channels", live=False, data=DATA_7, fig=FIG_7),
    dict(name="fig08-change-petrole",
         fig_fr="Le monde extérieur : deux cadrans",
         fig_en="The outside world: two dials", live=False, data=DATA_8, fig=FIG_8),
    dict(name="fig09-boucle-cadrans",
         fig_fr="Aucun cadran ne se lit seul",
         fig_en="No dial is read alone", live=False, data=DATA_9, fig=FIG_9),
    dict(name="fig10-surprise-niveau",
         fig_fr="Ce qui fait bouger les prix : l'écart au consensus, pas le niveau",
         fig_en="What moves prices: the gap to consensus, not the level",
         live=False, data=DATA_10, fig=FIG_10),
    dict(name="fig11-trois-reflexes",
         fig_fr="Trois réflexes à emporter",
         fig_en="Three reflexes to carry away", live=False, data=DATA_11, fig=FIG_11),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out4")
    nb_kit.build_all(META, DIR, FIGURES)
