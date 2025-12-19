import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import time

# 解決 SSL: CERTIFICATE_VERIFY_FAILED 問題
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

all_movies = []
print("--- Part 2: 電影網站爬蟲開始 (共 10 頁) ---")

for page in range(1, 11):
    url = f"https://ssr1.scrape.center/page/{page}"
    try:
        # 跳過 SSL 驗證
        res = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 抓取電影卡片
        items = soup.select('.el-card')
        for item in items:
            name = item.select_one('.m-b-sm').text.strip()
            score = item.select_one('.score').text.strip()
            img = item.select_one('.cover')['src']
            # 類型
            cats = [c.text.strip() for c in item.select('.categories button span')]
            
            all_movies.append({
                "電影名稱": name,
                "評分": score,
                "圖片URL": img,
                "類型": "/".join(cats)
            })
        print(f"✅ 第 {page}/10 頁爬取完成")
        time.sleep(0.3) # 禮貌性停頓
    except Exception as e:
        print(f"❌ 第 {page} 頁發生錯誤: {e}")

# 2. 儲存成 movie.csv
df = pd.DataFrame(all_movies)
df.to_csv('movie.csv', index=False, encoding='utf-8-sig')
print("\n--- 任務完成 ---")
print(f"已成功產出電影清單: movie.csv (共 {len(all_movies)} 筆)")