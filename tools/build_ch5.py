#!/usr/bin/env python3
"""Notebooks du chapitre 5 — « Le vocabulaire essentiel de la macroéconomie financière ».

Douze figures reproductibles. Onze sont des schémas conceptuels éditables (cartes,
frises, courbes stylisées, barres illustratives) et une seule charge une série FRED en
direct (fig03, IPC/inflation via CPIAUCSL). Chaque notebook = une seule cellule code
(load_*() puis build_figure(...) -> Figure), style NMLab partagé.
"""

import sys

sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit


# ═════════════════════════════════════════════════════════════════════════════
# Figure 01 — trois lignes, sept mots de passe (mur de jargon)
# ═════════════════════════════════════════════════════════════════════════════

DATA_1 = '''def jargon(lang: str) -> tuple[str, list[str]]:
    """La citation d'ouverture et les sept mots de passe à déplier, localisés.
    The opening quote and the seven passwords to unfold, localized."""
    if lang == "fr":
        quote = ("« La Fed a opté pour le statu quo, mais un communiqué jugé hawkish\\n"
                 "a aplati la courbe ; les marchés, qui avaient déjà intégré le pivot,\\n"
                 "relèvent leurs anticipations de taux terminal, et le consensus\\n"
                 "table désormais sur un atterrissage en douceur. »")
        words = ["statu quo ?", "hawkish ?", "courbe aplatie ?", "intégré (priced in) ?",
                 "pivot ?", "taux terminal ?", "atterrissage en douceur ?"]
        return quote, words
    quote = ("« The Fed opted for a hold, but a statement judged hawkish\\n"
             "flattened the curve; the markets, which had already priced in the pivot,\\n"
             "raise their terminal-rate expectations, and the consensus\\n"
             "now bets on a soft landing. »")
    words = ["a hold?", "hawkish?", "flattened curve?", "priced in?",
             "pivot?", "terminal rate?", "soft landing?"]
    return quote, words

quote, words = jargon(LANG)'''

FIG_1 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Trois lignes, sept mots de passe",
               sub="La dépêche d'un soir de réunion de la Fed",
               note="Chaque mot semble français, et la phrase glisse sans laisser prise. À la fin du chapitre,\\n"
                    "elle sera transparente — il n'y a pas de mur, seulement des mécanismes pliés dans des mots."),
    "en": dict(title="Three lines, seven passwords",
               sub="The dispatch of a Fed-meeting evening",
               note="Every word looks like English, and the sentence slips by without a grip. By the end of the chapter\\n"
                    "it will be transparent — there is no wall, only mechanisms folded into words."),
}

def draw_row(ax, words_row, cy, h):
    """Une rangée de mots-cartes (liseré rose), centrée, largeur ajustée au texte."""
    widths = [max(240, 20 * len(w) + 70) for w in words_row]
    gap = 44
    x = (1747 - (sum(widths) + gap * (len(widths) - 1))) / 2
    for w, word in zip(widths, words_row):
        nm.card(ax, x, cy - h / 2, w, h, edge=nm.COLORS["rose"], lw=2.4, radius=16)
        ax.text(x + w / 2, cy, word, ha="center", va="center", fontsize=23,
                fontweight="bold", color=nm.COLORS["text"])
        x += w + gap

