#!/usr/bin/env python3
"""Notebooks Colab du chapitre 7 — « Module 1 en pratique : se bâtir une routine de veille macro ».

Neuf figures : huit schémas / tableaux de bord (cartes ``nm.blank_axes`` + ``nm.card``,
libellés éditables) et une figure calculée (probabilité de gain selon la fréquence, loi
normale — parabole du dentiste de Taleb). Aucune n'est une capture : toutes sont
reproductibles → toutes reçoivent un notebook (``live=False``, données embarquées / calculées).

Usage :
    python build_ch7.py            # rend les PNG (out7/) puis écrit les .ipynb du miroir
Convention « strict » (cf. build_notebooks.py) : une seule cellule code, ``load_*()`` puis
``build_figure(...) -> Figure``, ``LABELS = {"fr":…, "en":…}`` piloté par ``LANG``.
"""

from nb_kit import build_all, test_all

META = dict(
    num="7",
    title_fr="Module 1 en pratique : se bâtir une routine de veille macro",
    title_en="Module 1 in Practice: Building Your Macro Monitoring Routine",
    slug_fr="se-batir-une-routine-de-veille-macro",
    slug_en="building-your-macro-monitoring-routine",
)
DIR = "macro/07-routine-veille-macro"


# ═════════════════════════════════════════════════════════════════════════════
# Figure 01 — Deux lundis (deux cartes en regard : le déluge vs le rituel)
# ═════════════════════════════════════════════════════════════════════════════

DATA_01 = '''def two_mondays(lang: str) -> dict:
    """Les deux colonnes du schéma : (titre, liste de puces), localisées.
    Each column of the diagram: (heading, list of bullets), localized."""
    if lang == "fr":
        return dict(
            left=("7 h 04 — le déluge", [
                ["trois alertes, un fil social,", "une note en « repricing hawkish »"],
                ["quarante minutes, le pouls plus haut"],
                ["rien d'utilisable en tête"],
                ["à refaire ce soir"]]),
            right=("Plus tard — le rituel", [
                ["le calendrier des publications du jour"],
                ["une poignée de prix connus par cœur"],
                ["l'écart au consensus"],
                ["une ligne dans un carnet"],
                ["quinze minutes, l'onglet se ferme"]]))
    return dict(
        left=("7:04 — the deluge", [
            ["three alerts, a social feed,", "a « hawkish repricing » note"],
            ["forty minutes, a higher pulse"],
            ["nothing usable in mind"],
            ["to be done again tonight"]]),
        right=("Later — the ritual", [
            ["the day's release calendar"],
            ["a handful of prices known by heart"],
            ["the gap to the consensus"],
            ["one line in a notebook"],
            ["fifteen minutes, the tab closes"]]))'''

FIG_01 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Deux lundis",
               sub="Les mêmes chiffres, gratuits, aux mêmes heures — deux méthodes",
               note="Au bout d'un an, le premier aura « suivi les marchés » ; le second saura où il en est —\\n"
                    "en y ayant passé dix fois moins de temps."),
    "en": dict(title="Two Mondays",
               sub="The same figures, free, at the same hours — two methods",
               note="After a year, the first will have « followed the markets »; the second will know where things stand —\\n"
                    "having spent ten times less time on it."),
}

