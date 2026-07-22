#!/usr/bin/env python3
"""Génère les notebooks Colab du chapitre 3 — Microéconomie et macroéconomie.

Importe nb_kit, définit META (d'après get_article 6/7) + FIGURES (une cellule code
par figure : load_*/build_figure typés), rend les PNG (test_all) puis écrit les
.ipynb (build_all). Blocs DATA_*/FIG_* dans le style « strict » des chapitres
18/19/20 : schémas éditables (cartes) et une série historique embarquée.
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="3",
    title_fr="Microéconomie et macroéconomie : la différence avec des exemples concrets",
    title_en="Microeconomics and Macroeconomics: The Difference, with Concrete Examples",
    slug_fr="microeconomie-et-macroeconomie-la-difference",
    slug_en="microeconomics-and-macroeconomics-the-difference",
)
DIR = "macro/03-micro-et-macro"


# ── Figure 01 — la ville d'usine (frise à cinq étapes, schéma) ────────────────

DATA_1 = '''def factory_town(lang: str) -> list[tuple[str, str, str]]:
    """Les cinq étapes de la boucle de la ville d'usine : (couleur, titre, sous-titre),
    localisées. The five steps of the factory-town loop: (color, title, subtitle)."""
    blue, rose = nm.COLORS["blue"], nm.COLORS["rose"]
    if lang == "fr":
        return [
            (blue, "La rumeur d'un plan social court", "chaque ménage voit l'orage venir"),
            (blue, "Chacun fait le geste juste", "moins de dépenses, plus d'épargne"),
            (rose, "Ma dépense est ton revenu", "les ventes reculent partout"),
            (rose, "Les entreprises réduisent la voilure", "licenciements"),
            (rose, "La récession redoutée arrive", "l'ouvrier prévoyant perd son emploi"),
        ]
    return [
        (blue, "Word of layoffs spreads", "each household sees the storm coming"),
        (blue, "Everyone does the sensible thing", "spend less, save more"),
        (rose, "My spending is your income", "sales fall everywhere"),
        (rose, "Firms cut back", "layoffs"),
        (rose, "The dreaded recession arrives", "the prudent worker loses his job"),
    ]'''

FIG_1 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="La ville d'usine",
        sub="La prudence de chacun, l'hiver de tous — la scène qui ouvre le chapitre",
        note="Personne n'a été irrationnel : chacun a fait le geste juste. C'est leur somme qui a\\n"
             "mal tourné — le paradoxe qui ouvre la frontière entre micro et macro."),
    "en": dict(
        title="The factory town",
        sub="Everyone's prudence, everyone's winter — the chapter's opening scene",
        note="No one was irrational: everyone did the right thing. It is the sum that went\\n"
             "wrong — the paradox that opens the border between micro and macro."),
}

def build_figure(steps: list[tuple[str, str, str]], lang: str) -> Figure:
    """Schéma : cinq cartes empilées, reliées par des chevrons — la boucle de la récession."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1178)
    ax = nm.blank_axes(fig)

    x, w = 100, 1550
    card_h, gap, top = 118, 30, 900
    for i, (color, title, sub) in enumerate(steps):
        card_top = top - i * (card_h + gap)
        nm.card(ax, x, card_top - card_h, w, card_h, edge=nm.COLORS["edge"], lw=2.0, radius=20)
        ax.text(x + 55, card_top - card_h / 2, str(i + 1), ha="center", va="center",
                fontsize=34, fontweight="bold", color=color)
        ax.text(x + 115, card_top - 40, title, ha="left", va="center",
                fontsize=29, fontweight="bold", color=nm.COLORS["text"])
        ax.text(x + 115, card_top - 82, sub, ha="left", va="center",
                fontsize=22, color=nm.COLORS["muted"])
        if i < len(steps) - 1:                        # chevron entre deux cartes
            ax.scatter([x + w / 2], [card_top - card_h - gap / 2], marker="v",
                       s=150, color=nm.COLORS["muted"], zorder=3)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(factory_town(LANG), LANG)'''


# ── Figure 02 — deux regards, pas deux tailles (deux cartes + bandeau) ────────

DATA_2 = '''def two_lenses(lang: str) -> tuple[tuple, tuple, str]:
    """Les deux cartes (micro, macro) et le bandeau de conclusion : (titre, couleur, lignes)
    plus le texte du bandeau, localisés. The two cards and the closing banner."""
    if lang == "fr":
        micro = ("La microéconomie", nm.COLORS["blue"],
                 ["· un ménage, une entreprise, UN marché",
                  "· questions locales : pourquoi ce prix ?",
                  "· méthode : isoler le marché,\\n   toutes choses égales par ailleurs"])
        macro = ("La macroéconomie", nm.COLORS["rose"],
                 ["· l'économie prise comme un tout",
                  "· agrégats : PIB, inflation, emploi, taux",
                  "· questions globales : pourquoi tout\\n   accélère-t-il, puis ralentit ?"])
        banner = "pas une différence de taille — une différence de nature :\\nen additionnant les individus, les interactions surgissent"
        return micro, macro, banner
    micro = ("Microeconomics", nm.COLORS["blue"],
             ["· one household, one firm, ONE market",
              "· local questions: why this price?",
              "· method: isolate the market,\\n   all else held equal"])
    macro = ("Macroeconomics", nm.COLORS["rose"],
             ["· the economy taken as a whole",
              "· aggregates: GDP, inflation, jobs, rates",
              "· global questions: why does\\n   everything speed up, then slow?"])
    banner = "not a difference of size — a difference of nature:\\nadding individuals up makes the interactions emerge"
    return micro, macro, banner'''

FIG_2 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Deux regards, pas deux tailles",
        sub="L'arbre et la forêt — et une forêt n'est pas un grand arbre",
        note="Mon voisin et moi pouvons chacun vendre au prix affiché ; si tout le quartier vend\\n"
             "le même jour, ce prix n'existe plus. La foule fait émerger ce que nul ne contenait."),
    "en": dict(
        title="Two lenses, not two sizes",
        sub="The tree and the forest — and a forest is not a big tree",
        note="My neighbor and I can each sell at the listed price; if the whole neighborhood\\n"
             "sells the same day, that price no longer exists. The crowd creates what no member held."),
}

def build_figure(content: tuple, lang: str) -> Figure:
    """Schéma : microéconomie (bleu) et macroéconomie (rose) en regard, un bandeau les tranche."""
    text = LABELS[lang]
    micro, macro, banner = content
    fig = nm.figure(height_px=1064)
    ax = nm.blank_axes(fig)

    top, bottom = 825, 350
    for x0, (name, color, lines) in [(100, micro), (965, macro)]:
        nm.card(ax, x0, bottom, 760, top - bottom, edge=color, lw=2.8, radius=26)
        ax.text(x0 + 48, top - 68, name, ha="left", va="center",
                fontsize=32, fontweight="bold", color=nm.COLORS["text"])
        for j, line in enumerate(lines):
            ax.text(x0 + 48, top - 155 - j * 88, line, ha="left", va="top",
                    fontsize=25, color=nm.COLORS["muted"], linespacing=1.35)

    nm.card(ax, 100, 160, 1547, 138, edge=nm.COLORS["edge"], lw=2.2, radius=22)
    ax.text(873, 229, banner, ha="center", va="center", fontsize=25,
            fontweight="bold", color=nm.COLORS["text"], linespacing=1.5)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(two_lenses(LANG), LANG)'''