def build_figure(quote: str, words: list[str], lang: str) -> Figure:
    """Carte-citation en haut, puis les sept mots de passe en deux rangées."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    nm.card(ax, 100, 560, 1547, 305, edge=nm.COLORS["muted"], lw=2.2, radius=22)
    ax.text(873, 712, quote, ha="center", va="center", fontsize=27, fontstyle="italic",
            color=nm.COLORS["text"], linespacing=1.75)

    draw_row(ax, words[:4], 424, 92)
    draw_row(ax, words[4:], 306, 92)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(quote, words, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 02 — un mot = un mécanisme plié
# ═════════════════════════════════════════════════════════════════════════════

DATA_2 = '''def mechanism(lang: str) -> tuple[str, str, str, list[str]]:
    """Le mot compressé, sa mesure, l'intitulé du mécanisme et ses trois temps, localisés.
    The compressed word, its measure, the mechanism title and its three steps, localized."""
    if lang == "fr":
        return ("« Inversion\\nde la courbe »", "le mot : quatre syllabes", "le mécanisme",
                ["les taux courts dépassent les taux longs…",
                 "…parce que le marché anticipe des baisses…",
                 "…parce qu'il redoute un ralentissement"])
    return ("« Curve\\ninversion »", "the word : two words", "the mechanism",
            ["short rates rise above long rates…",
             "…because the market expects cuts…",
             "…because it fears a slowdown"])

word, syllables, head, steps = mechanism(LANG)'''

FIG_2 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Un mot = un mécanisme plié",
               sub="Le savoir n'est pas dans le vocabulaire, il est dans le mécanisme",
               unfold="déplier",
               note="Ne demandez pas ce que le mot veut dire — demandez ce qu'il compresse : qui achète,\\n"
                    "qui vend, ce qui monte, ce qui baisse, quel étage de la fraction bouge."),
    "en": dict(title="One word = one folded mechanism",
               sub="The knowledge is not in the vocabulary, it is in the mechanism",
               unfold="unfold",
               note="Don't ask what the word means — ask what it compresses: who buys,\\n"
                    "who sells, what rises, what falls, which floor of the fraction moves."),
}

def build_figure(word: str, syllables: str, head: str, steps: list[str], lang: str) -> Figure:
    """Carte-mot (rose) → flèche « déplier » → carte-mécanisme (bleu) en trois temps."""
    text = LABELS[lang]
    fig = nm.figure(height_px=988)
    ax = nm.blank_axes(fig)

    nm.card(ax, 100, 430, 470, 210, edge=nm.COLORS["rose"], lw=2.6, radius=18)
    ax.text(335, 535, word, ha="center", va="center", fontsize=30, fontweight="bold",
            color=nm.COLORS["text"], linespacing=1.35)
    ax.text(335, 388, syllables, ha="center", va="center", fontsize=22,
            fontstyle="italic", color=nm.COLORS["muted"])

    ax.annotate("", xy=(775, 535), xytext=(600, 535),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["text"], lw=2.6))
    ax.text(688, 582, text["unfold"], ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])

    nm.card(ax, 805, 250, 842, 500, edge=nm.COLORS["blue"], lw=2.6, radius=18)
    ax.text(850, 688, head, ha="left", va="center", fontsize=30, fontweight="bold", color=nm.COLORS["text"])
    for j, step in enumerate(steps):
        ax.text(850, 578 - j * 100, step, ha="left", va="center", fontsize=24, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(word, syllables, head, steps, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 03 — le niveau contre la variation (IPC, FRED en direct)
# ═════════════════════════════════════════════════════════════════════════════

DATA_3 = '''from pandas import Series

def load_prices() -> tuple[Series, Series]:
    """Indice des prix (CPIAUCSL) depuis 2018 et son glissement annuel — l'inflation — depuis 2019.
    Live from FRED: CPI level since 2018 and its year-over-year change (inflation) since 2019."""
    cpi = nm.load_fred("CPIAUCSL").loc["2018":]
    inflation = ((cpi / cpi.shift(12) - 1) * 100).loc["2019":]
    return cpi, inflation

cpi, inflation = load_prices()
print(f"Dernier point / latest: {inflation.index[-1]:%Y-%m} → {inflation.iloc[-1]:.1f} %")'''

FIG_3 = '''import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="« L'inflation ralentit » ne veut pas dire « les prix baissent »",
        sub="États-Unis, 2018-2025 — le même indice des prix, lu de deux façons",
        lvl="Le niveau : l'indice des prix (IPC)", chg="La variation : l'inflation sur un an",
        lvl_ann="les prix continuent\\nde monter…", chg_ann="…pendant que\\nl'inflation retombe :\\nla désinflation",
        peak="pic : ≈ 9 %", target="cible : 2 %",
        note="Source : Bureau of Labor Statistics, via FRED (série CPIAUCSL). Zone grisée : la désinflation de 2022-2025 —\\n"
             "la courbe de droite descend, celle de gauche monte toujours."),
    "en": dict(
        title="« Inflation is slowing » does not mean « prices are falling »",
        sub="United States, 2018-2025 — the same price index, read two ways",
        lvl="The level: the price index (CPI)", chg="The change: inflation year over year",
        lvl_ann="prices keep\\nrising…", chg_ann="…while inflation\\nfalls back:\\ndisinflation",
        peak="peak: ≈ 9%", target="target: 2%",
        note="Source: Bureau of Labor Statistics, via FRED (CPIAUCSL series). Shaded zone: the 2022-2025 disinflation —\\n"
             "the right curve falls, the left one still rises."),
}

def build_figure(cpi: Series, inflation: Series, lang: str) -> Figure:
    """Deux panneaux : le niveau de l'IPC (gauche) et sa variation annuelle (droite)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=874)
    left = fig.add_axes([0.058, 0.165, 0.395, 0.515])
    right = fig.add_axes([0.567, 0.165, 0.415, 0.515])
    band0 = pd.Timestamp("2022-07-01")

    left.axvspan(band0, cpi.index[-1], color=nm.COLORS["edge"], alpha=0.4, linewidth=0)
    left.plot(cpi.index, cpi, color=nm.COLORS["blue"], linewidth=3)
    left.set_ylim(240, 340)
    left.set_yticks(range(240, 341, 20))
    left.set_title(text["lvl"], loc="left", color=nm.COLORS["text"], fontsize=23, fontweight="bold", pad=12)
    left.text(0.62, 0.26, text["lvl_ann"], transform=left.transAxes, fontsize=21,
              fontweight="bold", color=nm.COLORS["blue"], linespacing=1.4)

    right.axvspan(band0, inflation.index[-1], color=nm.COLORS["edge"], alpha=0.4, linewidth=0)
    right.axhline(2, color=nm.COLORS["muted"], linestyle=(0, (6, 4)), linewidth=2, alpha=0.9)
    right.plot(inflation.index, inflation, color=nm.COLORS["rose"], linewidth=3)
    peak = inflation.idxmax()
    right.scatter([peak], [inflation.max()], s=70, color=nm.COLORS["rose"], zorder=5)
    right.set_ylim(0, 10.5)
    right.set_yticks(range(0, 11, 2))
    right.set_yticklabels([f"{v} %" for v in range(0, 11, 2)])
    right.set_title(text["chg"], loc="left", color=nm.COLORS["text"], fontsize=23, fontweight="bold", pad=12)
    right.annotate(text["peak"], xy=(peak, inflation.max()), xytext=(14, 2),
                   textcoords="offset points", ha="left", va="center", fontsize=20, color=nm.COLORS["text"])
    right.text(0.635, 0.72, text["chg_ann"], transform=right.transAxes, va="top", fontsize=21,
               fontweight="bold", color=nm.COLORS["rose"], linespacing=1.45)
    right.text(0.975, 0.15, text["target"], transform=right.transAxes, ha="right", va="center",
               fontsize=20, color=nm.COLORS["muted"])

    for ax, series in ((left, cpi), (right, inflation)):
        ax.set_xlim(series.index[0], series.index[-1])
        ax.margins(x=0.01)
        ax.xaxis.set_major_locator(mdates.YearLocator(2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(cpi, inflation, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 04 — le nominal affiche, le réel décide
# ═════════════════════════════════════════════════════════════════════════════

DATA_4 = '''def project(years: int = 25, rate: float = 0.03) -> dict:
    """10 000 € placés à 3 %/an : valeur nominale et pouvoir d'achat à 2 % et 5 % d'inflation.
    €10,000 at 3%/yr: nominal value and purchasing power at 2% and 5% inflation."""
    t = list(range(years + 1))
    nominal = [10_000 * (1 + rate) ** k for k in t]
    real2 = [10_000 * ((1 + rate) / 1.02) ** k for k in t]
    real5 = [10_000 * ((1 + rate) / 1.05) ** k for k in t]
    return dict(t=t, nominal=nominal, real2=real2, real5=real5)

series = project()'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le nominal affiche, le réel décide",
        sub="10 000 € placés à 3 % par an pendant 25 ans — valeur affichée et pouvoir d'achat",
        nominal="≈ 20 900 €\\nvaleur nominale\\n(le relevé bancaire)",
        real2="≈ 12 800 €\\npouvoir d'achat\\nsi inflation à 2 %",
        real5="≈ 6 200 €\\npouvoir d'achat\\nsi inflation à 5 %",
        start="capital de départ : 10 000 €",
        xticklabels=["0", "5", "10", "15", "20", "25 ans"],
        yticklabels=["5 000 €", "10 000 €", "15 000 €", "20 000 €"],
        note="Illustration (chiffres exacts : 20 938 €, 12 762 €, 6 183 €). Pouvoir d'achat = valeur nominale corrigée\\n"
             "d'une inflation constante — approximation de Fisher : taux réel ≈ taux nominal − inflation."),
    "en": dict(
        title="The nominal shows, the real decides",
        sub="€10,000 invested at 3% a year for 25 years — displayed value and purchasing power",
        nominal="≈ €20,900\\nnominal value\\n(the bank statement)",
        real2="≈ €12,800\\npurchasing power\\nif inflation at 2%",
        real5="≈ €6,200\\npurchasing power\\nif inflation at 5%",
        start="starting capital: €10,000",
        xticklabels=["0", "5", "10", "15", "20", "25 yrs"],
        yticklabels=["€5,000", "€10,000", "€15,000", "€20,000"],
        note="Illustration (exact figures: €20,938, €12,762, €6,183). Purchasing power = nominal value adjusted\\n"
             "for constant inflation — Fisher approximation: real rate ≈ nominal rate − inflation."),
}

def build_figure(series: dict, lang: str) -> Figure:
    """Trois trajectoires : valeur nominale (bleu), pouvoir d'achat à 2 % (pointillé) et à 5 % (rose)."""
    text = LABELS[lang]
    t = series["t"]
    fig = nm.figure(height_px=806)
    ax = nm.axes(fig, left=0.075, right=0.985)
    ax.grid(axis="x", visible=False)
    ax.plot(t, series["nominal"], color=nm.COLORS["blue"], linewidth=3.4)
    ax.plot(t, series["real2"], color=nm.COLORS["muted"], linewidth=3.0, linestyle=(0, (7, 5)))
    ax.plot(t, series["real5"], color=nm.COLORS["rose"], linewidth=3.4)
    ax.axhline(10_000, color=nm.COLORS["muted"], linewidth=1.4, alpha=0.6)
    ax.set_xlim(0, 38)
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.set_xticklabels(text["xticklabels"])
    ax.set_ylim(4500, 22500)
    ax.set_yticks([5000, 10000, 15000, 20000])
    ax.set_yticklabels(text["yticklabels"])
    ax.text(25.8, series["nominal"][-1], text["nominal"], va="center", fontsize=21,
            fontweight="bold", color=nm.COLORS["blue"], linespacing=1.15)
    ax.text(25.8, series["real2"][-1], text["real2"], va="center", fontsize=21,
            color=nm.COLORS["muted"], linespacing=1.15)
    ax.text(25.8, series["real5"][-1], text["real5"], va="center", fontsize=21,
            fontweight="bold", color=nm.COLORS["rose"], linespacing=1.15)
    ax.text(25.8, 9350, text["start"], va="center", fontsize=20, color=nm.COLORS["muted"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(series, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 05 — le déficit baisse, la dette monte quand même (stock vs flux)
# ═════════════════════════════════════════════════════════════════════════════

DATA_5 = '''def load_country() -> dict:
    """Pays imaginaire : déficit annuel (flux, en baisse) et dette accumulée (stock, 1 000 → 1 910).
    Imaginary country: annual deficit (flow, falling) and accumulated debt (stock)."""
    years = list(range(1, 13))
    deficit = [120, 115, 105, 95, 85, 75, 65, 60, 55, 50, 45, 40]
    debt, running = [], 1000
    for d in deficit:
        running += d
        debt.append(running)
    return dict(years=years, deficit=deficit, debt=debt)

country = load_country()'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le déficit baisse, la dette monte quand même",
        sub="Pays imaginaire — chaque déficit annuel (flux) vient s'ajouter à la dette (stock)",
        yl="déficit annuel — le FLUX (milliards)", yr="dette accumulée — le STOCK (milliards)",
        xword="an", ann_stock="le stock monte toujours :\\n1 000 → 1 910",
        ann_flow="le flux se tarit :\\ndéficit divisé par 3",
        note="Chiffres fictifs. Tant que le flux est un déficit, le stock grossit : la dette ne se stabilise qu'au retour à\\n"
             "l'équilibre, et ne recule qu'en excédent (ou si le PIB croît plus vite qu'elle)."),
    "en": dict(
        title="The deficit falls, the debt rises anyway",
        sub="Imaginary country — each annual deficit (flow) adds to the debt (stock)",
        yl="annual deficit — the FLOW (billions)", yr="accumulated debt — the STOCK (billions)",
        xword="yr", ann_stock="the stock keeps rising:\\n1,000 → 1,910",
        ann_flow="the flow dries up:\\ndeficit divided by 3",
        note="Fictional figures. As long as the flow is a deficit, the stock grows: the debt stabilizes only when the budget\\n"
             "balances, and falls only in surplus (or when GDP grows faster than it)."),
}

def build_figure(country: dict, lang: str) -> Figure:
    """Barres de déficit (axe rose, gauche) et courbe de dette cumulée (axe bleu, droite)."""
    text = LABELS[lang]
    years, deficit, debt = country["years"], country["deficit"], country["debt"]
    fig = nm.figure(height_px=896)
    ax = nm.axes(fig, left=0.09, right=0.91, bottom=0.185)
    ax.grid(axis="x", visible=False)
    ax.bar(years, deficit, width=0.62, color=nm.COLORS["rose"], zorder=3)
    ax.set_ylim(0, 150)
    ax.set_yticks(range(0, 151, 30))
    ax.set_ylabel(text["yl"], color=nm.COLORS["rose"])
    ax.tick_params(axis="y", colors=nm.COLORS["rose"])
    ax.spines["left"].set_color(nm.COLORS["rose"])
    ax.set_xlim(0.3, 12.7)
    ax.set_xticks(years)
    ax.set_xticklabels([f"{text['xword']} {i}" for i in years], fontsize=19)

    ax2 = ax.twinx()
    ax2.plot(years, debt, color=nm.COLORS["blue"], linewidth=3, marker="o", markersize=8, zorder=4)
    ax2.set_ylim(904, 2151)
    ax2.set_yticks([1000, 1300, 1600, 1900])
    ax2.set_ylabel(text["yr"], color=nm.COLORS["blue"], labelpad=30)
    ax2.tick_params(axis="y", colors=nm.COLORS["blue"])
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(nm.COLORS["blue"])
    ax2.spines["top"].set_visible(False)
    ax2.grid(False)

    ax.text(0.42, 0.90, text["ann_stock"], transform=ax.transAxes, ha="center", va="center",
            fontsize=23, fontweight="bold", color=nm.COLORS["blue"], linespacing=1.4)
    ax.text(0.65, 0.53, text["ann_flow"], transform=ax.transAxes, ha="center", va="center",
            fontsize=23, fontweight="bold", color=nm.COLORS["rose"], linespacing=1.4)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(country, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 06 — les mots du cycle (courbe stylisée)
# ═════════════════════════════════════════════════════════════════════════════

DATA_6 = '''def cycle_curve() -> dict:
    """Ancrages de la courbe stylisée du cycle (unités arbitraires) et des deux atterrissages.
    Anchors of the stylized cycle curve and the two landing branches."""
    return dict(
        main_x=[0.0, 1.6, 3.2, 5.8], main_y=[0.30, 0.56, 0.18, 0.62],
        soft_x=[5.8, 7.2, 9.0], soft_y=[0.62, 0.60, 0.55],
        hard_x=[5.8, 6.7, 7.6, 8.6], hard_y=[0.62, 0.55, 0.34, 0.17],
        band=[2.3, 3.95])

curve = cycle_curve()'''

FIG_6 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Les mots du cycle",
        sub="Expansion, pic, contraction, creux — et les deux atterrissages",
        expansion="expansion", pic="pic", contraction="contraction", creux="creux",
        reprise="reprise", surchauffe="surchauffe", recession="récession",
        soft="atterrissage en douceur", hard="atterrissage brutal", ylab="activité",
        note="Récession « technique » : deux trimestres consécutifs de recul ; le NBER exige un recul significatif,\\n"
             "diffusé, durable — en 2022, les deux verdicts ont divergé. Stagflation : stagnation + inflation."),
    "en": dict(
        title="The words of the cycle",
        sub="Expansion, peak, contraction, trough — and the two landings",
        expansion="expansion", pic="peak", contraction="contraction", creux="trough",
        reprise="recovery", surchauffe="overheating", recession="recession",
        soft="soft landing", hard="hard landing", ylab="activity",
        note="« Technical » recession: two consecutive quarters of decline; the NBER requires a significant, diffuse,\\n"
             "lasting decline — in 2022 the two verdicts diverged. Stagflation: stagnation + inflation."),
}

