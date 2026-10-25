from src.ingestion import build_chunks
from src.retrieval import PolicyRetriever
def test_leave_policy():
    r=PolicyRetriever(build_chunks()).search("How many annual leave days can be carried forward?",role="employee",region="IN")
    assert any(x["doc_id"]=="HR-LEAVE-001" for x in r)
def test_privileged_doc_filtered_from_employee():
    r=PolicyRetriever(build_chunks()).search("privileged system access administrator",role="employee",region="IN")
    assert all(x["doc_id"]!="IT-PRIV-008" for x in r)
def test_privileged_doc_for_it():
    r=PolicyRetriever(build_chunks()).search("privileged system access administrator",role="it",region="IN")
    assert any(x["doc_id"]=="IT-PRIV-008" for x in r)
