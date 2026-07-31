#!/usr/bin/env python3
"""Notebooks de l'enquête « L'or monte-t-il parce que les monnaies s'effondrent ? ».

Quatre figures reproductibles à partir de sources publiques : trois graphiques
en direct (or de la Banque mondiale + change H.10 de la Réserve fédérale + M2)
et une décomposition comptable dont les parts sont celles publiées.

Les figures 3 et 4 de l'article demandent les huit IPC et les huit agrégats de
monnaie large locaux : leurs séries ne sont pas reconstructibles ici (voir le
compte rendu de session) et ne sont donc pas incluses.
"""

import sys

sys.path.insert(0, "/home/claudeagent/cms-workspace/nmlab-figures-tools")
import nb_kit

META = dict(num="", title_fr="L'or monte-t-il parce que les monnaies s'effondrent ?",
            title_en="Is gold rising because currencies are collapsing?",
            slug_fr="prix-de-l-or-et-effondrement-des-monnaies",
            slug_en="prix-de-l-or-et-effondrement-des-monnaies")

DIR = "marches/prix-de-l-or-et-effondrement-des-monnaies"


def intro_md(meta, fig_fr, fig_en, live=True, source=None):
    """Intro adaptée à une enquête hors série (pas de numéro de chapitre, pas de version anglaise)."""
    art = f"https://nmlab.io/ressources/{meta['slug_fr']}"
    if source:
        run_fr = f"la figure se régénère à partir des **{source[0]}**"
        run_en = f"rebuild the figure from **{source[1]}**"
    elif live:
        run_fr = "la figure se régénère avec les **données publiques du jour**"
        run_en = "rebuild the figure with **today's public data**"
    else:
        run_fr = "la figure est régénérée par le code — un **schéma éditable** : changez les libellés à votre guise"
        run_en = "rebuild the figure from code — an **editable diagram**: change the labels as you like"
    return f"""# {fig_fr} · *{fig_en}*

Notebook compagnon de l'enquête **{meta['title_fr']}** — [lire l'article]({art}).
Companion notebook to the study **{meta['title_en']}**.

**Exécutez l'unique cellule ci-dessous** (bouton ▶ ou Ctrl+Entrée) : {run_fr}. Passez `LANG = "en"` en tête de cellule pour les libellés anglais. — Run the single cell below (▶ or Ctrl+Enter) to {run_en}; set `LANG = "en"` at the top for English labels.

Code : licence MIT · © 2026 [NMLab](https://nmlab.io) · dépôt [nmlab-finance/nmlab-figures](https://github.com/nmlab-finance/nmlab-figures)"""


nb_kit.intro_md = intro_md          # l'enquête n'est pas un chapitre numéroté


# ═════════════════════════════════════════════════════════════════════════════
# Chargeurs communs — or (Banque mondiale) et change H.10 (Réserve fédérale)
# ═════════════════════════════════════════════════════════════════════════════

