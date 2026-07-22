#!/usr/bin/env python3
"""Notebooks du chapitre 15 — Croissance potentielle et output gap.

Même méthode que les chapitres 18/19/20 : META + FIGURES, puis test_all/build_all
via nb_kit. Une seule cellule code par notebook : load_*() puis build_figure(...).
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="15",
    title_fr="Croissance potentielle et output gap : la carte que personne ne peut mesurer",
    title_en="Potential Growth and the Output Gap: The Map No One Can Measure",
    slug_fr="croissance-potentielle-et-output-gap",
    slug_en="potential-growth-and-output-gap",
)
DIR = "macro/15-croissance-potentielle"


# ── Figure 01 — PIB réel vs PIB potentiel, échelle log (FRED en direct) ───────

DATA_1 = '''from pandas import Series

def load_gdp() -> tuple[Series, Series]:
    """PIB réel (GDPC1) et PIB potentiel (GDPPOT), en direct depuis FRED.
    U.S. real GDP and potential GDP (CBO), live from FRED."""
    real = nm.load_fred("GDPC1")
    potential = nm.load_fred("GDPPOT").loc[:real.index[-1]]   # borne aux données réelles
    return real, potential

real, potential = load_gdp()'''

FIG_1 = '''import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="L'économie et sa vitesse de croisière",
        sub="PIB réel et PIB potentiel des États-Unis, 1949-2026",
        ylab="milliards de dollars de 2017 (échelle log)",
        real="PIB réel", potential="PIB potentiel (CBO)",
        gfc="2009", covid="COVID\\n2020",
        note="Le PIB potentiel (la « ligne » soutenable) ne se mesure pas : il s'estime, et se révise. Le PIB réel oscille\\n"
             "autour de lui — en dessous dans les récessions. Source : BEA et CBO via FRED (GDPC1, GDPPOT)."),
    "en": dict(
        title="The economy and its cruising speed",
        sub="U.S. real GDP and potential GDP, 1949-2026",
        ylab="billions of 2017 dollars (log scale)",
        real="real GDP", potential="potential GDP (CBO)",
        gfc="2009", covid="COVID\\n2020",
        note="Potential GDP (the sustainable « line ») is not measured: it is estimated, and revised. Real GDP oscillates\\n"
             "around it — below it in recessions. Source: BEA and CBO via FRED (GDPC1, GDPPOT)."),
}

_SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

def _sci(value: float, _) -> str:
    """Formate un tick logarithmique en « n × 10ᵏ » (exposant Unicode)."""
    exp = int(np.floor(np.log10(value)))
    mant = int(round(value / 10 ** exp))
    return f"{mant} × 10{str(exp).translate(_SUP)}"

def build_figure(real: Series, potential: Series, lang: str) -> Figure:
    """PIB réel (bleu plein) et potentiel (ambre pointillé) en échelle log."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.092)
    h_real, = ax.plot(real.index, real, color=nm.COLORS["blue"], linewidth=2.9,
                      label=text["real"], zorder=2)
    h_pot, = ax.plot(potential.index, potential, color=nm.COLORS["amber"], linewidth=3.0,
                     linestyle=(0, (6, 4)), label=text["potential"], zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(2000, 33000)
    ax.set_yticks([2000, 5000, 10000, 20000])
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.set_yticks([3000, 4000, 6000, 30000], minor=True)
    ax.yaxis.set_minor_formatter(FuncFormatter(_sci))
    ax.tick_params(axis="y", which="minor", labelsize=20, labelcolor=nm.COLORS["muted"])
    ax.grid(which="minor", visible=False)
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend([h_pot, h_real], [text["potential"], text["real"]], loc="upper left",
              frameon=False, fontsize=23, labelcolor=nm.COLORS["text"],
              handlelength=2.6, borderaxespad=1.4)
    # Annotations : creux de 2009 et choc COVID de 2020.
    ax.annotate(text["gfc"], xy=(pd.Timestamp("2009-01-01"), float(real.loc["2009"].min())),
                xytext=(pd.Timestamp("2011-06-01"), 8800), ha="center", va="center",
                fontsize=22, color=nm.COLORS["muted"],
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=1.6))
    ax.annotate(text["covid"], xy=(pd.Timestamp("2020-04-01"), float(real.loc["2020"].min())),
                xytext=(pd.Timestamp("2015-06-01"), 24200), ha="center", va="center",
                fontsize=22, color=nm.COLORS["muted"], linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=1.6))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(real, potential, LANG)'''


# ── Figure 02 — écart de production (FRED en direct) ──────────────────────────

DATA_2 = '''from pandas import Series

