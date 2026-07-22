#!/usr/bin/env python3
"""Notebooks du chapitre 6 — D'où viennent les chiffres macro ?

Même méthode que les chapitres 18/19/20 : META + FIGURES, puis test_all/build_all
via nb_kit. Une seule cellule code par notebook : load_*()/data localisée puis
build_figure(...). Toutes les figures de ce chapitre sont des schémas ou des
données millésimées embarquées (aucune série FRED en direct) → live=False.
"""

import sys
sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(
    num="6",
    title_fr="D'où viennent les chiffres macro ? Sources, fréquence et fiabilité",
    title_en="Where Do Macro Numbers Come From? Sources, Frequency and Reliability",
    slug_fr="d-ou-viennent-les-chiffres-macro",
    slug_en="where-do-macro-numbers-come-from",
)
DIR = "macro/06-chiffres-macro"


# ── Figure 01 — 8 h 30 à Washington (schéma frise) ────────────────────────────

DATA_1 = '''def release_minute(lang: str) -> list[tuple[str, str, str]]:
    """La frise de la minute de publication : (pastille horaire, texte, couleur), localisée.
    The release-minute timeline: (time pill, text, colour), localized."""
    if lang == "fr":
        return [
            ("8 h 29", "les conversations s'éteignent, les algorithmes sont armés", "blue"),
            ("8 h 30:00", "l'embargo tombe : le chiffre part pour tous au même instant", "blue"),
            ("+ 0,1 s", "les machines ont lu, comparé au consensus, tradé", "rose"),
            ("+ quelques s", "des dizaines de milliards de dollars ont changé de mains", "rose"),
        ]
    return [
        ("8:29", "conversations die down, the algorithms are armed", "blue"),
        ("8:30:00", "the embargo lifts: the number goes out to all at the same instant", "blue"),
        ("+ 0.1 s", "the machines have read, compared to consensus, traded", "rose"),
        ("+ a few s", "tens of billions of dollars have changed hands", "rose"),
    ]'''

FIG_1 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="8 h 30 à Washington",
        sub="La minute la plus dense de la planète financière",
        note="Le chiffre le plus attendu du monde n'est pas une lecture de la réalité : c'est un produit manufacturé —\\n"
             "matières premières, délais, défauts de série, et un service après-vente : les révisions."),
    "en": dict(
        title="8:30 a.m. in Washington",
        sub="The densest minute on the financial planet",
        note="The most awaited number in the world is not a reading of reality: it is a manufactured product —\\n"
             "raw materials, lead times, factory defects, and an after-sales service: revisions."),
}

