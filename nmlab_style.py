"""Style NMLab pour matplotlib — reproduit le design system des figures de nmlab.io.

Usage (Colab ou local) :

    import nmlab_style as nm
    nm.setup()                        # police Inter + thème sombre NMLab
    fig = nm.figure(height_px=1045)
    ax  = nm.axes(fig)
    ax.plot(x, y, color=nm.COLORS["blue"])
    nm.header(fig, "Titre", "Sous-titre")
    nm.footer(fig, "Note de bas de figure. Source : FRED.")

Code sous licence MIT — © 2026 NMLab (nmlab.io).
"""

import io
import os
import zipfile
import urllib.request

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

# ── Tokens du design system ──────────────────────────────────────────────────
COLORS = {
    "bg":    "#0d1826",   # fond de figure
    "card":  "#17233a",   # cartes / encarts
    "edge":  "#31405c",   # liserés, axes, bandes de récession
    "text":  "#f3f6fb",   # titres
    "muted": "#8ba0bd",   # sous-titres, axes, notes
    "grid":  "#1e2e46",   # grille discrète
    "blue":  "#3399dd",
    "blue2": "#3f9fe0",
    "rose":  "#f46079",
    "amber": "#e6a93c",
    "teal":  "#39b3a6",
    "green": "#4bb573",
}

WIDTH_PX = 1747          # largeur standard des figures NMLab
DPI = 100

_INTER_ZIP = "https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
_INTER_WEIGHTS = ["Regular", "Medium", "SemiBold", "Bold", "ExtraBold"]


def _install_inter():
    """Télécharge Inter (une seule fois) et l'enregistre auprès de matplotlib."""
    cache = os.path.join(os.path.expanduser("~"), ".cache", "nmlab_fonts")
    os.makedirs(cache, exist_ok=True)
    paths = [os.path.join(cache, f"Inter-{w}.ttf") for w in _INTER_WEIGHTS]
    if not all(os.path.exists(p) for p in paths):
        data = urllib.request.urlopen(_INTER_ZIP, timeout=60).read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for w, path in zip(_INTER_WEIGHTS, paths):
                with open(path, "wb") as f:
                    f.write(z.read(f"extras/ttf/Inter-{w}.ttf"))
    for p in paths:
        font_manager.fontManager.addfont(p)


def setup():
    """Configure matplotlib : police Inter + thème sombre NMLab. Renvoie COLORS."""
    try:
        _install_inter()
        matplotlib.rcParams["font.family"] = "Inter"
    except Exception as exc:                          # pas de réseau → police par défaut
        print(f"[nmlab_style] Inter indisponible ({exc}) ; police par défaut.")
    matplotlib.rcParams.update({
        "figure.facecolor": COLORS["bg"],
        "savefig.facecolor": COLORS["bg"],
        "axes.facecolor":  COLORS["bg"],
        "axes.edgecolor":  COLORS["edge"],
        "axes.linewidth":  1.5,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.labelcolor": COLORS["muted"],
        "axes.labelsize":  20,
        "axes.grid":       True,
        "axes.axisbelow":  True,
        "grid.color":      COLORS["grid"],
        "grid.linewidth":  1.2,
        "xtick.color":       COLORS["edge"],
        "ytick.color":       COLORS["edge"],
        "xtick.labelcolor":  COLORS["muted"],
        "ytick.labelcolor":  COLORS["muted"],
        "xtick.labelsize":   20,
        "ytick.labelsize":   20,
        "text.color":      COLORS["text"],
        "font.size":       20,
        "lines.linewidth": 2.9,
        "figure.dpi":      DPI,
    })
    return COLORS


def figure(height_px=1045):
    """Figure au format NMLab : 1747 px de large, fond sombre."""
    return plt.figure(figsize=(WIDTH_PX / DPI, height_px / DPI), dpi=DPI)


def axes(fig, left=0.075, right=0.982, top=None, bottom=None):
    """Axes avec les marges standard (place pour le titre en haut, la note en bas)."""
    h = fig.get_size_inches()[1] * DPI
    if top is None:
        top = 1 - 258 / h
    if bottom is None:
        bottom = 160 / h
    return fig.add_axes([left, bottom, right - left, top - bottom])


def header(fig, title, subtitle=None):
    """Titre gras haut-gauche + sous-titre gris, comme sur les figures du site."""
    h = fig.get_size_inches()[1] * DPI
    fig.text(0.0458, 1 - 38 / h, title, fontsize=36, fontweight=800,
             color=COLORS["text"], va="top", ha="left")
    if subtitle:
        fig.text(0.0458, 1 - 102 / h, subtitle, fontsize=21.5,
                 color=COLORS["muted"], va="top", ha="left")


def footer(fig, note=None, signature=True):
    """Note interne bas-gauche + signature « ▪ NMLab » bas-droite."""
    h = fig.get_size_inches()[1] * DPI
    if note:
        fig.text(0.0458, 14 / h, note, fontsize=16.5, color=COLORS["muted"],
                 va="bottom", ha="left", linespacing=1.65)
    if signature:
        fig.text(0.9715, 14 / h, "▪ NMLab", fontsize=16.5,
                 color=COLORS["muted"], va="bottom", ha="right")


def blank_axes(fig):
    """Toile plein cadre en coordonnées PIXELS (origine bas-gauche, y vers le haut),
    sans axes ni grille — pour les figures-schémas (cartes, encadrés).

    1 unité de données = 1 pixel dans les deux directions, donc les coins arrondis
    de ``card`` restent circulaires sans avoir à forcer l'aspect."""
    h = fig.get_size_inches()[1] * DPI
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH_PX)
    ax.set_ylim(0, h)
    ax.axis("off")
    return ax


def card(ax, x, y, w, h, *, edge, fill=None, lw=2.4, radius=16):
    """Carte arrondie au style NMLab, occupant exactement [x, x+w] × [y, y+h]
    (coordonnées pixels de ``blank_axes``). ``edge`` = couleur du liseré."""
    box = FancyBboxPatch(
        (x + radius, y + radius), w - 2 * radius, h - 2 * radius,
        boxstyle=f"round,pad={radius},rounding_size={radius}",
        linewidth=lw, edgecolor=edge,
        facecolor=fill if fill else COLORS["card"], zorder=2)
    ax.add_patch(box)
    return box


def thousands(lang="fr"):
    """Formateur de milliers pour les axes : 845 000 (fr) / 845,000 (en)."""
    from matplotlib.ticker import FuncFormatter
    if lang == "fr":
        return FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " "))
    return FuncFormatter(lambda v, _: f"{v:,.0f}")
