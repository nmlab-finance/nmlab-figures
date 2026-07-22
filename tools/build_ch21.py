#!/usr/bin/env python3
"""Notebooks du chapitre 21 — « Qu'est-ce que la monnaie ? Origines et fonctions ».

Huit figures, toutes des schémas conceptuels éditables (aucune série FRED en direct) :
timeline, cartes, tableau, T-comptes et barres d'agrégats. Chaque notebook = une seule
cellule code (load_*() puis build_figure(...) -> Figure), style NMLab partagé.
"""

import sys

sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit


# ═════════════════════════════════════════════════════════════════════════════
# Figure 01 — six mois sans banques : la grève bancaire irlandaise de 1970
# ═════════════════════════════════════════════════════════════════════════════

DATA_1 = '''def strike_cards(lang: str) -> list[tuple[str, str]]:
    """Les trois enseignements de la grève : (titre, corps), localisés.
    The three lessons of the strike: (title, body), localized."""
    if lang == "fr":
        return [
            ("Comptes gelés",
             "Les dépôts restent inscrits,\\nmais les comptes deviennent\\ninaccessibles et les chèques ne\\nsont plus compensés."),
            ("Chèques sur réputation",
             "Commerçants et pubs acceptent\\nles chèques de clients connus ;\\nquelques-uns sont endossés et\\ncirculent."),
            ("Créances en attente",
             "Le risque s'accumule, mais\\nl'échange survit grâce à la\\nconfiance locale et à un\\nrèglement futur attendu."),
        ]
    return [
        ("Frozen accounts",
         "Deposits stay recorded, but\\naccounts become inaccessible\\nand cheques are no longer\\ncleared."),
        ("Cheques on reputation",
         "Shopkeepers and pubs accept\\ncheques from known customers;\\na few are endorsed and\\ncirculate."),
        ("Claims awaiting clearing",
         "Risk accumulates, but exchange\\nsurvives through local trust\\nand an expected future\\nsettlement."),
    ]'''

FIG_1 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Six mois et demi sans banques — l'économie tient",
        sub="Irlande, 1970 : les quatre grandes banques de compensation ferment ; les chèques circulent sur la réputation.",
        left_date="1er mai 1970", left_sub="Fermeture",
        right_date="17 nov. 1970", right_sub="Réouverture",
        pill="≈ 200 jours",
        note="Quatre banques restent fermées 200 jours : la monnaie n'est pas l'objet « billet » mais une\\n"
             "architecture de comptes, de promesses et de confiance."),
    "en": dict(
        title="Six and a half months without banks — the economy holds",
        sub="Ireland, 1970: the four main clearing banks close; cheques circulate on reputation.",
        left_date="1 May 1970", left_sub="Closure",
        right_date="17 Nov. 1970", right_sub="Reopening",
        pill="≈ 200 days",
        note="Four banks stay closed for 200 days: money is not the « banknote » object but an\\n"
             "architecture of accounts, promises and trust."),
}

