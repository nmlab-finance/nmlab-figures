#!/usr/bin/env python3
"""Assemble les 15 notebooks à partir du code de production des figures.

Le code des figures vit dans newfigs/figs_{a,b,c}.py ; on le transpose ici en
cellules autonomes (SETUP + data + fig) conformes à la convention du dépôt.
"""
import sys, os, re, inspect
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
sys.path.insert(0, "/home/claudeagent/cms-workspace/newfigs")
os.chdir("/home/claudeagent/cms-workspace/newfigs")
import nb_kit
from build_new15 import CH, HELPERS

import figs_a, figs_b, figs_c
MODS = {}
for m in (figs_a, figs_b, figs_c):
    MODS.update({k: (m, v) for k, v in m.FIGS.items()})

# (clé, chapitre, nom notebook, titre fr, titre en, live)
SPEC = [
 ("ch12-07", "12", "fig07-deux-moteurs", "Deux moteurs sous le capot", "Two engines under the hood", False),
 ("ch13-07", "13", "fig07-ptf", "Le second témoin : la productivité globale des facteurs",
  "The second witness: total factor productivity", True),
 ("ch14-06", "14", "fig06-equation-croissance", "L'équation la plus simple de la macroéconomie",
  "The simplest equation in macroeconomics", False),
 ("ch14-07", "14", "fig07-dependance-japon", "Six actifs par senior en 1990, deux aujourd'hui",
  "Six workers per senior in 1990, two today", False),
 ("ch15-06", "15", "fig06-gap-inflation", "Le pont entre l'activité et les prix s'est affaissé",
  "The bridge between activity and prices has sagged", True),
 ("ch15-07", "15", "fig07-signe-du-gap", "Ce que dit le signe de l'écart",
  "What the sign of the gap says", False),
 ("ch16-06", "16", "fig06-epargne-investissement", "Épargne et investissement : même cycle, écart variable",
  "Saving and investment: same cycle, shifting gap", True),
 ("ch16-07", "16", "fig07-epargne-ue-us", "L'Europe ne manque pas d'épargne",
  "Europe does not lack savings", False),
 ("ch17-07", "17", "fig07-taux-actualisation", "Le taux d'actualisation décide de tout",
  "The discount rate decides everything", False),
 ("ch18-06", "18", "fig06-anatomie-page-fred", "Anatomie d'une page de série FRED",
  "Anatomy of a FRED series page", False),
 ("ch18-07", "18", "fig07-sa-contre-nsa", "Deux lettres qui changent la lecture : CPIAUCSL ou CPIAUCNS",
  "Two letters that change the reading: CPIAUCSL or CPIAUCNS", True),
 ("ch19-06", "19", "fig06-script-quatre-gestes", "Le script en quatre gestes",
  "The script in four moves", False),
 ("ch19-07", "19", "fig07-trois-erreurs", "Trois erreurs classiques, trois remèdes d'une ligne",
  "Three classic errors, three one-line fixes", False),
 ("ch20-06", "20", "fig06-surprise-pas-niveau", "Le marché paie la surprise, jamais le niveau",
  "Markets pay for the surprise, never the level", False),
 ("ch20-07", "20", "fig07-trois-formes-efficience", "Les trois formes d'efficience de Fama",
  "Fama's three forms of efficiency", False),
]


def cell_for(key):
    """Reconstruit le code autonome d'une figure : dict LABELS + corps de fonction."""
    mod, func = MODS[key]
    tkey = key.replace("-", "_")
    labels = mod.T[tkey]
    src = inspect.getsource(func)
    body = src.split("\n", 1)[1]
    body = re.sub(r'^\s*"""[\s\S]*?"""\n', "", body)          # docstring éventuelle
    body = body.replace('t = T["%s"][lang]' % tkey, "t = LABELS[lang]")
    body = re.sub(r"return save\(fig, f?\"[^\"]*\"\)", "return fig", body)
    body = "\n".join(l[4:] if l.startswith("    ") else l for l in body.split("\n"))
    lab = "LABELS = {\n"
    for lg in ("fr", "en"):
        lab += f'    "{lg}": dict(\n'
        for k, v in labels[lg].items():
            lab += f"        {k}={v!r},\n"
        lab += "    ),\n"
    lab += "}"
    return f'''{HELPERS}


{lab}


def build_figure(lang: str = "fr") -> Figure:
    """Construit la figure NMLab (libellés selon ``lang``)."""
{chr(10).join("    " + l if l.strip() else l for l in body.strip().split(chr(10)))}


build_figure(LANG)'''


by_ch = {}
for key, ch, name, fr, en, live in SPEC:
    by_ch.setdefault(ch, []).append(
        dict(name=name, fig_fr=fr, fig_en=en, live=live, data="", fig=cell_for(key)))

for ch, figs in by_ch.items():
    meta = CH[ch]
    for f in figs:
        f["data"] = "# (aucune donnée externe à charger)" if not f["live"] else "# données FRED chargées dans build_figure"
    nb_kit.build_all(meta, meta["dir"], figs)
print("\nnotebooks écrits :", sum(len(v) for v in by_ch.values()))
