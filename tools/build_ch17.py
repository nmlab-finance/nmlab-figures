#!/usr/bin/env python3
"""Génère les notebooks du chapitre 17 — Climat et macroéconomie.

Sources variées, souvent NON-FRED (température NASA, pertes Swiss Re, coûts IRENA,
réserves McGlade & Ekins) → données EMBARQUÉES (live=False, valeurs lues sur la
figure). Convention « strict » : une seule cellule code, fonctions typées + docstrings
— load_*() puis build_figure(...) -> Figure ; LABELS={"fr":…,"en":…} ; LANG.
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit


META = dict(
    num="17",
    title_fr="Climat et macroéconomie : risque physique, transition et croissance potentielle",
    title_en="Climate and Macroeconomics: Physical Risk, Transition and Potential Growth",
    slug_fr="climat-et-macroeconomie",
    slug_en="climate-and-macroeconomics",
)
DIR = "macro/17-climat-macroeconomie"


# ── Figure 01 — anomalie de température mondiale (NASA GISTEMP, embarquée) ─────

DATA_1 = '''def load_temperature() -> tuple[list[int], list[float]]:
    """Anomalie de température moyenne mondiale (°C, base 1951-1980), valeurs annuelles
    NASA GISTEMP v4 embarquées, de 1880 à 2024.
    Global mean temperature anomaly (NASA GISTEMP v4), annual, 1880-2024."""
    years = list(range(1880, 2025))
    anomaly = [
        -0.17, -0.09, -0.11, -0.17, -0.28, -0.33, -0.31, -0.36, -0.17, -0.10,
        -0.35, -0.22, -0.27, -0.31, -0.30, -0.23, -0.11, -0.11, -0.27, -0.17,
        -0.08, -0.15, -0.28, -0.37, -0.47, -0.26, -0.22, -0.39, -0.43, -0.48,
        -0.44, -0.44, -0.36, -0.34, -0.15, -0.14, -0.36, -0.46, -0.30, -0.28,
        -0.27, -0.19, -0.28, -0.26, -0.27, -0.22, -0.11, -0.22, -0.20, -0.36,
        -0.16, -0.09, -0.16, -0.29, -0.13, -0.20, -0.15, -0.03, -0.02, -0.02,
         0.13,  0.19,  0.07,  0.09,  0.20,  0.09, -0.07, -0.03, -0.11, -0.11,
        -0.17, -0.07,  0.01,  0.08, -0.13, -0.14, -0.19,  0.05,  0.06,  0.03,
        -0.03,  0.06,  0.04,  0.06, -0.20, -0.11, -0.06, -0.02, -0.08,  0.05,
         0.03, -0.08,  0.01,  0.16, -0.07, -0.01, -0.10,  0.18,  0.07,  0.16,
         0.26,  0.32,  0.14,  0.31,  0.16,  0.12,  0.18,  0.32,  0.39,  0.27,
         0.45,  0.41,  0.22,  0.23,  0.32,  0.45,  0.33,  0.46,  0.61,  0.38,
         0.39,  0.54,  0.63,  0.62,  0.54,  0.68,  0.64,  0.67,  0.54,  0.66,
         0.72,  0.61,  0.65,  0.68,  0.75,  0.90,  1.01,  0.92,  0.85,  0.98,
         1.02,  0.85,  0.89,  1.17,  1.28,
    ]
    return years, anomaly

years, anomaly = load_temperature()'''

FIG_1 = '''import numpy as np
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter

LABELS = {
    "fr": dict(
        title="Le fait physique, sans détour",
        sub="Température moyenne mondiale, écart à la moyenne 1951-1980",
        ylab="anomalie de température, °C (vs 1951-1980)",
        paris="≈ seuil de Paris : +1,5 °C vs préindustriel",
        peak="2024 : +1,28 °C\\n(année la plus chaude)",
        note="La base est 1951-1980 ; par rapport au préindustriel (1850-1900), ajoutez ≈ 0,3 °C — 2024 fut donc à\\n"
             "≈ +1,58 °C (OMM, Copernicus). Source : NASA GISTEMP v4."),
    "en": dict(
        title="The physical fact, plainly",
        sub="Global mean temperature, deviation from the 1951-1980 average",
        ylab="temperature anomaly, °C (vs 1951-1980)",
        paris="≈ Paris threshold: +1.5 °C vs pre-industrial",
        peak="2024: +1.28 °C\\n(warmest year on record)",
        note="The baseline is 1951-1980; versus pre-industrial (1850-1900), add ≈ 0.3 °C — so 2024 was\\n"
             "≈ +1.58 °C (WMO, Copernicus). Source: NASA GISTEMP v4."),
}

def build_figure(years: list[int], anomaly: list[float], lang: str) -> Figure:
    """Courbe de l'anomalie annuelle, seuil de Paris (dashed) et pic de 2024."""
    text = LABELS[lang]
    yr = np.array(years)
    an = np.array(anomaly)
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.112)
    ax.fill_between(yr, an, 0, where=an > 0, color=nm.COLORS["rose"], alpha=0.13, interpolate=True)
    ax.axhline(0, color=nm.COLORS["muted"], linewidth=1.5, alpha=0.85)
    ax.axhline(1.2, color=nm.COLORS["amber"], linestyle=(0, (7, 5)), linewidth=2.8)
    ax.plot(yr, an, color=nm.COLORS["rose"], linewidth=2.6)
    ax.scatter([yr[-1]], [an[-1]], s=90, color=nm.COLORS["rose"], zorder=5)
    ax.set_ylim(-0.55, 1.62)
    ax.set_yticks([-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(1878, 2028)
    ax.set_xticks(range(1880, 2021, 20))
    ax.text(1892, 1.30, text["paris"], fontsize=21.5, fontweight="bold",
            color=nm.COLORS["amber"], va="center")
    ax.annotate(text["peak"], xy=(yr[-1], an[-1]), xytext=(2000, 1.46),
                ha="center", va="center", fontsize=21.5, color=nm.COLORS["text"], linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=1.6))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(years, anomaly, LANG)'''


# ── Figure 02 — pertes assurées des catastrophes (Swiss Re / Munich Re) ───────

DATA_2 = '''def load_losses() -> list[float]:
    """Pertes assurées mondiales des catastrophes naturelles, corrigées de l'inflation
    (Md$) : moyenne annuelle des années 1980, des années 2000, puis 2024.
    Inflation-adjusted global insured catastrophe losses ($bn)."""
    return [10.0, 50.0, 137.0]

losses = load_losses()'''

FIG_2 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La facture arrive déjà",
        sub="Pertes assurées des catastrophes naturelles, corrigées de l'inflation",
        ylab="pertes assurées mondiales, milliards de dollars",
        cats=["années 1980\\n(moy./an)", "années 2000\\n(moy./an)", "2024"],
        value_labels=["10 Md$", "50 Md$", "137 Md$"],
        note="De 10 à 137 milliards par an en une génération. 2024 fut la 5ᵉ année d'affilée au-dessus de 100 milliards.\\n"
             "Sources : Munich Re (repère 1980s-2000s, via Carney 2015) ; Swiss Re Institute (2024)."),
    "en": dict(
        title="The bill is already coming due",
        sub="Insured losses from natural catastrophes, adjusted for inflation",
        ylab="global insured losses, billions of dollars",
        cats=["1980s\\n(avg./yr)", "2000s\\n(avg./yr)", "2024"],
        value_labels=["$10bn", "$50bn", "$137bn"],
        note="From $10 to $137 billion a year in one generation. 2024 was the 5th straight year above $100 billion.\\n"
             "Sources: Munich Re (1980s-2000s benchmark, via Carney 2015); Swiss Re Institute (2024)."),
}

def build_figure(losses: list[float], lang: str) -> Figure:
    """Trois barres : pertes moyennes des années 1980, 2000, puis le pic de 2024."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.10, bottom=0.20)
    ax.grid(axis="x", visible=False)
    positions = range(len(losses))
    colors = ["#c9d4e7", nm.COLORS["amber"], nm.COLORS["rose"]]
    ax.bar(positions, losses, width=0.62, color=colors, zorder=3)
    ax.set_ylim(0, 165)
    ax.set_yticks(range(0, 161, 20))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 2.6)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"], fontsize=21.5, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for pos, value, label in zip(positions, losses, text["value_labels"]):
        ax.annotate(label, (pos, value), xytext=(0, 16), textcoords="offset points",
                    ha="center", va="bottom", fontsize=34, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(losses, LANG)'''


# ── Figure 03 — coût des renouvelables 2010 vs 2023 (IRENA) ───────────────────

DATA_3 = '''def load_costs() -> tuple[list[float], list[float]]:
    """Coût moyen actualisé de l'électricité ($/MWh, LCOE), 2010 et 2023, pour le solaire
    photovoltaïque et l'éolien terrestre. Source : IRENA (2023).
    Levelized cost of electricity ($/MWh) in 2010 and 2023: solar PV and onshore wind."""
    cost_2010 = [460.0, 111.0]
    cost_2023 = [44.0, 33.0]
    return cost_2010, cost_2023

cost_2010, cost_2023 = load_costs()'''

FIG_3 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La transition n'est plus chère — elle est bon marché",
        sub="Coût moyen de l'électricité renouvelable dans le monde, 2010 contre 2023",
        ylab="coût de production, $ par MWh",
        cats=["Solaire\\nphotovoltaïque", "Éolien\\nterrestre"],
        legend=["2010", "2023"],
        drops=["−90 %", "−70 %"],
        note="Le solaire a chuté de 90 %, l'éolien de 70 %. Les batteries : −93 % depuis 2010. Le risque de transition\\n"
             "est aussi une opportunité. Source : IRENA, Renewable Power Generation Costs 2023."),
    "en": dict(
        title="The transition is no longer expensive — it's cheap",
        sub="Average cost of renewable electricity worldwide, 2010 versus 2023",
        ylab="cost of production, $ per MWh",
        cats=["Solar\\nphotovoltaic", "Onshore\\nwind"],
        legend=["2010", "2023"],
        drops=["−90%", "−70%"],
        note="Solar fell 90%, wind 70%. Batteries: −93% since 2010. The transition risk is also an\\n"
             "opportunity. Source: IRENA, Renewable Power Generation Costs 2023."),
}