def build_figure(rows: list[tuple[str, str, str]], lang: str) -> Figure:
    """Schéma : quatre étapes (pastille horaire colorée → texte), reliées par des flèches."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    pill_x, pill_w = 100, 380
    card_x, card_w = 520, 1130
    top0, row_h, gap = 800, 130, 35
    centers = []
    for i, (label, body, color_key) in enumerate(rows):
        row_top = top0 - i * (row_h + gap)
        color = nm.COLORS[color_key]
        nm.card(ax, pill_x, row_top - row_h, pill_w, row_h, edge=color, lw=2.8, radius=18)
        ax.text(pill_x + pill_w / 2, row_top - row_h / 2, label, ha="center", va="center",
                fontsize=30, fontweight="bold", color=color)
        nm.card(ax, card_x, row_top - row_h, card_w, row_h, edge=nm.COLORS["edge"], lw=2.0, radius=18)
        ax.text(card_x + 44, row_top - row_h / 2, body, ha="left", va="center",
                fontsize=27, color=nm.COLORS["text"])
        centers.append((pill_x + pill_w / 2, row_top - row_h))

    for (cx, bottom_prev), (_, _) in zip(centers[:-1], centers[1:]):
        top_next = bottom_prev - gap
        ax.annotate("", xy=(cx, top_next + 3), xytext=(cx, bottom_prev - 3),
                    arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["muted"], lw=2.4))

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(release_minute(LANG), LANG)'''


# ── Figure 02 — un chiffre macro est un produit manufacturé (schéma flux) ─────

DATA_2 = '''def manufacturing_chain(lang: str) -> list[list[str]]:
    """Les cinq maillons de la chaîne de fabrication d'un chiffre macro, localisés.
    The five links of the manufacturing chain of a macro number, localized."""
    if lang == "fr":
        return [
            ["La réalité", "économique"],
            ["Des conventions :", "que compte-t-on ?"],
            ["Des dispositifs :", "enquêtes, registres"],
            ["Des traitements :", "saisonnalité, qualité"],
            ["Le chiffre publié,", "± marge d'erreur"],
        ]
    return [
        ["Economic", "reality"],
        ["Conventions:", "what do we count?"],
        ["Instruments:", "surveys, registers"],
        ["Processing:", "seasonality, quality"],
        ["The published number,", "± error margin"],
    ]'''

FIG_2 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Un chiffre macro est un produit manufacturé",
        sub="Personne n'a jamais croisé un PIB dans la rue",
        note="Kuznets, père du PIB, fut le premier à en borner le sens (1934) ; Morgenstern rappelait qu'aucun physicien\\n"
             "ne publierait une constante sans son incertitude. L'exactitude vient par approximations successives."),
    "en": dict(
        title="A macro number is a manufactured product",
        sub="No one has ever bumped into a GDP in the street",
        note="Kuznets, the father of GDP, was the first to bound its meaning (1934); Morgenstern recalled that no physicist\\n"
             "would publish a constant without its uncertainty. Accuracy comes by successive approximations."),
}

def build_figure(boxes: list[list[str]], lang: str) -> Figure:
    """Schéma-flux : cinq encadrés (réalité → conventions → dispositifs → traitements → chiffre)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1026)
    ax = nm.blank_axes(fig)

    box_w, box_h, gap = 470, 200, 95
    x1 = 95
    x2 = x1 + box_w + gap
    x3 = x2 + box_w + gap
    top_top, top_bot = 720, 520
    bot_top, bot_bot = 430, 230
    coords = [
        (x1, top_top, top_bot, "blue"),
        (x2, top_top, top_bot, "edge"),
        (x3, top_top, top_bot, "edge"),
        (x2, bot_top, bot_bot, "edge"),
        (x3, bot_top, bot_bot, "rose"),
    ]
    for (x, ytop, ybot, key), lines in zip(coords, boxes):
        nm.card(ax, x, ybot, box_w, ytop - ybot, edge=nm.COLORS[key], lw=2.6, radius=20)
        cx, cy = x + box_w / 2, (ytop + ybot) / 2
        for j, line in enumerate(lines):
            ax.text(cx, cy + 30 - j * 60, line, ha="center", va="center",
                    fontsize=28, fontweight="bold", color=nm.COLORS["text"])

    arrow = dict(arrowstyle="-|>", color=nm.COLORS["muted"], lw=2.6)
    mid = (top_top + top_bot) / 2
    ax.annotate("", xy=(x2 - 6, mid), xytext=(x1 + box_w + 6, mid), arrowprops=arrow)
    ax.annotate("", xy=(x3 - 6, mid), xytext=(x2 + box_w + 6, mid), arrowprops=arrow)
    # Diagonale : dispositifs (haut-droite) → traitements (bas-milieu)
    ax.annotate("", xy=(x2 + box_w / 2 + 40, bot_top + 6), xytext=(x3 + 40, top_bot - 6),
                arrowprops=arrow)
    ax.annotate("", xy=(x3 - 6, (bot_top + bot_bot) / 2), xytext=(x2 + box_w + 6, (bot_top + bot_bot) / 2),
                arrowprops=arrow)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(manufacturing_chain(LANG), LANG)'''


# ── Figure 03 — qui fabrique les chiffres macro ? (schéma-carte) ──────────────

DATA_3 = '''def producers(lang: str) -> dict:
    """Les quatre familles de producteurs de statistiques macro, localisées.
    The four families of macro-statistics producers, localized."""
    if lang == "fr":
        return dict(
            left=dict(
                title="Instituts nationaux de statistique", dot="blue",
                sub="le cœur du système : les enquêtes officielles",
                blocks=[
                    ("États-Unis — trois guichets",
                     ["BLS · emploi, prix (IPC)", "BEA · PIB, inflation PCE",
                      "Census · ventes, logement, commerce"]),
                    ("Europe — un institut par pays",
                     ["INSEE · Destatis · ONS", "Eurostat coiffe la zone euro"]),
                ]),
            right=[
                dict(title="Banques centrales", dot="blue",
                     sub="productrices autant que consommatrices",
                     items=["Fed · production industrielle", "Fed · comptes financiers",
                            "BCE · monnaie, crédit, banques"]),
                dict(title="Organisations internationales", dot="muted",
                     sub="comparer les pays, fixer les normes",
                     items=["FMI · OCDE · Banque mondiale · BRI", "Comparaisons entre pays",
                            "Normes de qualité et de diffusion"]),
                dict(title="Producteurs privés", dot="rose",
                     sub="le pouls en avance — mais des opinions",
                     items=["ISM · PMI de l'industrie (années 1930)", "S&P Global · PMI, dizaines de pays",
                            "Conf. Board, U. Michigan · confiance"]),
            ],
            legend=[("blue", "activité réalisée — donnée « dure »"),
                    ("rose", "enquête d'opinion — donnée « molle »"),
                    ("muted", "comparaisons & normes")],
        )
    return dict(
        left=dict(
            title="National statistical institutes", dot="blue",
            sub="the heart of the system: the official surveys",
            blocks=[
                ("United States — three counters",
                 ["BLS · employment, prices (CPI)", "BEA · GDP, PCE inflation",
                  "Census · sales, housing, trade"]),
                ("Europe — one institute per country",
                 ["INSEE · Destatis · ONS", "Eurostat heads the euro area"]),
            ]),
        right=[
            dict(title="Central banks", dot="blue",
                 sub="producers as much as consumers",
                 items=["Fed · industrial production", "Fed · financial accounts",
                        "ECB · money, credit, banks"]),
            dict(title="International organizations", dot="muted",
                 sub="compare countries, set standards",
                 items=["IMF · OECD · World Bank · BIS", "Comparisons between countries",
                        "Quality and dissemination standards"]),
            dict(title="Private producers", dot="rose",
                 sub="the pulse ahead — but opinions",
                 items=["ISM · industry PMI (1930s)", "S&P Global · PMI, dozens of countries",
                        "Conf. Board, U. Michigan · confidence"]),
        ],
        legend=[("blue", "realized activity — « hard » data"),
                ("rose", "opinion survey — « soft » data"),
                ("muted", "comparisons & standards")],
    )'''

FIG_3 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(title="Qui fabrique les chiffres macro ?",
               sub="Quatre familles de producteurs — et à quelle porte frapper pour chaque indicateur"),
    "en": dict(title="Who makes the macro numbers?",
               sub="Four families of producers — and which door to knock on for each indicator"),
}

def _bullets(ax, x_dot, x_text, y0, items, color, step=62, fs=23):
    """Trace une liste à puces (petits points colorés) et renvoie le y de la dernière ligne."""
    y = y0
    for item in items:
        ax.scatter([x_dot], [y], s=70, color=color, zorder=3)
        ax.text(x_text, y, item, ha="left", va="center", fontsize=fs, color=nm.COLORS["text"])
        y -= step
    return y

def build_figure(data: dict, lang: str) -> Figure:
    """Schéma-carte : un grand encadré (instituts) + trois encadrés, dots codés couleur + légende."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1316)
    ax = nm.blank_axes(fig)

    # Grand encadré de gauche.
    lx, lw, ltop, lbot = 45, 830, 1035, 150
    nm.card(ax, lx, lbot, lw, ltop - lbot, edge=nm.COLORS["edge"], lw=2.2, radius=26)
    left = data["left"]
    ax.scatter([lx + 62], [ltop - 55], s=230, color=nm.COLORS[left["dot"]], zorder=3)
    ax.text(lx + 108, ltop - 55, left["title"], ha="left", va="center",
            fontsize=29, fontweight="bold", color=nm.COLORS["text"])
    ax.text(lx + 70, ltop - 120, left["sub"], ha="left", va="center",
            fontsize=23, fontstyle="italic", color=nm.COLORS["muted"])
    ax.plot([lx + 70, lx + lw - 60], [ltop - 165, ltop - 165], color=nm.COLORS[left["dot"]],
            linewidth=2.2, alpha=0.9)
    y = ltop - 235
    for heading, items in left["blocks"]:
        ax.text(lx + 70, y, heading, ha="left", va="center", fontsize=25,
                fontweight="bold", color=nm.COLORS["muted"])
        y = _bullets(ax, lx + 90, lx + 135, y - 72, items, nm.COLORS[left["dot"]])
        y -= 44

    # Trois encadrés de droite.
    rx, rw = 905, 795
    tops = [1035, 721, 407]
    height = 268
    for card, rtop in zip(data["right"], tops):
        rbot = rtop - height
        nm.card(ax, rx, rbot, rw, height, edge=nm.COLORS["edge"], lw=2.2, radius=24)
        ax.scatter([rx + 50], [rtop - 46], s=190, color=nm.COLORS[card["dot"]], zorder=3)
        ax.text(rx + 88, rtop - 46, card["title"], ha="left", va="center",
                fontsize=26, fontweight="bold", color=nm.COLORS["text"])
        ax.text(rx + 50, rtop - 92, card["sub"], ha="left", va="center",
                fontsize=21, fontstyle="italic", color=nm.COLORS["muted"])
        ax.plot([rx + 50, rx + rw - 45], [rtop - 126, rtop - 126], color=nm.COLORS[card["dot"]],
                linewidth=2.0, alpha=0.9)
        _bullets(ax, rx + 70, rx + 106, rtop - 170, card["items"], nm.COLORS[card["dot"]], step=45, fs=22)

    # Légende en bas.
    lx0 = [60, 700, 1330]
    for x0, (color_key, label) in zip(lx0, data["legend"]):
        ax.scatter([x0], [72], s=190, color=nm.COLORS[color_key], zorder=3)
        ax.text(x0 + 40, 72, label, ha="left", va="center", fontsize=21, color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    hpx = fig.get_size_inches()[1] * nm.DPI
    fig.text(0.9715, 1 - 58 / hpx, "▪ NMLab", fontsize=16.5,
             color=nm.COLORS["muted"], va="top", ha="right")
    return fig

build_figure(producers(LANG), LANG)'''