LOADERS = '''import io
import re
import urllib.request
from functools import lru_cache

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

CMO_PAGE = "https://www.worldbank.org/en/research/commodity-markets"
CMO_FILE = ("https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026"
            "/related/CMO-Historical-Data-Monthly.xlsx")
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"

# H.10 : EUR, GBP et AUD sont cotés en dollars par unité étrangère — on les inverse
# pour obtenir partout des unités locales par dollar, comme dans l'article.
# H.10 quotes EUR, GBP and AUD as dollars per foreign unit: invert them so every
# series is local units per dollar, as in the article.
FX = {"EUR": ("DEXUSEU", True), "JPY": ("DEXJPUS", False), "GBP": ("DEXUSUK", True),
      "CHF": ("DEXSZUS", False), "CAD": ("DEXCAUS", False), "AUD": ("DEXUSAL", True),
      "CNY": ("DEXCHUS", False)}


def _fetch(url: str, tries: int = 5, headers: dict | None = None,
           data: str | None = None) -> bytes:
    """Télécharge une URL, avec reprises. Deux pièges de ces diffuseurs publics :
    la connexion peut être coupée sans raison, et un quota (HTTP 429) peut s'appliquer
    quand plusieurs personnes partagent la même adresse — d'où l'attente plus longue.
    Download with retries: connections get dropped, and shared addresses can hit HTTP 429.
    """
    import time
    for attempt in range(tries):
        try:
            request = urllib.request.Request(url, headers=headers or {},
                                             data=data.encode() if data else None)
            return urllib.request.urlopen(request, timeout=120).read()
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == tries - 1:
                raise
            print(f"[or] quota atteint chez le diffuseur, nouvelle tentative dans "
                  f"{20 * (attempt + 1)} s…")
            time.sleep(20 * (attempt + 1))
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(3 * (attempt + 1))
    raise RuntimeError("unreachable")


@lru_cache(maxsize=None)
def load_gold_usd() -> Series:
    """Or en dollars par once, moyennes mensuelles depuis 1960.

    Source : « Commodity Price Data » (Pink Sheet) de la Banque mondiale, feuille
    « Monthly Prices », colonne Gold — le fixing de Londres, en accès libre.
    World Bank Pink Sheet, monthly London gold price in US dollars per troy ounce.
    """
    try:
        raw = _fetch(CMO_FILE)
    except Exception:                                  # millésime renouvelé : on relit le lien
        page = _fetch(CMO_PAGE).decode("utf-8", "ignore")
        link = re.search(r"https://[^\\"']*CMO-Historical-Data-Monthly\\.xlsx", page)
        raw = _fetch(link.group(0))
    table = pd.read_excel(io.BytesIO(raw), sheet_name="Monthly Prices", skiprows=4)
    table = table.rename(columns={table.columns[0]: "date"})[["date", "Gold"]].dropna()
    dates = pd.to_datetime(table["date"].str.replace("M", "-"), format="%Y-%m")
    return Series(table["Gold"].values, index=dates).astype(float)


@lru_cache(maxsize=None)
def load_fred(series_id: str) -> Series:
    """Série FRED (CSV public, sans clé) ramenée à des moyennes mensuelles.
    A FRED series (public CSV, no key) averaged to monthly frequency."""
    table = pd.read_csv(io.StringIO(_fetch(FRED_CSV.format(series_id)).decode()))
    values = pd.to_numeric(table[table.columns[1]], errors="coerce")
    series = Series(values.values, index=pd.to_datetime(table[table.columns[0]])).dropna()
    return series.resample("MS").mean()


def load_gold_in_currencies(start: str, end: str) -> DataFrame:
    """Prix de l'or dans les huit devises du panier, mois par mois.

    Chaque prix local est le produit de la moyenne mensuelle de l'or en dollars
    et de la moyenne mensuelle du taux de change — l'ordre des opérations retenu
    par l'article. Le dollar vaut 1 par construction.
    Gold priced in the eight basket currencies, month by month.
    """
    gold = load_gold_usd()
    prices = {"USD": gold}
    for code, (series_id, invert) in FX.items():
        rate = load_fred(series_id)
        prices[code] = gold * (1 / rate if invert else rate)
    return DataFrame(prices).loc[start:end].dropna()


def effective_index(prices: DataFrame) -> Series:
    """Indice or effectif : moyenne géométrique équipondérée des huit prix locaux,
    base 100 au premier mois. Seule la moyenne géométrique garantit que l'indice
    des devises mesurées contre l'or est exactement l'inverse de celui-ci.
    Equal-weighted geometric mean of the eight local prices, first month = 100.
    """
    return 100 * np.exp(np.log(prices / prices.iloc[0]).mean(axis=1))'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 1 — l'or dans huit devises
# ═════════════════════════════════════════════════════════════════════════════

DATA_1 = LOADERS

FIG_1 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FixedLocator, FuncFormatter

START, END = "1999-01-01", "2026-05-01"

LABELS = {
    "fr": dict(
        title="L'or a monté dans les huit devises, sans exception",
        sub="Prix de l'once dans chaque devise, base 100 en janvier 1999 — échelle logarithmique.",
        eff="Indice or effectif", high="JPY — le plus haut", low="CHF — le plus bas",
        others="Les six autres devises du panier",
        note="Le faisceau reste serré : l'écart entre la devise la plus faible et la plus forte est petit devant\\n"
             "la hausse commune. Sources : Banque mondiale (or, fixing de Londres) ; Réserve fédérale, H.10 (change)."),
    "en": dict(
        title="Gold rose in all eight currencies, without exception",
        sub="Price of an ounce in each currency, January 1999 = 100 — logarithmic scale.",
        eff="Effective gold index", high="JPY — highest", low="CHF — lowest",
        others="The six other basket currencies",
        note="The bundle stays tight: the gap between the weakest and the strongest currency is small next to the\\n"
             "common rise. Sources: World Bank (gold, London fixing); Federal Reserve, H.10 (exchange rates)."),
}


def build_figure(prices: DataFrame, lang: str) -> Figure:
    """Huit courbes en base 100, les deux extrêmes mises en avant, indice effectif en blanc."""
    text = LABELS[lang]
    base = 100 * prices / prices.iloc[0]
    index = effective_index(prices)
    final = base.iloc[-1].sort_values(ascending=False)
    high, low = final.index[0], final.index[-1]

    fig = nm.figure(height_px=1120)
    ax = nm.axes(fig, left=0.062, right=0.982)
    for rank, code in enumerate(c for c in base.columns if c not in (high, low)):
        ax.plot(base.index, base[code], color=nm.COLORS["blue"], lw=2.0, alpha=0.5, zorder=2,
                label=text["others"] if rank == 0 else None)
    ax.plot(base.index, base[high], color=nm.COLORS["rose"], lw=3.0, zorder=4, label=text["high"])
    ax.plot(base.index, base[low], color=nm.COLORS["teal"], lw=3.0, zorder=4, label=text["low"])
    ax.plot(index.index, index, color=nm.COLORS["text"], lw=3.6, zorder=5, label=text["eff"])

    ax.set_yscale("log")
    ax.yaxis.set_major_locator(FixedLocator([100, 200, 500, 1000, 2000]))
    ax.yaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"{v:,.0f}".replace(",", " " if lang == "fr" else ",")))
    ax.yaxis.set_minor_locator(FixedLocator([]))
    ax.set_ylim(72, 3050)

    # Le faisceau reste anonyme — c'est le propos : les six autres courbes sont
    # indiscernables. Seuls les deux extrêmes et l'indice sont nommés.
    handles = dict(zip(*ax.get_legend_handles_labels()[::-1]))      # libellé → tracé
    order = [text["eff"], text["high"], text["others"], text["low"]]
    legend = ax.legend([handles[label] for label in order], order, loc="upper left",
                       frameon=False, fontsize=20.5, labelcolor="linecolor",
                       handlelength=1.6, borderaxespad=1.2)
    for handle in legend.get_lines():
        handle.set_linewidth(3.4)
        handle.set_alpha(1)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig


build_figure(load_gold_in_currencies(START, END), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 2 — la part du dollar dans la hausse
# ═════════════════════════════════════════════════════════════════════════════

DATA_2 = LOADERS

FIG_2 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

START, END = "1999-01-01", "2026-05-01"

LABELS = {
    "fr": dict(
        title="Presque rien de la hausse ne vient du dollar",
        sub="Croissance cumulée en logarithmes, exprimée en pourcentage — décomposition exacte, pas une estimation.",
        usd="Prix de l'or en dollars", eff="Indice or effectif (les huit devises)",
        fx="Composante dollar contre le panier", share="{:.0f} % de la hausse",
        note="Identité comptable : prix en dollars = indice or effectif + composante dollar. Aucune approximation,\\n"
             "aucune cause démontrée. Sources : Banque mondiale (or) ; Réserve fédérale, H.10 (change)."),
    "en": dict(
        title="Almost none of the rise comes from the dollar",
        sub="Cumulative log growth, shown in percent — an exact decomposition, not an estimate.",
        usd="Gold price in dollars", eff="Effective gold index (the eight currencies)",
        fx="Dollar component against the basket", share="{:.0f}% of the rise",
        note="Accounting identity: dollar price = effective gold index + dollar component. No approximation, and no\\n"
             "cause established. Sources: World Bank (gold); Federal Reserve, H.10 (exchange rates)."),
}


def build_figure(prices: DataFrame, lang: str) -> Figure:
    """Le prix en dollars et ses deux composantes comptables, en croissance logarithmique."""
    text = LABELS[lang]
    usd = 100 * np.log(prices["USD"] / prices["USD"].iloc[0])
    eff = 100 * np.log(effective_index(prices) / 100)
    fx = usd - eff                     # ce que le dollar apporte face au panier

    fig = nm.figure(height_px=1120)
    ax = nm.axes(fig, left=0.075, right=0.982)
    ax.axhline(0, color=nm.COLORS["edge"], lw=2, zorder=1)
    ax.plot(usd.index, usd, color=nm.COLORS["text"], lw=3.4, zorder=5, label=text["usd"])
    ax.plot(eff.index, eff, color=nm.COLORS["amber"], lw=3.0, zorder=4, label=text["eff"])
    ax.plot(fx.index, fx, color=nm.COLORS["blue"], lw=3.0, zorder=4, label=text["fx"])
    ax.fill_between(fx.index, 0, fx, color=nm.COLORS["blue"], alpha=0.16, zorder=2)

    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f} %".replace(",", " ")
                                               if lang == "fr" else f"{v:,.0f}%"))
    ax.set_ylim(-40, 330)
    legend = ax.legend(loc="upper left", frameon=False, fontsize=20.5, labelcolor="linecolor",
                       handlelength=1.6, borderaxespad=1.2)
    for handle in legend.get_lines():
        handle.set_linewidth(3.4)

    share = 100 * float(fx.iloc[-1] / usd.iloc[-1])
    ax.annotate(text["share"].format(share),
                xy=(fx.index[-1], float(fx.iloc[-1])),
                xytext=(fx.index[int(len(fx) * 0.72)], 78),
                color=nm.COLORS["blue"], fontsize=21, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="-", color=nm.COLORS["blue"], lw=2, alpha=0.7))

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig


build_figure(load_gold_in_currencies(START, END), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Chargeurs locaux — huit IPC et huit agrégats de monnaie large
# ═════════════════════════════════════════════════════════════════════════════

LOCALS = '''import json

