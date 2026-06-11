"""Day 1 (6/23 二) — 抵達 ➜ 弘大"""
import streamlit as st
from utils import stop, hotel_bottom, custom_card, multi_card, gmap_url, naver_url, set_scheduled

# 當天主行程已排清單（「其他」expander 會把這些沉到最下面標「已排」）
TODAY_FOOD = ["yukmong", "bhc"]
TODAY_SHOP = ["olive_young_hongdae", "hongdae_street", "ak_plaza"]


def show_day():
    set_scheduled(TODAY_FOOD, TODAY_SHOP)
    st.caption("📍 6/23 (二)｜台中 → 仁川 T2 → 弘大 9 Brick Hotel")

    # ============ 第1格：自駕到 RMQ ============
    custom_card(
        tag="🚗",
        title="台中機場 RMQ",
        meta="開車｜停佳安停車場（清泉崗）",
        links=[
            {"label": "G", "url": gmap_url("佳安停車場 清泉崗", mode="driving"), "cls": "g"},
        ],
        dashed=False,
    )

    # ============ 第2格：飛機 + 入境 ============
    custom_card(
        tag="✈️",
        title="10:40 台中 → 14:15 仁川 T2 · 2h35m",
        note="Arrival / 도착 → 入境審查 (準備 K-ETA) → 1F 行李轉盤 → 海關 → 入境大廳",
        dashed=False,
    )

    # ============ 第3格：機場 → 弘大 → 飯店（合併同一格） ============
    multi_card(
        tag="🚆",
        sections=[
            {"title": "機場 → 弘大 → 飯店"},
            {
                "title": "AREX (T2 → 弘大 · 홍대입구)",
                "meta": "一般車 · B1 月台 · 藍色閘門 · ₩4,750/人 · 55 min",
                "note": "⚠️ 不要走橘色閘門 (Express 直達車不停弘대)。方向：往 Seoul Station，第 11 站「홍대입구」下車。",
                "links": [
                    {"label": "G", "url": gmap_url("홍대입구역 9번 출구", mode="transit"), "cls": "g"},
                    {"label": "N", "url": naver_url(query="홍대입구역 9번 출구"), "cls": "n"},
                ],
            },
            {
                "title": "9 號出口 → 9 Brick Hotel",
                "note": "9 號出口有手扶梯 → 直走 150m → 左轉 → 第一條巷子右轉 → 直走 2 min",
                "links": [
                    {"label": "G", "url": gmap_url("나인브릭 호텔 서울 마포구 홍익로5길 32", mode="walking"), "cls": "g"},
                    {"label": "N", "url": naver_url(lat=37.5537661, lng=126.9205306, name="9 Brick Hotel", mode="walking"), "cls": "n"},
                ],
            },
        ],
    )

    st.divider()

    # ============ 第4格：晚餐 ============
    stop(
        "晚",
        "yukmong",
        others="food",
        notes="",
        show_taxi=True,
        mode="walking",
    )

    # ============ 第5格：逛（合併同一格） ============
    multi_card(
        tag="🛒",
        sections=[
            {"place_id": "olive_young_hongdae"},
            {"place_id": "hongdae_street"},
        ],
        others="shop",
        show_taxi=True,
        mode="walking",
    )

    # ============ 第6格：宵夜 ============
    stop(
        "🍗",
        "bhc",
        show_taxi=True,
        mode="walking",
    )

    # ============ 第7格：住 + 飯店附近 ============
    hotel_bottom(today_food=TODAY_FOOD, today_shop=TODAY_SHOP)


def show():
    show_day()


if __name__ == "__main__":
    show()