# ── Figure 04 — les trois matières premières (schéma trois cartes) ────────────

DATA_4 = '''def raw_materials(lang: str) -> list[tuple[str, str, list[list[str]]]]:
    """Les trois matières premières du chiffre macro : (titre, couleur, paragraphes), localisées.
    The three raw materials of a macro number: (title, colour, paragraphs), localized."""
    if lang == "fr":
        return [
            ("L'enquête", "blue",
             [["80 000 prix relevés (IPC),", "60 000 ménages, 120 000", "employeurs interrogés"],
              ["rapide et large — mais", "échantillonnée : ± 130 000", "sur l'emploi d'un mois"]]),
            ("Le registre", "muted",
             [["guichets du chômage,", "douanes, fisc : le comptage", "de ce qui est géré"],
              ["quasi exhaustif, mais étroit", "et lent — il recale l'enquête", "une fois l'an"]]),
            ("La donnée massive", "rose",
             [["données de caisse (INSEE,", "2020), prix en ligne (Billion", "Prices Project), cartes",
               "bancaires, satellites"],
              ["des millions de transactions", "réelles, en complément"]]),
        ]
    return [
        ("The survey", "blue",
         [["80,000 prices collected (CPI),", "60,000 households, 120,000", "employers polled"],
          ["fast and broad — but", "sampled: ± 130,000", "on one month's jobs"]]),
        ("The register", "muted",
         [["unemployment counters,", "customs, tax: the count", "of what is managed"],
          ["near-exhaustive, but narrow", "and slow — it re-anchors the", "survey once a year"]]),
        ("Big data", "rose",
         [["scanner data (INSEE, 2020),", "online prices (Billion Prices", "Project), card payments,",
           "satellites"],
          ["millions of real", "transactions, as a complement"]]),
    ]'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Les trois matières premières",
        sub="Aucune ne suffit ; la statistique moderne les marie",
        note="L'enquête pour la rapidité, le registre pour l'exactitude, la donnée massive pour la finesse —\\n"
             "et une cuisine commune : désaisonnalisation, imputations, effets de qualité."),
    "en": dict(
        title="The three raw materials",
        sub="None is enough; modern statistics marries them",
        note="The survey for speed, the register for accuracy, big data for fine detail —\\n"
             "and a common kitchen: seasonal adjustment, imputations, quality effects."),
}

def build_figure(cards: list[tuple[str, str, list[list[str]]]], lang: str) -> Figure:
    """Schéma : trois cartes (enquête, registre, donnée massive) au liseré codé couleur."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1078)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 505, 63, 53
    top, bottom = 800, 235
    for i, (name, color_key, paras) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS[color_key], lw=2.6, radius=26)
        ax.text(x + 52, top - 62, name, ha="left", va="center",
                fontsize=32, fontweight="bold", color=nm.COLORS["text"])
        y = top - 165
        for para in paras:
            for line in para:
                ax.text(x + 52, y, line, ha="left", va="center", fontsize=25, color=nm.COLORS["muted"])
                y -= 55
            y -= 42

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(raw_materials(LANG), LANG)'''


# ── Figure 05 — le mois type de l'investisseur (calendrier stylisé, embarqué) ─

