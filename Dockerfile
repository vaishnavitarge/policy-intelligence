FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m src.ingestion
EXPOSE 8000
CMD ["python","-m","streamlit","run","dashboard.py","--server.port","8000","--server.address","0.0.0.0","--server.headless","true"]
