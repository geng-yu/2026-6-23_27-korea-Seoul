"""
渲染共用函式（v2 卡片版）：
- 所有 HTML 一律用「單行串接」組出來，零縮排 → 永遠不會被 Markdown 當成程式碼區塊
- 卡片式設計：左側彩色類別晶片 + 卡片陰影 + 左側色條
- expander 內容固定高度 320px，超過用上下滑動
- set_scheduled()：登記當天主行程已排的店，所有「其他」expander 會把已排的沉到最下面並標「已排」
"""
import streamlit as st
import urllib.parse
import html as html_lib

from places import PLACES, get_by_area, AREA_HONGDAE


# ================================================================
# 當天已排清單（每次 rerun 由 day 檔重新登記）
# ================================================================
_SCHEDULED = {"food": set(), "shop": set()}


def set_scheduled(today_food=None, today_shop=None):
    """在每天 show_day() 最開頭呼叫，登記當天主行程已排的 place_ids。
    之後所有「其他吃的/逛的」expander 都會自動把這些項目排到最後並標「已排」。"""
    _SCHEDULED["food"] = set(today_food or [])
    _SCHEDULED["shop"] = set(today_shop or [])


# ================================================================
# 全域 CSS
# ================================================================
# 注意：這段字串「故意完全靠左、不縮排」。
# st.markdown 遇到縮排 4 格以上的行會當成 code block，CSS 就會直接印在畫面上。
_CSS = """
<style>
/* ===== 主卡片 ===== */
.stop-card{
  position:relative;
  background:var(--secondary-background-color);
  border:1px solid rgba(128,128,128,.16);
  border-radius:14px;
  padding:12px 14px 12px 12px;
  margin:8px 0;
  display:flex;
  align-items:flex-start;
  gap:11px;
  box-shadow:0 1px 4px rgba(0,0,0,.05);
  overflow:hidden;
}
.stop-card::before{
  content:"";
  position:absolute; left:0; top:0; bottom:0;
  width:4px;
  background:var(--card-accent,#9aa0a6);
}

/* 類別晶片 */
.stop-card .chip{
  flex-shrink:0;
  width:34px; height:34px;
  border-radius:10px;
  display:flex; align-items:center; justify-content:center;
  font-size:15px; font-weight:800;
  color:#fff;
  background:var(--card-accent,#9aa0a6);
  margin-top:1px;
}
.stop-card .chip.ghost{
  background:transparent;
  color:transparent;
}

/* 類別顏色 */
.acc-morning{ --card-accent:#f59e0b; }   /* 早 */
.acc-lunch  { --card-accent:#f97316; }   /* 午 */
.acc-dinner { --card-accent:#ef4444; }   /* 晚 */
.acc-night  { --card-accent:#6366f1; }   /* 宵 */
.acc-snack  { --card-accent:#ec4899; }   /* 點 */
.acc-shop   { --card-accent:#a855f7; }   /* 逛/買 */
.acc-sight  { --card-accent:#10b981; }   /* 景 */
.acc-stay   { --card-accent:#3b82f6; }   /* 住 */
.acc-move   { --card-accent:#94a3b8; }   /* 交通/其他 */

.stop-card .body{ flex-grow:1; min-width:0; }
.stop-card .top-row{
  display:flex; align-items:center; gap:8px;
  flex-wrap:nowrap; justify-content:space-between;
}
.stop-card h4{
  margin:0; font-size:15.5px; font-weight:700;
  color:var(--text-color); line-height:1.35;
  flex:1; min-width:0;
}
.stop-card .meta{
  font-size:12px; color:var(--text-color); opacity:.62;
  margin:4px 0 0 0; line-height:1.45;
}
.stop-card .note{
  font-size:12.5px; color:var(--text-color); opacity:.88;
  margin:5px 0 0 0; line-height:1.5;
}
.stop-card .star{ color:#ff4b4b; font-size:13px; }

/* ===== 純說明卡（交通/提醒，虛線） ===== */
.note-card{
  position:relative;
  background:transparent;
  border:1.5px dashed rgba(128,128,128,.35);
  border-radius:14px;
  padding:10px 14px;
  margin:8px 0;
  display:flex; gap:11px; align-items:flex-start;
}
.note-card .chip{
  flex-shrink:0; width:34px; height:34px;
  border-radius:10px;
  display:flex; align-items:center; justify-content:center;
  font-size:16px;
  background:rgba(128,128,128,.10);
}
.note-card .body{ flex-grow:1; min-width:0; }
.note-card .top-row{
  display:flex; align-items:center; gap:8px;
  flex-wrap:nowrap; justify-content:space-between;
}
.note-card h5{
  margin:0; font-size:14.5px; font-weight:700;
  line-height:1.35; flex:1; min-width:0;
}
.note-card .meta{ font-size:12px; opacity:.68; margin-top:3px; line-height:1.45; }
.note-card .note{ font-size:12.5px; opacity:.86; margin-top:4px; line-height:1.5; }

/* ===== G / N / T 圓鈕 ===== */
.nav-btns{ display:flex; gap:6px; flex-shrink:0; align-items:center; }
.nav-btn{
  display:inline-flex; align-items:center; justify-content:center;
  width:30px; height:30px; border-radius:50%;
  font-weight:800; font-size:13.5px;
  text-decoration:none !important;
  transition:transform .1s;
  font-family:system-ui,-apple-system,sans-serif;
  box-shadow:0 1px 2px rgba(0,0,0,.15);
}
.nav-btn:active{ transform:scale(.92); }
.nav-btn.g{ background:#4285F4; color:#fff !important; }
.nav-btn.n{ background:#03C75A; color:#fff !important; }
.nav-btn.t{ background:#FAE100; color:#371D1E !important; }

/* ===== 備案 / 飯店附近清單項目 ===== */
.backup-item{
  background:var(--secondary-background-color);
  border:1px solid rgba(128,128,128,.14);
  border-radius:12px;
  padding:9px 11px;
  margin:6px 2px;
  display:flex; gap:10px; align-items:flex-start;
  box-shadow:0 1px 2px rgba(0,0,0,.04);
}
.backup-item.scheduled{ opacity:.62; }
.backup-item .info{ flex-grow:1; min-width:0; }
.backup-item .name{ font-size:13.5px; font-weight:700; line-height:1.35; }
.backup-item .small-meta{ font-size:11.5px; opacity:.65; margin-top:2px; line-height:1.4; }
.backup-item .small-note{ font-size:11.5px; opacity:.82; margin-top:3px; line-height:1.45; }
.backup-item .already{
  font-size:10px; font-weight:700;
  background:rgba(255,75,75,.13); color:#ff4b4b;
  padding:2px 7px; border-radius:99px;
  margin-left:6px; white-space:nowrap; vertical-align:middle;
}

/* ===== expander：固定高度 + 上下滑動 ===== */
div[data-testid="stExpander"] [data-testid="stExpanderDetails"]{
  max-height:320px;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
  padding-top:4px !important;
  padding-right:6px;
}
/* 舊版 Streamlit 結構 fallback */
div[data-testid="stExpander"] details > div{
  max-height:320px;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
  padding-top:4px !important;
}


/* ===== 同一張卡片內的多個分段 ===== */
.stop-card .section{
  padding:9px 0 2px 0;
  border-top:1px dashed rgba(128,128,128,.22);
  margin-top:7px;
}
.stop-card .section:first-of-type{
  border-top:none; margin-top:0; padding-top:0;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


# ================================================================
# 類別 → 顏色 class
# ================================================================
_TAG_ACCENT = {
    "早": "acc-morning",
    "午": "acc-lunch",
    "晚": "acc-dinner",
    "宵": "acc-night",
    "點": "acc-snack",
    "逛": "acc-shop",
    "買": "acc-shop",
    "景": "acc-sight",
    "住": "acc-stay",
}


def _accent_cls(tag):
    return _TAG_ACCENT.get(tag, "acc-move")


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


def _safe_href(url: str) -> str:
    return html_lib.escape(url, quote=True)


# ================================================================
# HTML 片段建構器（全部單行串接，零縮排）
# ================================================================
def _nav_btns_html(place, show_taxi=True, mode="walking"):
    name = place["name"]
    name_kr = place.get("name_kr", name)
    lat = place.get("lat")
    lng = place.get("lng")

    g = _safe_href(gmap_url(f"{name_kr} {place.get('address', '')}", mode))
    n = _safe_href(naver_url(query=name_kr, lat=lat, lng=lng, name=name, mode=mode))

    parts = [
        f'<a class="nav-btn g" href="{g}" target="_blank" title="Google Maps">G</a>',
        f'<a class="nav-btn n" href="{n}" title="NAVER">N</a>',
    ]
    if show_taxi:
        t = _safe_href(kakaot_url())
        parts.append(f'<a class="nav-btn t" href="{t}" title="Kakao T">T</a>')
    return '<div class="nav-btns">' + ''.join(parts) + '</div>'


def _build_meta_line(place):
    """產生 'name_kr｜sub · hours' 這一行。"""
    name_kr = place.get("name_kr", "")
    parts = []
    if place.get("sub"):
        parts.append(place["sub"])
    if place.get("hours"):
        parts.append(place["hours"])
    meta = " · ".join(parts)

    if name_kr and meta:
        return f"{html_lib.escape(name_kr)}｜{html_lib.escape(meta)}"
    elif name_kr:
        return html_lib.escape(name_kr)
    elif meta:
        return html_lib.escape(meta)
    return ""


def _card_html(accent_cls, chip_html, title_html, btns_html, meta_html, note_html,
               card_class="stop-card", title_tag="h4"):
    """組出一張卡片的完整 HTML（單行，零換行零縮排）。"""
    return (
        f'<div class="{card_class} {accent_cls}">'
        f'{chip_html}'
        f'<div class="body">'
        f'<div class="top-row">'
        f'<{title_tag}>{title_html}</{title_tag}>'
        f'{btns_html}'
        f'</div>'
        f'{meta_html}'
        f'{note_html}'
        f'</div>'
        f'</div>'
    )


# ================================================================
# 主行程卡片渲染
# ================================================================
def _render_card(tag, place_id, note_override=None, show_taxi=True, mode="walking",
                 accent_override=None):
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

    accent = accent_override or _accent_cls(tag)
    if tag:
        chip_html = f'<div class="chip">{html_lib.escape(tag)}</div>'
    else:
        chip_html = '<div class="chip ghost">·</div>'

    btns = _nav_btns_html(p, show_taxi=show_taxi, mode=mode)

    st.markdown(
        _card_html(accent, chip_html, f'{name}{star}', btns, meta_html, note_html),
        unsafe_allow_html=True,
    )


def custom_card(tag, title, meta=None, note=None, links=None, dashed=False):
    """
    自訂卡片：給 Day1 第1~3格這種特殊內容用。
    links: list[dict]，例如 [{"label": "G", "url": "...", "cls": "g"}]
    """
    card_class = "note-card" if dashed else "stop-card"
    title_tag = "h5" if dashed else "h4"
    accent = _accent_cls(tag)

    tag_e = html_lib.escape(tag) if tag else "·"
    if dashed:
        chip_html = f'<div class="chip">{tag_e}</div>'
    elif tag:
        chip_html = f'<div class="chip">{tag_e}</div>'
    else:
        chip_html = '<div class="chip ghost">·</div>'

    title_e = html_lib.escape(title)
    meta_html = f'<p class="meta">{html_lib.escape(meta)}</p>' if meta else ''
    note_html = f'<p class="note">{html_lib.escape(note)}</p>' if note else ''

    btns_html = ""
    if links:
        parts = []
        for item in links:
            label = html_lib.escape(item.get("label", ""))
            cls = html_lib.escape(item.get("cls", "g"))
            url = _safe_href(item.get("url", "#"))
            target = ' target="_blank"' if url.startswith("http") else ""
            parts.append(
                f'<a class="nav-btn {cls}" href="{url}"{target} title="{label}">{label}</a>'
            )
        btns_html = '<div class="nav-btns">' + ''.join(parts) + '</div>'

    st.markdown(
        _card_html(accent, chip_html, title_e, btns_html, meta_html, note_html,
                   card_class=card_class, title_tag=title_tag),
        unsafe_allow_html=True,
    )


# ================================================================
# 備案 / 飯店附近清單項目
# ================================================================
def _render_backup_item(p, already=False):
    name = html_lib.escape(p["name"])
    star = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    already_tag = '<span class="already">已排</span>' if already else ''
    name_kr = html_lib.escape(p.get("name_kr", ""))

    parts = []
    if p.get("sub"):
        parts.append(p["sub"])
    if p.get("hours"):
        parts.append(p["hours"])
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
    btns = _nav_btns_html(p, show_taxi=True, mode="walking")
    item_cls = "backup-item scheduled" if already else "backup-item"

    st.markdown(
        (
            f'<div class="{item_cls}">'
            f'<div class="info">'
            f'<div class="name">{name}{star}{already_tag}</div>'
            f'{meta_html}'
            f'{note_html}'
            f'</div>'
            f'{btns}'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )


def _render_backup_list(items, scheduled_ids):
    """已排的沉到最下面 + 標「已排」。items: list[(pid, place)]"""
    items_sorted = sorted(items, key=lambda x: (x[0] in scheduled_ids, x[0]))
    for pid, p in items_sorted:
        _render_backup_item(p, already=(pid in scheduled_ids))


# ================================================================
# 公開 API
# ================================================================
def stop(tag, place_ids, others=None, notes=None, show_taxi=True, mode="walking"):
    """
    顯示一個或多個主行程地點，共用一個類別標籤。

    Args:
        tag: '早'/'午'/'晚'/'宵'/'點'/'逛'/'買'/'景'/'住' 等。
        place_ids: str (單筆) 或 list[str] (group)
        others: None / "food" / "shop" — 加一個「其他」expander。
                清單中若有「當天主行程已排」(set_scheduled 登記過) 的項目，
                會沉到最下面並標「已排」。
        notes: None / str / list — 覆寫卡片上的 note。
        show_taxi: 是否顯示 Kakao T (T) 按鈕。
        mode: walking / driving / transit
    """
    if isinstance(place_ids, str):
        place_ids = [place_ids]

    if notes is None:
        notes = [None] * len(place_ids)
    elif isinstance(notes, str):
        notes = [notes] + [None] * (len(place_ids) - 1)

    accent = _accent_cls(tag)
    for i, pid in enumerate(place_ids):
        _render_card(
            tag=tag if i == 0 else "",
            place_id=pid,
            note_override=notes[i] if i < len(notes) else None,
            show_taxi=show_taxi,
            mode=mode,
            accent_override=accent,
        )

    if others:
        first_p = PLACES[place_ids[0]]
        area = first_p.get("area")
        cat_label = {"food": "其他吃的", "shop": "其他逛的"}.get(others, "其他")
        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            # 只排除「這一格自己」的店；當天其他時段已排的會顯示在最下面標「已排」
            items = get_by_area(area, exclude=place_ids, cat=others)
            if not items:
                st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            else:
                _render_backup_list(items, _SCHEDULED.get(others, set()))


def note(tag, title, meta=None, note=None):
    """顯示一個沒有座標、沒有 G/N/T 按鈕的純說明卡。"""
    custom_card(tag=tag, title=title, meta=meta, note=note, links=None, dashed=True)


def hotel_bottom(today_food=None, today_shop=None):
    """
    每天最下面：🏠 (卡片) + 🍽️吃 (expander) + 🛍️逛 (expander)。
    today_food / today_shop 不傳的話，自動用 set_scheduled() 登記的清單。
    已排項目沉到最下面 + 標「已排」。
    """
    food_sched = set(today_food) if today_food is not None else _SCHEDULED["food"]
    shop_sched = set(today_shop) if today_shop is not None else _SCHEDULED["shop"]

    _render_card(tag="🏠", place_id="hotel", show_taxi=True)

    food_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="food")
    with st.expander("🍽️ 吃 — 飯店附近"):
        st.caption("")
        _render_backup_list(food_all, food_sched)

    shop_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="shop")
    with st.expander("🛍️ 逛 — 飯店附近"):
        st.caption("")
        _render_backup_list(shop_all, shop_sched)


# ================================================================
# 多段合併卡片：多個主要點放在同一張卡片裡，每點標題粗體
# ================================================================
def multi_card(tag, sections, others=None, show_taxi=True, mode="walking"):
    """
    把多個「主要點」合併在同一張卡片內，每點標題用粗體 (h4)，
    各自可以有 meta / note / G·N·T 按鈕，點與點之間用虛線分隔。

    sections: list[dict]，每個 dict 二選一：
      A. {"place_id": "yukmong", "note": "覆寫備註(選填)"}
         → 從 PLACES 撈名稱/⭐/meta/座標，自動產生 G/N/T 按鈕
      B. {"title": "AREX (...)", "meta": "...", "note": "...",
          "links": [{"label":"G","url":"...","cls":"g"}, ...]}
         → 自訂內容
    others: None / "food" / "shop" — 同 stop()，加「其他」expander，
            已排的沉底標「已排」。
    """
    accent = _accent_cls(tag)
    chip_html = f'<div class="chip">{html_lib.escape(tag)}</div>' if tag else '<div class="chip ghost">·</div>'

    place_ids = []
    sec_parts = []
    for s in sections:
        if "place_id" in s:
            pid = s["place_id"]
            if pid not in PLACES:
                st.error(f"❌ 找不到地點: {pid}")
                continue
            place_ids.append(pid)
            p = PLACES[pid]
            title_html = html_lib.escape(p["name"]) + ('<span class="star"> ⭐</span>' if p.get("priority") else '')
            meta = _build_meta_line(p)
            note_txt = s.get("note") if s.get("note") is not None else p.get("note", "")
            btns = _nav_btns_html(p, show_taxi=show_taxi, mode=mode)
        else:
            title_html = html_lib.escape(s.get("title", ""))
            meta = html_lib.escape(s["meta"]) if s.get("meta") else ""
            note_txt = s.get("note", "")
            btns = ""
            if s.get("links"):
                bp = []
                for item in s["links"]:
                    label = html_lib.escape(item.get("label", ""))
                    cls = html_lib.escape(item.get("cls", "g"))
                    url = _safe_href(item.get("url", "#"))
                    target = ' target="_blank"' if url.startswith("http") else ""
                    bp.append(f'<a class="nav-btn {cls}" href="{url}"{target} title="{label}">{label}</a>')
                btns = '<div class="nav-btns">' + ''.join(bp) + '</div>'

        meta_html = f'<p class="meta">{meta}</p>' if meta else ''
        note_html = f'<p class="note">{html_lib.escape(note_txt)}</p>' if note_txt else ''
        sec_parts.append(
            f'<div class="section">'
            f'<div class="top-row"><h4>{title_html}</h4>{btns}</div>'
            f'{meta_html}{note_html}'
            f'</div>'
        )

    st.markdown(
        f'<div class="stop-card {accent}">{chip_html}<div class="body">' + ''.join(sec_parts) + '</div></div>',
        unsafe_allow_html=True,
    )

    if others and place_ids:
        area = PLACES[place_ids[0]].get("area")
        cat_label = {"food": "其他吃的", "shop": "其他逛的"}.get(others, "其他")
        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            items = get_by_area(area, exclude=place_ids, cat=others)
            if not items:
                st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            else:
                _render_backup_list(items, _SCHEDULED.get(others, set()))
