# 美食推薦整合器 (Food Recommendation Aggregator)

> 一個將 Instagram 與 Threads 社群美食推薦貼文自動轉化為結構化資訊、Google Maps 導航地標與地區分類響應式網頁的 AI 輔助工具。

---

## 🌟 核心特色

1. **社群資訊結構化**：運用 LLM 自動從非結構化貼文中萃取「店名、詳細地址、推薦品項、價位區間、營業時間與備註」。
2. **直開 Google Maps**：自動生成標準 Google Maps Universal Search 導航連結，手機點擊可直接喚起 Google Maps App。
3. **多層級地區標籤分類**：支援「縣市總覽 (如 📍台南市、📍高雄市)」與「具體生活圈 (如 永康區、中西區、鹽埕區)」一鍵切換過濾。
4. **即時檢索 (Instant Search)**：全站純前端秒級關鍵字搜尋（店名、餐點、地址、特色標籤）。
5. **免編譯輕量部署**：產出的 `index.html` 可直接透過 GitHub Pages 免費架設為手機友善的公開網站。

---

## 📁 專案架構

```
.
├── AGENTS.md                 # 系統規格書與 AI Agent 指引
├── README.md                 # 專案說明文件
├── requirements.txt          # Python 依賴清單
├── .env.example              # API Key 環境變數範本
├── config.py                 # 專案路徑與環境設定
├── modules/
│   ├── storage.py            # 資料儲存、Google Maps 連結生成與臺/台正規化
│   ├── extractor.py          # Gemini AI 結構化資訊萃取器
│   └── generator.py          # 靜態網頁編譯與渲染器
├── templates/
│   └── index_template.html   # 現代化 RWD 網頁模板 (Tailwind CSS)
├── data/
│   └── restaurants.json      # 核心結構化餐廳資料庫
├── main.py                   # 終端機互動式執行入口
└── index.html                # 成果展示網頁 (支援 GitHub Pages)
```

---

## 🚀 快速開始

### 1. 安裝環境依賴
```bash
pip install -r requirements.txt
```

### 2. 設定 API Key
複製 `.env.example` 為 `.env`，並填入 Google Gemini API Key：
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. 執行程式新增美食
```bash
python main.py
```
依提示貼入 Instagram 或 Threads 的貼文網址與複製內文，系統將自動解析、存入 `data/restaurants.json`，並更新產出 `index.html`。

---

## 🌐 如何透過 GitHub Pages 發布線上網站

1. 將本專案推送到您的 GitHub Repository。
2. 進入 Repository 頁面的 **Settings** > **Pages**。
3. 在 **Build and deployment** 下方的 **Branch** 選擇 `main`，資料夾選擇 `/ (root)`，點擊 **Save**。
4. 等待 1~2 分鐘，即可獲得您專屬的公開網站網址（例如 `https://your-name.github.io/your-repo/`），在手機上隨開隨用！
