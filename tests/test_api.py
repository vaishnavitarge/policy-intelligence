from fastapi.testclient import TestClient
from src.api import app
client=TestClient(app)
def test_health():
    r=client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"
def test_ask():
    r=client.post("/ask",json={"question":"How many annual leave days can be carried forward?","role":"employee","region":"IN","top_k":4})
    assert r.status_code==200 and "sources" in r.json()
