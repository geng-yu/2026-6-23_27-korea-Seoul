"""Day 4 (6/26 五) — 弘대 + 望遠市場 + 延南洞"""
import streamlit as st
from utils import stop, note, hotel_bottom, set_scheduled

# 當天主行程已排清單（其他 expander 會把這些沉到最下面標「已排」）
TODAY_FOOD = ["bagel_land", "moment_coffee", "mangwon_market", "jo_dawson",
              "pungcheon", "bhc"]
TODAY_SHOP = ["yeon_throughvintage", "musinsa_terrace_hongdae"]


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/26 (五)｜望遠 + 延南")

    # 1) 早餐 Bagel Land (8:30 開) — 從飯店走 4 min
    stop("", "bagel_land", others="food",
         notes="從飯店走 4 min<br>"
               "8:30 開，早餐選擇之一<br>"
               "招牌：地瓜貝果 / 艾草貝果 / 羅勒貝果<br>"
               "💡 建議外帶 1-2 個貝果，到 Moment Coffee 配咖啡一起吃")

    # 2) 早餐 Moment Coffee 二號 — 從 Bagel Land 走 4 min
    stop("", "moment_coffee", others="food",
         notes="從 Bagel Land 走 4 min<br>"
               "10:00 開門前後人少<br>"
               "招牌 Yaki-Pan Set ₩14,000<br>"
               "8 片吐司 + 紅豆 + 奶油 + 半熟蛋<br>"
               "草莓拿鐵必點<br>"
               "💡 怕吃太飽 → 只點咖啡，貝果在 Bagel Land 已經吃過")

    # 3) 弘대 → 望遠
    note("🚇", "弘대 → 望遠市場",
              "2 號線本線｜2 站｜~4 min｜₩1,500",
              "進站：弘大入口站 (홍대입구역) 9 號出口旁邊入口<br>"
              "→ 2 號線「往시청 方向」(外線循環)<br>"
              "→ 2 站到「望遠站 (망원역 / Mangwon)」<br>"
              "→ 出 2 號出口 → 走 4 min 到望遠市場入口<br>"
              "｜💡 走路要 17 min，地鐵省力且涼")

    # 4) 望遠市場
    stop("", "mangwon_market", others="food",
         notes="必吃：望遠可樂餅 (馬鈴薯沙拉 ₩1,000)、Yeon Mandu 蒸餃<br>"
               "傳說王餃子、Kyuseu 炸雞、雨耳樂炸辣椒 (招牌)")

    # 5) 望遠 → 延南 (回弘大入口走過去)
    note("🚇", "望遠 → 延南洞",
              "2 號線本線｜1 站｜~3 min｜₩1,500",
              "進站：望遠站 (망원역) 2 號出口入口<br>"
              "→ 2 號線「往홍대입구 方向」(內線循環)<br>"
              "→ 1 站到「弘大入口站 (홍대입구역)」<br>"
              "→ 出 3 號出口 → 走 4 min 到延南洞 Yeontral Park<br>"
              "｜💡 或直接走 22 min 沿延南路慢慢逛")

    # 6) 延南洞早午餐：JO & DAWSON
    stop("", "jo_dawson", others="food",
         notes="法式吐司 + 焦糖 + 冰淇淋<br>"
               "建議 Catchtable 抽號碼(13:30 過後較鬆)<br>"
               "備案 Tongin 豬排/Cafe Le Nuage 法式甜點")

    # 7) 延南洞 vintage 逛街
    stop("", "yeon_throughvintage", others="shop",
         notes="Polo / Ralph Lauren 二手丹寧<br>"
               "順路逛 Some Store/延南 Vintage Sky")

    # 8) 延南 → 弘대商店街 (走過去)
    note("🚶", "延南 → 弘대商店街",
              "走路｜~10 min",
              "Yeontral Park → 經過 ABC-MART → 弘大正門口商圈<br>"
              "沿 Donggyo-ro / Yanghwa-ro 走<br>"
              "💡 順路看 SPAO 弘대旗艦 / Stylenanda Pink Pool")

    # 9) 風川鰻魚 (晚餐)
    stop("", "pungcheon", others="food",
         notes="主推炭烤鰻魚 ₩30,000/兩人<br>"
               "預訂建議 18:30 前到")

    # 10) 弘대商店街逛街 (主行程) — 注意：在 AK& 17F 不是 7F
    stop("", "musinsa_terrace_hongdae", others="shop",
         notes="AK& 17F (整層) 韓本土小眾品牌<br>"
               "平日 19:30 後逛街人不多<br>"
               "順路看 ABC-MART Grand Stage/<br>Wacky Willy / "
               "NERDY / LMC 都在「其他」")

    # 11) 宵夜 BHC 炸雞
    stop("", "bhc",
         notes=" ")

    # 12) 住 + 飯店附近
    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
