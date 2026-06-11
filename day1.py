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
    # 1. 飛行 + 入境
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="step-num">1.</div>
      <div class="body">
        <div class="title-row">
          <h4>🛫 10:40 台中 → 🛬 14:15 仁川 </h4>
        </div>
        <p class="meta">真航空｜10:40 RMQ 起飛｜14:15 ICN T2 抵達</p>
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
    # 3. AREX → 弘대입구 → 飯店 Check-in
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="step-num">3.</div>
      <div class="body">
        <div class="title-row">
          <h4>🚆 AREX → 🚶 弘대입구 → 🏨 9 Brick Hotel Check-in</h4>
        </div>
        <p class="meta">B1 藍色閘門｜₩4,750｜55 min → 9 號出口走路 6 min</p>
        <p class="note">① B1 找「AREX」→ 藍色閘門進站 → 第 11 站「홍대입구」下車<br>
        ② 9 號出口 (有手扶梯) → 直走 150m → 左轉 → 小巷右轉 → 直走 2 min<br>
        ③ Check-in 15:00 / Check-out 11:00</p>
        <div class="nav-btns">
          <a class="nav-btn g" href="https://www.google.com/maps/dir/?api=1&destination=나인브릭+호텔+서울+마포구+홍익로5길+32&travelmode=walking" target="_blank" title="Google Maps">G</a>
          <a class="nav-btn n" href="nmap://route/walk?dlat=37.5537661&dlng=126.9205306&dname=9+Brick+Hotel&appname=seoul_trip_2026" title="NAVER Map">N</a>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
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