# ── Figure 03 — vrai pour un, faux pour tous (tableau) ────────────────────────

DATA_3 = '''def composition_rows(lang: str) -> tuple[tuple, list[tuple[str, str, str]]]:
    """En-têtes de colonnes et cinq lignes du tableau « vrai pour un, faux pour tous » :
    (geste, pour un seul, pour tous), localisés. Column headers and five table rows."""
    if lang == "fr":
        heads = ("LE GESTE", "POUR UN SEUL", "POUR TOUS À LA FOIS")
        rows = [
            ("Se lever au stade\\npour mieux voir", "on voit mieux",
             "personne ne voit mieux :\\ntout le monde est debout"),
            ("Épargner davantage", "on s'enrichit",
             "les revenus baissent,\\nl'épargne totale stagne"),
            ("Vendre dans la panique", "on sort au prix affiché",
             "le prix s'effondre :\\ntous ne peuvent sortir"),
            ("Baisser les salaires\\n(une entreprise)", "on gagne en compétitivité",
             "la demande recule : les salariés\\nsont aussi les clients"),
            ("Retirer son dépôt\\n(une banque)", "on récupère son argent",
             "la ruée fait tomber la banque"),
        ]
        return heads, rows
    heads = ("THE ACT", "FOR A SINGLE ONE", "FOR ALL AT ONCE")
    rows = [
        ("Standing up at the match\\nto see better", "you see better",
         "no one sees better:\\neveryone is standing"),
        ("Saving more", "you grow richer",
         "incomes fall,\\ntotal saving stalls"),
        ("Selling in a panic", "you exit at the quoted price",
         "the price collapses:\\nnot all can exit"),
        ("Cutting wages\\n(one firm)", "you gain competitiveness",
         "demand falls: workers\\nare also the customers"),
        ("Withdrawing your deposit\\n(one bank)", "you get your money back",
         "the run brings the bank down"),
    ]
    return heads, rows'''

