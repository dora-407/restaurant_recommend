import sys
import argparse
from modules.extractor import extract_restaurant_info
from modules.storage import save_restaurant
from modules.generator import generate_html

def collect_multiline_input() -> str:
    """收集多行使用者文字輸入，直到使用者輸入 EOF 或連續按兩次回車"""
    print("\n👉 請貼上貼文內文（貼上後，請在獨立一行輸入 'EOF' 或直接按 Enter 兩次送出）：")
    lines = []
    empty_count = 0
    while True:
        try:
            line = input()
        except EOFError:
            break
            
        if line.strip() == "EOF":
            break
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
        lines.append(line)
        
    return "\n".join(lines).strip()

def process_post(post_url: str, raw_content: str, overwrite: bool = True):
    """處理單篇貼文萃取、儲存與 HTML 更新的完整管線"""
    print("\n" + "=" * 50)
    print("🚀 開始處理貼文資訊...")
    print(f"🔗 來源連結：{post_url}")
    
    # 1. LLM 結構化萃取
    print("🤖 正在透過 AI 結構化萃取美食資訊...")
    try:
        extracted = extract_restaurant_info(post_url, raw_content)
    except Exception as e:
        print(f"❌ 萃取失敗：{e}")
        return False
        
    print("\n✅ 萃取結果：")
    print(f"  • 店名：{extracted.get('name')}")
    print(f"  • 地區：{extracted.get('city')} {extracted.get('district')}")
    print(f"  • 地址：{extracted.get('address')}")
    print(f"  • 推薦品項：{', '.join(extracted.get('recommended_dishes', []))}")
    print(f"  • 價位：{extracted.get('price_range')}")
    print(f"  • 心得備註：{extracted.get('notes')}")
    
    # 2. 資料正規化與儲存
    print("\n💾 正在儲存至資料庫並生成 Google Maps 導航連結...")
    record = save_restaurant(extracted, post_url, raw_content, overwrite=overwrite)
    print(f"📍 Maps 連結：{record.get('google_maps_url')}")
    
    # 3. 靜態網頁更新
    print("\n🌐 正在重新編譯並生成 index.html...")
    out_path = generate_html()
    print(f"✨ 完成！成果已更新至：{out_path}")
    print("=" * 50 + "\n")
    return True

def interactive_cli():
    """CLI 互動入口"""
    print("\n" + "#" * 50)
    print("  🍱 美食推薦整合器 (Food Recommendation Aggregator)")
    print("#" * 50)
    
    while True:
        try:
            post_url = input("\n👉 請輸入 IG 或 Threads 貼文網址（輸入 'q' 離開）：").strip()
            if post_url.lower() in ['q', 'quit', 'exit']:
                print("👋 感謝使用，再見！")
                break
            if not post_url:
                print("⚠️ 網址不得為空，請重新輸入。")
                continue
                
            raw_content = collect_multiline_input()
            if not raw_content:
                print("⚠️ 貼文內容不得為空，請重新輸入。")
                continue
                
            process_post(post_url, raw_content)
            
            cont = input("是否繼續新增下一篇？(Y/n): ").strip().lower()
            if cont == 'n':
                print("👋 感謝使用，已退出！")
                break
        except KeyboardInterrupt:
            print("\n👋 程式已終止。")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="美食推薦整合器 CLI")
    parser.add_argument("--url", help="貼文來源網址")
    parser.add_argument("--file", help="存放貼文內文的純文字檔路徑")
    
    args = parser.parse_args()
    
    if args.url and args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
        process_post(args.url, content)
    else:
        interactive_cli()
