"""
渲染共用函式（v7 v2排版 + 穩定Kakao T功能版）：
- 保留 v2 卡片視覺排版
- G / N / T 放在店名右邊
- T：先複製韓文店名，再開 Kakao T App
- 改用 components.html() 承載按鈕列，避免 st.markdown 內嵌 script 不執行
- 不做 fallback 網頁，避免多開頁
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
    """在每天 show_day() 最開頭呼叫，登記當天主行程已排的 place_ids。"""
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
.stop-card h4{
  margin:0; font-size:15.5px; font-weight:700;
  color:var(--text-color); line-height:1.35;
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
.note-card h5{
  margin:0; font-size:14.5px; font-weight:700;
  line-height:1.35;
}
.note-card .meta{ font-size:12px; opacity:.68; margin-top:3px; line-height:1.45; }
.note-card .note{ font-size:12.5px; opacity:.86; margin-top:4px; line-height:1.5; }

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

/* ===== expander ===== */
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

/* ===== 多段卡片 ===== */
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


def _build_meta_line(place):
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


# ================================================================
# 穩定按鈕列元件
# ================================================================
def _render_nav_component(place, show_taxi=True, mode="walking", key_prefix="btn"):
    name = place["name"]
    name_kr = place.get("name_kr", name)

    g = _safe_href(gmap_url(f"{name_kr} {place.get('address', '')}", mode))
    n = _safe_href(
        naver_url(
            query=name_kr,
            lat=place.get("lat"),
            lng=place.get("lng"),
            name=name,
            mode=mode,
        )
    )
    k = _js_escape_text(kakaot_url())
    copy_text = _js_escape_text(name_kr)
    btn_id = f"kbtn_{_next_key(key_prefix)}"

    t_btn = ""
    if show_taxi:
        t_btn = f"""
        <button id="{btn_id}" type="button" title="Copy Korean name and open Kakao T"
          style="
            display:inline-flex;align-items:center;justify-content:center;
            width:30px;min-width:30px;height:30px;border-radius:50%;
            border:none;background:#FAE100;color:#371D1E;
            font-weight:800;font-size:13.5px;font-family:system-ui,-apple-system,sans-serif;
            box-shadow:0 1px 2px rgba(0,0,0,.15);cursor:pointer;padding:0;flex:0 0 30px;
          ">T</button>
        <script>
        (function(){{
          const btn = document.getElementById("{btn_id}");
          if (!btn) return;
          btn.addEventListener("click", async function(){{
            const original = btn.innerText;
            let copied = false;
            try {{
              if (navigator.clipboard && window.isSecureContext) {{
                await navigator.clipboard.writeText("{copy_text}");
                copied = true;
              }} else {{
                const ta = document.createElement("textarea");
                ta.value = "{copy_text}";
                ta.style.position = "fixed";
                ta.style.left = "-9999px";
                ta.style.top = "0";
                document.body.appendChild(ta);
                ta.focus();
                ta.select();
                copied = document.execCommand("copy");
                document.body.removeChild(ta);
              }}
            }} catch (e) {{
              copied = false;
            }}
            btn.innerText = copied ? "✓" : "T";
            setTimeout(function(){{ btn.innerText = original; }}, 1000);
            window.location.href = "{k}";
          }});
        }})();
        </script>
        """

    html_code = f"""
    <div style="
      display:flex;justify-content:flex-end;align-items:center;gap:6px;
      width:132px;min-width:132px;white-space:nowrap;overflow:hidden;margin:0;padding:0;
    ">
      <a href="{g}" target="_blank" rel="noopener noreferrer" title="Google Maps"
         style="
           display:inline-flex;align-items:center;justify-content:center;
           width:30px;min-width:30px;height:30px;border-radius:50%;
           background:#4285F4;color:#fff;text-decoration:none;
           font-weight:800;font-size:13.5px;font-family:system-ui,-apple-system,sans-serif;
           box-shadow:0 1px 2px rgba(0,0,0,.15);flex:0 0 30px;
         ">G</a>
      <a href="{n}" title="NAVER"
         style="
           display:inline-flex;align-items:center;justify-content:center;
           width:30px;min-width:30px;height:30px;border-radius:50%;
           background:#03C75A;color:#fff;text-decoration:none;
           font-weight:800;font-size:13.5px;font-family:system-ui,-apple-system,sans-serif;
           box-shadow:0 1px 2px rgba(0,0,0,.15);flex:0 0 30px;
         ">N</a>
      {t_btn}
    </div>
    """
    components.html(html_code, height=36, width=132)


# ================================================================
# 主卡片
# ================================================================
def _render_card(tag, place_id, note_override=None, show_taxi=True, mode="walking",
                 accent_override=None):
    if place_id not in PLACES:
        st.error(f"❌ 找不到地點: {place_id}")
        return

    p = PLACES[place_id]
    accent = accent_override or _accent_cls(tag)
    chip_html = f'<div class="chip">{html_lib.escape(tag)}</div>' if tag else '<div class="chip ghost">·</div>'

    name = html_lib.escape(p["name"])
    star = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    meta = _build_meta_line(p)
    note = note_override if note_override is not None else p.get("note", "")

    left, right = st.columns([12, 4], gap="small")

    with left:
        meta_html = f'<p class="meta">{meta}</p>' if meta else ''
        note_html = f'<p class="note">{html_lib.escape(note)}</p>' if note else ''
        st.markdown(
            f'<div class="stop-card {accent}">{chip_html}<div class="body"><h4>{name}{star}</h4>{meta_html}{note_html}</div></div>',
            unsafe_allow_html=True,
        )

    with right:
        _render_nav_component(
            place=p,
            show_taxi=show_taxi,
            mode=mode,
            key_prefix=f"main_{place_id}_{tag}_{mode}"
        )


def custom_card(tag, title, meta=None, note=None, links=None, dashed=False):
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
            raw_url = item.get("url", "#")
            url = _safe_href(raw_url)
            target = ' target="_blank" rel="noopener noreferrer"' if str(raw_url).startswith("http") else ""
            parts.append(f'<a class="nav-btn {cls}" href="{url}"{target} title="{label}">{label}</a>')
        btns_html = '<div class="nav-btns">' + ''.join(parts) + '</div>'

    st.markdown(
        f'<div class="{card_class} {accent}">{chip_html}<div class="body"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px;"><{title_tag} style="margin:0;flex:1;min-width:0;">{title_e}</{title_tag}>{btns_html}</div>{meta_html}{note_html}</div></div>',
        unsafe_allow_html=True,
    )


# ================================================================
# 備案清單
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
    item_cls = "backup-item scheduled" if already else "backup-item"

    left, right = st.columns([12, 4], gap="small")

    with left:
        st.markdown(
            f'<div class="{item_cls}"><div class="info"><div class="name">{name}{star}{already_tag}</div>{meta_html}{note_html}</div></div>',
            unsafe_allow_html=True,
        )

    with right:
        _render_nav_component(
            place=p,
            show_taxi=True,
            mode="walking",
            key_prefix=f"backup_{p.get('name', 'x')}"
        )


def _render_backup_list(items, scheduled_ids):
    items_sorted = sorted(items, key=lambda x: (x[0] in scheduled_ids, x[0]))
    for pid, p in items_sorted:
        _render_backup_item(p, already=(pid in scheduled_ids))


# ================================================================
# 公開 API
# ================================================================
def stop(tag, place_ids, others=None, notes=None, show_taxi=True, mode="walking"):
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
    custom_card(tag=tag, title=title, meta=meta, note=note, links=None, dashed=True)


def hotel_bottom(today_food=None, today_shop=None):
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
# 多段卡片
# ================================================================
def multi_card(tag, sections, others=None, show_taxi=True, mode="walking"):
    accent = _accent_cls(tag)
    place_ids = []

    for idx, s in enumerate(sections):
        left, right = st.columns([12, 4], gap="small")

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

            meta_html = f'<p class="meta">{meta}</p>' if meta else ''
            note_html = f'<p class="note">{html_lib.escape(note_txt)}</p>' if note_txt else ''
            chip_html = f'<div class="chip">{html_lib.escape(tag)}</div>' if idx == 0 and tag else '<div class="chip ghost">·</div>'

            with left:
                st.markdown(
                    f'<div class="stop-card {accent}">{chip_html}<div class="body"><h4>{title_html}</h4>{meta_html}{note_html}</div></div>',
                    unsafe_allow_html=True,
                )

            with right:
                _render_nav_component(
                    place=p,
                    show_taxi=show_taxi,
                    mode=mode,
                    key_prefix=f"multi_{pid}_{idx}"
                )

        else:
            title_html = html_lib.escape(s.get("title", ""))
            meta = html_lib.escape(s["meta"]) if s.get("meta") else ""
            note_txt = s.get("note", "")
            meta_html = f'<p class="meta">{meta}</p>' if meta else ''
            note_html = f'<p class="note">{html_lib.escape(note_txt)}</p>' if note_txt else ''
            chip_html = f'<div class="chip">{html_lib.escape(tag)}</div>' if idx == 0 and tag else '<div class="chip ghost">·</div>'

            with left:
                st.markdown(
                    f'<div class="stop-card {accent}">{chip_html}<div class="body"><h4>{title_html}</h4>{meta_html}{note_html}</div></div>',
                    unsafe_allow_html=True,
                )

            with right:
                if s.get("links"):
                    parts = []
                    for item in s["links"]:
                        label = html_lib.escape(item.get("label", ""))
                        cls = html_lib.escape(item.get("cls", "g"))
                        raw_url = item.get("url", "#")
                        url = _safe_href(raw_url)
                        target = ' target="_blank" rel="noopener noreferrer"' if str(raw_url).startswith("http") else ""
                        parts.append(f'<a class="nav-btn {cls}" href="{url}"{target} title="{label}">{label}</a>')
                    st.markdown('<div class="nav-btns">' + ''.join(parts) + '</div>', unsafe_allow_html=True)

    if others and place_ids:
        area = PLACES[place_ids[0]].get("area")
        cat_label = {"food": "其他吃的", "shop": "其他逛的"}.get(others, "其他")
        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            items = get_by_area(area, exclude=place_ids, cat=others)
            if not items:
                st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            else:
                _render_backup_list(items, _SCHEDULED.get(others, set()))
