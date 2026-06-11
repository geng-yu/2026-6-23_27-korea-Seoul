"""Day 1 (6/23 二) — 抵達 ➜ 弘대本區"""
import streamlit as st
from utils import show_stop, show_hotel_nearby


def show():
    st.caption("📍 6/23 (二)｜10:40 RMQ 起飛 → 14:15 仁川 T2 抵達 → 弘대 9 Brick Hotel")

    # ==============================
    # 0. 出發 RMQ
    # ==============================
    show_stop("08:00", "rmq",
              override_note=" ",
              show_g=True, show_n=False, show_t=False,
              mode="driving",
              no_backup=True)

    # ==============================
    # 1. 飛行
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">10:40</div>
      <div class="body">
        <h4>🛫 Jin Air LJ736</h4>
        <p class="meta">真航空｜經濟艙｜Boeing 737 MAX 8｜2h35m</p>
        <p class="note">RMQ → ICN T2 抵達 14:15</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 2. 仁川 T2 入境
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">14:15</div>
      <div class="body">
        <div class="title-row">
          <h4>🛬 仁川 T2 入境</h4>
        </div>
        <p class="meta">인천공항 제2터미널｜機場 · 24h</p>
        <p class="note">入境動線：① Arrival/도착 → ② 入境審查 (準備 K-ETA) → ③ 1F 行李轉盤 → ④ 海關 → ⑤ 1F 入境大廳</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 3. T-money 加值
    # ==============================
    # st.markdown("""
    # <div class="stop-card">
    #   <div class="time">15:00</div>
    #   <div class="body">
    #     <h4>💳 加值 T-money</h4>
    #     <p class="meta">CU / GS25 / 7-Eleven｜建議 ₩50,000–100,000</p>
    #     <p class="note">跟店員說「티머니 충전 (Tmoney chong-jeon)」+ 金額，手機背面靠讀卡機。Visa 不能用 App 加值，現金最穩。</p>
    #   </div>
    # </div>
    # """, unsafe_allow_html=True)
    # ==============================
    # 4. AREX T2 → 弘大입구
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">15:30</div>
      <div class="body">
        <h4>🚆 AREX 一般車 (T2 → 弘대입구)</h4>
        <p class="meta">B1 交通中心｜<b>藍色閘門</b> (勿走橘色)｜₩4,750｜55 min</p>
        <p class="note">B1 找「AREX」指標 → 藍色閘門進站 → 往 Seoul Station 方向 → 第 11 站「홍대입구」下車</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 5. 步行到飯店
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">16:30</div>
      <div class="body">
        <h4>🚶 弘대입구站 9 號出口 → 9 Brick Hotel</h4>
        <p class="meta">走路 6 min｜450 m</p>
        <p class="note">9 號出口 (有手扶梯) → 直走 150m → 左轉 → 第一條小巷右轉 → 直走 2 min</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 6. 飯店 Check-in
    # ==============================
    show_stop("16:40", "hotel",
              override_note="Check-in 15:00 / Check-out 11:00",
              show_g=True, show_n=True, show_t=False,
              mode="walking",
              no_backup=True)

    # ==============================
    # 7. Olive Young 補貨
    # ==============================
    show_stop("17:30", "olive_young_hongdae",
              override_note="美妝藥妝旗艦店，三層樓。飯店走 5 min。第一天大買，最後一天可補貨。",
              show_g=True, show_n=True, show_t=False,
              mode="walking")

    # ==============================
    # 8. 弘대主街
    # ==============================
    show_stop("18:30", "hongdae_street",
              override_note="弘益路主街，街頭表演、潮店、咖啡。慢慢晃。",
              show_g=True, show_n=True, show_t=False,
              mode="walking")

    # ==============================
    # 9. 晚餐：肉夢
    # ==============================
    show_stop("19:30", "yukmong",
              override_note="三層樓燒烤 ⭐。Google 4.8 / 3000+ 評論。沒位置跳備案。",
              show_g=True, show_n=True, show_t=True,
              mode="walking")

    # ==============================
    # 10. AK Plaza
    # ==============================
    show_stop("21:30", "ak_plaza",
              override_note="弘대입구站直結，潮玩百貨。順路逛 ARTBOX (1F) 買伴手禮。",
              show_g=True, show_n=True, show_t=False,
              mode="walking")

    # ==============================
    # 11. 宵夜：BHC 炸雞
    # ==============================
    show_stop("22:30", "bhc",
              override_note="起司炸雞 (시그니처)、玫瑰辣炒年糕，配啤酒。飯店走 3 min。",
              show_g=True, show_n=True, show_t=False,
              mode="walking")

    # ==============================
    # 飯店附近
    # ==============================
    show_hotel_nearby(exclude_ids=[
        "yukmong", "bhc", "olive_young_hongdae", "ak_plaza", "hongdae_street"
    ])


if __name__ == "__main__":
    show()
