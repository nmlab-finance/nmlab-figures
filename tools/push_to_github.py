#!/usr/bin/env python3
"""Pousse les fichiers du miroir local vers nmlab-finance/nmlab-figures (API Contents).

Usage : push_to_github.py [chemins relatifs…]   (défaut : tous les fichiers du miroir)
Crée le fichier s'il est absent, le met à jour sinon (sha récupéré au préalable).
"""

import base64
import json
import os
import sys
import urllib.error
import urllib.request

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.normpath(os.path.join(TOOLS, "..", "nmlab-figures"))
API = "https://api.github.com/repos/nmlab-finance/nmlab-figures/contents/"

with open(os.path.expanduser("~/cms-workspace/.github-token")) as f:
    TOKEN = f.read().strip()
HEADERS = {"Authorization": f"Bearer {TOKEN}",
           "Accept": "application/vnd.github+json",
           "X-GitHub-Api-Version": "2022-11-28"}


def call(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def push(rel):
    with open(os.path.join(REPO_DIR, rel), "rb") as f:
        content = base64.b64encode(f.read()).decode()
    status, existing = call("GET", API + rel + "?ref=main")
    payload = {"message": f"Ajout de {rel}" if status == 404 else f"Mise à jour de {rel}",
               "content": content, "branch": "main"}
    if status == 200:
        if existing.get("content", "").replace("\n", "") == content:
            print(f"  = {rel} (inchangé)")
            return
        payload["sha"] = existing["sha"]
    status, resp = call("PUT", API + rel, payload)
    if status in (200, 201):
        print(f"  ✓ {rel} → {resp['commit']['sha'][:9]}")
    else:
        print(f"  ✗ {rel} → HTTP {status}: {resp.get('message')}")
        sys.exit(1)


def default_files():
    for root, _, names in os.walk(REPO_DIR):
        for n in sorted(names):
            yield os.path.relpath(os.path.join(root, n), REPO_DIR)


if __name__ == "__main__":
    files = sys.argv[1:] or list(default_files())
    print(f"Envoi de {len(files)} fichier(s) vers nmlab-finance/nmlab-figures@main :")
    for rel in files:
        push(rel.replace(os.sep, "/"))
