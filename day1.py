"""Day 1 (6/23 二) — 抵達 ➜ 弘大"""
import streamlit as st
from utils import stop, hotel_bottom


def show_day():
    st.caption("📍 6/23 (二)｜台中 → 仁川 T2 → 弘大 9 Brick Hotel")

    # ============ 第1格：自駕到 RMQ ============
    st.markdown("""
    <div class="note-card">
      <div class="tag">車</div>
      <div class="body">
        <div class="top-row">
          <h5 style="margin:0; font-size:14.5px; font-weight:700;">台中機場 RMQ</h5>
          <div class="nav-btns">
            <a class="nav-btn g" href="https://www.google.com/maps/dir/?api=1&destination=%E4%BD%B3%E5%AE%89%E5%81%9C%E8%BB%8A%E5%A0%B4%20%E6%B8%85%E6%B3%89%E5%B4%97&travelmode=driving" target="_blank" title="Google Maps">G</a>
          </div>
        </div>
        <p class="meta">開車｜停佳安停車場（清泉崗）</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ============ 第2格：飛機 + 入境 ============
    st.markdown("""
    <div class="note-card">
      <div class="tag">✈️</div>
      <div class="body">
        <div class="top-row">
          <h5 style="margin:0; font-size:14.5px; font-weight:700;">10:40 台中 → 14:15 仁川 T2 · 2h35m</h5>
        </div>
        <p class="note">Arrival / 도착 → 入境審查 (準備 K-ETA) → 1F 行李轉盤 → 海關 → 入境大廳</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ============ 第3格：機場 → 弘大 → 飯店 ============
    st.markdown("""
    <div class="note-card">
      <div class="tag">🚆</div>
      <div class="body">
        <div class="top-row">
          <h5 style="margin:0; font-size:14.5px; font-weight:700;">機場 → 弘大 → 飯店</h5>
        </div>

        <div class="top-row" style="margin-top:8px;">
          <h5 style="margin:0; font-size:14px; font-weight:800;">AREX (T2 → 弘大 · 홍대입구)</h5>
          <div class="nav-btns">
            <a class="nav-btn g" href="https://www.google.com/maps/dir/?api=1&destination=%ED%99%8D%EB%8C%80%EC%9E%85%EA%B5%AC%EC%97%AD%209%EB%B2%88%20%EC%B6%9C%EA%B5%AC&travelmode=transit" target="_blank" title="Google Maps">G</a>
            <a class="nav-btn n" href="nmap://route/public?dlat=37.5578422&dlng=126.9244145&dname=%ED%99%8D%EB%8C%80%EC%9E%85%EA%B5%AC%EC%97%AD%209%EB%B2%88%20%EC%B6%9C%EA%B5%AC&appname=seoul_trip_2026" title="NAVER">N</a>
          </div>
        </div>
        <p class="meta">一般車 · B1 月台 · 藍色閘門 · ₩4,750/人 · 55 min</p>
        <p class="note">⚠️ 不要走橘色閘門 (Express 直達車不停弘대)。方向：往 Seoul Station，第 11 站「홍대입구」下車。</p>

        <div class="top-row" style="margin-top:10px;">
          <h5 style="margin:0; font-size:14px; font-weight:800;">9 號出口 → 9 Brick Hotel</h5>
          <div class="nav-btns">
            <a class="nav-btn g" href="https://www.google.com/maps/dir/?api=1&destination=%EB%82%98%EC%9D%B8%EB%B8%8C%EB%A6%AD%20%ED%98%B8%ED%85%94%20%EC%84%9C%EC%9A%B8%20%EB%A7%88%ED%8F%AC%EA%B5%AC%20%ED%99%8D%EC%9D%B5%EB%A1%9C5%EA%B8%B8%2032&travelmode=walking" target="_blank" title="Google Maps">G</a>
            <a class="nav-btn n" href="nmap://route/walk?dlat=37.5537661&dlng=126.9205306&dname=9%20Brick%20Hotel&appname=seoul_trip_2026" title="NAVER">N</a>
          </div>
        </div>
        <p class="note">9 號出口有手扶梯 → 直走 150m → 左轉 → 第一條巷子右轉 → 直走 2 min</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ============ 第4格：晚餐 ============
    stop(
        "晚",
        "yukmong",
        others="food",
        notes="燒烤",
        show_taxi=True
    )

    # ============ 第5格：逛 ============
    stop(
        "逛",
        ["olive_young_hongdae", "hongdae_street", "ak_plaza"],
        others="shop",
        notes=[None, None, None],
        show_taxi=True
    )

    # ============ 第6格：宵夜 ============
    stop(
        "宵",
        "bhc",
        show_taxi=True
    )

    # ============ 第7格：住 + 飯店附近 ============
    hotel_bottom(
        today_food=["yukmong", "bhc"],
        today_shop=["olive_young_hongdae", "hongdae_street", "ak_plaza"],
    )


def show():
    show_day()


if __name__ == "__main__":
    show()