def build_figure(cards: list[tuple[str, str]], lang: str) -> Figure:
    """Frise de la fermeture (dot rose → dot bleu) puis trois cartes d'enseignements."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1040)
    ax = nm.blank_axes(fig)

    # Frise : ligne, deux jalons, pastille centrale.
    y = 695
    ax.plot([205, 1540], [y, y], color=nm.COLORS["edge"], linewidth=3, zorder=1)
    ax.scatter([178], [y], s=300, color=nm.COLORS["rose"], zorder=3, clip_on=False)
    ax.scatter([1568], [y], s=300, color=nm.COLORS["blue"], zorder=3, clip_on=False)
    nm.card(ax, 758, y - 39, 232, 78, edge=nm.COLORS["blue"], radius=39, lw=2.4)
    ax.text(874, y, text["pill"], ha="center", va="center", fontsize=30,
            fontweight="bold", color=nm.COLORS["blue"], zorder=4)
    ax.text(90, y + 62, text["left_date"], ha="left", va="center", fontsize=28,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(120, y - 62, text["left_sub"], ha="left", va="center", fontsize=23, color=nm.COLORS["muted"])
    ax.text(1660, y + 62, text["right_date"], ha="right", va="center", fontsize=28,
            fontweight="bold", color=nm.COLORS["text"])
    ax.text(1628, y - 62, text["right_sub"], ha="right", va="center", fontsize=23, color=nm.COLORS["muted"])

    # Trois cartes d'enseignements.
    card_w, gap, x0 = 515, 35, 65
    top, bottom = 552, 215
    for i, (title, body) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS["edge"], lw=2.2, radius=22)
        ax.text(x + 42, top - 56, title, ha="left", va="center", fontsize=30,
                fontweight="bold", color=nm.COLORS["text"])
        ax.text(x + 42, top - 150, body, ha="left", va="top", fontsize=24,
                color=nm.COLORS["muted"], linespacing=1.5)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(strike_cards(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 02 — trois fonctions, trois épreuves
# ═════════════════════════════════════════════════════════════════════════════

DATA_2 = '''def function_panels(lang: str) -> list[str]:
    """Les titres des trois panneaux (unité de compte, intermédiaire, réserve), localisés.
    The three panel titles (unit of account, medium, store of value), localized."""
    if lang == "fr":
        return ["Unité de compte", "Intermédiaire", "Réserve de valeur"]
    return ["Unit of account", "Medium of exchange", "Store of value"]'''

FIG_2 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Trois fonctions, trois épreuves",
        sub="Compter les prix, séparer la vente de l'achat, transporter le pouvoir d'achat dans le temps.",
        goods="10 biens", prices="prix bilatéraux", versus="contre", common="avec une unité commune",
        sep="La vente et l'achat\\nsont séparés",
        box1="Vendre son pain → monnaie", box2="Monnaie → acheter plus tard",
        accepted="Un actif accepté parce que\\nd'autres l'accepteront.",
        infl="Inflation zone euro", date="oct. 2022", later="un an plus tard",
        before="100 €", after="≈ 90 €",
        note="Dix biens exigent 45 prix bilatéraux, un seul avec une unité monétaire ; l'inflation érode\\n"
             "ensuite le pouvoir d'achat conservé."),
    "en": dict(
        title="Three functions, three tests",
        sub="Count prices, separate sale from purchase, carry purchasing power through time.",
        goods="10 goods", prices="bilateral prices", versus="versus", common="with a common unit",
        sep="Sale and purchase\\nare separated",
        box1="Sell your bread → money", box2="Money → buy later",
        accepted="An asset accepted because\\nothers will accept it.",
        infl="Euro-area inflation", date="Oct. 2022", later="a year later",
        before="€100", after="≈ €90",
        note="Ten goods require 45 bilateral prices, just one with a monetary unit; inflation then\\n"
             "erodes the purchasing power stored."),
}

def build_figure(panels: list[str], lang: str) -> Figure:
    """Trois panneaux : le calcul 45 vs 10, l'échange en deux temps, l'érosion par l'inflation."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1080)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 512, 35, 65
    top, bottom = 822, 162
    cx = [x0 + i * (card_w + gap) + card_w / 2 for i in range(3)]
    for i in range(3):
        x = x0 + i * (card_w + gap)
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS["edge"], lw=2.2, radius=22)
        ax.text(cx[i], top - 52, panels[i], ha="center", va="center", fontsize=30,
                fontweight="bold", color=nm.COLORS["blue"])

    # Panneau 1 — 45 prix bilatéraux contre 10.
    ax.text(cx[0], 668, text["goods"], ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])
    ax.text(cx[0], 600, "45", ha="center", va="center", fontsize=68, fontweight="bold", color=nm.COLORS["text"])
    ax.text(cx[0], 528, text["prices"], ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])
    ax.text(cx[0], 440, text["versus"], ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])
    ax.text(cx[0], 372, "10", ha="center", va="center", fontsize=60, fontweight="bold", color=nm.COLORS["blue"])
    ax.text(cx[0], 292, text["common"], ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])

    # Panneau 2 — l'échange en deux temps.
    ax.text(cx[1], 672, text["sep"], ha="center", va="center", fontsize=24,
            color=nm.COLORS["muted"], linespacing=1.4)
    nm.card(ax, cx[1] - 195, 530, 390, 66, edge=nm.COLORS["edge"], fill=nm.COLORS["bg"], radius=14, lw=2)
    ax.text(cx[1], 563, text["box1"], ha="center", va="center", fontsize=23, color=nm.COLORS["text"])
    ax.text(cx[1], 480, "▼", ha="center", va="center", fontsize=30, color=nm.COLORS["blue"])
    nm.card(ax, cx[1] - 195, 400, 390, 66, edge=nm.COLORS["edge"], fill=nm.COLORS["bg"], radius=14, lw=2)
    ax.text(cx[1], 433, text["box2"], ha="center", va="center", fontsize=23, color=nm.COLORS["text"])
    ax.text(cx[1], 320, text["accepted"], ha="center", va="center", fontsize=24,
            color=nm.COLORS["muted"], linespacing=1.4)

    # Panneau 3 — l'inflation érode le pouvoir d'achat.
    ax.text(cx[2], 675, text["infl"], ha="center", va="center", fontsize=24, color=nm.COLORS["muted"])
    ax.text(cx[2], 615, text["date"], ha="center", va="center", fontsize=22, color=nm.COLORS["muted"])
    ax.text(cx[2], 545, "10,6 %" if lang == "fr" else "10.6%", ha="center", va="center",
            fontsize=62, fontweight="bold", color=nm.COLORS["rose"])
    ax.text(cx[2], 460, text["later"], ha="center", va="center", fontsize=23, color=nm.COLORS["muted"])
    nm.card(ax, cx[2] - 150, 345, 95, 95, edge=nm.COLORS["blue"], fill=nm.COLORS["blue"], radius=12)
    nm.card(ax, cx[2] + 55, 345, 95, 95, edge=nm.COLORS["rose"], fill=nm.COLORS["rose"], radius=12)
    ax.annotate("", xy=(cx[2] + 48, 392), xytext=(cx[2] - 48, 392),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["muted"], lw=2.2))
    ax.text(cx[2] - 102, 300, text["before"], ha="center", va="center", fontsize=23, color=nm.COLORS["muted"])
    ax.text(cx[2] + 102, 300, text["after"], ha="center", va="center", fontsize=23, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(function_panels(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 03 — quatre jalons, quatre voies vers la monnaie
# ═════════════════════════════════════════════════════════════════════════════

DATA_3 = '''def milestones(lang: str) -> list[tuple[str, str, str, str]]:
    """Les quatre jalons : (badge, couleur, titre, corps), localisés.
    The four milestones: (badge, color, title, body), localized."""
    if lang == "fr":
        return [
            ("COMPTER", nm.COLORS["blue"], "Comptes d'Uruk",
             "Rations, loyers et\\ndettes comptabilisés en\\nunités de céréales ou\\nd'argent, bien avant la\\npièce."),
            ("PROMETTRE", nm.COLORS["teal"], "Prêt de 3 kg\\nd'argent",
             "Mésopotamie : crédit et\\npaiement différé\\nattestés sur tablettes\\nd'argile."),
            ("STANDARDISER", nm.COLORS["amber"], "Pièces lydiennes",
             "Électrum, ouest de\\nl'Anatolie, vers la fin\\ndu VIIᵉ s. av. J.-C. :\\npoids et marque\\nauthentifiés."),
            ("TRANSFÉRER", nm.COLORS["rose"], "Jiaozi (Song du\\nNord)",
             "XIᵉ siècle : les jiaozi\\nprivés précèdent la\\npremière monnaie de\\npapier publique."),
        ]
    return [
        ("COUNT", nm.COLORS["blue"], "Uruk accounts",
         "Rations, rents and\\ndebts recorded in units\\nof grain or silver, long\\nbefore the coin."),
        ("PROMISE", nm.COLORS["teal"], "3 kg silver loan",
         "Mesopotamia: credit\\nand deferred payment\\nattested on clay\\ntablets."),
        ("STANDARDIZE", nm.COLORS["amber"], "Lydian coins",
         "Electrum, western\\nAnatolia, around the\\nend of the 7th c. BCE:\\nweight and mark\\nauthenticated."),
        ("TRANSFER", nm.COLORS["rose"], "Jiaozi (Northern\\nSong)",
         "11th century: private\\njiaozi precede the first\\npublic paper money."),
    ]'''

FIG_3 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Quatre jalons, quatre voies vers la monnaie",
        sub="Ni troc universel ni inventeur unique : compter, promettre, standardiser et transférer se répondent.",
        note="Quatre jalons documentent des voies distinctes ; la pièce frappée n'invente pas la monnaie,\\n"
             "elle standardise et authentifie des pratiques déjà anciennes."),
    "en": dict(
        title="Four milestones, four paths to money",
        sub="Neither universal barter nor a single inventor: counting, promising, standardizing and transferring answer one another.",
        note="Four milestones document distinct paths; the struck coin does not invent money,\\n"
             "it standardizes and authenticates already-old practices."),
}

def build_figure(cards: list[tuple[str, str, str, str]], lang: str) -> Figure:
    """Quatre cartes à badge coloré (compter, promettre, standardiser, transférer)."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1010)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 388, 25, 65
    top, bottom = 745, 225
    for i, (badge, color, title, body) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS["edge"], lw=2.2, radius=22)
        # Badge : pastille arrondie au liseré coloré.
        bw = 14 * len(badge) + 44
        nm.card(ax, cx - bw / 2, top - 78, bw, 48, edge=color, fill=nm.COLORS["card"], radius=24, lw=2.2)
        ax.text(cx, top - 54, badge, ha="center", va="center", fontsize=20,
                fontweight="bold", color=color)
        ax.text(cx, top - 160, title, ha="center", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["text"], linespacing=1.35)
        ax.text(cx, top - 290, body, ha="center", va="top", fontsize=23,
                color=nm.COLORS["muted"], linespacing=1.5)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(milestones(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 04 — billet, dépôt, carte, réserves : un tableau comparatif
# ═════════════════════════════════════════════════════════════════════════════

DATA_4 = '''def money_table(lang: str) -> tuple[list[str], list[str], list[list[str]]]:
    """Tableau comparatif : (colonnes, lignes, cellules[ligne][colonne]), localisé.
    Comparison table: (columns, rows, cells[row][col]), localized."""
    if lang == "fr":
        cols = ["Billet", "Dépôt bancaire", "Carte", "Réserves"]
        rows = ["Nature", "Émetteur", "Détenteur", "Rôle", "Cours légal"]
        cells = [
            ["Monnaie fiduciaire", "Créance sur la\\nbanque", "Instruction de\\ntransfert", "Monnaie de banque\\ncentrale"],
            ["Banque centrale", "Banque commerciale", "Réseau / banque", "Banque centrale"],
            ["Public", "Client", "Client", "Banques"],
            ["Paiement final", "Paiement scriptural", "Déplace un dépôt", "Règlement\\ninterbancaire"],
            ["Oui (valeur faciale)", "Non", "Non", "—"],
        ]
        return cols, rows, cells
    cols = ["Banknote", "Bank deposit", "Card", "Reserves"]
    rows = ["Nature", "Issuer", "Holder", "Role", "Legal tender"]
    cells = [
        ["Fiat money", "Claim on the bank", "Transfer instruction", "Central bank money"],
        ["Central bank", "Commercial bank", "Network / bank", "Central bank"],
        ["Public", "Customer", "Customer", "Banks"],
        ["Final payment", "Book-money payment", "Moves a deposit", "Interbank\\nsettlement"],
        ["Yes (face value)", "No", "No", "—"],
    ]
    return cols, rows, cells'''

FIG_4 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Quatre objets, un même euro — pas le même statut",
        sub="Billet, dépôt, carte et réserves diffèrent par leur émetteur, leur nature et leur statut juridique.",
        note="Tous sont libellés en euros, mais l'émetteur, la nature de la créance et le statut légal\\n"
             "diffèrent — d'où l'importance de distinguer monnaie et moyen de paiement."),
    "en": dict(
        title="Four objects, one euro — not the same status",
        sub="A banknote, deposit, card and reserves differ by their issuer, their nature and their legal status.",
        note="All are denominated in euros, but the issuer, the nature of the claim and the legal status\\n"
             "differ — hence the importance of distinguishing money from means of payment."),
}

def build_figure(table: tuple, lang: str) -> Figure:
    """Tableau : quatre colonnes (objets) × cinq lignes (propriétés)."""
    text = LABELS[lang]
    cols, rows, cells = table
    fig = nm.figure(height_px=1150)
    ax = nm.blank_axes(fig)

    col_cx = [528, 858, 1188, 1518]
    head_y = 874
    for c, name in enumerate(cols):
        nm.card(ax, col_cx[c] - 150, head_y - 39, 300, 78, edge=nm.COLORS["edge"],
                fill=nm.COLORS["card"], radius=14, lw=2)
        ax.text(col_cx[c], head_y, name, ha="center", va="center", fontsize=26,
                fontweight="bold", color=nm.COLORS["text"])

    row_y = [745, 629, 513, 397, 281]
    for r, label in enumerate(rows):
        ax.plot([65, 1685], [row_y[r] + 58, row_y[r] + 58], color=nm.COLORS["edge"],
                linewidth=1.2, alpha=0.7, zorder=1)
        ax.text(88, row_y[r], label, ha="left", va="center", fontsize=24,
                fontweight="bold", color=nm.COLORS["muted"])
        for c in range(4):
            value = cells[r][c]
            highlight = (label in ("Cours légal", "Legal tender") and c == 0)
            ax.text(col_cx[c], row_y[r], value, ha="center", va="center", fontsize=24,
                    color=nm.COLORS["amber"] if highlight else nm.COLORS["text"],
                    fontweight="bold" if highlight else "normal", linespacing=1.35)
    ax.plot([65, 1685], [row_y[-1] - 58, row_y[-1] - 58], color=nm.COLORS["edge"],
            linewidth=1.2, alpha=0.7, zorder=1)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(money_table(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 05 — pourquoi 1 € en vaut toujours 1 € (parité au pair)
# ═════════════════════════════════════════════════════════════════════════════

DATA_5 = '''def parity_pillars(lang: str) -> list[tuple[str, str]]:
    """Les trois piliers de la parité au pair : (titre, corps), localisés.
    The three pillars of par convertibility: (title, body), localized."""
    if lang == "fr":
        return [
            ("Stabilité des prix", "Une cible d'inflation de 2 %\\nancre la valeur de l'unité de\\ncompte."),
            ("Garantie des dépôts", "Jusqu'à 100 000 € par déposant\\net par banque dans l'Union."),
            ("Règlement en réserves", "Les banques soldent entre\\nelles en monnaie de banque\\ncentrale."),
        ]
    return [
        ("Price stability", "A 2% inflation target anchors\\nthe value of the unit of\\naccount."),
        ("Deposit guarantee", "Up to €100,000 per depositor\\nand per bank in the Union."),
        ("Settlement in reserves", "Banks settle among\\nthemselves in central bank\\nmoney."),
    ]'''

FIG_5 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Pourquoi 1 € en vaut toujours 1 €",
        sub="Un dépôt vaut le même euro d'une banque à l'autre, et se convertit au pair en espèces.",
        box1="Espèces", box2="Dépôt banque A", box3="Dépôt banque B", val="1 €",
        bridge="...parce que trois piliers soutiennent la parité",
        note="La parité 1:1 n'a rien de spontané : stabilité des prix, garantie des dépôts et règlement en\\n"
             "réserves rendent interchangeables des passifs privés hétérogènes."),
    "en": dict(
        title="Why €1 is always worth €1",
        sub="A deposit is worth the same euro from one bank to the next, and converts at par into cash.",
        box1="Cash", box2="Bank A deposit", box3="Bank B deposit", val="€1",
        bridge="...because three pillars support the parity",
        note="The 1:1 parity is nothing spontaneous: price stability, deposit protection and settlement in\\n"
             "reserves make heterogeneous private liabilities interchangeable."),
}

def build_figure(pillars: list[tuple[str, str]], lang: str) -> Figure:
    """Rangée « espèces = dépôt A = dépôt B », puis trois piliers de la parité."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1030)
    ax = nm.blank_axes(fig)

    # Rangée d'équivalences.
    cy, bw, bh = 650, 420, 150
    boxes = [(122, text["box1"], nm.COLORS["amber"]),
             (660, text["box2"], nm.COLORS["blue"]),
             (1198, text["box3"], nm.COLORS["blue2"])]
    for x, name, color in boxes:
        nm.card(ax, x, cy - bh / 2, bw, bh, edge=color, radius=18, lw=2.6)
        ax.text(x + bw / 2, cy + 28, name, ha="center", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["text"])
        ax.text(x + bw / 2, cy - 32, text["val"], ha="center", va="center", fontsize=30,
                fontweight="bold", color=color)
    for xeq in (601, 1139):
        ax.text(xeq, cy, "=", ha="center", va="center", fontsize=44, color=nm.COLORS["muted"])

    ax.text(873, 492, text["bridge"], ha="center", va="center", fontsize=26, color=nm.COLORS["muted"])

    # Trois piliers.
    card_w, gap, x0 = 512, 35, 65
    top, bottom = 430, 125
    for i, (title, body) in enumerate(pillars):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS["edge"], lw=2.2, radius=22)
        ax.text(cx, top - 55, title, ha="center", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["blue"])
        ax.text(cx, top - 135, body, ha="center", va="top", fontsize=24,
                color=nm.COLORS["muted"], linespacing=1.5)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(parity_pillars(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 06 — un paiement déplace la monnaie, il n'en crée pas
# ═════════════════════════════════════════════════════════════════════════════

DATA_6 = '''def transfer_sides(lang: str) -> tuple[dict, dict]:
    """Les deux bilans du virement : (banque A, banque B), avec lignes et signes, localisés.
    The two balance sheets of the transfer: (Bank A, Bank B), localized."""
    if lang == "fr":
        a = dict(title="Banque A — Alice",
                 rows=[("Dépôt d'Alice", "− 100 €"), ("Réserves", "− 100 €")], color=nm.COLORS["rose"])
        b = dict(title="Banque B — Bilal",
                 rows=[("Dépôt de Bilal", "+ 100 €"), ("Réserves", "+ 100 €")], color=nm.COLORS["green"])
        return a, b
    a = dict(title="Bank A — Alice",
             rows=[("Alice's deposit", "− €100"), ("Reserves", "− €100")], color=nm.COLORS["rose"])
    b = dict(title="Bank B — Bilal",
             rows=[("Bilal's deposit", "+ €100"), ("Reserves", "+ €100")], color=nm.COLORS["green"])
    return a, b'''

FIG_6 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Un paiement déplace la monnaie, il n'en crée pas",
        sub="Alice (banque A) vire 100 € à Bilal (banque B) : aucun total ne varie dans le système.",
        flow="100 €", net="Création monétaire nette : 0",
        note="Le paiement vu par l'utilisateur et le règlement entre banques sont deux moments distincts :\\n"
             "les dépôts et les réserves se déplacent, leurs totaux restent constants."),
    "en": dict(
        title="A payment moves money, it does not create it",
        sub="Alice (Bank A) transfers €100 to Bilal (Bank B): no total changes in the system.",
        flow="€100", net="Net money creation: 0",
        note="The payment seen by the user and the settlement between banks are two distinct moments:\\n"
             "deposits and reserves move, their totals stay constant."),
}