def build_figure(content: dict, lang: str) -> Figure:
    """Schéma : deux cartes en regard, le déluge (rose) contre le rituel (bleu)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    card_w, top, bottom = 736, 862, 250
    columns = [(content["left"], nm.COLORS["rose"], 96),
               (content["right"], nm.COLORS["blue"], 915)]
    for (heading, bullets), color, x in columns:
        nm.card(ax, x, bottom, card_w, top - bottom, edge=color, lw=2.6, radius=26)
        tx = x + 54
        ax.text(tx, top - 74, heading, ha="left", va="top",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        y = top - 200
        for group in bullets:
            ax.text(tx + 2, y, "·", ha="left", va="top", fontsize=30, color=nm.COLORS["muted"])
            for line in group:
                ax.text(tx + 34, y, line, ha="left", va="top", fontsize=26, color=nm.COLORS["text"])
                y -= 46
            y -= 30

    nm.header(fig, text["title"], text["sub"])
    fig.text(0.0458, 24 / 1102, text["note"], fontsize=16.5, color=nm.COLORS["muted"],
             va="bottom", ha="left", linespacing=1.65, fontstyle="italic")
    nm.footer(fig)
    return fig

build_figure(two_mondays(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 02 — Probabilité d'observer un gain selon la fréquence (loi normale)
# ═════════════════════════════════════════════════════════════════════════════

DATA_02 = '''import math

def gain_probabilities() -> list[float]:
    """Probabilité (%) d'observer un gain selon la fréquence d'observation.

    Parabole du dentiste (Taleb, 2001) : un portefeuille d'espérance 15 %/an et de
    volatilité 10 %/an. Sur une fraction d'année ``t``, le rendement est un tirage normal
    de dérive ``0,15·t`` et d'écart-type ``0,10·√t`` ; la probabilité d'un gain vaut donc
    ``Φ(1,5·√t)`` (ratio de Sharpe = 0,15/0,10 = 1,5). Année de cotation : 252 séances de
    8 heures. / Normal-law probability of seeing a gain at each observation frequency."""
    sharpe = 0.15 / 0.10
    year = 252 * 8 * 3600                 # secondes de cotation par an (252 j × 8 h)
    periods = [1 / year, 60 / year, 3600 / year, 1 / 252, 1 / 12, 1 / 4, 1.0]
    phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return [100 * phi(sharpe * math.sqrt(t)) for t in periods]'''

FIG_02 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Voir un gain : une question de fréquence d'observation",
        xlab="Fréquence d'observation du portefeuille",
        ylab="Probabilité d'observer un gain (%)",
        cats=["1 seconde", "1 minute", "1 heure", "1 jour", "1 mois", "1 trimestre", "1 an"],
        note="Probabilité qu'un coup d'œil affiche un gain — espérance 15 %/an, volatilité 10 %/an (Taleb, 2001).\\n"
             "Ligne rouge : 50 % = pile ou face. Loi normale ; « 1 jour » = une séance de bourse."),
    "en": dict(
        title="Seeing a gain: a matter of observation frequency",
        xlab="Portfolio observation frequency",
        ylab="Probability of observing a gain (%)",
        cats=["1 second", "1 minute", "1 hour", "1 day", "1 month", "1 quarter", "1 year"],
        note="Probability that a glance shows a gain — 15%/yr expected return, 10%/yr volatility (Taleb, 2001).\\n"
             "Red line: 50% = coin flip. Normal law; « 1 day » = one trading session."),
}

def _fmt(value: float, lang: str) -> str:
    """Étiquette de barre : 2 décimales sous 52 %, 1 au-dessus ; virgule + « % » en fr."""
    decimals = 2 if value < 52 else 1
    label = f"{value:.{decimals}f}"
    return label.replace(".", ",") + " %" if lang == "fr" else label + "%"

def build_figure(probabilities: list[float], lang: str) -> Figure:
    """Diagramme en barres : la compétence n'est visible qu'à basse fréquence."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1235)
    ax = nm.axes(fig, top=1 - 168 / 1235, bottom=0.205)
    ax.grid(axis="x", visible=False)
    positions = range(len(probabilities))
    ax.bar(positions, probabilities, width=0.68, color=nm.COLORS["blue"], zorder=3)
    ax.axhline(50, color=nm.COLORS["rose"], linestyle="--", linewidth=2.6, zorder=2)
    ax.set_ylim(0, 103)
    ax.set_yticks(range(0, 101, 25))
    ax.set_ylabel(text["ylab"])
    ax.set_xlabel(text["xlab"], labelpad=14)
    ax.set_xlim(-0.7, len(probabilities) - 0.3)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(text["cats"])
    for pos, value in zip(positions, probabilities):
        ax.annotate(_fmt(value, lang), (pos, value), xytext=(0, 12),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=27, fontweight="bold", color=nm.COLORS["text"])
    nm.header(fig, text["title"])
    nm.footer(fig, text["note"])
    return fig