def build_figure(cost_2010: list[float], cost_2023: list[float], lang: str) -> Figure:
    """Barres groupées : coût 2010 (gris) contre 2023 (bleu), solaire et éolien."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.axes(fig, left=0.088, bottom=0.215)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(cost_2010))
    width = 0.38
    ax.bar(x - width / 2, cost_2010, width, color="#c9d4e7", zorder=3, label=text["legend"][0])
    ax.bar(x + width / 2, cost_2023, width, color=nm.COLORS["blue"], zorder=3, label=text["legend"][1])
    ax.set_ylim(0, 520)
    ax.set_yticks(range(0, 501, 100))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks(x)
    ax.set_xticklabels(text["cats"], fontsize=22, color=nm.COLORS["muted"], linespacing=1.5)
    ax.tick_params(axis="x", length=0)
    for xi, v2010, v2023 in zip(x, cost_2010, cost_2023):
        ax.annotate(f"{v2010:.0f}", (xi - width / 2, v2010), xytext=(0, 12), textcoords="offset points",
                    ha="center", va="bottom", fontsize=27, fontweight="bold", color=nm.COLORS["text"])
        ax.annotate(f"{v2023:.0f}", (xi + width / 2, v2023), xytext=(0, 12), textcoords="offset points",
                    ha="center", va="bottom", fontsize=27, fontweight="bold", color=nm.COLORS["blue2"])
    for xi, drop in zip(x, text["drops"]):
        ax.text(xi + 0.02, 232, drop, ha="center", va="center",
                fontsize=34, fontweight="bold", color=nm.COLORS["rose"])
    ax.legend(loc="upper center", ncol=2, frameon=False, fontsize=22, labelcolor=nm.COLORS["muted"],
              handletextpad=0.6, columnspacing=2.2, bbox_to_anchor=(0.5, 1.0))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(cost_2010, cost_2023, LANG)'''


# ── Figure 04 — les trois risques de Carney (schéma à trois cartes) ───────────

DATA_4 = '''def risk_cards(lang: str) -> list[tuple[str, str, list[str]]]:
    """Les trois risques climatiques de Carney : (nom, couleur, lignes), localisés.
    Carney's three climate risks: (name, color, lines), localized."""
    if lang == "fr":
        return [
            ("Physique", nm.COLORS["rose"],
             ["les dommages directs :", "inondations, tempêtes,", "sécheresses"]),
            ("Transition", nm.COLORS["amber"],
             ["les actifs dévalorisés", "par le passage au", "bas-carbone"]),
            ("Responsabilité", nm.COLORS["blue"],
             ["les procès de ceux qui", "subissent contre ceux", "qu'ils jugent responsables"]),
        ]
    return [
        ("Physical", nm.COLORS["rose"],
         ["the direct damages:", "floods, storms,", "droughts"]),
        ("Transition", nm.COLORS["amber"],
         ["assets devalued", "by the shift to", "low-carbon"]),
        ("Liability", nm.COLORS["blue"],
         ["the lawsuits of those", "harmed against those", "they deem responsible"]),
    ]'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Trois risques, pas deux",
        sub="La grille de lecture de Mark Carney (Banque d'Angleterre, 2015)",
        punch="Le troisième — le risque de responsabilité — est presque toujours oublié.",
        quote="« Une fois le climat devenu un enjeu de stabilité financière, il pourrait déjà être trop tard. »"),
    "en": dict(
        title="Three risks, not two",
        sub="Mark Carney's framework (Bank of England, 2015)",
        punch="The third — liability risk — is almost always forgotten.",
        quote="« Once climate becomes a financial-stability issue, it may already be too late. »"),
}

