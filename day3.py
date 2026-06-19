"""Day 3 (6/25 四) — 安國/北村/西村 + 益善洞 + 明洞 + 新世界"""
import streamlit as st
from utils import stop, note, hotel_bottom, set_scheduled

TODAY_FOOD = ["muguok", "rafre_fruit_seochon", "london_bagel",
              "myeongdong_kyoja", "bongsan"]
TODAY_SHOP = ["shinsegae_main"]


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/25 (四)｜安國/北村/西村 + 益善洞 + 明洞 + 新世界")

    # 1) 出發：弘대 → 安國
    note("🚇", "弘대 → 安國",
              "2 號線 → 3 號線｜~25 min｜₩1,500｜轉乘 1 次",
              "進站：弘大入口站 (홍대입구역) 9 號出口旁邊入口<br>"
              "→ 2 號線「往시청 方向」(外線循環)<br>"
              "→ 3 站到「乙支路 3 街站 (을지로3가역 / Euljiro 3-ga)」站內轉乘<br>"
              "→ 3 號線「往대화 方向」<br>"
              "→ 2 站到「安國站 (안국역 / Anguk)」<br>"
              "→ 出 1 號出口"
              "｜💡 Taxi ~₩9,000 / 20 min")

    # 1) 早午餐：無垢屋
    stop("", "muguok", others="food",
         notes="⚠️Catchtable 出門前先抽號碼<br>"
               "排不到備案：Cafe Onion Anguk、土俗村蔘雞湯<br>"
               "通仁市場銅板便當 (走 7 min)")

    # 2-3) 光化門 + 景福宮 (走路)
    stop("", ["gwanghwamun", "gyeongbokgung"],
         notes=[
             "11:00 守門將交班儀式<br>",
             "東門可借免費中文導覽機",
         ])

    # 4) Rafre Fruit 西村 (走路)
    stop("🍰", "rafre_fruit_seochon", others="food",
         notes="從景福宮往西走 11 min (穿越通仁市場順路看)<br>"
               "草莓蛋糕 / 濟州芒果刨冰 / 草莓拿鐵<br>"
               "建議在景福宮用 Catchtable 抽號碼")

    # 5) Rafre → 北村 (有點繞，建議計程車)
    note("🚖", "Rafre 西村 → 北村",
              "Taxi ~₩4,000 / 5 min｜或走 19 min",
              "Rafre 在景福宮西邊、北村在景福宮東北邊<br>"
              "中間隔著景福宮整個範圍 (1.5 km)<br>")

    stop("", "bukchon",
         notes="10-17 開放，八景拍照走逛")

    # 6) 倫敦貝果 (走路)
    stop("🥯", "london_bagel", others="food",
         notes="⚠️ Catchtable 抽號碼牌，平日可能等 1-2 小時<br>"
               "建議北村時先抽<br>排不到 → Hanok Langsom 益善(韓屋庭院)")

    # 7) 益善洞 (走路)
    stop(" ", "ikseondong",
         notes="從倫敦貝果走 9 min。「鬼怪」取景<br>"
               "小夏鹽田鹽可頌、Mil Toast、Solsot 釜飯")

    # 8) 益善洞 → 明洞 (地鐵)
    note("🚇", "益善洞 → 明洞",
              "3 號線 → 4 號線｜~15 min｜₩1,500｜轉乘 1 次",
              "進站：益善洞走 5 min 到「鍾路 3 街站 (종로3가역 / Jongno 3-ga)」<br>"
              "→ 3 號線「往오금 方向」<br>"
              "→ 1 站到「忠武路站 (충무로역 / Chungmuro)」站內轉乘<br>"
              "→ 4 號線「往오이도 方向」<br>"
              "→ 1 站到「明洞站 (명동역 / Myeong-dong)」<br>"
              "→ 出 6 號出口 → 走 3 min 到明洞主街<br>"
              "💡 Taxi ~₩6,000 / 10 min (省 5 min)")

    # 9) 明洞餃子
    stop("🥟", "myeongdong_kyoja", others="food",
         notes="米其林必比登，刀削麵+餃子<br>"
               "先吃一碗麵留肚子等鳳山精肉<br>"
               "⚠️ 主店滿就去 New Building MJ")

    # 10) 逛街：明洞商圈順路逛到新世界
    stop("", "shinsegae_main", others="shop",
         notes="新世界 8-11F 免稅店要先 app 預約<br>退稅 1F 統一處理")

    # 11) 回弘대
    note("🚇", "明洞 → 弘대",
              "2 號線本線直達｜~22 min｜₩1,500",
              "進站：新世界走到「乙支路入口站(을지로입구역/Euljiro 1-ga)<br>"
              "→ 2 號線「往홍대입구 方向」(外線循環)<br>"
              "→ 6 站到「弘大入口站 (홍대입구역)」<br>"
              "→ 出 9 號出口 💡Taxi ~₩12,000 / 25 min")

    # 12) 晚餐：鳳山精肉
    stop("", "bongsan", others="food",
         notes="燒烤")

    # 13) 住 + 飯店附近
    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
