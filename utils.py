"""
渲染共用函式（v9 空白修正版）：
- 保留 v8 整卡 iframe 版的所有功能
- 修正：卡片間 / 卡片與 expander 間 / expander 內卡片間的大空白
  根本原因：
    1. Streamlit stVerticalBlock 有 gap，每個 components.html iframe 都是一個 block
    2. iframe 高度估算偏大，底部留白
  解法：
    1. 用更完整的 CSS selector 壓掉 Streamlit 所有 gap 和 iframe margin（涵蓋新舊版本）
    2. 改用 ResizeObserver 精確回報 iframe 高度
    3. 初始高度估算調小，讓 ResizeObserver 校正收縮
"""
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import html as html_lib
import json

from places import PLACES, get_by_area, AREA_HONGDAE


# ================================================================
# 當天已排清單
# ================================================================
_SCHEDULED = {"food": set(), "shop": set()}


def set_scheduled(today_food=None, today_shop=None):
    _SCHEDULED["food"] = set(today_food or [])
    _SCHEDULED["shop"] = set(today_shop or [])


# ================================================================
# 類別 → 顏色
# ================================================================
_TAG_ACCENT_HEX = {
    "早": "#f59e0b",
    "午": "#f97316",
    "晚": "#ef4444",
    "宵": "#6366f1",
    "點": "#ec4899",
    "逛": "#a855f7",
    "買": "#a855f7",
    "景": "#10b981",
    "住": "#3b82f6",
}


def _accent_hex(tag):
    return _TAG_ACCENT_HEX.get(tag, "#94a3b8")


