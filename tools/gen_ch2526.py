#!/usr/bin/env python3
"""Notebooks Colab des 14 figures des chapitres 25 et 26.

Le code de production vit dans ~/cms-workspace/ch2526/figs.py et lit des CSV
locaux ; on le transpose ici en cellules autonomes qui rechargent les séries
depuis FRED (ou la BCE pour M3) — ou embarquent les points quand la source
n'est pas rejouable.
"""
import sys, os, re, inspect
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
sys.path.insert(0, "/home/claudeagent/cms-workspace/ch2526")
os.chdir("/home/claudeagent/cms-workspace/ch2526")
import nb_kit
import figs as F

META = {
 "25": dict(num="25", title_fr="Masse monétaire M1, M2 : ce que ces agrégats mesurent vraiment",
            title_en="Money Supply M1, M2: What These Aggregates Really Measure",
            slug_fr="masse-monetaire-m1-m2", slug_en="money-supply-m1-m2",
            dir="macro/25-masse-monetaire-m1-m2"),
 "26": dict(num="26", title_fr="La théorie quantitative de la monnaie (MV = PQ) : relier monnaie, prix et activité",
            title_en="The Quantity Theory of Money (MV = PQ): Linking Money, Prices and Activity",
            slug_fr="theorie-quantitative-monnaie-mv-pq", slug_en="quantity-theory-of-money",
            dir="macro/26-theorie-quantitative-monnaie"),
}

PRELUDE = '''import numpy as np
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

C, W = nm.COLORS, nm.WIDTH_PX

EA_M3_KEY = "BSI/M.U2.Y.V.M30.X.1.U2.2300.Z01.E"   # encours M3 zone euro (BCE)


def load(series_id: str, start: str | None = None, end: str | None = None) -> pd.Series:
    """Charge une série en direct : FRED, ou le portail de la BCE pour « EA_M3 »."""
    if series_id == "EA_M3":
        url = (f"https://data-api.ecb.europa.eu/service/data/{EA_M3_KEY}"
               "?format=csvdata&detail=dataonly")
        raw = pd.read_csv(url)
        s = pd.Series(raw["OBS_VALUE"].values,
                      index=pd.PeriodIndex(raw["TIME_PERIOD"], freq="M").to_timestamp())
        s = s.sort_index() / 1000.0                 # millions -> milliards d'euros
    else:
        s = nm.load_fred(series_id)
    return s.loc[start:end]


def T(d: dict, lang: str):
    """Sélectionne le jeu de libellés de la langue demandée."""
    return d[lang]'''

SPEC = [
 ("c25_01", "25", "fig01-saut-m1", "Le jour où M1 a triplé — sans un dollar de plus",
  "The day M1 tripled — without a single new dollar", True),
 ("c25_02", "25", "fig02-poupees-russes", "Les poupées russes de la monnaie",
  "The nesting dolls of money", False),
 ("c25_03", "25", "fig03-anatomie-m2", "L'anatomie de M2",
  "The anatomy of M2", True),
 ("c25_04", "25", "fig04-deux-continents", "Mêmes lettres, contenus différents",
  "Same letters, different contents", False),
 ("c25_05", "25", "fig05-frontieres-mouvantes", "Les frontières bougent",
  "The borders move", False),
 ("c25_06", "25", "fig06-dedans-dehors", "Où s'arrête la monnaie",
  "Where money stops", False),
 ("c25_07", "25", "fig07-agregats-respirent", "Les agrégats respirent",
  "The aggregates breathe", True),
 ("c26_01", "26", "fig01-equation-mvpq", "L'équation des échanges, décomposée",
  "The equation of exchange, unpacked", False),
 ("c26_02", "26", "fig02-identite", "L'identité qui ne peut pas être fausse",
  "The identity that cannot be false", False),
 ("c26_03", "26", "fig03-trois-verrous", "Les trois verrous",
  "The three locks", False),
 ("c26_04", "26", "fig04-monnaie-prix-long-terme", "Monnaie et prix sur le long terme",
  "Money and prices over the long run", True),
 ("c26_05", "26", "fig05-vitesse-m2", "Le maillon faible : la vitesse",
  "The weak link: velocity", True),
 ("c26_06", "26", "fig06-monetarisme", "Le monétarisme et sa défaite",
  "Monetarism and its defeat", False),
 ("c26_07", "26", "fig07-money-inflation-2020", "Quand l'équation reparle",
  "When the equation speaks again", True),
]


def cell_for(name):
    """Transpose une fonction figXX(lang) en cellule autonome build_figure(lang)."""
    src = inspect.getsource(getattr(F, name))
    body = src.split("\n", 1)[1]
    body = re.sub(r"^\s*#[^\n]*\n", "", body, count=0)
    body = re.sub(r"\s*save\(fig,[^)]*\)\s*", "\n    return fig\n", body)
    if "return fig" not in body:
        body += "\n    return fig\n"
    return f'''{PRELUDE}


def build_figure(lang: str = "fr") -> Figure:
    """Construit la figure NMLab du chapitre (libellés selon ``lang``)."""
{body.rstrip()}


build_figure(LANG)'''


by_ch = {}
for fn, ch, nb_name, fr, en, live in SPEC:
    by_ch.setdefault(ch, []).append(dict(
        name=nb_name, fig_fr=fr, fig_en=en, live=live,
        data="# (les séries sont chargées dans build_figure)" if live
             else "# (schéma : aucune donnée externe)",
        fig=cell_for(fn)))

for ch, figs in by_ch.items():
    nb_kit.build_all(META[ch], META[ch]["dir"], figs)
print("\ntotal :", sum(len(v) for v in by_ch.values()))
