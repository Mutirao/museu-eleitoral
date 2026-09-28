"""Junta dataset.json + classificacao.json + candidatos.json em real.json (dados do protótipo)."""
from pathlib import Path
DADOS = Path(__file__).resolve().parent / "dados"
BRUTOS, GERADOS = DADOS / "brutos", DADOS / "gerados"
GERADOS.mkdir(exist_ok=True)
import json
from datetime import datetime

ds = json.load(open(GERADOS / "dataset.json"))
cls = json.load(open(DADOS / "classificacao.json"))
meta = json.load(open(DADOS / "candidatos.json"))
NETLABEL = {"instagram": "Instagram", "x": "X", "youtube": "YouTube"}


def num(v):
    if v in (None, "", 0, "0"):
        return None
    if isinstance(v, str):
        return v
    s = f"{v:,}".replace(",", ".")
    if v >= 1_000_000:
        s = f"{v/1_000_000:.1f} mi".replace(".", ",")
    elif v >= 10_000:
        s = f"{v/1000:.1f} mil".replace(".", ",")
    return s


out = {"collectedAt": meta["collectedAt"], "tool": meta["tool"], "cands": {}}
for c, items in ds.items():
    m = meta["cands"][c]
    its = []
    for x in items:
        dt = datetime.fromisoformat(x["dt"])
        metrics = [(k, num(x.get(k2))) for k, k2 in (("views", "views"), ("likes", "likes"), ("comments", "comments"), ("reposts", "retweets"))]
        badges = []
        if x.get("is_retweet"):
            badges.append("Repostagem")
        if x["ad"]:
            badges.append("Propaganda eleitoral identificada")
        ad_line = ""
        if x["ad"]:
            tail = x["text"][x["text"].upper().rfind("PROPAGANDA ELEITORAL") - 40:] if "PROPAGANDA ELEITORAL" in x["text"].upper() else ""
            ad_line = "Identificação exibida no post: " + (tail.split("\n")[-1].strip() or "propaganda eleitoral")
        its.append({
            "id": x["id"], "net": x["net"], "acct": x["acct"], "url": x["url"], "kind": x["kind"],
            "date": dt.strftime("%d/%m/%Y"), "time": dt.strftime("%H:%M") if x["time_known"] else "",
            "title": x.get("title") or "", "text": x["text"] or "", "thumb": x.get("thumb") or "",
            "embed": f"https://www.youtube-nocookie.com/embed/{x['vid']}" if x.get("vid") else "",
            "metrics": [[k, v] for k, v in metrics if v], "badges": badges, "ad": x["ad"], "adText": ad_line,
            "rt": bool(x.get("is_retweet")), "cid": x["cid"], "types": [],
            "transcript": x.get("transcript") or [],
        })
    contribs = []
    for k, (typ, quote) in enumerate(cls[c]):
        hits = [i for i in its if quote in i["text"] or quote in i["title"] or quote in " ".join(t for _, t in i["transcript"])]
        assert hits, f"trecho não encontrado em {c}: {quote[:60]!r}"
        prim = next((i for i in hits if i["net"] == "x"), hits[0])
        for i in hits:
            if typ not in i["types"]:
                i["types"].append(typ)
        contribs.append({"id": f"{c[0]}c{k+1:02d}", "item": prim["id"], "type": typ, "quote": quote})
    by_net = {n: sum(1 for i in its if i["net"] == n) for n in NETLABEL}
    note = "Coleta da última semana (18 a 25/09/2026): " + ", ".join(f"{v} de {NETLABEL[n]}" for n, v in by_net.items() if v) + f". {m['collectNote']}"
    out["cands"][c] = {**{k: v for k, v in m.items() if k != "collectNote"}, "collectNote": note, "items": its, "contribs": contribs}
    print(c, len(its), "itens,", len(contribs), "trechos")
json.dump(out, open(GERADOS / "real.json", "w"), ensure_ascii=False, indent=1)
