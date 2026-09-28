"""Normaliza a coleta (Instagram, X, YouTube RSS) em dataset.json, com CIDv1 de cada registro."""
from pathlib import Path
DADOS = Path(__file__).resolve().parent / "dados"
BRUTOS, GERADOS = DADOS / "brutos", DADOS / "gerados"
GERADOS.mkdir(exist_ok=True)
import os, json, re, hashlib, base64, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
BRT=timezone(timedelta(hours=-3)); START=datetime(2026,9,18,tzinfo=BRT)  # recorte da apresentação: última semana
MONTHS={m:i for i,m in enumerate("January February March April May June July August September October November December".split(),1)}
def cid(b):  # CIDv1, codec raw (0x55), sha2-256, base32
    raw=bytes([1,0x55,0x12,0x20])+hashlib.sha256(b).digest()
    return "b"+base64.b32encode(raw).decode().lower().rstrip("=")
out={"jones":[],"nikolas":[]}
owner={"jones.manoel":"jones","nikolasferreiradm":"nikolas","nikolasferreirabr":"nikolas","oquenikolasfez":"nikolas"}
for acct,items in json.load(open(BRUTOS/"ig-all.json")).items():
    for d in items:
        m=re.match(r'^.*? no Instagram(?:: "(.*)")?$', d.get("og") or "", re.S)
        desc=d.get("desc") or ""
        lk=re.match(r'([\d.,]+[KMk]?) likes?, ([\d.,]+[KMk]?) comments?', desc)
        if d.get("t"): dt=datetime.fromisoformat(d["t"].replace("Z","+00:00"))
        else:
            md=re.search(r' (?:on|no) (\w+) (\d+), (\d{4})', desc)
            dt=datetime(int(md[3]),MONTHS[md[1]],int(md[2]),12,tzinfo=BRT) if md else None
        out[owner[acct]].append(dict(net="instagram",acct="@"+acct,url=d["url"],kind="reel" if d["kind"]=="reel" else ("vídeo" if d.get("vid") else "imagem"),
            dt=dt,time_known=bool(d.get("t")),text=(m.group(1) if m and m.group(1) else "").strip(),likes=lk[1] if lk else None,comments=lk[2] if lk else None,raw=d))
for u,c in [("jonesmanoel_pe","jones"),("nikolas_dm","nikolas")]:
    tweets=json.load(open(BRUTOS/f"x-{u}.json"))
    priv=DADOS/"privado"/f"x-{u}-terceiros.json"  # repostagens e citações de terceiros, fora do git
    if priv.exists():
        p=json.load(open(priv))
        tweets=[{**t,"quoted_tweet":p["citados"].get(t["id"],t.get("quoted_tweet"))} for t in tweets]+p["reposts"]
    for t in tweets:
        q=t.get("quoted_tweet") or {}
        out[c].append(dict(net="x",acct="@"+t["author"],url=t["url"],kind="imagem" if t.get("has_media") else "texto",
            dt=datetime.strptime(t["created_at"],"%a %b %d %H:%M:%S %z %Y"),time_known=True,text=t["text"],
            likes=t.get("likes"),retweets=t.get("retweets"),replies=t.get("replies"),views=t.get("views"),is_retweet=t.get("is_retweet"),
            quoted=q.get("text"),quoted_author=q.get("author"),thumb=(t.get("media_posters") or [None])[0],raw=t))
ns={'a':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015','media':'http://search.yahoo.com/mrss/'}
for e in ET.parse(BRUTOS/"rss-UCxI9vN6UbxmBt8VIvUKtJaA.xml").getroot().findall('a:entry',ns):
    vid=e.find('yt:videoId',ns).text; g=e.find('media:group',ns)
    st=g.find('media:community/media:statistics',ns); rt=g.find('media:community/media:starRating',ns)
    out["nikolas"].append(dict(net="youtube",acct="@NikolasFerreiraO",url=f"https://www.youtube.com/watch?v={vid}",kind="vídeo",vid=vid,
        dt=datetime.fromisoformat(e.find('a:published',ns).text),time_known=True,title=e.find('a:title',ns).text,
        text=(e.find('a:title',ns).text+"\n\n"+(g.find('media:description',ns).text or "")).strip(),
        views=st.get('views') if st is not None else None,likes=rt.get('count') if rt is not None else None,
        thumb=f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",raw=ET.tostring(e,encoding='unicode'),
        transcript=json.load(open(GERADOS/"legendas"/f"{vid}.json")) if (GERADOS/"legendas"/f"{vid}.json").exists() else []))
for c in out:
    items=sorted([x for x in out[c] if x["dt"] and x["dt"]>=START],key=lambda x:x["dt"],reverse=True)
    for i,x in enumerate(items):
        x["id"]=f"{c[0]}{i+1:02d}"
        r=x.pop("raw"); x["cid"]=cid(r.encode() if isinstance(r,str) else json.dumps(r,ensure_ascii=False,sort_keys=True).encode())
        x["ad"]=bool(re.search(r"PROPAGANDA ELEITORAL|CNPJ\s*[\d./-]{14,}",x["text"] or "",re.I))
        x["dt"]=x["dt"].astimezone(BRT).isoformat()
    out[c]=items
json.dump(out,open(GERADOS/"dataset.json","w"),ensure_ascii=False,indent=1)
for c,items in out.items(): print(c,len(items),{n:sum(1 for x in items if x["net"]==n) for n in ("instagram","x","youtube")})
