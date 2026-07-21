# nmlab-figures

Notebooks [Google Colab](https://colab.research.google.com) compagnons des figures « data » des
articles [NMLab](https://nmlab.io) : chaque notebook reproduit une figure du site avec les
**données du jour** (FRED…) et le style NMLab (thème sombre, police Inter).

*Companion Colab notebooks for the data figures of [NMLab](https://nmlab.io) articles — each
notebook rebuilds a figure of the site with **today's data** and the NMLab visual style.*

## Ouvrir un notebook · Open a notebook

Cliquez le badge « Ouvrir dans Colab » sous une figure d'un article, ou ouvrez directement :
*Click the badge under a figure in an article, or open directly:*

```
https://colab.research.google.com/github/nmlab-finance/nmlab-figures/blob/main/<chemin>.ipynb
```

Dans Colab : **Exécution ▸ Tout exécuter** (*Runtime ▸ Run all*). Passez `LANG = "en"` dans la
première cellule pour les libellés anglais. *Set `LANG = "en"` in the first cell for English labels.*

## Structure

- `nmlab_style.py` — thème matplotlib NMLab (fond sombre, Inter, en-tête/pied de figure)
- `templates/template-figure.ipynb` — gabarit pour créer une nouvelle figure
- `macro/<chapitre>/figNN-<slug>.ipynb` — un notebook par figure, rangé par chapitre

⚠️ **Les chemins des notebooks publiés ne changent jamais** : les articles du site pointent dessus.
*Published notebook paths never change: the site's articles link to them.*

## Licence · License

Code sous licence [MIT](LICENSE) ; design des figures © NMLab ; les données restent la propriété
de leurs sources (Federal Reserve Bank of St. Louis / FRED, BLS, NBER…).
*Code is MIT-licensed; figure design © NMLab; the data belongs to its sources.*
