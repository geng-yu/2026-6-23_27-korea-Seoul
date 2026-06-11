"""Day 2 (6/24 三) — 聖水 ➜ 東大門 ➜ 弘대"""
import streamlit as st
from utils import show_stop, show_hotel_nearby


def show():
    st.caption("📍 6/24 (三)｜聖水洞 (韓國布魯克林) + 東大門 (一隻雞)")

    # ==============================
    # 1. 出發前往聖水洞
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">10:00</div>
      <div class="body">
        <h4>🚖 弘대 → 聖水洞</h4>
        <p class="meta">Taxi ~₩15,000 / 25 min (兩人較划算)</p>
        <p class="note">或地鐵 2 號線一鐵到底 (홍대입구→성수, ~30min, ₩1,500/人)。
        計程車省 15 min 搬東西也比較鬆。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 2. 聖水洞 — 早午餐
    # ==============================
    show_stop("10:30", "gamjatang",
              override_note="排骨湯 24h 開，避開正午排隊潮。骨肉分離，會香一整天衣服。")

    # ==============================
    # 3. 聖水洞 — TAMBURINS 香氛
    # ==============================
    show_stop("12:00", "tamburins_seongsu",
              override_note="Jennie 同款 PUMKINI 香水、貝殼護手霜。3層樓旗艦店。")

    # ==============================
    # 4. 聖水洞 — 文具/復古
    # ==============================
    show_stop("13:00", "point_of_view",
              override_note="高質感文具/生活雜貨，伴手禮聖地，三層樓像小型博物館。")

    # ==============================
    # 5. 聖水洞 — Maman Gelato
    # ==============================
    show_stop("14:30", "maman_gelato",
              override_note="必點 Pistachiotella 開心果義式冰淇淋 ₩9,000。Google 4.8/788。")

    # ==============================
    # 6. 聖水洞 — LCDC Seoul
    # ==============================
    show_stop("15:00", "lcdc",
              override_note="四層樓選物百貨，每層都有小品牌+咖啡廳，倫敦貝果博物館創辦人作品展。")

    # ==============================
    # 7. 移動到東大門
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">16:30</div>
      <div class="body">
        <h4>🚖 聖水洞 → 東大門</h4>
        <p class="meta">Taxi ~₩7,000 / 10 min</p>
        <p class="note">同江北，距離很近。地鐵 2 號線也 OK 但小走一段。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 8. DDP 設計廣場
    # ==============================
    show_stop("17:00", "ddp",
              override_note="Zaha Hadid 建築，外觀必拍。可以順便逛 Doota / Migliore。")

    # ==============================
    # 9. 晚餐：陳玉華一隻雞
    # ==============================
    show_stop("19:30", "jin_okhwa",
              override_note="老店⭐優先，8000+ 評論。等位約 20 min，吃完點清麵下到湯裡。")

    # ==============================
    # 10. 回弘대
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">21:00</div>
      <div class="body">
        <h4>🚖 東大門 → 弘대</h4>
        <p class="meta">Taxi ~₩10,000 / 20 min (晚上+戰利品推 Taxi)</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 11. 宵夜：橋村炸雞
    # ==============================
    show_stop("22:00", "kyochon",
              override_note="醬油蒜味 / 紅辣味，國民炸雞品牌。或跳到飯店附近其他選擇。")

    # ==============================
    # 飯店附近
    # ==============================
    show_hotel_nearby(exclude_ids=["kyochon"])


if __name__ == "__main__":
    show()
