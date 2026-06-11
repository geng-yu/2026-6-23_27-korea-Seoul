"""Day 5 (6/27 六) — 早餐 ➜ 回程 (AREX)"""
import streamlit as st
from utils import show_stop, show_hotel_nearby


def show():
    st.caption("📍 6/27 (六)｜弘대 → 仁川 T2｜LJ737 14:50 起飛")

    # ==============================
    # 1. 退房
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">09:00</div>
      <div class="body">
        <h4>🧳 退房 (Check-out)</h4>
        <p class="meta">9 Brick Hotel｜行李寄飯店 lobby</p>
        <p class="note">11:00 前退房。寄完行李去吃早餐，回來拿。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 2. 早餐：百年蔘雞湯
    # ==============================
    show_stop("09:30", "baeknyeon",
              override_note="⭐優先。2017 米其林推介，09:00 開門。走路 4 min。"
              "如果想清淡 → 跳備案的 Egg Drop 或 Moment Coffee。")

    # ==============================
    # 3. T-money 餘額用掉
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">10:30</div>
      <div class="body">
        <h4>💳 T-money 餘額處理</h4>
        <p class="meta">趕在登機前讓餘額 ≤ ₩20,000</p>
        <p class="note">便利店買水/零食用嗶卡用掉。&gt;₩20,000 要去 T-money 總公司退太麻煩。
        &le;₩20,000 在 CU/GS25/7-Eleven/emart24 都可退現金 (扣 ₩500 手續費)。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 4. 弘대最後採買 + Olive Young 補貨
    # ==============================
    show_stop("11:00", "olive_young_hongdae",
              override_note="最後補貨機會。3 樓有藥品/保健品，記得拿退稅單。")

    # ==============================
    # 5. 飯店拿行李
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">11:30</div>
      <div class="body">
        <h4>🧳 飯店拿行李 → 出發機場</h4>
        <p class="meta">弘대입구站 9 號出口走 6 min</p>
        <p class="note">走到站內，直接 AREX (不走 2 號線方向)。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 6. AREX 一般車回 T2
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">12:00</div>
      <div class="body">
        <h4>🚆 AREX 一般車 (弘대입구 → 인천공항 T2)</h4>
        <p class="meta">B1 月台｜<b>藍色閘門</b>｜₩4,750/人｜55 min</p>
        <p class="note">方向：往「인천공항 T2 (Incheon Airport T2)」終點站。
        弘대入口是<b>始發站之一</b>(部分班次)，有機會搶到座位。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 7. 抵達 T2 → 報到
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">12:55</div>
      <div class="body">
        <h4>🛬 仁川 T2 → LJ737 報到</h4>
        <p class="meta">3F 出境大廳｜真航空櫃台 (現場顯示)｜起飛前 2 小時開放</p>
        <p class="note">12:50 開始報到。退稅機要在報到前處理 (找 KIOSK 或 Global Blue 櫃台)。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 8. 過海關 / 候機
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">14:00</div>
      <div class="body">
        <h4>🍔 過海關 → SHAKE SHACK 候機</h4>
        <p class="meta">T2 出境後 28 號登機門附近</p>
        <p class="note">時間夠的話吃 SHAKE SHACK，或逛免稅店 (新羅、樂天)。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 9. 起飛
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">14:50</div>
      <div class="body">
        <h4>🛫 Jin Air LJ737</h4>
        <p class="meta">真航空｜經濟艙｜2h40m</p>
        <p class="note">ICN T2 → RMQ 抵達 16:30。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 飯店附近 (萬一早起時間多)
    # ==============================
    show_hotel_nearby(exclude_ids=["baeknyeon", "olive_young_hongdae"])


if __name__ == "__main__":
    show()

