import streamlit as st
import pandas as pd
from utils import get_gmap_link, get_naver_link, show_nav_buttons

# 9 Brick Hotel 座標 (NAVER 路線規劃用)
HOTEL_LAT = 37.5537661
HOTEL_LNG = 126.9205306
HOTEL_NAME = "9 Brick Hotel"
HOTEL_ADDR_KR = "서울 마포구 홍익로5길 32"  # 韓文地址
HOTEL_ADDR_EN = "32 Hongik-ro 5-gil, Mapo-gu, Seoul"


def show():
    st.caption("6/23 (二)")

    # ==========================================
    # 0. 出發 → 台中機場
    # ==========================================
    st.subheader("0️⃣ 自行開車 ➔ 台中機場 (RMQ)")
    st.markdown("""
    * 建議起飛 **2 小時前** 抵達機場 → **8:40 前** 到
    * 機場停車：第二航廈停車場 (室內) 或 周邊配合的私人停車場
    """)
    st.link_button("🅿️ 導航：台中國際機場", get_gmap_link("台中國際機場", "driving"))

    # ==========================================
    # 1. 航班資訊
    # ==========================================
    with st.container(border=True):
        st.markdown("### 🛫 真航空 LJ736 (去程)")
        st.markdown("""
        * **10:40** 台中 RMQ ➔ **14:15** 仁川 **T2**
        * Boeing 737 MAX 8 / 經濟艙 / 2h35m
        * ⚠️ **抵達航廈是 T2 (不是 T1)**，AREX 跟巴士的搭乘指引都不同
        """)

    st.divider()

    # ==========================================
    # 2. 抵達 T2 的標準動線
    # ==========================================
    st.subheader("1️⃣ 仁川 T2 入境流程")
    st.markdown("""
    1. 下機後跟著 **「Arrival / 도착」** 指標走
    2. **入境審查 (Immigration)**：外國人櫃台，準備護照 + 已填好的 **K-ETA / Q-Code** 或紙本入境卡
    3. **行李轉盤 (Baggage Claim)**：在 1F
    4. **海關 (Customs)**：沒申報就走綠色通道
    5. 出來就是 **1F 入境大廳**
    """)

    st.info("💡 出關後請先別急著找車，看下面 **2️⃣ T-money** 再走")

    st.divider()

    # ==========================================
    # 3. T-money 處理 (iPhone)
    # ==========================================
    st.subheader("2️⃣ 設定 T-money 交通卡")

    with st.container(border=True):
        st.markdown("### 📱 方案 A：iPhone Apple Wallet (推薦，最快)")
        st.markdown("""
        **加入卡片 (台灣就可以先做好，免註冊)：**
        1. 打開 **Apple 錢包 App**
        2. 點右上角 **「＋」**
        3. 選 **「交通卡」** → **「T-money」** → 加入 (餘額 ₩0)
        4. **設定 → 錢包與 Apple Pay → 快速交通卡 → 選 T-money** ✅ 開啟快速模式

        **需求：** iOS 17.2 以上，iPhone XS / XR 以上
        """)

        st.success("✨ **快速模式神在哪：** 不用 Face ID、不用解鎖、**手機沒電還能再用 5 小時** (XS 之後的機型)")

        st.markdown("---")
        st.markdown("### 💳 加值 (Top-up) — 這邊有坑")
        st.warning("""
        ⚠️ **2026/6 最新狀況：**

        - **Visa 卡 ❌ 不能直接在 App 內加值** (payment gateway 限制)
        - **Mastercard / Amex / 銀聯 ✅** 可以用 **Mobile T-money App** 內建的 **Apple Pay 加值** (3 月更新後支援，要點 "Foreigner" 按鈕)
        - **現金加值 ✅** 永遠可用，到便利店 (CU / GS25 / 7-Eleven / emart24) 或地鐵站機台
        """)

        st.markdown("""
        **➡️ 建議流程：**
        1. **台灣時** 先把卡加進 Apple Wallet (餘額 ₩0)
        2. **落地後** 在 T2 入境大廳找 **CU / GS25** 換點現金 (₩50,000-100,000 夠了)
        3. 在 CU 跟店員說 **"티머니 충전 (Tmoney chong-jeon) ₩30,000"** → 把手機背面靠近讀卡機
        4. 之後地鐵 / 公車 / 便利店都嗶 iPhone

        ⚠️ **如果是 Mastercard**：可以下載 **Mobile T-money App** 試試直接信用卡加值，省去找現金
        """)

    with st.container(border=True):
        st.markdown("### 💳 方案 B：實體 T-money 卡 (備案)")
        st.markdown("""
        - 在 **T2 1F 入境大廳** 任何便利店買，₩2,500-3,000
        - 加值方式跟 Apple Wallet 一樣
        - 適合：手機機型太舊、不想搞 App 的人
        """)

    st.divider()

    # ==========================================
    # 4. 機場 → 飯店：方案 A (AREX 一般列車)
    # ==========================================
    st.subheader("3️⃣ 交通方案 A：AREX 一般列車 (推薦)")

    st.markdown("""
    **為什麼推這個：**
    - **直達** 弘大入口站，**不用轉車**
    - 便宜 ₩4,750
    - 不受塞車影響
    - 行李架空間夠用

    **不要搭直達列車 (Express, 橘色閘門)：**
    - 直達車只到首爾車站，**不停弘大入口**，反而要再轉地鐵 2 號線
    """)

    st.markdown("**Step 1：從 T2 入境大廳走到 AREX 月台 (B1)**")
    st.markdown("""
    1. 沿著 **「Train / 기차」** 或 **「AREX」** 指標走
    2. 搭手扶梯下到 **B1 交通中心 (Transportation Center)**
    3. **重要：找藍色 (BLUE) 閘門 → AREX 一般列車**
    4. ⚠️ **橘色 (ORANGE) 閘門是直達車 → 不要走錯**
    5. 進站方式：用剛剛加值好的 T-money 嗶閘門
    """)

    show_nav_buttons(
        "Incheon International Airport Terminal 2 Station",
        mode="walking",
        label_prefix="🚶 ",
    )

    st.markdown("**Step 2：搭車 (T2 → 弘大入口)**")
    st.markdown("""
    * **方向**：往 Seoul Station (首爾站)
    * **下車站**：**홍대입구 (Hongik University / 弘大入口)**，T2 出發第 11 站
    * **耗時**：約 55 分鐘
    * **班距**：白天約 10-15 分鐘一班
    """)

    with st.expander("🚇 T2 AREX 一般列車時刻表 (15:00-17:00 區間)"):
        st.markdown("[🔗 AREX 官方時刻表](https://www.arex.or.kr/jsp/eng/main.jsp)")
        st.caption("實際出發時間以現場為準，下表為平日大約時間")
        schedule_data = [
            {"T2 出發": "15:08", "弘大入口": "16:01", "耗時": "53分"},
            {"T2 出發": "15:22", "弘大入口": "16:15", "耗時": "53分"},
            {"T2 出發": "15:38", "弘大入口": "16:31", "耗時": "53分"},
            {"T2 出發": "15:52", "弘大入口": "16:45", "耗時": "53分"},
            {"T2 出發": "16:08", "弘大入口": "17:01", "耗時": "53分"},
            {"T2 出發": "16:22", "弘大入口": "17:15", "耗時": "53分"},
            {"T2 出發": "16:38", "弘大入口": "17:31", "耗時": "53分"},
            {"T2 出發": "16:52", "弘大入口": "17:45", "耗時": "53分"},
        ]
        df = pd.DataFrame(schedule_data)
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.divider()

    # ==========================================
    # 5. 機場 → 飯店：方案 B (機場巴士 6002)
    # ==========================================
    st.subheader("4️⃣ 交通方案 B：機場巴士 6002 (備案)")
    st.markdown("""
    **適合情境：** 行李特別多、或剛好錯過 AREX、人不想擠地鐵

    * **路線**：6002 號 (機場 ➔ 弘大方向)
    * **T2 搭車處**：**B1 樓** 機場巴士月台
    * **下車站**：**서교동 (Seogyo-dong / 西橋洞)** — 飯店官網指定下車點
    * **車資**：約 ₩17,000 (T-money 嗶卡或現金)
    * **耗時**：約 **1 小時 20 分** (尖峰可能拖到 2 小時)
    * **班距**：約 20-30 分鐘一班
    """)

    show_nav_buttons(
        "Incheon Airport T2 Bus Stop 6002",
        mode="walking",
        label_prefix="🚌 ",
    )

    st.warning("⚠️ 6002 容易塞車，**強烈建議優先用 AREX**。巴士只是行李太多時的備案。")

    st.divider()

    # ==========================================
    # 6. 弘大入口站 → 9 Brick Hotel (走路)
    # ==========================================
    st.subheader("5️⃣ 弘大入口站 ➔ 9 Brick Hotel")

    st.markdown("""
    **動線 (飯店官網指引)：**
    1. 從 **2 號線 弘大入口站 9 號出口** 出來
    2. 直走 **150 公尺**
    3. **左轉**
    4. 看到第一條小巷子 **右轉**
    5. 直走 **2 分鐘** 就到

    * **總時間**：約 6 分鐘
    * 拿行李建議走 9 號出口 (有手扶梯)
    """)

    show_nav_buttons(
        "9 Brick Hotel Seoul",
        lat=HOTEL_LAT,
        lng=HOTEL_LNG,
        mode="walking",
        name=HOTEL_NAME,
        label_prefix="🚶 ",
    )

    st.divider()

    # ==========================================
    # 7. 飯店資訊
    # ==========================================
    st.subheader("🏨 9 Brick Hotel (나인브릭 호텔)")

    show_nav_buttons(
        "9 Brick Hotel Seoul",
        lat=HOTEL_LAT,
        lng=HOTEL_LNG,
        mode="walking",
        name=HOTEL_NAME,
    )

    with st.container(border=True):
        st.text("9 Brick Hotel / 나인브릭 호텔")
        st.text(f"📍 韓：{HOTEL_ADDR_KR}")
        st.text(f"📍 英：{HOTEL_ADDR_EN}, 04038")
        st.text("☎️ +82-2-3141-8800")
        st.text("✉️ 9brickhotel@naver.com")
        st.text("🕒 Check-in 15:00 / Check-out 11:00")

    st.divider()

    # ==========================================
    # 8. 晚餐 / 行程 (等使用者補)
    # ==========================================
    st.subheader("6️⃣ 弘大晚餐 & 逛街")
    st.info("📝 待補：晚餐安排、想逛的店、夜市等")


if __name__ == "__main__":
    show()
