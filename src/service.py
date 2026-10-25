from .retrieval import get_retriever
from .answering import answer,sources
def ask_policy(question,role="employee",region="IN",top_k=5):
    rows=get_retriever().search(question,top_k,role,region); text,mode=answer(question,rows)
    return {"question":question,"answer":text,"answer_mode":mode,"result_count":len(rows),"sources":sources(rows),
      "disclaimer":"Fictional portfolio demo. Verify approved policy; role selection is not authentication."}
def search_policy(query,role="employee",region="IN",top_k=5):
    rows=get_retriever().search(query,top_k,role,region)
    return {"query":query,"result_count":len(rows),"results":sources(rows)}