FIG_3 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Vrai pour un, faux pour tous",
        sub="Le même geste, rationnel pour un individu isolé, se retourne dès que tous l'accomplissent ensemble.\\n"
            "C'est le sophisme de composition — le péché originel du raisonnement économique.",
        note="Chaque ligne oppose une vérité microéconomique (à gauche) à son sort une fois généralisée (à droite). Le passage de l'une à l'autre n'est pas\\n"
             "affaire d'échelle mais d'interaction : en agissant, chacun déforme le décor où agissent tous les autres."),
    "en": dict(
        title="True for one, false for all",
        sub="The same act, rational for a lone individual, backfires the moment everyone does it together.\\n"
            "This is the fallacy of composition — the original sin of economic reasoning.",
        note="Each row sets a microeconomic truth (left) against its fate once generalized (right). The shift is not one of scale but of interaction: in\\n"
             "acting, each one warps the backdrop against which all the others act."),
}

def build_figure(content: tuple, lang: str) -> Figure:
    """Tableau : cinq gestes, chacun vrai « pour un seul » (bleu) et faux « pour tous » (rose)."""
    text = LABELS[lang]
    heads, rows = content
    pale_blue, pale_rose = "#a9bcda", "#e6a7b4"
    fill_blue, fill_rose = "#14293a", "#3a1e28"
    fig = nm.figure(height_px=1291)
    ax = nm.blank_axes(fig)

    act_x = 78
    mid_x, mid_w = 634, 486                            # carte « pour un seul »
    right_x, right_w = 1150, 500                       # carte « pour tous »
    mid_cx, right_cx = mid_x + mid_w / 2, right_x + right_w / 2

    ax.text(act_x + 175, 1015, heads[0], ha="center", va="center",
            fontsize=20, fontweight="bold", color=nm.COLORS["muted"])
    ax.text(mid_cx, 1015, heads[1], ha="center", va="center",
            fontsize=23, fontweight="bold", color=pale_blue)
    ax.text(right_cx, 1015, heads[2], ha="center", va="center",
            fontsize=23, fontweight="bold", color=pale_rose)

    top, card_h, pitch = 885, 118, 155
    for i, (act, single, allof) in enumerate(rows):
        cy = top - i * pitch
        ax.text(act_x, cy, act, ha="left", va="center", fontsize=24,
                fontweight="bold", color=nm.COLORS["text"], linespacing=1.35)
        ax.scatter([560], [cy], marker=">", s=90, color=nm.COLORS["muted"], zorder=3)
        nm.card(ax, mid_x, cy - card_h / 2, mid_w, card_h, edge=nm.COLORS["blue"],
                fill=fill_blue, lw=2.2, radius=18)
        ax.text(mid_cx, cy, single, ha="center", va="center", fontsize=23,
                color=nm.COLORS["text"], linespacing=1.4)
        nm.card(ax, right_x, cy - card_h / 2, right_w, card_h, edge=nm.COLORS["rose"],
                fill=fill_rose, lw=2.2, radius=18)
        ax.text(right_cx, cy, allof, ha="center", va="center", fontsize=23,
                color="#f3e3e7", linespacing=1.4)

    fig.text(0.5, 1 - 46 / 1291, text["title"], fontsize=36, fontweight=800,
             color=nm.COLORS["text"], va="top", ha="center")
    fig.text(0.5, 1 - 108 / 1291, text["sub"], fontsize=20.5, color=nm.COLORS["muted"],
             va="top", ha="center", linespacing=1.5)
    nm.footer(fig, text["note"])
    return fig

build_figure(composition_rows(LANG), LANG)'''


# ── Figure 04 — le paradoxe de l'épargne (barres + chaîne, schéma) ────────────

DATA_4 = '''def thrift_paradox(lang: str) -> tuple[dict, list[str], str]:
    """Le volet micro (deux barres + carte) et le volet macro (chaîne de cinq maillons),
    localisés. The micro side (two bars + card) and the macro side (five-link chain)."""
    bars = [100.0, 62.0]                               # revenu (repère) et épargne (relatif)
    if lang == "fr":
        left = dict(head="Un seul ménage épargne plus", cats=["revenu", "épargne"],
                    card="son patrimoine\\ns'accroît", caption="le reste de l'économie\\nsert de décor fixe")
        chain = ["Chacun dépense moins", "Or ma dépense = ton revenu", "Les revenus reculent",
                 "Ventes et emploi en baisse", "Épargne totale : inchangée,\\nvoire plus faible"]
        head_right = "Tous les ménages épargnent plus, ensemble"
        return left, chain, head_right
    left = dict(head="One household saves more", cats=["income", "saving"],
                card="its wealth\\ngrows", caption="the rest of the economy\\nstays put")
    chain = ["Each one spends less", "But my spending = your income", "Incomes fall",
             "Sales and jobs decline", "Total saving: unchanged,\\neven lower"]
    head_right = "All households save more, together"
    return left, chain, head_right'''

FIG_4 = '''from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

