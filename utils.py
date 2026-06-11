"""
渲染共用函式：
- 彩色 G (Google) / N (NAVER) / T (Kakao T) 圓角按鈕
- 主行程卡片 + 該卡的「附近備案」expander
- 飯店附近隨時可去 expander
"""
import streamlit as st
import urllib.parse
import html as html_lib

from places import PLACES, get_by_area, AREA_HONGDAE


# ================================================================
# 全域 CSS — 注入一次就好，所有 HTML 都共用
# ================================================================
def inject_css():
    """在 app.py 開頭呼叫，注入全域樣式。"""
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
    .stop-card .body {
        flex-grow: 1;
        min-width: 0;
    }
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
    .stop-card .star {
        color: #ff4b4b;
        font-size: 14px;
    }

    /* ---- 三顆動作按鈕 ---- */
    .nav-btns {
        display: flex;
        gap: 8px;
        margin-top: 8px;
    }
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
    .nav-btn:active {
        transform: scale(0.95);
    }
    .nav-btn.g {
        background: #4285F4;
        color: white !important;
    }
    .nav-btn.n {
        background: #03C75A;
        color: white !important;
    }
    .nav-btn.t {
        background: #FAE100;
        color: #371D1E !important;
    }

    /* ---- 備案區塊 ---- */
    .backup-cat-title {
        font-size: 13px;
        font-weight: 700;
        opacity: 0.7;
        margin: 12px 0 6px 0;
        padding: 0;
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
    .backup-item .info {
        flex-grow: 1;
        min-width: 0;
    }
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

    /* 隱掉 expander 內 streamlit 預設 padding 太大的問題 */
    div[data-testid="stExpander"] details > div {
        padding-top: 6px !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ================================================================
# 連結產生 — Google / NAVER / Kakao T
# ================================================================
def gmap_url(query, mode="walking"):
    """Google Maps 導航。mode: driving/walking/transit"""
    q = urllib.parse.quote(str(query))
    return f"https://www.google.com/maps/dir/?api=1&destination={q}&travelmode={mode}"


def naver_url(query=None, lat=None, lng=None, name=None, mode="walking"):
    """NAVER Maps app deep link (nmap://)。手機要裝네이버지도。"""
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
    """Kakao T 計程車 deep link — 開 App 後手動輸入目的地 (Kakao 沒開放外部設目的地)"""
    return "kakaotaxi://"


# ================================================================
# 卡片渲染
# ================================================================
def _btns_html(place, show_taxi=True):
    """產生 G / N / T 三顆按鈕的 HTML。"""
    name = place["name"]
    name_kr = place.get("name_kr", name)
    lat = place.get("lat")
    lng = place.get("lng")

    g = gmap_url(f"{name_kr} {place.get('address', '')}", "walking")
    n = naver_url(query=name_kr, lat=lat, lng=lng, name=name, mode="walking")
    t = kakaot_url()

    btns = []
    btns.append(f'<a class="nav-btn g" href="{g}" target="_blank" title="Google Maps">G</a>')
    btns.append(f'<a class="nav-btn n" href="{n}" title="NAVER Map">N</a>')
    if show_taxi:
        btns.append(f'<a class="nav-btn t" href="{t}" title="Kakao T">T</a>')
    return '<div class="nav-btns">' + ''.join(btns) + '</div>'


def show_stop(time, place_id, override_note=None, show_taxi=True, no_backup=False):
    """主行程卡片 + (可選) 該地點同區的備案 expander。

    Args:
        time: "10:30" 之類的時間字串
        place_id: PLACES 字典裡的 key
        override_note: 取代 places.py 裡的 note (顯示在卡片上)
        show_taxi: 是否顯示 Kakao T 按鈕 (機場類就不用)
        no_backup: True 時不顯示備案 expander (例如交通類)
    """
    if place_id not in PLACES:
        st.error(f"❌ 找不到地點：{place_id}")
        return

    p = PLACES[place_id]
    name = html_lib.escape(p["name"])
    name_kr = html_lib.escape(p.get("name_kr", ""))
    star = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    area = html_lib.escape(p.get("area", ""))
    hours = html_lib.escape(p.get("hours", ""))
    sub = html_lib.escape(p.get("sub", ""))
    meta_parts = [x for x in [area, sub, hours] if x]
    meta = ' · '.join(meta_parts)
    note = override_note if override_note is not None else p.get("note", "")
    note_html = f'<p class="note">{html_lib.escape(note)}</p>' if note else ''

    btns_html = _btns_html(p, show_taxi=show_taxi)

    st.markdown(f"""
    <div class="stop-card">
      <div class="time">{html_lib.escape(time)}</div>
      <div class="body">
        <h4>{name}{star}</h4>
        <p class="meta">{name_kr}{('｜' + meta) if meta else ''}</p>
        {note_html}
        {btns_html}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 同區備案 expander (排除自己)
    if not no_backup and p.get("area") not in ("機場", None):
        _show_backup_expander(place_id, p)


def _show_backup_expander(this_id, place):
    """渲染「附近備案」expander，內部按 吃/逛/景點 分類。"""
    area = place["area"]
    backup_label = f"🔄 {place['name']} 附近備案 (吃/逛/景點)"

    with st.expander(backup_label):
        # 分類
        food_places = get_by_area(area, exclude=this_id, cat="food")
        cafe_places = get_by_area(area, exclude=this_id, cat="cafe")
        food_all = food_places + cafe_places
        shop_places = get_by_area(area, exclude=this_id, cat="shop")
        sight_places = get_by_area(area, exclude=this_id, cat="sight")

        if not food_all and not shop_places and not sight_places:
            st.caption(f"({area} 沒有其他備案資料)")
            return

        if food_all:
            st.markdown('<div class="backup-cat-title">🍽️ 吃</div>', unsafe_allow_html=True)
            for pid, p in food_all:
                _render_backup_item(p)

        if shop_places:
            st.markdown('<div class="backup-cat-title">🛍️ 逛/買</div>', unsafe_allow_html=True)
            for pid, p in shop_places:
                _render_backup_item(p)

        if sight_places:
            st.markdown('<div class="backup-cat-title">🏛️ 景點</div>', unsafe_allow_html=True)
            for pid, p in sight_places:
                _render_backup_item(p)


def _render_backup_item(p):
    """渲染備案 / 飯店附近清單裡的單一項目。"""
    name = html_lib.escape(p["name"])
    name_kr = html_lib.escape(p.get("name_kr", ""))
    star = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    sub = p.get("sub", "")
    hours = p.get("hours", "")
    note = p.get("note", "")
    meta_parts = [x for x in [sub, hours] if x]
    meta = ' · '.join(meta_parts)
    note_line = f'<div class="small-meta">{html_lib.escape(note)}</div>' if note else ''

    btns_html = _btns_html(p)

    st.markdown(f"""
    <div class="backup-item">
      <div class="info">
        <div class="name">{name}{star}</div>
        <div class="small-meta">{name_kr}{('｜' + html_lib.escape(meta)) if meta else ''}</div>
        {note_line}
      </div>
      {btns_html}
    </div>
    """, unsafe_allow_html=True)


# ================================================================
# 飯店附近 — 永遠是弘대區 (每天的下面都會放一個)
# ================================================================
def show_hotel_nearby(exclude_ids=None):
    """飯店 (弘대) 附近永遠可去的清單，每天底下都會放。
    exclude_ids 用來排除當天主行程已經安排的，避免重複。"""
    exclude_ids = exclude_ids or []
    if isinstance(exclude_ids, str):
        exclude_ids = [exclude_ids]

    with st.expander("🏨 飯店附近 — 隨時可以去 (吃/逛/買/景點)"):
        st.caption("9 Brick Hotel 附近走路 1-15 min 範圍內的清單。當天行程提早結束就過來。")

        food_all = get_by_area(AREA_HONGDAE, exclude=exclude_ids + ["hotel"], cat="food")
        shop_all = get_by_area(AREA_HONGDAE, exclude=exclude_ids + ["hotel"], cat="shop")
        sight_all = get_by_area(AREA_HONGDAE, exclude=exclude_ids + ["hotel"], cat="sight")

        # 把吃再依照 sub 分組 (使用者要求「分類」)
        if food_all:
            st.markdown('<div class="hotel-section-title">🍽️ 吃</div>', unsafe_allow_html=True)
            # 依 sub 分組
            food_by_sub = {}
            for pid, p in food_all:
                sub = p.get("sub", "其他")
                food_by_sub.setdefault(sub, []).append((pid, p))
            for sub, items in food_by_sub.items():
                st.markdown(f'<div class="backup-cat-title">— {sub} —</div>', unsafe_allow_html=True)
                for pid, p in items:
                    _render_backup_item(p)

        if shop_all:
            st.markdown('<div class="hotel-section-title">🛍️ 逛/買</div>', unsafe_allow_html=True)
            shop_by_sub = {}
            for pid, p in shop_all:
                sub = p.get("sub", "其他")
                shop_by_sub.setdefault(sub, []).append((pid, p))
            for sub, items in shop_by_sub.items():
                st.markdown(f'<div class="backup-cat-title">— {sub} —</div>', unsafe_allow_html=True)
                for pid, p in items:
                    _render_backup_item(p)

        if sight_all:
            st.markdown('<div class="hotel-section-title">🏛️ 景點</div>', unsafe_allow_html=True)
            for pid, p in sight_all:
                _render_backup_item(p)
