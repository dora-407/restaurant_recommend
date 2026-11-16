import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from config import TEMPLATES_DIR, TEMPLATE_FILE, OUTPUT_HTML
from modules.storage import load_restaurants

def generate_html() -> str:
    """
    讀取最新餐廳資料並生成 index.html
    回傳生成之 HTML 絕對路徑字串
    """
    restaurants = load_restaurants()
    
    # 按建立時間倒序排列（新加入的在最前面）
    sorted_restaurants = sorted(
        restaurants, 
        key=lambda r: r.get("created_at", ""), 
        reverse=True
    )
    
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(TEMPLATE_FILE.name)
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    rendered_content = template.render(
        restaurants=sorted_restaurants,
        restaurants_json=json.dumps(sorted_restaurants, ensure_ascii=False),
        last_updated=now_str
    )
    
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(rendered_content)
        
    return str(OUTPUT_HTML)

if __name__ == "__main__":
    out = generate_html()
    print(f"HTML 生成完畢：{out}")
