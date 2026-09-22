#!/usr/bin/env python3
"""Drive the user's Chrome (Apple Events JavaScript) to pull Google Scholar's BibTeX for every cited entry.
Writes scholar_bibtex.json {key: {title, scholar_title, bibtex}} and a log; pauses on CAPTCHA until the user solves it."""
import re,json,glob,time,subprocess,urllib.parse,sys,os
os.chdir(os.path.expanduser("~/Desktop/iclr2027-new"))
OUT=sys.argv[1]; LOG=open(sys.argv[2],"a")
def log(*a): print(*a,file=LOG,flush=True)
bib=open("iclr2027_conference.bib").read()
ents={}
for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}",bib,flags=re.S):
    typ,key,body=m.groups(); f={}
    for fm in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|\d+)",body): f[fm.group(1).lower()]=fm.group(2).strip("{}\"").strip()
    ents[key]=(typ,f)
used=set()
for fn in ["iclr2027_conference.tex"]+glob.glob("sections/*.tex"):
    for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]+)\}",open(fn).read()):
        for k in m.group(1).split(","): used.add(k.strip())
def delatex(t): t=re.sub(r"\\[`'\"^~cv=.]\{?([A-Za-z])\}?",r"\1",t); return re.sub(r"[{}\\]","",t)
def osa(script):
    r=subprocess.run(["osascript","-e",script],capture_output=True,text=True); return r.stdout.strip() if r.returncode==0 else "OSA_ERR:"+r.stderr.strip()
def js(code):
    code=code.replace("\\","\\\\").replace('"','\\"')
    return osa(f'tell application "Google Chrome" to execute front window\'s active tab javascript "{code}"')
def goto(url):
    osa(f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"')
def wait_page(timeout=40):
    t0=time.time()
    while time.time()-t0<timeout:
        st=js("(document.readyState==='complete'?'C':'L')+'|'+(document.querySelector('.gs_r[data-cid]')?'R':'')+(document.querySelector('#gs_captcha_f, #captcha-form, form#captcha, iframe[src*=recaptcha], #recaptcha')?'X':'')+(document.querySelector('.gs_alrt')?'Z':'')")
        if "R" in st: return "results"
        if "X" in st: return "captcha"
        if st.startswith("C") and "Z" in st: return "noresults"
        time.sleep(0.7)
    return "timeout"
def fetch_text(url):
    js(f"window.__t=null;fetch('{url}').then(r=>r.text()).then(t=>{{window.__t=t}}).catch(e=>{{window.__t='ERR:'+e}})")
    for _ in range(60):
        time.sleep(0.5); v=js("window.__t===null?'__PENDING__':window.__t")
        if v!="__PENDING__": return v
    return "ERR:timeout"
res=json.load(open(OUT)) if os.path.exists(OUT) else {}
osa('tell application "Google Chrome"\nif (count of windows)=0 then make new window\ntell front window to make new tab with properties {URL:"https://scholar.google.com/"}\nend tell')
time.sleep(3)
for key in sorted(used):
    if key in res and res[key].get("bibtex","").startswith("@"): continue
    typ,f=ents[key]; title=delatex(f.get("title",""))
    QOVERRIDE=json.loads(os.environ.get("QOVERRIDE","{}"))
    q=urllib.parse.quote_plus(QOVERRIDE.get(key,title))
    goto(f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={q}")
    st=wait_page()
    while st=="captcha":
        log(f"[{key}] CAPTCHA — waiting for the user"); print(f"CAPTCHA on {key}: please solve it in Chrome",flush=True)
        for _ in range(600):
            time.sleep(2); st=wait_page(5)
            if st!="captcha": break
    if st!="results":
        res[key]={"title":title,"error":st}; log(f"[{key}] {st}"); json.dump(res,open(OUT,"w"),indent=1,ensure_ascii=False); time.sleep(3); continue
    cid=js("document.querySelector('.gs_r[data-cid]').dataset.cid"); stitle=js("document.querySelector('.gs_r[data-cid] .gs_rt').innerText")
    def load_text(url,timeout=30):
        goto(url); t0=time.time()
        while time.time()-t0<timeout:
            st=js("document.readyState")
            if st=="complete" and js("location.href").startswith(url[:40]): break
            time.sleep(0.5)
        time.sleep(0.8)
        return js("document.documentElement.outerHTML")
    cite_url=f"https://scholar.google.com/scholar?q=info:{cid}:scholar.google.com/&output=cite&scirp=0&hl=en"
    html=load_text(cite_url); m=re.search(r'href="([^"]*scholar\.bib[^"]*)"',html)
    tries=0
    while not m and ("captcha" in html.lower() or "recaptcha" in html.lower()) and tries<30:
        log(f"[{key}] CAPTCHA on cite page — waiting"); print(f"CAPTCHA (cite) on {key}: please solve it in Chrome",flush=True)
        time.sleep(15); html=js("document.documentElement.outerHTML"); m=re.search(r'href="([^"]*scholar\.bib[^"]*)"',html); tries+=1
    if not m:
        res[key]={"title":title,"scholar_title":stitle,"error":"no bibtex link","cite_html":re.sub(r"<[^>]+>"," ",html)[:300]}; log(f"[{key}] no bibtex link"); json.dump(res,open(OUT,"w"),indent=1,ensure_ascii=False); time.sleep(3); continue
    link=m.group(1).replace("&amp;","&")
    if not link.startswith("http"): link="https://scholar.google.com"+link
    goto(link); time.sleep(2.5)
    for _ in range(20):
        bt=js("document.body?document.body.innerText:''")
        if bt.strip().startswith("@"): break
        time.sleep(0.7)
    res[key]={"title":title,"scholar_title":stitle,"bibtex":bt}; log(f"[{key}] ok: {stitle[:60]} | {bt[:60]!r}"); print(f"{key}: {stitle[:70]}",flush=True)
    json.dump(res,open(OUT,"w"),indent=1,ensure_ascii=False); time.sleep(4)
print("SCHOLAR_DONE",flush=True); log("SCHOLAR_DONE")