LABELS = {
    "fr": dict(
        title="Le paradoxe de l'épargne",
        sub="Épargner enrichit un ménage. Mais si tous épargnent en même temps, la dépense de l'un étant le revenu de l'autre,\\n"
            "les revenus reculent — et l'épargne totale n'augmente pas ; elle peut même diminuer.",
        note="À gauche, la vérité micro : pour un ménage isolé, épargner, c'est s'enrichir. À droite, la vérité macro : quand tous serrent la ceinture\\n"
             "ensemble, les revenus baissent et l'effort d'épargne se sabote lui-même. C'est pourquoi l'économie n'est pas un ménage."),
    "en": dict(
        title="The paradox of thrift",
        sub="Saving makes a household richer. But if all save at once, since one person's spending is another's income,\\n"
            "incomes fall — and total saving does not rise; it may even shrink.",
        note="Left, the micro truth: for a lone household, to save is to grow richer. Right, the macro truth: when all tighten their belts at once, incomes\\n"
             "fall and the saving effort sabotages itself. This is why the economy is not a household."),
}

def build_figure(content: tuple, lang: str) -> Figure:
    """Schéma : à gauche deux barres (le ménage isolé s'enrichit), à droite la chaîne qui se sabote."""
    text = LABELS[lang]
    left, chain, head_right = content
    fig = nm.figure(height_px=1143)
    ax = nm.blank_axes(fig)

    # ── volet micro : deux barres (revenu, épargne) ──────────────────────────
    ax.text(360, 880, left["head"], ha="center", va="center", fontsize=27,
            fontweight="bold", color="#8fb8e6")
    base, bar_w = 430, 118
    xs, bar_h = [235, 445], [335, 208]
    colors = ["#7f92b8", nm.COLORS["blue"]]
    for x, h, c in zip(xs, bar_h, colors):
        ax.add_patch(Rectangle((x, base), bar_w, h, facecolor=c, edgecolor="none", zorder=2))
    ax.plot([150, 610], [base, base], color=nm.COLORS["muted"], lw=1.6)
    ax.annotate("", xy=(xs[1] + bar_w / 2, base + 208 + 92), xytext=(xs[1] + bar_w / 2, base + 208),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["blue"], lw=3.2))
    ax.text(xs[0] + bar_w / 2, base - 40, left["cats"][0], ha="center", va="top",
            fontsize=24, color=nm.COLORS["muted"])
    ax.text(xs[1] + bar_w / 2, base - 40, left["cats"][1], ha="center", va="top",
            fontsize=24, fontweight="bold", color=nm.COLORS["text"])
    nm.card(ax, 232, 208, 258, 96, edge=nm.COLORS["blue"], fill="#14293a", lw=2.2, radius=16)
    ax.text(361, 256, left["card"], ha="center", va="center", fontsize=23,
            fontweight="bold", color=nm.COLORS["text"], linespacing=1.35)
    ax.text(361, 150, left["caption"], ha="center", va="center", fontsize=20,
            fontstyle="italic", color=nm.COLORS["muted"], linespacing=1.4)

    # ── volet macro : chaîne de cinq maillons ────────────────────────────────
    ax.text(1245, 880, head_right, ha="center", va="center", fontsize=27,
            fontweight="bold", color="#f2879a")
    cx, box_w, box_h = 1245, 660, 92
    top, pitch = 812, 126
    for i, line in enumerate(chain):
        cy = top - i * pitch
        last = i == len(chain) - 1
        nm.card(ax, cx - box_w / 2, cy - box_h / 2, box_w, box_h,
                edge=nm.COLORS["rose"] if last else nm.COLORS["edge"],
                fill="#3a1e28" if last else None, lw=2.4 if last else 2.0, radius=16)
        ax.text(cx, cy, line, ha="center", va="center",
                fontsize=23 if not last else 23, fontweight="bold" if last else "normal",
                color=nm.COLORS["text"], linespacing=1.35)
        if not last:
            ax.annotate("", xy=(cx, cy - box_h / 2 - (pitch - box_h) + 6),
                        xytext=(cx, cy - box_h / 2 - 4),
                        arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["rose"], lw=2.6))

    fig.text(0.5, 1 - 46 / 1143, text["title"], fontsize=36, fontweight=800,
             color=nm.COLORS["text"], va="top", ha="center")
    fig.text(0.5, 1 - 108 / 1143, text["sub"], fontsize=20, color=nm.COLORS["muted"],
             va="top", ha="center", linespacing=1.5)
    nm.footer(fig, text["note"])
    return fig