def smooth(xa: list, ya: list, n: int = 400) -> tuple:
    """Interpolation cosinus entre ancrages : courbe lisse à dérivée nulle aux sommets."""
    xa, ya = np.asarray(xa, float), np.asarray(ya, float)
    xs = np.linspace(xa[0], xa[-1], n)
    ys = np.empty_like(xs)
    for i in range(len(xa) - 1):
        m = (xs >= xa[i]) & (xs <= xa[i + 1])
        t = (xs[m] - xa[i]) / (xa[i + 1] - xa[i])
        ys[m] = ya[i] + (ya[i + 1] - ya[i]) * (0.5 - 0.5 * np.cos(np.pi * t))
    return xs, ys

def build_figure(curve: dict, lang: str) -> Figure:
    """Une onde (expansion→creux→surchauffe) qui se scinde en deux atterrissages en pointillés."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.axes(fig, left=0.05, right=0.975)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel(text["ylab"])

    mx, my = smooth(curve["main_x"], curve["main_y"])
    ax.plot(mx, my, color=nm.COLORS["blue"], linewidth=5, solid_capstyle="round")
    sx, sy = smooth(curve["soft_x"], curve["soft_y"])
    ax.plot(sx, sy, color=nm.COLORS["blue"], linewidth=4.5, linestyle=(0, (6, 5)))
    hx, hy = smooth(curve["hard_x"], curve["hard_y"])
    ax.plot(hx, hy, color=nm.COLORS["rose"], linewidth=4.5, linestyle=(0, (6, 5)))

    ax.axvspan(curve["band"][0], curve["band"][1], color=nm.COLORS["edge"], alpha=0.5, linewidth=0)
    ax.set_xlim(-0.35, 9.6)
    ax.set_ylim(0, 0.9)

    white = nm.COLORS["text"]
    ax.text(0.8, 0.40, text["expansion"], ha="center", fontsize=27, color=white)
    ax.text(1.55, 0.655, text["pic"], ha="center", fontsize=27, color=white)
    ax.text(2.72, 0.335, text["contraction"], ha="center", fontsize=27, color=white)
    ax.text(3.2, 0.075, text["creux"], ha="center", fontsize=27, color=white)
    ax.text(4.55, 0.40, text["reprise"], ha="center", fontsize=27, color=white)
    ax.text(5.4, 0.72, text["surchauffe"], ha="center", fontsize=27, color=white)
    ax.text(3.12, 0.03, text["recession"], ha="center", va="bottom", fontsize=22,
            fontstyle="italic", color=nm.COLORS["muted"])
    ax.text(7.15, 0.665, text["soft"], ha="center", fontsize=24, fontweight="bold", color=nm.COLORS["blue"])
    ax.text(7.75, 0.135, text["hard"], ha="center", fontsize=24, fontweight="bold", color=nm.COLORS["rose"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(curve, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 07 — le thermomètre des prix (échelle en cartes)
# ═════════════════════════════════════════════════════════════════════════════

DATA_7 = '''def price_scale(lang: str) -> list[tuple[str, str, str]]:
    """Cinq zones de l'échelle des prix : (titre, sous-libellé, couleur du liseré), localisées.
    Five zones of the price scale: (title, sublabel, edge color), localized."""
    B, R, M = nm.COLORS["blue"], nm.COLORS["rose"], nm.COLORS["muted"]
    if lang == "fr":
        return [("déflation", "prix en baisse", R), ("cible ~2 %", "l'ancre", B),
                ("inflation modérée", "2 à 5 %", M), ("inflation forte", "2022 : 9-10 %", R),
                ("hyper-\\ninflation", "> 50 % / mois", R)]
    return [("deflation", "prices falling", R), ("target ~2%", "the anchor", B),
            ("moderate inflation", "2 to 5%", M), ("high inflation", "2022: 9-10%", R),
            ("hyper-\\ninflation", "> 50% / month", R)]

zones = price_scale(LANG)'''

FIG_7 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Le thermomètre des prix",
               sub="Où placer chaque mot de la famille — échelle indicative",
               zero="0 %", arrow="la désinflation redescend l'échelle — sans passer sous zéro",
               note="L'inflation sous-jacente retire énergie et alimentation pour lire la tendance de fond ;\\n"
                    "les anticipations, elles, décident si un choc reste un épisode — ou devient une spirale."),
    "en": dict(title="The price thermometer",
               sub="Where to place each word of the family — indicative scale",
               zero="0%", arrow="disinflation climbs back down the scale — without going below zero",
               note="Core inflation strips out energy and food to read the underlying trend;\\n"
                    "expectations, in turn, decide whether a shock stays an episode — or becomes a spiral."),
}

def build_figure(zones: list[tuple[str, str, str]], lang: str) -> Figure:
    """Cinq cartes-zones en ligne (une coupure « // » avant l'hyperinflation) et une flèche de désinflation."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.blank_axes(fig)

    cw, gap, top, bottom = 290, 16, 600, 452
    xs = [100 + i * (cw + gap) for i in range(4)]
    xs.append(xs[3] + cw + 70)
    for x, (title, sub, color) in zip(xs, zones):
        nm.card(ax, x, bottom, cw, top - bottom, edge=color, lw=2.6, radius=18)
        ax.text(x + cw / 2, top + 62, title, ha="center", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["text"], linespacing=1.15)
        ax.text(x + cw / 2, bottom - 40, sub, ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])

    ax.text((xs[3] + cw + xs[4]) / 2, (top + bottom) / 2, "//", ha="center", va="center",
            fontsize=40, fontweight="bold", color=nm.COLORS["muted"])
    ax.text(xs[1], bottom - 8, text["zero"], ha="center", va="center", fontsize=22, color=nm.COLORS["muted"])

    ax.annotate("", xy=(xs[1] + 40, 330), xytext=(xs[3] + cw - 40, 330),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["blue"], lw=3))
    ax.text((xs[1] + xs[3] + cw) / 2, 278, text["arrow"], ha="center", va="center",
            fontsize=24, color=nm.COLORS["blue"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(zones, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 08 — la volière : faucons, colombes et la boîte à outils
# ═════════════════════════════════════════════════════════════════════════════

DATA_8 = '''def aviary(lang: str) -> tuple[dict, dict, tuple[str, str]]:
    """Faucon (rose) et colombe (bleu) avec leurs trois traits, plus la boîte à outils, localisés.
    Hawk (rose) and dove (blue) with their three traits, plus the toolbox, localized."""
    if lang == "fr":
        hawk = dict(title="Le faucon (hawkish)", color=nm.COLORS["rose"],
                    bullets=["· priorité : casser l'inflation", "· des taux plus hauts, plus longtemps",
                             "· accepte de freiner l'activité"])
        dove = dict(title="La colombe (dovish)", color=nm.COLORS["blue"],
                    bullets=["· priorité : l'activité et l'emploi", "· des taux plus bas, plus vite",
                             "· accepte un peu plus d'inflation"])
        tools = ("la boîte à outils",
                 "taux directeur (le court terme) · bilan, QE / QT (le long terme) · la parole,\\nforward guidance (les anticipations)")
        return hawk, dove, tools
    hawk = dict(title="The hawk (hawkish)", color=nm.COLORS["rose"],
                bullets=["· priority: break inflation", "· higher rates, for longer",
                         "· accepts braking activity"])
    dove = dict(title="The dove (dovish)", color=nm.COLORS["blue"],
                bullets=["· priority: activity and jobs", "· lower rates, sooner",
                         "· accepts a bit more inflation"])
    tools = ("the toolbox",
             "policy rate (the short term) · balance sheet, QE / QT (the long term) · the word,\\nforward guidance (expectations)")
    return hawk, dove, tools

hawk, dove, tools = aviary(LANG)'''

FIG_8 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="La volière de la banque centrale",
               sub="Faucons, colombes — et une boîte à trois outils",
               note="Un communiqué est « hawkish » ou « dovish » selon le côté vers lequel il fait pencher les anticipations —\\n"
                    "c'est ainsi qu'un adjectif déplace des milliards. Le pivot : le cap qui s'inverse."),
    "en": dict(title="The central bank's aviary",
               sub="Hawks, doves — and a three-tool box",
               note="A statement is « hawkish » or « dovish » depending on the side it tilts expectations toward —\\n"
                    "that is how one adjective moves billions. The pivot: the course reversing."),
}

def draw_card(ax, x, w, top, bottom, side):
    """Carte à liseré coloré : titre puis trois puces alignées à gauche."""
    nm.card(ax, x, bottom, w, top - bottom, edge=side["color"], lw=2.6, radius=20)
    ax.text(x + 48, top - 66, side["title"], ha="left", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["text"])
    for j, bullet in enumerate(side["bullets"]):
        ax.text(x + 48, top - 168 - j * 92, bullet, ha="left", va="center",
                fontsize=25, color=nm.COLORS["text"])

def build_figure(hawk: dict, dove: dict, tools: tuple[str, str], lang: str) -> Figure:
    """Deux cartes (faucon / colombe) et un bandeau « boîte à outils » en pied."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    cw, gap = 725, 90
    x0 = (1747 - (2 * cw + gap)) / 2
    draw_card(ax, x0, cw, 845, 440, hawk)
    draw_card(ax, x0 + cw + gap, cw, 845, 440, dove)

    bw = 2 * cw + gap
    nm.card(ax, x0, 180, bw, 195, edge=nm.COLORS["muted"], lw=2.2, radius=18)
    ax.text(x0 + bw / 2, 320, tools[0], ha="center", va="center", fontsize=27,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(x0 + bw / 2, 245, tools[1], ha="center", va="center", fontsize=24,
            color=nm.COLORS["muted"], linespacing=1.45)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(hawk, dove, tools, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 09 — la courbe des taux (deux courbes stylisées)
# ═════════════════════════════════════════════════════════════════════════════

DATA_9 = '''def yield_curves() -> dict:
    """Deux courbes des taux stylisées (non issues de données réelles) : normale et inversée.
    Two stylized yield curves (not from real data): normal and inverted, crossing near 6 years."""
    import numpy as np
    m = np.geomspace(1, 30, 240)
    normal = 4.85 - 2.8 * m ** -0.8
    inverted = 3.85 + 1.4 * m ** -0.8
    return dict(m=m, normal=normal, inverted=inverted)

curves = yield_curves()'''

FIG_9 = '''from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La courbe des taux : la pente qui parle",
        sub="Rendement selon l'échéance du prêt — deux photographies stylisées d'un même marché",
        xlabels=["1 an", "5 ans", "10 ans", "20 ans", "30 ans"],
        short="à gauche, les taux courts — pilotés par la banque centrale",
        normal="courbe NORMALE — pentue :\\nl'attente est rémunérée, les taux longs\\nau-dessus des taux courts",
        long="à droite, les taux longs — fixés par le marché obligataire",
        inverted="courbe INVERSÉE — les taux courts dominent :\\nle marché anticipe des baisses de taux,\\nsouvent par crainte d'un ralentissement",
        note="Courbes stylisées, non issues de données réelles. Pentification : la courbe se redresse ; aplatissement : elle\\n"
             "s'écrase ; inversion : elle bascule, les taux courts passant au-dessus des taux longs."),
    "en": dict(
        title="The yield curve: the slope that speaks",
        sub="Yield by loan maturity — two stylized snapshots of one market",
        xlabels=["1 yr", "5 yrs", "10 yrs", "20 yrs", "30 yrs"],
        short="on the left, short rates — steered by the central bank",
        normal="NORMAL curve — upward:\\nwaiting is rewarded, long rates\\nabove short rates",
        long="on the right, long rates — set by the bond market",
        inverted="INVERTED curve — short rates dominate:\\nthe market expects rate cuts,\\noften fearing a slowdown",
        note="Stylized curves, not from real data. Steepening: the curve straightens; flattening: it squashes; inversion:\\n"
             "it flips, short rates rising above long rates."),
}

def build_figure(curves: dict, lang: str) -> Figure:
    """Courbe normale (bleu, pentue) et courbe inversée (rose, descendante) selon l'échéance (log)."""
    text = LABELS[lang]
    unit = " %" if lang == "fr" else "%"
    fig = nm.figure(height_px=834)
    ax = nm.axes(fig, left=0.06, right=0.95, bottom=0.205)
    m = curves["m"]
    ax.plot(m, curves["normal"], color=nm.COLORS["blue"], linewidth=4.2)
    ax.plot(m, curves["inverted"], color=nm.COLORS["rose"], linewidth=4.2)
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator([1, 5, 10, 20, 30]))
    ax.xaxis.set_major_formatter(FixedFormatter(text["xlabels"]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xlim(1, 30)
    ax.set_ylim(0, 6.5)
    ax.set_yticks(range(0, 7))
    ax.set_yticklabels([f"{v}{unit}" for v in range(0, 7)])

    ax.text(0.015, 0.99, text["short"], transform=ax.transAxes, va="top", fontsize=18, color=nm.COLORS["muted"])
    ax.text(0.30, 0.90, text["normal"], transform=ax.transAxes, va="top", fontsize=18,
            fontweight="bold", color=nm.COLORS["blue"], linespacing=1.15)
    ax.text(0.56, 0.662, text["long"], transform=ax.transAxes, va="center", fontsize=17, color=nm.COLORS["muted"])
    ax.text(0.295, 0.54, text["inverted"], transform=ax.transAxes, va="top", fontsize=18,
            fontweight="bold", color=nm.COLORS["rose"], linespacing=1.15)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(curves, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 10 — l'échelle des baisses (trajectoire boursière stylisée)
# ═════════════════════════════════════════════════════════════════════════════

DATA_10 = '''def market_path() -> dict:
    """Trajectoire boursière stylisée (indice, sommet = 150) : hausse, sommet, chute, krach, rebond.
    Stylized market path (index, peak = 150): rise, peak, fall, crash, rally."""
    return dict(x=[0.0, 3.0, 5.2, 6.4, 6.9, 7.6, 8.6, 10.0],
                y=[100, 150, 135, 120, 103, 105, 122, 130])

path = market_path()'''

FIG_10 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="L'échelle des baisses",
        sub="Correction, marché baissier, krach, rebond — les conventions du gros titre",
        ylab="indice (sommet = 150)", sommet="sommet = 150", bull="marché haussier (bull)",
        krach="krach : la chute brutale", rally="rebond (rally)",
        correction="correction : −10 %", bear="marché baissier\\n(bear) : −20 %",
        note="Conventions journalistiques : la correction vers −10 %, le marché baissier à −20 % du sommet ;\\n"
             "le krach se joue en séances, la bulle ne s'identifie qu'après coup. VIX : le thermomètre de la peur."),
    "en": dict(
        title="The ladder of declines",
        sub="Correction, bear market, crash, rally — the headline conventions",
        ylab="index (peak = 150)", sommet="peak = 150", bull="bull market",
        krach="crash: the brutal drop", rally="rally",
        correction="correction: −10%", bear="bear market:\\n−20%",
        note="Journalistic conventions: the correction around −10%, the bear market at −20% from the peak;\\n"
             "the crash plays out over sessions, the bubble is only identified after the fact. VIX: the fear gauge."),
}

def smooth(xa: list, ya: list, n: int = 500) -> tuple:
    """Interpolation cosinus entre ancrages : trajectoire lisse (le krach reste raide, en x court)."""
    xa, ya = np.asarray(xa, float), np.asarray(ya, float)
    xs = np.linspace(xa[0], xa[-1], n)
    ys = np.empty_like(xs)
    for i in range(len(xa) - 1):
        m = (xs >= xa[i]) & (xs <= xa[i + 1])
        t = (xs[m] - xa[i]) / (xa[i + 1] - xa[i])
        ys[m] = ya[i] + (ya[i + 1] - ya[i]) * (0.5 - 0.5 * np.cos(np.pi * t))
    return xs, ys

def build_figure(path: dict, lang: str) -> Figure:
    """Une trajectoire d'indice, seuils −10 % / −20 % en pointillés, krach puis rebond."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.axes(fig, left=0.075, right=0.985)
    ax.grid(False)
    ax.set_xticks([])
    xs, ys = smooth(path["x"], path["y"])
    ax.plot(xs, ys, color=nm.COLORS["blue"], linewidth=5, solid_capstyle="round")
    ax.set_ylim(93, 158)
    ax.set_yticks([100, 120, 135, 150])
    ax.set_xlim(-0.3, 10.5)
    ax.set_ylabel(text["ylab"])

    ax.axhline(150, color=nm.COLORS["edge"], linewidth=1.2, alpha=0.6)
    ax.axhline(100, color=nm.COLORS["edge"], linewidth=1.2, alpha=0.6)
    ax.axhline(135, color=nm.COLORS["muted"], linestyle=(0, (7, 5)), linewidth=2.2, alpha=0.9)
    ax.axhline(120, color=nm.COLORS["rose"], linestyle=(0, (7, 5)), linewidth=2.2, alpha=0.9)

    ax.text(0.05, 153, text["sommet"], va="bottom", fontsize=22, color=nm.COLORS["muted"])
    ax.annotate(text["bull"], xy=(1.9, 127), xytext=(1.35, 143), ha="left", fontsize=24,
                color=nm.COLORS["text"], arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    ax.annotate(text["krach"], xy=(6.78, 109), xytext=(3.5, 104), ha="left", va="center", fontsize=24,
                color=nm.COLORS["rose"], arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.3))
    ax.text(7.5, 107, text["rally"], ha="left", va="center", fontsize=24, color=nm.COLORS["text"])
    ax.text(10.4, 136, text["correction"], ha="right", va="bottom", fontsize=22, color=nm.COLORS["muted"])
    ax.text(10.45, 119, text["bear"], ha="right", va="top", fontsize=22, color=nm.COLORS["rose"], linespacing=1.35)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(path, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 11 — l'État et le monde (budget vs change, deux cartes)
# ═════════════════════════════════════════════════════════════════════════════

DATA_11 = '''def state_world(lang: str) -> tuple[dict, dict]:
    """Deux cartes : politique budgétaire (bleu) et change & balances (rose), avec puces à deux lignes.
    Two cards: fiscal policy (blue) and currency & balances (rose), bullets on two lines, localized."""
    if lang == "fr":
        left = dict(title="La politique budgétaire", color=nm.COLORS["blue"],
                    bullets=[["· relance : dépenser plus, taxer", "  moins — soutenir la demande"],
                             ["· austérité / consolidation : l'inverse"],
                             ["· stabilisateurs automatiques : le", "  déficit se creuse seul en récession"]])
        right = dict(title="Le change et les balances", color=nm.COLORS["rose"],
                     bullets=[["· change flottant : la monnaie se", "  déprécie / s'apprécie (le marché)"],
                              ["· change fixe : elle est dévaluée /", "  réévaluée (une décision)"],
                              ["· balance commerciale : les biens ;", "  courante : + services et revenus"]])
        return left, right
    left = dict(title="Fiscal policy", color=nm.COLORS["blue"],
                bullets=[["· stimulus: spend more, tax", "  less — support demand"],
                         ["· austerity / consolidation: the reverse"],
                         ["· automatic stabilizers: the", "  deficit widens on its own in a recession"]])
    right = dict(title="Currency and balances", color=nm.COLORS["rose"],
                 bullets=[["· floating: the currency", "  depreciates / appreciates (the market)"],
                          ["· fixed: it is devalued /", "  revalued (a decision)"],
                          ["· trade balance: goods;", "  current account: + services and income"]])
    return left, right

left, right = state_world(LANG)'''

FIG_11 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="L'État et le monde",
               sub="Le deuxième pilote de l'économie — et les mots précis du dehors",
               note="Dire que « l'euro a été dévalué » parce qu'il glisse face au dollar est un abus de langage :\\n"
                    "l'euro flotte, il se déprécie. La nuance dit qui agit — le marché ou un gouvernement."),
    "en": dict(title="The State and the world",
               sub="The economy's second pilot — and the precise words of the outside",
               note="Saying « the euro was devalued » because it slips against the dollar is a misuse:\\n"
                    "the euro floats, it depreciates. The nuance says who acts — the market or a government."),
}

def draw_card(ax, x, w, top, bottom, side):
    """Carte à liseré coloré : titre puis trois puces (chacune sur une ou deux lignes)."""
    nm.card(ax, x, bottom, w, top - bottom, edge=side["color"], lw=2.6, radius=20)
    ax.text(x + 48, top - 70, side["title"], ha="left", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["text"])
    y = top - 185
    for bullet in side["bullets"]:
        for line in bullet:
            ax.text(x + 48, y, line, ha="left", va="center", fontsize=24, color=nm.COLORS["text"])
            y -= 52
        y -= 34

def build_figure(left: dict, right: dict, lang: str) -> Figure:
    """Carte budgétaire (bleu) et carte change/balances (rose), face à face."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.blank_axes(fig)

    cw, gap = 725, 90
    x0 = (1747 - (2 * cw + gap)) / 2
    draw_card(ax, x0, cw, 830, 205, left)
    draw_card(ax, x0 + cw + gap, cw, 830, 205, right)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(left, right, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 12 — la même dépêche, dépliée (quatre mécanismes)
# ═════════════════════════════════════════════════════════════════════════════

DATA_12 = '''def dispatch_rows(lang: str) -> list[tuple[str, str]]:
    """Quatre lignes de la dépêche décodée : (citation rose, explication grise), localisées.
    Four rows of the decoded dispatch: (rose quote, grey explanation), localized."""
    if lang == "fr":
        return [("« La Fed a opté pour le statu quo »", "le taux directeur n'a pas bougé"),
                ("« un communiqué hawkish a aplati la courbe »",
                 "ton plus ferme : les taux courts montent\\nvers les taux longs"),
                ("« déjà intégré le pivot… taux terminal relevé »",
                 "le sommet attendu du cycle de hausses\\nest revu vers le haut"),
                ("« le consensus table sur un atterrissage\\nen douceur »",
                 "prévision moyenne : l'inflation revient\\nà la cible sans récession")]
    return [("« The Fed opted for a hold »", "the policy rate did not move"),
            ("« a hawkish statement flattened the curve »",
             "a firmer tone: short rates rise\\ntoward long rates"),
            ("« already priced in the pivot… terminal rate lifted »",
             "the expected summit of the hiking\\ncycle is revised upward"),
            ("« the consensus bets on a soft\\nlanding »",
             "average forecast: inflation returns\\nto target without a recession")]

rows = dispatch_rows(LANG)'''

FIG_12 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="La même dépêche, dépliée", sub="Il n'y a jamais eu de mur",
               note="Quatre mécanismes pliés dans quatre mots de passe : qui bouge, ce qui monte, ce qui baisse.\\n"
                    "La méthode vaut pour tout mot qu'on inventera demain."),
    "en": dict(title="The same dispatch, unfolded", sub="There was never a wall",
               note="Four mechanisms folded into four passwords: what moves, what rises, what falls.\\n"
                    "The method holds for any word coined tomorrow."),
}

