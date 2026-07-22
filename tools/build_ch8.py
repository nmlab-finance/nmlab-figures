#!/usr/bin/env python3
"""Génère les notebooks du chapitre 8 — De la COVID au soft landing (2020-2025).

Chapitre « carte du voyage » : sept figures, toutes construites sur des séries FRED
publiques (inflation, pétrole, PIB, postes vacants, taux directeurs, 10 ans, chômage)
→ toutes EN DIRECT (live=True, nm.load_fred). Convention « strict » : une seule cellule
code, fonctions typées + docstrings — load_*() puis build_figure(...) -> Figure ;
LABELS={"fr":…,"en":…} ; LANG. Titres seuls (sans sous-titre), façon des WebP du chapitre.
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit


META = dict(
    num="8",
    title_fr="La carte du voyage : de la COVID au soft landing (2020-2025)",
    title_en="The Map of the Journey: From COVID to the Soft Landing (2020-2025)",
    slug_fr="de-la-covid-au-soft-landing-2020-2025",
    slug_en="from-covid-to-the-soft-landing-2020-2025",
)
DIR = "macro/08-covid-soft-landing"


# ── Figure 01 — l'inflation, six étapes (CPIAUCNS + euro HICP, FRED en direct) ─

DATA_1 = '''from pandas import Series

def load_inflation() -> tuple[Series, Series]:
    """Inflation en glissement annuel, É.-U. (IPC, CPIAUCNS) et zone euro (IPCH,
    CP0000EZ19M086NEST), de 2019 à 2025, en direct de FRED.
    Year-over-year inflation, U.S. and euro area, 2019-2025, live from FRED."""
    us_cpi = nm.load_fred("CPIAUCNS", start="2017")
    eu_hicp = nm.load_fred("CP0000EZ19M086NEST", start="2017")
    us = ((us_cpi / us_cpi.shift(12) - 1) * 100).loc["2019":"2025"]
    eu = ((eu_hicp / eu_hicp.shift(12) - 1) * 100).loc["2019":"2025"]
    return us, eu

us, eu = load_inflation()'''

FIG_1 = '''import matplotlib.dates as mdates
from pandas import Timestamp as T
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="La carte du voyage : l'inflation, 2019-2025",
        legend=["États-Unis (IPC)", "Zone euro (IPCH)"],
        target="cible : 2 %",
        steps=["1 · L'arrêt", "2 · La riposte", "3 · La surchauffe",
               "4 · Le choc & le resserrement", "5 · La désinflation", "6 · L'atterrissage"],
        us_peak="É.-U. : pic à 9,1 % (juin 2022)",
        eu_peak="zone euro : 10,6 %\\n(oct. 2022)",
        end_us="2,7 %", end_eu="1,9 %",
        note="Sources : BLS (IPC) et Eurostat (IPCH zone euro), via FRED. Glissement annuel, mensuel, janv. 2019 – déc. 2025.\\n"
             "Les six bandes correspondent aux six étapes du chapitre ; valeurs de fin 2025 à droite des courbes."),
    "en": dict(
        title="The map of the journey: inflation, 2019-2025",
        legend=["United States (CPI)", "Euro area (HICP)"],
        target="2% target",
        steps=["1 · The stop", "2 · The response", "3 · The overheat",
               "4 · The shock & tightening", "5 · The disinflation", "6 · The landing"],
        us_peak="U.S.: peak at 9.1% (June 2022)",
        eu_peak="euro area: 10.6%\\n(Oct. 2022)",
        end_us="2.7%", end_eu="1.9%",
        note="Sources: BLS (CPI) and Eurostat (euro-area HICP), via FRED. Year-over-year, monthly, Jan. 2019 – Dec. 2025.\\n"
             "The six bands mark the chapter's six legs; end-2025 values to the right of the curves."),
}

def build_figure(us: Series, eu: Series, lang: str) -> Figure:
    """Deux courbes d'inflation, six bandes-étapes, pics annotés et valeurs de fin."""
    text = LABELS[lang]
    pct = FuncFormatter(lambda v, _: (f"{v:.0f} %" if lang == "fr" else f"{v:.0f}%").replace("-", "−"))
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.072, top=0.86)

    # Six bandes-étapes alternées (très discrètes) / six alternating step bands.
    bounds = [T("2019-01-01"), T("2020-05-01"), T("2021-03-01"), T("2022-02-01"),
              T("2023-07-01"), T("2024-07-01"), T("2026-01-01")]
    for i in range(6):
        if i % 2 == 1:
            ax.axvspan(bounds[i], bounds[i + 1], color=nm.COLORS["edge"], alpha=0.14, linewidth=0)

    ax.axhline(2, color=nm.COLORS["muted"], linestyle=(0, (6, 4)), linewidth=1.8, alpha=0.85)
    ax.plot(us.index, us, color=nm.COLORS["blue"], linewidth=2.9, label=text["legend"][0])
    ax.plot(eu.index, eu, color=nm.COLORS["rose"], linewidth=2.9, label=text["legend"][1])

    ax.set_ylim(-1, 13.3)
    ax.set_yticks(range(0, 13, 2))
    ax.yaxis.set_major_formatter(pct)
    ax.set_xlim(T("2019-01-01"), T("2026-03-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.text(T("2019-02-01"), 2.55, text["target"], fontsize=20, color=nm.COLORS["muted"], va="bottom")
    step_x = [T("2019-10-01"), T("2020-04-01"), T("2021-02-01"),
              T("2021-11-01"), T("2023-05-01"), T("2024-08-01")]
    for i, (x, label) in enumerate(zip(step_x, text["steps"])):
        ax.text(x, 12.6 if i % 2 == 0 else 11.5, label, fontsize=20.5,
                color=nm.COLORS["muted"], va="center", ha="left")

    us_pk = us.loc["2021":"2023"].idxmax()
    eu_pk = eu.loc["2021":"2023"].idxmax()
    ax.annotate(text["us_peak"], xy=(us_pk, us.loc[us_pk]), xytext=(T("2020-09-01"), 10.4),
                fontsize=21.5, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["eu_peak"], xy=(eu_pk, eu.loc[eu_pk]), xytext=(T("2023-02-01"), 11.2),
                fontsize=21.5, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))

    ax.annotate(text["end_us"], xy=(us.index[-1], us.iloc[-1]), xytext=(10, 6),
                textcoords="offset points", fontsize=26, fontweight="bold",
                color=nm.COLORS["blue2"], va="center", ha="left", annotation_clip=False)
    ax.annotate(text["end_eu"], xy=(eu.index[-1], eu.iloc[-1]), xytext=(10, -8),
                textcoords="offset points", fontsize=26, fontweight="bold",
                color=nm.COLORS["rose"], va="center", ha="left", annotation_clip=False)

    leg = ax.legend(loc="upper left", bbox_to_anchor=(0.015, 0.72), fontsize=22,
                    labelcolor=nm.COLORS["text"], handlelength=1.5, borderpad=0.8,
                    labelspacing=0.6, fancybox=True)
    leg.get_frame().set_facecolor(nm.COLORS["card"])
    leg.get_frame().set_edgecolor(nm.COLORS["edge"])
    nm.header(fig, text["title"])
    nm.footer(fig, text["note"])
    return fig

build_figure(us, eu, LANG)'''


# ── Figure 02 — le pétrole à prix négatif (DCOILWTICO, FRED en direct) ────────

DATA_2 = '''from pandas import Series

def load_oil() -> Series:
    """Prix quotidien du pétrole WTI spot (DCOILWTICO), 2019-2020, en direct de FRED —
    la série contient le −36,98 $ du 20 avril 2020.
    Daily WTI spot crude (DCOILWTICO), 2019-2020, live from FRED (incl. the negative print)."""
    return nm.load_fred("DCOILWTICO", start="2019").loc["2019":"2020"].dropna()

oil = load_oil()'''

FIG_2 = '''from pandas import Timestamp as T
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="L'impensable : le pétrole à prix négatif (avril 2020)",
        pre="~60 $ avant la pandémie",
        neg="20 avr. 2020 : −37 $",
        note="Source : EIA via FRED (DCOILWTICO), pétrole brut WTI spot (Cushing), quotidien, 2019-2020.\\n"
             "20 avril 2020 : spot −36,98 $, contrat de mai réglé −37,63 $ — premier prix négatif de l'histoire du contrat."),
    "en": dict(
        title="The unthinkable: negative oil prices (April 2020)",
        pre="~$60 before the pandemic",
        neg="Apr. 20, 2020: −$37",
        note="Source: EIA via FRED (DCOILWTICO), WTI spot crude (Cushing), daily, 2019-2020.\\n"
             "April 20, 2020: spot −$36.98, May contract settled at −$37.63 — the first negative price in the contract's history."),
}

