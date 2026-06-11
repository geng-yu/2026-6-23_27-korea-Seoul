"""
渲染共用函式：
- 彩色 G (Google) / N (NAVER) / T (Kakao T) 圓角按鈕
- 卡片格式：[類別標籤] [名稱 ⭐] + meta + 動作按鈕
- 同類別多家可以 group 在同一個標籤下
- 飯店附近：住 + 吃 (expander) + 逛 (expander)，含主行程已排項目放最後
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
    /* === 主卡片 === */
    .stop-card {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 12px;
        padding: 11px 13px;
        margin: 5px 0;
        display: flex;
        align-items: flex-start;
        gap: 10px;
    }
    .stop-card .tag {
        flex-shrink: 0;
        font-size: 16px;
        font-weight: 800;
        color: #ff4b4b;
        min-width: 26px;
        text-align: center;
        line-height: 1.3;
        padding-top: 2px;
    }
    .stop-card .tag.empty { visibility: hidden; }
    .stop-card .body { flex-grow: 1; min-width: 0; }
    .stop-card .top-row {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        justify-content: space-between;
    }
    .stop-card h4 {
        margin: 0;
        font-size: 15.5px;
        font-weight: 700;
        color: var(--text-color);
        line-height: 1.3;
        flex: 1;
        min-width: 0;
    }
    .stop-card .meta {
        font-size: 12px;
        color: var(--text-color);
        opacity: 0.65;
        margin: 3px 0 0 0;
        line-height: 1.4;
    }
    .stop-card .note {
        font-size: 12.5px;
        color: var(--text-color);
        opacity: 0.85;
        margin: 4px 0 0 0;
        line-height: 1.45;
    }
    .stop-card .star { color: #ff4b4b; font-size: 13px; }

    /* === 三顆按鈕 === */
    .nav-btns {
        display: flex;
        gap: 6px;
        flex-shrink: 0;
    }
    .nav-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        font-weight: 800;
        font-size: 13.5px;
        text-decoration: none !important;
        transition: transform 0.1s;
        font-family: system-ui, -apple-system, sans-serif;
    }
    .nav-btn:active { transform: scale(0.92); }
    .nav-btn.g { background: #4285F4; color: white !important; }
    .nav-btn.n { background: #03C75A; color: white !important; }
    .nav-btn.t { background: #FAE100; color: #371D1E !important; }

    /* === 純說明卡 (transit) === */
    .note-card {
        background: var(--secondary-background-color);
        border: 1px dashed rgba(128,128,128,0.30);
        border-radius: 12px;
        padding: 10px 13px;
        margin: 5px 0;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }
    .note-card .tag {
        flex-shrink: 0;
        font-size: 15px;
        font-weight: 700;
        opacity: 0.75;
        min-width: 26px;
        text-align: center;
        padding-top: 2px;
    }
    .note-card .body { flex-grow: 1; min-width: 0; }
    .note-card h5 {
        margin: 0;
        font-size: 14.5px;
        font-weight: 700;
        line-height: 1.3;
    }
    .note-card .meta {
        font-size: 12px;
        opacity: 0.7;
        margin-top: 2px;
        line-height: 1.4;
    }
    .note-card .note {
        font-size: 12.5px;
        opacity: 0.85;
        margin-top: 4px;
        line-height: 1.45;
    }

    /* === 備案區塊 (expander 內部) === */
    .backup-item {
        background: var(--background-color);
        border: 1px solid rgba(128,128,128,0.12);
        border-radius: 10px;
        padding: 9px 11px;
        margin: 5px 0;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }
    .backup-item .info { flex-grow: 1; min-width: 0; }
    .backup-item .name {
        font-size: 13.5px;
        font-weight: 700;
        line-height: 1.3;
    }
    .backup-item .small-meta {
        font-size: 11.5px;
        opacity: 0.65;
        margin-top: 2px;
        line-height: 1.4;
    }
    .backup-item .small-note {
        font-size: 11.5px;
        opacity: 0.8;
        margin-top: 3px;
        line-height: 1.4;
    }
    .backup-item .already {
        font-size: 10px;
        background: rgba(255,75,75,0.12);
        color: #ff4b4b;
        padding: 1px 6px;
        border-radius: 4px;
        margin-left: 6px;
        white-space: nowrap;
        vertical-align: middle;
    }
    /* expander 內部 padding 修正 */
    div[data-testid="stExpander"] details > div { padding-top: 4px !important; }

    /* 隱藏 streamlit 預設選單 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ================================================================
# 連結
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
# HTML 片段建構器
# ================================================================
def _nav_btns_html(place, show_taxi=True):
    name = place["name"]
    name_kr = place.get("name_kr", name)
    lat = place.get("lat")
    lng = place.get("lng")
    g = gmap_url(f"{name_kr} {place.get('address', '')}", "walking")
    n = naver_url(query=name_kr, lat=lat, lng=lng, name=name, mode="walking")
    parts = [
        f'<a class="nav-btn g" href="{g}" target="_blank" title="Google Maps">G</a>',
        f'<a class="nav-btn n" href="{n}" title="NAVER">N</a>',
    ]
    if show_taxi:
        parts.append(f'<a class="nav-btn t" href="{kakaot_url()}" title="Kakao T">T</a>')
    return '<div class="nav-btns">' + ''.join(parts) + '</div>'


def _build_meta_line(place):
    """產生 'name_kr｜sub · hours' 這一行。"""
    name_kr = place.get("name_kr", "")
    parts = []
    if place.get("sub"): parts.append(place["sub"])
    if place.get("hours"): parts.append(place["hours"])
    meta = " · ".join(parts)
    if name_kr and meta:
        return f"{html_lib.escape(name_kr)}｜{html_lib.escape(meta)}"
    elif name_kr:
        return html_lib.escape(name_kr)
    elif meta:
        return html_lib.escape(meta)
    return ""


# ================================================================
# 主行程卡片渲染
# ================================================================
def _render_card(tag, place_id, note_override=None, show_taxi=True):
    """渲染單張主行程卡片。tag 是 '晚'/'逛'/'宵' 等；空字串就隱形(對齊用)。"""
    if place_id not in PLACES:
        st.error(f"❌ 找不到地點: {place_id}")
        return
    p = PLACES[place_id]
    name = html_lib.escape(p["name"])
    star = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    meta = _build_meta_line(p)
    meta_html = f'<p class="meta">{meta}</p>' if meta else ''
    note = note_override if note_override is not None else p.get("note", "")
    note_html = f'<p class="note">{html_lib.escape(note)}</p>' if note else ''
    tag_cls = "tag" if tag else "tag empty"
    tag_text = html_lib.escape(tag) if tag else "·"
    btns = _nav_btns_html(p, show_taxi=show_taxi)

    st.markdown(f"""
    <div class="stop-card">
      <div class="{tag_cls}">{tag_text}</div>
      <div class="body">
        <div class="top-row">
          <h4>{name}{star}</h4>
          {btns}
        </div>
        {meta_html}
        {note_html}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ================================================================
