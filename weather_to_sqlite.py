import requests
import sqlite3
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 這是中央氣象局備用的簡單 API 路徑，成功率最高
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F&format=JSON"

try:
    print("正在連線氣象局...")
    response = requests.get(url, verify=False, timeout=10)
    data = response.json()
    
    # 針對 F-C0032-001 結構解析
    locations = data['records']['location']
    weather_data = []

    for loc in locations:
        city = loc['locationName']
        # 取出天氣描述、最低溫、最高溫
        desc = loc['weatherElement'][0]['time'][0]['parameter']['parameterName']
        min_t = loc['weatherElement'][2]['time'][0]['parameter']['parameterName']
        max_t = loc['weatherElement'][4]['time'][0]['parameter']['parameterName']
        weather_data.append((city, float(min_t), float(max_t), desc))

    # 寫入 SQLite
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS weather')
    cursor.execute('''CREATE TABLE weather (id INTEGER PRIMARY KEY AUTOINCREMENT, location TEXT, min_temp REAL, max_temp REAL, description TEXT)''')
    cursor.executemany('INSERT INTO weather (location, min_temp, max_temp, description) VALUES (?, ?, ?, ?)', weather_data)
    conn.commit()
    conn.close()
    print(f"✅ 成功解析 {len(weather_data)} 筆資料並存入 data.db")

except Exception as e:
    print(f"❌ 錯誤: {e}")