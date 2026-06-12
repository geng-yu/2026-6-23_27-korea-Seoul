"""
渲染共用函式（v11 主行程原生排版 + 備案 iframe 版）

設計：
- 主行程：改用原生 Streamlit 排版，避免 iframe 高度 / 間距問題
- 備案 / 飯店附近 expander：維持 iframe 卡片版
- G / N / T：主行程直接放店名旁或下一行，不強求卡片右上角
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
    "🚗": "#64748b",
    "✈️": "#64748b",
    "🚆": "#64748b",
    "🛒": "#a855f7",
    "🍗": "#6366f1",
}


def _accent_hex(tag):
    return _TAG_ACCENT_HEX.get(tag, "#94a3b8")


# ================================================================
# 全域 CSS
# ================================================================
_CSS = """
<style>
/* 主畫面基本間距 */
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMainBlockContainer"]{
  gap:0 !important;
}

[data-testid="stIFrame"],
[data-testid="stCustomComponentV1"],
iframe{
  display:block !important;
  margin:0 !important;
  padding:0 !important;
  border:none !important;
}

div.element-container,
div[data-testid="element-container"],
[data-testid="stElementContainer"]{
  margin:0 0 0.28rem 0 !important;
  padding:0 !important;
}

div[data-testid="stExpander"]{
  margin:0.18rem 0 0.34rem 0 !important;
}

div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
div[data-testid="stExpander"] details > div{
  max-height:320px;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
  padding:4px 6px 4px 0 !important;
}

div[data-testid="stExpander"] [data-testid="stVerticalBlock"],
div[data-testid="stExpander"] [data-testid="stVerticalBlockBorderWrapper"]{
  gap:0 !important;
}

div[data-testid="stExpander"] div.element-container,
div[data-testid="stExpander"] div[data-testid="element-container"],
div[data-testid="stExpander"] [data-testid="stElementContainer"]{
  margin:0 0 0.2rem 0 !important;
  padding:0 !important;
}

div[data-testid="stExpander"] div.element-container:last-child,
div[data-testid="stExpander"] div[data-testid="element-container"]:last-child,
div[data-testid="stExpander"] [data-testid="stElementContainer"]:last-child{
  margin-bottom:0 !important;
}

