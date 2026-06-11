"""Day 3 (6/25 四) — 安國/北村 + 益善洞 + 明洞"""
import streamlit as st
from utils import stop, note, hotel_bottom, set_scheduled

TODAY_FOOD = ["cafe_onion_anguk", "muguok", "london_bagel", "myeongdong_kyoja", "bongsan"]
TODAY_SHOP = []


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/25 (四)｜安國/北村 + 益善洞 + 明洞｜⚠️ 景福宮週四開")

    note("🚖", "弘대 → 安國",
              "Taxi ~₩9,000 / 20 min",
              "省 15min vs 地鐵 (要轉車 2 號線→3 號線)")

    stop("早", "cafe_onion_anguk",
         notes="韓屋風咖啡店元老，4500+ 評論。早上 9 點較不擠。")

    stop("景", ["gwanghwamun", "gyeongbokgung"],
         notes=[
             "⭐優先。11:00 守門將交班儀式 (約 20 min) 必看。",
             "穿韓服免門票 ₩3,000。週四 OK。場地大，至少留 1 小時。",
         ])

    stop("午", "muguok", others="food",
         notes="⭐優先。⚠️ 限時 11:30-14:00 / 17:30-20:00，要早點到。"
               "Catchtable 線上排隊。排不到跳「其他」或回弘대吃「百年蔘雞湯」")

    stop("景", "bukchon",
         notes="⭐優先。居民區 (請放低音量)。10-17 對遊客開放。")

    stop("點", "london_bagel", others="food",
         notes="⚠️ Catchtable 抽號碼牌，平日可能等 1-2 小時。"
               "排不到 → 走到附近 Cafe Onion 或直接去益善洞。")

    stop("景", "ikseondong",
         notes="北村走 8 min / Taxi 4 min。「鬼怪」取景，韓屋變咖啡街，比北村更有生活感。"
               "小夏鹽田鹽可頌、Mil Toast、Solsot 釜飯都在「其他」清單。")

    note("🚖", "益善洞 → 明洞",
              "Taxi ~₩6,000 / 10 min",
              "或地鐵 3 號線 안국→4 號線 명동 (1 transfer, 15 min)")

    stop("點", "myeongdong_kyoja", others="food",
         notes="米其林必比登，刀削麵+餃子，14500+ 評論。先吃一碗麵留肚子等鳳山精肉。")

    note("🚖", "明洞 → 弘대",
              "Taxi ~₩10,000 / 20 min")

    stop("晚", "bongsan", others="food",
         notes="⭐優先。5.0/2400+ 評論。員工幫烤肉。不想吃燒烤跳「其他」豬腳/鰻魚。")

    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
