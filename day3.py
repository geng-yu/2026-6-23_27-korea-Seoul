"""Day 3 (6/25 四) — 安國/北村 ➜ 益善洞 ➜ 明洞 ➜ 弘대"""
import streamlit as st
from utils import show_stop, show_hotel_nearby


def show():
    st.caption("📍 6/25 (四)｜安國/北村 + 益善洞 + 明洞｜⚠️ 景福宮週四開")

    # ==============================
    # 1. 出發 → 安國
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">09:30</div>
      <div class="body">
        <h4>🚖 弘대 → 安國</h4>
        <p class="meta">Taxi ~₩9,000 / 20 min</p>
        <p class="note">省 15min vs 地鐵 (要轉車)。地鐵也行 (홍대입구 → 2 호선 → 시청 → 3 호선 → 안국)。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 2. Cafe Onion Anguk 早餐
    # ==============================
    show_stop("10:00", "cafe_onion_anguk",
              override_note="韓屋風咖啡店元老，4500+ 評論。早上 9 點較不擠，避開週末。")

    # ==============================
    # 3. 光化門 + 景福宮
    # ==============================
    show_stop("11:00", "gwanghwamun",
              override_note="11:00 守門將交班儀式 (約 20 min)，比景福宮門口更壯觀。")

    show_stop("11:30", "gyeongbokgung",
              override_note="穿韓服免門票 ₩3,000。週四 OK。場地大，至少留 1 小時。")

    # ==============================
    # 4. 無垢屋 蔘雞湯
    # ==============================
    show_stop("13:00", "muguok",
              override_note="⚠️ 限時開放 11:30-14:00 / 17:30-20:00，要早點到。Catchtable 線上排隊。"
              "如果排不到 → 跳備案中的「Solsot 釜飯 (益善洞)」或「百年蔘雞湯 (弘대)」")

    # ==============================
    # 5. 北村韓屋村
    # ==============================
    show_stop("14:30", "bukchon",
              override_note="居民區，請放低音量。10-17 點對遊客開放。北村 8 景拍照景點。")

    # ==============================
    # 6. 倫敦貝果 (排不到就跳)
    # ==============================
    show_stop("15:30", "london_bagel",
              override_note="⚠️ Catchtable 抽號碼牌，平日下午可能等 1-2 小時。"
              "排不到就直接走到附近的「Cafe Onion Anguk」(那邊比較容易吃到)，或直接去益善洞。")

    # ==============================
    # 7. 益善洞 (使用者新加)
    # ==============================
    show_stop("16:00", "ikseondong",
              override_note="北村走過去 8 min / Taxi 4 min。「鬼怪」取景地，韓屋變咖啡街，比北村更有生活感。"
              "推薦小夏鹽田鹽可頌、Mil Toast、Solsot 釜飯 (見備案)。")

    # ==============================
    # 8. 移動到明洞
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">17:30</div>
      <div class="body">
        <h4>🚖 益善洞 → 明洞</h4>
        <p class="meta">Taxi ~₩6,000 / 10 min</p>
        <p class="note">或地鐵 3 號線 안국 → 4 號線 명동 (1 transfer, 15 min)</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 9. 明洞餃子 (米其林) — 點心或晚餐
    # ==============================
    show_stop("18:00", "myeongdong_kyoja",
              override_note="米其林必比登，刀削麵+餃子，14500+ 評論。"
              "如果想留肚子等鳳山精肉，這邊就只吃一碗麵。")

    # ==============================
    # 10. 回弘대
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">19:30</div>
      <div class="body">
        <h4>🚖 明洞 → 弘대</h4>
        <p class="meta">Taxi ~₩10,000 / 20 min</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 11. 晚餐：鳳山精肉
    # ==============================
    show_stop("20:00", "bongsan",
              override_note="⭐優先，5.0/2400+ 評論。員工幫烤肉，可訂位。"
              "如果不想吃燒烤 → 跳備案的「豬腳小姐」或「一片鰻魚」。")

    # ==============================
    # 飯店附近
    # ==============================
    show_hotel_nearby(exclude_ids=["bongsan"])


if __name__ == "__main__":
    show()

