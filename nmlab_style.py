"""Style NMLab pour matplotlib — reproduit le design system des figures de nmlab.io.

Usage (Colab ou local) :

    import nmlab_style as nm
    nm.setup()                              # police Inter + thème sombre NMLab
    gdp = nm.load_fred("GDPC1", start="2000")
    fig = nm.figure(height_px=1045)
    ax = nm.axes(fig)
    ax.plot(gdp.index, gdp, color=nm.COLORS["blue"])
    nm.header(fig, "Titre", "Sous-titre")
    nm.footer(fig, "Note de bas de figure. Source : FRED.")

Module partagé par tous les notebooks Colab du dépôt. Code sous licence MIT
— © 2026 NMLab (nmlab.io).
"""

from __future__ import annotations

import io
import os
import urllib.request
import zipfile
from typing import TYPE_CHECKING

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import Formatter, FuncFormatter

if TYPE_CHECKING:                       # imports réservés au typage / typing-only imports
    import pandas as pd

# ── Tokens du design system ──────────────────────────────────────────────────
COLORS: dict[str, str] = {
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

WIDTH_PX = 1747          # largeur standard des figures NMLab (px)
DPI = 100

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"

_INTER_ZIP = "https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
_INTER_WEIGHTS = ("Regular", "Medium", "SemiBold", "Bold", "ExtraBold")


def _install_inter() -> None:
    """Télécharge Inter (une seule fois, en cache) et l'enregistre auprès de matplotlib."""
    cache = os.path.join(os.path.expanduser("~"), ".cache", "nmlab_fonts")
    os.makedirs(cache, exist_ok=True)
    paths = [os.path.join(cache, f"Inter-{weight}.ttf") for weight in _INTER_WEIGHTS]
    if not all(os.path.exists(path) for path in paths):
        archive = urllib.request.urlopen(_INTER_ZIP, timeout=60).read()
        with zipfile.ZipFile(io.BytesIO(archive)) as zf:
            for weight, path in zip(_INTER_WEIGHTS, paths):
                with open(path, "wb") as out:
                    out.write(zf.read(f"extras/ttf/Inter-{weight}.ttf"))
    for path in paths:
        font_manager.fontManager.addfont(path)


def setup() -> dict[str, str]:
    """Configure matplotlib (police Inter + thème sombre NMLab) ; renvoie ``COLORS``."""
    try:
        _install_inter()
        matplotlib.rcParams["font.family"] = "Inter"
    except Exception as exc:                          # pas de réseau → police par défaut
        print(f"[nmlab_style] Inter indisponible ({exc}) ; police par défaut.")
    matplotlib.rcParams.update({
        "figure.facecolor":  COLORS["bg"],
        "savefig.facecolor": COLORS["bg"],
        "axes.facecolor":    COLORS["bg"],
        "axes.edgecolor":    COLORS["edge"],
        "axes.linewidth":    1.5,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.labelcolor":   COLORS["muted"],
        "axes.labelsize":    20,
        "axes.grid":         True,
        "axes.axisbelow":    True,
        "grid.color":        COLORS["grid"],
        "grid.linewidth":    1.2,
        "xtick.color":       COLORS["edge"],
        "ytick.color":       COLORS["edge"],
        "xtick.labelcolor":  COLORS["muted"],
        "ytick.labelcolor":  COLORS["muted"],
        "xtick.labelsize":   20,
        "ytick.labelsize":   20,
        "text.color":        COLORS["text"],
        "font.size":         20,
        "lines.linewidth":   2.9,
        "figure.dpi":        DPI,
    })
    return COLORS


def load_fred(series_id: str, start: str | None = None) -> pd.Series:
    """Charge une série FRED (CSV public, sans clé API) en ``pandas.Series`` datée.

    ``start`` (ex. ``"1995"``) tronque le début de l'historique.
    Load a FRED series as a date-indexed pandas Series; ``start`` trims the history.
    """
    import pandas as pd

    series = pd.read_csv(
        FRED_CSV.format(series_id), index_col="observation_date", parse_dates=True
    )[series_id]
    return series.loc[start:] if start else series


def figure(height_px: int = 1045) -> Figure:
    """Figure au format NMLab : 1747 px de large, fond sombre."""
    return plt.figure(figsize=(WIDTH_PX / DPI, height_px / DPI), dpi=DPI)


def axes(
    fig: Figure,
    left: float = 0.075,
    right: float = 0.982,
    top: float | None = None,
    bottom: float | None = None,
) -> Axes:
    """Axes aux marges standard : place réservée au titre (haut) et à la note (bas)."""
    height_px = fig.get_size_inches()[1] * DPI
    if top is None:
        top = 1 - 258 / height_px
    if bottom is None:
        bottom = 160 / height_px
    return fig.add_axes([left, bottom, right - left, top - bottom])


def header(fig: Figure, title: str, subtitle: str | None = None) -> None:
    """Titre gras (Inter ExtraBold) haut-gauche + sous-titre gris, façon nmlab.io."""
    height_px = fig.get_size_inches()[1] * DPI
    fig.text(0.0458, 1 - 38 / height_px, title, fontsize=36, fontweight=800,
             color=COLORS["text"], va="top", ha="left")
    if subtitle:
        fig.text(0.0458, 1 - 102 / height_px, subtitle, fontsize=21.5,
                 color=COLORS["muted"], va="top", ha="left")


def footer(fig: Figure, note: str | None = None, signature: bool = True) -> None:
    """Note interne bas-gauche (optionnelle) + signature « ▪ NMLab » bas-droite."""
    height_px = fig.get_size_inches()[1] * DPI
    if note:
        fig.text(0.0458, 14 / height_px, note, fontsize=16.5, color=COLORS["muted"],
                 va="bottom", ha="left", linespacing=1.65)
    if signature:
        fig.text(0.9715, 14 / height_px, "▪ NMLab", fontsize=16.5,
                 color=COLORS["muted"], va="bottom", ha="right")


def blank_axes(fig: Figure) -> Axes:
    """Toile plein cadre en coordonnées PIXELS (origine bas-gauche, y vers le haut),
    sans axes ni grille — pour les figures-schémas (cartes, encadrés).

    1 unité de données = 1 pixel dans les deux directions, donc les coins arrondis
    de ``card`` restent circulaires sans avoir à forcer l'aspect.
    """
    height_px = fig.get_size_inches()[1] * DPI
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH_PX)
    ax.set_ylim(0, height_px)
    ax.axis("off")
    return ax


def card(
    ax: Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    edge: str,
    fill: str | None = None,
    lw: float = 2.4,
    radius: float = 16,
) -> FancyBboxPatch:
    """Carte arrondie au style NMLab, occupant exactement ``[x, x+w] × [y, y+h]``
    (coordonnées pixels de ``blank_axes``). ``edge`` = couleur du liseré.
    """
    box = FancyBboxPatch(
        (x + radius, y + radius), w - 2 * radius, h - 2 * radius,
        boxstyle=f"round,pad={radius},rounding_size={radius}",
        linewidth=lw, edgecolor=edge,
        facecolor=fill or COLORS["card"], zorder=2,
    )
    ax.add_patch(box)
    return box


def thousands(lang: str = "fr") -> Formatter:
    """Formateur d'axe pour les grands nombres : ``845 000`` (fr) / ``845,000`` (en)."""
    if lang == "fr":
        return FuncFormatter(lambda value, _: f"{value:,.0f}".replace(",", " "))
    return FuncFormatter(lambda value, _: f"{value:,.0f}")
