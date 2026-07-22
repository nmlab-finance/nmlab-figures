#!/usr/bin/env python3
"""Génère les notebooks du chapitre 2 — Pourquoi comprendre l'économie.

Toutes les figures sont des schémas ou des illustrations stylisées (aucune série
FRED en direct, aucune photo) → données EMBARQUÉES (live=False). Convention
« strict » : une seule cellule code, fonctions typées + docstrings — load_*()
puis build_figure(...) -> Figure ; LABELS={"fr":…,"en":…} ; LANG.
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit


META = dict(
    num="2",
    title_fr="Pourquoi un investisseur a besoin de comprendre l'économie : l'intuition de départ",
    title_en="Why an Investor Needs to Understand the Economy: The Starting Intuition",
    slug_fr="pourquoi-un-investisseur-doit-comprendre-l-economie",
    slug_en="why-investors-need-to-understand-the-economy",
)
DIR = "macro/02-comprendre-l-economie"


# ── Figure 01 — deux épargnants sur quinze ans (trajectoires simulées) ────────

DATA_1 = '''import numpy as np
from pandas import Series, date_range

def load_paths() -> tuple[Series, Series]:
    """Deux trajectoires de portefeuille simulées sur quinze ans (base 100), 2010-2025.
    L'épargnant immobile reste investi ; l'actif vend au creux de 2020 et revient après
    le rebond, verrouillant son retard. Données simulées à graine fixe — illustration
    stylisée dans l'esprit des études SPIVA et Mind the Gap.
    Two simulated fifteen-year portfolio paths (base 100). The active saver sells at the
    2020 trough and returns after the rebound, locking in his lag. Fixed-seed data."""
    dates = date_range("2010-01-01", "2025-06-01", freq="MS")
    t = np.array([d.year + (d.month - 1) / 12 for d in dates])
    # marché = épargnant immobile : points de contrôle interpolés
    imm_x = [2010, 2013, 2016, 2019, 2020.0, 2020.25, 2020.42, 2021.5, 2022.8, 2024.2, 2025.5]
    imm_y = [100, 124, 150, 184, 205, 221, 176, 238, 201, 270, 298]
    # ondulation douce : pont brownien à graine fixe, ancré à 0 aux extrémités
    rng = np.random.default_rng(11)
    wander = np.cumsum(rng.normal(0, 0.9, len(t)))
    wander = (wander - np.linspace(0, wander[-1], len(t))) * 0.45
    immobile = np.interp(t, imm_x, imm_y) + wander
    # épargnant actif : identique jusqu'à la vente, puis trajectoire propre
    act_x = [2020.42, 2021.1, 2021.7, 2023.0, 2024.2, 2025.5]
    act_y = [176, 176, 193, 163, 169, 180]
    active = immobile.copy()
    sold = t >= 2020.42
    active[sold] = np.interp(t[sold], act_x, act_y) + wander[sold]
    return Series(immobile, index=dates), Series(active, index=dates)

immobile, active = load_paths()'''

FIG_1 = '''import matplotlib.dates as mdates
from matplotlib.figure import Figure
from pandas import Series

LABELS = {
    "fr": dict(
        title="Quinze ans, deux épargnants",
        sub="Le même marché, deux comportements — la scène qui ouvre le chapitre (stylisée)",
        ylab="portefeuille, base 100",
        immobile="l'épargnant immobile", active="l'épargnant actif",
        mult_imm="\\u00d7 3,0", mult_act="\\u00d7 1,8",
        sells="sort après la chute", returns="revient après le rebond",
        note="Illustration stylisée (données simulées), dans l'esprit des études SPIVA et Mind the Gap :\\n"
             "rester investi bat presque toujours les allers-retours dictés par les convictions du moment."),
    "en": dict(
        title="Fifteen years, two savers",
        sub="The same market, two behaviors — the scene that opens the chapter (stylized)",
        ylab="portfolio, base 100",
        immobile="the motionless saver", active="the active saver",
        mult_imm="\\u00d7 3.0", mult_act="\\u00d7 1.8",
        sells="sells after the fall", returns="returns after the rebound",
        note="Stylized illustration (simulated data), in the spirit of the SPIVA and Mind the Gap studies:\\n"
             "staying invested almost always beats the round-trips dictated by the conviction of the moment."),
}

def build_figure(immobile: Series, active: Series, lang: str) -> Figure:
    """Deux trajectoires base 100 : l'immobile (×3,0) contre l'actif (×1,8)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1083)
    ax = nm.axes(fig, left=0.088, right=0.93)
    line_act, = ax.plot(active.index, active, color=nm.COLORS["rose"], linewidth=2.9, label=text["active"], zorder=3)
    line_imm, = ax.plot(immobile.index, immobile, color=nm.COLORS["blue"], linewidth=3.1, label=text["immobile"], zorder=4)
    ax.set_ylim(90, 315)
    ax.set_yticks(range(100, 301, 25))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.set_xlim(immobile.index[0], immobile.index[-1])
    ax.xaxis.set_major_locator(mdates.YearLocator(3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.annotate(text["mult_imm"], xy=(immobile.index[-1], immobile.iloc[-1]), xytext=(12, 0),
                textcoords="offset points", ha="left", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["blue2"], annotation_clip=False)
    ax.annotate(text["mult_act"], xy=(active.index[-1], active.iloc[-1]), xytext=(12, 0),
                textcoords="offset points", ha="left", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["rose"], annotation_clip=False)
    leg = ax.legend(handles=[line_imm, line_act], loc="upper left", fontsize=22, framealpha=1.0,
                    facecolor=nm.COLORS["card"], edgecolor=nm.COLORS["edge"], labelcolor=nm.COLORS["text"],
                    borderpad=0.9, handlelength=1.6, bbox_to_anchor=(0.02, 0.98))
    leg.set_zorder(6)
    sell_x = active.index[(active.index.year == 2020) & (active.index.month == 6)][0]
    ax.annotate(text["sells"], xy=(sell_x, active.loc[sell_x]), xytext=(0, -78),
                textcoords="offset points", ha="center", va="top", fontsize=21,
                color=nm.COLORS["rose"], arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.2))
    ret_x = active.index[(active.index.year == 2021) & (active.index.month == 8)][0]
    ax.annotate(text["returns"], xy=(ret_x, active.loc[ret_x]), xytext=(6, 58),
                textcoords="offset points", ha="center", va="bottom", fontsize=21,
                color=nm.COLORS["rose"], arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.2))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(immobile, active, LANG)'''


# ── Figure 02 — la surprise, pas le niveau (schéma) ──────────────────────────

DATA_2 = '''def surprise_scene(lang: str) -> dict:
    """Textes localisés du schéma « surprise vs niveau ».
    Localized texts of the « surprise vs level » diagram."""
    if lang == "fr":
        return dict(
            up="hausse du prix \\u25b2", down="\\u25bc baisse du prix",
            react="réaction", solid="2,5 %, c'est une croissance solide\\u2026",
            left="\\u25c4 le chiffre déçoit", right="le chiffre surprend en bien \\u25ba",
            callout=["Ce n'est pas le niveau qui compte,", "c'est l'écart au consensus"],
            box=["Croissance publiée : 2,5 %", "Consensus attendu : 3,0 %", "surprise de \\u22120,5 point"],
            miss="\\u2026mais c'est une déception : le marché recule",
            formula="SURPRISE  =  chiffre publié  \\u2212  ce que le marché attendait")
    return dict(
        up="price rises \\u25b2", down="\\u25bc price falls",
        react="reaction", solid="2.5% is solid growth\\u2026",
        left="\\u25c4 the figure disappoints", right="the figure surprises to the upside \\u25ba",
        callout=["It is not the level that matters,", "it is the gap to consensus"],
        box=["Reported growth: 2.5%", "Expected consensus: 3.0%", "surprise of \\u22120.5 point"],
        miss="\\u2026but it is a disappointment: the market falls",
        formula="SURPRISE  =  reported figure  \\u2212  what the market expected")'''

FIG_2 = '''from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

