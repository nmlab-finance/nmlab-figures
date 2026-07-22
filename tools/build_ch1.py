#!/usr/bin/env python3
"""Notebooks du chapitre 1 — « Qu'est-ce que la macroéconomie financière ? ».

Dix figures, toutes reproductibles par le code (aucune série FRED en direct) :
quatre graphiques à données embarquées (scène stylisée, valeur actuelle, courbe des
taux 2022, chemin anticipé) et six schémas conceptuels éditables (cartes, fraction,
boucle de rétroaction, deux colonnes, feuille de route). Chaque notebook = une seule
cellule code (load_*/valeurs puis build_figure(...) -> Figure), style NMLab partagé.
"""

import sys

sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit


# ═════════════════════════════════════════════════════════════════════════════
# Figure 01 — la publication qui réajuste tout (scène stylisée, données simulées)
# ═════════════════════════════════════════════════════════════════════════════

DATA_1 = '''import numpy as np
from numpy import ndarray

def simulate_reaction(pre: float, post: float, drift: float, pre_noise: float,
                      post_noise: float, scale: float, seed: int) -> tuple[ndarray, ndarray]:
    """Scène stylisée : une série bruitée qui saute au moment de la publication (t=0).
    Stylized scene: a noisy series that steps at the release (t=0).
    pre -> post est la marche ; drift ajoute une lente dérive post-publication."""
    rng = np.random.default_rng(seed)
    t = np.linspace(-30, 60, 271)
    step = 1.0 / (1.0 + np.exp(-t / scale))
    base = pre + (post - pre) * step + drift * np.clip(t, 0, None) / 60.0
    noise = np.where(t < 0, pre_noise, post_noise) * rng.standard_normal(t.size)
    noise = np.convolve(noise, np.ones(5) / 5, mode="same")
    return t, base + noise

futures = simulate_reaction(0.0, -0.78, -0.02, 0.020, 0.014, 3.0, seed=1)
yields = simulate_reaction(4.195, 4.253, -0.045, 0.006, 0.006, 1.4, seed=7)
dollar = simulate_reaction(0.0, 0.385, -0.03, 0.012, 0.010, 1.2, seed=3)'''

FIG_1 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="Un chiffre tombe, tout se réajuste",
        sub="Premier vendredi du mois, 14 h 30 à Paris : les créations d'emplois américaines",
        panels=["Contrats à terme sur indice", "Rendement à 10 ans", "Dollar face à l'euro"],
        release="publication",
        xticklabels=["−30 s", "0", "+30 s", "+60 s"],
        note="Scène stylisée (données simulées) : le sens et l'ampleur des mouvements dépendent\\n"
             "de l'écart entre le chiffre et le consensus — le monde concret, lui, n'a pas bougé."),
    "en": dict(
        title="One number lands, everything reprices",
        sub="First Friday of the month, 8:30 a.m. in New York: the U.S. job creations",
        panels=["Index futures", "10-year yield", "Dollar against the euro"],
        release="release",
        xticklabels=["−30 s", "0", "+30 s", "+60 s"],
        note="Stylized scene (simulated data): the direction and size of the moves depend on the gap\\n"
             "between the number and the consensus — the tangible world has not moved."),
}

def pct(decimals: int, lang: str) -> FuncFormatter:
    """Formateur d'axe en pourcentage, virgule décimale en français."""
    def fmt(v, _):
        s = f"{v:.{decimals}f} %"
        return s.replace(".", ",") if lang == "fr" else s
    return FuncFormatter(fmt)