def build_figure(oil: Series, lang: str) -> Figure:
    """Cours du pétrole, ligne de zéro, plongeon du 20 avril cerclé de rose."""
    text = LABELS[lang]
    import matplotlib
    matplotlib.rcParams["text.parse_math"] = False   # les « $ » restent littéraux
    def usd(v, _):
        s = "$" if lang == "en" else " $"
        if v < 0:
            return f"−${abs(v):.0f}" if lang == "en" else f"−{abs(v):.0f} $"
        return f"${v:.0f}" if lang == "en" else f"{v:.0f} $"
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.078, top=0.86)
    ax.axhline(0, color=nm.COLORS["muted"], linestyle=(0, (6, 4)), linewidth=1.8, alpha=0.85)
    ax.plot(oil.index, oil, color=nm.COLORS["blue"], linewidth=2.0)

    trough = oil.loc["2020-04"].idxmin()
    tval = oil.loc[trough]
    ax.scatter([trough], [tval], s=150, facecolors="none", edgecolors=nm.COLORS["rose"],
               linewidths=2.6, zorder=6)

    ax.set_ylim(-46, 84)
    ax.set_yticks(range(-40, 81, 20))
    ax.yaxis.set_major_formatter(FuncFormatter(usd))
    ax.set_xlim(T("2019-01-01"), T("2021-01-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.annotate(text["pre"], xy=(T("2020-02-01"), 60), xytext=(T("2019-02-15"), 71),
                fontsize=22, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["neg"], xy=(trough, tval), xytext=(T("2020-06-01"), -29),
                fontsize=22, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    nm.header(fig, text["title"])
    nm.footer(fig, text["note"])
    return fig

build_figure(oil, LANG)'''


# ── Figure 03 — PIB réel indexé (GDPC1 + zone euro, FRED en direct) ───────────

DATA_3 = '''from pandas import Series

def load_gdp() -> tuple[Series, Series]:
    """PIB réel É.-U. (GDPC1) et zone euro (CLVMNACSCAB1GQEA19), base 100 = T4 2019,
    2019-2025, en direct de FRED.
    Real GDP, U.S. and euro area, indexed to Q4 2019 = 100, live from FRED."""
    us_g = nm.load_fred("GDPC1", start="2018")
    eu_g = nm.load_fred("CLVMNACSCAB1GQEA19", start="2018")
    us = (us_g / us_g.loc["2019-10-01"] * 100).loc["2019":"2025"]
    eu = (eu_g / eu_g.loc["2019-10-01"] * 100).loc["2019":"2025"]
    return us, eu

us, eu = load_gdp()'''

FIG_3 = '''from pandas import Timestamp as T
import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le choc, le V, la divergence : PIB réel, base 100 = fin 2019",
        legend=["États-Unis", "Zone euro"],
        base="niveau de fin 2019",
        us_rec="les É.-U. effacent la chute\\ndès le début 2021",
        eu_rec="la zone euro y revient\\nà l'été 2021",
        us_low="É.-U. : −9 % (mi-2020)",
        eu_low="zone euro : −14 %",
        end_us="É.-U. : +15 %", end_eu="zone euro : +7 %",
        note="Sources : BEA et Eurostat (PIB en volume, zone euro à 19), via FRED. Trimestriel, T1 2019 – T4 2025.\\n"
             "Base 100 = T4 2019, millésime de juillet 2026 — les premières estimations de 2020 étaient plus sombres encore."),
    "en": dict(
        title="The shock, the V, the divergence: real GDP, 100 = end-2019",
        legend=["United States", "Euro area"],
        base="end-2019 level",
        us_rec="the U.S. erase the drop\\nby early 2021",
        eu_rec="the euro area returns\\nby summer 2021",
        us_low="U.S.: −9% (mid-2020)",
        eu_low="euro area: −14%",
        end_us="U.S.: +15%", end_eu="euro area: +7%",
        note="Sources: BEA and Eurostat (real GDP, euro area 19), via FRED. Quarterly, Q1 2019 – Q4 2025.\\n"
             "100 = Q4 2019, July 2026 vintage — the first 2020 estimates were darker still."),
}