LABELS = {
    "fr": dict(
        title="Le marché paie la surprise, pas le niveau",
        sub="Ce qui fait bouger un prix, ce n'est pas qu'un chiffre soit bon ou mauvais dans l'absolu,\\n"
            "mais qu'il batte ou déçoive ce que le marché attendait déjà",
        note="Schéma de principe. Une croissance de 2,5 % est solide dans l'absolu ; mais si le consensus attendait 3,0 %,\\n"
             "la nouvelle déçoit — la bonne partie était déjà dans les prix, seule la déception restait à intégrer."),
    "en": dict(
        title="The market pays for surprise, not level",
        sub="What moves a price is not whether a figure is good or bad in absolute terms,\\n"
            "but whether it beats or disappoints what the market already expected",
        note="Schematic. Growth of 2.5% is solid in absolute terms; but if the consensus expected 3.0%, the news\\n"
             "disappoints — the good part was already in the price, only the disappointment was left to absorb."),
}

def build_figure(scene: dict, lang: str) -> Figure:
    """Schéma : une droite surprise → réaction du prix, sur quatre quadrants."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)
    pl, pr, pt, pb = 110, 1637, 858, 250            # cadre du panneau (px)
    cx, cy = (pl + pr) / 2, (pt + pb) / 2           # croisement des axes
    ax.add_patch(Rectangle((pl, pb), cx - pl, pt - pb, facecolor="#241a2b", edgecolor="none", zorder=1))
    ax.add_patch(Rectangle((cx, pb), pr - cx, pt - pb, facecolor="#152238", edgecolor="none", zorder=1))
    # axes internes
    ax.annotate("", xy=(pr - 6, cy), xytext=(pl + 6, cy),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["muted"], lw=2.0), zorder=3)
    ax.annotate("", xy=(cx, pt - 30), xytext=(cx, pb + 24),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["muted"], lw=2.0), zorder=3)
    ax.text(cx + 24, pt - 34, scene["up"], ha="left", va="top", fontsize=22, color=nm.COLORS["text"])
    ax.text(cx + 24, pb + 20, scene["down"], ha="left", va="bottom", fontsize=22, color=nm.COLORS["rose"])
    # droite surprise → réaction
    x0, y0, x1, y1 = pl + 42, pb + 40, pr - 42, pt - 40
    ax.plot([x0, x1], [y0, y1], color=nm.COLORS["muted"], linewidth=4.0, zorder=2)
    ax.text(x1 - 30, y1 - 6, scene["react"], ha="right", va="bottom", fontsize=21,
            style="italic", color=nm.COLORS["muted"])
    # point : surprise −0,5 (quadrant bas-gauche)
    dx = 545
    dy = y0 + (y1 - y0) * (dx - x0) / (x1 - x0)
    ax.plot([dx, dx], [cy, dy], color=nm.COLORS["rose"], linewidth=1.8, linestyle=(0, (5, 4)), zorder=3)
    ax.plot([dx, cx], [dy, dy], color=nm.COLORS["rose"], linewidth=1.8, linestyle=(0, (5, 4)), zorder=3)
    ax.scatter([dx], [dy], s=180, color=nm.COLORS["rose"], zorder=5)
    # libellés gauche / droite
    ax.text(pl + 90, cy + 190, scene["solid"], ha="left", va="center", fontsize=21,
            style="italic", color=nm.COLORS["muted"])
    ax.text(pl + 66, cy + 78, scene["left"], ha="left", va="center", fontsize=23,
            fontweight="bold", color=nm.COLORS["rose"])
    ax.text(pr - 40, cy + 78, scene["right"], ha="right", va="center", fontsize=23,
            fontweight="bold", color=nm.COLORS["rose"])
    ax.text(dx - 6, dy - 96, scene["miss"], ha="center", va="center", fontsize=22,
            fontweight="bold", color=nm.COLORS["rose"])
    # encart bleu haut-droite
    nm.card(ax, 995, 632, 590, 150, edge=nm.COLORS["edge"], lw=2.2, radius=20)
    for i, line in enumerate(scene["callout"]):
        ax.text(1290, 730 - i * 52, line, ha="center", va="center", fontsize=25, color=nm.COLORS["text"])
    # encart rose bas-droite
    nm.card(ax, 1040, 300, 470, 190, edge=nm.COLORS["rose"], lw=2.4, radius=20)
    for i, line in enumerate(scene["box"]):
        ax.text(1275, 448 - i * 56, line, ha="center", va="center", fontsize=24,
                fontweight="bold", color=nm.COLORS["text"])
    # formule sous le panneau
    ax.text(cx, 205, scene["formula"], ha="center", va="center", fontsize=27,
            fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(surprise_scene(LANG), LANG)'''


# ── Figure 03 — les quatre régimes macroéconomiques (schéma 2×2) ─────────────

DATA_3 = '''def regime_quadrants(lang: str) -> list[dict]:
    """Les quatre régimes : position, couleurs et textes localisés.
    The four regimes: position, colors and localized texts."""
    if lang == "fr":
        data = [
            ("tl", nm.COLORS["blue"], "#16283f", "Reprise désinflationniste", "\\u00ab Goldilocks \\u00bb",
             ["Actions (surtout croissance),", "crédit, immobilier"], "ex. 2014-2019 \\u00b7 2024"),
            ("tr", "#7e6a92", "#241d31", "Surchauffe", "expansion inflationniste",
             ["Matières premières, actions", "cycliques / value, obligations indexées"], "ex. 2021"),
            ("bl", nm.COLORS["edge"], "#161f30", "Ralentissement", "récession désinflationniste",
             ["Obligations d'État (duration),", "valeurs défensives, qualité"], "ex. 2008 \\u00b7 début 2020"),
            ("br", "#9c4a5a", "#2c1922", "Stagflation", "le pire des deux mondes",
             ["Liquidités, or, énergie ;", "actions ET obligations souffrent"], "ex. 1973-1980 \\u00b7 2022"),
        ]
    else:
        data = [
            ("tl", nm.COLORS["blue"], "#16283f", "Disinflationary recovery", "\\u00ab Goldilocks \\u00bb",
             ["Equities (especially growth),", "credit, real estate"], "e.g. 2014-2019 \\u00b7 2024"),
            ("tr", "#7e6a92", "#241d31", "Overheating", "inflationary expansion",
             ["Commodities, cyclical /", "value equities, inflation-linked bonds"], "e.g. 2021"),
            ("bl", nm.COLORS["edge"], "#161f30", "Slowdown", "disinflationary recession",
             ["Government bonds (duration),", "defensive, quality stocks"], "e.g. 2008 \\u00b7 early 2020"),
            ("br", "#9c4a5a", "#2c1922", "Stagflation", "the worst of both worlds",
             ["Cash, gold, energy;", "equities AND bonds suffer"], "e.g. 1973-1980 \\u00b7 2022"),
        ]
    keys = ["pos", "edge", "fill", "name", "sub", "body", "ex"]
    return [dict(zip(keys, row)) for row in data]'''

FIG_3 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le climat, pas la météo : les quatre régimes",
        sub="Croissance qui accélère ou ralentit, inflation qui monte ou reflue — les actifs qui résistent changent",
        up="CROISSANCE QUI ACCÉLÈRE \\u25b2", down="\\u25bc CROISSANCE QUI RALENTIT",
        infl_down="INFLATION QUI REFLUE \\u25bc", infl_up="INFLATION QUI MONTE \\u25bc",
        note="Carte stylisée : des tendances historiques, pas des lois. Les actifs cités sont ceux qui résistent le mieux en moyenne dans chaque régime."),
    "en": dict(
        title="Climate, not weather: the four regimes",
        sub="Growth accelerating or slowing, inflation rising or falling — the assets that hold up change",
        up="GROWTH ACCELERATING \\u25b2", down="\\u25bc GROWTH SLOWING",
        infl_down="INFLATION FALLING \\u25bc", infl_up="INFLATION RISING \\u25bc",
        note="Stylized map: historical tendencies, not laws. The assets named are those that best resist, on average, in each regime."),
}

def build_figure(quadrants: list[dict], lang: str) -> Figure:
    """Schéma : quatre cartes croisant croissance et inflation, avec la bascule 2021→2022."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1501)
    ax = nm.blank_axes(fig)
    gl, gr, gtop, gbot = 175, 1572, 1120, 178       # emprise de la grille (px)
    cx, cy = (gl + gr) / 2, (gtop + gbot) / 2
    gap = 42
    spans = dict(
        tl=(gl, cy + gap, cx - gap, gtop),
        tr=(cx + gap, cy + gap, gr, gtop),
        bl=(gl, gbot, cx - gap, cy - gap),
        br=(cx + gap, gbot, gr, cy - gap),
    )
    for q in quadrants:
        x0, y0, x1, y1 = spans[q["pos"]]
        w, h = x1 - x0, y1 - y0
        ccx, ctop = x0 + w / 2, y1
        nm.card(ax, x0, y0, w, h, edge=q["edge"], fill=q["fill"], lw=2.6, radius=26)
        ax.text(ccx, ctop - 78, q["name"], ha="center", va="center", fontsize=32,
                fontweight="bold", color=nm.COLORS["text"])
        ax.text(ccx, ctop - 148, q["sub"], ha="center", va="center", fontsize=23,
                style="italic", color=nm.COLORS["muted"])
        for j, line in enumerate(q["body"]):
            ax.text(ccx, ctop - 250 - j * 48, line, ha="center", va="center",
                    fontsize=25, color=nm.COLORS["text"])
        ax.text(ccx, y0 + 62, q["ex"], ha="center", va="center", fontsize=22, color=nm.COLORS["muted"])
    # axes centraux
    ax.annotate("", xy=(cx, gtop + 44), xytext=(cx, gbot - 44),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["muted"], lw=2.0))
    ax.annotate("", xy=(gr + 44, cy), xytext=(gl - 44, cy),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["muted"], lw=2.0))
    ax.scatter([cx], [cy], s=120, color=nm.COLORS["muted"], zorder=6)
    ax.text(cx, gtop + 70, text["up"], ha="center", va="bottom", fontsize=22,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(cx, gbot - 70, text["down"], ha="center", va="top", fontsize=22,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(88, cy, text["infl_down"], ha="center", va="center", fontsize=21,
            fontweight="bold", color=nm.COLORS["muted"], rotation=90)
    ax.text(1662, cy, text["infl_up"], ha="center", va="center", fontsize=21,
            fontweight="bold", color=nm.COLORS["muted"], rotation=-90)
    # bascule 2021 → 2022
    ax.annotate("", xy=(1476, cy - 118), xytext=(1476, cy + 118),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=2.2, linestyle=(0, (1, 2))))
    ax.text(1516, cy + 118, "2021", ha="left", va="center", fontsize=22, fontweight="bold", color=nm.COLORS["rose"])
    ax.text(1516, cy - 118, "2022", ha="left", va="center", fontsize=22, fontweight="bold", color=nm.COLORS["rose"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(regime_quadrants(LANG), LANG)'''


# ── Figure 04 — 2022 : la diversification a disparu (barres groupées) ────────

DATA_4 = '''def diversification_bars() -> tuple[list[float], list[float]]:
    """Performances annuelles stylisées : repli classique (actions, obligations, 60/40)
    contre l'année 2022 (ordres de grandeur). / Stylized annual returns: a typical
    sell-off vs the year 2022 (rough magnitudes)."""
    classic = [-20.0, 5.0, -10.0]                   # actions, obligations, 60/40
    year_2022 = [-18.0, -13.0, -16.0]
    return classic, year_2022

classic, year_2022 = diversification_bars()'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="2022 : l'année où la diversification a disparu",
        sub="Le portefeuille 60/40 passe pour prudent parce que, d'ordinaire, les obligations montent\\n"
            "quand les actions chutent. Cette année-là, les deux ont reculé de concert.",
        ylab="Performance sur l'année",
        head_left="Repli classique \\u2014 le schéma habituel", head_right="2022 \\u2014 ce qui s'est réellement passé",
        cats=["Actions", "Obligations", "60 / 40"],
        cushion="D'ordinaire, les obligations montent\\net amortissent la baisse des actions",
        plunge="Cette fois, ce qui devait\\namortir a plongé aussi",
        note="\\u00ab Repli classique \\u00bb : illustration schématique. \\u00ab 2022 \\u00bb : ordres de grandeur (actions \\u2248 \\u221218 %,\\n"
             "obligations \\u2248 \\u221213 %, 60/40 \\u2248 \\u221216 %). Une même cause frappait les deux poches : l'inflation et les taux."),
    "en": dict(
        title="2022: the year diversification vanished",
        sub="The 60/40 portfolio passes for prudent because, ordinarily, bonds rise when\\n"
            "stocks fall. That year, both fell in concert.",
        ylab="Return over the year",
        head_left="Typical sell-off \\u2014 the usual pattern", head_right="2022 \\u2014 what actually happened",
        cats=["Stocks", "Bonds", "60 / 40"],
        cushion="Ordinarily, bonds rise and\\ncushion the fall in stocks",
        plunge="This time, what was meant\\nto cushion plunged too",
        note="\\u00ab Typical sell-off \\u00bb: schematic illustration. \\u00ab 2022 \\u00bb: rough magnitudes (stocks \\u2248 \\u221218%,\\n"
             "bonds \\u2248 \\u221213%, 60/40 \\u2248 \\u221216%). One and the same cause struck both pockets: inflation and rates."),
}

def pct(value: float, lang: str) -> str:
    """Étiquette de pourcentage signée, localisée."""
    sign = "+" if value > 0 else "\\u2212"
    body = f"{abs(value):.0f}"
    return f"{sign}{body} %" if lang == "fr" else f"{sign}{body}%"

def build_figure(classic: list[float], year_2022: list[float], lang: str) -> Figure:
    """Deux groupes de barres : repli classique (obligations amortissent) contre 2022."""
    text = LABELS[lang]
    fig = nm.figure(height_px=952)
    ax = nm.axes(fig, left=0.088, bottom=0.11)
    ax.grid(axis="x", visible=False)
    left_pos = [0, 1, 2]
    right_pos = [4, 5, 6]
    values = classic + year_2022
    positions = left_pos + right_pos
    colors = [nm.COLORS["rose"], nm.COLORS["blue"], nm.COLORS["rose"]] + [nm.COLORS["rose"]] * 3
    ax.bar(positions, values, width=0.62, color=colors, zorder=3)
    ax.axhline(0, color=nm.COLORS["text"], linewidth=1.8, alpha=0.85)
    ax.axvline(3, color=nm.COLORS["edge"], linewidth=1.8, linestyle=(0, (6, 5)))
    ax.set_ylim(-24, 15.5)
    ax.set_yticks([-20, -10, 0, 10])
    ax.set_yticklabels([pct(v, lang) for v in (-20, -10, 0, 10)])
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.7, 6.7)
    ax.set_xticks([])
    # titres de groupe
    ax.text(1, 14.2, text["head_left"], ha="center", va="bottom", fontsize=24,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(5, 14.2, text["head_right"], ha="center", va="bottom", fontsize=24,
            fontweight="bold", color=nm.COLORS["rose"])
    # étiquettes de catégorie + valeurs
    for pos, value in zip(positions, values):
        cat = text["cats"][pos % 4] if pos < 3 else text["cats"][pos - 4]
        ax.text(pos, 10.6, cat, ha="center", va="center", fontsize=20, color=nm.COLORS["muted"])
        above = value > 0
        ax.annotate(pct(value, lang), (pos, value), xytext=(0, 12 if above else -12),
                    textcoords="offset points", ha="center", va="bottom" if above else "top",
                    fontsize=27, fontweight="bold", color=nm.COLORS["text"])
    # annotations
    ax.annotate(text["cushion"], xy=(1, 4.4), xytext=(1.75, -8.5), ha="left", va="center",
                fontsize=19, style="italic", color=nm.COLORS["muted"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["blue"], lw=1.8,
                                connectionstyle="arc3,rad=-0.35"))
    ax.annotate(text["plunge"], xy=(5, -0.4), xytext=(4.4, 4.9), ha="center", va="bottom",
                fontsize=19, fontweight="bold", color=nm.COLORS["rose"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(classic, year_2022, LANG)'''


# ── Figure 05 — lire une nouvelle en trois questions (schéma) ────────────────

DATA_5 = '''def reading_questions(lang: str) -> list[tuple[str, str]]:
    """Les trois questions pour lire une nouvelle : (question, précision), localisées.
    The three questions to read a release: (question, gloss), localized."""
    if lang == "fr":
        return [
            ("Par rapport à quoi l'attendait-on ?", "l'écart au consensus fait le mouvement, pas le niveau"),
            ("Quel étage de la fraction bouge ?", "profits attendus (le haut) ou taux d'actualisation (le bas) ?"),
            ("Que change-t-elle au chemin des taux ?", "la conversation permanente entre marchés et banque centrale"),
        ]
    return [
        ("Relative to what was it expected?", "the gap to consensus makes the move, not the level"),
        ("Which floor of the fraction moves?", "expected profits (the top) or the discount rate (the bottom)?"),
        ("What does it change about the path of rates?", "the permanent conversation between markets and the central bank"),
    ]'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Lire une nouvelle, en trois questions",
        sub="Une grammaire d'interprétation — rien à prédire",
        note="Le même réflexe transforme le flot des nouvelles en texte lisible : ce qui était attendu,\\n"
             "ce que cela change aux deux étages de la fraction, et ce que la banque centrale en fera."),
    "en": dict(
        title="Reading a release, in three questions",
        sub="A grammar of interpretation — nothing to predict",
        note="The same reflex turns the stream of news into readable text: what was expected,\\n"
             "what it changes at the two floors of the fraction, and what the central bank will do about it."),
}

def build_figure(rows: list[tuple[str, str]], lang: str) -> Figure:
    """Schéma : trois cartes horizontales numérotées (question + précision)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.blank_axes(fig)
    card_x, card_w, card_h = 105, 1537, 152
    for i, (question, gloss) in enumerate(rows):
        top = 760 - i * 200
        nm.card(ax, card_x, top - card_h, card_w, card_h, edge=nm.COLORS["edge"], lw=2.2, radius=22)
        ax.text(178, top - card_h / 2, str(i + 1), ha="center", va="center",
                fontsize=44, fontweight="bold", color=nm.COLORS["blue"])
        ax.text(268, top - 52, question, ha="left", va="center", fontsize=31,
                fontweight="bold", color=nm.COLORS["text"])
        ax.text(268, top - 108, gloss, ha="left", va="center", fontsize=24, color=nm.COLORS["muted"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(reading_questions(LANG), LANG)'''


# ── Figure 06 — le behavior gap (schéma composite) ───────────────────────────

DATA_6 = '''def behavior_gap(lang: str) -> dict:
    """Textes et ordres de grandeur du schéma « behavior gap ».
    Texts and magnitudes of the « behavior gap » diagram."""
    common = dict(placement=8.0, investor=5.5)
    if lang == "fr":
        common.update(
            left_title="Acheter haut, vendre bas", right_title="Ce que cela coûte, au fil des ans",
            trend="le placement monte sur le long terme", time="le temps  \\u2192",
            buy="on achète\\n(euphorie)", sell="on vend\\n(panique)",
            r_place="\\u2248 +8 % / an", r_invest="\\u2248 +5,5 % / an",
            place_lab="Rendement\\ndu placement", invest_lab="Rendement\\nde l'investisseur",
            gap="behavior gap", gap_val="\\u2248 \\u22122,5 pts / an")
    else:
        common.update(
            left_title="Buy high, sell low", right_title="What it costs, over the years",
            trend="the investment rises over the long run", time="time  \\u2192",
            buy="buy\\n(euphoria)", sell="sell\\n(panic)",
            r_place="\\u2248 +8% / yr", r_invest="\\u2248 +5.5% / yr",
            place_lab="Investment\\nreturn", invest_lab="Investor's\\nreturn",
            gap="behavior gap", gap_val="\\u2248 \\u22122.5 pts / yr")
    return common'''

FIG_6 = '''import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

LABELS = {
    "fr": dict(
        title="Le pire ennemi de l'investisseur, c'est lui-même",
        sub="Acheter dans l'euphorie, vendre dans la panique : le \\u00ab behavior gap \\u00bb fait gagner\\n"
            "à l'épargnant moins que le placement qu'il détient pourtant",
        note="À gauche, le mécanisme ; à droite, des ordres de grandeur illustratifs. Le \\u00ab behavior gap \\u00bb sépare le\\n"
             "rendement d'un placement du rendement encaissé, creusé par des entrées et des sorties à contretemps."),
    "en": dict(
        title="The investor's worst enemy is himself",
        sub="Buying in euphoria, selling in panic: the \\u00ab behavior gap \\u00bb makes the saver earn\\n"
            "less than the very investment he nonetheless holds",
        note="On the left, the mechanism; on the right, illustrative magnitudes. The \\u00ab behavior gap \\u00bb separates the\\n"
             "return of an investment from the return actually pocketed, dug by badly-timed entries and exits."),
}

def build_figure(scene: dict, lang: str) -> Figure:
    """Schéma : à gauche le mécanisme (acheter haut / vendre bas), à droite le coût en barres."""
    text = LABELS[lang]
    fig = nm.figure(height_px=931)
    ax = nm.blank_axes(fig)
    # ── panneau gauche : la courbe du placement ──
    ax.text(130, 648, scene["left_title"], ha="left", va="center", fontsize=27,
            fontweight="bold", color=nm.COLORS["text"])
    x = np.linspace(150, 940, 240)
    u = (x - 150) / 790
    trend = 360 + u * 150
    y = trend + 42 * np.sin(u * 3.2 * np.pi + 0.5)
    ax.plot([120, 965], [300, 300], color=nm.COLORS["muted"], linewidth=1.6)
    ax.annotate("", xy=(975, 300), xytext=(955, 300),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=1.6))
    ax.fill_between(x, y, 300, color=nm.COLORS["blue"], alpha=0.16, zorder=1)
    ax.plot(x, trend, color=nm.COLORS["muted"], linewidth=2.0, linestyle=(0, (6, 5)), zorder=2)
    ax.plot(x, y, color=nm.COLORS["blue"], linewidth=3.0, zorder=3)
    ax.text(150, 328, scene["time"], ha="left", va="center", fontsize=21, color=nm.COLORS["muted"])
    ax.text(430, 505, scene["trend"], ha="center", va="center", fontsize=20,
            color=nm.COLORS["muted"], rotation=11)
    # vente (creux) et achat (sommet)
    xs = 430.0
    ys = 360 + (xs - 150) / 790 * 150 + 42 * np.sin((xs - 150) / 790 * 3.2 * np.pi + 0.5)
    ax.scatter([xs], [ys], marker="v", s=260, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(scene["sell"], xy=(xs, ys), xytext=(xs, 210), ha="center", va="center",
                fontsize=21, fontweight="bold", color=nm.COLORS["text"], linespacing=1.4,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    xb = 690.0
    yb = 360 + (xb - 150) / 790 * 150 + 42 * np.sin((xb - 150) / 790 * 3.2 * np.pi + 0.5)
    ax.scatter([xb], [yb], s=200, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(scene["buy"], xy=(xb, yb), xytext=(xb, 720), ha="center", va="center",
                fontsize=21, fontweight="bold", color=nm.COLORS["rose"], linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    # ── panneau droit : le coût en barres ──
    ax.text(1075, 648, scene["right_title"], ha="left", va="center", fontsize=27,
            fontweight="bold", color=nm.COLORS["text"])
    base, scale = 300, 30.0
    b1x, b2x, bw = 1180, 1440, 120
    h1 = scene["placement"] * scale
    h2 = scene["investor"] * scale
    ax.add_patch(Rectangle((b1x, base), bw, h1, facecolor=nm.COLORS["blue"], edgecolor="none", zorder=3))
    ax.add_patch(Rectangle((b2x, base), bw, h2, facecolor="#5f7699", edgecolor="none", zorder=3))
    ax.text(b1x + bw / 2, base + h1 + 26, scene["r_place"], ha="center", va="bottom",
            fontsize=25, fontweight="bold", color=nm.COLORS["text"])
    ax.text(b2x + bw / 2, base + h2 + 26, scene["r_invest"], ha="center", va="bottom",
            fontsize=25, fontweight="bold", color=nm.COLORS["text"])
    ax.text(b1x + bw / 2, 262, scene["place_lab"], ha="center", va="top", fontsize=21,
            color=nm.COLORS["muted"], linespacing=1.4)
    ax.text(b2x + bw / 2, 262, scene["invest_lab"], ha="center", va="top", fontsize=21,
            color=nm.COLORS["muted"], linespacing=1.4)
    # crochet du gap
    gy1, gy2 = base + h1, base + h2
    gx = b2x + bw + 40
    ax.plot([b1x + bw / 2, gx + 18], [gy1, gy1], color=nm.COLORS["rose"], linewidth=1.6, linestyle=(0, (4, 3)))
    ax.plot([b2x + bw / 2, gx + 18], [gy2, gy2], color=nm.COLORS["rose"], linewidth=1.6, linestyle=(0, (4, 3)))
    ax.annotate("", xy=(gx, gy1), xytext=(gx, gy2),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["rose"], lw=2.0))
    ax.text(b2x + bw / 2, gy1 + 64, scene["gap"], ha="center", va="center",
            fontsize=22, fontweight="bold", color=nm.COLORS["rose"])
    ax.text(b2x + bw / 2, gy1 + 30, scene["gap_val"], ha="center", va="center",
            fontsize=21, color=nm.COLORS["rose"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(behavior_gap(LANG), LANG)'''


# ── Figure 07 — l'efficience ne compose pas votre repas (schéma) ─────────────

DATA_7 = '''def efficiency_scene(lang: str) -> dict:
    """Textes localisés du schéma « le marché fixe les prix, pas votre portefeuille ».
    Localized texts of the « market sets prices, not your portfolio » diagram."""
    if lang == "fr":
        return dict(
            card_title="Ce que dit l'efficience : le prix du menu est juste",
            card_lines=["chaque actif est valorisé pour son risque \\u2014 pas de repas gratuit, pas de marché battu",
                        "avec un savoir que tout le monde partage"],
            mid="\\u2026 mais il ne compose pas votre repas :",
            cards=[["Protection contre", "l'inflation ?"], ["Obligations longues", "ou courtes ?"],
                   ["Actions ou", "liquidités ?"], ["Diversifier entre", "quels régimes ?"]],
            below="le trentenaire et le retraité font face au même marché efficient \\u2014 et ne doivent pas détenir le même portefeuille")
    return dict(
        card_title="What efficiency says: the menu price is fair",
        card_lines=["each asset is priced for its risk \\u2014 no free lunch, no beating the market",
                    "with knowledge that everyone shares"],
        mid="\\u2026 but it does not compose your meal:",
        cards=[["Protection against", "inflation?"], ["Long bonds", "or short?"],
               ["Equities or", "cash?"], ["Diversify across", "which regimes?"]],
        below="the thirty-year-old and the retiree face the same efficient market \\u2014 and should not hold the same portfolio")'''

FIG_7 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le marché fixe les prix, pas votre portefeuille",
        sub="Même parfaitement efficient, il vous laisse toutes les décisions qui comptent",
        note="L'efficience répond à \\u00ab puis-je battre le marché ? \\u00bb ; elle ne répond pas à\\n"
             "\\u00ab quel portefeuille me convient ? \\u00bb. Ces deux questions n'ont jamais été la même."),
    "en": dict(
        title="The market sets prices, not your portfolio",
        sub="Even perfectly efficient, it leaves you every decision that matters",
        note="Efficiency answers \\u00ab can I beat the market? \\u00bb; it does not answer\\n"
             "\\u00ab which portfolio suits me? \\u00bb. These two questions were never the same."),
}

def build_figure(scene: dict, lang: str) -> Figure:
    """Schéma : l'encart bleu de l'efficience, puis quatre décisions qui restent vôtres."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)
    # grande carte du haut
    nm.card(ax, 105, 762, 1537, 166, edge=nm.COLORS["blue"], lw=2.6, radius=24)
    ax.text(150, 898, scene["card_title"], ha="left", va="center", fontsize=29,
            fontweight="bold", color=nm.COLORS["text"])
    for i, line in enumerate(scene["card_lines"]):
        ax.text(150, 846 - i * 44, line, ha="left", va="center", fontsize=23, color=nm.COLORS["muted"])
    # phrase pivot
    ax.text(nm.WIDTH_PX / 2, 690, scene["mid"], ha="center", va="center", fontsize=29,
            fontweight="bold", color=nm.COLORS["text"])
    # quatre petites cartes
    card_w, gap, x0 = 348, 48, 105
    top, bottom = 590, 430
    for i, lines in enumerate(scene["cards"]):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS["rose"], lw=2.4, radius=20)
        for j, line in enumerate(lines):
            ax.text(cx, 528 - j * 46, line, ha="center", va="center", fontsize=25, color=nm.COLORS["text"])
    # phrase sous les cartes
    ax.text(nm.WIDTH_PX / 2, 320, scene["below"], ha="center", va="center", fontsize=23, color=nm.COLORS["muted"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(efficiency_scene(LANG), LANG)'''


# ── Figure 08 — se préparer plutôt que prévoir (schéma à deux panneaux) ──────

DATA_8 = '''def prepare_scene(lang: str) -> dict:
    """Textes localisés du schéma « se préparer plutôt que prévoir ».
    Localized texts of the « prepare rather than predict » diagram."""
    if lang == "fr":
        return dict(
            predict="Prédire", prepare="Se préparer",
            today="aujourd'hui", one=["un seul", "scénario"],
            judged=["jugé sur la venue", "d'un seul monde"],
            center=["votre", "portefeuille"], bearable="tenable ?",
            regimes=["Goldilocks", "Surchauffe", "Ralentissement", "Stagflation"])
    return dict(
        predict="Predict", prepare="Prepare",
        today="today", one=["a single", "scenario"],
        judged=["judged on one", "world showing up"],
        center=["your", "portfolio"], bearable="bearable?",
        regimes=["Goldilocks", "Overheating", "Slowdown", "Stagflation"])'''

FIG_8 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Se préparer plutôt que prévoir",
        sub="Cartographier les mondes plausibles au lieu d'en parier un seul",
        note="La bonne question n'est plus \\u00ab que va-t-il se passer ? \\u00bb mais \\u00ab si le régime X survient,\\n"
             "suis-je ruiné ou seulement mal à l'aise ? \\u00bb \\u2014 un raisonnement par scénarios."),
    "en": dict(
        title="Prepare rather than predict",
        sub="Map the plausible worlds instead of betting on a single one",
        note="The right question is no longer \\u00ab what will happen? \\u00bb but \\u00ab if regime X arrives,\\n"
             "am I ruined or merely uncomfortable? \\u00bb \\u2014 reasoning by scenarios."),
}

def build_figure(scene: dict, lang: str) -> Figure:
    """Schéma : à gauche « Prédire » (un seul scénario), à droite « Se préparer » (quatre régimes)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.blank_axes(fig)
    # panneau gauche « Prédire »
    nm.card(ax, 95, 150, 560, 670, edge=nm.COLORS["edge"], fill="#141f31", lw=2.4, radius=28)
    ax.text(375, 762, scene["predict"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["rose"])
    ax.scatter([215], [452], s=150, color=nm.COLORS["text"], zorder=5)
    ax.text(215, 402, scene["today"], ha="center", va="center", fontsize=23, color=nm.COLORS["text"])
    nm.card(ax, 388, 508, 224, 128, edge=nm.COLORS["rose"], lw=2.4, radius=18)
    for j, line in enumerate(scene["one"]):
        ax.text(500, 596 - j * 48, line, ha="center", va="center", fontsize=24, color=nm.COLORS["text"])
    ax.annotate("", xy=(392, 556), xytext=(238, 468),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=4.0))
    for j, line in enumerate(scene["judged"]):
        ax.text(375, 300 - j * 42, line, ha="center", va="center", fontsize=22,
                style="italic", color=nm.COLORS["muted"])
    # panneau droit « Se préparer »
    nm.card(ax, 720, 150, 935, 670, edge=nm.COLORS["edge"], fill="#141f31", lw=2.4, radius=28)
    ax.text(1187, 762, scene["prepare"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["blue"])
    ccx, ccy = 1187, 470
    nm.card(ax, ccx - 128, ccy - 52, 256, 104, edge=nm.COLORS["blue"], lw=2.6, radius=18)
    for j, line in enumerate(scene["center"]):
        ax.text(ccx, ccy + 22 - j * 44, line, ha="center", va="center", fontsize=24,
                fontweight="bold", color=nm.COLORS["text"])
    corners = [(900, 640), (1474, 640), (900, 300), (1474, 300)]
    for (rx, ry), name in zip(corners, scene["regimes"]):
        nm.card(ax, rx - 145, ry - 52, 290, 104, edge=nm.COLORS["edge"], lw=2.2, radius=16)
        ax.text(rx, ry + 16, name, ha="center", va="center", fontsize=24, fontweight="bold", color=nm.COLORS["text"])
        ax.text(rx, ry - 26, scene["bearable"], ha="center", va="center", fontsize=20, color=nm.COLORS["muted"])
        ex = rx + (95 if rx < ccx else -95)
        ey = ry + (-42 if ry > ccy else 42)
        cx_edge = ccx + (-118 if rx < ccx else 118)
        cy_edge = ccy + (42 if ry > ccy else -42)
        ax.annotate("", xy=(ex, ey), xytext=(cx_edge, cy_edge),
                    arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=2.2))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(prepare_scene(LANG), LANG)'''


# ── Assemblage ───────────────────────────────────────────────────────────────

FIGURES = [
    dict(name="fig01-deux-epargnants", fig_fr="Quinze ans, deux épargnants",
         fig_en="Fifteen years, two savers", live=False, data=DATA_1, fig=FIG_1),
    dict(name="fig02-surprise-vs-niveau", fig_fr="Le marché paie la surprise, pas le niveau",
         fig_en="The market pays for surprise, not level", live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-regimes-macro", fig_fr="Le climat, pas la météo : les quatre grands régimes macroéconomiques",
         fig_en="Climate, not weather: the four great macroeconomic regimes", live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-diversification-2022", fig_fr="2022 : l'année où la diversification a disparu",
         fig_en="2022: the year diversification vanished", live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-lire-une-nouvelle", fig_fr="Lire une nouvelle, en trois questions",
         fig_en="Reading a release, in three questions", live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-behavior-gap", fig_fr="Le pire ennemi de l'investisseur, c'est lui-même",
         fig_en="The investor's worst enemy is himself", live=False, data=DATA_6, fig=FIG_6),
    dict(name="fig07-efficience-menu", fig_fr="Le marché fixe les prix, pas votre portefeuille",
         fig_en="The market sets prices, not your portfolio", live=False, data=DATA_7, fig=FIG_7),
    dict(name="fig08-se-preparer-scenarios", fig_fr="Se préparer plutôt que prévoir",
         fig_en="Prepare rather than predict", live=False, data=DATA_8, fig=FIG_8),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out2")
    nb_kit.build_all(META, DIR, FIGURES)