build_figure(thrift_paradox(LANG), LANG)'''


# ── Figure 05 — un marché isolé, ou toute la toile (offre/demande + boucle) ───

DATA_5 = '''def equilibrium_scene(lang: str) -> dict:
    """Libellés des deux volets : le marché offre-demande isolé (micro) et la boucle des
    quatre secteurs (macro), localisés. Labels for the isolated market and the four-sector loop."""
    if lang == "fr":
        return dict(
            micro_h="Regard micro — équilibre partiel", micro_s="un seul marché, tout le reste figé",
            supply="offre", demand="demande", eq="équilibre", price="prix", qty="quantité",
            ceteris="« toutes choses\\négales par ailleurs »",
            macro_h="Regard macro — équilibre général", macro_s="tous les marchés reliés, en boucle",
            nodes=["Ménages", "Entreprises", "État", "Banques\\n& marchés"],
            center="la dépense de l'un\\n= le revenu de l'autre")
    return dict(
        micro_h="Micro lens — partial equilibrium", micro_s="one market, everything else frozen",
        supply="supply", demand="demand", eq="equilibrium", price="price", qty="quantity",
        ceteris='"all else\\nequal"',
        macro_h="Macro lens — general equilibrium", macro_s="all markets linked, in a loop",
        nodes=["Households", "Firms", "Government", "Banks\\n& markets"],
        center="one's spending\\n= another's income")'''

FIG_5 = '''from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch

LABELS = {
    "fr": dict(
        title="Un marché isolé, ou toute la toile",
        sub="La microéconomie étudie un marché en gelant tout le reste ; la macroéconomie ne le peut pas :\\n"
            "chaque revenu est la dépense d'un autre, et tout finit par se boucler.",
        note="À gauche, l'outil micro : isoler un marché et geler son environnement pour l'analyser proprement.\\n"
             "À droite, ce que la macro ne peut ignorer : les marchés s'alimentent l'un l'autre — tout est relié."),
    "en": dict(
        title="One market alone, or the whole web",
        sub="Microeconomics studies one market with everything else frozen; macroeconomics cannot:\\n"
            "each income is someone else's spending, and everything loops back.",
        note="Left, the micro tool: isolate one market and freeze its environment to analyze it cleanly.\\n"
             "Right, what macro cannot ignore: markets feed one another — everything is connected."),
}

def _arrow(ax, p0, p1, color, rad):
    """Flèche courbe entre deux points (coordonnées pixels)."""
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                 arrowstyle="-|>", mutation_scale=22, lw=2.4, color=color, zorder=1))

def build_figure(t: dict, lang: str) -> Figure:
    """Schéma : à gauche l'offre-demande figée (micro), à droite la boucle des secteurs (macro)."""
    text = LABELS[lang]
    mauve = "#b18fc9"
    fig = nm.figure(height_px=950)
    ax = nm.blank_axes(fig)

    # ── volet micro : carte encadrée avec le marché offre-demande ────────────
    nm.card(ax, 87, 152, 682, 551, edge=nm.COLORS["edge"], lw=2.2, radius=24)
    ax.text(428, 648, t["micro_h"], ha="center", va="center", fontsize=26,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(428, 606, t["micro_s"], ha="center", va="center", fontsize=20,
            fontstyle="italic", color=nm.COLORS["muted"])
    ox, oy = 190, 235                                  # origine des axes
    ax.annotate("", xy=(690, oy), xytext=(ox, oy),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["muted"], lw=1.8))
    ax.annotate("", xy=(ox, 560), xytext=(ox, oy),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["muted"], lw=1.8))
    ax.plot([230, 640], [270, 520], color=nm.COLORS["blue"], lw=3.0)       # offre
    ax.plot([230, 640], [520, 270], color=nm.COLORS["rose"], lw=3.0)       # demande
    ax.scatter([435], [395], s=110, color=nm.COLORS["text"], zorder=4, edgecolors="none")
    ax.text(410, 445, t["eq"], ha="right", va="center", fontsize=21,
            fontstyle="italic", color=nm.COLORS["text"])
    ax.text(655, 520, t["supply"], ha="left", va="center", fontsize=22,
            fontweight="bold", color=nm.COLORS["blue"])
    ax.text(655, 268, t["demand"], ha="left", va="center", fontsize=22,
            fontweight="bold", color=nm.COLORS["rose"])
    ax.text(ox - 22, 555, t["price"], ha="center", va="top", rotation=90,
            fontsize=20, color=nm.COLORS["muted"])
    ax.text(690, oy - 26, t["qty"], ha="right", va="top", fontsize=20, color=nm.COLORS["muted"])
    ax.text(455, 300, t["ceteris"], ha="center", va="center", fontsize=20,
            fontstyle="italic", color=nm.COLORS["muted"], linespacing=1.4)

    # ── volet macro : quatre secteurs en boucle ──────────────────────────────
    ax.text(1300, 705, t["macro_h"], ha="center", va="center", fontsize=26,
            fontweight="bold", color=nm.COLORS["rose"])
    ax.text(1300, 663, t["macro_s"], ha="center", va="center", fontsize=20,
            fontstyle="italic", color=nm.COLORS["muted"])
    nw, nh = 250, 96
    centers = {"tl": (1075, 520), "tr": (1525, 520), "bl": (1075, 250), "br": (1525, 250)}
    for key, label in zip(("tl", "tr", "bl", "br"), t["nodes"]):
        cxx, cyy = centers[key]
        nm.card(ax, cxx - nw / 2, cyy - nh / 2, nw, nh, edge=nm.COLORS["blue"], lw=2.6, radius=20)
        ax.text(cxx, cyy, label, ha="center", va="center", fontsize=24,
                fontweight="bold", color=nm.COLORS["text"], linespacing=1.2)
    # boucle : bleu dans le sens direct, mauve en retour
    _arrow(ax, (1140, 560), (1460, 560), nm.COLORS["blue"], -0.35)     # ménages -> entreprises
    _arrow(ax, (1450, 500), (1150, 500), mauve, -0.18)                 # entreprises -> ménages
    _arrow(ax, (1560, 462), (1560, 300), nm.COLORS["blue"], -0.35)     # entreprises -> banques
    _arrow(ax, (1075, 300), (1075, 462), mauve, -0.30)                 # état -> ménages (retour)
    _arrow(ax, (1010, 462), (1010, 300), nm.COLORS["blue"], -0.30)     # ménages -> état
    _arrow(ax, (1200, 250), (1400, 250), nm.COLORS["blue"], -0.35)     # état -> banques
    _arrow(ax, (1400, 210), (1200, 210), mauve, -0.35)                 # banques -> état
    nm.card(ax, 1210, 340, 180, 92, edge=nm.COLORS["edge"], fill=nm.COLORS["bg"], lw=1.8, radius=14)
    ax.text(1300, 386, t["center"], ha="center", va="center", fontsize=19,
            fontstyle="italic", color=nm.COLORS["muted"], linespacing=1.4)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(equilibrium_scene(LANG), LANG)'''


# ── Figure 06 — le chômage de la Grande Dépression (série historique embarquée) ─

DATA_6 = '''def great_depression_unemployment() -> tuple[list[int], list[float]]:
    """Taux de chômage annuel des États-Unis, 1925-1945, en % (estimations historiques
    de l'entre-deux-guerres, ordres de grandeur — d'après Lebergott, 1964, complété par
    les reconstructions du BLS). U.S. annual unemployment rate, 1925-1945 (%)."""
    years = list(range(1925, 1946))
    rate = [3.2, 1.8, 3.3, 4.2, 3.2, 8.7, 15.9, 23.6, 24.9, 21.7, 20.1,
            16.9, 14.3, 19.0, 17.2, 14.6, 9.9, 4.7, 1.9, 1.2, 1.9]
    return years, rate