def build_figure(us: Series, eu: Series, lang: str) -> Figure:
    """Deux courbes de PIB indexées à 100 (fin 2019), creux et fin annotés."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.062, top=0.86)
    ax.axhline(100, color=nm.COLORS["muted"], linestyle=(0, (6, 4)), linewidth=1.8, alpha=0.85)
    ax.plot(us.index, us, color=nm.COLORS["blue"], linewidth=2.7, marker="o", markersize=5,
            markerfacecolor=nm.COLORS["blue"], markeredgecolor=nm.COLORS["blue"], label=text["legend"][0])
    ax.plot(eu.index, eu, color=nm.COLORS["rose"], linewidth=2.7, marker="o", markersize=5,
            markerfacecolor=nm.COLORS["rose"], markeredgecolor=nm.COLORS["rose"], label=text["legend"][1])

    ax.set_ylim(84, 117)
    ax.set_yticks(range(85, 116, 5))
    ax.set_xlim(T("2019-01-01"), T("2026-01-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.text(T("2019-02-01"), 100.7, text["base"], fontsize=20, color=nm.COLORS["muted"], va="bottom")

    us_tr = us.loc["2020"].idxmin(); eu_tr = eu.loc["2020"].idxmin()
    ax.annotate(text["us_rec"], xy=(T("2021-01-01"), us.loc["2021-01-01"]),
                xytext=(T("2020-08-01"), 107.5), fontsize=21, color=nm.COLORS["text"],
                va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["eu_rec"], xy=(T("2021-07-01"), eu.loc["2021-07-01"]),
                xytext=(T("2022-01-01"), 97.5), fontsize=21, color=nm.COLORS["text"],
                va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["us_low"], xy=(us_tr, us.loc[us_tr]), xytext=(T("2021-03-01"), 91),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["eu_low"], xy=(eu_tr, eu.loc[eu_tr]), xytext=(T("2021-05-01"), 86.3),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))

    ax.annotate(text["end_us"], xy=(us.index[-1], us.iloc[-1]), xytext=(0, 20),
                textcoords="offset points", fontsize=25, fontweight="bold",
                color=nm.COLORS["blue2"], va="bottom", ha="right")
    ax.annotate(text["end_eu"], xy=(eu.index[-1], eu.iloc[-1]), xytext=(0, -22),
                textcoords="offset points", fontsize=25, fontweight="bold",
                color=nm.COLORS["rose"], va="top", ha="right")

    leg = ax.legend(loc="upper left", bbox_to_anchor=(0.015, 0.97), fontsize=22,
                    labelcolor=nm.COLORS["text"], handlelength=1.5, borderpad=0.8,
                    labelspacing=0.6, fancybox=True)
    leg.get_frame().set_facecolor(nm.COLORS["card"])
    leg.get_frame().set_edgecolor(nm.COLORS["edge"])
    nm.header(fig, text["title"])
    nm.footer(fig, text["note"])
    return fig

build_figure(us, eu, LANG)'''


# ── Figure 04 — postes vacants par chômeur (JTSJOL / UNEMPLOY, FRED direct) ────

DATA_4 = '''from pandas import Series

def load_ratio() -> Series:
    """Postes vacants (JOLTS, JTSJOL) rapportés au nombre de chômeurs (UNEMPLOY),
    2019-2025, en direct de FRED.
    JOLTS job openings over the number of unemployed, 2019-2025, live from FRED."""
    openings = nm.load_fred("JTSJOL", start="2019")
    unemployed = nm.load_fred("UNEMPLOY", start="2019")
    return (openings / unemployed).loc["2019":"2025"].dropna()

ratio = load_ratio()'''

FIG_4 = '''from pandas import Timestamp as T
import matplotlib.dates as mdates
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La surchauffe en un chiffre : postes vacants par chômeur",
        equil="équilibre : 1 pour 1",
        peak="mars 2022 : 2 postes vacants\\npar chômeur",
        trough="avr. 2020 : 0,2",
        end="fin 2025 : 0,9",
        note="Sources : BLS via FRED — offres d'emploi JOLTS (JTSJOL) rapportées au nombre de chômeurs (UNEMPLOY). Mensuel, 2019-2025.\\n"
             "Pic de mars 2022 : 2,0. La détente de 2022 à 2025 est passée par les offres, pas par les licenciements."),
    "en": dict(
        title="Overheating in one number: job openings per unemployed",
        equil="balance: 1 to 1",
        peak="Mar. 2022: 2 job openings\\nper unemployed",
        trough="Apr. 2020: 0.2",
        end="end 2025: 0.9",
        note="Sources: BLS via FRED — JOLTS job openings (JTSJOL) over the number of unemployed (UNEMPLOY). Monthly, 2019-2025.\\n"
             "March 2022 peak: 2.0. The 2022-2025 easing came through openings, not layoffs."),
}

def build_figure(ratio: Series, lang: str) -> Figure:
    """Ratio offres/chômeurs, ligne d'équilibre à 1, pic et creux annotés."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.058, top=0.86)
    ax.axhline(1, color=nm.COLORS["muted"], linestyle=(0, (6, 4)), linewidth=1.8, alpha=0.85)
    ax.plot(ratio.index, ratio, color=nm.COLORS["blue"], linewidth=2.9)

    ax.set_ylim(0, 2.72)
    ax.set_yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax.set_xlim(T("2019-01-01"), T("2026-01-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.text(T("2019-02-01"), 0.92, text["equil"], fontsize=20, color=nm.COLORS["muted"], va="top")
    peak = ratio.loc["2021":"2023"].idxmax()
    trough = ratio.loc["2020"].idxmin()
    ax.annotate(text["peak"], xy=(peak, ratio.loc[peak]), xytext=(T("2020-06-01"), 2.36),
                fontsize=21.5, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["trough"], xy=(trough, ratio.loc[trough]), xytext=(T("2020-08-01"), 0.28),
                fontsize=21.5, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["end"], xy=(ratio.index[-1], ratio.iloc[-1]), xytext=(T("2024-06-01"), 1.42),
                fontsize=21.5, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    nm.header(fig, text["title"])
    nm.footer(fig, text["note"])
    return fig

build_figure(ratio, LANG)'''


# ── Figure 05 — taux directeurs Fed & BCE (DFEDTARU + ECBDFR, FRED direct) ─────

DATA_5 = '''from pandas import Series

def load_rates() -> tuple[Series, Series]:
    """Taux directeurs quotidiens : borne haute de la Fed (DFEDTARU) et taux de la
    facilité de dépôt de la BCE (ECBDFR), 2019-2025, en direct de FRED.
    Daily policy rates: Fed target top (DFEDTARU) and ECB deposit rate (ECBDFR)."""
    fed = nm.load_fred("DFEDTARU", start="2019").loc["2019":"2025"].dropna()
    ecb = nm.load_fred("ECBDFR", start="2019").loc["2019":"2025"].dropna()
    return fed, ecb

fed, ecb = load_rates()'''

FIG_5 = '''from pandas import Timestamp as T
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="L'escalier des taux : montée éclair, descente prudente",
        legend=["Fed — borne haute de la fourchette", "BCE — taux de la facilité de dépôt"],
        fed_zero="mars 2020 : 0-0,25 %\\nen deux réunions d'urgence",
        ecb_exit="juil. 2022 : la BCE sort\\nde huit ans de taux négatifs",
        fed_peak="juil. 2023 : 5,25-5,50 %",
        ecb_peak="sept. 2023 :\\ndépôt à 4,00 %",
        cuts="premières baisses :\\nBCE juin, Fed sept. 2024",
        end_fed="3,50-3,75 %", end_ecb="2,00 %",
        note="Sources : Réserve fédérale (borne haute des fed funds) et BCE (facilité de dépôt), via FRED, quotidien.\\n"
             "Fed : +525 pb en 16 mois, BCE : +450 pb en 14 mois. Les dates sont les prises d'effet des décisions."),
    "en": dict(
        title="The rate staircase: lightning climb, cautious descent",
        legend=["Fed — top of the target range", "ECB — deposit facility rate"],
        fed_zero="Mar. 2020: 0-0.25%\\nin two emergency meetings",
        ecb_exit="Jul. 2022: the ECB exits\\neight years of negative rates",
        fed_peak="Jul. 2023: 5.25-5.50%",
        ecb_peak="Sept. 2023:\\ndeposit at 4.00%",
        cuts="first cuts:\\nECB June, Fed Sept. 2024",
        end_fed="3.50-3.75%", end_ecb="2.00%",
        note="Sources: Federal Reserve (top of the fed funds range) and ECB (deposit facility), via FRED, daily.\\n"
             "Fed: +525 bp in 16 months, ECB: +450 bp in 14 months. Dates are the effective dates of the decisions."),
}

def build_figure(fed: Series, ecb: Series, lang: str) -> Figure:
    """Deux escaliers de taux, réunions et premières baisses annotées."""
    text = LABELS[lang]
    pct = FuncFormatter(lambda v, _: (f"{v:.0f} %" if lang == "fr" else f"{v:.0f}%").replace("-", "−"))
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.062, top=0.86)
    ax.axhline(0, color=nm.COLORS["muted"], linewidth=1.3, alpha=0.6)
    ax.plot(fed.index, fed, color=nm.COLORS["blue"], linewidth=2.6, label=text["legend"][0])
    ax.plot(ecb.index, ecb, color=nm.COLORS["rose"], linewidth=2.6, label=text["legend"][1])

    fed_cut = fed[fed.diff() < 0].loc["2024"].index[0]
    ecb_cut = ecb[ecb.diff() < 0].loc["2024"].index[0]
    ax.scatter([fed_cut], [fed.loc[fed_cut]], s=130, facecolors="none",
               edgecolors=nm.COLORS["blue"], linewidths=2.4, zorder=6)
    ax.scatter([ecb_cut], [ecb.loc[ecb_cut]], s=130, facecolors="none",
               edgecolors=nm.COLORS["rose"], linewidths=2.4, zorder=6)

    ax.set_ylim(-1.35, 6.4)
    ax.set_yticks(range(-1, 7))
    ax.yaxis.set_major_formatter(pct)
    ax.set_xlim(T("2019-01-01"), T("2026-01-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.annotate(text["fed_zero"], xy=(T("2020-03-16"), 0.25), xytext=(T("2020-06-01"), 1.55),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["ecb_exit"], xy=(T("2022-07-27"), -0.5), xytext=(T("2020-08-01"), -0.75),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.text(T("2022-08-01"), 5.85, text["fed_peak"], fontsize=21, color=nm.COLORS["text"], va="center", ha="left")
    ax.text(T("2023-07-01"), 3.15, text["ecb_peak"], fontsize=21, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5)
    ax.text(T("2023-10-01"), 1.55, text["cuts"], fontsize=21, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5)

    ax.text(T("2024-08-01"), 3.35, text["end_fed"], fontsize=24, fontweight="bold",
            color=nm.COLORS["blue2"], va="center", ha="left")
    ax.text(T("2025-03-01"), 1.75, text["end_ecb"], fontsize=24, fontweight="bold",
            color=nm.COLORS["rose"], va="center", ha="left")

    leg = ax.legend(loc="upper left", bbox_to_anchor=(0.015, 0.97), fontsize=21,
                    labelcolor=nm.COLORS["text"], handlelength=1.5, borderpad=0.8,
                    labelspacing=0.6, fancybox=True)
    leg.get_frame().set_facecolor(nm.COLORS["card"])
    leg.get_frame().set_edgecolor(nm.COLORS["edge"])
    nm.header(fig, text["title"])
    nm.footer(fig, text["note"])
    return fig

build_figure(fed, ecb, LANG)'''


# ── Figure 06 — rendement du 10 ans américain (DGS10, FRED en direct) ─────────

DATA_6 = '''from pandas import Series

def load_yield() -> Series:
    """Rendement quotidien du Treasury américain à 10 ans (DGS10), 2019-2025,
    en direct de FRED / Daily U.S. 10-year Treasury yield, live from FRED."""
    return nm.load_fred("DGS10", start="2019").loc["2019":"2025"].dropna()

dgs = load_yield()'''

FIG_6 = '''from pandas import Timestamp as T
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="Le prix de l'argent : le rendement américain à 10 ans",
        peak="oct. 2023 : 5 % frôlés,\\nplus haut depuis 2007",
        pivot="déc. 2023 : la Fed pivote,\\nle 10 ans reflue",
        end="fin 2025 : 4,2 %",
        floor="4 août 2020 : 0,52 %",
        note="Source : Réserve fédérale via FRED (DGS10), rendement du Treasury à 10 ans, quotidien, 2019-2025.\\n"
             "Plancher : 0,52 % le 4 août 2020 ; sommet : 4,98 % en clôture le 19 oct. 2023 — 5 % franchis en séance."),
    "en": dict(
        title="The price of money: the U.S. 10-year yield",
        peak="Oct. 2023: 5% brushed,\\nhighest since 2007",
        pivot="Dec. 2023: the Fed pivots,\\nthe 10-year eases",
        end="end 2025: 4.2%",
        floor="Aug. 4, 2020: 0.52%",
        note="Source: Federal Reserve via FRED (DGS10), 10-year Treasury yield, daily, 2019-2025.\\n"
             "Floor: 0.52% on Aug. 4, 2020; peak: 4.98% at close on Oct. 19, 2023 — 5% crossed intraday."),
}

