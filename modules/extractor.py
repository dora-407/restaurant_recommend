import json
import re
from typing import Dict, Any, List, Optional
from config import GEMINI_API_KEY

SYSTEM_PROMPT = """你是一位專業的美食資訊架構師。使用者會提供美食推薦貼文的內容。
你的任務是精確萃取出該餐廳的結構化資訊，並以標準 JSON 格式回傳。

請嚴格遵循以下 JSON 欄位定義：
{
  "name": "餐廳店名（請去除宣傳用形容詞，僅保留店名）",
  "city": "縣市名稱（例如：台北市、新北市、台中市、台南市、高雄市等，若無提及則填'其他'）",
  "district": "行政區或鄉鎮市區（例如：大安區、西區、板橋區，若無提及則填'其他'）",
  "address": "詳細地址或門市位置（若貼文僅提及捷運站或地標，請標註如'捷運忠孝復興站附近'；若完全未提地址請填'貼文未提及，建議搜尋店名確認'）",
  "recommended_dishes": ["推薦品項1", "推薦品項2"],
  "price_range": "價位區間（例如'NT$ 100 - 200'、'單點約80元'，若貼文完全無提及價錢，請填'未註明（依現場菜單為準）'）",
  "notes": "貼文中的心得特色、排隊狀況或特別建議（簡明扼要，1-2句話）"
}

注意事項：
1. 只輸出符合上述結構的純 JSON 字串，不要包含任何開頭或結尾的 Markdown 語法（如 ```json ... ```）。
2. 若有分店資訊且貼文特別推薦某分店，店名或地址請附上分店名。
"""

def clean_json_response(text: str) -> str:
    """清理 Markdown 標記，取得純 JSON 字串"""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text

def extract_restaurant_info(post_url: str, raw_content: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    呼叫 LLM 剖析貼文文字，回傳結構化字典。
    """
    key = api_key or GEMINI_API_KEY
    if not key:
        raise ValueError(
            "未偵測到 GEMINI_API_KEY！\n"
            "請在專案目錄下的 .env 檔案中設定 GEMINI_API_KEY=your_key，\n"
            "或傳入有效的 API Key。"
        )

    # 優先嘗試使用官方 google-genai SDK
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=key)
        prompt = f"貼文來源網址：{post_url}\n\n貼文內容如下：\n{raw_content}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                temperature=0.2,
            )
        )
        json_str = clean_json_response(response.text)
        return json.loads(json_str)

    except ImportError:
        # 相容使用舊版 google-generativeai
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=key)
            model = legacy_genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT,
                generation_config={"response_mime_type": "application/json", "temperature": 0.2}
            )
            prompt = f"貼文來源網址：{post_url}\n\n貼文內容如下：\n{raw_content}"
            response = model.generate_content(prompt)
            json_str = clean_json_response(response.text)
            return json.loads(json_str)
        except Exception as e:
            raise RuntimeError(f"呼叫舊版 Gemini API 失敗：{e}")
    except Exception as e:
        raise RuntimeError(f"呼叫 Gemini API 失敗：{e}")