# 公開 API
# ================================================================
def stop(tag, place_ids, others=None, notes=None, show_taxi=True):
    """
    顯示一個或多個主行程地點，共用一個類別標籤。

    Args:
        tag: '早'/'午'/'晚'/'宵'/'點'/'逛'/'買'/'景'/'住' 等。
        place_ids: str (單筆) 或 list[str] (group, 例如逛多家)
        others: None / "food" / "shop" — 加一個「其他」expander，列出同區同類其他選擇。
        notes: None / str / list — 覆寫卡片上的 note。
        show_taxi: 是否顯示 Kakao T (T) 按鈕。
    """
    if isinstance(place_ids, str):
        place_ids = [place_ids]

    # notes 標準化
    if notes is None:
        notes = [None] * len(place_ids)
    elif isinstance(notes, str):
        notes = [notes] + [None] * (len(place_ids) - 1)

    # 渲染所有卡片 (第一張顯示 tag，其餘 tag 留空 = 對齊)
    for i, pid in enumerate(place_ids):
        _render_card(
            tag=tag if i == 0 else "",
            place_id=pid,
            note_override=notes[i] if i < len(notes) else None,
            show_taxi=show_taxi,
        )

    # 「其他 (附近...)」 expander
    if others:
        first_p = PLACES[place_ids[0]]
        area = first_p.get("area")
        cat_label = {"food": "其他吃的", "shop": "其他逛的"}.get(others, "其他")
        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            items = get_by_area(area, exclude=place_ids, cat=others)
            if not items:
                st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            for pid, p in items:
                _render_backup_item(p)


