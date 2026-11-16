import os
from pathlib import Path
from dotenv import load_dotenv

# 專案根目錄
BASE_DIR = Path(__file__).resolve().parent

# 載入 .env 檔案
load_dotenv(BASE_DIR / ".env")

# API 金鑰
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# 資料路徑
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "restaurants.json"

# 模板與網頁路徑
TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATE_FILE = TEMPLATES_DIR / "index_template.html"
OUTPUT_HTML = BASE_DIR / "index.html"

# 確保必要資料夾存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
