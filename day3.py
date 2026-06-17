"""Day 3 (6/25 四) — 安國/北村 + 益善洞 + 明洞 + 新世界"""
import streamlit as st
from utils import stop, note, hotel_bottom, set_scheduled

TODAY_FOOD = ["cafe_onion_anguk", "muguok", "london_bagel",
              "myeongdong_kyoja", "bongsan"]
TODAY_SHOP = ["shinsegae_main"]


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/25 (四)｜安國/北村 + 益善洞 + 明洞 + 新世界｜⚠️ 景福宮週四開")

    # 1) 出發：弘대 → 安國
    note("🚇", "弘대 → 安國",
              "2 號線 → 3 號線｜~25 min｜₩1,500｜轉乘 1 次",
              "進站：弘大入口站 (홍대입구역) 9 號出口旁邊入口<br>"
              "→ 2 號線「往시청 方向」(外線循環)<br>"
              "→ 3 站到「乙支路 3 街站 (을지로3가역 / Euljiro 3-ga)」站內轉乘<br>"
              "→ 3 號線「往대화 方向」<br>"
              "→ 2 站到「安國站 (안국역 / Anguk)」<br>"
              "→ 出 6 號出口 → 走 3 min 到 Cafe Onion"
              "｜💡 Taxi ~₩9,000 / 20 min (省 5 min)")

    # 2) 早午餐
    stop("早", "cafe_onion_anguk",
         notes="韓屋風咖啡店元老，4500+ 評論。早上 9 點較不擠。"
               "招牌 Pandoro + 美式咖啡，內用要找位先點再點才有座。")

    # 3) 景點 group：光化門 + 景福宮
    stop("景", ["gwanghwamun", "gyeongbokgung"],
         notes=[
             "⭐優先。11:00 守門將交班儀式 (約 20 min) 必看。"
             "從 Cafe Onion 走 8 min 到。",
             "穿韓服免門票 ₩3,000。週四 OK 開放。場地大，至少留 1 小時。"
             "東門可借免費中文導覽機。",
         ])

    # 4) 午餐：무굴
    stop("午", "muguok", others="food",
         notes="⭐優先。⚠️ 限時 11:30-14:00 / 17:30-20:00，要早點到。"
               "Catchtable 線上排隊建議出門前先抽。"
               "排不到跳「其他」→ 通仁市場銅板便當體驗。")

    # 5) 北村
    stop("景", "bukchon",
         notes="⭐優先。居民區 (請放低音量)。10-17 對遊客開放。"
               "從무굴走 5 min。八景拍照走逛 1 小時。")

    # 6) 點心：倫敦貝果
    stop("點", "london_bagel", others="food",
         notes="⚠️ Catchtable 抽號碼牌，平日可能等 1-2 小時，建議北村前就先抽。"
               "排不到 → 走到 Hanok Langsom 益善韓屋庭院咖啡，或直接去益善洞。")

    # 7) 益善洞
    stop("景", "ikseondong",
         notes="北村走 8 min。「鬼怪」取景，韓屋變咖啡街，比北村更有生活感。"
               "小夏鹽田鹽可頌、Mil Toast、Solsot 釜飯都在「其他」清單。")

    # 8) 益善洞 → 明洞
    note("🚇", "益善洞 → 明洞",
              "3 號線 → 4 號線｜~15 min｜₩1,500｜轉乘 1 次",
              "進站：益善洞走 5 min 到「鍾路 3 街站 (종로3가역 / Jongno 3-ga)」<br>"
              "→ 3 號線「往오금 方向」<br>"
              "→ 1 站到「忠武路站 (충무로역 / Chungmuro)」站內轉乘<br>"
              "→ 4 號線「往오이도 方向」<br>"
              "→ 1 站到「明洞站 (명동역 / Myeong-dong)」<br>"
              "→ 出 6 號出口 → 走 3 min 到明洞主街"
              "｜💡 Taxi ~₩6,000 / 10 min (省 5 min)")

    # 9) 點心：明洞餃子
    stop("點", "myeongdong_kyoja", others="food",
         notes="米其林必比登，刀削麵+餃子，14500+ 評論。"
               "先吃一碗麵留肚子等鳳山精肉。⚠️ 主店滿就去 New Building MJ (走 1 min)。")

    # 10) 逛街：新世界百貨本店
    stop("逛", "shinsegae_main", others="shop",
         notes="⭐從明洞餃子走 5 min。3 棟相連 25 層。"
               "8-11F 免稅店要先在 app 預約。B1 美食街排隊去買巴黎可頌。"
               "退稅在 1F 服務中心統一處理。")

    # 11) 回弘대
    note("🚇", "明洞 → 弘대",
              "2 號線本線直達｜~22 min｜₩1,500",
              "進站：新世界百貨走 8 min 到「乙支路入口站 (을지로입구역 / Euljiro 1-ga)」<br>"
              "→ 2 號線「往홍대입구 方向」(外線循環)<br>"
              "→ 6 站到「弘大入口站 (홍대입구역)」<br>"
              "→ 出 9 號出口 → 走 5 min 回飯店"
              "｜💡 戰利品多推 Taxi ~₩10,000 / 20 min")

    # 12) 晚餐：鳳山精肉
    stop("晚", "bongsan", others="food",
         notes="⭐優先。5.0/2400+ 評論。員工幫烤肉。從飯店走 7 min。"
               "不想吃燒烤跳「其他」豬腳/鰻魚。")

    # 13) 住 + 飯店附近
    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