build_figure(gain_probabilities(), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 03 — Les trois horloges de la veille (jour / semaine / mois)
# ═════════════════════════════════════════════════════════════════════════════

DATA_03 = '''def clocks(lang: str) -> list[dict]:
    """Les trois horloges : (accent, titre coloré, durée, question, 4 gestes), localisées.
    The three clocks: (accent color, heading, duration, question, four gestures)."""
    if lang == "fr":
        return [
            dict(color=nm.COLORS["blue"], heading="CHAQUE JOUR", time="15 minutes",
                 question="« Qu'est-ce qui a changé ? »", items=[
                     "Calendrier du jour : publications, heures, consensus",
                     "Les cadrans : une poignée de prix, toujours les mêmes",
                     "La surprise : l'écart au consensus, jamais le chiffre seul",
                     "Le carnet : une ligne — date, fait, lecture"]),
            dict(color=nm.COLORS["rose"], heading="CHAQUE SEMAINE", time="1 heure",
                 question="« Que raconte la semaine ? »", items=[
                     "Relire le carnet : des points à la pente",
                     "Mettre à jour le tableau de bord",
                     "Un avis contraire, choisi exprès",
                     "Agenda de la semaine suivante, consensus notés"]),
            dict(color=nm.COLORS["muted"], heading="CHAQUE MOIS", time="2 à 3 heures",
                 question="« Ma lecture tient-elle ? »", items=[
                     "Niveaux et tendances : inflation, emploi, taux, nowcast",
                     "Révisions : le chiffre d'il y a deux mois existe-t-il encore ?",
                     "Thèse de régime en trois phrases, seuils d'alerte écrits",
                     "Une lecture longue — une seule, mais entière"]),
        ]
    return [
        dict(color=nm.COLORS["blue"], heading="EVERY DAY", time="15 minutes",
             question="« What has changed? »", items=[
                 "Today's calendar: releases, times, consensus",
                 "The dials: a handful of prices, always the same",
                 "The surprise: the gap to consensus, never the number alone",
                 "The notebook: one line — date, fact, reading"]),
        dict(color=nm.COLORS["rose"], heading="EVERY WEEK", time="1 hour",
             question="« What does the week say? »", items=[
                 "Reread the notebook: from dots to a slope",
                 "Update the dashboard",
                 "One contrary view, chosen on purpose",
                 "Next week's agenda, consensus noted"]),
        dict(color=nm.COLORS["muted"], heading="EVERY MONTH", time="2 to 3 hours",
             question="« Does my reading still hold? »", items=[
                 "Levels and trends: inflation, jobs, rates, nowcast",
                 "Revisions: does the two-month-old number still exist?",
                 "Regime thesis in three sentences, alert thresholds written",
                 "One long read — just one, but whole"]),
    ]'''

FIG_03 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Les trois horloges de la veille",
               note="La fréquence de la veille se cale sur la fréquence de vos décisions — pas sur celle des dépêches."),
    "en": dict(title="The three clocks of monitoring",
               note="Monitoring's frequency matches the frequency of your decisions — not that of the news wires."),
}