DATA_5 = '''def calendar(lang: str) -> dict:
    """Calendrier stylisé : quatre lignes (période racontée), points datés et libellés, localisé.
    Stylized calendar: four lanes (period told), dated dots and labels, localized."""
    lanes_fr = ["sur le mois\\nEN COURS", "sur le mois\\nÉCOULÉ", "sur le trimestre\\nécoulé",
                "sur la semaine\\npassée"]
    lanes_en = ["on the current\\nmonth", "on the past\\nmonth", "on the past\\nquarter",
                "on the past\\nweek"]
    # (jour, ligne 0-3, couleur, libellé au-dessus, libellé en dessous)
    if lang == "fr":
        dots = [
            (23, 0, "rose", "PMI flash\\n(≈ 85 % des réponses)", "vers le 23"),
            (31, 0, "blue", "inflation flash\\nzone euro", "fin de mois"),
            (5, 1, "blue", "rapport\\nemploi", "1er vendredi"),
            (12, 1, "blue", "inflation\\nIPC", "vers le 12"),
            (16, 1, "blue", "ventes\\nau détail", "vers le 16"),
            (28, 1, "blue", "inflation\\nPCE", "vers le 28"),
            (27, 2, "blue", "vers le 27", "PIB trimestriel — 1re estimation,\\npuis 2e et 3e les mois suivants"),
        ]
        claims = "inscriptions au chômage — chaque jeudi"
        leg = ["donnée « dure » (activité réalisée)", "enquête d'opinion (donnée « molle »)"]
        xlab = "jour du mois"
    else:
        dots = [
            (23, 0, "rose", "flash PMI\\n(≈ 85% of responses)", "around the 23rd"),
            (31, 0, "blue", "euro-area\\nflash inflation", "end of month"),
            (5, 1, "blue", "jobs\\nreport", "1st Friday"),
            (12, 1, "blue", "CPI\\ninflation", "around the 12th"),
            (16, 1, "blue", "retail\\nsales", "around the 16th"),
            (28, 1, "blue", "PCE\\ninflation", "around the 28th"),
            (27, 2, "blue", "around the 27th", "quarterly GDP — 1st estimate,\\nthen 2nd and 3rd the next months"),
        ]
        claims = "jobless claims — every Thursday"
        leg = ["hard data (realized activity)", "opinion survey (soft data)"]
        xlab = "day of the month"
    lanes = lanes_fr if lang == "fr" else lanes_en
    return dict(lanes=lanes, dots=dots, claims=claims, legend=leg, xlab=xlab)'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le mois type de l'investisseur",
        sub="Calendrier américain stylisé : chaque publication raconte une autre période",
        note="Dates typiques (elles varient de quelques jours selon les mois). La plupart des chiffres américains\\n"
             "tombent à 8 h 30 à Washington, 14 h 30 à Paris. Plus une donnée arrive tôt, plus elle est provisoire."),
    "en": dict(
        title="The investor's typical month",
        sub="Stylized American calendar: each release tells a different period",
        note="Typical dates (they vary by a few days each month). Most American figures drop at 8:30 a.m. in\\n"
             "Washington, 2:30 p.m. in Paris. The earlier a datum arrives, the more provisional it is."),
}

def build_figure(cal: dict, lang: str) -> Figure:
    """Calendrier stylisé : quatre lignes datées, points « durs » (bleu) et « molle » (rose)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1263)
    ax = nm.axes(fig, left=0.19, bottom=0.155)
    ax.grid(False)
    ax.set_xlim(0.5, 33)
    ax.set_ylim(-0.2, 4.35)
    lane_y = [3.7, 2.55, 1.4, 0.55]
    for y, name in zip(lane_y, cal["lanes"]):
        ax.plot([1, 32], [y, y], color=nm.COLORS["edge"], linewidth=1.4, alpha=0.7, zorder=1)
        ax.text(-0.02, y, name, transform=ax.get_yaxis_transform(), ha="right", va="center",
                fontsize=21, fontstyle="italic", color=nm.COLORS["muted"], linespacing=1.3)
    for day, lane, color_key, above, below in cal["dots"]:
        y = lane_y[lane]
        ax.scatter([day], [y], s=340, color=nm.COLORS[color_key], zorder=4)
        ax.annotate(above, (day, y), xytext=(0, 46), textcoords="offset points", ha="center",
                    va="bottom", fontsize=22, fontweight="bold", color=nm.COLORS[color_key],
                    linespacing=1.25)
        ax.annotate(below, (day, y), xytext=(0, -30), textcoords="offset points", ha="center",
                    va="top", fontsize=20, color=nm.COLORS["muted"], linespacing=1.25)
    # Ligne « semaine passée » : quatre jeudis en gris.
    for day in (4, 11, 18, 25):
        ax.scatter([day], [lane_y[3]], s=300, color="#9fb0c9", zorder=4)
    ax.annotate(cal["claims"], (14.5, lane_y[3]), xytext=(0, -34), textcoords="offset points",
                ha="center", va="top", fontsize=22, fontweight="bold", color=nm.COLORS["text"])
    ax.set_xticks([1, 5, 10, 15, 20, 25, 31])
    ax.set_xticklabels((["1er"] if lang == "fr" else ["1st"]) + ["5", "10", "15", "20", "25", "31"])
    ax.set_yticks([])
    ax.set_xlabel(cal["xlab"])
    for spine in ("left", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="x", length=0)
    # Légende en haut à gauche.
    lx, ly = 2.0, 4.15
    for i, (color_key, label) in enumerate(zip(["blue", "rose"], cal["legend"])):
        yy = ly - i * 0.32
        ax.scatter([lx], [yy], s=280, color=nm.COLORS[color_key], zorder=5)
        ax.text(lx + 0.8, yy, label, ha="left", va="center", fontsize=22, color=nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(calendar(LANG), LANG)'''


# ── Figure 06 — tôt, riche, définitif (nuage stylisé, embarqué) ───────────────

DATA_6 = '''def releases() -> list[tuple[float, float, str]]:
    """Positions stylisées des grandes publications : (délai en jours, ampleur des révisions 0-3, couleur).
    Stylized positions of major releases: (lag in days, revision magnitude 0-3, colour)."""
    return [
        (-8, 1.05, "rose"),    # PMI flash
        (8, 0.32, "grey"),     # inscriptions au chômage
        (13, 0.95, "blue"),    # IPC
        (16, 2.00, "blue"),    # ventes au détail
        (11, 2.62, "blue"),    # rapport emploi
        (30, 3.02, "blue"),    # PIB — 1re estimation
        (90, 2.00, "blue"),    # PIB — 3e estimation
    ]

points = releases()'''

