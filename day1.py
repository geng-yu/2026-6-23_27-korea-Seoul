"""Day 1 (6/23 二) — 抵達 ➜ 弘대本區"""
import streamlit as st
from utils import show_stop, show_hotel_nearby


def show():
    st.caption("📍 6/23 (二)｜14:15 抵達仁川 T2 → 弘대 9 Brick Hotel")

    # ==============================
    # 0. 自行開車 → RMQ
    # ==============================
    show_stop("08:00", "rmq",
              override_note="",show_taxi=False, no_backup=True)

    # ==============================
    # 1. 飛行
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">10:40</div>
      <div class="body">
        <h4>🛫 Jin Air LJ736</h4>
        <p class="meta">真航空｜經濟艙｜Boeing 737 MAX 8｜2h35m</p>
        <p class="note">RMQ → ICN T2 抵達 14:15。<b>抵達是 T2 不是 T1</b>，AREX 跟巴士都在 T2。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 2. 仁川 T2 入境流程
    # ==============================
    show_stop("14:15", "icn_t2",
              override_note="入境動線：1) 跟著「Arrival/도착」走 → 2) 入境審查 (準備 K-ETA) → 3) 1F 行李轉盤 → 4) 海關 → 5) 1F 入境大廳 (找 CU 加值 T-money)",
              show_taxi=False, no_backup=True)

    # ==============================
    # 3. T-money 加值
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">15:00</div>
      <div class="body">
        <h4>💳 加值 T-money</h4>
        <p class="meta">CU / GS25 / 7-Eleven｜建議 ₩50,000-100,000</p>
        <p class="note">出發前已用 Apple Wallet 加好卡 (餘額₩0)，這邊用現金或 Mastercard 加值。
        Visa 不能用 App 加值，現金最穩。跟店員說「티머니 충전 (Tmoney chong-jeon)」+ 金額，手機背面靠讀卡機。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 4. AREX 一般車 T2 → 弘대入口
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">15:30</div>
      <div class="body">
        <h4>🚆 AREX 一般車 (T2 → 弘대입구)</h4>
        <p class="meta">B1 交通中心｜<b>藍色閘門</b> (不要走橘色)｜₩4,750｜55min</p>
        <p class="note">下到 B1 找「AREX」指標 → <b>藍色 (一般)</b> 閘門進站 → 月台搭往 Seoul Station 方向 → 第 11 站「홍대입구」下車。
        橘色閘門是直達車 (Express)，不停弘대。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 5. 弘대入口站 → 飯店
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">16:30</div>
      <div class="body">
        <h4>🚶 弘대입구站 9 號出口 → 9 Brick Hotel</h4>
        <p class="meta">走路 6 min｜450m</p>
        <p class="note">9 號出口 (有手扶梯) → 直走 150m → 左轉 → 第一條小巷右轉 → 直走 2 min。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    show_stop("16:40", "hotel", override_note="Check-in 15:00 / Check-out 11:00")

    # ==============================
    # 6. Olive Young 補貨
    # ==============================
    show_stop("17:30", "olive_young_hongdae",
              override_note="美妝藥妝旗艦店，三層樓，飯店走 5 min。建議第一天大買，最後一天還可以補貨。")

    # ==============================
    # 7. 弘대主街
    # ==============================
    show_stop("18:30", "hongdae_street",
              override_note="弘益路 (Hongik-ro) 主街，街頭表演、潮店、咖啡。慢慢晃晃。")

    # ==============================
    # 8. 晚餐：肉夢
    # ==============================
    show_stop("19:30", "yukmong",
              override_note="三層樓燒烤，使用者⭐優先。Google 4.8 / 3000+ 評論。沒位置就跳備案的其他燒烤。")

    # ==============================
    # 9. AK Plaza + 弘대商店街
    # ==============================
    show_stop("21:30", "ak_plaza",
              override_note="弘대입구站直結，潮玩百貨。順路逛 ARTBOX (1樓) 買伴手禮。")

    # ==============================
    # 10. 宵夜：BHC 起司炸雞
    # ==============================
    show_stop("22:30", "bhc",
              override_note="起司炸雞 (시그니처)、玫瑰辣炒年糕，配啤酒。飯店走 3 min。")

    # ==============================
    # 飯店附近 (永遠在最下面)
    # ==============================
    # 排除今天主行程已經安排的，避免重複
    show_hotel_nearby(exclude_ids=[
        "yukmong", "bhc", "olive_young_hongdae", "ak_plaza", "hongdae_street"
    ])


if __name__ == "__main__":
    show()
