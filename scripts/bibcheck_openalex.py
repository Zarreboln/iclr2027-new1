import re,json,glob,time,subprocess,urllib.parse,difflib,sys,unicodedata
bib=open("iclr2027_conference.bib").read()
ents={}
for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}",bib,flags=re.S):
    typ,key,body=m.groups(); f={}
    for fm in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|\d+)",body):
        f[fm.group(1).lower()]=fm.group(2).strip("{}\"").strip()
    ents[key]=(typ,f)
used=set()
for fn in ["iclr2027_conference.tex"]+glob.glob("sections/*.tex"):
    for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]+)\}",open(fn).read()):
        for k in m.group(1).split(","): used.add(k.strip())
ACC={"\\'":"","\\`":"","\\\"":"","\\^":"","\\~":"","\\c":"","\\v":""}
def delatex(t):
    t=re.sub(r"\\[`'\"^~cv=.]\{?([A-Za-z])\}?",r"\1",t); t=re.sub(r"\{\\[a-z]+\}","",t); return re.sub(r"[{}\\]","",t)
def ascii_(t): return unicodedata.normalize("NFKD",t).encode("ascii","ignore").decode().lower()
def norm_title(t): return re.sub(r"[^a-z0-9 ]","",ascii_(delatex(t))).strip()
def bib_lastnames(a):
    out=[]
    for p in re.split(r"\s+and\s+",delatex(a)):
        p=p.strip()
        if p.lower()=="others": out.append("others"); continue
        out.append(ascii_(p.split(",")[0].strip() if "," in p else p.split()[-1]))
    return out
def oa(title):
    q=urllib.parse.quote(delatex(title)); url=f"https://api.openalex.org/works?search={q}&per-page=5&mailto=zining@visionteam.me"
    for _ in range(3):
        r=subprocess.run(["curl","-s","-m","30",url],capture_output=True,text=True)
        try: return json.loads(r.stdout).get("results",[])
        except Exception: time.sleep(2)
    return []
rows=[]
for key in sorted(used):
    typ,f=ents[key]; title=f.get("title","")
    best=None;bs=0
    for w in oa(title):
        s=difflib.SequenceMatcher(None,norm_title(w.get("title") or ""),norm_title(title)).ratio()
        if s>bs: bs=s;best=w
    rec={"key":key,"type":typ,"title":delatex(title),"bib_authors":bib_lastnames(f.get("author","")),"bib_venue":delatex(f.get("booktitle",f.get("journal",""))),"bib_year":f.get("year",""),"bib_pages":f.get("pages",""),"bib_volume":f.get("volume",""),"match":round(bs,2)}
    if best:
        au=[ascii_(a["author"]["display_name"].split()[-1]) for a in best.get("authorships",[])]
        loc=best.get("primary_location") or {}; src=(loc.get("source") or {}).get("display_name")
        b=best.get("biblio") or {}
        rec.update({"oa_title":best.get("title"),"oa_authors":au,"oa_year":best.get("publication_year"),"oa_venue":src,"oa_pages":(f"{b.get('first_page')}--{b.get('last_page')}" if b.get("first_page") else ""),"oa_volume":b.get("volume"),"oa_type":best.get("type"),"oa_doi":best.get("doi"),"oa_id":best.get("id")})
    rows.append(rec); print(key,rec["match"],rec.get("oa_year"),(rec.get("oa_venue") or "")[:50],file=sys.stderr,flush=True); time.sleep(0.3)
json.dump(rows,open(sys.argv[1],"w"),indent=1,ensure_ascii=False)
# report
print("\n=== discrepancies ===")
for r in rows:
    issues=[]
    if r["match"]<0.85: issues.append(f"NO CONFIDENT MATCH (best {r['match']})")
    else:
        if str(r["bib_year"])!=str(r.get("oa_year")): issues.append(f"year bib {r['bib_year']} vs {r.get('oa_year')}")
        ba=[a for a in r["bib_authors"] if a!="others"]; oa_=r.get("oa_authors",[])
        if "others" not in r["bib_authors"] and len(ba)!=len(oa_): issues.append(f"author count bib {len(ba)} vs {len(oa_)}: {oa_}")
        else:
            miss=[a for a in ba if not any(a in x or x in a for x in oa_)]
            if miss: issues.append(f"authors not found on OpenAlex: {miss} (OA: {oa_})")
        if r["bib_pages"] and r.get("oa_pages") and r["bib_pages"].replace("–","--")!=r["oa_pages"]: issues.append(f"pages bib {r['bib_pages']} vs {r['oa_pages']}")
        if not r["bib_pages"] and r.get("oa_pages"): issues.append(f"pages missing (OA {r['oa_pages']})")
    print(f"{r['key']:16s} {r['type']:14s} bib[{r['bib_venue'][:38]} {r['bib_year']}]  OA[{(r.get('oa_venue') or '')[:38]} {r.get('oa_year')}]  " + (" | ".join(issues) if issues else "ok"))