FIG_6 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Tôt, riche, définitif : aucun chiffre n'offre les trois",
        sub="Grandes publications américaines : délai de parution et ampleur des révisions",
        names=["PMI flash", "inscriptions au chômage", "IPC", "ventes au détail", "rapport emploi",
               "PIB — 1re estimation", "PIB — 3e estimation"],
        ylabels=["quasi\\ndéfinitif", "retouches\\nlégères", "révisions\\nsensibles", "peut changer\\nl'histoire"],
        xlabels=["fin de la\\npériode", "+15 j", "+30 j", "+60 j", "+90 j"],
        before="publié AVANT la fin\\nde la période mesurée",
        after="publié après la fin de la période",
        block_hi="riche mais mouvant : les grands chiffres « durs »\\nsont publiés vite... puis révisés longtemps",
        block_lo="rapide et stable : guichets administratifs\\net enquêtes — mais les uns sont étroits,\\nles autres ne mesurent qu'un ressenti",
        note="Positions stylisées, à lire comme des ordres de grandeur. L'IPC brut n'est pratiquement jamais révisé ;\\n"
             "PIB et emploi le sont pendant des années. Bleu : activité réalisée. Rouge : enquêtes d'opinion."),
    "en": dict(
        title="Early, rich, final: no number offers all three",
        sub="Major US releases: publication lag and size of revisions",
        names=["PMI flash", "jobless claims", "CPI", "retail sales", "jobs report",
               "GDP — 1st estimate", "GDP — 3rd estimate"],
        ylabels=["near-\\nfinal", "light\\ntouch-ups", "sensitive\\nrevisions", "can change\\nhistory"],
        xlabels=["end of the\\nperiod", "+15 d", "+30 d", "+60 d", "+90 d"],
        before="published BEFORE the end\\nof the measured period",
        after="published after the end of the period",
        block_hi="rich but moving: the big « hard » numbers\\nare published fast... then revised for years",
        block_lo="fast and stable: administrative counters\\nand surveys — but the former are narrow,\\nthe latter measure only a feeling",
        note="Stylized positions, to read as orders of magnitude. Raw CPI is almost never revised; GDP and\\n"
             "employment are revised for years. Blue: realized activity. Red: opinion surveys."),
}

def build_figure(points: list[tuple[float, float, str]], lang: str) -> Figure:
    """Nuage stylisé : délai de parution (x) vs ampleur des révisions (y), publications datées."""
    text = LABELS[lang]
    palette = {"blue": nm.COLORS["blue"], "rose": nm.COLORS["rose"], "grey": "#9fb0c9"}
    # (dx, dy, ha, va) en unités de données pour placer chaque libellé autour de son point.
    offsets = [(0, -0.32, "center", "top"), (4, -0.26, "left", "top"), (0, 0.28, "center", "bottom"),
               (0, 0.30, "center", "bottom"), (0, 0.30, "center", "bottom"), (3, 0, "left", "center"),
               (-3, 0.17, "right", "bottom")]
    fig = nm.figure(height_px=1310)
    ax = nm.axes(fig, left=0.135, bottom=0.185)
    ax.grid(True, color=nm.COLORS["grid"], linewidth=1.0)
    ax.set_xlim(-16, 98)
    ax.set_ylim(-0.15, 3.7)
    ax.axvline(0, color=nm.COLORS["muted"], linestyle=(0, (5, 4)), linewidth=2.0, alpha=0.85, zorder=1)
    for (x, y, key), name, (dx, dy, ha, va) in zip(points, text["names"], offsets):
        ax.scatter([x], [y], s=430, color=palette[key], zorder=4)
        ax.text(x + dx, y + dy, name, ha=ha, va=va, fontsize=23, fontweight="bold", color=palette[key])
    ax.set_xticks([0, 15, 30, 60, 90])
    ax.set_xticklabels(text["xlabels"], linespacing=1.2)
    ax.set_yticks([0.2, 1.05, 2.0, 3.0])
    ax.set_yticklabels(text["ylabels"], linespacing=1.2)
    ax.tick_params(length=0)
    # Repères des deux moitiés (avant / après la fin de période).
    ax.text(-9, 3.45, text["before"], ha="center", va="center", fontsize=20,
            fontstyle="italic", color=nm.COLORS["muted"], linespacing=1.25)
    ax.text(6, 3.52, text["after"], ha="left", va="center", fontsize=20,
            fontstyle="italic", color=nm.COLORS["muted"])
    ax.text(55, 2.72, text["block_hi"], ha="center", va="center", fontsize=21,
            color=nm.COLORS["muted"], linespacing=1.35)
    ax.text(60, 0.72, text["block_lo"], ha="center", va="center", fontsize=21,
            color=nm.COLORS["muted"], linespacing=1.35)
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(points, LANG)'''


# ── Figure 07 — le trimestre qui a changé de signe (millésimes, embarqué) ─────

DATA_7 = '''import pandas as pd
from pandas import Timestamp

def gdp_vintages() -> dict:
    """Croissance annualisée des T1 et T2 2022 (série BEA A191RL1Q225SBEA), telle que
    lue à chaque date, d'après les millésimes ALFRED. Valeurs en escalier (steps-post).
    Annualized growth of Q1 and Q2 2022 as read at each date, from ALFRED vintages."""
    t1 = [("2022-07-28", -1.4), ("2022-08-25", -1.5), ("2022-09-29", -1.6),
          ("2023-09-28", -2.0), ("2024-10-30", -1.0), ("2026-06-30", -1.0)]
    t2 = [("2022-07-28", -0.9), ("2022-08-25", -0.6), ("2024-09-26", 0.3),
          ("2025-06-26", 0.6), ("2026-06-30", 0.6)]
    to_series = lambda pts: ([Timestamp(d) for d, _ in pts], [v for _, v in pts])
    return dict(t1=to_series(t1), t2=to_series(t2))

