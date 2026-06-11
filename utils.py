"""
渲染共用函式
"""
import streamlit as st
import urllib.parse
import html as html_lib

from places import PLACES, get_by_area, AREA_HONGDAE


# ================================================================
# 全域 CSS
# ================================================================
def inject_css():
    st.markdown("""
    <style>
    /* ---- 主行程卡片 ---- */
    .stop-card {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 14px;
        padding: 14px 16px;
        margin: 8px 0;
        display: flex;
        align-items: flex-start;
        gap: 14px;
    }
    .stop-card .time {
        flex-shrink: 0;
        font-size: 15px;
        font-weight: 700;
        color: var(--text-color);
        opacity: 0.85;
        min-width: 50px;
        padding-top: 2px;
    }
    .stop-card .body { flex-grow: 1; min-width: 0; }
    .stop-card h4 {
        margin: 0 0 4px 0;
        font-size: 16px;
        font-weight: 700;
        color: var(--text-color);
        line-height: 1.3;
    }
    .stop-card .meta {
        font-size: 12.5px;
        color: var(--text-color);
        opacity: 0.65;
        margin: 0 0 4px 0;
        line-height: 1.4;
    }
    .stop-card .note {
        font-size: 13px;
        color: var(--text-color);
        opacity: 0.85;
        margin: 4px 0 8px 0;
        line-height: 1.5;
    }
    .stop-card .star { color: #ff4b4b; font-size: 14px; }
    /* ---- 標題列（名稱 + 按鈕同行）---- */
    .title-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 4px;
    }
    .title-row h4 {
        margin: 0;
        flex: 1;
        min-width: 0;
    }
    .title-row .nav-btns {
        margin-top: 0;   /* 覆蓋原本的 margin-top: 8px */
        flex-shrink: 0;
    }

    /* ---- 導航按鈕 ---- */
    .nav-btns { display: flex; gap: 8px; margin-top: 8px; }
    .nav-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        font-weight: 800;
        font-size: 14px;
        text-decoration: none !important;
        transition: transform 0.1s;
        font-family: system-ui, -apple-system, sans-serif;
    }
    .nav-btn:active { transform: scale(0.95); }
    .nav-btn.g { background: #4285F4; color: white !important; }
    .nav-btn.n { background: #03C75A; color: white !important; }
    .nav-btn.t { background: #FAE100; color: #371D1E !important; }

    /* ---- 備案區塊 ---- */
    .backup-cat-title {
        font-size: 13px;
        font-weight: 700;
        opacity: 0.7;
        margin: 12px 0 6px 0;
        padding: 0;
    }
    /* 備案清單限高捲動容器 */
    .backup-scroll {
        max-height: 320px;
        overflow-y: auto;
        padding-right: 4px;
    }
    .backup-scroll::-webkit-scrollbar { width: 4px; }
    .backup-scroll::-webkit-scrollbar-track { background: transparent; }
    .backup-scroll::-webkit-scrollbar-thumb {
        background: rgba(128,128,128,0.3);
        border-radius: 2px;
    }
    .backup-item {
        background: var(--background-color);
        border: 1px solid rgba(128,128,128,0.12);
        border-radius: 10px;
        padding: 10px 12px;
        margin: 6px 0;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 10px;
    }
    .backup-item .info { flex-grow: 1; min-width: 0; }
    .backup-item .name {
        font-size: 14px;
        font-weight: 700;
        line-height: 1.3;
        color: var(--text-color);
    }
    .backup-item .small-meta {
        font-size: 11.5px;
        opacity: 0.65;
        margin-top: 2px;
        color: var(--text-color);
        line-height: 1.4;
    }

    /* ---- 飯店區塊標題 ---- */
    .hotel-section-title {
        font-size: 14px;
        font-weight: 700;
        margin: 16px 0 6px 0;
        padding: 6px 10px;
        background: var(--secondary-background-color);
        border-radius: 8px;
        border-left: 3px solid #ff4b4b;
    }

    div[data-testid="stExpander"] details > div {
        padding-top: 6px !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ================================================================
# 連結產生
# ================================================================
def gmap_url(query, mode="walking"):
    q = urllib.parse.quote(str(query))
    return f"https://www.google.com/maps/dir/?api=1&destination={q}&travelmode={mode}"


def naver_url(query=None, lat=None, lng=None, name=None, mode="walking"):
    appname = "seoul_trip_2026"
    mode_map = {"walking": "walk", "driving": "car", "transit": "public"}
    nm = mode_map.get(mode, "walk")
    if lat is not None and lng is not None:
        dname = urllib.parse.quote(str(name or "目的地"))
        return f"nmap://route/{nm}?dlat={lat}&dlng={lng}&dname={dname}&appname={appname}"
    if query:
        q = urllib.parse.quote(str(query))
        return f"nmap://search?query={q}&appname={appname}"
    return f"nmap://map?appname={appname}"


def kakaot_url():
    return "kakaotaxi://"


# ================================================================
# 卡片渲染
# ================================================================
def _btns_html(place, show_g=True, show_n=True, show_t=True, mode="walking"):
    """產生導航按鈕 HTML。
    show_g / show_n / show_t：各自獨立控制顯示
    mode：walking / transit / driving
    """
    name_kr = place.get("name_kr", place["name"])
    lat = place.get("lat")
    lng = place.get("lng")

    btns = []
    if show_g:
        g = gmap_url(f"{name_kr} {place.get('address', '')}", mode)
        btns.append(f'<a class="nav-btn g" href="{g}" target="_blank" title="Google Maps">G</a>')
    if show_n:
        n = naver_url(query=name_kr, lat=lat, lng=lng, name=place["name"], mode=mode)
        btns.append(f'<a class="nav-btn n" href="{n}" title="NAVER Map">N</a>')
    if show_t:
        btns.append(f'<a class="nav-btn t" href="{kakaot_url()}" title="Kakao T">T</a>')

    if not btns:
        return ""
    return '<div class="nav-btns">' + ''.join(btns) + '</div>'


def show_stop(time, place_id,
              override_note=None,
              show_g=True, show_n=True, show_t=True,
              mode="walking",
              no_backup=False):
    """主行程卡片。

    參數：
        time          : 時間字串，e.g. "10:30"
        place_id      : places.py 的 key
        override_note : 覆蓋 places.py 裡的 note（傳 " " 可清空）
        show_g        : 是否顯示 Google Maps 按鈕（預設 True）
        show_n        : 是否顯示 NAVER 按鈕（預設 True）
        show_t        : 是否顯示 Kakao T 按鈕（預設 True）
        mode          : 導航模式 "walking" / "transit" / "driving"
        no_backup     : True = 不顯示備案 expander
    """
    if place_id not in PLACES:
        st.error(f"❌ 找不到地點：{place_id}")
        return

    p = PLACES[place_id]
    name     = html_lib.escape(p["name"])
    name_kr  = html_lib.escape(p.get("name_kr", ""))
    star     = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    area     = html_lib.escape(p.get("area", ""))
    hours    = html_lib.escape(p.get("hours", ""))
    sub      = html_lib.escape(p.get("sub", ""))
    meta_parts = [x for x in [area, sub, hours] if x]
    meta     = ' · '.join(meta_parts)
    note     = override_note if override_note is not None else p.get("note", "")
    note_html = f'<p class="note">{html_lib.escape(note)}</p>' if note else ''
    btns_html = _btns_html(p, show_g=show_g, show_n=show_n, show_t=show_t, mode=mode)

    st.markdown(f"""
    <div class="stop-card">
      <div class="time">{html_lib.escape(time)}</div>
      <div class="body">
        <div class="title-row">
          <h4>{name}{star}</h4>
          {btns_html}
        </div>
        <p class="meta">{name_kr}{('｜' + meta) if meta else ''}</p>
        {note_html}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not no_backup and p.get("area") not in ("機場", None):
        _show_backup_expander(place_id, p)


def _show_backup_expander(this_id, place):
    """備案 expander，內容限高 320px 可捲動。"""
    area = place["area"]

    with st.expander(f"🔄 {place['name']} 附近備案"):
        food_all  = get_by_area(area, exclude=this_id, cat="food") + \
                    get_by_area(area, exclude=this_id, cat="cafe")
        shop_all  = get_by_area(area, exclude=this_id, cat="shop")
        sight_all = get_by_area(area, exclude=this_id, cat="sight")

        if not food_all and not shop_all and not sight_all:
            st.caption(f"({area} 沒有其他備案資料)")
            return

        inner_html = ""
        if food_all:
            inner_html += '<div class="backup-cat-title">🍽️ 吃</div>'
            for _, p in food_all:
                inner_html += _backup_item_html(p)
        if shop_all:
            inner_html += '<div class="backup-cat-title">🛍️ 逛/買</div>'
            for _, p in shop_all:
                inner_html += _backup_item_html(p)
        if sight_all:
            inner_html += '<div class="backup-cat-title">🏛️ 景點</div>'
            for _, p in sight_all:
                inner_html += _backup_item_html(p)

        st.markdown(f'<div class="backup-scroll">{inner_html}</div>',
                    unsafe_allow_html=True)


def _backup_item_html(p):
    """產生單一備案項目的 HTML 字串。"""
    name      = html_lib.escape(p["name"])
    name_kr   = html_lib.escape(p.get("name_kr", ""))
    star      = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    sub       = p.get("sub", "")
    hours     = p.get("hours", "")
    note      = p.get("note", "")
    meta_parts = [x for x in [sub, hours] if x]
    meta      = ' · '.join(meta_parts)
    note_line = f'<div class="small-meta">{html_lib.escape(note)}</div>' if note else ''
    btns      = _btns_html(p)  # 備案預設 G+N+T 全開，walking

    return f"""
    <div class="backup-item">
      <div class="info">
        <div class="name">{name}{star}</div>
        <div class="small-meta">{name_kr}{('｜' + html_lib.escape(meta)) if meta else ''}</div>
        {note_line}
      </div>
      {btns}
    </div>"""


# ================================================================
# 飯店附近
# ================================================================
def show_hotel_nearby(exclude_ids=None):
    """飯店 (弘대) 附近永遠可去的清單，限高捲動。"""
    exclude_ids = exclude_ids or []
    if isinstance(exclude_ids, str):
        exclude_ids = [exclude_ids]

    with st.expander("🏨 飯店附近 — 隨時可以去"):
        st.caption("9 Brick Hotel 走路 1-15 min 範圍內。")

        food_all  = get_by_area(AREA_HONGDAE, exclude=exclude_ids + ["hotel"], cat="food") + \
                    get_by_area(AREA_HONGDAE, exclude=exclude_ids + ["hotel"], cat="cafe")
        shop_all  = get_by_area(AREA_HONGDAE, exclude=exclude_ids + ["hotel"], cat="shop")
        sight_all = get_by_area(AREA_HONGDAE, exclude=exclude_ids + ["hotel"], cat="sight")

        inner_html = ""
        if food_all:
            inner_html += '<div class="backup-cat-title">🍽️ 吃</div>'
            for _, p in food_all:
                inner_html += _backup_item_html(p)
        if shop_all:
            inner_html += '<div class="backup-cat-title">🛍️ 逛/買</div>'
            for _, p in shop_all:
                inner_html += _backup_item_html(p)
        if sight_all:
            inner_html += '<div class="backup-cat-title">🏛️ 景點</div>'
            for _, p in sight_all:
                inner_html += _backup_item_html(p)

        if not inner_html:
            st.caption("(暫無資料)")
            return

        st.markdown(f'<div class="backup-scroll">{inner_html}</div>',
                    unsafe_allow_html=True)