def build_figure(cards: list[tuple[str, str, list[str]]], lang: str) -> Figure:
    """Schéma : trois cartes (physique, transition, responsabilité) + phrase et citation."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.blank_axes(fig)
    card_w, gap, x0 = 486, 94, 55
    top, bottom = 760, 305
    for i, (name, color, lines) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        nm.card(ax, x, bottom, card_w, top - bottom, edge=color, lw=2.6, radius=24)
        ax.text(cx, top - 62, name, ha="center", va="center",
                fontsize=31, fontweight="bold", color=color)
        for j, line in enumerate(lines):
            ax.text(cx, 542 - j * 46, line, ha="center", va="center",
                    fontsize=26, color=nm.COLORS["text"])
    ax.text(nm.WIDTH_PX / 2, 205, text["punch"], ha="center", va="center",
            fontsize=27, fontweight="bold", color=nm.COLORS["text"])
    ax.text(nm.WIDTH_PX / 2, 108, text["quote"], ha="center", va="center",
            fontsize=23, style="italic", color=nm.COLORS["muted"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig)
    return fig

build_figure(risk_cards(LANG), LANG)'''


# ── Figure 05 — la fourchette des coûts (barres horizontales) ─────────────────

DATA_5 = '''def cost_estimates(lang: str) -> list[tuple[str, float, str]]:
    """Estimations de perte de revenu/PIB dues au climat : (libellé, valeur %, type).
    Horizons et bases NON comparables. Kotz 2024 rétracté en décembre 2025.
    Climate income/GDP-loss estimates (libellé, value %, kind); non-comparable."""
    if lang == "fr":
        labels = ["Nordhaus (DICE), à +3 °C", "Kotz et al. 2024, d'ici 2049",
                  "Burke et al., d'ici 2100", "NGFS, d'ici 2100"]
    else:
        labels = ["Nordhaus (DICE), at +3 °C", "Kotz et al. 2024, by 2049",
                  "Burke et al., by 2100", "NGFS, by 2100"]
    values = [2.1, 19.0, 23.0, 30.0]
    kinds = ["blue", "retracted", "amber", "rose"]
    return list(zip(labels, values, kinds))'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le coût du climat : un facteur dix d'écart",
        sub="Estimations de perte de revenu ou de PIB — horizons et bases NON comparables",
        xlab="perte de revenu / PIB estimée, %",
        retracted="RÉTRACTÉ",
        fmt=lambda v: f"{v:.1f} %".replace(".", ","),
        note="Ces chiffres ne se comparent pas terme à terme (horizons et références différents) : c'est justement le\\n"
             "problème. Le plus cité (Kotz, −19 %) a été RÉTRACTÉ en décembre 2025. Sources : Nordhaus, Burke et al., NGFS."),
    "en": dict(
        title="The cost of climate: a tenfold spread",
        sub="Estimates of income or GDP loss — NON-comparable horizons and baselines",
        xlab="estimated income / GDP loss, %",
        retracted="RETRACTED",
        fmt=lambda v: f"{v:.1f}%",
        note="These figures don't compare term for term (different horizons and baselines): that is exactly the\\n"
             "problem. The most-cited (Kotz, −19%) was RETRACTED in December 2025. Sources: Nordhaus, Burke et al., NGFS."),
}

def build_figure(rows: list[tuple[str, float, str]], lang: str) -> Figure:
    """Barres horizontales : quatre estimations ; celle de Kotz, rétractée, est hachurée."""
    text = LABELS[lang]
    palette = {"blue": nm.COLORS["blue"], "amber": nm.COLORS["amber"], "rose": nm.COLORS["rose"]}
    fig = nm.figure(height_px=1102)
    ax = nm.axes(fig, left=0.30, right=0.965, bottom=0.17)
    ax.grid(axis="y", visible=False)
    n = len(rows)
    ypos = list(range(n - 1, -1, -1))                 # première ligne en haut
    for y, (label, value, kind) in zip(ypos, rows):
        if kind == "retracted":
            ax.barh(y, value, height=0.62, color=nm.COLORS["edge"], edgecolor=nm.COLORS["muted"],
                    hatch="///", linewidth=1.6, zorder=3)
            ax.text(value / 2, y, text["retracted"], ha="center", va="center",
                    fontsize=22, fontweight="bold", color=nm.COLORS["rose"], zorder=4)
        else:
            ax.barh(y, value, height=0.62, color=palette[kind], zorder=3)
        ax.annotate(text["fmt"](value), (value, y), xytext=(14, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=30, fontweight="bold", color=nm.COLORS["text"])
    ax.set_xlim(0, 34)
    ax.set_xticks(range(0, 31, 5))
    ax.set_xlabel(text["xlab"])
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_yticks(ypos)
    ax.set_yticklabels([r[0] for r in rows], fontsize=21.5, color=nm.COLORS["muted"])
    ax.tick_params(axis="y", length=0)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(cost_estimates(LANG), LANG)'''


# ── Figure 06 — le carbone imbrûlable (barres empilées) ───────────────────────

DATA_6 = '''def load_reserves() -> tuple[list[float], list[float]]:
    """Réserves fossiles connues (%) réparties en part « brûlable » (< 2 °C) et part
    à laisser sous terre — pétrole, gaz, charbon. Source : McGlade & Ekins, Nature (2015).
    Known fossil reserves (%) split into a burnable and a leave-underground share."""
    burnable = [67.0, 50.0, 18.0]
    underground = [100.0 - b for b in burnable]
    return burnable, underground

burnable, underground = load_reserves()'''

FIG_6 = '''import numpy as np
from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le carbone imbrûlable",
        sub="Part des réserves fossiles à laisser sous terre pour rester sous 2 °C",
        ylab="part des réserves connues, %",
        cats=["Pétrole", "Gaz", "Charbon"],
        legend=["brûlable (< 2 °C)", "à laisser sous terre"],
        fracs=["1/3", "1/2", "> 80 %"],
        note="Pour une chance de rester sous 2 °C : un tiers du pétrole, la moitié du gaz, plus de 80 % du charbon doivent\\n"
             "rester sous terre — des réserves comptées à pleine valeur dans les bilans. Source : McGlade & Ekins, Nature 2015."),
    "en": dict(
        title="Unburnable carbon",
        sub="Share of fossil reserves to leave underground to stay below 2 °C",
        ylab="share of known reserves, %",
        cats=["Oil", "Gas", "Coal"],
        legend=["burnable (< 2 °C)", "leave underground"],
        fracs=["1/3", "1/2", "> 80%"],
        note="For a chance to stay below 2 °C: a third of oil, half of gas, over 80% of coal must stay\\n"
             "underground — reserves carried at full value on balance sheets. Source: McGlade & Ekins, Nature 2015."),
}

def build_figure(burnable: list[float], underground: list[float], lang: str) -> Figure:
    """Barres empilées : part brûlable (bleu) et part à laisser sous terre (gris)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1083)
    ax = nm.axes(fig, left=0.085, bottom=0.165)
    ax.grid(axis="x", visible=False)
    x = np.arange(len(burnable))
    ax.bar(x, burnable, width=0.6, color=nm.COLORS["blue"], zorder=3, label=text["legend"][0])
    ax.bar(x, underground, width=0.6, bottom=burnable, color="#c9d4e7", zorder=3, label=text["legend"][1])
    ax.set_ylim(0, 105)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(-0.65, 2.65)
    ax.set_xticks(x)
    ax.set_xticklabels(text["cats"], fontsize=28, color=nm.COLORS["text"])
    ax.tick_params(axis="x", length=0)
    for xi, b, frac in zip(x, burnable, text["fracs"]):
        ax.text(xi, b + (100 - b) / 2, frac, ha="center", va="center",
                fontsize=34, fontweight="bold", color=nm.COLORS["bg"])
    ax.legend(loc="lower center", ncol=2, frameon=False, fontsize=21, labelcolor=nm.COLORS["muted"],
              handletextpad=0.6, columnspacing=2.4, bbox_to_anchor=(0.5, 1.02))
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(burnable, underground, LANG)'''


# ── Assemblage ───────────────────────────────────────────────────────────────

FIGURES = [
    dict(name="fig01-temperature", fig_fr="Le fait physique, sans détour",
         fig_en="The physical fact, plainly", live=False, data=DATA_1, fig=FIG_1),
    dict(name="fig02-pertes-assurees", fig_fr="La facture arrive déjà",
         fig_en="The bill is already coming due", live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-cout-renouvelables", fig_fr="La transition n'est plus chère — elle est bon marché",
         fig_en="The transition is no longer expensive — it's cheap", live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-trois-risques", fig_fr="Trois risques, pas deux",
         fig_en="Three risks, not two", live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-fourchette-couts", fig_fr="Le coût du climat : un facteur dix d'écart",
         fig_en="The cost of climate: a tenfold spread", live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-carbone-imbrulable", fig_fr="Le carbone imbrûlable",
         fig_en="Unburnable carbon", live=False, data=DATA_6, fig=FIG_6),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out17")
    nb_kit.build_all(META, DIR, FIGURES)
