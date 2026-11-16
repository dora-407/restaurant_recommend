import json
import urllib.parse
from datetime import datetime
from typing import Dict, Any, List, Optional
from config import DATA_FILE

def normalize_city_name(city: str) -> str:
    """將臺北市/臺中市/臺南市等統一正規化為'台'字頭，確保地區群組一致"""
    if not city:
        return "其他"
    return city.replace("臺", "台").strip()

def clean_post_url(url: str) -> str:
    """去除社群網址後面的 utm / ig_web 等追蹤雜訊參數"""
    parsed = urllib.parse.urlparse(url)
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if not clean_url.endswith("/"):
        clean_url += "/"
    return clean_url

def determine_platform(url: str) -> str:
    """根據 URL 判斷社群來源平台（相容 threads.net 與 threads.com）"""
    lower_url = url.lower()
    if "threads.net" in lower_url or "threads.com" in lower_url:
        return "threads"
    elif "instagram.com" in lower_url:
        return "instagram"
    return "other"

def generate_google_maps_url(name: str, address: str) -> str:
    """生成免 API Key 的 Google Maps Universal Search URL"""
    # 如果地址有具體內容且不是預設提示文字
    if address and "未提及" not in address:
        query = f"{name} {address}"
    else:
        query = name
    encoded_query = urllib.parse.quote(query.strip())
    return f"https://www.google.com/maps/search/?api=1&query={encoded_query}"

def load_restaurants() -> List[Dict[str, Any]]:
    """讀取餐廳資料庫"""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_restaurants(restaurants: List[Dict[str, Any]]) -> None:
    """儲存餐廳資料庫"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(restaurants, f, ensure_ascii=False, indent=2)

def save_restaurant(
    extracted_data: Dict[str, Any],
    post_url: str,
    raw_content: str,
    overwrite: bool = True
) -> Dict[str, Any]:
    """
    新增或更新一筆餐廳資料，並回傳儲存的完整物件
    """
    restaurants = load_restaurants()
    
    # 檢查是否已存在相同 post_url
    existing_idx = next((i for i, r in enumerate(restaurants) if r.get("post_url") == post_url), None)
    
    now_str = datetime.now().astimezone().isoformat(timespec="seconds")
    
    name = extracted_data.get("name", "未命名餐廳").strip()
    address = extracted_data.get("address", "貼文未提及，建議搜尋店名確認").strip()
    city = extracted_data.get("city", "其他").strip()
    district = extracted_data.get("district", "其他").strip()
    
    # 計算 Google Maps 連結
    maps_url = generate_google_maps_url(name, address)
    
    restaurant_record = {
        "id": f"rest_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "name": name,
        "city": city,
        "district": district,
        "address": address,
        "recommended_dishes": extracted_data.get("recommended_dishes", []),
        "price_range": extracted_data.get("price_range", "未註明（依現場菜單為準）"),
        "post_url": post_url,
        "source_platform": determine_platform(post_url),
        "google_maps_url": maps_url,
        "raw_content": raw_content,
        "notes": extracted_data.get("notes", ""),
        "created_at": now_str
    }
    
    if existing_idx is not None:
        if overwrite:
            # 保留原本的 ID 與建立時間
            restaurant_record["id"] = restaurants[existing_idx]["id"]
            restaurant_record["created_at"] = restaurants[existing_idx].get("created_at", now_str)
            restaurant_record["updated_at"] = now_str
            restaurants[existing_idx] = restaurant_record
        else:
            return restaurants[existing_idx]
    else:
        restaurants.append(restaurant_record)
        
    save_restaurants(restaurants)
    return restaurant_record
