"""Day 2 (6/24 三) — 聖水洞 (早午餐+逛+甜點) ➜ 東大門 (一隻雞) ➜ 弘대 (橋村)"""
import streamlit as st
from utils import stop, note, hotel_bottom, set_scheduled

# 當天主行程已排清單（其他 expander 會把這些沉到最下面標「已排」）
TODAY_FOOD = ["gamjatang", "maman_gelato", "jin_okhwa", "kyochon"]
TODAY_SHOP = ["blue_elephant_seongsu", "musinsa_standard_seongsu",
              "kasina_seongsu", "covernat_seongsu"]


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/24 (三)｜聖水洞 (韓國布魯克林) + 東大門 (一隻雞)")

    # 1) 出發
    note("🚇", "弘대 → 聖水洞",
              "2 號線本線直達｜13 站｜~28 min｜₩1,500",
              "9 號出口旁邊入口 "
              " → 2 號線「往강변/잠실」(內線循環/Inner)\n\n"
              " → 13 站到「聖水站 (성수역 / Seongsu)」\n"
              " → 出 3 號出口 → 直走到三代馬鈴薯排骨")

    # 2) 早午餐：三代馬鈴薯排骨湯
    stop("", "gamjatang", others="food",
         notes="優先。24h 不打烊，避開正午排隊潮，建議 10-11 點到")

    # 3) 聖水洞購物 (墨鏡 + 衣服 + 鞋子 + 潮牌)
    stop("", ["blue_elephant_seongsu", "musinsa_standard_seongsu",
                "kasina_seongsu", "covernat_seongsu"],
         others="shop",
         notes=[
             "墨鏡全首爾最大間",
             "韓版 UNIQLO/GU，極簡乾淨風。",
             "球鞋選物，Nike/Adidas/Salomon 少見配色。2F 還有 ASSC 等街頭品牌。",
             " ",
         ])

    # 4) 點心：Maman Gelato
    stop("", "maman_gelato", others="food",
         notes="必點 Pistachiotella 開心果義式冰淇淋 ₩9,000，碎開心果鋪滿。"
               "排隊約 20 min，店內小，建議外帶到聖水公園吃。")

    # 5) 移動：聖水洞 → 東大門
    note("🚇", "聖水洞 → 東大門",
              "2 號線本線｜4 站｜~10 min｜₩1,500",
              "3 號出口旁邊入口 "
              "→ 2 號線「往시청/홍대입구 方向」(外線循環 / Outer)"
              "→ 4 站到「東大門歷史文化公園站 (동대문역사문화공원역 / DDP)」"
              "→ 出 14 號出口 (14번 출구) → 過清溪川到陳玉華一隻雞")

    # 6) 晚餐：陳玉華一隻雞
    stop("", "jin_okhwa", others="food",
         notes="Tip：先丟馬鈴薯+蒜+蔥下湯，吃完雞肉再加手打麵收尾。")

    # 7) 回弘대
    note("🚇", "東大門 → 弘대",
              "2 號線本線直達｜10 站｜~22 min｜₩1,500",
              "「東大門歷史文化公園站 (동대문역사문화공원역 / DDP)」"
              "→ 14 號出口旁邊入口 → 2 號線「往시청/홍대입구 方向」(外線循環 / Outer)"
              "→ 10 站到「弘大入口站 (홍대입구역 / Hongik Univ.)」"
              "→ 出 9 號出口 (9번 출구) → 走 5 min 回飯店"
              "｜⚠️ 戰利品多可考慮 Taxi (~₩10,000 / 20 min)")

    # 8) 宵夜：橋村炸雞（飯店附近）
    stop("宵", "kyochon",
         notes="醬油蒜味 / 紅辣味雙拼")

    # 9) 住 + 飯店附近吃/逛
    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
