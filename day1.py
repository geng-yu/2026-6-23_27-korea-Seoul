"""Day 1 (6/23 二) — 抵達 ➜ 弘大"""
import streamlit as st
from utils import stop, note, hotel_bottom


def show_day():
    st.caption("📍 6/23 (二)｜14:15 抵達 ICN T2 → 弘대 9 Brick Hotel")

    # ============ 出發 → 抵達弘대 ============
    note("行", "自駕 → 台中機場 RMQ",
         "08:00 出發 / 起飛前 2 小時抵達",
         "建議停第二航廈停車場(室內) 或周邊配合私人停車場")

    note("✈️", "Jin Air LJ736",
         "10:40 RMQ → 14:15 ICN T2 · 經濟艙 / 737 MAX 8 / 2h35m",
         "抵達是 T2 不是 T1，AREX 跟巴士都在 T2")

    note("行", "ICN T2 入境",
         "14:15 抵達",
         "動線：跟著「Arrival / 도착」走 → 入境審查 (準備 K-ETA) → 1F 行李轉盤 → 海關 → 入境大廳")

    note("💳", "加值 T-money",
         "CU / GS25 in T2 入境大廳 · 建議 ₩50,000-100,000",
         "出發前 Apple Wallet 已加好卡 (餘額₩0)，這邊用現金加值。"
         "跟店員說「티머니 충전 (Tmoney chong-jeon) ₩30,000」→ 手機背面靠讀卡機。")

    note("🚆", "AREX 一般車 (T2 → 홍대입구)",
         "B1 月台 · 藍色閘門 · ₩4,750/人 · 55 min",
         "⚠️ 不要走橘色閘門 (Express 直達車不停弘대)。"
         "方向：往 Seoul Station，第 11 站「홍대입구」下車。")

    note("🚶", "弘대입구 9 號出口 → 9 Brick Hotel",
         "走路 6 min / 450 m",
         "9 號出口有手扶梯 → 直走 150m → 左轉 → 第一條巷子右轉 → 直走 2 min")

    st.divider()

    # ============ 晚間活動 ============
    # 晚餐 + 其他吃
    stop("晚", "yukmong", others="food",
         notes="⭐優先。三層樓燒烤，Google 4.8 / 3000+ 評論。沒位置就跳「其他」")

    # 逛街 (group: 3 家) + 其他逛
    stop("逛", ["olive_young_hongdae", "hongdae_street", "ak_plaza"], others="shop",
         notes=[
             "美妝藥妝旗艦店，三層樓。建議第一天大買，最後一天還可補貨。",
             "弘益路主街，街頭表演 + 潮店 + 咖啡。慢慢晃。",
             "弘대입구站直結，潮玩百貨。1樓 ARTBOX 必逛買伴手禮。",
         ])

    # 宵夜 + 其他吃
    stop("宵", "bhc", others="food",
         notes="起司炸雞 시그니처 / 玫瑰辣炒年糕，配啤酒。飯店走 3 min。")

    # ============ 最下面：住 + 飯店附近 ============
    hotel_bottom(
        today_food=["yukmong", "bhc"],
        today_shop=["olive_young_hongdae", "hongdae_street", "ak_plaza"],
    )


# 對外接口統一叫 show()，方便 app.py 呼叫
def show():
    show_day()


if __name__ == "__main__":
    show()
