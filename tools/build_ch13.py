#!/usr/bin/env python3
"""Notebooks Colab du chapitre 13 — IA, automatisation et productivité.

Importe la boîte à outils ``nb_kit`` (format META + liste FIGURES) et écrit
un notebook par figure dans le miroir ``nmlab-figures``. Convention « stricte » :
une seule cellule code, fonctions typées + docstrings (voir ch18/19/20).
"""

import sys

sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="13",
    title_fr="IA, automatisation et productivité : un nouveau moteur de croissance ?",
    title_en="AI, Automation and Productivity: A New Engine of Growth?",
    slug_fr="ia-automatisation-productivite",
    slug_en="ai-automation-and-productivity",
)
DIR = "macro/13-ia-automatisation-productivite"

PALE = "#c9d4e7"   # barre « contexte » (avant / autres), façon ch20 fig02


# ── Figure 01 — la productivité a accéléré (FRED OPHNFB, en direct) ───────────

DATA_01 = '''from pandas import Series

def load_productivity() -> Series:
    """Productivité horaire (OPHNFB, entreprises non agricoles) en glissement annuel.
    Labor productivity, year-over-year. pct_change(4) car la série est trimestrielle.
    U.S. labor productivity, live from FRED; year-over-year since the series is quarterly."""
    level = nm.load_fred("OPHNFB")
    return (level.pct_change(4) * 100).loc["2010":]

productivity = load_productivity()'''

FIG_01 = '''import matplotlib.dates as mdates
import pandas as pd
from matplotlib.figure import Figure

PALE = "#c9d4e7"   # ligne « moyenne 2011-2019 », teinte pâle

LABELS = {
    "fr": dict(
        title="La productivité a bel et bien accéléré",
        sub="Production par heure travaillée, entreprises non agricoles américaines",
        ylab="productivité horaire, glissement annuel %",
        chatgpt="ChatGPT\\nnov. 2022",
        note="Le rythme a plus que doublé depuis 2023. Mais l'accélération démarre quand moins de 10 % des grandes\\n"
             "entreprises envisageaient encore d'utiliser l'IA : dater n'est pas attribuer. Source : BLS (OPHNFB)."),
    "en": dict(
        title="Productivity really did accelerate",
        sub="Output per hour worked, U.S. nonfarm business",
        ylab="labor productivity, year over year %",
        chatgpt="ChatGPT\\nNov. 2022",
        note="The pace more than doubled since 2023. But the acceleration begins when fewer than 10% of large firms\\n"
             "still planned to use AI: dating is not attributing. Source: BLS (OPHNFB)."),
}

def averages(productivity: Series) -> tuple[float, float]:
    """Moyennes de glissement annuel : 2011-2019, puis depuis 2023 / period averages."""
    return productivity.loc["2011":"2019"].mean(), productivity.loc["2023":].mean()

def avg_label(value: float, lang: str, period_fr: str, period_en: str) -> str:
    """Libellé « moyenne … : X,XX % » localisé (virgule décimale en français)."""
    if lang == "fr":
        return f"moyenne {period_fr} : {value:.2f} %".replace(".", ",")
    return f"{period_en} average: {value:.2f}%"

def build_figure(productivity: Series, lang: str) -> Figure:
    """Glissement annuel de la productivité, ses deux moyennes et le repère ChatGPT."""
    text = LABELS[lang]
    avg_pre, avg_post = averages(productivity)
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig)

    ax.plot(productivity.index, productivity, color=nm.COLORS["blue"], linewidth=2.9, zorder=3)
    ax.axhline(0, color=nm.COLORS["muted"], linewidth=1.7, alpha=0.9)

    # Repère vertical : sortie de ChatGPT (novembre 2022).
    chatgpt = pd.Timestamp("2022-11-01")
    ax.axvline(chatgpt, color=nm.COLORS["rose"], linestyle=(0, (1, 3)), linewidth=2.4)
    ax.text(pd.Timestamp("2022-06-01"), -2.55, text["chatgpt"], ha="right", va="center",
            fontsize=21, color=nm.COLORS["rose"], linespacing=1.4)

    # Moyenne 2011-2019 (pâle) et moyenne depuis 2023 (ambre).
    ax.plot([pd.Timestamp("2010-07-01"), pd.Timestamp("2020-03-01")], [avg_pre, avg_pre],
            color=PALE, linestyle=(0, (6, 4)), linewidth=3.2)
    ax.plot([pd.Timestamp("2023-01-01"), productivity.index[-1]], [avg_post, avg_post],
            color=nm.COLORS["amber"], linestyle=(0, (6, 4)), linewidth=3.4)
    ax.text(pd.Timestamp("2015-06-01"), 1.45,
            avg_label(avg_pre, lang, "2011-2019", "2011-2019"),
            ha="center", va="bottom", fontsize=22, fontweight="bold", color=PALE)
    if lang == "fr":
        post_lines = f"moyenne\\ndepuis 2023 :\\n{avg_post:.2f} %".replace(".", ",")
    else:
        post_lines = f"average\\nsince 2023:\\n{avg_post:.2f}%"
    ax.text(pd.Timestamp("2024-06-01"), 3.7, post_lines, ha="center", va="center",
            fontsize=23, fontweight="bold", color=nm.COLORS["amber"], linespacing=1.55)

    ax.set_ylim(-4, 6.2)
    ax.set_yticks(range(-4, 7, 2))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(pd.Timestamp("2010-01-01"), pd.Timestamp("2026-06-01"))
    ax.xaxis.set_major_locator(mdates.YearLocator(2, month=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(productivity, LANG)'''


