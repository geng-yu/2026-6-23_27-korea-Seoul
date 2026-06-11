"""Day 2 (6/24 三) — 聖水洞 + 東大門"""
import streamlit as st
from utils import stop, note, hotel_bottom, set_scheduled

TODAY_FOOD = ["gamjatang", "maman_gelato", "jin_okhwa", "kyochon"]
TODAY_SHOP = ["tamburins_seongsu", "point_of_view", "lcdc"]


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/24 (三)｜聖水洞 (韓國布魯克林) + 東大門 (一隻雞)")

    # 出發
    note("🚖", "弘대 → 聖水洞",
              "Taxi ~₩15,000 / 25 min",
              "兩人較划算。或地鐵 2 號線一鐵到底 (홍대입구→성수, ~30min, ₩1,500/人)")

    # 早午餐
    stop("早", "gamjatang", others="food",
         notes="⭐優先。24h 不打烊，避開正午排隊潮。骨肉分離，會香一整天衣服。")

    # 聖水逛 group
    stop("逛", ["tamburins_seongsu", "point_of_view", "lcdc"],
         notes=[
             "Jennie 同款 PUMKINI 香水、貝殼護手霜。三層樓旗艦。",
             "高質感文具/生活雜貨選物，三層樓像小型博物館。",
             "四層樓選物百貨，每層都有小品牌 + 咖啡 + 倫敦貝果博物館創辦人作品展。",
         ])

    # 點心
    stop("點", "maman_gelato", others="food",
         notes="⭐優先。必點 Pistachiotella 開心果義式冰淇淋 ₩9,000。")

    # 移動
    note("🚖", "聖水洞 → 東大門",
              "Taxi ~₩7,000 / 10 min",
              "同江北，地鐵 2 號線 also OK 但小走一段")

    # 景點
    stop("景", "ddp",
         notes="Zaha Hadid 建築，外觀必拍。可順便逛 Doota/Migliore (備案有)。")

    # 晚餐
    stop("晚", "jin_okhwa", others="food",
         notes="⭐優先。老店 8000+ 評論。等位約 20 min，吃完點清麵下到湯裡。")

    # 回弘대
    note("🚖", "東大門 → 弘대",
              "Taxi ~₩10,000 / 20 min",
              "晚上 + 戰利品推 Taxi")

    # 宵夜
    stop("宵", "kyochon", others="food",
         notes="醬油蒜味 / 紅辣味，國民炸雞品牌。或跳「其他」換口味。")

    # 住 + 飯店附近
    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