def load_output_gap() -> Series:
    """Écart de production = (PIB réel − PIB potentiel) / PIB potentiel × 100.
    Output gap from real (GDPC1) and potential (GDPPOT) GDP, live from FRED."""
    real = nm.load_fred("GDPC1")
    potential = nm.load_fred("GDPPOT")
    return ((real / potential - 1) * 100).dropna()

gap = load_output_gap()
print(f"Dernier point / latest: {gap.index[-1]:%Y-%m} → {gap.iloc[-1]:+.1f} %")'''

FIG_2 = '''import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Au-dessus, en dessous : le pouls du cycle",
        sub="Écart de production américain (PIB réel − potentiel), 1949-2026",
        ylab="écart de production, % du potentiel",
        today="aujourd'hui\\n+1,0 %",
        gfc="Grande Récession\\n−5,0 % (2009)",
        covid="COVID : −8,8 %\\n(2020)",
        note="Positif (vert) = surchauffe ; négatif (rouge) = sous-emploi. ⚠ Ces valeurs dépendent du millésime CBO de\\n"
             "février 2026 et seront révisées. Source : BEA et CBO via FRED."),
    "en": dict(
        title="Above and below: the pulse of the cycle",
        sub="U.S. output gap (real GDP − potential), 1949-2026",
        ylab="output gap, % of potential",
        today="today\\n+1.0%",
        gfc="Great Recession\\n−5.0% (2009)",
        covid="COVID: −8.8%\\n(2020)",
        note="Positive (green) = overheating; negative (red) = slack. ⚠ These values depend on the February 2026 CBO\\n"
             "vintage and will be revised. Source: BEA and CBO via FRED."),
}

def build_figure(gap: Series, lang: str) -> Figure:
    """Écart de production ombré : vert au-dessus de 0, rouge en dessous."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig)
    ax.fill_between(gap.index, gap, 0, where=gap >= 0, color=nm.COLORS["green"],
                    alpha=0.58, interpolate=True)
    ax.fill_between(gap.index, gap, 0, where=gap < 0, color=nm.COLORS["rose"],
                    alpha=0.5, interpolate=True)
    ax.plot(gap.index, gap, color=nm.COLORS["text"], linewidth=1.5)
    ax.axhline(0, color=nm.COLORS["muted"], linewidth=1.4, alpha=0.9)
    ax.set_ylim(-10.2, 7.0)
    ax.set_yticks(range(-10, 7, 2))
    ax.set_ylabel(text["ylab"])
    ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.annotate(text["today"], xy=(gap.index[-1], float(gap.iloc[-1])),
                xytext=(pd.Timestamp("2019-06-01"), 5.2), ha="center", va="center",
                fontsize=22, fontweight="bold", color=nm.COLORS["green"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["green"], lw=1.8))
    ax.annotate(text["gfc"], xy=(pd.Timestamp("2009-09-01"), -4.9),
                xytext=(pd.Timestamp("2004-01-01"), -6.9), ha="center", va="center",
                fontsize=21, fontweight="bold", color=nm.COLORS["rose"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    ax.annotate(text["covid"], xy=(pd.Timestamp("2020-04-01"), -8.6),
                xytext=(pd.Timestamp("2015-06-01"), -7.9), ha="center", va="center",
                fontsize=21, fontweight="bold", color=nm.COLORS["rose"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(gap, LANG)'''


# ── Figure 03 — la loi d'Okun (nuage annuel, FRED en direct) ──────────────────

DATA_3 = '''import pandas as pd
from pandas import DataFrame

def load_okun() -> DataFrame:
    """Par année : variation du taux de chômage (UNRATE) et croissance du PIB réel (GDPC1),
    en moyennes annuelles depuis FRED. / Yearly change in unemployment and real GDP growth."""
    growth = nm.load_fred("GDPC1").resample("YS").mean().pct_change() * 100
    du = nm.load_fred("UNRATE").resample("YS").mean().diff()
    return pd.DataFrame({"du": du, "growth": growth}).dropna()

okun = load_okun()'''

FIG_3 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La loi d'Okun : chômage et croissance",
        sub="Chaque point = une année, États-Unis, 1949-2025",
        xlab="variation du taux de chômage sur l'année, points",
        ylab="croissance du PIB réel, %",
        slope="pente ≈ −1,5", l1="1 point de chômage", l2="≈ 1,5 point de PIB",
        note="Quand le chômage monte, la croissance faiblit — d'environ 1,5 point de PIB par point de chômage. Une\\n"
             "régularité robuste, mais pas une « loi » : le coefficient varie. Source : BEA et BLS via FRED (GDPC1, UNRATE)."),
    "en": dict(
        title="Okun's law: unemployment and growth",
        sub="Each dot = one year, United States, 1949-2025",
        xlab="change in the unemployment rate over the year, points",
        ylab="real GDP growth, %",
        slope="slope ≈ −1.5", l1="1 point of unemployment", l2="≈ 1.5 point of GDP",
        note="When unemployment rises, growth weakens — by about 1.5 points of GDP per point of unemployment. A robust\\n"
             "regularity, but not a « law »: the coefficient varies. Source: BEA and BLS via FRED (GDPC1, UNRATE)."),
}

def build_figure(okun: "DataFrame", lang: str) -> Figure:
    """Nuage annuel Δchômage vs croissance du PIB, avec droite de régression."""
    text = LABELS[lang]
    x, y = okun["du"].to_numpy(), okun["growth"].to_numpy()
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.072, bottom=0.185)
    ax.axhline(0, color=nm.COLORS["muted"], linewidth=1.6, alpha=0.78)
    ax.axvline(0, color=nm.COLORS["muted"], linewidth=1.6, alpha=0.78)
    ax.scatter(x, y, s=70, color=nm.COLORS["blue"], alpha=0.8, linewidths=0, zorder=3)
    slope, intercept = np.polyfit(x, y, 1)
    line_x = np.array([-1.7, 3.2])
    ax.plot(line_x, intercept + slope * line_x, color=nm.COLORS["amber"], linewidth=4.0, zorder=4)
    ax.set_xlim(-1.7, 3.2)
    ax.set_xticks(range(-1, 4))
    ax.set_ylim(-4.3, 9.2)
    ax.set_yticks(range(-4, 9, 2))
    ax.set_xlabel(text["xlab"])
    ax.set_ylabel(text["ylab"])
    ax.text(1.55, 6.15, text["slope"], ha="center", fontsize=27, fontweight="bold", color=nm.COLORS["amber"])
    ax.text(1.55, 5.2, text["l1"], ha="center", fontsize=22, color=nm.COLORS["muted"])
    ax.text(1.55, 4.45, text["l2"], ha="center", fontsize=22, color=nm.COLORS["muted"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(okun, LANG)'''


# ── Figure 04 — la révision du potentiel par le CBO (données embarquées) ──────

DATA_4 = '''def cbo_potential_2017() -> list[float]:
    """PIB potentiel projeté pour 2017 (base 100) selon les millésimes CBO de 2007 et 2014 :
    une révision à la baisse de 7,3 %. / CBO's projection of 2017 potential GDP, indexed to 100,
    in the 2007 and 2014 vintages: a 7.3% downward revision.
    Source : CBO, « Revisions to CBO's Projection of Potential Output Since 2007 » (2014)."""
    return [100.0, 92.7]