vintages = gdp_vintages()'''

FIG_7 = '''import pandas as pd
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="Le trimestre qui a changé de signe",
        sub="Croissance des T1 et T2 2022 aux États-Unis, selon la date de lecture",
        leg_t1="croissance du 1er trimestre 2022", leg_t2="croissance du 2e trimestre 2022",
        above="au-dessus de zéro : l'économie croît", below="en dessous : elle se contracte",
        zero="0 %", ann_t1="sept. 2023 : le T1\\ns'enfonce à −2,0 %", lab_t1="T1 à −1,0 %",
        ann_t2="sept. 2024 : le T2 repasse\\nAU-DESSUS de zéro", read26="lecture de 2026 :\\nT2 à +0,6 %",
        head="été 2022 : deux trimestres négatifs à la une\\n— la fameuse « récession technique »",
        xlab="date à laquelle on lit les données",
        xticks=["mi-2022", "2023", "2024", "2025", "2026", "mi-2026"],
        note="Données réelles millésimées : Bureau of Economic Analysis, via ALFRED (série A191RL1Q225SBEA).\\n"
             "Révisions successives : la « récession technique » de 2022 a fini par disparaître des données."),
    "en": dict(
        title="The quarter that changed sign",
        sub="Growth of Q1 and Q2 2022 in the US, by the date read",
        leg_t1="Q1 2022 growth", leg_t2="Q2 2022 growth",
        above="above zero: the economy grows", below="below: it contracts",
        zero="0%", ann_t1="Sept. 2023: Q1\\nsinks to −2.0%", lab_t1="Q1 at −1.0%",
        ann_t2="Sept. 2024: Q2 climbs\\nBACK ABOVE zero", read26="2026 reading:\\nQ2 at +0.6%",
        head="summer 2022: two negative quarters in the headlines\\n— the famous « technical recession »",
        xlab="date on which the data are read",
        xticks=["mid-2022", "2023", "2024", "2025", "2026", "mid-2026"],
        note="Real vintage data: Bureau of Economic Analysis, via ALFRED (series A191RL1Q225SBEA).\\n"
             "Successive revisions: the 2022 « technical recession » ended up vanishing from the data."),
}