def build_figure(dgs: Series, lang: str) -> Figure:
    """Rendement à 10 ans, plancher de 2020, sommet et pivot de 2023 annotés."""
    text = LABELS[lang]
    pct = FuncFormatter(lambda v, _: (f"{v:.0f} %" if lang == "fr" else f"{v:.0f}%"))
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.06, top=0.86)
    ax.plot(dgs.index, dgs, color=nm.COLORS["blue"], linewidth=1.9)

    ax.set_ylim(0, 6.3)
    ax.set_yticks(range(0, 7))
    ax.yaxis.set_major_formatter(pct)
    ax.set_xlim(T("2019-01-01"), T("2026-01-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    peak = dgs.loc["2023"].idxmax()
    floor = dgs.loc["2020"].idxmin()
    ax.annotate(text["peak"], xy=(peak, dgs.loc[peak]), xytext=(T("2021-06-01"), 5.25),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["pivot"], xy=(T("2023-12-27"), dgs.loc["2023-12-20":"2024-01-05"].mean()),
                xytext=(T("2024-01-01"), 2.55), fontsize=21, color=nm.COLORS["text"],
                va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["end"], xy=(dgs.index[-1], dgs.iloc[-1]), xytext=(T("2024-07-01"), 3.05),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.text(T("2019-08-01"), 0.72, text["floor"], fontsize=21, color=nm.COLORS["text"], va="bottom", ha="left")
    nm.header(fig, text["title"])
    nm.footer(fig, text["note"])
    return fig

build_figure(dgs, LANG)'''


# ── Figure 07 — le chômage américain (UNRATE + USREC, FRED en direct) ─────────

DATA_7 = '''from pandas import Series

def load_data() -> tuple[Series, Series]:
    """Taux de chômage américain (UNRATE) et indicateur de récession NBER (USREC),
    2019-2025, en direct de FRED.
    U.S. unemployment rate and NBER recession flag, 2019-2025, live from FRED."""
    unrate = nm.load_fred("UNRATE", start="2019").loc["2019":"2025"].dropna()
    recessions = nm.load_fred("USREC", start="2019").loc["2019":"2025"]
    return unrate, recessions

unrate, recessions = load_data()'''

FIG_7 = '''from pandas import Timestamp as T
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="Le soft landing en une courbe : le chômage américain",
        band="récession NBER : 2 mois",
        peak="avr. 2020 : 14,8 % — record\\nde la série d'après-guerre",
        start="févr. 2020 : 3,5 %",
        low="avr. 2023 : 3,4 %,\\nplus bas depuis 1969",
        sahm="été 2024 : la règle de Sahm\\ns'allume — fausse alerte",
        end="déc. 2025 : 4,4 %",
        note="Source : BLS via FRED (UNRATE). Mensuel, janv. 2019 – déc. 2025 — pas d'enquête ménages en oct. 2025.\\n"
             "Bande rouge : récession NBER (févr.-avr. 2020), la plus courte jamais datée — et aucune depuis."),
    "en": dict(
        title="The soft landing in one curve: U.S. unemployment",
        band="NBER recession: 2 months",
        peak="Apr. 2020: 14.8% — record\\nof the postwar series",
        start="Feb. 2020: 3.5%",
        low="Apr. 2023: 3.4%,\\nlowest since 1969",
        sahm="Summer 2024: the Sahm rule\\ntriggers — false alarm",
        end="Dec. 2025: 4.4%",
        note="Source: BLS via FRED (UNRATE). Monthly, Jan. 2019 – Dec. 2025 — no household survey in Oct. 2025.\\n"
             "Red band: NBER recession (Feb.-Apr. 2020), the shortest ever dated — and none since."),
}

def build_figure(unrate: Series, recessions: Series, lang: str) -> Figure:
    """Chômage (aire remplie) + bande de récession NBER rose, cinq points annotés."""
    text = LABELS[lang]
    pct = FuncFormatter(lambda v, _: (f"{v:.0f} %" if lang == "fr" else f"{v:.0f}%"))
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig, left=0.06, top=0.86)

    runs = recessions.ne(recessions.shift()).cumsum()
    for _, run in recessions.groupby(runs):
        if run.iloc[0] == 1:
            ax.axvspan(run.index[0], run.index[-1], color=nm.COLORS["rose"], alpha=0.18, linewidth=0)
            mid = run.index[0] + (run.index[-1] - run.index[0]) / 2
            ax.text(mid, 10, text["band"], rotation=90, ha="center", va="center",
                    fontsize=17, color=nm.COLORS["rose"])

    ax.fill_between(unrate.index, unrate, color=nm.COLORS["blue"], alpha=0.13)
    ax.plot(unrate.index, unrate, color=nm.COLORS["blue"], linewidth=2.9)

    ax.set_ylim(0, 17)
    ax.set_yticks(range(0, 17, 2))
    ax.yaxis.set_major_formatter(pct)
    ax.set_xlim(T("2019-01-01"), T("2026-01-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    peak = unrate.loc["2020"].idxmax()
    low = unrate.loc["2022":"2024"].idxmin()
    ax.annotate(text["peak"], xy=(peak, unrate.loc[peak]), xytext=(T("2020-08-01"), 14.6),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["start"], xy=(T("2020-02-01"), 3.5), xytext=(T("2019-01-20"), 5.7),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["low"], xy=(low, unrate.loc[low]), xytext=(T("2021-11-01"), 7.1),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["sahm"], xy=(T("2024-08-01"), unrate.loc["2024-08-01"]),
                xytext=(T("2023-06-01"), 10.6), fontsize=21, color=nm.COLORS["text"],
                va="center", ha="left", linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    ax.annotate(text["end"], xy=(unrate.index[-1], unrate.iloc[-1]), xytext=(T("2024-06-01"), 6),
                fontsize=21, color=nm.COLORS["text"], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["muted"], lw=1.4))
    nm.header(fig, text["title"])
    nm.footer(fig, text["note"])
    return fig

build_figure(unrate, recessions, LANG)'''


# ── Assemblage ───────────────────────────────────────────────────────────────

FIGURES = [
    dict(name="fig01-inflation",
         fig_fr="La carte du voyage : l'inflation, 2019-2025",
         fig_en="The map of the journey: inflation, 2019-2025",
         live=True, data=DATA_1, fig=FIG_1),
    dict(name="fig02-petrole",
         fig_fr="L'impensable : le pétrole à prix négatif (avril 2020)",
         fig_en="The unthinkable: negative oil prices (April 2020)",
         live=True, data=DATA_2, fig=FIG_2),
    dict(name="fig03-pib",
         fig_fr="Le choc, le V, la divergence : PIB réel, base 100 = fin 2019",
         fig_en="The shock, the V, the divergence: real GDP, 100 = end-2019",
         live=True, data=DATA_3, fig=FIG_3),
    dict(name="fig04-emplois-vacants",
         fig_fr="La surchauffe en un chiffre : postes vacants par chômeur",
         fig_en="Overheating in one number: job openings per unemployed",
         live=True, data=DATA_4, fig=FIG_4),
    dict(name="fig05-taux",
         fig_fr="L'escalier des taux : montée éclair, descente prudente",
         fig_en="The rate staircase: lightning climb, cautious descent",
         live=True, data=DATA_5, fig=FIG_5),
    dict(name="fig06-10ans",
         fig_fr="Le prix de l'argent : le rendement américain à 10 ans",
         fig_en="The price of money: the U.S. 10-year yield",
         live=True, data=DATA_6, fig=FIG_6),
    dict(name="fig07-chomage",
         fig_fr="Le soft landing en une courbe : le chômage américain",
         fig_en="The soft landing in one curve: U.S. unemployment",
         live=True, data=DATA_7, fig=FIG_7),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out8")
    nb_kit.build_all(META, DIR, FIGURES)
