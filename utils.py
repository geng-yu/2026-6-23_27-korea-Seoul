import streamlit as st
import pandas as pd
import urllib.parse

# ==================================================================
# 共用變數
# ==================================================================
# NAVER Maps URL Scheme 要求每個呼叫都帶 appname 參數
# 官方規範：mobile web 就用網頁 URL；這邊先用一個識別字串即可。
NAVER_APPNAME = "seoul_trip_2026"


# ==================================================================
# Google Maps 連結 (沿用 Nagoya 的格式)
# ==================================================================
def get_gmap_link(query, mode="transit"):
    """
    Google Maps 導航連結。
    mode: driving (開車), walking (走路), transit (大眾運輸)
    """
    base_url = "https://www.google.com/maps/dir/?api=1"
    return f"{base_url}&destination={urllib.parse.quote(str(query))}&travelmode={mode}"


def get_gmap_search_link(query):
    """Google Maps 純搜尋連結 (沒有導航起點)。"""
    return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(str(query))}"


# ==================================================================
# NAVER 地圖連結 (韓國當地最準的地圖 App)
# ==================================================================
# NAVER 的 URL Scheme 用 nmap:// 開頭。
# 只有手機裝了「네이버지도」App 才會跳轉，沒裝就什麼都不會發生 → 所以保留 Google 當備援很重要。
#
# mode 對照：
#   walking  → walk   (步行)
#   driving  → car    (開車)
#   transit  → public (大眾運輸)
#   bicycle  → bicycle(自行車)
# ==================================================================
_NAVER_MODE_MAP = {
    "walking": "walk",
    "driving": "car",
    "transit": "public",
    "bicycle": "bicycle",
}


def get_naver_link(query=None, lat=None, lng=None, name=None, mode="walking"):
    """
    NAVER Map App 深層連結。
    用法：
      1) 有經緯度 → 規劃路線
         get_naver_link(lat=37.55, lng=126.92, name="9 Brick Hotel", mode="walking")
      2) 只有店名 → 直接搜尋 (使用者自己點導航)
         get_naver_link(query="9 Brick Hotel")
    """
    naver_mode = _NAVER_MODE_MAP.get(mode, "walk")

    if lat is not None and lng is not None:
        dname = urllib.parse.quote(str(name) if name else "目的地")
        return (
            f"nmap://route/{naver_mode}"
            f"?dlat={lat}&dlng={lng}&dname={dname}"
            f"&appname={NAVER_APPNAME}"
        )
    elif query is not None:
        q = urllib.parse.quote(str(query))
        return f"nmap://search?query={q}&appname={NAVER_APPNAME}"
    else:
        return f"nmap://map?appname={NAVER_APPNAME}"


# ==================================================================
# 雙地圖導航按鈕 (Google + NAVER 並排)
# 用法：show_nav_buttons("9 Brick Hotel Seoul", lat=37.5537, lng=126.9205, mode="walking")
# ==================================================================
def show_nav_buttons(query, lat=None, lng=None, mode="walking", name=None, label_prefix=""):
    """
    顯示兩個並排的導航按鈕：Google + NAVER。
    - query: Google Maps 用的搜尋字串 (店名/地址都行)
    - lat, lng: NAVER 用的座標 (有座標的話路線最準)
    - mode: walking / driving / transit
    - name: NAVER 路線顯示用的目的地名稱 (沒給就用 query)
    - label_prefix: 按鈕前綴文字 (例如 "🚶 ")
    """
    col_g, col_n = st.columns(2)
    with col_g:
        st.link_button(
            f"{label_prefix}🟦 Google",
            get_gmap_link(query, mode),
            use_container_width=True,
        )
    with col_n:
        st.link_button(
            f"{label_prefix}🟢 NAVER",
            get_naver_link(
                query=query if (lat is None or lng is None) else None,
                lat=lat,
                lng=lng,
                name=name if name else query,
                mode=mode,
            ),
            use_container_width=True,
        )


# ==================================================================
# 美食店家表格 (一樣按地區整理，把 Google + NAVER 兩個導航欄都加進來)
# ==================================================================
def show_food_table(region):
    """
    顯示美食店家的表格，包含 Google 與 NAVER 雙地圖導航連結。
    Args:
        region (str): 地區名稱，例如 "弘大", "明洞", "江南"
    """

    # ==========================================
    # 1. 在這裡編輯您的店家資料
    # ==========================================
    data_source = {
        "弘大": [
            # 之後再依照行程加入店家，格式：{"店名": "", "時間": "", "備註": ""}
            # 範例：
            # {"店名": "Kyochon Chicken 弘大店", "時間": "11:00-02:00", "備註": "9 Brick Hotel 旁 1 分鐘"},
        ],
        "明洞": [],
        "江南": [],
        "東大門": [],
        "聖水洞": [],
    }

    if region not in data_source:
        st.warning(f"⚠️ 找不到 '{region}' 的資料，請檢查名稱是否正確。")
        return

    rows = data_source[region]
    if not rows:
        st.info(f"📝 {region} 美食清單還沒有資料。")
        return

    df = pd.DataFrame(rows)

    # 兩個導航連結
    df["Google"] = df["店名"].apply(get_gmap_search_link)
    df["NAVER"] = df["店名"].apply(lambda n: get_naver_link(query=n))

    # 欄位順序
    df = df[["店名", "Google", "NAVER", "時間", "備註"]]

    # 表格高度自動調整
    table_height = (len(df) + 1) * 38 + 3

    with st.expander(f"🍽️ 點我看：{region} 美食店家清單", expanded=False):
        st.data_editor(
            df,
            column_config={
                "店名": st.column_config.TextColumn("店名", width="medium"),
                "Google": st.column_config.LinkColumn(
                    "Google", display_text="🟦", help="Google Maps", width="small"
                ),
                "NAVER": st.column_config.LinkColumn(
                    "NAVER", display_text="🟢", help="NAVER 地圖 (需安裝 App)", width="small"
                ),
                "時間": st.column_config.TextColumn("時間", width="medium"),
                "備註": st.column_config.TextColumn("備註", width="large"),
            },
            hide_index=True,
            disabled=True,
            use_container_width=True,
            height=table_height,
        )