ZONES = ["US", "EA", "JP", "UK", "CH", "CA", "AU", "CN"]
Q0, QT = "1999Q1", "2026Q1"                # fenêtre commune imposée par l'IPC australien

OECD = ("https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,{dsd}@{flow},1.0/"
        "{key}?startPeriod=1998-12&format=csvfile")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}


def _fetch_h(url: str, headers: dict | None = None, data: str | None = None) -> bytes:
    """Téléchargement avec en-têtes et corps POST — certains diffuseurs les exigent.

    ⚠️ L'en-tête se choisit par diffuseur : l'OCDE, la Banque d'Angleterre et MOFCOM
    exigent un en-tête de navigateur, alors que FRED et la RBA le refusent.
    The header must be chosen per publisher: the OECD, the BoE and MOFCOM require a
    browser header, while FRED and the RBA reject it.
    """
    return _fetch(url, headers=headers, data=data)


def _monthly(index, values) -> Series:
    return Series(np.asarray(values, dtype=float), index=pd.PeriodIndex(index, freq="M")).sort_index()


def _fred_periods(series_id: str) -> Series:
    series = load_fred(series_id)
    return _monthly(series.index.to_period("M"), series.values)


def _oecd(key: str, coicop2018: bool = False) -> Series:
    """Indice de prix à la consommation diffusé par l'OCDE (SDMX public, format CSV).
    Consumer price index from the OECD SDMX public endpoint."""
    dsd, flow = (("DSD_PRICES_COICOP2018", "DF_PRICES_C2018_ALL") if coicop2018
                 else ("DSD_PRICES", "DF_PRICES_ALL"))
    # L'OCDE refuse les clients sans en-tête de navigateur (403) ; FRED et la RBA
    # refusent l'inverse. D'où deux fonctions de téléchargement distinctes.
    # The OECD rejects clients without a browser header (403); FRED and the RBA reject
    # the opposite. Hence the two separate download helpers.
    table = pd.read_csv(io.StringIO(_fetch_h(OECD.format(dsd=dsd, flow=flow, key=key), UA).decode()))
    time_col = [c for c in table.columns if "TIME" in c][0]
    value_col = [c for c in table.columns if c.startswith("OBS_VALUE")][0]
    table = table[[time_col, value_col]].dropna().sort_values(time_col)
    freq = "Q" if "Q" in str(table[time_col].iloc[0]) else "M"
    return Series(table[value_col].values.astype(float),
                  index=pd.PeriodIndex(table[time_col], freq=freq)).sort_index()


