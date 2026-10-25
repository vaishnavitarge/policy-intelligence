from pathlib import Path
import os
from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
DATA_DIR = Path(os.getenv("POLICY_DATA_DIR", ROOT / "data" / "policies"))
INDEX_PATH = Path(os.getenv("POLICY_INDEX_PATH", ROOT / "data" / "processed" / "chunks.json"))
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21").strip()
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()
def has_azure_openai():
    return all([ENDPOINT, API_KEY, DEPLOYMENT])