years, rate = great_depression_unemployment()'''

FIG_6 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Quand le regard micro a cédé : la Grande Dépression",
        sub="Un chômage de masse que nul effort individuel ne résorbait. C'est de cet échec qu'est née\\n"
            "la macroéconomie comme science distincte.",
        ylab="Taux de chômage aux États-Unis (%)",
        crash="Krach de 1929",
        peak="1933 : près d'un actif\\nsur quatre sans emploi (~25 %)",
        keynes="1936 — Keynes, la « Théorie générale » :\\nla macroéconomie devient une discipline",
        war="l'effort de guerre\\nrésorbe le chômage",
        note="Estimations historiques du chômage américain (entre-deux-guerres, ordres de grandeur).\\n"
             "Aucune décision individuelle rationnelle n'expliquait un tel chômage : il fallait raisonner sur l'ensemble."),
    "en": dict(
        title="When the micro lens failed: the Great Depression",
        sub="Mass unemployment that no individual effort could absorb. From that failure\\n"
            "macroeconomics was born as a distinct science.",
        ylab="U.S. unemployment rate (%)",
        crash="The 1929 crash",
        peak="1933: nearly one worker\\nin four unemployed (~25%)",
        keynes="1936 — Keynes's General Theory:\\nmacroeconomics becomes a discipline",
        war="the war effort\\nabsorbs unemployment",
        note="Historical estimates of U.S. unemployment (interwar years, orders of magnitude).\\n"
             "No sum of rational individual decisions could explain it: one had to reason about the economy as a whole."),
}

def build_figure(years: list[int], rate: list[float], lang: str) -> Figure:
    """Le chômage américain 1925-1945 : la Grande Dépression, ses repères de 1929 et 1936."""
    text = LABELS[lang]
    fig = nm.figure(height_px=968)
    ax = nm.axes(fig, left=0.088)
    ax.fill_between(years, rate, color=nm.COLORS["rose"], alpha=0.16)
    ax.plot(years, rate, color=nm.COLORS["rose"], linewidth=3.2, marker="o",
            markersize=8, clip_on=False, zorder=3)
    ax.axvline(1929, color=nm.COLORS["muted"], linestyle=(0, (6, 5)), linewidth=1.8, alpha=0.8)
    ax.axvline(1936, color=nm.COLORS["blue"], linestyle=(0, (6, 5)), linewidth=1.8, alpha=0.9)
    ax.set_ylim(0, 28)
    ax.set_yticks(range(0, 26, 5))
    ax.set_ylabel(text["ylab"])
    ax.set_xlim(1924, 1946)
    ax.set_xticks([1925, 1929, 1933, 1936, 1940, 1945])
    ax.grid(axis="x", visible=False)

    ax.scatter([1933], [24.9], s=120, color=nm.COLORS["rose"], zorder=5)
    ax.annotate(text["peak"], xy=(1933, 24.9), xytext=(1935.4, 27.4), ha="left", va="center",
                fontsize=21, fontweight="bold", color=nm.COLORS["text"], linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8),
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#3a1e28",
                          edgecolor=nm.COLORS["rose"], linewidth=2.0))
    ax.annotate(text["keynes"], xy=(1936, 20.5), xytext=(1937, 21.8), ha="left", va="center",
                fontsize=20, fontweight="bold", color=nm.COLORS["text"], linespacing=1.4,
                bbox=dict(boxstyle="round,pad=0.5", facecolor=nm.COLORS["card"],
                          edgecolor=nm.COLORS["blue"], linewidth=2.0))
    ax.annotate(text["crash"], xy=(1929, 3.2), xytext=(1927.3, 10.5), ha="center", va="bottom",
                fontsize=21, fontweight="bold", color=nm.COLORS["text"],
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=1.6))
    ax.annotate(text["war"], xy=(1942.4, 3.4), xytext=(1941.6, 9.3), ha="center", va="bottom",
                fontsize=20, fontstyle="italic", color=nm.COLORS["muted"], linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=1.5))

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(years, rate, LANG)'''


