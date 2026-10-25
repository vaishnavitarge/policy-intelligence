import streamlit as st, pandas as pd
from src.service import ask_policy,search_policy
from src.retrieval import get_retriever
st.set_page_config(page_title="Enterprise Policy Intelligence",page_icon="📚",layout="wide")
st.title("📚 Enterprise Policy Intelligence")
st.caption("Evidence-backed policy discovery · fictional portfolio demo")
with st.sidebar:
    role=st.selectbox("Demo role",["employee","manager","hr","finance","it","admin","safety"])
    region=st.selectbox("Region",["IN","US","UK","GLOBAL"])
    st.warning("Role is a search filter only, not authentication or access control.")
    if st.button("Refresh index"): get_retriever(refresh=True); st.success("Index refreshed.")
a,b,c=st.tabs(["Ask a question","Search evidence","About"])
with a:
    q=st.text_area("Policy question",placeholder="How many annual leave days can be carried forward?")
    k=st.slider("Evidence passages",1,10,4,key="ak")
    if st.button("Find answer",type="primary"):
        if len(q.strip())<3: st.warning("Enter at least 3 characters.")
        else:
            result=ask_policy(q.strip(),role,region,k); st.subheader("Answer"); st.markdown(result["answer"])
            st.caption(f"Mode: {result['answer_mode']} · {result['result_count']} evidence passages")
            st.subheader("Sources")
            for s in result["sources"]:
                with st.expander(f"{s['doc_id']} · {s['title']} · {s['section']} · score {s['score']}"):
                    st.write(f"Owner: {s['owner']} | Region: {s['region']} | Effective: {s['effective_date']}")
                    st.write(s["content"])
            st.info(result["disclaimer"])
with b:
    q2=st.text_input("Search terms",placeholder="phishing, travel expenses, annual leave")
    k2=st.slider("Results",1,10,5,key="bk")
    if st.button("Search documents"):
        res=search_policy(q2,role,region,k2) if len(q2.strip())>=2 else {"results":[]}
        if res["results"]:
            st.dataframe(pd.DataFrame([{"ID":x["doc_id"],"Title":x["title"],"Section":x["section"],"Owner":x["owner"],"Score":x["score"],"Evidence":x["content"]} for x in res["results"]]),use_container_width=True,hide_index=True)
        else: st.info("No matching documents.")
with c:
    st.markdown("### Included capabilities\n- Markdown ingestion and chunking\n- TF-IDF + lexical retrieval\n- Metadata filters and evidence citations\n- FastAPI endpoints\n- Optional Azure OpenAI answer synthesis")
    st.warning("Synthetic policy content only. Production requires SSO, server-side authorization, audit logs, approved document lifecycle, security review, monitoring, and human-reviewed evaluation.")