def load_cpi() -> dict[str, Series]:
    """Les huit indices de prix, chacun à sa source nationale ou à l'OCDE.
    The eight consumer price indices, each from its national source or the OECD."""
    return {
        "US": _fred_periods("CPIAUCNS"),                        # BLS, non désaisonnalisé
        "EA": _fred_periods("CP0000EZ19M086NEST"),              # IPCH, Eurostat
        "JP": _oecd("JPN.M.N.CPI.IX._T.N._Z", True),
        "UK": _oecd("GBR.M.N.CPI.IX._T.N._Z"),
        "CH": _oecd("CHE.M.N.CPI.IX._T.N._Z", True),
        "CA": _oecd("CAN.M.N.CPI.IX._T.N._Z", True),
        "AU": _oecd("AUS.Q.N.CPI.IX._T.N._Z"),                  # trimestriel à la source
        "CN": _oecd("CHN.M.N.CPI.IX._T.N._Z"),
    }


def _ecb_m3() -> Series:
    """M3 de la zone euro (BCE, base de données des statistiques monétaires BSI)."""
    url = ("https://data-api.ecb.europa.eu/service/data/BSI/"
           "M.U2.Y.V.M30.X.I.U2.2300.Z01.E?format=csvdata")
    table = pd.read_csv(io.StringIO(_fetch(url).decode()))
    return _monthly(pd.PeriodIndex(table["TIME_PERIOD"], freq="M"), table["OBS_VALUE"])


def _boe_m4() -> Series:
    """M4 du Royaume-Uni (Banque d'Angleterre, série LPMAUYN)."""
    url = ("https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes"
           "&Datefrom=01/Jan/1998&Dateto=01/Dec/2026&SeriesCodes=LPMAUYN&CSVF=TN"
           "&UsingCodes=Y&VPD=Y&VFD=N")
    table = pd.read_csv(io.StringIO(_fetch_h(url, UA).decode()))
    return _monthly(pd.to_datetime(table["DATE"], format="%d %b %Y").dt.to_period("M"),
                    table["LPMAUYN"])


def _snb_m3() -> Series:
    """M3 suisse (BNS, cube snbmonagg : dimension B = niveau, GM3 = agrégat M3)."""
    raw = _fetch("https://data.snb.ch/api/cube/snbmonagg/data/csv/en").decode("utf-8-sig")
    rows = [line.split(";") for line in raw.splitlines() if line.count(";") == 3]
    table = pd.DataFrame(rows[1:], columns=[c.strip('"') for c in rows[0]]).map(lambda x: x.strip('"'))
    table = table[(table["D0"] == "B") & (table["D1"] == "GM3")]
    return _monthly(pd.PeriodIndex(table["Date"], freq="M"),
                    pd.to_numeric(table["Value"], errors="coerce"))


def _boc_m2pp() -> Series:
    """M2++ canadien (Banque du Canada, série V41552801 via l'API Valet)."""
    raw = _fetch("https://www.bankofcanada.ca/valet/observations/V41552801/csv"
                 "?start_date=1998-01-01").decode()
    body = raw.split('"OBSERVATIONS"')[1].strip().splitlines()
    table = pd.DataFrame([r.replace('"', "").split(",") for r in body[1:]], columns=["date", "value"])
    return _monthly(pd.PeriodIndex(table["date"], freq="M"),
                    pd.to_numeric(table["value"], errors="coerce"))


def _rba_broad() -> Series:
    """Monnaie large australienne (RBA, tableau D3 des agrégats monétaires)."""
    raw = _fetch("https://www.rba.gov.au/statistics/tables/csv/d3-data.csv").decode("utf-8-sig")
    lines = raw.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Series ID"))
    header = [c.strip('"') for c in lines[head].split(",")]
    column = next(i for i, code in enumerate(header) if code.startswith("DMABM"))
    rows = [line.split(",") for line in lines[head + 1:] if line and line[0].isdigit()]
    table = pd.DataFrame(rows)
    return _monthly(pd.PeriodIndex(pd.to_datetime(table[0], dayfirst=True), freq="M"),
                    pd.to_numeric(table[column], errors="coerce")).dropna()