# ── Figure 07 — un pont étroit entre la partie et le tout (schéma) ────────────

DATA_7 = '''def bridge_part_whole(lang: str) -> dict:
    """Libellés du schéma partie-tout : les deux cartes, le pont central et les deux
    sophismes latéraux, localisés. Labels for the part-whole bridge diagram."""
    if lang == "fr":
        return dict(
            whole_t="LE TOUT", whole_s="les agrégats : PIB, inflation, chômage",
            part_t="LA PARTIE", part_s="un agent : ménage, entreprise",
            bridge_t="le pont : les microfondations",
            bridge_s="fécond, mais l'« agent représentatif »\\nefface les interactions —\\non bâtit le pont, pas sans la rivière",
            left_t="sophisme de\\ncomposition", left_s="généraliser au tout\\nle geste individuel",
            right_t="sophisme de\\ndivision", right_s="imputer la moyenne\\nà chacun (croissance\\n+3 % ≠ vous +3 %)")
    return dict(
        whole_t="THE WHOLE", whole_s="the aggregates: GDP, inflation, jobs",
        part_t="THE PART", part_s="one agent: a household, a firm",
        bridge_t="the bridge: microfoundations",
        bridge_s='fruitful, but the "representative agent"\\nerases the interactions —\\nthe bridge does not remove the river',
        left_t="fallacy of\\ncomposition", left_s="generalizing the\\nindividual move",
        right_t="fallacy of\\ndivision", right_s="reading the average\\nonto each (growth\\n+3% ≠ you +3%)")'''

FIG_7 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Un pont étroit entre la partie et le tout",
        sub="Deux trajets, le même terrain miné",
        note="La micro a raison sur l'arbre, la macro sur la forêt — toute l'habileté consiste\\n"
             "à ne jamais appliquer à l'un les lois de l'autre."),
    "en": dict(
        title="A narrow bridge between the part and the whole",
        sub="Two journeys across the same minefield",
        note="Micro is right about the tree, macro about the forest — the whole skill is\\n"
             "never to apply to one the laws of the other."),
}