def note(tag, title, meta=None, note=None):
    """顯示一個沒有座標、沒有 G/N/T 按鈕的純說明卡 (交通指引、提醒等)。"""
    title_e = html_lib.escape(title)
    meta_html = f'<p class="meta">{html_lib.escape(meta)}</p>' if meta else ''
    note_html = f'<p class="note">{html_lib.escape(note)}</p>' if note else ''
    tag_e = html_lib.escape(tag) if tag else "·"
    st.markdown(f"""
    <div class="note-card">
      <div class="tag">{tag_e}</div>
      <div class="body">
        <h5>{title_e}</h5>
        {meta_html}
        {note_html}
      </div>
    </div>
    """, unsafe_allow_html=True)


def _render_backup_item(p, already=False):
    """渲染備案/飯店附近清單裡的單一項目。"""
    name = html_lib.escape(p["name"])
    star = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    already_tag = '<span class="already">已排</span>' if already else ''
    name_kr = html_lib.escape(p.get("name_kr", ""))
    parts = []
    if p.get("sub"): parts.append(p["sub"])
    if p.get("hours"): parts.append(p["hours"])
    meta = " · ".join(parts)
    if name_kr and meta:
        meta_line = f"{name_kr}｜{html_lib.escape(meta)}"
    elif name_kr:
        meta_line = name_kr
    elif meta:
        meta_line = html_lib.escape(meta)
    else:
        meta_line = ""
    meta_html = f'<div class="small-meta">{meta_line}</div>' if meta_line else ''
    note_html = f'<div class="small-note">{html_lib.escape(p.get("note", ""))}</div>' if p.get("note") else ''
    btns = _nav_btns_html(p, show_taxi=True)
    st.markdown(f"""
    <div class="backup-item">
      <div class="info">
        <div class="name">{name}{star}{already_tag}</div>
        {meta_html}
        {note_html}
      </div>
      {btns}
    </div>
    """, unsafe_allow_html=True)


def hotel_bottom(today_food=None, today_shop=None):
    """
    每天最下面：住 (卡片) + 🏨吃 (expander) + 🏨逛 (expander)。
    today_food / today_shop 是當天主行程已經安排的 place_ids，
    它們仍然會顯示在 expander 裡，但 sorted 到清單最後並加「已排」標籤。
    """
    today_food = set(today_food or [])
    today_shop = set(today_shop or [])

    # 住卡片 (T 按鈕沒意義，因為已經在這裡了)
    _render_card(tag="住", place_id="hotel", show_taxi=False)

    # 🏨吃 expander
    food_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="food")
    food_sorted = sorted(food_all, key=lambda x: (x[0] in today_food, x[0]))
    with st.expander("🍽️ 吃 — 飯店附近"):
        st.caption("弘대區所有吃的清單。主行程已排的會放最下面標「已排」。")
        for pid, p in food_sorted:
            _render_backup_item(p, already=(pid in today_food))

    # 🏨逛 expander
    shop_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="shop")
    shop_sorted = sorted(shop_all, key=lambda x: (x[0] in today_shop, x[0]))
    with st.expander("🛍️ 逛 — 飯店附近"):
        st.caption("弘대區所有逛的清單。主行程已排的會放最下面標「已排」。")
        for pid, p in shop_sorted:
            _render_backup_item(p, already=(pid in today_shop))
