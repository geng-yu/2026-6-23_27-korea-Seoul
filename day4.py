"""Day 4 (6/26 五) — 弘대 + 望遠市場 + 延南洞"""
import streamlit as st
from utils import stop, note, hotel_bottom, set_scheduled

# 當天主行程已排清單（其他 expander 會把這些沉到最下面標「已排」）
TODAY_FOOD = ["moment_coffee", "mangwon_market", "jo_dawson",
              "pungcheon", "bhc"]
TODAY_SHOP = ["yeon_throughvintage", "musinsa_terrace_hongdae"]


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/26 (五)｜弘대深度日｜Moment + 望遠 + 延南 + 弘대商店街")

    # 1) 早餐 Moment Coffee 二號
    stop("早", "moment_coffee", others="food",
         notes="⭐優先。從飯店走 6 min。10:00 開門前後人少。"
               "招牌「Yaki-Pan Set」自己烤吐司 ₩14,000，8 片吐司 + 紅豆 + 奶油 + 半熟蛋。"
               "草莓拿鐵也必點。"
               "10:00 之前沒開 → 跳 Egg Drop (07:00 開) 或 Knotted 延南 / Nognog 延南。")

    # 2) 弘대 → 望遠
    note("🚇", "弘대 → 望遠市場",
              "2 號線本線｜2 站｜~4 min｜₩1,500",
              "進站：弘大入口站 (홍대입구역) 9 號出口旁邊入口<br>"
              "→ 2 號線「往시청 方向」(外線循環)<br>"
              "→ 2 站到「望遠站 (망원역 / Mangwon)」<br>"
              "→ 出 2 號出口 → 走 4 min 到望遠市場入口"
              "｜💡 走路要 17 min，地鐵省力且涼")

    # 3) 望遠市場
    stop("景", "mangwon_market", others="food",
         notes="⭐優先。在地人傳統市場，比廣藏更生活。"
               "必吃：望遠可樂餅 (馬鈴薯沙拉 ₩1,000)、Yeon Mandu 蒸餃、"
               "傳說王餃子、Kyuseu 炸雞、雨耳樂炸辣椒 (招牌)。"
               "邊吃邊逛 1 小時。⚠️ 週六日某些店家會休 (Mangwon Croquette 週末休)。")

    # 4) 望遠 → 延南 (回弘大入口走過去)
    note("🚇", "望遠 → 延南洞",
              "2 號線本線｜1 站｜~3 min｜₩1,500",
              "進站：望遠站 (망원역) 2 號出口入口<br>"
              "→ 2 號線「往홍대입구 方向」(內線循環)<br>"
              "→ 1 站到「弘大入口站 (홍대입구역)」<br>"
              "→ 出 3 號出口 → 走 4 min 到延南洞 Yeontral Park"
              "｜💡 或直接走 22 min 沿延南路慢慢逛")

    # 5) 延南洞早午餐：JO & DAWSON
    stop("午", "jo_dawson", others="food",
         notes="⭐優先。法式吐司 + 焦糖 + 冰淇淋 ₩14,000，IG 神店。"
               "排隊建議 Catchtable 抽號碼 / 13:30 過後較鬆。"
               "排不到 → Tongin 豬排 / Cafe Le Nuage 法式甜點 (走 3 min) 都在「其他」")

    # 6) 延南洞 vintage 逛街
    stop("逛", "yeon_throughvintage", others="shop",
         notes="⭐優先。延南洞最大 vintage 店，Polo / Ralph Lauren 二手丹寧 ₩10,000 起。"
               "24h 開，店員會中文。"
               "順路逛 Some Store / 延南 Vintage Sky 都在「其他」。")

    # 7) 延南 → 弘대商店街 (走過去)
    note("🚶", "延南 → 弘대商店街",
              "走路｜~10 min｜免費",
              "Yeontral Park → 經過 ABC-MART → 弘大正門口商圈<br>"
              "沿 Donggyo-ro / Yanghwa-ro 走，整條路兩側都店。"
              "💡 可順路看 SPAO 弘대旗艦 / Stylenanda Pink Pool。")

    # 8) 風川鰻魚 (晚餐)
    stop("晚", "pungcheon", others="food",
         notes="⭐優先。風川鰻魚特色：先烤再淋醬，主推炭烤鰻魚 ₩30,000/兩人。"
               "從延南走 8 min。位置低調，店外無大招牌。"
               "預訂建議 18:30 前到，假日要等。")

    # 9) 弘대商店街逛街 (主行程)
    stop("逛", "musinsa_terrace_hongdae", others="shop",
         notes="⭐AK& 7F，100+ 韓本土小眾品牌一次搞定。"
               "弘대平日 19:30 後逛街最對，店都開、人不多。"
               "順路看 ABC-MART Grand Stage / MARK GONZALES / Wacky Willy / "
               "NERDY / LMC 都在「其他」。")

    # 10) 宵夜 BHC 炸雞
    stop("宵", "bhc",
         notes="從弘대商店街走 4 min。蜂蜜口味 ₩25,000，配啤酒。"
               "21:00 後等位較鬆。不想吃炸雞跳「飯店附近吃」換口味。")

    # 11) 住 + 飯店附近
    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