# ── Figure 02 — le chiffre qui affole, remis à l'échelle (embarqué, log) ──────

DATA_02 = '''def layoffs() -> tuple[list[float], list[float]]:
    """Deux ordres de grandeur, en emplois par mois : suppressions « attribuées à l'IA »
    (101 743 sur le 1er semestre 2026, Challenger, soit 16 957/mois) contre licenciements
    RÉELS (1,7 million/mois, JOLTS, mai 2026). Valeurs embarquées (schéma éditable).
    Jobs per month: AI-attributed announcements vs real layoffs. Source: Challenger; BLS (JOLTS)."""
    positions = [0, 1]
    values = [16_957, 1_700_000]
    return positions, values

positions, values = layoffs()'''

FIG_02 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le chiffre qui affole, remis à l'échelle",
        sub="Suppressions annoncées « à cause de l'IA » et licenciements effectivement enregistrés",
        ylab="nombre d'emplois (échelle log)",
        cats=["Annonces\\n« attribuées à l'IA »\\n(par mois, S1 2026)", "Licenciements RÉELS\\n(par mois, mai 2026)"],
        value_labels=["16 957", "1 700 000"],
        ratio="environ 1 %",
        note="Les 101 743 suppressions attribuées à l'IA au premier semestre 2026 pèsent environ 1 % des licenciements\\n"
             "réels. Et ce sont des ANNONCES, avec la raison DÉCLARÉE par l'employeur. Sources : Challenger ; BLS (JOLTS)."),
    "en": dict(
        title="The alarming figure, put back to scale",
        sub="Announced cuts « because of AI » and layoffs actually recorded",
        ylab="number of jobs (log scale)",
        cats=["Announcements\\n« attributed to AI »\\n(per month, H1 2026)", "REAL layoffs\\n(per month, May 2026)"],
        value_labels=["16,957", "1,700,000"],
        ratio="about 1%",
        note="The 101,743 cuts attributed to AI in the first half of 2026 weigh about 1% of real layoffs. And these\\n"
             "are ANNOUNCEMENTS, with the reason DECLARED by the employer. Sources: Challenger; BLS (JOLTS)."),
}

