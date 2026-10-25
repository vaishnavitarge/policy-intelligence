# Enterprise Policy Intelligence and Knowledge Platform

Runnable portfolio prototype: document ingestion, metadata-aware retrieval, evidence-backed Q&A, Streamlit UI, FastAPI, tests, evaluation, Docker, and Azure App Service workflow.

**Safety note:** all policy content is fictional. The role selector is a search filter, not authentication. Do not use real confidential policies without security, privacy, and access-control engineering.

## 1. Local setup (Windows PowerShell / VS Code)
Extract ZIP to a simple folder, open that folder in VS Code, then run in the terminal:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m src.ingestion
streamlit run dashboard.py
```
Open `http://localhost:8501`. Example questions: “How many annual leave days can be carried forward?”, “What should I do if I receive a phishing email?”, “How soon should I submit travel expenses?”

If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
Use Python 3.11 for the most predictable setup.

## 2. Start API in a second terminal
Keep Streamlit running. Open another VS Code terminal:
```powershell
.\.venv\Scripts\Activate.ps1
uvicorn src.api:app --reload --host 127.0.0.1 --port 8000
```
Visit `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8000/health`.
PowerShell API example:
```powershell
$body = @{ question = "How many annual leave days can be carried forward?"; role = "employee"; region = "IN"; top_k = 4 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" -Method Post -ContentType "application/json" -Body $body
```
Search endpoint uses `POST /search` with `query`, `role`, `region`, and `top_k`.

## 3. Tests and evaluation
```powershell
pytest -q
python scripts/evaluate.py
```
The small Recall@5 test is a smoke test, not a reliable production benchmark.

## 4. Optional Azure OpenAI
Without credentials, local retrieval returns evidence excerpts. To enable answer synthesis, copy `.env.example` to `.env` and set `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_API_VERSION`, and `AZURE_OPENAI_DEPLOYMENT` (the deployment name in your Azure resource). Never commit `.env` or expose keys. Azure OpenAI is optional and may incur charges.

## 5. GitHub
Create an empty GitHub repository called `enterprise-policy-intelligence`, then run:
```powershell
git init
git add .
git status
git commit -m "Build Enterprise Policy Intelligence platform"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/enterprise-policy-intelligence.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. `.env` and `.venv` are ignored.

## 6. Deploy Streamlit frontend to Azure App Service using GitHub Actions
The included `.github/workflows/azure-webapp.yml` deploys the **Streamlit dashboard only**. The FastAPI service is not deployed by this workflow.

1. In Azure Portal create a Web App: Publish **Code**, Runtime **Python 3.11** (if available), OS **Linux**, unique app name. Review pricing; resources can cost money.
2. In Web App settings, set startup command:
   `python -m streamlit run dashboard.py --server.port 8000 --server.address 0.0.0.0 --server.headless true`
   Save/restart. Portal wording varies by UI version.
3. In Azure Web App → **Get publish profile**, download the XML.
4. In GitHub repo → **Settings → Secrets and variables → Actions** create secret `AZURE_WEBAPP_PUBLISH_PROFILE` and paste the complete XML.
5. Create repository variable `AZURE_WEBAPP_NAME` with the exact app name.
6. Commit/push the workflow if needed; open GitHub **Actions** and inspect the run.
7. Open `https://YOUR-WEBAPP-NAME.azurewebsites.net`. Confirm the page loads; a green workflow alone does not prove app startup. If it fails, check Azure **Log stream**, startup command, variable/secret names, then restart.
8. If using Azure OpenAI, configure those environment variables under the Web App's Environment variables/settings. Do not put keys in GitHub code.

## 7. Docker (optional)
Install Docker Desktop first, then:
```powershell
docker compose up --build
```
Open `http://localhost:8501`. Stop with Ctrl+C, then `docker compose down`.

## Architecture and limitations
Markdown files → chunk index → TF-IDF plus lexical-overlap retrieval → evidence-first answer (optional Azure OpenAI) → Streamlit and FastAPI. This is a portfolio prototype, not a production-grade security boundary. Before enterprise use, add Entra ID/SSO, server-side authorization, durable managed search/vector index, audit logs, document approvals/versioning, prompt-injection defenses, PII controls, monitoring, load/security tests, and a larger human-reviewed evaluation set. For public cloud deployment, this starter workflow deploys only the UI; host FastAPI separately if required.
