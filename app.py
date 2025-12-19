import streamlit as st
import sqlite3
import pandas as pd

st.title("🌦️ 中央氣象局天氣預報資料")

# 讀取 SQLite 資料
conn = sqlite3.connect('data.db')
df = pd.read_sql_query("SELECT * FROM weather", conn)
conn.close()

# 顯示資料表格
st.subheader("各地區溫度統計表")
st.dataframe(df, use_container_width=True)

# 額外小功能：顯示簡單圖表
st.line_chart(df.set_index('location')[['min_temp', 'max_temp']])