values = cbo_potential_2017()'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Sept points de « vitesse de croisière » évaporés",
        sub="Estimations successives du CBO pour le PIB potentiel de 2017",
        ylab="PIB potentiel projeté pour 2017 (base 100)",
        cats=["projection\\nde 2007", "projection\\nde 2014"],
        value_labels=["100", "92,7"], delta="−7,3 %",
        note="Entre 2007 et 2014, le CBO abaisse de 7,3 % son estimation du potentiel de 2017 — l'essentiel dû à une\\n"
             "réévaluation des tendances d'AVANT-crise. La ligne qu'on croyait connaître était déjà fausse. Source : CBO (2014)."),
    "en": dict(
        title="Seven points of « cruising speed » evaporated",
        sub="Successive CBO estimates of 2017 potential GDP",
        ylab="projected 2017 potential GDP (base 100)",
        cats=["2007\\nprojection", "2014\\nprojection"],
        value_labels=["100", "92.7"], delta="−7.3%",
        note="Between 2007 and 2014, the CBO cut its estimate of 2017 potential by 7.3% — mostly due to a re-evaluation\\n"
             "of pre-crisis trends. The line we thought we knew was already wrong. Source: CBO (2014)."),
}

def build_figure(values: list[float], lang: str) -> Figure:
    """Deux barres : le potentiel 2017 vu en 2007 (100) puis en 2014 (92,7)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1083)
    ax = nm.axes(fig, left=0.092, bottom=0.185)
    ax.grid(axis="x", visible=False)
    positions = range(len(values))
    ax.bar(positions, values, width=0.62, color=["#c9d4e7", nm.COLORS["blue"]], zorder=3)
    ax.set_ylim(0, 108)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 2.9)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, values, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 15), textcoords="offset points",
                    ha="center", va="bottom", fontsize=36, fontweight="bold", color=nm.COLORS["text"])
    # Repère au niveau 100 et flèche de révision.
    ax.plot([0.31, 2.4], [100, 100], color=nm.COLORS["muted"], linestyle=(0, (6, 4)),
            linewidth=2.0, zorder=2)
    ax.plot([2.0], [96], marker="*", color=nm.COLORS["rose"], markersize=17, zorder=4)
    ax.text(2.28, 95.5, text["delta"], ha="left", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["rose"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(values, LANG)'''


# ── Figure 05 — trois « étoiles », une même brume (schéma) ────────────────────

DATA_5 = '''def stars(lang: str) -> list[tuple[str, list[str]]]:
    """Les trois grandeurs « avec étoile » : (titre, description sur deux lignes), localisées.
    The three « starred » quantities: (title, two-line description), localized."""
    if lang == "fr":
        return [
            ("y*  —  potentiel", ["le niveau de production", "soutenable"]),
            ("u*  —  NAIRU", ["le chômage sans", "tension inflationniste"]),
            ("r*  —  taux naturel", ["le taux qui suit", "la croissance tendancielle"]),
        ]
    return [
        ("y*  —  potential", ["the level of output", "that is sustainable"]),
        ("u*  —  NAIRU", ["unemployment with no", "inflationary pressure"]),
        ("r*  —  natural rate", ["the rate that tracks", "trend growth"]),
    ]'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Trois étoiles, une même brume",
        sub="Les grandeurs « avec étoile » que la Fed doit estimer sans jamais les voir",
        bold="Estimées ensemble, dans les mêmes modèles.",
        muted="Réviser l'une force à réviser les autres : un même brouillard les enveloppe."),
    "en": dict(
        title="Three stars, one same fog",
        sub="The « starred » quantities the Fed must estimate without ever seeing them",
        bold="Estimated together, in the same models.",
        muted="Revising one forces revising the others: one same fog envelops them."),
}

def build_figure(cards: list[tuple[str, list[str]]], lang: str) -> Figure:
    """Schéma : trois cartes ambre (y*, u*, r*) reliées, puis une carte de synthèse bleue."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 486, 94, 55
    top, bottom = 780, 410
    mid = (top + bottom) / 2
    centers = []
    for i, (title, lines) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        centers.append(cx)
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS["amber"], lw=2.6, radius=24)
        ax.text(cx, top - 82, title, ha="center", va="center",
                fontsize=31, fontweight="bold", color=nm.COLORS["amber"])
        for j, line in enumerate(lines):
            ax.text(cx, 566 - j * 46, line, ha="center", va="center",
                    fontsize=27, color=nm.COLORS["text"])

    # Connecteurs pointillés entre cartes adjacentes.
    for a, b in zip(centers, centers[1:]):
        ax.plot([a + card_w / 2 + 8, b - card_w / 2 - 8], [mid, mid], color=nm.COLORS["muted"],
                linestyle=(0, (2, 3)), linewidth=2.0, alpha=0.8, zorder=1)

    # Carte de synthèse (bleue).
    bx, bw, bbot, btop = 95, 1560, 60, 300
    nm.card(ax, bx, bbot, bw, btop - bbot, edge=nm.COLORS["blue"], lw=2.6, radius=26)
    bcx = bx + bw / 2
    ax.text(bcx, btop - 96, text["bold"], ha="center", va="center",
            fontsize=31, fontweight="bold", color=nm.COLORS["text"])
    ax.text(bcx, btop - 176, text["muted"], ha="center", va="center",
            fontsize=25, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    # Signature en haut à droite (comme la figure d'origine, sans note de bas).
    hpx = fig.get_size_inches()[1] * nm.DPI
    fig.text(0.9715, 1 - 58 / hpx, "▪ NMLab", fontsize=16.5,
             color=nm.COLORS["muted"], va="top", ha="right")
    return fig

build_figure(stars(LANG), LANG)'''


FIGURES = [
    dict(name="fig01-pib-potentiel", fig_fr="L'économie et sa vitesse de croisière",
         fig_en="The economy and its cruising speed", live=True, data=DATA_1, fig=FIG_1),
    dict(name="fig02-output-gap", fig_fr="Au-dessus, en dessous : le pouls du cycle",
         fig_en="Above and below: the pulse of the cycle", live=True, data=DATA_2, fig=FIG_2),
    dict(name="fig03-loi-okun", fig_fr="La loi d'Okun : chômage et croissance",
         fig_en="Okun's law: unemployment and growth", live=True, data=DATA_3, fig=FIG_3),
    dict(name="fig04-revision-potentiel", fig_fr="Sept points de « vitesse de croisière » évaporés",
         fig_en="Seven points of « cruising speed » evaporated", live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-trois-etoiles", fig_fr="Trois étoiles, une même brume",
         fig_en="Three stars, one same fog", live=False, data=DATA_5, fig=FIG_5),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out15")
    nb_kit.build_all(META, DIR, FIGURES)
