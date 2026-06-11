"""Day 4 (6/26 五) — 望遠 ➜ 延南 ➜ 弘대採買日"""
import streamlit as st
from utils import show_stop, show_hotel_nearby


def show():
    st.caption("📍 6/26 (五)｜望遠市場 + 延南洞咖啡 + 弘대戰利品採買")

    # ==============================
    # 1. 早餐
    # ==============================
    show_stop("09:30", "moment_coffee",
              override_note="自己烤吐司套餐 ₩14,000 (8 片+果醬/紅豆/水煮蛋)。"
              "或跳備案的 Egg Drop (08:30 開)。")

    # ==============================
    # 2. 望遠市場 (走路或地鐵 1 站)
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">10:30</div>
      <div class="body">
        <h4>🚶 弘대 → 望遠市場</h4>
        <p class="meta">走路 20 min / 6 호선 1 站 ₩1,500</p>
        <p class="note">走京義線林蔭道 (順路打卡)，到了再進市場。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    show_stop("11:00", "mangwon_market",
              override_note="9-21 點，平日不擠週末爆滿。8000+ 評論。")

    # ==============================
    # 3. 望遠市場必吃
    # ==============================
    show_stop("11:30", "uirak",
              override_note="炸辣椒配啤酒，韓國酒場文化代表，4.7/870+ 評論。")

    show_stop("12:30", "matjib",
              override_note="炸魷魚飯捲、辣炒年糕、魚板湯。⚠️ 週一公休 (週五 OK)")

    # ==============================
    # 4. 移動回延南洞
    # ==============================
    st.markdown("""
    <div class="stop-card">
      <div class="time">13:00</div>
      <div class="body">
        <h4>🚶 望遠 → 延南洞 (沿京義線林蔭道)</h4>
        <p class="meta">走路 15 min｜邊走邊逛小店</p>
        <p class="note">線狀公園，兩旁全是延南洞的獨立小店、咖啡廳。</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # 5. JO & DAWSON
    # ==============================
    show_stop("13:30", "jo_dawson",
              override_note="⭐優先。首爾最強法式吐司，茶葉自己烘，會送 mini tea bag。"
              "下午茶時段不擁擠，趕下午 5 點前去。")

    # ==============================
    # 6. 午餐補強 — 豬腳小姐
    # ==============================
    show_stop("15:00", "myth_jokbal",
              override_note="⭐優先。如果還沒飽就過來，飯店附近走路 5 min。中份吃兩個人剛好。")

    # ==============================
    # 7. 弘대採買戰
    # ==============================
    show_stop("16:30", "musinsa_hongdae",
              override_note="韓版 UNIQLO/GU，平價基本款，必逛。")

    show_stop("17:00", "covernat",
              override_note="韓國街頭潮牌，灰機 logo，限定款常缺貨。")

    show_stop("17:30", "wonderplace",
              override_note="thisisneverthat / Lee / Matin Kim 一次買齊。")

    show_stop("18:00", "abc_mart_gs",
              override_note="球鞋特別款 (Grand Stage 才有)。可比較 Shoopen。")

    # ==============================
    # 8. 晚餐：風川鰻魚
    # ==============================
    show_stop("19:00", "pungcheon",
              override_note="⭐優先。⚠️ 15:30-16:30 休息，19:00 OK。"
              "只有一道菜：炭烤鰻魚 + 包菜，員工教你怎麼吃。")

    # ==============================
    # 9. 宵夜
    # ==============================
    show_stop("21:30", "bhc",
              override_note="再吃一次 BHC，或跳備案的橋村/豚百壽湯飯。")

    # ==============================
    # 飯店附近
    # ==============================
    show_hotel_nearby(exclude_ids=[
        "musinsa_hongdae", "covernat", "wonderplace", "abc_mart_gs",
        "myth_jokbal", "bhc", "moment_coffee", "pungcheon", "jo_dawson"
    ])


if __name__ == "__main__":
    show()

