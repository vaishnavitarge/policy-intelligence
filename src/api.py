from fastapi import FastAPI
from pydantic import BaseModel,Field
from .service import ask_policy,search_policy
from .retrieval import get_retriever
app=FastAPI(title="Enterprise Policy Intelligence API",version="1.0.0")
class Ask(BaseModel):
    question:str=Field(min_length=3,max_length=1000); role:str="employee"; region:str="IN"; top_k:int=Field(5,ge=1,le=10)
class Search(BaseModel):
    query:str=Field(min_length=2,max_length=1000); role:str="employee"; region:str="IN"; top_k:int=Field(5,ge=1,le=10)
@app.get("/")
def root(): return {"message":"Enterprise Policy Intelligence API","docs":"/docs","health":"/health"}
@app.get("/health")
def health(): return {"status":"ok","indexed_chunks":len(get_retriever().chunks)}
@app.post("/ask")
def ask(req:Ask): return ask_policy(req.question,req.role,req.region,req.top_k)
@app.post("/search")
def search(req:Search): return search_policy(req.query,req.role,req.region,req.top_k)
