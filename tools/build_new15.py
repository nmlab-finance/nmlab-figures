#!/usr/bin/env python3
"""Notebooks des 15 figures ajoutées (harmonisation du rythme visuel, ch. 12-20).

Chaque figure existe déjà dans ~/cms-workspace/newfigs/figs_{a,b,c}.py ; ce script
en extrait le code sous la convention « stricte » du dépôt : une seule cellule,
load_*() typée puis build_figure(...) -> Figure, LABELS bilingue.
"""
import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

CH = {
 "12": dict(num="12", title_fr="Productivité et croissance de long terme : la variable qui décide de tout",
            title_en="Productivity and Long-Run Growth: The Variable That Decides Everything",
            slug_fr="productivite-et-croissance-long-terme", slug_en="productivity-and-long-term-growth",
            dir="macro/12-productivite-croissance-long-terme"),
 "13": dict(num="13", title_fr="IA, automatisation et productivité : un nouveau moteur de croissance ?",
            title_en="AI, Automation and Productivity: A New Engine of Growth?",
            slug_fr="ia-automatisation-productivite", slug_en="ai-automation-and-productivity",
            dir="macro/13-ia-automatisation-productivite"),
 "14": dict(num="14", title_fr="Démographie et croissance : comment la population façonne l'économie",
            title_en="Demography and Growth: How Population Shapes the Economy",
            slug_fr="demographie-et-croissance", slug_en="demography-and-growth",
            dir="macro/14-demographie-et-croissance"),
 "15": dict(num="15", title_fr="Croissance potentielle et output gap : la carte que personne ne peut mesurer",
            title_en="Potential Growth and the Output Gap: The Map No One Can Measure",
            slug_fr="croissance-potentielle-et-output-gap", slug_en="potential-growth-and-output-gap",
            dir="macro/15-croissance-potentielle"),
 "16": dict(num="16", title_fr="Épargne et investissement : les deux moteurs du financement de l'économie",
            title_en="Saving and Investment: The Two Engines Financing the Economy",
            slug_fr="epargne-et-investissement", slug_en="saving-and-investment",
            dir="macro/16-epargne-investissement"),
 "17": dict(num="17", title_fr="Climat et macroéconomie : risque physique, transition et croissance potentielle",
            title_en="Climate and Macroeconomics: Physical Risk, Transition and Potential Growth",
            slug_fr="climat-et-macroeconomie", slug_en="climate-and-macroeconomics",
            dir="macro/17-climat-macroeconomie"),
 "18": dict(num="18", title_fr="Atelier données : découvrir FRED, l'entrepôt de la Réserve fédérale",
            title_en="Data Workshop: Discovering FRED, the Federal Reserve's Warehouse",
            slug_fr="atelier-donnees-decouvrir-fred", slug_en="data-workshop-discovering-fred",
            dir="macro/18-atelier-donnees-fred"),
 "19": dict(num="19", title_fr="Premier script Python : charger une série FRED et la tracer en dix lignes",
            title_en="Your First Python Script: Load a FRED Series and Plot It in Ten Lines",
            slug_fr="premier-script-python-fred", slug_en="first-python-script-fred",
            dir="macro/19-premier-script-python"),
 "20": dict(num="20", title_fr="La croissance déjà anticipée : pourquoi elle est souvent dans les cours",
            title_en="Growth Already Anticipated: Why It's Often Already in the Price",
            slug_fr="croissance-deja-anticipee-dans-les-cours", slug_en="growth-already-priced-in",
            dir="macro/20-croissance-deja-anticipee"),
}

HELPERS = '''from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

C, W = nm.COLORS, nm.WIDTH_PX


def wrap(ax, x: float, y: float, text: str, *, size: float = 19, color: str | None = None,
         weight: int = 500, ha: str = "left", va: str = "top", width: int = 42,
         lh: float = 1.5) -> int:
    """Écrit un texte replié à ``width`` caractères (coordonnées pixels)."""
    import textwrap
    lines: list[str] = []
    for para in text.split("\\n"):
        lines += textwrap.wrap(para, width) or [""]
    ax.text(x, y, "\\n".join(lines), fontsize=size, color=color or C["muted"],
            fontweight=weight, ha=ha, va=va, linespacing=lh, zorder=5)
    return len(lines)


def start(height: int = 1010) -> Figure:
    """Figure NMLab au format du site : 1747 px de large, fond sombre."""
    fig = nm.figure(height_px=height)
    fig.patch.set_facecolor(C["bg"])
    return fig


def dec(v: float, lang: str, n: int = 1, sign: bool = False) -> str:
    """Formate un nombre à la française (virgule, moins typographique) ou à l'anglaise."""
    s = f"{v:+.{n}f}" if sign else f"{v:.{n}f}"
    return s.replace("-", "\u2212").replace(".", ",") if lang == "fr" else s'''