def build_figure(vintages: dict, lang: str) -> Figure:
    """Courbes en escalier : T1 (bleu) et T2 (rose) 2022, révisées de négatives à positives."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1250)
    ax = nm.axes(fig, left=0.10, bottom=0.165)
    x1, y1 = vintages["t1"]
    x2, y2 = vintages["t2"]
    ax.axhline(0, color=nm.COLORS["text"], linewidth=1.8, zorder=2)
    ax.step(x1, y1, where="post", color=nm.COLORS["blue"], linewidth=3.0, label=text["leg_t1"], zorder=4)
    ax.scatter(x1, y1, s=90, color=nm.COLORS["blue"], zorder=5)
    ax.step(x2, y2, where="post", color=nm.COLORS["rose"], linewidth=3.0, label=text["leg_t2"], zorder=4)
    ax.scatter(x2, y2, s=90, color=nm.COLORS["rose"], zorder=5)
    ax.set_xlim(pd.Timestamp("2022-06-01"), pd.Timestamp("2026-07-20"))
    ax.set_ylim(-2.25, 1.2)
    ax.set_yticks([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0])
    fmt = (lambda v, _: f"{v:+.1f} %".replace(".", ",").replace("+0,0 %", "0,0 %")) if lang == "fr" \\
        else (lambda v, _: f"{v:+.1f}%".replace("+0.0%", "0.0%"))
    ax.yaxis.set_major_formatter(FuncFormatter(fmt))
    xt = [pd.Timestamp(d) for d in ("2022-07-01", "2023-01-01", "2024-01-01", "2025-01-01",
                                    "2026-01-01", "2026-07-01")]
    ax.set_xticks(xt)
    ax.set_xticklabels(text["xticks"])
    ax.set_xlabel(text["xlab"])
    ax.grid(True, color=nm.COLORS["grid"], linewidth=1.0)
    # Repères et annotations.
    ax.text(pd.Timestamp("2022-09-15"), 0.24, text["above"], ha="left", va="center",
            fontsize=21, color=nm.COLORS["muted"])
    ax.text(pd.Timestamp("2022-09-15"), -0.28, text["below"], ha="left", va="center",
            fontsize=21, color=nm.COLORS["muted"])
    ax.text(pd.Timestamp("2026-06-20"), 0.06, text["zero"], ha="right", va="bottom",
            fontsize=24, color=nm.COLORS["text"])
    ax.text(pd.Timestamp("2023-01-15"), -1.28, text["ann_t1"], ha="left", va="center",
            fontsize=22, fontweight="bold", color=nm.COLORS["blue"], linespacing=1.35)
    ax.text(pd.Timestamp("2025-02-01"), -0.86, text["lab_t1"], ha="left", va="center",
            fontsize=23, fontweight="bold", color=nm.COLORS["blue"])
    ax.annotate(text["ann_t2"], xy=(pd.Timestamp("2024-09-26"), 0.3),
                xytext=(pd.Timestamp("2025-01-01"), -0.62), ha="left", va="center",
                fontsize=22, fontweight="bold", color=nm.COLORS["rose"], linespacing=1.35,
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["rose"], lw=1.8))
    ax.text(pd.Timestamp("2024-11-01"), 0.92, text["read26"], ha="left", va="center",
            fontsize=22, fontweight="bold", color=nm.COLORS["rose"], linespacing=1.35)
    ax.text(pd.Timestamp("2022-07-10"), -1.9, text["head"], ha="left", va="top",
            fontsize=22, fontweight="bold", color=nm.COLORS["text"], linespacing=1.35)
    legend = ax.legend(loc="upper left", fontsize=21, frameon=True, handlelength=1.8,
                       borderpad=0.9, labelspacing=0.6, bbox_to_anchor=(0.015, 0.98))
    legend.get_frame().set_facecolor(nm.COLORS["card"])
    legend.get_frame().set_edgecolor(nm.COLORS["edge"])
    for txt in legend.get_texts():
        txt.set_color(nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(vintages, LANG)'''


# ── Figure 08 — 2024, raconté deux fois (millésimes, embarqué) ────────────────

DATA_8 = '''def jobs_2024() -> tuple[list[float], list[float], float]:
    """Créations d'emplois mensuelles aux États-Unis en 2024 (série BLS PAYEMS), en milliers :
    première estimation, estimation de mi-2026 (millésimes ALFRED), et l'incertitude BLS.
    U.S. monthly job gains in 2024 (thousands): first estimate, mid-2026 estimate, BLS error band."""
    first = [353, 275, 303, 175, 272, 206, 114, 142, 254, 12, 227, 256]
    revised = [175, 207, 228, 63, 78, 87, 54, 8, 155, 33, 133, 237]
    return first, revised, 130.0

first, revised, err = jobs_2024()'''

FIG_8 = '''from matplotlib.figure import Figure
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="2024, raconté deux fois",
        sub="Emplois créés chaque mois aux États-Unis : annoncé (bleu) contre retenu (rouge)",
        months=["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
        legend_first="première estimation — cumul annoncé : ≈ +2,59 millions",
        legend_rev="estimation de mi-2026 — cumul restant : ≈ +1,46 million",
        note="Données réelles millésimées : BLS via ALFRED/FRED (série PAYEMS). Barres fines : l'incertitude publiée\\n"
             "par le BLS (± 130 000). L'écart bleu-rouge vient des réponses tardives et des recalages annuels."),
    "en": dict(
        title="2024, told twice",
        sub="Jobs created each month in the US: announced (blue) versus retained (red)",
        months=["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."],
        legend_first="first estimate — announced total: ≈ +2.59 million",
        legend_rev="mid-2026 estimate — remaining total: ≈ +1.46 million",
        note="Real vintage data: BLS via ALFRED/FRED (series PAYEMS). Thin bars: the uncertainty published by\\n"
             "the BLS (± 130,000). The blue-red gap comes from late responses and annual benchmarks."),
}

def build_figure(first: list[float], revised: list[float], err: float, lang: str) -> Figure:
    """Barres groupées : 12 mois, première estimation (bleu, ± 130 k) vs estimation de mi-2026 (rouge)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1316)
    ax = nm.axes(fig, left=0.10, bottom=0.11)
    ax.grid(axis="x", visible=False)
    groups = range(len(first))
    width = 0.4
    fpos = [g - width / 2 for g in groups]
    rpos = [g + width / 2 for g in groups]
    ax.bar(fpos, first, width=width, color=nm.COLORS["blue"], zorder=3)
    ax.errorbar(fpos, first, yerr=err, fmt="none", ecolor=nm.COLORS["muted"], elinewidth=1.6,
                capsize=6, capthick=1.6, zorder=4)
    ax.bar(rpos, revised, width=width, color=nm.COLORS["rose"], zorder=3)
    ax.axhline(0, color=nm.COLORS["text"], linewidth=1.6)
    ax.set_ylim(-160, 500)
    ax.set_yticks([-100, 0, 100, 200, 300, 400])
    fmt = (lambda v, _: f"{v:+.0f} k".replace("+0 k", "0 k")) if lang == "fr" \\
        else (lambda v, _: f"{v:+.0f}k".replace("+0k", "0k"))
    ax.yaxis.set_major_formatter(FuncFormatter(fmt))
    ax.set_xlim(-0.6, len(first) - 0.4)
    ax.set_xticks(list(groups))
    ax.set_xticklabels(text["months"], fontsize=21)
    ax.tick_params(axis="x", length=0)
    handles = [Patch(facecolor=nm.COLORS["blue"], label=text["legend_first"]),
               Patch(facecolor=nm.COLORS["rose"], label=text["legend_rev"])]
    legend = ax.legend(handles=handles, loc="upper right", fontsize=21, frameon=False,
                       handlelength=1.2, handleheight=1.2, labelspacing=0.7)
    for txt in legend.get_texts():
        txt.set_color(nm.COLORS["text"])
    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(first, revised, err, LANG)'''


# ── Figure 09 — de l'imprécision au mensonge (schéma trois cartes) ────────────

DATA_9 = '''def trust_continuum(lang: str) -> list[tuple[str, str, list[str]]]:
    """Le continuum de la confiance : (titre, couleur, lignes), localisé.
    The trust continuum: (title, colour, lines), localized."""
    if lang == "fr":
        return [
            ("Erreurs honnêtes", "blue",
             ["débats de mesure publics :", "Boskin 1996 — IPC surestimé",
              "d'environ 1,1 point par an ;", "loyers intégrés avec un an", "de retard (2021-2023)"]),
            ("La zone grise", "muted",
             ["loi de Goodhart : une mesure", "devenue objectif cesse d'être",
              "une bonne mesure —", "un chiffre surveillé est un", "chiffre qu'on a intérêt à travailler"]),
            ("Chiffres sous influence", "rose",
             ["Grèce 2009 : déficit 3,7 %", "→ 15,4 % du PIB ;",
              "Argentine : censure du FMI", "(2013) ; PIB provincial chinois", "« fabriqué par l'homme »"]),
        ]
    return [
        ("Honest errors", "blue",
         ["public measurement debates:", "Boskin 1996 — CPI overstated",
          "by about 1.1 points a year;", "rents entering the index", "a year late (2021-2023)"]),
        ("The gray zone", "muted",
         ["Goodhart's law: a measure", "turned into a target ceases",
          "to be a good measure —", "a watched number is one", "worth working"]),
        ("Numbers under influence", "rose",
         ["Greece 2009: deficit 3.7%", "→ 15.4% of GDP;",
          "Argentina: IMF censure", "(2013); « man-made »", "Chinese provincial GDP"]),
    ]'''

FIG_9 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="De l'imprécision au mensonge : un continuum",
        sub="La fiabilité se juge à la transparence, pas à l'exactitude",
        arrow="la confiance s'érode — et se paie en prime de risque",
        note="Le jour où un institut cesse de réviser, ne publie plus ses méthodes ou fait taire ses\\n"
             "contradicteurs, c'est ce jour-là qu'il faut s'inquiéter."),
    "en": dict(
        title="From imprecision to lie: a continuum",
        sub="Reliability is judged by transparency, not accuracy",
        arrow="trust erodes — and is paid for in a risk premium",
        note="The day an institute stops revising, no longer publishes its methods or silences its\\n"
             "critics is the day to worry."),
}

def build_figure(cards: list[tuple[str, str, list[str]]], lang: str) -> Figure:
    """Schéma : trois cartes (erreurs honnêtes → zone grise → chiffres sous influence) + flèche."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1078)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 505, 63, 53
    top, bottom = 835, 335
    for i, (name, color_key, lines) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS[color_key], lw=2.6, radius=26)
        ax.text(x + 52, top - 62, name, ha="left", va="center",
                fontsize=30, fontweight="bold", color=nm.COLORS["text"])
        for j, line in enumerate(lines):
            ax.text(x + 52, top - 158 - j * 66, line, ha="left", va="center",
                    fontsize=24, color=nm.COLORS["muted"])

    ax.annotate("", xy=(1620, 250), xytext=(280, 250),
                arrowprops=dict(arrowstyle="-|>", color=nm.COLORS["muted"], lw=2.4))
    ax.text(nm.WIDTH_PX / 2, 185, text["arrow"], ha="center", va="center",
            fontsize=24, fontstyle="italic", color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(trust_continuum(LANG), LANG)'''


