import json, re
from .config import DATA_DIR, INDEX_PATH

def parse(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    meta, body = {}, lines[:]
    if lines and lines[0].strip() == "<!--":
        end = next((i for i,x in enumerate(lines) if x.strip() == "-->"), None)
        if end is not None:
            for line in lines[1:end]:
                if ":" in line:
                    k,v = line.split(":",1); meta[k.strip().lower()] = v.strip()
            body = lines[end+1:]
    return {"doc_id":meta.get("id",path.stem.upper()),"title":meta.get("title",path.stem),
      "owner":meta.get("owner","Policy Office"),"region":meta.get("region","GLOBAL"),
      "audience":meta.get("audience","employee"),"status":meta.get("status","active").lower(),
      "effective_date":meta.get("effective_date","2026-01-01"),"source_file":path.name,"body":"\n".join(body).strip()}

def build_chunks():
    chunks=[]
    for path in sorted(DATA_DIR.glob("*.md")):
        doc=parse(path); heading="Overview"; section=[]
        def emit(h, lines):
            text=" ".join("\n".join(lines).split())
            words=text.split()
            for n,start in enumerate(range(0,len(words),145)):
                part=" ".join(words[start:start+180])
                if part:
                    chunks.append({**{k:v for k,v in doc.items() if k!="body"},"section":h,
                      "chunk_id":f"{doc['doc_id']}::{h.lower().replace(' ','-')}::{n+1}","content":part})
        for line in doc["body"].splitlines():
            if line.startswith("#"):
                if section: emit(heading,section)
                heading=line.lstrip("#").strip(); section=[]
            else: section.append(line)
        if section: emit(heading,section)
    INDEX_PATH.parent.mkdir(parents=True,exist_ok=True)
    INDEX_PATH.write_text(json.dumps(chunks,indent=2),encoding="utf-8")
    return chunks

def load_chunks():
    try:
        data=json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        if data: return data
    except (OSError,json.JSONDecodeError): pass
    return build_chunks()

if __name__=="__main__":
    rows=build_chunks()
    print(f"Built {len(rows)} chunks from {len(list(DATA_DIR.glob('*.md')))} policy documents.")