def build_figure(series: list[tuple], lang: str) -> Figure:
    """Trois panneaux : contrats à terme, rendement à 10 ans, dollar — autour de t=0."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    specs = [
        dict(data=series[0], color=nm.COLORS["rose"], ylim=(-0.95, 0.30),
             yticks=[-0.8, -0.4, 0.0, 0.2], dec=1),
        dict(data=series[1], color=nm.COLORS["blue"], ylim=(4.14, 4.315),
             yticks=[4.15, 4.20, 4.25, 4.30], dec=2),
        dict(data=series[2], color=nm.COLORS["blue"], ylim=(-0.28, 0.50),
             yticks=[-0.2, 0.0, 0.2, 0.4], dec=1),
    ]
    lefts, width = [0.075, 0.396, 0.717], 0.265
    for i, sp in enumerate(specs):
        ax = fig.add_axes([lefts[i], 0.195, width, 0.452])
        t, y = sp["data"]
        ax.axvline(0, color=nm.COLORS["muted"], linestyle=(0, (5, 4)), linewidth=1.8, alpha=0.9)
        ax.plot(t, y, color=sp["color"], linewidth=2.6)
        ax.set_xlim(-30, 60)
        ax.set_xticks([-30, 0, 30, 60])
        ax.set_xticklabels(text["xticklabels"])
        ax.set_ylim(*sp["ylim"])
        ax.set_yticks(sp["yticks"])
        ax.yaxis.set_major_formatter(pct(sp["dec"], lang))
        ax.set_title(text["panels"][i], fontsize=25, fontweight="bold",
                     color=nm.COLORS["text"], pad=14)
    fig.axes[1].text(-27, 4.307, text["release"], fontsize=18, color=nm.COLORS["muted"],
                     va="top", ha="left")
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure([futures, yields, dollar], LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 02 — deux mondes, deux vitesses (schéma à deux cartes)
# ═════════════════════════════════════════════════════════════════════════════

DATA_2 = '''def two_worlds(lang: str) -> dict:
    """Les deux cartes (économie réelle / marchés) et les textes du pont, localisés.
    The two cards (real economy / markets) and the bridge texts, localized."""
    if lang == "fr":
        return dict(
            left_title="L'économie réelle",
            left=["produire, employer, dépenser", "des choses présentes, tangibles",
                  "le rythme des trimestres", "agrégats : PIB, prix, emploi"],
            right_title="Les marchés financiers",
            right=["cotent des droits sur l'avenir", "actions, obligations, devises",
                   "le rythme de la seconde", "révisés à chaque information"],
            mid_top="le point de\\nrencontre permanent",
            mid_bot="l'économie devient prix ;\\nles prix agissent en retour",
            left_foot="elle marche", right_foot="ils courent")
    return dict(
        left_title="The real economy",
        left=["producing, employing, spending", "present, tangible things",
              "the rhythm of quarters", "aggregates: GDP, prices, jobs"],
        right_title="Financial markets",
        right=["pricing claims on the future", "stocks, bonds, currencies",
               "the rhythm of the second", "revised with every headline"],
        mid_top="the permanent\\nmeeting point",
        mid_bot="the economy becomes prices;\\nprices act back on it",
        left_foot="it walks", right_foot="they run")'''

FIG_2 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Deux mondes, deux vitesses",
        sub="On les confond souvent ; tout ce parcours vit de leur différence",
        note="L'objet de l'échange, sur un marché, est l'avenir : le prix se rejoue donc à chaque\\n"
             "nouvelle — là où l'économie marche, les marchés courent."),
    "en": dict(
        title="Two worlds, two speeds",
        sub="We often confuse them; this whole journey lives on their difference",
        note="What is traded on a market is the future: the price is replayed with every piece of\\n"
             "news — where the economy walks, markets run."),
}

def build_figure(content: dict, lang: str) -> Figure:
    """Deux cartes face à face (bleue / rose), un pont central à deux flèches."""
    text = LABELS[lang]
    fig = nm.figure(height_px=988)
    ax = nm.blank_axes(fig)

    top, bottom, w = 762, 250, 545
    for x, color, title, bullets, foot in [
            (90, nm.COLORS["blue"], content["left_title"], content["left"], content["left_foot"]),
            (1112, nm.COLORS["rose"], content["right_title"], content["right"], content["right_foot"])]:
        nm.card(ax, x, bottom, w, top - bottom, edge=color, lw=2.8, radius=26)
        ax.text(x + 46, top - 72, title, ha="left", va="center", fontsize=30,
                fontweight="bold", color=nm.COLORS["text"])
        for j, item in enumerate(bullets):
            ax.text(x + 46, top - 178 - j * 92, "·  " + item, ha="left", va="center",
                    fontsize=25, color=nm.COLORS["muted"])
        ax.text(x + w / 2, bottom - 55, foot, ha="center", va="center", fontsize=25,
                color=nm.COLORS["muted"], style="italic")

    cx = 873
    ax.text(cx, 692, content["mid_top"], ha="center", va="center", fontsize=24,
            fontweight="bold", color=nm.COLORS["text"], linespacing=1.4)
    ax.annotate("", xy=(1023, 560), xytext=(723, 560),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["text"], lw=3))
    ax.annotate("", xy=(723, 492), xytext=(1023, 492),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["text"], lw=3))
    ax.text(cx, 388, content["mid_bot"], ha="center", va="center", fontsize=22,
            color=nm.COLORS["muted"], linespacing=1.45)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(two_worlds(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 03 — une discipline de jonction (trois cartes, centre mis en avant)
# ═════════════════════════════════════════════════════════════════════════════

DATA_3 = '''def junction(lang: str) -> dict:
    """Les trois cartes (macro pure, macro financière au centre, analyse d'entreprise).
    The three cards (pure macro, financial macro at center, corporate analysis)."""
    if lang == "fr":
        return dict(
            left_title="Macroéconomie pure",
            left="croissance, inflation,\\nchômage — sans se demander\\nce qu'en font les marchés",
            mid_title="Macroéconomie\\nfinancière", mid_tag="le trait d'union",
            mid="une question en tête :\\nqu'est-ce que cela change\\nau prix des actifs ?",
            right_title="Analyse d'entreprise",
            right="un bilan, une société, une\\nvalorisation — sans le décor\\ncommun des titres",
            decor="le décor commun : taux · inflation · cycle · liquidité")
    return dict(
        left_title="Pure macroeconomics",
        left="growth, inflation,\\nunemployment — never asking\\nwhat markets make of it",
        mid_title="Financial\\nmacroeconomics", mid_tag="the hyphen",
        mid="one standing question:\\nwhat does this change\\nabout asset prices?",
        right_title="Corporate analysis",
        right="one balance sheet, one firm,\\none valuation — without the\\nbackdrop shared by all",
        decor="the shared backdrop: rates · inflation · cycle · liquidity")'''

FIG_3 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Une discipline de jonction",
        sub="Deux frontières : la macro qui ignore les marchés, la finance qui ignore la macro",
        note="Son objet n'est pas tel titre, mais le décor dans lequel tous les titres sont\\n"
             "valorisés à la fois — et ce trait d'union se parcourt dans les deux sens."),
    "en": dict(
        title="A discipline of junction",
        sub="Two borders: macro that ignores markets, finance that ignores macro",
        note="Its object is not any one security, but the backdrop in which all securities are\\n"
             "valued at once — and this hyphen is traveled both ways."),
}

def build_figure(content: dict, lang: str) -> Figure:
    """Deux cartes grises encadrant une carte centrale bleue, flèches convergentes."""
    text = LABELS[lang]
    fig = nm.figure(height_px=988)
    ax = nm.blank_axes(fig)

    # Cartes latérales (liseré discret).
    for x, title, body in [(95, content["left_title"], content["left"]),
                           (1188, content["right_title"], content["right"])]:
        w = 470
        nm.card(ax, x, 352, w, 360, edge=nm.COLORS["edge"], lw=2.4, radius=24)
        ax.text(x + w / 2, 640, title, ha="center", va="center", fontsize=28,
                fontweight="bold", color=nm.COLORS["text"])
        ax.text(x + w / 2, 505, body, ha="center", va="center", fontsize=24,
                color=nm.COLORS["muted"], linespacing=1.5)

    # Carte centrale (bleue, plus haute).
    cx = 875
    nm.card(ax, 648, 300, 455, 452, edge=nm.COLORS["blue"], lw=3.0, radius=26)
    ax.text(cx, 675, content["mid_title"], ha="center", va="center", fontsize=28,
            fontweight="bold", color=nm.COLORS["text"], linespacing=1.3)
    ax.text(cx, 548, content["mid_tag"], ha="center", va="center", fontsize=25,
            fontweight="bold", color=nm.COLORS["rose"], style="italic")
    ax.text(cx, 430, content["mid"], ha="center", va="center", fontsize=24,
            color=nm.COLORS["muted"], linespacing=1.5)

    ax.annotate("", xy=(645, 525), xytext=(568, 525),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=2.6))
    ax.annotate("", xy=(1106, 525), xytext=(1183, 525),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=2.6))
    ax.text(cx, 250, content["decor"], ha="center", va="center", fontsize=25,
            color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(junction(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 04 — le prix d'un actif est une fraction (schéma)
# ═════════════════════════════════════════════════════════════════════════════

DATA_4 = '''def fraction_parts(lang: str) -> dict:
    """Le numérateur / dénominateur de la fraction et les deux cartes-leviers.
    The numerator / denominator of the fraction and the two lever cards."""
    if lang == "fr":
        return dict(
            price="Prix de l'actif  =",
            num="Revenus futurs attendus", num_sub="bénéfices · dividendes · intérêts · loyers",
            den="Taux d'actualisation", den_sub="taux d'intérêt + inflation attendue + prime de risque",
            up_title="Le haut monte", up_body="profits espérés en hausse",
            up_arrow="→  le prix de l'actif MONTE",
            down_title="Le bas monte", down_body="taux ou prime de risque en hausse",
            down_arrow="→  le prix de l'actif BAISSE")
    return dict(
        price="Asset price  =",
        num="Expected future income", num_sub="profits · dividends · interest · rents",
        den="Discount rate", den_sub="interest rate + expected inflation + risk premium",
        up_title="The top rises", up_body="expected profits up",
        up_arrow="→  the asset price RISES",
        down_title="The bottom rises", down_body="rates or risk premium up",
        down_arrow="→  the asset price FALLS")'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le prix d'un actif est une fraction",
        sub="Deux leviers seulement — et l'économie agit sur les deux à la fois",
        note="Une même nouvelle peut pousser les deux étages à la fois : le résultat dépend du levier qui l'emporte."),
    "en": dict(
        title="An asset's price is a fraction",
        sub="Two levers only — and the economy acts on both at once",
        note="The same news can push both floors at once: the result depends on which lever wins."),
}

def build_figure(content: dict, lang: str) -> Figure:
    """Fraction à gauche (revenus / taux), deux cartes-leviers à droite (monte / baisse)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=932)
    ax = nm.blank_axes(fig)

    # Fraction.
    ax.text(60, 500, content["price"], ha="left", va="center", fontsize=34, color=nm.COLORS["text"])
    ax.plot([432, 812], [500, 500], color=nm.COLORS["text"], linewidth=2.6)
    ax.text(622, 585, content["num"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(622, 527, content["num_sub"], ha="center", va="center", fontsize=22, color=nm.COLORS["blue"])
    ax.text(622, 452, content["den"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(622, 396, content["den_sub"], ha="center", va="center", fontsize=22, color=nm.COLORS["rose"])

    # Cartes-leviers.
    nm.card(ax, 990, 505, 655, 178, edge=nm.COLORS["blue"], lw=2.6, radius=22)
    ax.text(1030, 642, content["up_title"], ha="left", va="center", fontsize=28,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(1030, 588, content["up_body"], ha="left", va="center", fontsize=24, color=nm.COLORS["muted"])
    ax.text(1030, 538, content["up_arrow"], ha="left", va="center", fontsize=25,
            fontweight="bold", color=nm.COLORS["blue"])

    nm.card(ax, 990, 252, 655, 190, edge=nm.COLORS["rose"], lw=2.6, radius=22)
    ax.text(1030, 405, content["down_title"], ha="left", va="center", fontsize=28,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(1030, 350, content["down_body"], ha="left", va="center", fontsize=24, color=nm.COLORS["muted"])
    ax.text(1030, 298, content["down_arrow"], ha="left", va="center", fontsize=25,
            fontweight="bold", color=nm.COLORS["rose"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(fraction_parts(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 05 — valeur actuelle de 100 € selon l'horizon (données calculées)
# ═════════════════════════════════════════════════════════════════════════════

DATA_5 = '''import numpy as np
from numpy import ndarray

def present_value() -> tuple[ndarray, ndarray, ndarray]:
    """Valeur actuelle d'une promesse de 100 € selon l'horizon, à 4 % et 8 %.
    Present value of a €100 promise by horizon, at 4% and 8%. P = 100 / (1+r)**t."""
    years = np.linspace(0, 30, 301)
    return years, 100 / 1.04 ** years, 100 / 1.08 ** years

years, pv4, pv8 = present_value()'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Ce que vaut aujourd'hui une promesse de 100 €",
        sub="selon l'horizon du versement et le taux d'actualisation",
        xlab="Dans combien d'années la promesse de 100 € est-elle versée ?",
        ylab="Valeur aujourd'hui (en €)",
        lab4="à 4 % par an", lab8="à 8 % par an",
        inner="Le même écart de taux, presque invisible à un an,\\nécrase la valeur des promesses lointaines.",
        v96="≈ 96 €", v93="≈ 93 €", v31="≈ 31 €", v10="≈ 10 €"),
    "en": dict(
        title="What a €100 promise is worth today",
        sub="by payment horizon and discount rate",
        xlab="In how many years is the €100 promise paid?",
        ylab="Value today (in €)",
        lab4="at 4% per year", lab8="at 8% per year",
        inner="The same rate gap, almost invisible at one year,\\ncrushes the value of distant promises.",
        v96="≈ €96", v93="≈ €93", v31="≈ €31", v10="≈ €10"),
}

def build_figure(years, pv4, pv8, lang: str) -> Figure:
    """Deux courbes d'actualisation (4 % bleu, 8 % rose), repères à 1 an et 30 ans."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1210)
    ax = nm.axes(fig, left=0.09, bottom=0.115)
    for xv in (1, 30):
        ax.axvline(xv, color=nm.COLORS["muted"], linestyle=(0, (5, 4)), linewidth=1.5, alpha=0.6)
    ax.plot(years, pv4, color=nm.COLORS["blue"], linewidth=3.4, zorder=3)
    ax.plot(years, pv8, color=nm.COLORS["rose"], linewidth=3.4, zorder=3)
    ax.scatter([1, 30], [100 / 1.04, 100 / 1.04 ** 30], s=70, color=nm.COLORS["blue"], zorder=5)
    ax.scatter([1, 30], [100 / 1.08, 100 / 1.08 ** 30], s=70, color=nm.COLORS["rose"], zorder=5)
    ax.set_xlim(0, 31.5)
    ax.set_xticks([0, 1, 5, 10, 15, 20, 25, 30])
    ax.set_ylim(0, 104)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel(text["xlab"])
    ax.set_ylabel(text["ylab"])
    ax.text(1.5, 97.5, text["v96"], fontsize=25, fontweight="bold", color=nm.COLORS["text"], va="center")
    ax.text(1.5, 88.0, text["v93"], fontsize=25, fontweight="bold", color=nm.COLORS["text"], va="center")
    ax.text(29.3, 34, text["v31"], fontsize=25, fontweight="bold", color=nm.COLORS["text"], va="center", ha="right")
    ax.text(29.3, 13, text["v10"], fontsize=25, fontweight="bold", color=nm.COLORS["text"], va="center", ha="right")
    ax.text(15.5, 62, text["lab4"], fontsize=25, fontweight="bold", color=nm.COLORS["blue"], ha="center")
    ax.text(13.5, 22, text["lab8"], fontsize=25, fontweight="bold", color=nm.COLORS["rose"], ha="center")
    ax.text(14.0, 88, text["inner"], fontsize=21, color=nm.COLORS["muted"], style="italic",
            ha="center", va="center", linespacing=1.5)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig)
    return fig

build_figure(years, pv4, pv8, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 06 — la courbe des taux 2022 (deux dates, valeurs lues sur la figure)
# ═════════════════════════════════════════════════════════════════════════════

DATA_6 = '''def yield_curves() -> tuple[list[float], list[float]]:
    """Rendement du Trésor américain par échéance, deux dates (valeurs lues sur la figure).
    U.S. Treasury yield by maturity on two dates (values read from the figure).
    Source : U.S. Department of the Treasury (daily yield curve)."""
    jan_2022 = [0.05, 0.08, 0.22, 0.40, 0.78, 1.02, 1.37, 1.55, 1.63, 2.05, 2.01]
    dec_2022 = [4.12, 4.42, 4.76, 4.72, 4.41, 4.22, 3.99, 3.96, 3.88, 4.14, 3.97]
    return jan_2022, dec_2022

jan22, dec22 = yield_curves()'''

FIG_6 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="En 2022, le prix de l'argent a bondi sur toutes les échéances",
        sub="Rendement des emprunts d'État américains selon leur durée, avant et après le resserrement de la Fed",
        mats=["1M", "3M", "6M", "1A", "2A", "3A", "5A", "7A", "10A", "20A", "30A"],
        xlab="Maturité  —  durée de l'emprunt, de 1 mois à 30 ans",
        ylab="Rendement annuel exigé par les prêteurs",
        leg_jan="3 janvier 2022   ·   début du resserrement",
        leg_dec="30 décembre 2022   ·   un an plus tard",
        rise="Toute la courbe a monté :\\nc'est le bond du taux d'actualisation",
        gap="+2,6 points\\nen un an",
        invert="fin 2022, le 2 ans rapporte\\nplus que le 10 ans :\\ncourbe « inversée »",
        note="Source : U.S. Department of the Treasury — rendements des bons et obligations du Trésor."),
    "en": dict(
        title="In 2022, the price of money jumped across every maturity",
        sub="Yield on U.S. government debt by maturity, before and after the Fed's tightening",
        mats=["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"],
        xlab="Maturity  —  loan term, from 1 month to 30 years",
        ylab="Annual yield required by lenders",
        leg_jan="January 3, 2022   ·   start of tightening",
        leg_dec="December 30, 2022   ·   one year later",
        rise="The whole curve moved up:\\nthat is the jump in the discount rate",
        gap="+2.6 points\\nin one year",
        invert="by end-2022, the 2-year pays\\nmore than the 10-year:\\nan « inverted » curve",
        note="Source: U.S. Department of the Treasury — Treasury bill and bond yields."),
}

def pct(lang: str) -> FuncFormatter:
    """Formateur d'axe : « 4 % » (virgule décimale non nécessaire ici)."""
    return FuncFormatter(lambda v, _: f"{v:.0f} %")

def build_figure(jan22: list[float], dec22: list[float], lang: str) -> Figure:
    """Deux courbes de taux (janv. bleu, déc. rose), écart de +2,6 pts marqué à 5 ans."""
    text = LABELS[lang]
    x = list(range(len(text["mats"])))
    fig = nm.figure(height_px=1154)
    ax = nm.axes(fig, left=0.088, bottom=0.13)

    ax.plot(x, jan22, color=nm.COLORS["blue"], linewidth=3.2, marker="o", markersize=11,
            markerfacecolor=nm.COLORS["bg"], markeredgewidth=2.6, label=text["leg_jan"], zorder=3)
    ax.plot(x, dec22, color=nm.COLORS["rose"], linewidth=3.2, marker="o", markersize=11,
            markerfacecolor=nm.COLORS["bg"], markeredgewidth=2.6, label=text["leg_dec"], zorder=3)

    ax.set_xlim(-0.4, len(x) - 0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(text["mats"])
    ax.set_ylim(-0.25, 5.6)
    ax.set_yticks(range(0, 6))
    ax.yaxis.set_major_formatter(pct(lang))
    ax.set_xlabel(text["xlab"])
    ax.set_ylabel(text["ylab"])

    # Écart à 5 ans (index 6) : double flèche + libellé.
    ax.annotate("", xy=(6, dec22[6] - 0.05), xytext=(6, jan22[6] + 0.05),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["muted"], lw=1.8))
    ax.text(6.28, 2.55, text["gap"], ha="left", va="center", fontsize=24, fontweight="bold",
            color=nm.COLORS["text"], linespacing=1.4)
    ax.text(6.0, 4.15, text["rise"], ha="left", va="bottom", fontsize=22, fontweight="bold",
            color=nm.COLORS["rose"], linespacing=1.4)
    ax.text(8.35, 3.3, text["invert"], ha="center", va="center", fontsize=18,
            color=nm.COLORS["muted"], style="italic", linespacing=1.4)

    ax.legend(loc="center left", bbox_to_anchor=(0.02, 0.40), frameon=True, fontsize=19,
              labelcolor=nm.COLORS["muted"], facecolor=nm.COLORS["card"], edgecolor=nm.COLORS["edge"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(jan22, dec22, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 07 — le marché cote le chemin, pas le taux du jour (stylisé)
# ═════════════════════════════════════════════════════════════════════════════

DATA_7 = '''def rate_paths() -> tuple[list[float], list[float], list[float]]:
    """Deux trajectoires stylisées du taux directeur sur trois ans (points lus).
    Two stylized policy-rate paths over three years (points read from the figure)."""
    x = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    veille = [4.0, 3.75, 3.5, 3.25, 3.0, 2.75, 2.5]
    revise = [4.0, 3.9, 3.75, 3.6, 3.5, 3.4, 3.3]
    return x, veille, revise

xpts, veille, revise = rate_paths()'''

FIG_7 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="Le marché cote le chemin, pas le taux du jour",
        sub="Trajectoire anticipée du taux directeur, avant et après une surprise d'inflation",
        xticklabels=["aujourd'hui", "+1 an", "+2 ans", "+3 ans"],
        today="aujourd'hui : le taux n'a pas bougé",
        move="c'est ce déplacement\\nque le marché cote",
        leg_v="chemin anticipé la veille", leg_r="chemin révisé après la surprise",
        note="Une donnée ne déplace les prix que si elle modifie la trajectoire attendue de la\\n"
             "politique monétaire : moins de baisses anticipées, taux du jour inchangé. Stylisé."),
    "en": dict(
        title="The market prices the path, not today's rate",
        sub="Expected policy-rate path, before and after an inflation surprise",
        xticklabels=["today", "+1 yr", "+2 yr", "+3 yr"],
        today="today: the rate has not moved",
        move="this is the shift\\nthe market prices",
        leg_v="path expected the day before", leg_r="path revised after the surprise",
        note="A data point moves prices only if it shifts the expected path of monetary policy:\\n"
             "fewer anticipated cuts, today's rate unchanged. Stylized."),
}

def pct(lang: str) -> FuncFormatter:
    """Formateur d'axe en pourcentage à une décimale (virgule en français)."""
    def fmt(v, _):
        s = f"{v:.1f} %"
        return s.replace(".", ",") if lang == "fr" else s
    return FuncFormatter(fmt)

def build_figure(xpts, veille, revise, lang: str) -> Figure:
    """Chemin de la veille (bleu plein) vs chemin révisé (rose tireté), aire entre les deux."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.axes(fig, left=0.072, bottom=0.135)
    ax.fill_between(xpts, veille, revise, color=nm.COLORS["rose"], alpha=0.14, zorder=1)
    ax.plot(xpts, revise, color=nm.COLORS["rose"], linewidth=3.4, linestyle=(0, (7, 4)),
            marker="o", markersize=11, markerfacecolor=nm.COLORS["rose"], zorder=3, label=text["leg_r"])
    ax.plot(xpts, veille, color=nm.COLORS["blue"], linewidth=3.4, marker="o", markersize=11,
            markerfacecolor=nm.COLORS["blue"], zorder=3, label=text["leg_v"])
    ax.scatter([0], [4.0], s=200, color=nm.COLORS["text"], zorder=6, edgecolors=nm.COLORS["bg"], linewidths=2)

    ax.set_xlim(-0.14, 3.18)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(text["xticklabels"])
    ax.set_ylim(2.35, 4.28)
    ax.set_yticks([2.5, 3.0, 3.5, 4.0])
    ax.yaxis.set_major_formatter(pct(lang))

    ax.annotate(text["today"], xy=(0.03, 4.0), xytext=(0.55, 4.14),
                fontsize=23, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.text(2.15, 3.02, text["move"], ha="center", va="center", fontsize=24,
            color=nm.COLORS["text"], linespacing=1.4)

    handles, labels = ax.get_legend_handles_labels()
    order = [labels.index(text["leg_v"]), labels.index(text["leg_r"])]
    ax.legend([handles[i] for i in order], [labels[i] for i in order],
              loc="lower left", bbox_to_anchor=(0.02, 0.03), frameon=True, fontsize=20,
              labelcolor=nm.COLORS["muted"], facecolor=nm.COLORS["card"], edgecolor=nm.COLORS["edge"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(xpts, veille, revise, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 08 — le miroir agit sur ce qu'il reflète (boucle de rétroaction)
# ═════════════════════════════════════════════════════════════════════════════

DATA_8 = '''def loop_texts(lang: str) -> dict:
    """Cartes de la boucle (économie / marchés), conditions financières et légendes.
    Loop cards (economy / markets), financial conditions and captions, localized."""
    if lang == "fr":
        return dict(
            eco_title="L'ÉCONOMIE RÉELLE", eco_sub="croissance · inflation · emploi",
            mkt_title="LES MARCHÉS", mkt_sub="actions · obligations · change",
            out="données, résultats,\\ndécisions", out_tag="(l'aller)",
            back="les conditions financières",
            small=[("Patrimoine", "richesse perçue → dépense"),
                   ("Crédit", "crédit cher → projets gelés"),
                   ("Change", "exportations, prix importés")])
    return dict(
        eco_title="THE REAL ECONOMY", eco_sub="growth · inflation · jobs",
        mkt_title="THE MARKETS", mkt_sub="stocks · bonds · FX",
        out="data, results,\\ndecisions", out_tag="(the outbound)",
        back="financial conditions",
        small=[("Wealth", "perceived wealth → spending"),
               ("Credit", "costly credit → frozen projects"),
               ("FX", "exports, import prices")])'''

FIG_8 = '''from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch

LABELS = {
    "fr": dict(
        title="Le miroir agit sur ce qu'il reflète",
        sub="Les prix d'actifs n'enregistrent pas seulement l'économie : ils la modifient en retour",
        note="La banque centrale ne fixe qu'un taux à très court terme : tout le reste — taux longs,\\n"
             "crédit, Bourse, change — passe par ce relais. « Ce n'est pas la banque centrale qui fixe\\n"
             "votre taux immobilier, c'est le marché obligataire. »"),
    "en": dict(
        title="The mirror acts on what it reflects",
        sub="Asset prices don't just record the economy: they change it back",
        note="The central bank sets only a very short-term rate: everything else — long rates,\\n"
             "credit, the stock market, FX — runs through this relay. « It is not the central bank that\\n"
             "sets your mortgage rate, it is the bond market. »"),
}

def build_figure(content: dict, lang: str) -> Figure:
    """Deux cartes reliées par une boucle (aller/retour) ; trois cartes de conditions."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    ax = nm.blank_axes(fig)

    # Cartes centrales.
    nm.card(ax, 595, 830, 680, 150, edge=nm.COLORS["blue"], lw=2.8, radius=22)
    ax.text(935, 933, content["eco_title"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(935, 878, content["eco_sub"], ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])
    nm.card(ax, 595, 165, 680, 150, edge=nm.COLORS["rose"], lw=2.8, radius=22)
    ax.text(935, 268, content["mkt_title"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(935, 213, content["mkt_sub"], ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])

    # Boucle : flèche descendante à droite (aller), montante à gauche (retour).
    ax.add_patch(FancyArrowPatch((1255, 828), (1255, 317), connectionstyle="arc3,rad=-0.42",
                 arrowstyle="-|>", mutation_scale=30, lw=3, color=nm.COLORS["muted"]))
    ax.add_patch(FancyArrowPatch((615, 317), (615, 828), connectionstyle="arc3,rad=-0.42",
                 arrowstyle="-|>", mutation_scale=30, lw=3, color=nm.COLORS["muted"]))
    ax.text(1560, 615, content["out"], ha="center", va="center", fontsize=25,
            color=nm.COLORS["text"], linespacing=1.4)
    ax.text(1548, 470, content["out_tag"], ha="center", va="center", fontsize=22,
            color=nm.COLORS["muted"], style="italic")

    # Trois cartes de conditions financières (à gauche).
    ax.text(245, 735, content["back"], ha="left", va="center", fontsize=26,
            fontweight="bold", color=nm.COLORS["text"])
    for i, (title, body) in enumerate(content["small"]):
        y = 585 - i * 145
        nm.card(ax, 45, y, 400, 110, edge=nm.COLORS["edge"], lw=2.2, radius=18)
        ax.text(70, y + 68, title, ha="left", va="center", fontsize=25,
                fontweight="bold", color=nm.COLORS["text"])
        ax.text(70, y + 26, body, ha="left", va="center", fontsize=22, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(loop_texts(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 09 — boussole, pas boule de cristal (deux colonnes)
# ═════════════════════════════════════════════════════════════════════════════

DATA_9 = '''def compass(lang: str) -> tuple[dict, dict]:
    """Les deux colonnes : ce que la discipline permet / interdit d'espérer, localisées.
    The two columns: what the discipline allows / forbids hoping for, localized."""
    if lang == "fr":
        left = dict(title="Elle permet", items=[
            "savoir dans quel régime on investit —\\ninflation, taux, cycle",
            "distinguer, dans une nouvelle, l'attendu\\nde la vraie surprise",
            "garder son sang-froid dans la panique\\ncomme dans l'euphorie",
            "bâtir un portefeuille qui résiste\\nà plusieurs scénarios"])
        right = dict(title="Elle interdit d'espérer", items=[
            "prédire le prochain mouvement\\ndes marchés",
            "exploiter une régularité connue de tous :\\nelle est déjà dans les prix",
            "s'enrichir en entrant et sortant\\nsans cesse (market timing)",
            "prendre les régularités pour des lois —\\n2022 a démenti courbe des taux et 60/40"])
        return left, right
    left = dict(title="What it allows", items=[
        "knowing which regime you invest in —\\ninflation, rates, cycle",
        "telling, in a piece of news, the expected\\nfrom the true surprise",
        "keeping your nerve in panic\\nas in euphoria",
        "building a portfolio that withstands\\nseveral scenarios"])
    right = dict(title="What it forbids hoping for", items=[
        "predicting the next market\\nmove",
        "exploiting a regularity everyone knows:\\nit is already in the price",
        "getting rich by entering and exiting\\nconstantly (market timing)",
        "taking regularities for laws —\\n2022 belied the yield curve and 60/40"])
    return left, right'''

FIG_9 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Boussole, pas boule de cristal",
        sub="Ce que la macroéconomie financière permet — et ce qu'elle interdit d'espérer",
        note="La réflexivité : dès qu'un scénario fait consensus, les prix se déplacent et le défont.\\n"
             "Une prévision de marché n'est jamais une prévision météo."),
    "en": dict(
        title="A compass, not a crystal ball",
        sub="What financial macroeconomics allows — and what it forbids hoping for",
        note="Reflexivity: as soon as a scenario becomes consensus, prices move and undo it.\\n"
             "A market forecast is never a weather forecast."),
}

def build_figure(columns: tuple[dict, dict], lang: str) -> Figure:
    """Deux grandes cartes (permet / interdit), quatre puces fléchées chacune."""
    text = LABELS[lang]
    left, right = columns
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    top, bottom, w = 848, 155, 675
    for x, color, col in [(95, nm.COLORS["blue"], left), (978, nm.COLORS["rose"], right)]:
        nm.card(ax, x, bottom, w, top - bottom, edge=color, lw=2.8, radius=26)
        ax.text(x + 50, top - 68, col["title"], ha="left", va="center", fontsize=30,
                fontweight="bold", color=color)
        for j, item in enumerate(col["items"]):
            y = top - 192 - j * 130
            ax.text(x + 48, y, "→", ha="left", va="center", fontsize=24, color=color)
            ax.text(x + 100, y, item, ha="left", va="center", fontsize=23,
                    color=nm.COLORS["muted"], linespacing=1.45)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(compass(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 10 — la carte du parcours (quatre étapes + bandeau fil rouge)
# ═════════════════════════════════════════════════════════════════════════════

DATA_10 = '''def roadmap(lang: str) -> tuple[list[tuple[str, str, list[str]]], str]:
    """Les quatre étapes (numéro, titre, puces) et le bandeau fil rouge, localisés.
    The four stages (number, title, bullets) and the common-thread banner, localized."""
    if lang == "fr":
        stages = [
            ("1", "Les briques", ["PIB & croissance", "monnaie", "inflation", "taux d'intérêt"]),
            ("2", "La dynamique", ["cycle économique", "marché du travail", "indicateurs", "banques centrales"]),
            ("3", "Macro & marchés", ["dette publique", "liquidité mondiale", "crédit & crises", "régimes & allocation"]),
            ("4", "La pratique", ["tableau de bord", "veille automatisée"]),
        ]
        banner = "Fil rouge : 2020 → 2025, du choc COVID à l'atterrissage en douceur"
        return stages, banner
    stages = [
        ("1", "The building blocks", ["GDP & growth", "money", "inflation", "interest rates"]),
        ("2", "The dynamics", ["business cycle", "labor market", "indicators", "central banks"]),
        ("3", "Macro & markets", ["public debt", "global liquidity", "credit & crises", "regimes & allocation"]),
        ("4", "Practice", ["dashboard", "automated monitoring"]),
    ]
    banner = "Common thread: 2020 → 2025, from the COVID shock to the soft landing"
    return stages, banner'''

FIG_10 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La carte du parcours",
        sub="Du plus élémentaire au plus complet — et un même épisode pour tout ancrer",
        note="Chaque module viendra chercher ses exemples dans la même histoire vraie : cinq ans\\n"
             "qui ont mis presque toutes les certitudes en défaut."),
    "en": dict(
        title="The roadmap",
        sub="From the most elementary to the most complete — and one same episode to anchor it all",
        note="Each module will draw its examples from the same true story: five years that put\\n"
             "almost every certainty to the test."),
}

def build_figure(content: tuple, lang: str) -> Figure:
    """Quatre cartes numérotées reliées par des flèches, puis un bandeau fil rouge."""
    text = LABELS[lang]
    stages, banner = content
    fig = nm.figure(height_px=1004)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 372, 45, 100
    top, bottom = 735, 305
    cy = (top + bottom) / 2
    for i, (num, title, bullets) in enumerate(stages):
        x = x0 + i * (card_w + gap)
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS["blue"], lw=2.4, radius=22)
        ax.text(x + 40, top - 58, num, ha="left", va="center", fontsize=36,
                fontweight="bold", color=nm.COLORS["blue"])
        ax.text(x + 95, top - 58, title, ha="left", va="center", fontsize=25.5,
                fontweight="bold", color=nm.COLORS["text"])
        for j, item in enumerate(bullets):
            ax.text(x + 38, top - 148 - j * 66, "·  " + item, ha="left", va="center",
                    fontsize=22, color=nm.COLORS["muted"])
        if i < len(stages) - 1:
            ax.annotate("", xy=(x + card_w + gap - 6, cy), xytext=(x + card_w + 6, cy),
                        arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["muted"], lw=2.4))

    nm.card(ax, x0, 108, (x0 + 4 * card_w + 3 * gap) - x0, 100, edge=nm.COLORS["rose"], lw=2.6, radius=24)
    ax.text((2 * x0 + 4 * card_w + 3 * gap) / 2, 158, banner, ha="center", va="center",
            fontsize=29, fontweight="bold", color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(roadmap(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Assemblage
# ═════════════════════════════════════════════════════════════════════════════

META = dict(
    num="1",
    title_fr="Qu'est-ce que la macroéconomie financière ?",
    title_en="What Is Financial Macroeconomics? When the Economy Meets the Markets",
    slug_fr="qu-est-ce-que-la-macroeconomie-financiere",
    slug_en="what-is-financial-macroeconomics",
)
DIR = "macro/01-macroeconomie-financiere"

FIGURES = [
    dict(name="fig01-onde-de-choc",
         fig_fr="Un chiffre tombe, tout se réajuste",
         fig_en="One number lands, everything reprices",
         live=False, data=DATA_1, fig=FIG_1),
    dict(name="fig02-economie-marches",
         fig_fr="Deux mondes, deux vitesses",
         fig_en="Two worlds, two speeds",
         live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-discipline-jonction",
         fig_fr="Une discipline de jonction",
         fig_en="A discipline of junction",
         live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-fraction-prix",
         fig_fr="Le prix d'un actif est une fraction",
         fig_en="An asset's price is a fraction",
         live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-valeur-actuelle",
         fig_fr="Ce que vaut aujourd'hui une promesse de 100 €",
         fig_en="What a €100 promise is worth today",
         live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-courbe-taux",
         fig_fr="En 2022, le prix de l'argent a bondi sur toutes les échéances",
         fig_en="In 2022, the price of money jumped across every maturity",
         live=False, data=DATA_6, fig=FIG_6),
    dict(name="fig07-chemin-taux",
         fig_fr="Le marché cote le chemin, pas le taux du jour",
         fig_en="The market prices the path, not today's rate",
         live=False, data=DATA_7, fig=FIG_7),
    dict(name="fig08-boucle-retroaction",
         fig_fr="Le miroir agit sur ce qu'il reflète",
         fig_en="The mirror acts on what it reflects",
         live=False, data=DATA_8, fig=FIG_8),
    dict(name="fig09-boussole",
         fig_fr="Boussole, pas boule de cristal",
         fig_en="A compass, not a crystal ball",
         live=False, data=DATA_9, fig=FIG_9),
    dict(name="fig10-carte-parcours",
         fig_fr="La carte du parcours",
         fig_en="The roadmap",
         live=False, data=DATA_10, fig=FIG_10),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out1")
    nb_kit.build_all(META, DIR, FIGURES)
