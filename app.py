# 檔案名稱：app.py
import streamlit as st
from datetime import datetime, date
import pytz  # 用於處理時區

# 匯入每一天的模組
import day1, day2, day3, day4, day5

# --- 頁面基本設定 ---
st.set_page_config(
    page_title="2026 首爾",
    page_icon="🇰🇷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS 優化 (深色模式適應 + 橫向捲動 + 按鈕置中) ---
st.markdown("""
    <style>
    /* 全域按鈕樣式 */
    .stButton button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        border: 1px solid var(--text-color);
        opacity: 0.8;
    }

    /* 隱藏預設選單與頁尾 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Day Card 樣式 - 自動適應深淺色 */
    .day-card {
        background-color: var(--secondary-background-color);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

    /* --- 橫向滑動導覽列 CSS 魔改 --- */

    /* 1. 容器設定：橫向排列、可滑動 */
    div[role="radiogroup"] {
        flex-direction: row;
        overflow-x: auto;
        flex-wrap: nowrap !important;
        gap: 8px;
        padding-bottom: 5px;
        -webkit-overflow-scrolling: touch;
    }

    /* 2. 徹底隱藏 Radio 的圓圈 */
    div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    /* 3. 按鈕外觀 (未選中) - 使用變數適應深淺色模式 */
    div[role="radiogroup"] label {
        background-color: var(--secondary-background-color);
        color: var(--text-color);

        padding: 6px 4px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        cursor: pointer;
        transition: all 0.2s;

        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;

        min-width: 68px;
        height: 55px;
    }

    /* 4. 文字內容設定 */
    div[role="radiogroup"] label p {
        font-size: 14px;
        line-height: 1.3;
        font-weight: bold;
        margin: 0px !important;
        padding: 0px !important;
        width: 100%;
        white-space: pre-wrap;
        text-align: center;
    }

    /* 5. 滑鼠滑過或被選中時的樣式 */
    div[role="radiogroup"] label:hover {
        border-color: #ff4b4b;
        background-color: var(--background-color);
    }

    div[role="radiogroup"] label[data-baseweb="radio"] {
        border-color: #ff4b4b !important;
        background-color: var(--background-color) !important;
    }

    div[role="radiogroup"]::-webkit-scrollbar {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 資料設定 ---
# 格式: Key顯示文字 : (日期物件, 模組, 完整標題)
trip_dates = {
    "Day1\n6/23 二": (date(2026, 6, 23), day1, "Day 1(二): 出發 & 抵達弘大"),
    "Day2\n6/24 三": (date(2026, 6, 24), day2, "Day 2(三): "),
    "Day3\n6/25 四": (date(2026, 6, 25), day3, "Day 3(四): "),
    "Day4\n6/26 五": (date(2026, 6, 26), day4, "Day 4(五): "),
    "Day5\n6/27 六": (date(2026, 6, 27), day5, "Day 5(六): 回程"),
}

# --- 自動判斷日期邏輯 (使用韓國時間) ---
# 韓國時區 = Asia/Seoul (KST, UTC+9，與日本時間相同)
korea_tz = pytz.timezone('Asia/Seoul')
today = datetime.now(korea_tz).date()

# --- 測試區 (測試完請註解掉下面這行) ---
# today = date(2026, 6, 23)
# ------------------------------------

default_index = 0
options = list(trip_dates.keys())

for i, key in enumerate(options):
    d = trip_dates[key][0]
    if d == today:
        default_index = i
        break

# --- 介面呈現 ---
st.title("🇰🇷 2026 首爾")
st.caption("6/23~27")

selected_key = st.radio(
    "選擇行程日期",
    options,
    index=default_index,
    horizontal=True,
    label_visibility="collapsed"
)

# --- 韓國常用 App / 優惠券區塊 (之後可以慢慢補) ---
st.markdown("""
🗺️ **地圖：** [NAVER Map](https://apps.apple.com/tw/app/naver-map-navigation/id311867728)｜
[KakaoMap](https://apps.apple.com/tw/app/kakaomap/id304608425)｜
🚕 [Kakao T](https://apps.apple.com/tw/app/kakao-t/id981110422)
""")
st.markdown("""
💳 **支付/交通：** Apple Wallet 加 T-money｜
📶 [Mobile T-money App](https://apps.apple.com/tw/app/id1100428659)
""")
st.divider()

# --- 顯示內容 ---
selected_data = trip_dates[selected_key]
target_module = selected_data[1]
full_title = selected_data[2]

st.markdown(f"### {full_title}")

target_module.show()