/* 主行程原生卡片 */
.trip-card{
  position:relative;
  background:#f0f2f6;
  border:1px solid rgba(128,128,128,.16);
  border-radius:14px;
  padding:12px 14px 12px 12px;
  box-shadow:0 1px 4px rgba(0,0,0,.05);
  overflow:hidden;
}
.trip-card::before{
  content:"";
  position:absolute;
  left:0; top:0; bottom:0;
  width:4px;
  background:var(--accent, #94a3b8);
}
.trip-card.dashed{
  background:transparent;
  border:1.5px dashed rgba(128,128,128,.35);
  box-shadow:none;
}
.trip-card.dashed::before{
  display:none;
}
.trip-row{
  display:flex;
  align-items:flex-start;
  gap:11px;
}
.trip-chip{
  flex-shrink:0;
  width:34px;
  height:34px;
  border-radius:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:15px;
  font-weight:800;
  color:#fff;
  background:var(--accent, #94a3b8);
  margin-top:1px;
}
.trip-chip.ghost{
  background:transparent;
  color:transparent;
}
.trip-chip.dashed{
  background:rgba(128,128,128,.14);
  color:#1a1a1a;
}
.trip-body{
  min-width:0;
  flex:1;
}
.trip-title{
  font-size:15.5px;
  font-weight:700;
  line-height:1.35;
  color:#1a1a1a;
  margin:0;
}
.trip-title.small{
  font-size:14.5px;
}
.trip-meta{
  font-size:12px;
  color:rgba(26,26,26,.68);
  line-height:1.45;
  margin-top:4px;
}
.trip-note{
  font-size:12.5px;
  color:rgba(26,26,26,.9);
  line-height:1.5;
  margin-top:5px;
}
.trip-links{
  font-size:12.5px;
  line-height:1.45;
  margin-top:5px;
}
.trip-links a{
  text-decoration:none;
}
.trip-links a:hover{
  text-decoration:underline;
}
.trip-section{
  margin-top:10px;
  padding-top:8px;
  border-top:1px dashed rgba(128,128,128,.20);
}
.trip-section:first-child{
  margin-top:0;
  padding-top:0;
  border-top:none;
}
.trip-star{
  color:#ff4b4b;
  font-size:13px;
}

@media (prefers-color-scheme: dark){
  .trip-card{
    background:#262730;
    border-color:rgba(250,250,250,.16);
  }
  .trip-card.dashed{
    border-color:rgba(250,250,250,.30);
  }
  .trip-chip.dashed{
    background:rgba(250,250,250,.12);
    color:#fafafa;
  }
  .trip-title{ color:#fafafa; }
  .trip-meta{ color:rgba(250,250,250,.68); }
  .trip-note{ color:rgba(250,250,250,.9); }
  .trip-section{ border-top:1px dashed rgba(250,250,250,.20); }
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
# iframe 卡片（只給備案 / expander 用）
# ================================================================
_IFRAME_STYLE = """
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:transparent;overflow:hidden;}
body{font-family:-apple-system,BlinkMacSystemFont,system-ui,"Noto Sans TC","Noto Sans KR",sans-serif;}
:root{
  --bg:#f0f2f6;--text:#1a1a1a;
  --border:rgba(128,128,128,.16);
  --border-dash:rgba(128,128,128,.35);
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#262730;--text:#fafafa;
    --border:rgba(250,250,250,.16);
    --border-dash:rgba(250,250,250,.30);
  }
}
.card{
  position:relative;
  background:var(--bg);
  border:1px solid var(--border);
  border-radius:14px;
  padding:12px 14px 12px 12px;
  display:flex;
  align-items:flex-start;
  gap:11px;
  box-shadow:0 1px 4px rgba(0,0,0,.05);
  overflow:hidden;
}
.card::before{
  content:"";
  position:absolute;
  left:0;top:0;bottom:0;
  width:4px;
  background:var(--accent,#94a3b8);
}
.chip{
  flex-shrink:0;width:34px;height:34px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-size:15px;font-weight:800;color:#fff;background:var(--accent,#94a3b8);margin-top:1px;
}
.chip.ghost{background:transparent;color:transparent;}
.body{flex-grow:1;min-width:0;}
.title-row{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;}
h4{font-size:13.5px;font-weight:700;color:var(--text);line-height:1.35;word-break:break-word;flex:1;min-width:0;margin:0;}
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

_HEIGHT_REPORTER = """
(function(){
  function getHeight(){
    const body = document.body;
    const html = document.documentElement;
    const h = Math.max(
      body.scrollHeight,
      body.offsetHeight,
      body.getBoundingClientRect().height,
      html.scrollHeight,
      html.offsetHeight,
      html.clientHeight,
      html.getBoundingClientRect().height
    );
    return Math.ceil(h) + 6;
  }
  function report(){
    const h = getHeight();
    window.parent.postMessage(
      {isStreamlitMessage:true, type:"streamlit:setFrameHeight", height:h},
      "*"
    );
  }
  if (window.ResizeObserver) {
    const ro = new ResizeObserver(function(){ report(); });
    ro.observe(document.body);
    ro.observe(document.documentElement);
  }
  window.addEventListener("load", report);
  window.addEventListener("resize", report);
  setTimeout(report, 50);
  setTimeout(report, 150);
  setTimeout(report, 300);
})();
"""


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
        f'else{{'
        f'var ta=document.createElement("textarea");'
        f'ta.value={ct};'
        f'ta.style.cssText="position:fixed;left:-9999px;top:0";'
        f'document.body.appendChild(ta);'
        f'ta.focus();ta.select();'
        f'try{{document.execCommand("copy");}}catch(e){{}}'
        f'document.body.removeChild(ta);'
        f'}}'
        f'}}catch(e){{}}'
        f'el.innerText="\\u2713";'
        f'setTimeout(function(){{el.innerText="T";}},1000);'
        f'window.location.href={k};'
        f'}});'
        f'}})();'
    )


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


def _emit_card(accent_hex, inner_html, t_scripts, est_height):
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
# 原生主行程渲染
# ================================================================
def _render_inline_links(links):
    if not links:
        return ""
    parts = []
    for item in links:
        label = html_lib.escape(item.get("label", ""))
        raw_url = item.get("url", "#")
        url = _safe_href(raw_url)
        target = ' target="_blank" rel="noopener"' if str(raw_url).startswith("http") else ""
        parts.append(f'<a href="{url}"{target}>[{label}]</a>')
    return " ".join(parts)


def _render_place_links(place, mode="walking", show_taxi=True):
    name = place["name"]
    name_kr = place.get("name_kr", name)

    links = [
        {"label": "G", "url": gmap_url(f"{name_kr} {place.get('address', '')}", mode)},
        {"label": "N", "url": naver_url(query=name_kr, lat=place.get("lat"), lng=place.get("lng"),
                                        name=name_kr or name, mode=mode)},
    ]
    if show_taxi:
        # 原生排版不做複製 JS，直接開 Kakao T
        links.append({"label": "T", "url": kakaot_url()})
    return _render_inline_links(links)


def _render_native_card(tag, title, meta=None, note=None, links_html=None, dashed=False):
    accent = _accent_hex(tag)
    chip_text = html_lib.escape(tag) if tag else "·"
    chip_cls = "trip-chip dashed" if dashed else ("trip-chip" if tag else "trip-chip ghost")
    card_cls = "trip-card dashed" if dashed else "trip-card"

    title_tag_cls = "trip-title small" if dashed else "trip-title"

    html = f'''
    <div class="{card_cls}" style="--accent:{accent};">
      <div class="trip-row">
        <div class="{chip_cls}">{chip_text}</div>
        <div class="trip-body">
          <div class="{title_tag_cls}">{html_lib.escape(title)}</div>
          {f'<div class="trip-meta">{html_lib.escape(meta)}</div>' if meta else ''}
          {f'<div class="trip-note">{html_lib.escape(note)}</div>' if note else ''}
          {f'<div class="trip-links">{links_html}</div>' if links_html else ''}
        </div>
      </div>
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)


def _render_native_place_card(tag, place_id, note_override=None, show_taxi=True, mode="walking",
                              accent_override_hex=None):
    if place_id not in PLACES:
        st.error(f"❌ 找不到地點: {place_id}")
        return

    p = PLACES[place_id]
    title = p["name"] + (" ⭐" if p.get("priority") else "")
    meta = _build_meta_line(p)
    note = note_override if note_override is not None else p.get("note", "")
    links_html = _render_place_links(p, mode=mode, show_taxi=show_taxi)

    accent = accent_override_hex or _accent_hex(tag)
    chip_text = html_lib.escape(tag) if tag else "·"
    chip_cls = "trip-chip" if tag else "trip-chip ghost"

    html = f'''
    <div class="trip-card" style="--accent:{accent};">
      <div class="trip-row">
        <div class="{chip_cls}">{chip_text}</div>
        <div class="trip-body">
          <div class="trip-title">{html_lib.escape(title)}</div>
          {f'<div class="trip-meta">{html_lib.escape(meta)}</div>' if meta else ''}
          {f'<div class="trip-note">{html_lib.escape(note)}</div>' if note else ''}
          <div class="trip-links">{links_html}</div>
        </div>
      </div>
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)


def _render_native_multi_card(tag, sections, show_taxi=True, mode="walking"):
    accent = _accent_hex(tag)
    chip_text = html_lib.escape(tag) if tag else "·"
    chip_cls = "trip-chip" if tag else "trip-chip ghost"

    sec_html = []
    for s in sections:
        if "place_id" in s:
            pid = s["place_id"]
            if pid not in PLACES:
                st.error(f"❌ 找不到地點: {pid}")
                continue

            p = PLACES[pid]
            title = p["name"] + (" ⭐" if p.get("priority") else "")
            meta = _build_meta_line(p)
            note_txt = s.get("note") if s.get("note") is not None else p.get("note", "")
            links_html = _render_place_links(p, mode=mode, show_taxi=show_taxi)
        else:
            title = s.get("title", "")
            meta = s.get("meta", "")
            note_txt = s.get("note", "")
            links_html = _render_inline_links(s.get("links"))

        sec_html.append(
            f'''
            <div class="trip-section">
              <div class="trip-title">{html_lib.escape(title)}</div>
              {f'<div class="trip-meta">{html_lib.escape(meta)}</div>' if meta else ''}
              {f'<div class="trip-note">{html_lib.escape(note_txt)}</div>' if note_txt else ''}
              {f'<div class="trip-links">{links_html}</div>' if links_html else ''}
            </div>
            '''
        )

    html = f'''
    <div class="trip-card" style="--accent:{accent};">
      <div class="trip-row">
        <div class="{chip_cls}">{chip_text}</div>
        <div class="trip-body">
          {''.join(sec_html)}
        </div>
      </div>
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)


# ================================================================
# 備案 / 飯店附近清單項目（iframe 保留）
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
        f'<div class="title-row"><h4>{name}{star}{already_tag}</h4>{btns}</div>'
        f'{meta_html}{note_html}'
        f'</div></div>'
    )

    t_scripts = [_t_script(uid, p.get("name_kr") or p["name"])]
    est = 72 + (18 if meta_line else 0) + (42 if p.get("note") else 0)
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
        _render_native_place_card(
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
    _render_native_card(tag=tag, title=title, meta=meta, note=note, links_html=None, dashed=True)


def custom_card(tag, title, meta=None, note=None, links=None, dashed=False):
    links_html = _render_inline_links(links)
    _render_native_card(tag=tag, title=title, meta=meta, note=note, links_html=links_html, dashed=dashed)


def hotel_bottom(today_food=None, today_shop=None):
    food_sched = set(today_food) if today_food is not None else _SCHEDULED["food"]
    shop_sched = set(today_shop) if today_shop is not None else _SCHEDULED["shop"]

    _render_native_place_card(tag="住", place_id="hotel", show_taxi=True)

    food_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="food")
    with st.expander("🍽️ 吃 — 飯店附近"):
        st.caption("弘대區所有吃的清單。主行程已排的會放最下面標「已排」。")
        _render_backup_list(food_all, food_sched)

    shop_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="shop")
    with st.expander("🛍️ 逛 — 飯店附近"):
        st.caption("弘대區所有逛的清單。主行程已排的會放最下面標「已排」。")
        _render_backup_list(shop_all, shop_sched)


def multi_card(tag, sections, others=None, show_taxi=True, mode="walking"):
    _render_native_multi_card(tag=tag, sections=sections, show_taxi=show_taxi, mode=mode)

    place_ids = [s["place_id"] for s in sections if "place_id" in s and s["place_id"] in PLACES]
    if others and place_ids:
        area = PLACES[place_ids[0]].get("area")
        cat_label = {"food": "其他吃的", "shop": "其他逛的"}.get(others, "其他")

        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            items = get_by_area(area, exclude=place_ids, cat=others)
            if not items:
                st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            else:
                _render_backup_list(items, _SCHEDULED.get(others, set()))