def draw_bank(ax, x, w, top, bottom, side):
    """Une carte-bilan : titre puis deux lignes (libellé + montant signé coloré)."""
    nm.card(ax, x, bottom, w, top - bottom, edge=nm.COLORS["edge"], lw=2.2, radius=22)
    ax.text(x + w / 2, top - 55, side["title"], ha="center", va="center", fontsize=28,
            fontweight="bold", color=nm.COLORS["text"])
    for j, (label, amount) in enumerate(side["rows"]):
        ry = top - 150 - j * 110
        nm.card(ax, x + 40, ry - 39, w - 80, 78, edge=nm.COLORS["edge"], fill=nm.COLORS["bg"], radius=14, lw=1.8)
        ax.text(x + 70, ry, label, ha="left", va="center", fontsize=25, color=nm.COLORS["text"])
        ax.text(x + w - 70, ry, amount, ha="right", va="center", fontsize=27,
                fontweight="bold", color=side["color"])

def build_figure(sides: tuple[dict, dict], lang: str) -> Figure:
    """Deux bilans reliés par une flèche ; pastille « création nette : 0 »."""
    text = LABELS[lang]
    a, b = sides
    fig = nm.figure(height_px=1060)
    ax = nm.blank_axes(fig)

    top, bottom = 785, 375
    draw_bank(ax, 65, 620, top, bottom, a)
    draw_bank(ax, 1062, 620, top, bottom, b)

    ax.annotate("", xy=(1055, 635), xytext=(695, 635),
                arrowprops=dict(arrowstyle="->", color=nm.COLORS["blue"], lw=3))
    ax.text(875, 690, text["flow"], ha="center", va="center", fontsize=27,
            fontweight="bold", color=nm.COLORS["blue"])

    nm.card(ax, 538, 205, 670, 90, edge=nm.COLORS["green"], radius=45, lw=2.4)
    ax.text(873, 250, text["net"], ha="center", va="center", fontsize=29,
            fontweight="bold", color=nm.COLORS["green"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(transfer_sides(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 07 — le prêt crée le dépôt, pas la richesse (T-comptes)
# ═════════════════════════════════════════════════════════════════════════════

DATA_7 = '''def loan_stages(lang: str) -> list[dict]:
    """Les trois étapes du prêt : T-comptes (actif/passif) + légende, localisés.
    The three stages of the loan: T-accounts (asset/liability) + caption, localized."""
    G, R = nm.COLORS["green"], nm.COLORS["rose"]
    if lang == "fr":
        return [
            dict(num="1", title="À l'octroi (banque)",
                 al=("Prêt", "+ 100 000 €", G), pl=("Dépôt", "+ 100 000 €", G),
                 caption=("Un dépôt neuf = monnaie\\ncréée", nm.COLORS["text"])),
            dict(num="2", title="Côté emprunteur",
                 al=("Dépôt", "+ 100 000 €", G), pl=("Dette", "+ 100 000 €", R),
                 caption=("Patrimoine net : inchangé", nm.COLORS["amber"])),
            dict(num="3", title="Au remboursement",
                 al=("Prêt", "− 100 000 €", R), pl=("Dépôt", "− 100 000 €", R),
                 caption=("La monnaie est détruite", nm.COLORS["text"])),
        ]
    return [
        dict(num="1", title="On disbursement (bank)",
             al=("Loan", "+ €100,000", G), pl=("Deposit", "+ €100,000", G),
             caption=("A new deposit = money\\ncreated", nm.COLORS["text"])),
        dict(num="2", title="Borrower side",
             al=("Deposit", "+ €100,000", G), pl=("Debt", "+ €100,000", R),
             caption=("Net worth: unchanged", nm.COLORS["amber"])),
        dict(num="3", title="On repayment",
             al=("Loan", "− €100,000", R), pl=("Deposit", "− €100,000", R),
             caption=("The money is destroyed", nm.COLORS["text"])),
    ]'''

FIG_7 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="Le prêt crée le dépôt — pas la richesse",
        sub="Un crédit de 100 000 € inscrit d'un même geste un actif et un passif ; le remboursement les efface.",
        asset="Actif", liab="Passif",
        note="La comptabilité explique le dépôt, pas sa richesse : l'actif monétaire de l'emprunteur est\\n"
             "compensé par sa dette, et rembourser le principal détruit la monnaie créée."),
    "en": dict(
        title="The loan creates the deposit — not wealth",
        sub="A €100,000 loan records an asset and a liability in one move; repayment erases them.",
        asset="Asset", liab="Liability",
        note="The accounting explains the deposit, not the wealth: the borrower's monetary asset is\\n"
             "offset by their debt, and repaying the principal destroys the money created."),
}

def build_figure(stages: list[dict], lang: str) -> Figure:
    """Trois cartes numérotées, chacune un T-compte (actif | passif) et sa légende."""
    text = LABELS[lang]
    fig = nm.figure(height_px=1090)
    ax = nm.blank_axes(fig)

    card_w, gap, x0 = 512, 35, 65
    top, bottom = 832, 262
    for i, s in enumerate(stages):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        nm.card(ax, x, bottom, card_w, top - bottom, edge=nm.COLORS["edge"], lw=2.2, radius=22)
        # Badge numéroté.
        nm.card(ax, cx - 55, top - 77, 110, 50, edge=nm.COLORS["blue"], fill=nm.COLORS["card"], radius=25, lw=2.2)
        ax.text(cx, top - 52, s["num"], ha="center", va="center", fontsize=25,
                fontweight="bold", color=nm.COLORS["blue"])
        ax.text(cx, top - 130, s["title"], ha="center", va="center", fontsize=27,
                fontweight="bold", color=nm.COLORS["text"])
        # T-compte.
        ax.text(cx - 105, top - 235, text["asset"], ha="center", va="center", fontsize=22,
                fontweight="bold", color=nm.COLORS["muted"])
        ax.text(cx + 105, top - 235, text["liab"], ha="center", va="center", fontsize=22,
                fontweight="bold", color=nm.COLORS["muted"])
        ax.plot([cx - 200, cx + 200], [top - 262, top - 262], color=nm.COLORS["edge"], linewidth=1.4)
        ax.plot([cx, cx], [top - 218, top - 372], color=nm.COLORS["edge"], linewidth=1.4)
        al, av, ac = s["al"]
        pl, pv, pc = s["pl"]
        ax.text(cx - 105, top - 302, al, ha="center", va="center", fontsize=23, color=nm.COLORS["muted"])
        ax.text(cx - 105, top - 348, av, ha="center", va="center", fontsize=25, fontweight="bold", color=ac)
        ax.text(cx + 105, top - 302, pl, ha="center", va="center", fontsize=23, color=nm.COLORS["muted"])
        ax.text(cx + 105, top - 348, pv, ha="center", va="center", fontsize=25, fontweight="bold", color=pc)
        cap, cap_color = s["caption"]
        ax.text(cx, top - 460, cap, ha="center", va="center", fontsize=25,
                fontweight="bold", color=cap_color, linespacing=1.4)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(loan_stages(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 08 — M1, M2, M3 : des agrégats emboîtés + frise de l'euro numérique
# ═════════════════════════════════════════════════════════════════════════════

DATA_8 = '''def aggregates(lang: str) -> tuple[list[dict], list[tuple[str, str]]]:
    """Barres d'agrégats (M1/M2/M3) et frise de l'euro numérique, localisées.
    Aggregate bars (M1/M2/M3) and the digital-euro timeline, localized."""
    if lang == "fr":
        bars = [
            dict(name="M1", value=11000, label="11 000 Md€", color=nm.COLORS["blue"],
                 caption="Billets, pièces et dépôts à vue"),
            dict(name="M2", value=16000, label="16 000 Md€", color=nm.COLORS["teal"],
                 caption="+ dépôts à terme ≤ 2 ans et préavis ≤ 3 mois"),
            dict(name="M3", value=18000, label="18 000 Md€", color=nm.COLORS["amber"],
                 caption="+ pensions, OPC monétaires et titres ≤ 2 ans"),
        ]
        timeline = [
            ("2023", "Phase de\\npréparation"), ("oct. 2025", "Fin de la\\npréparation"),
            ("14 juil. 2026", "Pilote : 36 PSP\\nretenus"), ("S2 2027", "Test bêta\\ncontrôlé"),
            ("2029", "Émission\\npossible"),
        ]
        return bars, timeline
    bars = [
        dict(name="M1", value=11000, label="€11,000bn", color=nm.COLORS["blue"],
             caption="Banknotes, coins and overnight deposits"),
        dict(name="M2", value=16000, label="€16,000bn", color=nm.COLORS["teal"],
             caption="+ time deposits ≤ 2 yr and notice ≤ 3 mo"),
        dict(name="M3", value=18000, label="€18,000bn", color=nm.COLORS["amber"],
             caption="+ repos, MMF shares and securities ≤ 2 yr"),
    ]
    timeline = [
        ("2023", "Preparation\\nphase"), ("Oct. 2025", "End of\\npreparation"),
        ("14 Jul. 2026", "Pilot: 36 PSPs\\nselected"), ("H2 2027", "Controlled\\nbeta test"),
        ("2029", "Possible\\nissuance"),
    ]
    return bars, timeline'''

FIG_8 = '''from matplotlib.figure import Figure

LABELS = {
    "fr": dict(
        title="M1, M2, M3 : des agrégats emboîtés",
        sub="Zone euro, mai 2026 — du plus liquide (espèces, dépôts à vue) au plus large.",
        agg="agrégat", section="Euro numérique — un projet, pas un lancement",
        note="En mai 2026, M1 avoisine 11 000 Md€, M2 16 000 Md€ et M3 18 000 Md€ (arrondis) ; le pilote\\n"
             "de l'euro numérique reste un test, sans décision d'émission."),
    "en": dict(
        title="M1, M2, M3: nested aggregates",
        sub="Euro area, May 2026 — from most liquid (cash, overnight deposits) to broadest.",
        agg="aggregate", section="Digital euro — a project, not a launch",
        note="In May 2026, M1 is about €11,000bn, M2 €16,000bn and M3 €18,000bn (rounded); the digital\\n"
             "euro pilot remains a test, with no issuance decision."),
}

def build_figure(content: tuple, lang: str) -> Figure:
    """Trois barres horizontales emboîtées, puis la frise des jalons de l'euro numérique."""
    text = LABELS[lang]
    bars, timeline = content
    fig = nm.figure(height_px=1150)
    ax = nm.blank_axes(fig)

    # Barres d'agrégats (longueur proportionnelle à la valeur).
    x_left, x_max, vmax = 468, 1690, 18000
    bar_h, centers = 94, [808, 668, 528]
    for bar, cy in zip(bars, centers):
        length = bar["value"] / vmax * (x_max - x_left)
        nm.card(ax, x_left, cy - bar_h / 2, length, bar_h, edge=bar["color"],
                fill=bar["color"], radius=14)
        ax.text(68, cy + 8, bar["name"], ha="left", va="center", fontsize=38,
                fontweight="bold", color=bar["color"])
        ax.text(68, cy - 46, text["agg"], ha="left", va="center", fontsize=22, color=nm.COLORS["muted"])
        ax.text(x_left + length - 26, cy, bar["label"], ha="right", va="center", fontsize=34,
                fontweight="bold", color=nm.COLORS["bg"])
        ax.text(x_left, cy - bar_h / 2 - 30, bar["caption"], ha="left", va="center",
                fontsize=22, color=nm.COLORS["muted"])

    # Frise de l'euro numérique.
    ax.plot([65, 1685], [408, 408], color=nm.COLORS["edge"], linewidth=1.2, alpha=0.7)
    ax.text(68, 372, text["section"], ha="left", va="center", fontsize=26,
            fontweight="bold", color=nm.COLORS["text"])
    xs = [118, 490, 875, 1260, 1628]
    ax.plot([xs[0], xs[-1]], [250, 250], color=nm.COLORS["edge"], linewidth=2.5, zorder=1)
    for i, (date, sub) in enumerate(timeline):
        last = (i == len(timeline) - 1)
        color = nm.COLORS["amber"] if last else nm.COLORS["blue"]
        ax.scatter([xs[i]], [250], s=220, color=color, zorder=3)
        ax.text(xs[i], 308, date, ha="center", va="center", fontsize=23, fontweight="bold",
                color=nm.COLORS["amber"] if last else nm.COLORS["text"])
        ax.text(xs[i], 188, sub, ha="center", va="center", fontsize=21,
                color=nm.COLORS["muted"], linespacing=1.4)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig

build_figure(aggregates(LANG), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Assemblage
# ═════════════════════════════════════════════════════════════════════════════

META = dict(
    num="21",
    title_fr="Qu'est-ce que la monnaie ? Origines et fonctions",
    title_en="What Is Money? Origins and Functions",
    slug_fr="qu-est-ce-que-la-monnaie",
    slug_en="what-is-money",
)
DIR = "macro/21-qu-est-ce-que-la-monnaie"

FIGURES = [
    dict(name="fig01-greve-bancaire-irlande",
         fig_fr="Six mois et demi sans banques — l'économie tient",
         fig_en="Six and a half months without banks — the economy holds",
         live=False, data=DATA_1, fig=FIG_1),
    dict(name="fig02-trois-fonctions-monnaie",
         fig_fr="Trois fonctions, trois épreuves",
         fig_en="Three functions, three tests",
         live=False, data=DATA_2, fig=FIG_2),
    dict(name="fig03-quatre-jalons-monnaie",
         fig_fr="Quatre jalons, quatre voies vers la monnaie",
         fig_en="Four milestones, four paths to money",
         live=False, data=DATA_3, fig=FIG_3),
    dict(name="fig04-billet-depot-carte-reserves",
         fig_fr="Quatre objets, un même euro — pas le même statut",
         fig_en="Four objects, one euro — not the same status",
         live=False, data=DATA_4, fig=FIG_4),
    dict(name="fig05-parite-au-pair-euro",
         fig_fr="Pourquoi 1 € en vaut toujours 1 €",
         fig_en="Why €1 is always worth €1",
         live=False, data=DATA_5, fig=FIG_5),
    dict(name="fig06-virement-100-euros",
         fig_fr="Un paiement déplace la monnaie, il n'en crée pas",
         fig_en="A payment moves money, it does not create it",
         live=False, data=DATA_6, fig=FIG_6),
    dict(name="fig07-pret-cree-depot",
         fig_fr="Le prêt crée le dépôt — pas la richesse",
         fig_en="The loan creates the deposit — not wealth",
         live=False, data=DATA_7, fig=FIG_7),
    dict(name="fig08-agregats-m1-m2-m3",
         fig_fr="M1, M2, M3 : des agrégats emboîtés",
         fig_en="M1, M2, M3: nested aggregates",
         live=False, data=DATA_8, fig=FIG_8),
]


if __name__ == "__main__":
    nb_kit.test_all(FIGURES, "out21")
    nb_kit.build_all(META, DIR, FIGURES)
