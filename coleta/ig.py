"""Coleta posts de contas do Instagram via opencli browser (a API do adaptador dá HTTP 429)."""
from pathlib import Path
DADOS = Path(__file__).resolve().parent / "dados"
BRUTOS, GERADOS = DADOS / "brutos", DADOS / "gerados"
GERADOS.mkdir(exist_ok=True)
import subprocess, json, time, sys, re, os
def oc(*a):
    return subprocess.run(["opencli","browser","museu",*a],capture_output=True,text=True,timeout=120).stdout.strip()
def ev(js):
    out=oc("eval",js).splitlines(); return out[-1] if out else ""
LINKS="JSON.stringify([...new Set([...document.querySelectorAll('a[href*=\"/p/\"],a[href*=\"/reel/\"]')].map(a=>a.getAttribute('href')))])"
POST="JSON.stringify({t:document.querySelector('time[datetime]')?.getAttribute('datetime'),og:document.querySelector('meta[property=\"og:title\"]')?.content,desc:document.querySelector('meta[name=\"description\"]')?.content,vid:!!document.querySelector('video')})"
ARQ=BRUTOS/"ig-all.json"
res=json.load(open(ARQ)) if ARQ.exists() else {}
for arg in sys.argv[1:]:
    user,n=arg.split(":"); n=int(n)
    if res.get(user): print(user,"já coletado"); continue
    oc("open",f"https://www.instagram.com/{user}/"); time.sleep(7)
    links=json.loads(ev(LINKS) or "[]")[:n]; print(user,len(links),"links",flush=True)
    items=[]
    for l in links:
        url="https://www.instagram.com"+re.sub(r"^/[^/]+(?=/(p|reel)/)","",l)
        oc("open",url); time.sleep(6)
        try: d=json.loads(ev(POST))
        except Exception as e: print("  falhou",url,e); continue
        d["url"]=url; d["kind"]="reel" if "/reel/" in url else "post"; items.append(d)
        print("  ",d.get("t"),url,(d.get("og") or "")[:60].replace("\n"," "),flush=True); time.sleep(4)
    res[user]=items; json.dump(res,open(ARQ,"w"),ensure_ascii=False,indent=1)