def _china_m2() -> Series:
    """M2 chinoise de fin de mois : diffusion MOFCOM (module 047), complétée par le
    pont FMI/FRED pour 1999 et par le Bureau national des statistiques pour 2026.
    Chinese end-of-month M2: MOFCOM module 047, bridged with IMF/FRED and NBS."""
    raw = _fetch_h("https://data.mofcom.gov.cn/datamofcom/front/zhtj/dateQuery",
                   {**UA, "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "https://data.mofcom.gov.cn/zhtj/coin.shtml"},
                   "start_date=1999-01&end_date=2026-12&type=7&module_no=047")
    rows = json.loads(raw.decode())[0]
    money = _monthly([f"{r['time_view'][:4]}-{r['time_view'][4:]}" for r in rows],
                     [r["value"] for r in rows])                      # en 亿元 (10⁸ yuans)
    bridge = _fred_periods("MYAGM2CNM189N") / 1e8                     # yuans → 亿元
    latest = json.loads(_fetch("https://api.db.nomics.world/v22/series/NBS/M_A0D01/A0D0101"
                               "?observations=1").decode())["series"]["docs"][0]
    for extra in (bridge, _monthly(latest["period"], latest["value"])):
        money = money.combine_first(extra)
    return money.sort_index()


def _japan_m3() -> Series:
    """M3 japonaise : niveaux OCDE/FRED, prolongés par les variations annuelles de la BOJ.

    La Banque du Japon ne publie plus les niveaux dans un format lisible sans clé ; ses
    variations sur douze mois (tableau MD02) permettent de prolonger la série de niveaux.
    Japanese M3: OECD/FRED levels extended with the BOJ's year-on-year changes.
    """
    levels = _fred_periods("MABMM301JPM189S")
    try:
        page = _fetch("https://www.stat-search.boj.or.jp/ssi/mtshtml/md02_m_1.html")
        table = pd.read_html(io.StringIO(page.decode("shift_jis", "ignore")))[0]
        rows = table.iloc[5:, [0, 2]].dropna()                        # date, M3 en % sur un an
        rows = rows[rows[0].astype(str).str.match(r"\\d{4}/\\d{2}")]
        growth = _monthly(pd.PeriodIndex(rows[0].astype(str).str.replace("/", "-"), freq="M"),
                          pd.to_numeric(rows[2], errors="coerce"))
        for period in growth.index:
            if period in levels.index or period - 12 not in levels.index or pd.isna(growth[period]):
                continue
            levels.loc[period] = levels.loc[period - 12] * (1 + growth[period] / 100)
    except Exception as error:                                        # la série reste utilisable
        print(f"[or] prolongation BOJ indisponible ({error})")
    return levels.sort_index()


def load_money() -> dict[str, Series]:
    """Les huit agrégats de monnaie large, chacun à sa banque centrale.
    The eight broad money aggregates, each from its own central bank."""
    return {"US": _fred_periods("M2SL"), "EA": _ecb_m3(), "JP": _japan_m3(), "UK": _boe_m4(),
            "CH": _snb_m3(), "CA": _boc_m2pp(), "AU": _rba_broad(), "CN": _china_m2()}


def to_quarterly(series: Series) -> Series:
    """Moyenne des trois mois du trimestre ; les séries déjà trimestrielles sont gardées telles quelles.
    Quarterly average; natively quarterly series are kept as published."""
    if series.index.freqstr.startswith("Q"):
        return series
    return series.groupby(series.index.asfreq("Q")).mean()


def basket(series_by_zone: dict[str, Series]) -> Series:
    """Indice composite : moyenne géométrique équipondérée des huit séries, base 100 en 1999 T1.
    Equal-weighted geometric mean of the eight series, 1999 Q1 = 100."""
    frame = pd.DataFrame({zone: to_quarterly(series) for zone, series in series_by_zone.items()})
    frame = frame.loc[Q0:QT]
    return 100 * np.exp(np.log(frame / frame.loc[Q0]).mean(axis=1))


def gold_basket() -> Series:
    """Indice or effectif en trimestriel, construit mois par mois puis moyenné.
    Effective gold index, built monthly then averaged to quarters."""
    prices = load_gold_in_currencies("1999-01-01", "2026-03-01")
    prices.index = prices.index.to_period("M")
    return basket({zone: prices[zone] for zone in prices.columns})'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 3 — trois lectures du même panier
# ═════════════════════════════════════════════════════════════════════════════

DATA_3 = LOADERS + "\n\n\n" + LOCALS

FIG_3 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FixedLocator, FuncFormatter

LABELS = {
    "fr": dict(
        title="Ce qui reste de la hausse, dénominateur après dénominateur",
        sub="Indice or effectif du panier de huit zones, base 100 au premier trimestre 1999 — échelle logarithmique.",
        raw="Indice or effectif", cpi="Après les huit IPC locaux",
        money="Après les huit agrégats de monnaie large",
        note="Diviser n'est pas expliquer : le rapport dit ce qui subsiste relativement à chaque dénominateur,\\n"
             "pas ce qui a causé la hausse. Sources : Banque mondiale, Réserve fédérale, OCDE, BCE, BoE, BNS, BoC, RBA, MOFCOM."),
    "en": dict(
        title="What is left of the rise, denominator after denominator",
        sub="Effective gold index for the eight-zone basket, 1999 Q1 = 100 — logarithmic scale.",
        raw="Effective gold index", cpi="After the eight local CPIs",
        money="After the eight broad money aggregates",
        note="Dividing is not explaining: the ratio says what survives relative to each denominator, not what caused\\n"
             "the rise. Sources: World Bank, Federal Reserve, OECD, ECB, BoE, SNB, BoC, RBA, MOFCOM."),
}


def build_figure(gold: Series, cpi: Series, money: Series, lang: str) -> Figure:
    """Les trois courbes du panier : brut, déflaté par les prix, rapporté à la monnaie large."""
    text = LABELS[lang]
    curves = ((gold, "raw", nm.COLORS["text"], 3.6),
              (100 * gold / cpi, "cpi", nm.COLORS["teal"], 3.0),
              (100 * gold / money, "money", nm.COLORS["amber"], 3.0))

    fig = nm.figure(height_px=1120)
    ax = nm.axes(fig, left=0.075, right=0.982)
    for series, key, color, width in curves:
        # Le facteur final va dans la légende : en fin de période les trois courbes se
        # rapprochent, et des étiquettes posées sur les points se chevaucheraient.
        factor = f"×{series.iloc[-1] / 100:.2f}".replace(".", "," if lang == "fr" else ".")
        ax.plot(series.index.to_timestamp(how="end"), series.values, color=color, lw=width,
                label=f"{text[key]}  ·  {factor}", zorder=4)

    ax.set_yscale("log")
    ax.yaxis.set_major_locator(FixedLocator([50, 100, 200, 500, 1000, 2000]))
    ax.yaxis.set_minor_locator(FixedLocator([]))
    ax.yaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"{v:,.0f}".replace(",", " " if lang == "fr" else ",")))
    legend = ax.legend(loc="upper left", frameon=False, fontsize=20.5, labelcolor="linecolor",
                       handlelength=1.6, borderaxespad=1.2)
    for handle in legend.get_lines():
        handle.set_linewidth(3.4)

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig


