"""Day 5 (6/27 六) — 早餐 + 回程"""
import streamlit as st
from utils import stop, note, hotel_bottom


def show_day():
    st.caption("📍 6/27 (六)｜弘대 → ICN T2｜LJ737 14:50 起飛")

    note("🧳", "退房 (Check-out)",
              "9 Brick Hotel · 11:00 前 / 行李寄 lobby",
              "寄完行李去吃早餐，回來拿。")

    stop("早", "baeknyeon", others="food",
         notes="⭐優先。2017 米其林推介，09:00 開門。走路 4 min。"
               "想清淡 → 跳「其他」Egg Drop 或 Moment Coffee。")

    note("💳", "T-money 餘額處理",
              "趕在登機前讓餘額 ≤ ₩20,000",
              "便利店買水/零食用嗶卡用掉。&gt;₩20,000 要去總公司退太麻煩。"
              "&le;₩20,000 在 CU/GS25 都可退現金 (扣 ₩500 手續費)。")

    stop("逛", "olive_young_hongdae",
         notes="最後補貨。3 樓有藥品/保健品，記得拿退稅單。")

    note("🧳", "飯店拿行李 → 出發",
              "弘대입구站 9 號出口走 6 min",
              "進站走 AREX (不走 2 號線方向)")

    note("🚆", "AREX 一般車 (홍대입구 → 인천공항 T2)",
              "B1 月台 · 藍色閘門 · ₩4,750/人 · 55 min",
              "方向：往「인천공항 T2」終點站。"
              "弘대입구是部分班次始發站，有機會搶到座位。")

    note("🛬", "ICN T2 → LJ737 報到",
              "3F 出境大廳 · 真航空櫃台 · 起飛前 2 小時開放 (12:50)",
              "退稅機要在報到前處理 (找 KIOSK 或 Global Blue 櫃台)")

    note("🍔", "過海關 → 候機",
              "14:00 / T2 28 號登機門附近",
              "想吃 SHAKE SHACK 或逛免稅店 (新羅、樂天)")

    note("✈️", "Jin Air LJ737",
              "14:50 ICN T2 → 16:30 RMQ · 經濟艙 / 737 MAX 8 / 2h40m")

    # 最後一天還是放飯店附近 (萬一早上多出時間)
    hotel_bottom(
        today_food=["baeknyeon"],
        today_shop=["olive_young_hongdae"],
    )


def show():
    show_day()

if __name__ == "__main__":
    stop()