def build_figure(rows: list[dict], lang: str) -> Figure:
    """Schéma : trois cartes empilées (jour, semaine, mois), colonne repère + gestes."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1349)
    ax = nm.blank_axes(fig)

    card_x, card_w = 95, 1557
    top, card_h, gap = 1165, 308, 32
    for i, row in enumerate(rows):
        c_top = top - i * (card_h + gap)
        c_bottom = c_top - card_h
        nm.card(ax, card_x, c_bottom, card_w, card_h, edge=row["color"], lw=2.6, radius=24)
        # Colonne repère (gauche) : horloge colorée, durée, question.
        lx = card_x + 42
        ax.text(lx, c_top - 62, row["heading"], ha="left", va="center",
                fontsize=28, fontweight="bold", color=row["color"])
        ax.text(lx, c_top - 130, row["time"], ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        ax.text(lx, c_top - 196, row["question"], ha="left", va="center",
                fontsize=21, color=nm.COLORS["muted"], fontstyle="italic")
        # Séparateur vertical.
        div_x = card_x + 555
        ax.plot([div_x, div_x], [c_bottom + 46, c_top - 46], color=nm.COLORS["edge"], lw=1.6)
        # Colonne des gestes (droite) : quatre puces.
        bx = card_x + 615
        for j, item in enumerate(row["items"]):
            y = c_top - 70 - j * 56
            ax.text(bx, y, "•", ha="left", va="center", fontsize=24, color=row["color"])
            ax.text(bx + 34, y, item, ha="left", va="center", fontsize=25, color=nm.COLORS["text"])

    nm.header(fig, text["title"])
    nm.footer(fig, text["note"], signature=False)
    fig.text(0.9715, 1 - 44 / 1349, "▪ NMLab", fontsize=16.5, color=nm.COLORS["muted"],
             va="top", ha="right")
    return fig

build_figure(clocks(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 04 — Le quart d'heure du matin (quatre gestes, budget de temps)
# ═════════════════════════════════════════════════════════════════════════════

DATA_04 = '''def gestures(lang: str) -> list[tuple[str, str, str]]:
    """Les quatre gestes du matin : (durée, titre, description), localisés.
    The four morning gestures: (duration, heading, description), localized."""
    if lang == "fr":
        return [
            ("2 min", "Le calendrier",
             "quelles publications aujourd'hui, à quelle heure, quel consensus ?"),
            ("5 min", "Les cadrans",
             "les mêmes prix, dans le même ordre : 10 ans, pente, euro-dollar, pétrole, indice, VIX"),
            ("5 min", "La surprise",
             "l'écart au consensus, jamais le chiffre seul — puis marge d'erreur et révisions"),
            ("3 min", "Le carnet",
             "une ligne : la date, le fait saillant, votre lecture en une phrase"),
        ]
    return [
        ("2 min", "The calendar",
         "which releases today, at what time, what consensus?"),
        ("5 min", "The dials",
         "the same prices, in the same order: 10-year, curve slope, euro-dollar, oil, index, VIX"),
        ("5 min", "The surprise",
         "the gap to consensus, never the number alone — then error margin and revisions"),
        ("3 min", "The notebook",
         "one line: the date, the salient fact, your reading in one sentence"),
    ]'''

FIG_04 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Le quart d'heure du matin",
               sub="Quatre gestes, quinze minutes, montre en main",
               note="Trois anti-règles ferment le rituel : les chiffres avant les opinions ; pas de cours du\\n"
                    "portefeuille dans le quart d'heure ; l'actualité en continu reste fermée."),
    "en": dict(title="The morning quarter-hour",
               sub="Four gestures, fifteen minutes, watch in hand",
               note="Three anti-rules close the ritual: figures before opinions; no portfolio prices in\\n"
                    "the quarter-hour; rolling news stays shut."),
}

def build_figure(rows: list[tuple[str, str, str]], lang: str) -> Figure:
    """Schéma : quatre rangées « pastille de durée + geste »."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    pill_x, pill_w = 95, 250
    wide_x, wide_w = 382, 1270
    top, row_h, gap = 845, 139, 28
    for i, (duration, heading, description) in enumerate(rows):
        r_top = top - i * (row_h + gap)
        r_bottom = r_top - row_h
        nm.card(ax, pill_x, r_bottom, pill_w, row_h, edge=nm.COLORS["blue"], lw=2.4, radius=18)
        ax.text(pill_x + pill_w / 2, r_bottom + row_h / 2, duration, ha="center", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["blue"])
        nm.card(ax, wide_x, r_bottom, wide_w, row_h, edge=nm.COLORS["edge"], lw=2.0, radius=18)
        ax.text(wide_x + 48, r_top - 48, heading, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        ax.text(wide_x + 48, r_top - 100, description, ha="left", va="center",
                fontsize=25, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    fig.text(0.0458, 24 / 1102, text["note"], fontsize=16.5, color=nm.COLORS["muted"],
             va="bottom", ha="left", linespacing=1.65, fontstyle="italic")
    nm.footer(fig)
    return fig

build_figure(gestures(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 05 — L'heure du week-end (quatre gestes, grille 2 × 2)
# ═════════════════════════════════════════════════════════════════════════════

DATA_05 = '''def weekend(lang: str) -> list[tuple[str, list[str]]]:
    """Les quatre gestes du week-end : (titre, deux lignes), localisés.
    The four weekend gestures: (heading, two lines), localized."""
    if lang == "fr":
        return [
            ("Relire le carnet", ["le jour voit des points ;", "la semaine voit une pente"]),
            ("Mettre à jour le tableau de bord", ["les valeurs de la semaine,", "la tendance sur 3 à 6 mois"]),
            ("Lire UN avis contraire", ["le contradicteur inscrit à l'agenda,", "comme un rendez-vous chez le kiné"]),
            ("Préparer la semaine", ["surligner 2-3 publications, noter", "le consensus : vérifier des hypothèses"]),
        ]
    return [
        ("Reread the notebook", ["the day sees dots;", "the week sees a slope"]),
        ("Update the dashboard", ["the week's values,", "the three-to-six-month trend"]),
        ("Read ONE contrary view", ["the contrarian booked in the diary,", "like an appointment with the physio"]),
        ("Prepare the week", ["highlight 2-3 releases, note", "the consensus: test hypotheses"]),
    ]'''

FIG_05 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="L'heure du week-end",
               sub="Comprendre : quatre gestes, café en main",
               note="Si les cinq lignes du carnet ne racontent rien, c'est une information aussi :\\n"
                    "semaine sans signal — et c'est très bien ainsi."),
    "en": dict(title="The weekend hour",
               sub="Understand: four gestures, coffee in hand",
               note="If the notebook's five lines say nothing, that too is information:\\n"
                    "a week without signal — and that is quite fine."),
}

def build_figure(cards: list[tuple[str, list[str]]], lang: str) -> Figure:
    """Schéma : quatre cartes en grille 2 × 2, un geste par carte."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1064)
    ax = nm.blank_axes(fig)

    card_w, gap_x, x0 = 748, 64, 95
    card_h, gap_y, top = 285, 45, 800
    for i, (heading, lines) in enumerate(cards):
        col, r = i % 2, i // 2
        x = x0 + col * (card_w + gap_x)
        c_top = top - r * (card_h + gap_y)
        c_bottom = c_top - card_h
        nm.card(ax, x, c_bottom, card_w, card_h, edge=nm.COLORS["edge"], lw=2.0, radius=22)
        tx = x + 44
        ax.text(tx, c_top - 62, heading, ha="left", va="center",
                fontsize=31, fontweight="bold", color=nm.COLORS["text"])
        for j, line in enumerate(lines):
            ax.text(tx, c_top - 158 - j * 50, line, ha="left", va="center",
                    fontsize=27, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    fig.text(0.0458, 24 / 1064, text["note"], fontsize=16.5, color=nm.COLORS["muted"],
             va="bottom", ha="left", linespacing=1.65, fontstyle="italic")
    nm.footer(fig)
    return fig

build_figure(weekend(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 06 — La revue mensuelle (quatre gestes numérotés, pleine largeur)
# ═════════════════════════════════════════════════════════════════════════════

DATA_06 = '''def monthly(lang: str) -> list[tuple[str, str, str]]:
    """Les quatre gestes de la revue mensuelle : (numéro, titre, description), localisés.
    The four gestures of the monthly review: (number, heading, description), localized."""
    if lang == "fr":
        return [
            ("1", "Les niveaux", "inflation totale et sous-jacente, emploi, taux, nowcast — la position sur la carte"),
            ("2", "Les révisions", "le chiffre célébré il y a deux mois existe-t-il encore ?"),
            ("3", "La thèse de régime", "trois phrases — et des seuils d'alerte écrits à froid, qui décideront pour vous"),
            ("4", "Une lecture longue", "un chapitre, un rapport, une étude — une seule, mais entière"),
        ]
    return [
        ("1", "The levels", "headline and core inflation, jobs, rates, nowcast — the position on the map"),
        ("2", "The revisions", "does the number celebrated two months ago still exist?"),
        ("3", "The regime thesis", "three sentences — and alert thresholds written cold, that will decide for you"),
        ("4", "One long read", "a chapter, a report, a study — just one, but whole"),
    ]'''

FIG_06 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="La revue mensuelle",
               sub="Deux à trois heures pour remettre la carte à jour",
               note="Le seuil pré-écrit décidera à froid, le jour où vous auriez décidé à chaud —\\n"
                    "c'est la version opérationnelle de « préparer plutôt que prédire »."),
    "en": dict(title="The monthly review",
               sub="Two to three hours to bring the map up to date",
               note="The pre-written threshold will decide in the cold, the day you would have decided in the heat —\\n"
                    "it is the operational version of « prepare rather than predict »."),
}

def build_figure(rows: list[tuple[str, str, str]], lang: str) -> Figure:
    """Schéma : quatre rangées numérotées, titre + description."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    card_x, card_w = 95, 1557
    top, card_h, gap = 838, 135, 26
    for i, (number, heading, description) in enumerate(rows):
        c_top = top - i * (card_h + gap)
        c_bottom = c_top - card_h
        nm.card(ax, card_x, c_bottom, card_w, card_h, edge=nm.COLORS["edge"], lw=2.0, radius=20)
        ax.text(card_x + 62, c_bottom + card_h / 2, number, ha="center", va="center",
                fontsize=44, fontweight="bold", color=nm.COLORS["blue"])
        ax.text(card_x + 132, c_top - 48, heading, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        ax.text(card_x + 132, c_top - 100, description, ha="left", va="center",
                fontsize=25, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    fig.text(0.0458, 24 / 1102, text["note"], fontsize=16.5, color=nm.COLORS["muted"],
             va="bottom", ha="left", linespacing=1.65, fontstyle="italic")
    nm.footer(fig)
    return fig

build_figure(monthly(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 07 — Le tableau de bord minimal (huit lignes, quatre colonnes)
# ═════════════════════════════════════════════════════════════════════════════

DATA_07 = '''def dashboard(lang: str) -> tuple[list[str], list[tuple]]:
    """Le tableau de bord : (en-têtes de colonnes, huit lignes), localisé.
    Ligne = (indicateur, sous-titre, cadran, rendez-vous, pourquoi je la suis).
    The dashboard: (column headers, eight rows), localized."""
    if lang == "fr":
        headers = ["INDICATEUR", "CADRAN", "RENDEZ-VOUS", "POURQUOI JE LA SUIS"]
        rows = [
            ("Inflation sous-jacente", "IPC, PCE — IPCH zone euro", "Inflation", "vers le 12 · fin de mois", "Le cap de la banque centrale"),
            ("Taux directeur", "date de la prochaine réunion", "Banque centrale", "Fed 8×/an · BCE ~6 sem.", "Le bas de la fraction"),
            ("Taux à 10 ans", "obligation d'État de référence", "Taux", "en continu", "Gravité des valorisations"),
            ("Pente de la courbe", "2 ans – 10 ans", "Taux", "en continu", "Le baromètre du cycle"),
            ("Emploi", "chômage & créations de postes", "Emploi", "1er vendredi du mois", "Le pouls de l'économie"),
            ("ISM & PMI", "enquêtes de conjoncture", "Croissance", "1er ouvré · vers le 23", "L'humeur avant le dur"),
            ("Pétrole", "Brent", "Monde", "en continu", "L'inflation importée"),
            ("Euro-dollar", "EUR/USD", "Monde", "en continu", "Compétitivité et change"),
        ]
        return headers, rows
    headers = ["INDICATOR", "DIAL", "NEXT RELEASE", "WHY I TRACK IT"]
    rows = [
        ("Core inflation", "CPI, PCE — HICP euro area", "Inflation", "around the 12th · month-end", "The central bank's course"),
        ("Policy rate", "date of the next meeting", "Central bank", "Fed 8×/yr · ECB ~6 wks", "The bottom of the fraction"),
        ("10-year yield", "benchmark government bond", "Rates", "continuous", "Gravity on valuations"),
        ("Curve slope", "2-year – 10-year", "Rates", "continuous", "The cycle's barometer"),
        ("Jobs", "unemployment & payroll gains", "Jobs", "1st Friday of month", "The economy's pulse"),
        ("ISM & PMIs", "business surveys", "Growth", "1st business day · ~23rd", "The mood before hard data"),
        ("Oil", "Brent", "World", "continuous", "Imported inflation"),
        ("Euro-dollar", "EUR/USD", "World", "continuous", "Competitiveness and FX"),
    ]
    return headers, rows'''

FIG_07 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Le tableau de bord minimal : huit lignes",
               note="À tenir dans un simple tableur ; ajoutez à la main « dernier relevé », « précédent » et « tendance 3-6 mois ».\\n"
                    "Règle d'or : une ligne dont vous ne savez plus pourquoi elle est là se supprime."),
    "en": dict(title="The minimal dashboard: eight lines",
               note="Keep it in a simple spreadsheet; add by hand « last reading », « previous » and « 3-6 month trend ».\\n"
                    "Golden rule: a line you no longer know why you track gets deleted."),
}
CONTINUOUS = {"en continu", "continuous"}

def build_figure(content: tuple, lang: str) -> Figure:
    """Tableau de bord : en-têtes de colonnes, huit lignes, badge de cadran par ligne."""
    headers, rows = content
    text = LABELS[lang]
    fig = nm.figure(height_px=1375)
    ax = nm.blank_axes(fig)

    col_x = [88, 585, 845, 1240]           # x des en-têtes / valeurs (gauche)
    badge_cx = 665                          # centre des badges de cadran
    head_y, first_top, row_h = 1215, 1180, 128

    for x, label in zip(col_x, headers):
        ax.text(x, head_y, label, ha="left", va="center", fontsize=20,
                fontweight="bold", color=nm.COLORS["muted"])
    ax.plot([85, 1662], [1196, 1196], color=nm.COLORS["edge"], lw=2)

    for i, (name, sub, dial, rdv, why) in enumerate(rows):
        r_top = first_top - i * row_h
        cy = r_top - row_h / 2
        if i:
            ax.plot([85, 1662], [r_top, r_top], color=nm.COLORS["edge"], lw=1.1, alpha=0.6)
        ax.text(col_x[0], cy + 22, name, ha="left", va="center",
                fontsize=28, fontweight="bold", color=nm.COLORS["text"])
        ax.text(col_x[0], cy - 30, sub, ha="left", va="center",
                fontsize=21, color=nm.COLORS["muted"])
        badge_w = 150 + 12.5 * len(dial)
        nm.card(ax, badge_cx - badge_w / 2, cy - 31, badge_w, 62,
                edge=nm.COLORS["blue"], lw=2.0, radius=14)
        ax.text(badge_cx, cy, dial, ha="center", va="center",
                fontsize=23, color=nm.COLORS["text"])
        italic = rdv in CONTINUOUS
        ax.text(col_x[2], cy, rdv, ha="left", va="center", fontsize=21,
                color=nm.COLORS["muted"] if italic else nm.COLORS["text"],
                fontstyle="italic" if italic else "normal")
        ax.text(col_x[3], cy, why, ha="left", va="center",
                fontsize=22, color=nm.COLORS["text"])

    nm.header(fig, text["title"])
    nm.footer(fig, text["note"], signature=False)
    fig.text(0.9715, 1 - 44 / 1375, "▪ NMLab", fontsize=16.5, color=nm.COLORS["muted"],
             va="top", ha="right")
    return fig

build_figure(dashboard(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 08 — Quatre pièges, quatre parades (grille 2 × 2)
# ═════════════════════════════════════════════════════════════════════════════

DATA_08 = '''def traps(lang: str) -> list[tuple[str, str, list[str]]]:
    """Les quatre pièges : (titre, description, parade en deux lignes), localisés.
    The four traps: (heading, description, two-line parry), localized."""
    if lang == "fr":
        return [
            ("La sur-veille", "confondre informé et préparé",
             ["parade : un budget temps : tout dépassement", "durable est un problème, pas du zèle"]),
            ("Le biais de confirmation", "collecter des munitions pour sa thèse",
             ["parade : l'avis contraire du week-end + le carnet,", "écrit avant de connaître la suite"]),
            ("La gâchette facile", "convertir la veille en signaux de trading",
             ["parade : aucune décision de portefeuille un jour", "de publication, sauf plan écrit d'avance"]),
            ("Le tout-ou-rien", "trois semaines parfaites, puis l'abandon",
             ["parade : la routine minimale viable : trois minutes", "qu'on ne rate jamais, même en vacances"]),
        ]
    return [
        ("Over-monitoring", "confusing informed with prepared",
         ["parry: a time budget: any lasting overrun", "is a problem, not zeal"]),
        ("Confirmation bias", "gathering ammunition for your thesis",
         ["parry: the weekend's contrary view + the notebook,", "written before knowing what came next"]),
        ("The itchy trigger", "turning monitoring into trading signals",
         ["parry: no portfolio decision on a release day,", "unless planned in writing beforehand"]),
        ("All-or-nothing", "three perfect weeks, then the giving up",
         ["parry: the minimum viable routine: three minutes", "you never miss, even on holiday"]),
    ]'''

FIG_08 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Quatre pièges, quatre parades",
               sub="Les échecs connus de la veille — et leurs remèdes",
               note="La plus importante des parades tient en trois minutes : le calendrier du jour, le 10 ans,\\n"
                    "une ligne de carnet — le plancher qu'on ne rate jamais."),
    "en": dict(title="Four traps, four parries",
               sub="The known failures of monitoring — and their remedies",
               note="The most important parry takes three minutes: the day's calendar, the 10-year,\\n"
                    "one notebook line — the floor you never miss."),
}

def build_figure(cards: list[tuple[str, str, list[str]]], lang: str) -> Figure:
    """Schéma : quatre cartes (piège rose) en grille 2 × 2 — titre, mal, parade."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1140)
    ax = nm.blank_axes(fig)

    card_w, gap_x, x0 = 748, 64, 95
    card_h, gap_y, top = 283, 48, 800
    for i, (heading, description, parry) in enumerate(cards):
        col, r = i % 2, i // 2
        x = x0 + col * (card_w + gap_x)
        c_top = top - r * (card_h + gap_y)
        c_bottom = c_top - card_h
        nm.card(ax, x, c_bottom, card_w, card_h, edge=nm.COLORS["rose"], lw=2.6, radius=22)
        tx = x + 44
        ax.text(tx, c_top - 56, heading, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        ax.text(tx, c_top - 118, description, ha="left", va="center",
                fontsize=24, color=nm.COLORS["muted"], fontstyle="italic")
        for j, line in enumerate(parry):
            ax.text(tx, c_top - 188 - j * 46, line, ha="left", va="center",
                    fontsize=24, color=nm.COLORS["blue"])

    nm.header(fig, text["title"], text["sub"])
    fig.text(0.0458, 24 / 1140, text["note"], fontsize=16.5, color=nm.COLORS["muted"],
             va="bottom", ha="left", linespacing=1.65, fontstyle="italic")
    nm.footer(fig)
    return fig

build_figure(traps(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 09 — Module 1 : la boîte à outils est complète (sept réflexes)
# ═════════════════════════════════════════════════════════════════════════════

DATA_09 = '''def reflexes(lang: str) -> list[tuple[str, list[str]]]:
    """Les sept réflexes du module 1 : (numéro, deux lignes), localisés.
    The seven reflexes of module 1: (number, two lines), localized."""
    if lang == "fr":
        return [
            ("1", ["la fraction : revenus futurs en haut,", "taux d'actualisation en bas"]),
            ("2", ["le climat, pas la météo :", "reconnaître le régime"]),
            ("3", ["le tout n'est pas la somme", "des parties"]),
            ("4", ["six cadrans, un seul mécanisme —", "et la surprise, pas le niveau"]),
            ("5", ["la langue : déplier chaque mot", "en son mécanisme"]),
            ("6", ["des chiffres manufacturés,", "révisés, à marge d'erreur"]),
            ("7", ["la routine : trois horloges,", "trois questions"]),
        ]
    return [
        ("1", ["the fraction: future income on top,", "the discount rate below"]),
        ("2", ["climate, not weather:", "recognize the regime"]),
        ("3", ["the whole is not the sum", "of the parts"]),
        ("4", ["six dials, one mechanism —", "and the surprise, not the level"]),
        ("5", ["the language: unfold each word", "into its mechanism"]),
        ("6", ["manufactured numbers,", "revised, with an error margin"]),
        ("7", ["the routine: three clocks,", "three questions"]),
    ]'''

FIG_09 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Module 1 : la boîte à outils est complète",
               sub="Sept chapitres, sept réflexes désormais installés",
               note="La culture macro est une langue vivante : sans pratique elle s'évapore en quelques mois ;\\n"
                    "avec un quart d'heure par jour, elle se compose comme des intérêts."),
    "en": dict(title="Module 1: the toolbox is complete",
               sub="Seven chapters, seven reflexes now in place",
               note="Macro literacy is a living language: without practice it evaporates in a few months;\\n"
                    "with a quarter-hour a day, it compounds like interest."),
}

def build_figure(cards: list[tuple[str, list[str]]], lang: str) -> Figure:
    """Schéma : sept réflexes numérotés — 1·3·5·7 à gauche, 2·4·6 à droite."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    card_w, gap_x, x0 = 748, 64, 95
    card_h, gap_y, top = 136, 30, 800
    for i, (number, lines) in enumerate(cards):
        col, r = i % 2, i // 2            # 1,3,5,7 → colonne gauche ; 2,4,6 → droite
        x = x0 + col * (card_w + gap_x)
        c_top = top - r * (card_h + gap_y)
        c_bottom = c_top - card_h
        cy = c_bottom + card_h / 2
        nm.card(ax, x, c_bottom, card_w, card_h, edge=nm.COLORS["edge"], lw=2.0, radius=22)
        color = nm.COLORS["rose"] if number == "7" else nm.COLORS["blue"]
        ax.text(x + 52, cy, number, ha="left", va="center",
                fontsize=42, fontweight="bold", color=color)
        for j, line in enumerate(lines):
            ax.text(x + 135, cy + 26 - j * 52, line, ha="left", va="center",
                    fontsize=26, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    fig.text(0.0458, 24 / 1102, text["note"], fontsize=16.5, color=nm.COLORS["muted"],
             va="bottom", ha="left", linespacing=1.65, fontstyle="italic")
    nm.footer(fig)
    return fig

build_figure(reflexes(LANG), LANG)'''


# ── Liste des figures du chapitre (ordre d'apparition dans l'article) ─────────

FIGURES = [
    dict(name="fig01-deux-lundis", fig_fr="Deux lundis", fig_en="Two Mondays",
         data=DATA_01, fig=FIG_01, live=False),
    dict(name="fig02-proba-gain-frequence",
         fig_fr="Voir un gain : une question de fréquence d'observation",
         fig_en="Seeing a gain: a matter of observation frequency",
         data=DATA_02, fig=FIG_02, live=False),
    dict(name="fig03-trois-horloges",
         fig_fr="Les trois horloges de la veille", fig_en="The three clocks of monitoring",
         data=DATA_03, fig=FIG_03, live=False),
    dict(name="fig04-quart-d-heure-du-matin",
         fig_fr="Le quart d'heure du matin", fig_en="The morning quarter-hour",
         data=DATA_04, fig=FIG_04, live=False),
    dict(name="fig05-heure-du-week-end",
         fig_fr="L'heure du week-end", fig_en="The weekend hour",
         data=DATA_05, fig=FIG_05, live=False),
    dict(name="fig06-revue-mensuelle",
         fig_fr="La revue mensuelle", fig_en="The monthly review",
         data=DATA_06, fig=FIG_06, live=False),
    dict(name="fig07-tableau-de-bord-minimal",
         fig_fr="Le tableau de bord minimal : huit lignes", fig_en="The minimal dashboard: eight lines",
         data=DATA_07, fig=FIG_07, live=False),
    dict(name="fig08-quatre-pieges",
         fig_fr="Quatre pièges, quatre parades", fig_en="Four traps, four parries",
         data=DATA_08, fig=FIG_08, live=False),
    dict(name="fig09-boite-a-outils-module-1",
         fig_fr="Module 1 : la boîte à outils est complète", fig_en="Module 1: the toolbox is complete",
         data=DATA_09, fig=FIG_09, live=False),
]


if __name__ == "__main__":
    test_all(FIGURES, "out7")
    build_all(META, DIR, FIGURES)