def build_figure(t: dict, lang: str) -> Figure:
    """Schéma : LE TOUT (rose) et LA PARTIE (bleu), le pont au centre, les deux sophismes de côté."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    ax = nm.blank_axes(fig)

    card_x, card_w = 585, 580
    cx = card_x + card_w / 2
    nm.card(ax, card_x, 758, card_w, 150, edge=nm.COLORS["rose"], lw=2.8, radius=22)
    ax.text(cx, 858, t["whole_t"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(cx, 806, t["whole_s"], ha="center", va="center", fontsize=22, color=nm.COLORS["muted"])
    nm.card(ax, card_x, 232, card_w, 150, edge=nm.COLORS["blue"], lw=2.8, radius=22)
    ax.text(cx, 332, t["part_t"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(cx, 280, t["part_s"], ha="center", va="center", fontsize=22, color=nm.COLORS["muted"])

    ax.text(cx, 588, t["bridge_t"], ha="center", va="center", fontsize=25,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(cx, 500, t["bridge_s"], ha="center", va="center", fontsize=21,
            color=nm.COLORS["muted"], linespacing=1.5)

    # flèches latérales : composition monte (gauche), division descend (droite)
    ax.annotate("", xy=(505, 740), xytext=(505, 400),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["rose"], lw=3.4))
    ax.annotate("", xy=(1250, 400), xytext=(1250, 740),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["rose"], lw=3.4))

    for x, title, subt in [(245, t["left_t"], t["left_s"]), (1560, t["right_t"], t["right_s"])]:
        ax.scatter([x], [640], marker="x", s=150, linewidths=4, color=nm.COLORS["rose"], zorder=3)
        ax.text(x, 576, title, ha="center", va="center", fontsize=25,
                fontweight="bold", color=nm.COLORS["text"], linespacing=1.35)
        ax.text(x, 452, subt, ha="center", va="top", fontsize=21,
                color=nm.COLORS["muted"], linespacing=1.5)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(bridge_part_whole(LANG), LANG)'''


# ── Figure 08 — trois garde-fous pour l'investisseur (schéma) ─────────────────

DATA_8 = '''def three_guardrails(lang: str) -> list[tuple[str, str]]:
    """Les trois garde-fous de l'investisseur : (titre, précision), localisés.
    The investor's three guardrails: (title, gloss), localized."""
    if lang == "fr":
        return [
            ("Le marché n'est pas un grand individu",
             "vous pouvez vendre ; tous ne le peuvent pas en même temps — la sortie est plus étroite que la salle"),
            ("L'économie n'est pas un ménage",
             "l'austérité d'une famille est prudente ; celle de tous peut approfondir la récession"),
            ("Sachez à quel étage vous raisonnez",
             "« bonne entreprise » (micro) n'est pas « bon placement » (macro) : le climat peut tout engloutir"),
        ]
    return [
        ("The market is not one big individual",
         "you can sell; everyone cannot sell at once — the exit is narrower than the room"),
        ("The economy is not a household",
         "one family's belt-tightening is prudent; everyone's can deepen the recession"),
        ("Know which floor you are reasoning on",
         "a good company (micro) is not a good investment (macro): the climate can swallow the best stock"),
    ]'''

FIG_8 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Trois garde-fous pour l'investisseur",
        sub="Le sophisme de composition, ramené à l'argent",
        note="Presque toutes les grandes bévues du raisonnement sur l'argent tiennent dans une\\n"
             "seule confusion : appliquer au tout une loi qui ne vaut que pour la partie."),
    "en": dict(
        title="Three guardrails for the investor",
        sub="The fallacy of composition, brought back to money",
        note="Nearly every great mistake in reasoning about money comes down to a single\\n"
             "confusion: applying to the whole a law that only holds for the part."),
}

def build_figure(rows: list[tuple[str, str]], lang: str) -> Figure:
    """Schéma : trois cartes numérotées, un garde-fou par carte."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.blank_axes(fig)

    x, w = 100, 1550
    card_h, gap, top = 130, 42, 780
    for i, (title, gloss) in enumerate(rows):
        card_top = top - i * (card_h + gap)
        nm.card(ax, x, card_top - card_h, w, card_h, edge=nm.COLORS["edge"], lw=2.0, radius=20)
        ax.text(x + 55, card_top - card_h / 2, str(i + 1), ha="center", va="center",
                fontsize=36, fontweight="bold", color=nm.COLORS["blue"])
        ax.text(x + 115, card_top - 46, title, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        ax.text(x + 115, card_top - 92, gloss, ha="left", va="center",
                fontsize=21, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(three_guardrails(LANG), LANG)'''


FIGURES = [
    dict(name="fig01-ville-d-usine",
         fig_fr="La ville d'usine", fig_en="The factory town",
         live=False, data=DATA_1, fig=FIG_1),
    dict(name="fig02-deux-regards",
         fig_fr="Deux regards, pas deux tailles", fig_en="Two lenses, not two sizes",
         live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-vrai-un-faux-tous",
         fig_fr="Vrai pour un, faux pour tous", fig_en="True for one, false for all",
         live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-paradoxe-epargne",
         fig_fr="Le paradoxe de l'épargne", fig_en="The paradox of thrift",
         live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-equilibre-partiel-general",
         fig_fr="Un marché isolé, ou toute la toile", fig_en="One market alone, or the whole web",
         live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-chomage-grande-depression",
         fig_fr="Quand le regard micro a cédé : la Grande Dépression",
         fig_en="When the micro lens failed: the Great Depression",
         live=False, data=DATA_6, fig=FIG_6),
    dict(name="fig07-pont-partie-tout",
         fig_fr="Un pont étroit entre la partie et le tout",
         fig_en="A narrow bridge between the part and the whole",
         live=False, data=DATA_7, fig=FIG_7),
    dict(name="fig08-trois-garde-fous",
         fig_fr="Trois garde-fous pour l'investisseur", fig_en="Three guardrails for the investor",
         live=False, data=DATA_8, fig=FIG_8),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out3")
    nb_kit.build_all(META, DIR, FIGURES)
