import re
from datetime import date
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .ingestion import load_chunks

STOP={"the","a","an","is","are","to","of","and","or","in","on","for","with","what","how","who","can","i","do","my","should"}
def terms(s): return {x for x in re.findall(r"[a-z0-9]+",s.lower()) if len(x)>1 and x not in STOP}
class PolicyRetriever:
    def __init__(self,chunks=None):
        self.chunks=chunks if chunks is not None else load_chunks()
        self.vectorizer=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True)
        self.matrix=self.vectorizer.fit_transform([self.text(c) for c in self.chunks]) if self.chunks else None
    @staticmethod
    def text(c): return f"{c.get('title','')} {c.get('section','')} {c.get('content','')}"
    def search(self,query,top_k=5,role="employee",region="IN"):
        if not query.strip() or not self.chunks: return []
        sims=cosine_similarity(self.vectorizer.transform([query]),self.matrix).ravel()
        qt=terms(query); out=[]; today=date.today().isoformat()
        for i,c in enumerate(self.chunks):
            if c.get("status","active")!="active": continue
            if c.get("region","GLOBAL").upper() not in ("GLOBAL",region.upper()): continue
            if c.get("effective_date","1900-01-01")>today: continue
            aud={a.strip().lower() for a in c.get("audience","employee").split(",")}
            if "all" not in aud and role.lower() not in aud: continue
            overlap=len(qt & terms(self.text(c)))/max(1,len(qt))
            score=.78*float(sims[i])+.22*overlap
            if score>0: out.append({**c,"score":round(score,4)})
        return sorted(out,key=lambda x:x["score"],reverse=True)[:max(1,min(int(top_k),10))]
_default=None
def get_retriever(refresh=False):
    global _default
    if refresh or _default is None: _default=PolicyRetriever()
    return _default
