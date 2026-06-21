"""
2026 首爾 5 日遊行程網頁。
- 自動偵測韓國時間 → 預設停在「今天」是哪一天
- 頂部 Day Tab 橫向滑動
- 每天 = 主行程卡片 + 附近備案 expander + 飯店附近 expander
"""
import streamlit as st
from datetime import datetime, date, timezone, timedelta

import day1, day2, day3, day4, day5
from utils import inject_css

# 頁面基本
st.set_page_config(
    page_title="2026 首爾",
    page_icon="🇰🇷",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 注入全域 CSS (主行程卡片 + 按鈕 + 備案區塊樣式)
inject_css()

# ---- 額外的 Day Tab 橫向滑動 + 其他 UI CSS ----
# 注意：這段 CSS 必須完全靠左不縮排，否則會被 Markdown 當成程式碼印出來
st.markdown("""
<style>
/* 隱掉預設選單 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* === Day Tab 橫向滑動 === */
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
div[role="radiogroup"] label:hover {
    border-color: #ff4b4b;
}
/* 選中的那個 Day Tab 才上色 (:has 支援 iOS15.4+ / Chrome105+) */
div[role="radiogroup"] label:has(input:checked) {
    border-color: #ff4b4b !important;
    background-color: rgba(255,75,75,0.08) !important;
    box-shadow: 0 1px 4px rgba(255,75,75,0.18);
}
</style>
""", unsafe_allow_html=True)


# ==============================
# 行程資料 (顯示文字, 日期, module, 完整標題)
# ==============================
trip_dates = {
    "Day1\n6/23 二": (date(2026, 6, 23), day1, "Day 1（二）抵達 ➜ 弘대"),
    "Day2\n6/24 三": (date(2026, 6, 24), day2, "Day 2（三）聖水 ➜ 東大門"),
    "Day3\n6/25 四": (date(2026, 6, 25), day3, "Day 3（四）安國/北村 ➜ 明洞"),
    "Day4\n6/26 五": (date(2026, 6, 26), day4, "Day 4（五）望遠/延南"),
    "Day5\n6/27 六": (date(2026, 6, 27), day5, "Day 5（六）早餐 ➜ 回程"),
}

# ==============================
# 自動判斷今天是哪一 Day → 預設選那個
# 韓國時區 UTC+9 寫死 (沒日光節約)
# ==============================
KST = timezone(timedelta(hours=9))
today = datetime.now(KST).date()

# 測試用：取消下行註解可手動指定今天
# today = date(2026, 6, 25)

default_index = 0
keys = list(trip_dates.keys())
for i, k in enumerate(keys):
    if trip_dates[k][0] == today:
        default_index = i
        break

# ==============================
# 介面
# ==============================
st.title("🇰🇷 2026 首爾")
st.caption("6/23 (二) – 6/27 (六)｜9 Brick Hotel｜真航空 LJ736/LJ737")

selected_key = st.radio(
    "Day",
    keys,
    index=default_index,
    horizontal=True,
    label_visibility="collapsed",
)

# ==============================
# 真航空劃位提醒 + 優惠券快捷列
# ==============================
# LJ737 起飛: 6/27 (六) 14:50 KST
# 線上劃位開放: 起飛前 24h ~ 1.5h 前 (6/26 14:50 ~ 6/27 13:20)
checkin_open  = datetime(2026, 6, 26, 14, 50, tzinfo=KST)
checkin_close = datetime(2026, 6, 27, 13, 20, tzinfo=KST)
now_kst       = datetime.now(KST)

checkin_url = "https://www.jinair.com/login/checkinLogin?returnUrl=/checkin/checkinList"

if now_kst < checkin_open:
    # 還沒開放：顯示倒數
    hours_left = int((checkin_open - now_kst).total_seconds() // 3600)
    st.warning(
        f"✈️ **LJ737 線上劃位** 還沒開放  \n6/26 (五) 14:50 起，倒數 {hours_left} 小時"
    )
elif now_kst <= checkin_close:
    # 開放中：顯示連結
    st.error(
        f"🔴 **LJ737 線上劃位開放中！**   \n請立刻 [點此劃位]({checkin_url})（截止 6/27 13:20）"
    )
else:
    # 已起飛或過期：什麼都不顯示這格
    pass

# 優惠券快捷列
st.markdown("""
🎟️ **優惠券：**
[Olive Young](https://www.oliveyoung.co.kr/store/main/getEventList.do?menuFlag=N)｜
[新世界免稅12F](https://www.seoultravelpass.com/en/products/1562-2026-shinsegae-duty-free-benefit-coupon)｜  \n
[ABC-MART 明洞 9 折](https://creatrip.com/zh-HK/blog/13244)｜
[Visit Korea 旅客專屬](https://english.visitkorea.or.kr/svc/main/index.do)
""")
st.divider()

# 顯示當日標題 + 內容
data = trip_dates[selected_key]
_date, module, full_title = data
st.markdown(f"### {full_title}")
module.show()