def build_figure(positions: list[float], values: list[float], lang: str) -> Figure:
    """Deux barres à l'échelle logarithmique : l'annonce IA face aux licenciements réels."""
    text = LABELS[lang]
    base = 6_000
    fig = nm.figure(height_px=1140)
    ax = nm.axes(fig, left=0.135, bottom=0.27)
    ax.set_yscale("log")
    ax.grid(axis="x", visible=False)
    ax.grid(which="minor", visible=False)
    ax.bar(positions, [v - base for v in values], width=0.62, bottom=base,
           color=[nm.COLORS["amber"], nm.COLORS["blue"]], zorder=3)
    ax.set_ylim(base, 4.5e6)
    ax.set_yticks([10_000, 100_000, 1_000_000])
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.tick_params(which="minor", left=False)
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(positions)
    ax.set_xticklabels(text["cats"], fontsize=21, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, values, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 15), textcoords="offset points",
                    ha="center", va="bottom", fontsize=32, fontweight="bold", color=nm.COLORS["text"])
    # Flèche double : « environ 1 % » entre les deux sommets.
    ax.annotate("", xy=(1, 1.45e6), xytext=(0, 1.45e6),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["rose"], lw=2.2))
    ax.text(0.5, 2.5e6, text["ratio"], ha="center", va="center",
            fontsize=30, fontweight="bold", color=nm.COLORS["rose"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(positions, values, LANG)'''


# ── Figure 03 — l'IA vs la bulle internet (embarqué, 2 barres) ────────────────

DATA_03 = f'''def it_share() -> list[float]:
    """Part de la croissance du PIB américain due à l'investissement en informatique
    et logiciels : 28 % en 2000 (bulle internet) contre 39 % en 2025 (IA). Même méthode,
    deux époques. Valeurs embarquées. Source : Federal Reserve Bank of St. Louis (2026)."""
    return [28, 39]

shares = it_share()'''

FIG_03 = f'''from matplotlib.figure import Figure

PALE = "{PALE}"

LABELS = {{
    "fr": dict(
        title="L'IA pèse déjà plus lourd que la bulle internet",
        sub="Part de la croissance du PIB américain due à l'investissement en informatique et logiciels",
        ylab="part de la croissance du PIB, %",
        cats=["2000\\n(bulle internet)", "2025\\n(IA)"],
        value_labels=["28 %", "39 %"],
        note="Même méthode, mêmes catégories, deux époques : la seule comparaison du dossier qui soit vraiment terme à\\n"
             "terme. Source : Federal Reserve Bank of St. Louis (12 janvier 2026)."),
    "en": dict(
        title="AI already weighs more than the dot-com bubble",
        sub="Share of U.S. GDP growth from investment in computers and software",
        ylab="share of GDP growth, %",
        cats=["2000\\n(dot-com bubble)", "2025\\n(AI)"],
        value_labels=["28%", "39%"],
        note="Same method, same categories, two eras: the only truly term-for-term comparison in the file.\\n"
             "Source: Federal Reserve Bank of St. Louis (January 12, 2026)."),
}}

def build_figure(shares: list[float], lang: str) -> Figure:
    """Deux barres : la part informatique de la croissance en 2000 contre 2025."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1083)
    ax = nm.axes(fig, left=0.10, bottom=0.20)
    ax.grid(axis="x", visible=False)
    positions = range(len(shares))
    ax.bar(positions, shares, width=0.60, color=[PALE, nm.COLORS["blue"]], zorder=3)
    ax.set_ylim(0, 44)
    ax.set_yticks(range(0, 41, 10))
    ax.yaxis.set_major_formatter(nm.thousands(lang))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, share, label in zip(positions, shares, text["value_labels"]):
        ax.annotate(label, (pos, share), xytext=(0, 15), textcoords="offset points",
                    ha="center", va="bottom", fontsize=36, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(shares, LANG)'''


# ── Figure 04 — le taux censé avoir doublé la productivité (embarqué) ─────────

DATA_04 = '''def adoption() -> list[float]:
    """Part des grandes entreprises américaines déclarant utiliser l'IA : moins de 10 %
    au 4e trimestre 2023, 12 % au 3e trimestre 2025 (U.S. Census Bureau, BTOS).
    Valeurs embarquées ; la 1re barre vaut 9 (« moins de 10 % »). Embedded values."""
    return [9, 12]

adoption_rates = adoption()'''

FIG_04 = f'''from matplotlib.figure import Figure

PALE = "{PALE}"

LABELS = {{
    "fr": dict(
        title="Le taux censé avoir doublé la productivité",
        sub="Part des grandes entreprises américaines déclarant utiliser l'IA",
        ylab="part des grandes entreprises utilisant l'IA, %",
        cats=["4ᵉ trim. 2023", "3ᵉ trim. 2025"],
        value_labels=["< 10 %", "12 %"],
        scale="100 % = toutes les grandes entreprises",
        note="Quand la productivité accélère, en 2023, moins d'une grande entreprise sur dix envisage même d'utiliser\\n"
             "l'IA ; deux ans plus tard, 12 %. Dater n'est pas attribuer. Source : U.S. Census Bureau (BTOS)."),
    "en": dict(
        title="The rate supposed to have doubled productivity",
        sub="Share of large U.S. firms reporting they use AI",
        ylab="share of large firms using AI, %",
        cats=["Q4 2023", "Q3 2025"],
        value_labels=["< 10%", "12%"],
        scale="100% = every large firm",
        note="When productivity accelerates, in 2023, fewer than one large firm in ten even plans to use AI;\\n"
             "two years later, 12%. Dating is not attributing. Source: U.S. Census Bureau (BTOS)."),
}}

def build_figure(adoption_rates: list[float], lang: str) -> Figure:
    """Deux petites barres, sous une ligne pointillée « 100 % = toutes les entreprises »."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.11, bottom=0.17)
    ax.grid(axis="x", visible=False)
    positions = range(len(adoption_rates))
    ax.bar(positions, adoption_rates, width=0.42, color=[PALE, nm.COLORS["blue"]], zorder=3)
    ax.axhline(100, color=nm.COLORS["muted"], linestyle=(0, (6, 4)), linewidth=2.2)
    ax.text(0.5, 94, text["scale"], ha="center", va="top", fontsize=22, color=nm.COLORS["muted"])
    ax.set_ylim(0, 108)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=22, color=nm.COLORS["muted"])
    ax.tick_params(axis="x", length=0)
    for pos, rate, label in zip(positions, adoption_rates, text["value_labels"]):
        ax.annotate(label, (pos, rate), xytext=(0, 14), textcoords="offset points",
                    ha="center", va="bottom", fontsize=34, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(adoption_rates, LANG)'''


# ── Figure 05 — six études, une même prudence (schéma) ────────────────────────

DATA_05 = '''def studies(lang: str) -> list[tuple[str, str, str]]:
    """Les six travaux du dossier : (nom, couleur de la pastille, résultat en une ligne).
    Ambre = seule étude à voir un déclin ; rose = l'explication concurrente ; bleu = aucun
    effet agrégé. The six works: (name, dot color, one-line finding), localized."""
    if lang == "fr":
        return [
            ("Stanford (Brynjolfsson)", nm.COLORS["amber"], "−16 % relatif (6 % brut) — n'établit pas la causalité"),
            ("Yale Budget Lab", nm.COLORS["blue"], "aucun impact visible — mais « trop peu puissant »"),
            ("Réserve fédérale", nm.COLORS["blue"], "aucune baisse des offres là où l'IA est adoptée"),
            ("NBER (≈750 dirigeants)", nm.COLORS["blue"], "peu de preuves d'un déclin agrégé — réallocation"),
            ("Anthropic", nm.COLORS["blue"], "aucune hausse du chômage des exposés"),
            ("Google / EIG", nm.COLORS["rose"], "le déclin des juniors commence avant ChatGPT"),
        ]
    return [
        ("Stanford (Brynjolfsson)", nm.COLORS["amber"], "−16% relative (6% raw) — does not establish causality"),
        ("Yale Budget Lab", nm.COLORS["blue"], "no visible impact — but « underpowered »"),
        ("Federal Reserve", nm.COLORS["blue"], "no drop in postings where AI is adopted"),
        ("NBER (≈750 executives)", nm.COLORS["blue"], "little evidence of an aggregate decline — reallocation"),
        ("Anthropic", nm.COLORS["blue"], "no rise in unemployment among the exposed"),
        ("Google / EIG", nm.COLORS["rose"], "the junior decline starts before ChatGPT"),
    ]'''

FIG_05 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Six études, une même prudence",
        sub="Ce que trouvent réellement les travaux sur l'IA et l'emploi",
        headline="Convergence : aucun effet agrégé détectable à ce jour.",
        mechanism="S'il existe un effet, il passe par le RALENTISSEMENT DES EMBAUCHES, pas les licenciements."),
    "en": dict(
        title="Six studies, one shared caution",
        sub="What the research on AI and jobs actually finds",
        headline="Convergence: no aggregate effect detectable so far.",
        mechanism="If an effect exists, it works through SLOWER HIRING, not layoffs."),
}

def build_figure(rows: list[tuple[str, str, str]], lang: str) -> Figure:
    """Schéma : six études en liste (pastille + nom + résultat), puis l'encadré de synthèse."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1254)
    ax = nm.blank_axes(fig)

    dot_x, name_x = 132, 210
    top_name, step = 1052, 142
    for i, (name, color, finding) in enumerate(rows):
        name_y = top_name - i * step
        ax.scatter([dot_x], [name_y], s=540, color=color, zorder=3)
        ax.text(name_x, name_y, name, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        ax.text(name_x, name_y - 52, finding, ha="left", va="center",
                fontsize=25, color=nm.COLORS["muted"])

    # Encadré de synthèse (liseré ambre) : la conclusion partagée.
    box_x, box_w, box_y, box_h = 78, 1591, 38, 186
    center_x = box_x + box_w / 2
    nm.card(ax, box_x, box_y, box_w, box_h, edge=nm.COLORS["amber"], lw=2.6, radius=22)
    ax.text(center_x, box_y + box_h - 62, text["headline"], ha="center", va="center",
            fontsize=27, fontweight="bold", color=nm.COLORS["amber"])
    ax.text(center_x, box_y + 68, text["mechanism"], ha="center", va="center",
            fontsize=24, color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig)
    return fig

build_figure(studies(LANG), LANG)'''


# ── Figure 06 — le crédit privé se rue sur l'IA (embarqué, deux panneaux) ─────

DATA_06 = '''def credit() -> tuple[list[float], list[float]]:
    """Deux mesures du crédit privé à l'IA (BRI, janv. 2026), embarquées :
    encours des prêts (≈ 0 en 2023, > 200 Md$ en 2026) et marge de risque exigée
    (6,2 points pour les prêts IA, 6,1 pour les autres). Embedded values."""
    outstanding = [3, 205]            # 2023 ≈ 0, 2026 > 200 Md$
    spreads = [6.2, 6.1]              # prêts IA, autres — quasi identiques
    return outstanding, spreads

outstanding, spreads = credit()'''

FIG_06 = f'''from matplotlib.figure import Figure

PALE = "{PALE}"

LABELS = {{
    "fr": dict(
        title="Le crédit privé se rue sur l'IA — au même prix que tout le reste",
        sub="Encours des prêts privés aux entreprises de l'IA, et marge de risque exigée",
        ylab_left="prêts privés aux entreprises de l'IA",
        ylab_right="marge exigée, points",
        cats_left=["2023", "2026"],
        cats_right=["prêts IA", "autres"],
        labels_left=["≈ 0", "> 200 Md$"],
        labels_right=["6,2", "6,1"],
        share="part du crédit privé : < 1 %  →  ~8 %",
        same="quasi identiques",
        note="De presque rien à plus de 200 milliards, à des marges quasi identiques au reste : « soit les prêteurs\\n"
             "sous-estiment le risque, soit les marchés surestiment les flux futurs » (BRI). Source : BRI (janv. 2026)."),
    "en": dict(
        title="Private credit rushes into AI — at the same price as everything else",
        sub="Outstanding private loans to AI firms, and the risk spread demanded",
        ylab_left="private loans to AI firms",
        ylab_right="spread demanded, points",
        cats_left=["2023", "2026"],
        cats_right=["AI loans", "others"],
        labels_left=["≈ 0", "> $200 bn"],
        labels_right=["6.2", "6.1"],
        share="share of private credit: < 1%  →  ~8%",
        same="nearly identical",
        note="From almost nothing to more than 200 billion, at spreads nearly identical to the rest: « either lenders\\n"
             "underestimate the risk, or markets overestimate future flows » (BIS). Source: BIS (Jan. 2026)."),
}}

def build_figure(outstanding: list[float], spreads: list[float], lang: str) -> Figure:
    """Deux panneaux : l'encours (à gauche) qui explose, la marge (à droite) qui ne bouge pas."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1121)
    left = fig.add_axes([0.075, 0.225, 0.505, 0.515])
    right = fig.add_axes([0.665, 0.225, 0.315, 0.515])

    # Panneau gauche : l'encours des prêts privés à l'IA.
    positions = range(2)
    left.grid(axis="x", visible=False)
    left.bar(positions, outstanding, width=0.5, color=[PALE, nm.COLORS["blue"]], zorder=3)
    left.set_ylim(0, 232)
    left.set_yticks(range(0, 201, 50))
    left.set_ylabel(text["ylab_left"])
    left.set_xlim(-0.6, 1.6)
    left.set_xticks(list(positions))
    left.set_xticklabels(text["cats_left"], fontsize=22, color=nm.COLORS["muted"])
    left.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, outstanding, text["labels_left"]):
        left.annotate(label, (pos, value), xytext=(0, 14), textcoords="offset points",
                      ha="center", va="bottom", fontsize=32, fontweight="bold", color=nm.COLORS["text"])
    fig.text(0.325, 0.115, text["share"], ha="center", va="center",
             fontsize=21, color=nm.COLORS["muted"])

    # Panneau droit : la marge de risque exigée.
    right.grid(axis="x", visible=False)
    right.bar(positions, spreads, width=0.62, color=[nm.COLORS["blue"], PALE], zorder=3)
    right.set_ylim(0, 7.5)
    right.set_yticks(range(0, 8))
    right.set_ylabel(text["ylab_right"])
    right.set_xlim(-0.6, 1.6)
    right.set_xticks(list(positions))
    right.set_xticklabels(text["cats_right"], fontsize=22, color=nm.COLORS["muted"])
    right.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, spreads, text["labels_right"]):
        right.annotate(label, (pos, value), xytext=(0, 12), textcoords="offset points",
                       ha="center", va="bottom", fontsize=30, fontweight="bold", color=nm.COLORS["text"])
    right.text(0.5, 7.15, text["same"], ha="center", va="center",
               fontsize=24, fontweight="bold", color=nm.COLORS["amber"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(outstanding, spreads, LANG)'''


FIGURES = [
    dict(name="fig01-productivite-acceleration",
         fig_fr="La productivité a bel et bien accéléré", fig_en="Productivity really did accelerate",
         live=True, data=DATA_01, fig=FIG_01),
    dict(name="fig02-attribue-vs-reel",
         fig_fr="Le chiffre qui affole, remis à l'échelle", fig_en="The alarming figure, put back to scale",
         live=False, data=DATA_02, fig=FIG_02),
    dict(name="fig03-ia-vs-dotcom",
         fig_fr="L'IA pèse déjà plus lourd que la bulle internet",
         fig_en="AI already weighs more than the dot-com bubble",
         live=False, data=DATA_03, fig=FIG_03),
    dict(name="fig04-adoption-ia",
         fig_fr="Le taux censé avoir doublé la productivité",
         fig_en="The rate supposed to have doubled productivity",
         live=False, data=DATA_04, fig=FIG_04),
    dict(name="fig05-paysage-etudes",
         fig_fr="Six études, une même prudence", fig_en="Six studies, one shared caution",
         live=False, data=DATA_05, fig=FIG_05),
    dict(name="fig06-credit-prive",
         fig_fr="Le crédit privé se rue sur l'IA — au même prix que tout le reste",
         fig_en="Private credit rushes into AI — at the same price as everything else",
         live=False, data=DATA_06, fig=FIG_06),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out13")
    nb_kit.build_all(META, DIR, FIGURES)
