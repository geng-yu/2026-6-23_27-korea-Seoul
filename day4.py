"""Day 4 (6/26 五) — 望遠 + 延南 + 弘대採買日"""
import streamlit as st
from utils import stop, note, hotel_bottom


def show_day():
    st.caption("📍 6/26 (五)｜望遠市場 + 延南洞咖啡 + 弘대戰利品採買")

    stop("早", "moment_coffee", others="food",
         notes="自己烤吐司套餐 ₩14,000。或跳「其他」吃 Egg Drop。")

    note("🚶", "弘대 → 望遠市場",
              "走路 20 min / 6 호선 1 站 ₩1,500",
              "走京義線林蔭道 (順路打卡)，到了再進市場")

    stop("景", "mangwon_market",
         notes="9-21 點，平日不擠週末爆滿。8000+ 評論。")

    # 望遠市場小吃 group
    stop("點", ["uirak", "matjib"], others="food",
         notes=[
             "炸辣椒配啤酒，韓國酒場文化，4.7/870+ 評論。",
             "炸魷魚飯捲、辣炒年糕、魚板湯。週一公休 (週五 OK)。",
         ])

    note("🚶", "望遠 → 延南洞",
              "走路 15 min · 沿京義線林蔭道",
              "兩旁全是延南獨立小店、咖啡廳")

    stop("點", "jo_dawson", others="food",
         notes="⭐優先。首爾最強法式吐司，茶葉自己烘。下午 5 點前去。")

    stop("午", "myth_jokbal", others="food",
         notes="⭐優先。如果還沒飽就過來，飯店附近走 5 min。中份 2 人剛好。")

    # 弘대購物 group
    stop("逛", ["musinsa_hongdae", "covernat", "wonderplace", "abc_mart_gs"],
         notes=[
             "韓版 UNIQLO/GU，平價基本款必逛。",
             "韓國街頭潮牌，灰機 logo，限定款常缺貨。",
             "thisisneverthat / Lee / Matin Kim 一次買齊。",
             "球鞋特別款 (Grand Stage 才有)。可比較 Shoopen。",
         ])

    stop("晚", "pungcheon", others="food",
         notes="⭐優先。⚠️ 15:30-16:30 休息，19:00 OK。"
               "只有一道菜：炭烤鰻魚 + 包菜，員工教吃法。")

    stop("宵", "bhc", others="food",
         notes="再吃一次 BHC，或跳「其他」橋村/豚百壽。")

    hotel_bottom(
        today_food=["moment_coffee", "uirak", "matjib", "jo_dawson", "myth_jokbal", "pungcheon", "bhc"],
        today_shop=["musinsa_hongdae", "covernat", "wonderplace", "abc_mart_gs"],
    )


def show():
    show_day()

if __name__ == "__main__":
    stop()
