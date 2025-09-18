import streamlit as st
import pandas as pd
import requests

# 檢查 st.secrets 是否包含所需的 API 金鑰
if "short_io_api" not in st.secrets:
    st.error("找不到 API 金鑰。請在 .streamlit/secrets.toml 中設定 [short_io_api] 區塊。")
    st.stop()

# 從 secrets 中讀取 domain_id 和 authorization
domain_id = st.secrets["domain_id"]
authorization = st.secrets["authorization"]

# API 請求的 URL 和標頭
url = f'https://api.short.io/api/links?domain_id={domain_id}'
headers = {
    'Authorization': authorization,
    'accept': 'application/json'
}

st.title('短網址列表')
st.markdown('---')

try:
    # 發送 GET 請求並獲取回應
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果請求不成功，會拋出 HTTPError

    # 將回應的 JSON 內容解析為 Python 字典
    data = response.json()

    # 從 'links' 列表中提取 'title' 和 'shortURL'
    links_list = data.get('links', [])
    if links_list:
        # 創建一個 DataFrame
        extracted_data = []
        for link in links_list:
            extracted_data.append({
                'Title': link.get('title', 'N/A'),
                'Short URL': link.get('shortURL', 'N/A')
            })
        
        df = pd.DataFrame(extracted_data)
        
        # 在 Streamlit 中顯示 DataFrame
        st.dataframe(df, use_container_width=True)
    else:
        st.info("沒有找到任何短網址。")

except requests.exceptions.RequestException as e:
    # 處理 API 請求過程中的錯誤
    st.error(f"無法連接到 API 或請求失敗：{e}")