def build_figure(rows: list[tuple[str, str]], lang: str) -> Figure:
    """Quatre bandeaux : citation rose à gauche, flèche, explication grise à droite."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1178)
    ax = nm.blank_axes(fig)

    x, w, h, gap, top0 = 100, 1547, 150, 36, 1000
    for i, (quote, expl) in enumerate(rows):
        top = top0 - i * (h + gap)
        cy = top - h / 2
        nm.card(ax, x, top - h, w, h, edge=nm.COLORS["edge"], lw=2.2, radius=18)
        ax.text(x + 45, cy, quote, ha="left", va="center", fontsize=24, fontweight="bold",
                color=nm.COLORS["rose"], linespacing=1.35)
        ax.annotate("", xy=(x + 935, cy), xytext=(x + 860, cy),
                    arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=2.4))
        ax.text(x + 965, cy, expl, ha="left", va="center", fontsize=23,
                color=nm.COLORS["muted"], linespacing=1.35)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(rows, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Assemblage
# ═════════════════════════════════════════════════════════════════════════════

META = dict(
    num="5",
    title_fr="Le vocabulaire essentiel de la macroéconomie financière, sans jargon",
    title_en="The Essential Vocabulary of Financial Macroeconomics, Without the Jargon",
    slug_fr="le-vocabulaire-essentiel-de-la-macroeconomie-financiere",
    slug_en="the-essential-vocabulary-of-financial-macroeconomics",
)
DIR = "macro/05-vocabulaire-essentiel"

FIGURES = [
    dict(name="fig01-mur-de-jargon",
         fig_fr="Trois lignes, sept mots de passe", fig_en="Three lines, seven passwords",
         live=False, data=DATA_1, fig=FIG_1),
    dict(name="fig02-mot-mecanisme-plie",
         fig_fr="Un mot = un mécanisme plié", fig_en="One word = one folded mechanism",
         live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-niveau-vs-variation",
         fig_fr="« L'inflation ralentit » ne veut pas dire « les prix baissent »",
         fig_en="« Inflation is slowing » does not mean « prices are falling »",
         live=True, data=DATA_3, fig=FIG_3),
    dict(name="fig04-nominal-vs-reel",
         fig_fr="Le nominal affiche, le réel décide", fig_en="The nominal shows, the real decides",
         live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-stock-flux-dette-deficit",
         fig_fr="Le déficit baisse, la dette monte quand même",
         fig_en="The deficit falls, the debt rises anyway",
         live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-les-mots-du-cycle",
         fig_fr="Les mots du cycle", fig_en="The words of the cycle",
         live=False, data=DATA_6, fig=FIG_6),
    dict(name="fig07-thermometre-des-prix",
         fig_fr="Le thermomètre des prix", fig_en="The price thermometer",
         live=False, data=DATA_7, fig=FIG_7),
    dict(name="fig08-faucons-et-colombes",
         fig_fr="La volière de la banque centrale", fig_en="The central bank's aviary",
         live=False, data=DATA_8, fig=FIG_8),
    dict(name="fig09-courbe-des-taux",
         fig_fr="La courbe des taux : la pente qui parle", fig_en="The yield curve: the slope that speaks",
         live=False, data=DATA_9, fig=FIG_9),
    dict(name="fig10-echelle-des-baisses",
         fig_fr="L'échelle des baisses", fig_en="The ladder of declines",
         live=False, data=DATA_10, fig=FIG_10),
    dict(name="fig11-etat-et-monde",
         fig_fr="L'État et le monde", fig_en="The State and the world",
         live=False, data=DATA_11, fig=FIG_11),
    dict(name="fig12-depeche-decodee",
         fig_fr="La même dépêche, dépliée", fig_en="The same dispatch, unfolded",
         live=False, data=DATA_12, fig=FIG_12),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out5")
    nb_kit.build_all(META, DIR, FIGURES)
