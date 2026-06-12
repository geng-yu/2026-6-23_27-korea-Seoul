"""
渲染共用函式（v2 卡片版 + Kakao T 功能修正版）：
- 保留 v2 排版：G / N / T 在店名右邊
- T 按鈕：先複製韓文店名，再嘗試開啟 Kakao T App
- 不做 fallback 網頁，避免多開頁
- 所有 HTML 盡量維持單行串接，避免被 Markdown 當成 code block
"""
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import html as html_lib

from places import PLACES, get_by_area, AREA_HONGDAE


# ================================================================
# 當天已排清單（每次 rerun 由 day 檔重新登記）
# ================================================================
_SCHEDULED = {"food": set(), "shop": set()}
_RENDER_SEQ = 0


def set_scheduled(today_food=None, today_shop=None):
    """在每天 show_day() 最開頭呼叫，登記當天主行程已排的 place_ids。
    之後所有「其他吃的/逛的」expander 都會自動把這些項目排到最後並標「已排」。"""
    _SCHEDULED["food"] = set(today_food or [])
    _SCHEDULED["shop"] = set(today_shop or [])


def _next_key(prefix: str) -> str:
    global _RENDER_SEQ
    _RENDER_SEQ += 1
    return f"{prefix}_{_RENDER_SEQ}"


# ================================================================
# 全域 CSS
# ================================================================
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
.acc-morning{ --card-accent:#f59e0b; }
.acc-lunch  { --card-accent:#f97316; }
.acc-dinner { --card-accent:#ef4444; }
.acc-night  { --card-accent:#6366f1; }
.acc-snack  { --card-accent:#ec4899; }
.acc-shop   { --card-accent:#a855f7; }
.acc-sight  { --card-accent:#10b981; }
.acc-stay   { --card-accent:#3b82f6; }
.acc-move   { --card-accent:#94a3b8; }

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
  border:none;
}
.nav-btn:active{ transform:scale(.92); }
.nav-btn.g{ background:#4285F4; color:#fff !important; }
.nav-btn.n{ background:#03C75A; color:#fff !important; }
.nav-btn.t{ background:#FAE100; color:#371D1E !important; cursor:pointer; }

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
    return "kakaot://home"


def _safe_href(url: str) -> str:
    return html_lib.escape(url, quote=True)


def _js_escape_text(text: str) -> str:
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "")
    )


# ================================================================
# HTML / JS 片段建構器
# ================================================================
def _nav_btns_html(place, show_taxi=True, mode="walking", key_prefix="btn"):
    name = place["name"]
    name_kr = place.get("name_kr", name)
    lat = place.get("lat")
    lng = place.get("lng")

    g = _safe_href(gmap_url(f"{name_kr} {place.get('address', '')}", mode))
    n = _safe_href(naver_url(query=name_kr, lat=lat, lng=lng, name=name, mode=mode))

    parts = [
        f'<a class="nav-btn g" href="{g}" target="_blank" rel="noopener noreferrer" title="Google Maps">G</a>',
        f'<a class="nav-btn n" href="{n}" title="NAVER">N</a>',
    ]

    if show_taxi:
        btn_id = f'kakao_btn_{_next_key(key_prefix)}'
        copy_text = _js_escape_text(name_kr)
        kakao_href = _js_escape_text(kakaot_url())
        parts.append(
            f'<button id="{btn_id}" class="nav-btn t" type="button" title="Copy Korean name and open Kakao T">T</button>'
            f'<script>'
            f'(function(){{'
            f'var btn=document.getElementById("{btn_id}");'
            f'if(!btn) return;'
            f'btn.addEventListener("click", async function(){{'
            f'var textToCopy="{copy_text}";'
            f'var original=btn.innerText;'
            f'var copied=false;'
            f'try{{'
            f'if(navigator.clipboard && window.isSecureContext){{'
            f'await navigator.clipboard.writeText(textToCopy);'
            f'copied=true;'
            f'}}else{{'
            f'var ta=document.createElement("textarea");'
            f'ta.value=textToCopy;'
            f'ta.style.position="fixed";'
            f'ta.style.left="-9999px";'
            f'ta.style.top="0";'
            f'document.body.appendChild(ta);'
            f'ta.focus();'
            f'ta.select();'
            f'copied=document.execCommand("copy");'
            f'document.body.removeChild(ta);'
            f'}}'
            f'}}catch(e){{copied=false;}}'
            f'btn.innerText=copied ? "✓" : "T";'
            f'setTimeout(function(){{btn.innerText=original;}},1000);'
            f'window.location.href="{kakao_href}";'
            f'}});'
            f'}})();'
            f'</script>'
        )

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

    btns = _nav_btns_html(p, show_taxi=show_taxi, mode=mode, key_prefix=f"main_{place_id}")

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
            target = ' target="_blank" rel="noopener noreferrer"' if str(item.get("url", "#")).startswith("http") else ""
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
    btns = _nav_btns_html(p, show_taxi=True, mode="walking", key_prefix=f"backup_{p.get('name','x')}")
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
    每天最下面：住 (卡片) + 🍽️吃 (expander) + 🛍️逛 (expander)。
    """
    food_sched = set(today_food) if today_food is not None else _SCHEDULED["food"]
    shop_sched = set(today_shop) if today_shop is not None else _SCHEDULED["shop"]

    _render_card(tag="住", place_id="hotel", show_taxi=True)

    food_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="food")
    with st.expander("🍽️ 吃 — 飯店附近"):
        st.caption("弘대區所有吃的清單。主行程已排的會放最下面標「已排」。")
        _render_backup_list(food_all, food_sched)

    shop_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="shop")
    with st.expander("🛍️ 逛 — 飯店附近"):
        st.caption("弘대區所有逛的清單。主行程已排的會放最下面標「已排」。")
        _render_backup_list(shop_all, shop_sched)


# ================================================================
# 多段合併卡片：多個主要點放在同一張卡片裡，每點標題粗體
# ================================================================
def multi_card(tag, sections, others=None, show_taxi=True, mode="walking"):
    """
    把多個主要點合併在同一張卡片內，每點標題用粗體 (h4)，
    各自可以有 meta / note / G·N·T 按鈕，點與點之間用虛線分隔。
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
            btns = _nav_btns_html(p, show_taxi=show_taxi, mode=mode, key_prefix=f"multi_{pid}")
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
                    target = ' target="_blank" rel="noopener noreferrer"' if str(item.get("url", "#")).startswith("http") else ""
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