# ================================================================
# 全域 CSS — 只處理 Streamlit 框架層的間距
# ================================================================
_CSS = """
<style>
/* ── 1) 外層 Streamlit block 不用 gap，避免和 iframe / wrapper 間距疊加 ── */
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMainBlockContainer"]{
  gap:0 !important;
}

/* ── 2) iframe 本身不要額外 margin / padding / border ── */
[data-testid="stIFrame"],
[data-testid="stCustomComponentV1"],
iframe{
  display:block !important;
  margin:0 !important;
  padding:0 !important;
  border:none !important;
}

/* ── 3) 每個元素容器自己給底部間距，主畫面統一用這個控制 ── */
div.element-container,
div[data-testid="element-container"],
[data-testid="stElementContainer"]{
  margin:0 0 0.3rem 0 !important;
  padding:0 !important;
}

/* ── 4) expander 內容區域 ── */
div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
div[data-testid="stExpander"] details > div{
  max-height:320px;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
  padding:4px 6px 4px 0 !important;
}

/* ── 5) expander 裡面的 block 一樣不要 gap ── */
div[data-testid="stExpander"] [data-testid="stVerticalBlock"],
div[data-testid="stExpander"] [data-testid="stVerticalBlockBorderWrapper"]{
  gap:0 !important;
}

/* ── 6) expander 裡每個卡片的距離再小一點 ── */
div[data-testid="stExpander"] div.element-container,
div[data-testid="stExpander"] div[data-testid="element-container"],
div[data-testid="stExpander"] [data-testid="stElementContainer"]{
  margin:0 0 0.2rem 0 !important;
  padding:0 !important;
}

/* ── 7) 最後一個元素不要多留白 ── */
div.element-container:last-child,
div[data-testid="element-container"]:last-child,
[data-testid="stElementContainer"]:last-child{
  margin-bottom:0 !important;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


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
        dname = urllib.parse.quote(str(name or "목적지"))
        return f"nmap://route/{nm}?dlat={lat}&dlng={lng}&dname={dname}&appname={appname}"
    if query:
        q = urllib.parse.quote(str(query))
        return f"nmap://search?query={q}&appname={appname}"
    return f"nmap://map?appname={appname}"


def kakaot_url():
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
        return f"{name_kr}｜{meta}"
    elif name_kr:
        return name_kr
    elif meta:
        return meta
    return ""


# ================================================================
# iframe 卡片內部 CSS（深淺色自適應）
# ================================================================
_IFRAME_STYLE = """
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:transparent;overflow:hidden;}
body{font-family:-apple-system,BlinkMacSystemFont,system-ui,"Noto Sans TC","Noto Sans KR",sans-serif;}
:root{
  --bg:#f0f2f6;--text:#1a1a1a;
  --border:rgba(128,128,128,.16);
  --border-dash:rgba(128,128,128,.35);
  --section-line:rgba(128,128,128,.22);
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#262730;--text:#fafafa;
    --border:rgba(250,250,250,.16);
    --border-dash:rgba(250,250,250,.30);
    --section-line:rgba(250,250,250,.20);
  }
}
.card{
  position:relative;background:var(--bg);
  border:1px solid var(--border);border-radius:14px;
  padding:12px 14px 12px 12px;
  display:flex;align-items:flex-start;gap:11px;
  box-shadow:0 1px 4px rgba(0,0,0,.05);overflow:hidden;
}
.card.dashed{background:transparent;border:1.5px dashed var(--border-dash);box-shadow:none;}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent,#94a3b8);}
.card.dashed::before{display:none;}
.chip{
  flex-shrink:0;width:34px;height:34px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-size:15px;font-weight:800;color:#fff;background:var(--accent,#94a3b8);margin-top:1px;
}
.chip.dashed{background:rgba(128,128,128,.14);color:var(--text);}
.chip.ghost{background:transparent;color:transparent;}
.body{flex-grow:1;min-width:0;}
.section{padding:9px 0 2px 0;border-top:1px dashed var(--section-line);margin-top:7px;}
.section:first-child{border-top:none;margin-top:0;padding-top:0;}
.title-row{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;}
h4{font-size:15.5px;font-weight:700;color:var(--text);line-height:1.35;word-break:break-word;flex:1;min-width:0;margin:0;}
h5{font-size:14.5px;font-weight:700;color:var(--text);line-height:1.35;word-break:break-word;flex:1;min-width:0;margin:0;}
.meta{font-size:12px;color:var(--text);opacity:.62;margin-top:4px;line-height:1.45;}
.note{font-size:12.5px;color:var(--text);opacity:.88;margin-top:5px;line-height:1.5;}
.star{color:#ff4b4b;font-size:13px;}
.btns{display:flex;gap:6px;flex-shrink:0;align-items:center;padding-top:1px;}
.b{
  width:30px;height:30px;border-radius:50%;
  display:inline-flex;align-items:center;justify-content:center;
  font-weight:800;font-size:13.5px;text-decoration:none;border:none;cursor:pointer;
  box-shadow:0 1px 2px rgba(0,0,0,.15);
  -webkit-tap-highlight-color:transparent;user-select:none;
  font-family:-apple-system,system-ui,sans-serif;
}
.b:active{transform:scale(.92);}
.b.g{background:#4285F4;color:#fff;}
.b.n{background:#03C75A;color:#fff;}
.b.t{background:#FAE100;color:#371D1E;}
"""

# ResizeObserver 高度自動回報腳本（比 getBoundingClientRect 精準）
_HEIGHT_REPORTER = """
(function(){
  function report(){
    var h=Math.ceil(document.documentElement.scrollHeight || document.body.scrollHeight);
    window.parent.postMessage({isStreamlitMessage:true,type:"streamlit:setFrameHeight",height:h},"*");
  }
  if(window.ResizeObserver){
    new ResizeObserver(report).observe(document.body);
  }
  report();
  setTimeout(report,50);
  setTimeout(report,250);
})();
"""


def _btns_html_for_place(p, mode, show_taxi, uid):
    name = p["name"]
    name_kr = p.get("name_kr", name)
    g = _safe_href(gmap_url(f"{name_kr} {p.get('address', '')}", mode))
    n = _safe_href(naver_url(query=name_kr, lat=p.get("lat"), lng=p.get("lng"),
                             name=name_kr or name, mode=mode))
    parts = [
        f'<a class="b g" href="{g}" target="_blank" rel="noopener" title="Google Maps">G</a>',
        f'<a class="b n" href="{n}" title="NAVER">N</a>',
    ]
    if show_taxi:
        parts.append(
            f'<button class="b t" id="t_{uid}" type="button" title="複製韓文店名並開啟 Kakao T">T</button>'
        )
    return '<div class="btns">' + ''.join(parts) + '</div>'


def _btns_html_for_links(links):
    if not links:
        return ""
    parts = []
    for item in links:
        label = html_lib.escape(item.get("label", ""))
        cls = html_lib.escape(item.get("cls", "g"))
        raw_url = item.get("url", "#")
        url = _safe_href(raw_url)
        target = ' target="_blank" rel="noopener"' if str(raw_url).startswith("http") else ""
        parts.append(f'<a class="b {cls}" href="{url}"{target} title="{label}">{label}</a>')
    return '<div class="btns">' + ''.join(parts) + '</div>'


def _t_script(uid, copy_text):
    ct = json.dumps(str(copy_text))
    k = json.dumps(kakaot_url())
    return (
        f'(function(){{'
        f'var el=document.getElementById("t_{uid}");'
        f'if(!el)return;'
        f'el.addEventListener("click",async function(){{'
        f'try{{'
        f'if(navigator.clipboard&&window.isSecureContext){{await navigator.clipboard.writeText({ct});}}'
        f'else{{var ta=document.createElement("textarea");ta.value={ct};'
        f'ta.style.cssText="position:fixed;left:-9999px;top:0";'
        f'document.body.appendChild(ta);ta.focus();ta.select();'
        f'try{{document.execCommand("copy");}}catch(e){{}}document.body.removeChild(ta);}}'
        f'}}catch(e){{}}'
        f'el.innerText="\\u2713";'
        f'setTimeout(function(){{el.innerText="T";}},1000);'
        f'window.location.href={k};'
        f'}});'
        f'}})();'
    )


def _emit_card(accent_hex, inner_html, t_scripts, est_height):
    """
    把卡片 HTML + JS 包成 iframe 輸出。
    est_height 調小 → ResizeObserver 向上校正，不留下白。
    """
    all_scripts = ''.join(t_scripts) + _HEIGHT_REPORTER
    doc = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<style>{_IFRAME_STYLE}:root{{--accent:{accent_hex};}}</style>'
        '</head><body>'
        f'{inner_html}'
        f'<script>{all_scripts}</script>'
        '</body></html>'
    )
    components.html(doc, height=est_height, scrolling=False)


# ================================================================
# 卡片渲染
# ================================================================
def _render_card(tag, place_id, note_override=None, show_taxi=True, mode="walking",
                 accent_override_hex=None):
    if place_id not in PLACES:
        st.error(f"❌ 找不到地點: {place_id}")
        return

    p = PLACES[place_id]
    accent = accent_override_hex or _accent_hex(tag)
    chip = f'<div class="chip">{html_lib.escape(tag)}</div>' if tag else '<div class="chip ghost">·</div>'
    name = html_lib.escape(p["name"])
    star = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    meta = _build_meta_line(p)
    meta_html = f'<p class="meta">{html_lib.escape(meta)}</p>' if meta else ''
    note = note_override if note_override is not None else p.get("note", "")
    note_html = f'<p class="note">{html_lib.escape(note)}</p>' if note else ''

    uid = place_id.replace("-", "_")
    btns = _btns_html_for_place(p, mode, show_taxi, uid)

    inner = (
        f'<div class="card">{chip}<div class="body">'
        f'<div class="title-row"><h4>{name}{star}</h4>{btns}</div>'
        f'{meta_html}{note_html}'
        f'</div></div>'
    )
    t_scripts = [_t_script(uid, p.get("name_kr") or p["name"])] if show_taxi else []
    # 估算高度：故意偏小，讓 ResizeObserver 向上收縮而不往下撐留白
    est = 62 + (18 if meta else 0) + (38 if note else 0)
    _emit_card(accent, inner, t_scripts, est)


def custom_card(tag, title, meta=None, note=None, links=None, dashed=False):
    accent = _accent_hex(tag)
    tag_e = html_lib.escape(tag) if tag else "·"
    if dashed:
        chip = f'<div class="chip dashed">{tag_e}</div>'
        card_cls = "card dashed"
        title_tag = "h5"
    elif tag:
        chip = f'<div class="chip">{tag_e}</div>'
        card_cls = "card"
        title_tag = "h4"
    else:
        chip = '<div class="chip ghost">·</div>'
        card_cls = "card"
        title_tag = "h4"

    title_e = html_lib.escape(title)
    meta_html = f'<p class="meta">{html_lib.escape(meta)}</p>' if meta else ''
    note_html = f'<p class="note">{html_lib.escape(note)}</p>' if note else ''
    btns = _btns_html_for_links(links)

    inner = (
        f'<div class="{card_cls}">{chip}<div class="body">'
        f'<div class="title-row"><{title_tag}>{title_e}</{title_tag}>{btns}</div>'
        f'{meta_html}{note_html}'
        f'</div></div>'
    )
    est = 58 + (18 if meta else 0) + (38 if note else 0)
    _emit_card(accent, inner, [], est)


# ================================================================
# 備案 / 飯店附近清單項目
# ================================================================
def _render_backup_item(pid, p, already=False):
    accent = "#94a3b8"
    name = html_lib.escape(p["name"])
    star = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    already_tag = (
        ' <span style="font-size:10px;font-weight:700;'
        'background:rgba(255,75,75,.13);color:#ff4b4b;'
        'padding:2px 7px;border-radius:99px;white-space:nowrap;">已排</span>'
    ) if already else ''
    name_kr = p.get("name_kr", "")

    parts = []
    if p.get("sub"):
        parts.append(p["sub"])
    if p.get("hours"):
        parts.append(p["hours"])
    meta = " · ".join(parts)
    if name_kr and meta:
        meta_line = f"{name_kr}｜{meta}"
    elif name_kr:
        meta_line = name_kr
    elif meta:
        meta_line = meta
    else:
        meta_line = ""

    meta_html = f'<p class="meta">{html_lib.escape(meta_line)}</p>' if meta_line else ''
    note_html = f'<p class="note">{html_lib.escape(p.get("note", ""))}</p>' if p.get("note") else ''

    uid = ("bk_" + pid).replace("-", "_")
    btns = _btns_html_for_place(p, "walking", True, uid)

    opacity = ' style="opacity:.62"' if already else ''
    inner = (
        f'<div class="card"{opacity}><div class="chip ghost">·</div><div class="body">'
        f'<div class="title-row"><h4 style="font-size:13.5px;">{name}{star}{already_tag}</h4>{btns}</div>'
        f'{meta_html}{note_html}'
        f'</div></div>'
    )
    t_scripts = [_t_script(uid, p.get("name_kr") or p["name"])]
    est = 56 + (16 if meta_line else 0) + (36 if p.get("note") else 0)
    _emit_card(accent, inner, t_scripts, est)


def _render_backup_list(items, scheduled_ids):
    items_sorted = sorted(items, key=lambda x: (x[0] in scheduled_ids, x[0]))
    for pid, p in items_sorted:
        _render_backup_item(pid, p, already=(pid in scheduled_ids))


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

    accent = _accent_hex(tag)
    for i, pid in enumerate(place_ids):
        _render_card(
            tag=tag if i == 0 else "",
            place_id=pid,
            note_override=notes[i] if i < len(notes) else None,
            show_taxi=show_taxi,
            mode=mode,
            accent_override_hex=accent,
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
    """多個主要點合併在同一張卡片內，每點標題粗體 + 按鈕在右、虛線分段。"""
    accent = _accent_hex(tag)
    place_ids = []
    sec_parts = []
    t_scripts = []

    for idx, s in enumerate(sections):
        if "place_id" in s:
            pid = s["place_id"]
            if pid not in PLACES:
                st.error(f"❌ 找不到地點: {pid}")
                continue

            place_ids.append(pid)
            p = PLACES[pid]
            title_html = html_lib.escape(p["name"]) + (
                '<span class="star"> ⭐</span>' if p.get("priority") else ''
            )
            meta = _build_meta_line(p)
            note_txt = s.get("note") if s.get("note") is not None else p.get("note", "")
            uid = ("m_" + pid + "_" + str(idx)).replace("-", "_")
            btns = _btns_html_for_place(p, mode, show_taxi, uid)

            if show_taxi:
                t_scripts.append(_t_script(uid, p.get("name_kr") or p["name"]))

        else:
            title_html = html_lib.escape(s.get("title", ""))
            meta = s.get("meta", "")
            note_txt = s.get("note", "")
            btns = _btns_html_for_links(s.get("links"))

        meta_html = f'<p class="meta">{html_lib.escape(meta)}</p>' if meta else ''
        note_html = f'<p class="note">{html_lib.escape(note_txt)}</p>' if note_txt else ''

        sec_parts.append(
            f'<div class="section">'
            f'<div class="title-row"><h4>{title_html}</h4>{btns}</div>'
            f'{meta_html}{note_html}'
            f'</div>'
        )

    chip = f'<div class="chip">{html_lib.escape(tag)}</div>' if tag else '<div class="chip ghost">·</div>'
    inner = f'<div class="card">{chip}<div class="body">' + ''.join(sec_parts) + '</div></div>'

    # 關鍵修正：
    # 不再手動累加每段的估算高度，避免多 section 卡片被估太高，
    # 導致上下多出空白。只給一個保守初始值，交給 ResizeObserver 校正。
    est = 72 + len(sections) * 56

    _emit_card(accent, inner, t_scripts, est)

    if others and place_ids:
        area = PLACES[place_ids[0]].get("area")
        cat_label = {"food": "其他吃的", "shop": "其他逛的"}.get(others, "其他")
        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            items = get_by_area(area, exclude=place_ids, cat=others)
            if not items:
                st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            else:
                _render_backup_list(items, _SCHEDULED.get(others, set()))