# ── Figure 10 — six réflexes de lecture (schéma six cartes) ───────────────────

DATA_10 = '''def reflexes(lang: str) -> list[list[str]]:
    """Les six réflexes de lecture d'un chiffre macro (deux lignes chacun), localisés.
    The six reflexes for reading a macro number (two lines each), localized."""
    if lang == "fr":
        return [
            ["Identifiez ce que vous lisez :", "niveau ou variation ? brut ou CVS ?"],
            ["Comparez au consensus —", "jamais à zéro ni au mois passé"],
            ["Respectez la marge d'erreur :", "3 mois = début de signal"],
            ["La première estimation sera", "révisée : conviction provisoire"],
            ["Croisez le mou et le dur :", "une enquête seule est une humeur"],
            ["En backtest : les données de", "l'époque (ALFRED), pas d'aujourd'hui"],
        ]
    return [
        ["Identify what you are reading:", "level or change? raw or adjusted?"],
        ["Compare to the consensus —", "never to zero nor the previous month"],
        ["Respect the margin of error:", "3 months = start of a signal"],
        ["The first estimate will be", "revised: provisional conviction"],
        ["Cross the soft and the hard:", "one survey alone is a mood"],
        ["In backtests: the data of the", "time (ALFRED), not today's"],
    ]'''

FIG_10 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Six réflexes de lecture",
        sub="Le mode d'emploi qui tient sur une carte",
        note="Les portes d'entrée gratuites : FRED et ALFRED (Fed de Saint-Louis), Eurostat, BCE, INSEE —\\n"
             "et un calendrier économique pour l'heure, le consensus et la valeur précédente."),
    "en": dict(
        title="Six reading reflexes",
        sub="The user manual that fits on a card",
        note="The free gateways: FRED and ALFRED (St. Louis Fed), Eurostat, ECB, INSEE —\\n"
             "and an economic calendar for the time, the consensus and the previous value."),
}

def build_figure(rows: list[list[str]], lang: str) -> Figure:
    """Schéma : six cartes numérotées (deux colonnes, trois rangées), un réflexe par carte."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1102)
    ax = nm.blank_axes(fig)

    card_w, card_h, gap = 740, 175, 45
    col_x = [100, 907]
    top0 = 820
    for i, lines in enumerate(rows):
        col, row = i % 2, i // 2
        x = col_x[col]
        card_top = top0 - row * (card_h + gap)
        nm.card(ax, x, card_top - card_h, card_w, card_h, edge=nm.COLORS["edge"], lw=2.2, radius=22)
        ax.text(x + 66, card_top - card_h / 2, str(i + 1), ha="center", va="center",
                fontsize=42, fontweight="bold", color=nm.COLORS["blue"])
        for j, line in enumerate(lines):
            ax.text(x + 150, card_top - card_h / 2 + 28 - j * 56, line, ha="left", va="center",
                    fontsize=25, color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(reflexes(LANG), LANG)'''


FIGURES = [
    dict(name="fig01-embargo-8h30", fig_fr="8 h 30 à Washington",
         fig_en="8:30 a.m. in Washington", live=False, data=DATA_1, fig=FIG_1),
    dict(name="fig02-chiffre-manufacture", fig_fr="Un chiffre macro est un produit manufacturé",
         fig_en="A macro number is a manufactured product", live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-carte-producteurs", fig_fr="Qui fabrique les chiffres macro ?",
         fig_en="Who makes the macro numbers?", live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-trois-matieres-premieres", fig_fr="Les trois matières premières",
         fig_en="The three raw materials", live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-calendrier-macro", fig_fr="Le mois type de l'investisseur",
         fig_en="The investor's typical month", live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-rapidite-fiabilite", fig_fr="Tôt, riche, définitif : aucun chiffre n'offre les trois",
         fig_en="Early, rich, final: no number offers all three", live=False, data=DATA_6, fig=FIG_6),
    dict(name="fig07-pib-2022-revisions", fig_fr="Le trimestre qui a changé de signe",
         fig_en="The quarter that changed sign", live=False, data=DATA_7, fig=FIG_7),
    dict(name="fig08-emplois-revisions", fig_fr="2024, raconté deux fois",
         fig_en="2024, told twice", live=False, data=DATA_8, fig=FIG_8),
    dict(name="fig09-continuum-confiance", fig_fr="De l'imprécision au mensonge : un continuum",
         fig_en="From imprecision to lie: a continuum", live=False, data=DATA_9, fig=FIG_9),
    dict(name="fig10-six-reflexes", fig_fr="Six réflexes de lecture",
         fig_en="Six reading reflexes", live=False, data=DATA_10, fig=FIG_10),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out6")
    nb_kit.build_all(META, DIR, FIGURES)
