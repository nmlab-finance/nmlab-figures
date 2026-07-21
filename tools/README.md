# Outillage interne (maintenance des notebooks et des boutons)

Scripts utilisés par l'assistant CMS pour maintenir ce dépôt. **Le container de
travail n'est PAS persistant** : après un rebuild, restaurer l'outillage depuis
ce dossier (source de vérité).

## Contenu

- `build_notebooks.py` — source unique des cellules des notebooks ; `--test`
  exécute tout localement et rend des PNG dans `out/`, sans argument il écrit
  les `.ipynb` dans le miroir du dépôt.
- `push_to_github.py` — pousse le miroir local vers `nmlab-finance/nmlab-figures`
  via l'API Contents (création + mise à jour, sha géré). Lit le token dans
  `~/cms-workspace/.github-token`.
- `gen-inline.js` — génère les boutons « Générer/Modifier l'image dans Google
  Colab » (SVG inline pour le MDX, largeur auto-mesurée, gabarits
  `inline-button-{fr,en}.html` avec placeholder `COLAB_URL` + aperçus PNG).
- `colab-badge-official.svg` — badge Colab officiel, dont `gen-inline.js`
  extrait les chemins du logo.

## Amorçage après un rebuild du container

```bash
# 1. Récupérer l'outillage (pas de git nécessaire)
mkdir -p ~/cms-workspace/nmlab-figures-tools ~/cms-workspace/badge-maker
for f in build_notebooks.py push_to_github.py; do
  curl -sL "https://raw.githubusercontent.com/nmlab-finance/nmlab-figures/main/tools/$f" \
    -o ~/cms-workspace/nmlab-figures-tools/$f; done
for f in gen-inline.js colab-badge-official.svg; do
  curl -sL "https://raw.githubusercontent.com/nmlab-finance/nmlab-figures/main/tools/$f" \
    -o ~/cms-workspace/badge-maker/$f; done

# 2. Python (test des notebooks)
python3 -m venv ~/cms-workspace/.venv
~/cms-workspace/.venv/bin/pip install matplotlib pandas

# 3. Node (rendu des boutons)
cd ~/cms-workspace/badge-maker && npm init -y && npm i sharp @expo-google-fonts/inter
cat > fonts.conf <<'EOF'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>/home/claudeagent/cms-workspace/badge-maker/node_modules/@expo-google-fonts/inter</dir>
  <cachedir>/home/claudeagent/cms-workspace/badge-maker/.fccache</cachedir>
</fontconfig>
EOF

# 4. Token GitHub (SECRET — jamais dans le dépôt) : à redemander à Nicolas,
#    puis : printf '%s' '<token>' > ~/cms-workspace/.github-token && chmod 600 …
```

Le miroir du dépôt (`~/cms-workspace/nmlab-figures/`) se reconstruit avec
`build_notebooks.py` (notebooks) + les fichiers statiques de ce dépôt.
