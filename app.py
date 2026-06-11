"""
2026 首爾 5 日遊行程網頁。
"""
import streamlit as st
from datetime import datetime, date, timezone, timedelta

import day1, day2, day3, day4, day5
from utils import inject_css

st.set_page_config(
    page_title="2026 首爾",
    page_icon="🇰🇷",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_css()

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

div[role="radiogroup"] {
    flex-direction: row !important;
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    gap: 8px;
    padding-bottom: 6px;
    -webkit-overflow-scrolling: touch;
}
div[role="radiogroup"]::-webkit-scrollbar { display: none; }
div[role="radiogroup"] label > div:first-child { display: none !important; }
div[role="radiogroup"] label {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    padding: 6px 4px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.2);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-width: 72px;
    height: 56px;
    transition: all 0.15s;
}
div[role="radiogroup"] label p {
    font-size: 13.5px;
    line-height: 1.3;
    font-weight: 700;
    margin: 0;
    padding: 0;
    width: 100%;
    white-space: pre-wrap;
    text-align: center;
}
div[role="radiogroup"] label:hover { border-color: #ff4b4b; }
div[role="radiogroup"] label[data-baseweb="radio"] {
    border-color: #ff4b4b !important;
    background-color: var(--background-color) !important;
}
</style>
""", unsafe_allow_html=True)

trip_dates = {
    "Day1\n6/23 二": (date(2026, 6, 23), day1, "Day 1（週二）抵達 ➜ 弘대"),
    "Day2\n6/24 三": (date(2026, 6, 24), day2, "Day 2（週三）聖水 ➜ 東大門"),
    "Day3\n6/25 四": (date(2026, 6, 25), day3, "Day 3（週四）安國/北村 ➜ 明洞"),
    "Day4\n6/26 五": (date(2026, 6, 26), day4, "Day 4（週五）望遠/延南/弘대採買"),
    "Day5\n6/27 六": (date(2026, 6, 27), day5, "Day 5（週六）早餐 ➜ 回程"),
}

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).date()
# today = date(2026, 6, 25)  # 測試用，解除註解可手動指定

default_index = 0
keys = list(trip_dates.keys())
for i, k in enumerate(keys):
    if trip_dates[k][0] == today:
        default_index = i
        break

st.title("🇰🇷 2026 首爾")
st.caption("6/23 (二) – 6/27 (六)｜9 Brick Hotel｜真航空 LJ736/LJ737")

selected_key = st.radio(
    "Day", keys,
    index=default_index,
    horizontal=True,
    label_visibility="collapsed",
)

# 工具列：只留 T-money
st.markdown("""
💳 [Mobile T-money](https://apps.apple.com/tw/app/id1100428659)
""")
st.divider()

data = trip_dates[selected_key]
_date, module, full_title = data
st.markdown(f"### {full_title}")
module.show()
