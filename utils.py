"""
渲染共用函式（v6 卡片內嵌按鈕版）：
- G / N / T 直接放在卡片內、店名右邊
- T 在 N 右邊
- 按 T：先複製韓文店名，再嘗試開啟 Kakao T
- 不再自動開 fallback 網頁，避免 iPhone 多開一個錯誤頁
- 其餘 stop / note / multi_card / hotel_bottom API 盡量維持不變
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
    """
    產生同一次 rerun 內唯一 key，避免重複元件衝突。
    """
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

.stop-card .body{
  flex-grow:1;
  min-width:0;
}

/* 店名列：左邊標題，右邊按鈕 */
.stop-card .title-row{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:8px;
  width:100%;
}
.stop-card .title-wrap{
  min-width:0;
  flex:1 1 auto;
}
.stop-card .title-wrap h4{
  margin:0;
  font-size:15.5px;
  font-weight:700;
  color:var(--text-color);
  line-height:1.35;
  word-break:break-word;
}
.stop-card .actions-wrap{
  flex:0 0 auto;
  min-width:132px;
  display:flex;
  justify-content:flex-end;
  align-items:flex-start;
  padding-top:1px;
}

.stop-card .meta{
  font-size:12px;
  color:var(--text-color);
  opacity:.62;
  margin:4px 0 0 0;
  line-height:1.45;
}
.stop-card .note{
  font-size:12.5px;
  color:var(--text-color);
  opacity:.88;
  margin:5px 0 0 0;
  line-height:1.5;
}
.stop-card .star{
  color:#ff4b4b;
  font-size:13px;
}

/* ===== 純說明卡（交通/提醒，虛線） ===== */
.note-card{
  position:relative;
  background:transparent;
  border:1.5px dashed rgba(128,128,128,.35);
  border-radius:14px;
  padding:10px 14px;
  margin:8px 0;
  display:flex;
  gap:11px;
  align-items:flex-start;
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

/* ===== G / N HTML 圓鈕 ===== */
.nav-btns{
  display:flex;
  gap:6px;
  align-items:center;
  justify-content:flex-end;
  margin-top:2px;
}
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

/* ===== 備案 / 飯店附近清單項目 ===== */
.backup-item{
  background:var(--secondary-background-color);
  border:1px solid rgba(128,128,128,.14);
  border-radius:12px;
  padding:9px 11px;
  margin:6px 2px;
  box-shadow:0 1px 2px rgba(0,0,0,.04);
}
.backup-item.scheduled{ opacity:.62; }

.backup-item .title-row{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:8px;
  width:100%;
}
.backup-item .title-wrap{
  min-width:0;
  flex:1 1 auto;
}
.backup-item .actions-wrap{
  flex:0 0 auto;
  min-width:132px;
  display:flex;
  justify-content:flex-end;
  align-items:flex-start;
  padding-top:1px;
}

.backup-item .name{
  font-size:13.5px;
  font-weight:700;
  line-height:1.35;
  word-break:break-word;
}
.backup-item .small-meta{
  font-size:11.5px;
  opacity:.65;
  margin-top:2px;
  line-height:1.4;
}
.backup-item .small-note{
  font-size:11.5px;
  opacity:.82;
  margin-top:3px;
  line-height:1.45;
}
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

/* ===== 手機微調 ===== */
@media (max-width: 640px){
  .stop-card .actions-wrap,
  .backup-item .actions-wrap{
    min-width:120px;
  }
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


def kakao_t_scheme_url():
    return "kakaot://home"


def _safe_href(url: str) -> str:
    return html_lib.escape(url, quote=True)


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


def _js_escape_text(text: str) -> str:
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", "\\n")
        .replace("\r", "")
    )


def _render_action_buttons(place, mode="walking", copy_text=None, key_prefix="btn"):
    """
    G | N | T 三顆按鈕固定同排，輸出成一個 HTML 元件。
    T：先複製韓文店名，再開啟 Kakao T。
    """
    unique = _next_key(key_prefix)
    name_kr = str(copy_text or place.get("name_kr") or place["name"])
    text_js = _js_escape_text(name_kr)

    g = _safe_href(gmap_url(f"{place.get('name_kr', place['name'])} {place.get('address', '')}", mode))
    n = _safe_href(
        naver_url(
            query=place.get("name_kr", place["name"]),
            lat=place.get("lat"),
            lng=place.get("lng"),
            name=place.get("name", place.get("name_kr", "目的地")),
            mode=mode
        )
    )
    t = kakao_t_scheme_url()

    button_id = f"btn_t_{unique}"

    html_code = f"""
    <div style="
      display:flex;
      justify-content:flex-end;
      align-items:center;
      gap:6px;
      width:132px;
      min-width:132px;
      white-space:nowrap;
      overflow:hidden;
      margin:0;
      padding:0;
    ">
      <a href="{g}" target="_blank" rel="noopener noreferrer" title="Google Maps"
         style="
           display:inline-flex; align-items:center; justify-content:center;
           width:30px; min-width:30px; height:30px; border-radius:50%;
           background:#4285F4; color:#fff; text-decoration:none;
           font-weight:800; font-size:13.5px;
           font-family:system-ui,-apple-system,sans-serif;
           box-shadow:0 1px 2px rgba(0,0,0,.15);
           flex:0 0 30px;
         ">G</a>

      <a href="{n}" title="NAVER"
         style="
           display:inline-flex; align-items:center; justify-content:center;
           width:30px; min-width:30px; height:30px; border-radius:50%;
           background:#03C75A; color:#fff; text-decoration:none;
           font-weight:800; font-size:13.5px;
           font-family:system-ui,-apple-system,sans-serif;
           box-shadow:0 1px 2px rgba(0,0,0,.15);
           flex:0 0 30px;
         ">N</a>

      <button id="{button_id}" type="button" title="Copy Korean name and open Kakao T"
         style="
           display:inline-flex; align-items:center; justify-content:center;
           width:30px; min-width:30px; height:30px; border:none; border-radius:50%;
           background:#FEE500; color:#191919;
           font-weight:800; font-size:13.5px;
           font-family:system-ui,-apple-system,sans-serif;
           box-shadow:0 1px 2px rgba(0,0,0,.15);
           cursor:pointer;
           padding:0;
           flex:0 0 30px;
         ">T</button>
    </div>

    <script>
    (function() {{
      const btn = document.getElementById('{button_id}');
      if (!btn) return;

      btn.addEventListener('click', async function() {{
        const textToCopy = '{text_js}';
        const original = btn.innerText;
        let copied = false;

        try {{
          if (navigator.clipboard && window.isSecureContext) {{
            await navigator.clipboard.writeText(textToCopy);
            copied = true;
          }} else {{
            const ta = document.createElement('textarea');
            ta.value = textToCopy;
            ta.style.position = 'fixed';
            ta.style.left = '-9999px';
            ta.style.top = '0';
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            copied = document.execCommand('copy');
            document.body.removeChild(ta);
          }}
        }} catch (e) {{
          copied = false;
        }}

        btn.innerText = copied ? '✓' : 'T';
        setTimeout(() => {{
          btn.innerText = original;
        }}, 1000);

        window.location.href = '{t}';
      }});
    }})();
    </script>
    """
    components.html(html_code, height=34, width=132)


def _render_card_inner(tag, title_html, meta_html="", note_html="", actions_html=None, accent_override=None):
    accent = accent_override or _accent_cls(tag)

    if tag:
        chip_html = f'<div class="chip">{html_lib.escape(tag)}</div>'
    else:
        chip_html = '<div class="chip ghost">·</div>'

    title_row = (
        '<div class="title-row">'
        f'<div class="title-wrap"><h4>{title_html}</h4></div>'
        f'<div class="actions-wrap">{actions_html or ""}</div>'
        '</div>'
    )

    return (
        f'<div class="stop-card {accent}">'
        f'{chip_html}'
        f'<div class="body">'
        f'{title_row}'
        f'{meta_html}'
        f'{note_html}'
        f'</div>'
        f'</div>'
    )


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

    unique_holder = f"holder_main_{_next_key(place_id)}"
    st.markdown(
        _render_card_inner(
            tag=tag,
            title_html=f"{name}{star}",
            meta_html=meta_html,
            note_html=note_html,
            actions_html=f'<div id="{unique_holder}"></div>',
            accent_override=accent_override,
        ),
        unsafe_allow_html=True,
    )

    if show_taxi:
        components.html(
            f"""
            <script>
            (function() {{
              const parentDoc = window.parent.document;
              const holder = parentDoc.getElementById('{unique_holder}');
              if (!holder) return;
            }})();
            </script>
            """,
            height=0,
        )
        _render_action_buttons(
            place=p,
            mode=mode,
            copy_text=str(p.get("name_kr") or p["name"]),
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
            parts.append(
                f'<a class="nav-btn {cls}" href="{url}"{target} title="{label}">{label}</a>'
            )
        btns_html = '<div class="nav-btns">' + ''.join(parts) + '</div>'

    st.markdown(
        (
            f'<div class="{card_class} {accent}">'
            f'{chip_html}'
            f'<div class="body">'
            f'<{title_tag}>{title_e}</{title_tag}>'
            f'{meta_html}'
            f'{note_html}'
            f'</div>'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )

    if btns_html:
        st.markdown(btns_html, unsafe_allow_html=True)


def _render_backup_item(pid, p, already=False):
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

    holder_id = f"holder_backup_{_next_key(pid)}"

    st.markdown(
        (
            f'<div class="{item_cls}">'
            f'<div class="title-row">'
            f'<div class="title-wrap"><div class="name">{name}{star}{already_tag}</div></div>'
            f'<div class="actions-wrap"><div id="{holder_id}"></div></div>'
            f'</div>'
            f'{meta_html}'
            f'{note_html}'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )

    components.html(
        f"""
        <script>
        (function() {{
          const parentDoc = window.parent.document;
          const holder = parentDoc.getElementById('{holder_id}');
          if (!holder) return;
        }})();
        </script>
        """,
        height=0,
    )

    _render_action_buttons(
        place=p,
        mode="walking",
        copy_text=str(p.get("name_kr") or p["name"]),
        key_prefix=f"backup_{pid}"
    )


def _render_backup_list(items, scheduled_ids):
    items_sorted = sorted(items, key=lambda x: (x[0] in scheduled_ids, x[0]))
    for pid, p in items_sorted:
        _render_backup_item(pid, p, already=(pid in scheduled_ids))


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


def multi_card(tag, sections, others=None, show_taxi=True, mode="walking"):
    accent = _accent_cls(tag)

    place_ids = []
    for idx, s in enumerate(sections):
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

            holder_id = f"holder_multi_{_next_key(pid)}"

            chip_html = f'<div class="chip">{html_lib.escape(tag)}</div>' if idx == 0 and tag else '<div class="chip ghost">·</div>'

            st.markdown(
                (
                    f'<div class="stop-card {accent}">'
                    f'{chip_html}'
                    f'<div class="body">'
                    f'<div class="title-row">'
                    f'<div class="title-wrap"><h4>{title_html}</h4></div>'
                    f'<div class="actions-wrap"><div id="{holder_id}"></div></div>'
                    f'</div>'
                    f'{meta_html}'
                    f'{note_html}'
                    f'</div>'
                    f'</div>'
                ),
                unsafe_allow_html=True,
            )

            components.html(
                f"""
                <script>
                (function() {{
                  const parentDoc = window.parent.document;
                  const holder = parentDoc.getElementById('{holder_id}');
                  if (!holder) return;
                }})();
                </script>
                """,
                height=0,
            )

            if show_taxi:
                _render_action_buttons(
                    place=p,
                    mode=mode,
                    copy_text=str(p.get("name_kr") or p["name"]),
                    key_prefix=f"multi_{pid}_{idx}"
                )

        else:
            title_html = html_lib.escape(s.get("title", ""))
            meta = html_lib.escape(s["meta"]) if s.get("meta") else ""
            note_txt = s.get("note", "")
            meta_html = f'<p class="meta">{meta}</p>' if meta else ''
            note_html = f'<p class="note">{html_lib.escape(note_txt)}</p>' if note_txt else ''

            chip_html = f'<div class="chip">{html_lib.escape(tag)}</div>' if idx == 0 and tag else '<div class="chip ghost">·</div>'

            st.markdown(
                (
                    f'<div class="stop-card {accent}">'
                    f'{chip_html}'
                    f'<div class="body">'
                    f'<div class="title-row">'
                    f'<div class="title-wrap"><h4>{title_html}</h4></div>'
                    f'</div>'
                    f'{meta_html}'
                    f'{note_html}'
                    f'</div>'
                    f'</div>'
                ),
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
