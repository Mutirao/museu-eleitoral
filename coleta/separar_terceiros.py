"""Tira conteúdo de terceiros da coleta do X antes de versionar.

Repostagens inteiras e tweets citados (quote tweets) vão para dados/privado/, fora do git.
Os posts dos próprios candidatos ficam em dados/brutos/. O norm.py junta as duas partes
quando a pasta privada existe, e os CIDs continuam os mesmos.
Rode depois de cada coleta do X.
"""
import json
from pathlib import Path
DADOS = Path(__file__).resolve().parent / "dados"
PRIV = DADOS / "privado"
PRIV.mkdir(exist_ok=True)
for u in ("jonesmanoel_pe", "nikolas_dm"):
    arq = DADOS / "brutos" / f"x-{u}.json"
    tweets = json.load(open(arq))
    proprios, reposts, citados = [], [], {}
    for t in tweets:
        if t.get("is_retweet"):
            reposts.append(t)
            continue
        if t.get("quoted_tweet"):
            citados[t["id"]] = t["quoted_tweet"]
            t = {**t, "quoted_tweet": None}
        proprios.append(t)
    json.dump(proprios, open(arq, "w"), ensure_ascii=False, indent=1)
    priv = PRIV / f"x-{u}-terceiros.json"
    antigo = json.load(open(priv)) if priv.exists() else {"reposts": [], "citados": {}}
    ids = {t["id"] for t in antigo["reposts"]}
    antigo["reposts"] += [t for t in reposts if t["id"] not in ids]
    antigo["citados"].update(citados)
    json.dump(antigo, open(priv, "w"), ensure_ascii=False, indent=1)
    print(u, len(proprios), "próprios ·", len(reposts), "repostagens e", len(citados), "citações → privado")
