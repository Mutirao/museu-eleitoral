"""Converte legendas automáticas (json3) em trechos de ~20s: legendas/<id>.json = [[seg_inicio, texto], ...]."""
from pathlib import Path
DADOS = Path(__file__).resolve().parent / "dados"
BRUTOS, GERADOS = DADOS / "brutos", DADOS / "gerados"
GERADOS.mkdir(exist_ok=True)
import json, glob, os, re
(GERADOS / "legendas").mkdir(exist_ok=True)
for f in glob.glob(str(BRUTOS / "legendas" / "*.pt-orig.json3")):
    vid = os.path.basename(f).split(".")[0]
    ev = json.load(open(f))["events"]
    words = []
    for e in ev:
        t = "".join(s.get("utf8", "") for s in e.get("segs", [])).replace("\n", " ")
        if t.strip():
            words.append((e["tStartMs"] / 1000, t))
    chunks, cur, start = [], "", None
    for t, w in words:
        if start is None:
            start = t
        cur += " " + w
        if t - start >= 20 and re.search(r"[\w\]]\s*$", cur):
            chunks.append([int(start), re.sub(r"\s+", " ", cur).strip()]); cur, start = "", None
    if cur.strip():
        chunks.append([int(start), re.sub(r"\s+", " ", cur).strip()])
    json.dump(chunks, open(GERADOS / "legendas" / f"{vid}.json", "w"), ensure_ascii=False, indent=0)
    print(vid, len(chunks), "trechos,", sum(len(c[1]) for c in chunks), "caracteres")
