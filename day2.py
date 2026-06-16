"""Day 2 (6/24 三) — 聖水洞 (早午餐+逛+甜點) ➜ 東大門 (一隻雞) ➜ 弘대 (橋村)"""
import streamlit as st
from utils import stop, note, hotel_bottom, set_scheduled

# 當天主行程已排清單（其他 expander 會把這些沉到最下面標「已排」）
TODAY_FOOD = ["gamjatang", "maman_gelato", "jin_okhwa", "kyochon"]
TODAY_SHOP = ["tamburins_seongsu", "point_of_view", "lcdc", "blue_elephant_seongsu"]


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/24 (三)｜聖水洞 (韓國布魯克林) + 東大門 (一隻雞)")

    # 1) 出發
    note("🚖", "弘대 → 聖水洞",
              "Taxi ~₩15,000 / 25 min",
              "兩人較划算。或地鐵 2 號線一鐵到底 (홍대입구→성수, ~30min, ₩1,500/人)")

    # 2) 早午餐：三代馬鈴薯排骨湯
    stop("早", "gamjatang", others="food",
         notes="⭐優先。24h 不打烊，避開正午排隊潮，建議 10-11 點到。"
               "骨肉分離,會香一整天衣服,記得脫外套。")

    # 3) 聖水洞購物 (四家 group 一起)
    stop("逛", ["tamburins_seongsu", "point_of_view", "lcdc", "blue_elephant_seongsu"],
         others="shop",
         notes=[
             "Jennie 同款 PUMKINI 香水、貝殼護手霜。三層樓旗艦。",
             "高質感文具/生活雜貨選物，三層樓像小型博物館。",
             "四層樓選物百貨，每層都有小品牌 + 咖啡 + 倫敦貝果博物館創辦人作品展。",
             "⭐眼鏡均一價 ~₩49,000，全首爾最大間，平價版 Gentle Monster。",
         ])

    # 4) 點心：Maman Gelato
    stop("點", "maman_gelato", others="food",
         notes="⭐優先。必點 Pistachiotella 開心果義式冰淇淋 ₩9,000，碎開心果鋪滿。"
               "排隊約 20 min，店內小，建議外帶到聖水公園吃。")

    # 5) 移動：聖水洞 → 東大門
    note("🚖", "聖水洞 → 東大門",
              "Taxi ~₩7,000 / 10 min",
              "同江北，地鐵 2 號線 also OK 但站到東大門要走 5 min")

    # 6) 晚餐：陳玉華一隻雞
    stop("晚", "jin_okhwa", others="food",
         notes="⭐優先。老店 8000+ 評論。等位約 20 min。"
               "Tip：先丟馬鈴薯+蒜+蔥下湯，吃完雞肉再加手打麵收尾。")

    # 7) 回弘대
    note("🚖", "東大門 → 弘대",
              "Taxi ~₩10,000 / 20 min",
              "晚上 + 戰利品推 Taxi")

    # 8) 宵夜：橋村炸雞（飯店附近）
    stop("宵", "kyochon",
         notes="從飯店走 3 min。醬油蒜味 / 紅辣味雙拼，配啤酒。"
               "不想吃炸雞跳「飯店附近吃」換口味。")

    # 9) 住 + 飯店附近吃/逛
    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