build_figure(gold_basket(), basket(load_cpi()), basket(load_money()), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 4 — la forme du mouvement, trimestre par trimestre
# ═════════════════════════════════════════════════════════════════════════════

DATA_4 = LOADERS + "\n\n\n" + LOCALS

FIG_4 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

LABELS = {
    "fr": dict(
        title="L'or recule un trimestre sur trois ; la monnaie, presque jamais",
        sub="Variations d'un trimestre sur l'autre, 1999 T1 – 2026 T1 — deux distributions, une même fenêtre.",
        gold="Indice or effectif", money="Panier de monnaie large",
        summary="{down} trimestre{s} en baisse sur {total} · le plus faible {worst}",
        count="trimestres",
        note="Deux séries peuvent suivre une tendance proche sans se déplacer ensemble : c'est ce contraste qui\\n"
             "réfute l'idée d'un miroir mécanique entre l'or et la quantité de monnaie."),
    "en": dict(
        title="Gold falls one quarter in three; money almost never",
        sub="Quarter-on-quarter changes, 1999 Q1 to 2026 Q1 — two distributions, one window.",
        gold="Effective gold index", money="Broad money basket",
        summary="{down} quarter{s} down out of {total} · lowest {worst}",
        count="quarters",
        note="Two series can share a trend without moving together: this contrast is what refutes the idea of a\\n"
             "mechanical mirror between gold and the quantity of money."),
}


def build_figure(gold: Series, money: Series, lang: str) -> Figure:
    """Deux histogrammes superposés des variations trimestrielles, annotés de leurs extrêmes."""
    text = LABELS[lang]
    changes = {"gold": 100 * gold.pct_change().dropna(), "money": 100 * money.pct_change().dropna()}
    colors = {"gold": nm.COLORS["rose"], "money": nm.COLORS["amber"]}
    bins = np.arange(-13, 15.5, 1.5)

    fig = nm.figure(height_px=1160)
    axes = [fig.add_axes([0.075, 0.545, 0.907, 0.215]), fig.add_axes([0.075, 0.175, 0.907, 0.215])]
    for ax, key in zip(axes, ("gold", "money")):
        values = changes[key]
        ax.hist(values, bins=bins, color=colors[key], alpha=0.88, zorder=3)
        ax.axvline(0, color=nm.COLORS["text"], lw=2, zorder=4)
        ax.set_xlim(bins[0], bins[-1])
        ax.xaxis.set_major_formatter(FuncFormatter(
            lambda v, _: f"{v:+.0f} %".replace(".", ",") if lang == "fr" else f"{v:+.0f}%"))
        ax.set_ylabel(text["count"], fontsize=18)
        ax.text(0.002, 1.10, text[key], transform=ax.transAxes, fontsize=23, fontweight="bold",
                color=colors[key], va="bottom")
        down, total, worst = int((values < 0).sum()), len(values), float(values.min())
        digits = 2 if abs(worst) < 1 else 1
        printed = f"{worst:+.{digits}f} %".replace(".", ",") if lang == "fr" else f"{worst:+.{digits}f}%"
        ax.text(0.998, 1.10, text["summary"].format(down=down, total=total, worst=printed,
                                                    s="" if down < 2 else "s"),
                transform=ax.transAxes, fontsize=19.5, color=nm.COLORS["muted"],
                va="bottom", ha="right")

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig


build_figure(gold_basket(), basket(load_money()), LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 5 — la décomposition comptable en quatre blocs
# ═════════════════════════════════════════════════════════════════════════════

DATA_5 = '''from matplotlib.figure import Figure

# Parts publiées dans l'article, calculées de 1999 T1 à 2026 T1 sur le prix en
# dollars (×17,00). Elles somment à 100 % par construction logarithmique.
# Shares published in the article, 1999 Q1 to 2026 Q1, on the dollar price.
BLOCKS = [("fx", 2.0), ("cpi", 18.0), ("money", 40.0), ("residual", 40.0)]'''

FIG_5 = '''from matplotlib.patches import Rectangle

LABELS = {
    "fr": dict(
        title="Quatre blocs qui somment exactement à 100 %",
        sub="Décomposition comptable de la hausse du prix de l'or en dollars, 1999 T1 – 2026 T1 (×17,00).",
        fx="Dollar\\nrelatif", cpi="Prix locaux", money="Monnaie large\\nau-delà des prix",
        residual="Résidu",
        legend=["Change du dollar contre les sept autres devises",
                "Hausse des huit indices de prix à la consommation",
                "Croissance des huit agrégats de monnaie large, au-delà des prix",
                "Ce que les trois dénominateurs ne retirent pas"],
        note="Le mot important est « comptable » : les logarithmes partagent la hausse sans en désigner la cause.\\n"
             "Le résidu peut refléter la demande d'or, les taux réels, la confiance ou les erreurs de mesure."),
    "en": dict(
        title="Four blocks that add up to exactly 100%",
        sub="Accounting decomposition of the dollar gold price, 1999 Q1 to 2026 Q1 (×17.00).",
        fx="Relative\\ndollar", cpi="Local prices", money="Broad money\\nbeyond prices",
        residual="Residual",
        legend=["Dollar against the seven other currencies",
                "Rise in the eight consumer price indices",
                "Growth of the eight broad money aggregates, beyond prices",
                "What the three denominators do not remove"],
        note="The operative word is \\"accounting\\": logs split the rise without naming its cause. The residual may\\n"
             "reflect gold demand, real rates, confidence — or measurement error."),
}


def build_figure(blocks: list[tuple[str, float]], lang: str) -> Figure:
    """Barre empilée unique : quatre parts logarithmiques, une couleur par bloc."""
    text = LABELS[lang]
    colors = {"fx": nm.COLORS["blue"], "cpi": nm.COLORS["teal"],
              "money": nm.COLORS["amber"], "residual": nm.COLORS["rose"]}

    fig = nm.figure(height_px=940)
    ax = nm.blank_axes(fig)
    x0, width, y0, height = 82, 1583, 496, 168

    start = 0.0
    for key, share in blocks:
        left = x0 + width * start / 100
        span = width * share / 100
        ax.add_patch(Rectangle((left, y0), span, height, facecolor=colors[key],
                               edgecolor=nm.COLORS["bg"], linewidth=3, zorder=3))
        ax.text(left + span / 2, y0 + height + 30, f"{share:.0f} %" if lang == "fr" else f"{share:.0f}%",
                ha="center", va="bottom", fontsize=30, fontweight="bold", color=colors[key])
        narrow = span < 150                     # bloc trop étroit pour un libellé centré
        ax.text(left if narrow else left + span / 2, y0 - 28, text[key],
                ha="left" if narrow else "center", va="top",
                fontsize=19 if narrow else 20.5, color=nm.COLORS["muted"], linespacing=1.35)
        start += share

    for rank, (key, _) in enumerate(blocks):
        y = 340 - rank * 48
        ax.add_patch(Rectangle((x0, y), 26, 26, facecolor=colors[key], zorder=3))
        ax.text(x0 + 44, y + 13, text["legend"][rank], ha="left", va="center",
                fontsize=19.5, color=nm.COLORS["muted"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig


build_figure(BLOCKS, LANG)'''


# ═════════════════════════════════════════════════════════════════════════════
# Figure 6 — contrôle américain : or rapporté à M2
# ═════════════════════════════════════════════════════════════════════════════

DATA_6 = LOADERS + '''


PARITY, PARITY_END = 35.0, "1968-03-01"   # parité officielle jusqu'au London Gold Pool
END = "2026-02-01"                        # borne de l'article ; None = jusqu'à aujourd'hui


def load_gold_over_m2(end: str | None = END) -> Series:
    """Rapport « or ÷ M2 » aux États-Unis, mensuel depuis 1959.

    Avant avril 1968, l'or est porté à sa parité officielle de 35 dollars l'once ;
    ensuite vient le marché londonien. Le raccord est volontairement visible : la
    partie ancienne est un contrôle historique, pas un prix de marché moderne.
    US gold-to-M2 ratio: official 35-dollar parity until March 1968, London market after.
    """
    market = load_gold_usd()
    official = Series(PARITY, index=pd.date_range("1959-01-01", PARITY_END, freq="MS"))
    gold = pd.concat([official, market.loc["1968-04-01":]])
    ratio = (gold / load_fred("M2SL")).dropna()
    return ratio.loc[:end] if end else ratio'''

FIG_6 = '''from matplotlib.figure import Figure
from matplotlib.ticker import FixedLocator, FuncFormatter

LABELS = {
    "fr": dict(
        title="Un ancrage très lâche : le rapport de l'or à la monnaie",
        sub="Prix de l'once divisé par M2, États-Unis, échelle logarithmique — contrôle séparé du panier.",
        peak="Sommet de janvier 1980", trough="Creux d'avril 2001", div="divisé par {:.0f}",
        parity="parité officielle\\n(35 dollars l'once)",
        note="Le niveau du rapport dépend des unités retenues (dollars par once, milliards de dollars) : seules ses\\n"
             "variations s'interprètent. Sources : Banque mondiale (or) ; Réserve fédérale, M2SL."),
    "en": dict(
        title="A very loose anchor: gold relative to money",
        sub="Ounce price divided by M2, United States, logarithmic scale — a control separate from the basket.",
        peak="January 1980 peak", trough="April 2001 trough", div="divided by {:.0f}",
        parity="official parity\\n(35 dollars an ounce)",
        note="The level of the ratio depends on the units used (dollars per ounce, billions of dollars): only its\\n"
             "variations can be read. Sources: World Bank (gold); Federal Reserve, M2SL."),
}


def build_figure(ratio: Series, lang: str) -> Figure:
    """Courbe logarithmique du rapport, sommet et creux annotés, période de parité grisée."""
    text = LABELS[lang]
    peak, trough = pd.Timestamp("1980-01-01"), pd.Timestamp("2001-04-01")

    fig = nm.figure(height_px=1080)
    ax = nm.axes(fig, left=0.075, right=0.982)
    ax.axvspan(ratio.index[0], pd.Timestamp(PARITY_END), color=nm.COLORS["card"], zorder=1)
    ax.plot(ratio.index, ratio, color=nm.COLORS["amber"], lw=3.0, zorder=4)
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(FixedLocator([0.05, 0.1, 0.2, 0.3, 0.4]))
    ax.yaxis.set_minor_locator(FixedLocator([]))
    ax.yaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"{v:.2f}".replace(".", "," if lang == "fr" else ".")))

    ax.text(pd.Timestamp("1959-06-01"), ratio.max() * 0.92, text["parity"], ha="left", va="top",
            fontsize=18.5, color=nm.COLORS["muted"], linespacing=1.4, zorder=5)
    ax.set_ylim(ratio.min() * 0.74, ratio.max() * 1.16)     # place pour les annotations
    for date, key, days, offset, align in ((peak, "peak", 760, 1.42, "left"),
                                           (trough, "trough", 420, 0.80, "left")):
        ax.plot([date], [ratio[date]], "o", ms=13, color=nm.COLORS["rose"], zorder=6)
        ax.annotate(text[key], xy=(date, ratio[date]),
                    xytext=(date + pd.Timedelta(days=days), ratio[date] * offset),
                    fontsize=20.5, color=nm.COLORS["rose"], fontweight="bold", va="center",
                    ha=align,
                    arrowprops=dict(arrowstyle="-", color=nm.COLORS["rose"], lw=1.8, alpha=0.75))
    mid = peak + (trough - peak) / 2
    ax.annotate("", xy=(mid, ratio[peak]), xytext=(mid, ratio[trough]),
                arrowprops=dict(arrowstyle="<->", color=nm.COLORS["muted"], lw=2))
    ax.text(mid + pd.Timedelta(days=260), (ratio[peak] * ratio[trough]) ** 0.5,
            text["div"].format(ratio[peak] / ratio[trough]), ha="left", va="center",
            fontsize=21, fontweight="bold", color=nm.COLORS["text"])

    nm.header(fig, text["title"], text["sub"])
    nm.footer(fig, text["note"])
    return fig


build_figure(load_gold_over_m2(), LANG)'''


FIGURES = [
    dict(name="fig01-or-huit-devises", data=DATA_1, fig=FIG_1, live=True,
         fig_fr="L'or dans huit devises", fig_en="Gold in eight currencies"),
    dict(name="fig02-composante-dollar", data=DATA_2, fig=FIG_2, live=True,
         fig_fr="La part du dollar dans la hausse", fig_en="The dollar's share of the rise"),
    dict(name="fig03-trois-lectures", data=DATA_3, fig=FIG_3, live=True,
         fig_fr="Trois lectures du même panier", fig_en="Three readings of the same basket"),
    dict(name="fig04-variations-trimestrielles", data=DATA_4, fig=FIG_4, live=True,
         fig_fr="La forme du mouvement, trimestre par trimestre",
         fig_en="The shape of the move, quarter by quarter"),
    dict(name="fig05-decomposition-comptable", data=DATA_5, fig=FIG_5, live=False,
         fig_fr="La décomposition comptable en quatre blocs",
         fig_en="The four-block accounting decomposition"),
    dict(name="fig06-or-sur-m2", data=DATA_6, fig=FIG_6, live=True,
         fig_fr="Le rapport de l'or à la monnaie aux États-Unis",
         fig_en="US gold relative to money"),
]

if __name__ == "__main__":
    if "--build" in sys.argv:
        nb_kit.build_all(META, DIR, FIGURES)
    else:
        only = [f for f in FIGURES if not sys.argv[1:] or f["name"][:5] in sys.argv[1:]]
        nb_kit.test_all(only, "outor")
