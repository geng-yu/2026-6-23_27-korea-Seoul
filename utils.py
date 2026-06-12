"""
渲染共用函式（v12 名古屋風純排版版）：

設計
--------------------------------------------------------------
* 主行程：完全用 Streamlit 原生元件「一行一行往下排」
  - st.subheader / st.markdown / st.link_button / st.divider / st.expander
  - 沒有卡片框、沒有 iframe（除了 T 按鈕本身）→ 完全沒有間距問題
* G / N：用 st.link_button 直接導向 Google Maps / NAVER scheme
* T：用一個 30×34 的小 inline iframe 嵌在按鈕列裡
  - 這是唯一的 iframe，固定高度，不會造成版面問題
  - 功能完整：點 T → 複製韓文店名 → 開 Kakao T
* 下拉框（其他吃的/逛的、飯店附近）：用同一套排版，每項用 markdown 列出
  - 已排項目沉到最下面 + 標「已排」徽章
* set_scheduled / stop / note / custom_card / multi_card / hotel_bottom
  API 全部保留，day1~5.py 不用改

T 功能說明
- 點 T 會：(1) 複製韓文店名到剪貼簿 (2) 開 Kakao T (kakaot://home)
- 如果不需要複製功能，可以把 _render_t_button() 整個換成一個 st.link_button
"""
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
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
# 連結
# ================================================================
def gmap_url(query, mode="walking"):
    q = urllib.parse.quote(str(query))
    return f"https://www.google.com/maps/dir/?api=1&destination={q}&travelmode={mode}"


def naver_url(query=None, lat=None, lng=None, name=None, mode="walking"):
    appname = "seoul_trip_2026"
    nm = {"walking": "walk", "driving": "car", "transit": "public"}.get(mode, "walk")
    if lat is not None and lng is not None:
        dname = urllib.parse.quote(str(name or "목적지"))
        return f"nmap://route/{nm}?dlat={lat}&dlng={lng}&dname={dname}&appname={appname}"
    if query:
        q = urllib.parse.quote(str(query))
        return f"nmap://search?query={q}&appname={appname}"
    return f"nmap://map?appname={appname}"


def kakaot_url():
    return "kakaot://home"


# ================================================================
# 全域 CSS — 只做小幅度按鈕外觀微調，不動 Streamlit 結構
# ================================================================
_CSS = """
<style>
/* st.link_button 微調：讓它更小巧，跟名古屋一樣 */
button[kind="secondary"], a[data-testid="stBaseLinkButton-secondary"]{
  padding:0.25rem 0.7rem !important;
  font-size:0.85rem !important;
  min-height:auto !important;
}
/* expander 內容區域：固定高度 + 上下滑動 */
div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
div[data-testid="stExpander"] details > div{
  max-height:360px;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
}
/* 主行程地點區塊之間的留白 */
.stop-block{
  margin-bottom:0.6rem;
}
.stop-title{
  font-size:1.05rem;
  font-weight:700;
  margin:0.3rem 0 0.2rem 0;
}
.stop-meta{
  font-size:0.82rem;
  color:rgba(128,128,128,1);
  margin:0 0 0.2rem 0;
  line-height:1.5;
}
.stop-note{
  font-size:0.86rem;
  margin:0.15rem 0 0.4rem 0;
  line-height:1.55;
}
.tag-emoji{
  font-size:1.1rem;
  margin-right:6px;
}
.star{color:#ff4b4b;}
.already-tag{
  display:inline-block;
  font-size:0.7rem;
  font-weight:700;
  background:rgba(255,75,75,.13);
  color:#ff4b4b;
  padding:1px 7px;
  border-radius:99px;
  margin-left:6px;
  vertical-align:middle;
  white-space:nowrap;
}
.backup-row{
  padding:0.3rem 0;
  border-bottom:1px dashed rgba(128,128,128,.18);
}
.backup-row:last-child{ border-bottom:none; }
.backup-row.scheduled{ opacity:.6; }
.backup-name{
  font-weight:700;
  font-size:0.92rem;
}
.backup-meta{
  font-size:0.78rem;
  opacity:.66;
  margin-top:2px;
  line-height:1.45;
}
.backup-note{
  font-size:0.8rem;
  opacity:.86;
  margin-top:3px;
  line-height:1.5;
}
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


# ================================================================
# T 按鈕（複製 + 開 app）—— 唯一的小 iframe
# ================================================================
_T_UID = [0]


def _render_t_button(copy_text: str):
    """渲染一個 30x30 的 T 按鈕（內含複製＋開 Kakao T 邏輯）。
    如果不需要這個功能，可以改成 st.link_button("T", kakaot_url()) 或直接拿掉。"""
    _T_UID[0] += 1
    uid = f"t{_T_UID[0]}"
    ct = json.dumps(str(copy_text))
    k = json.dumps(kakaot_url())
    doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{background:transparent;overflow:hidden;}}
button{{
  width:30px;height:30px;border-radius:50%;
  display:inline-flex;align-items:center;justify-content:center;
  font-weight:800;font-size:13.5px;
  border:none;cursor:pointer;
  background:#FAE100;color:#371D1E;
  box-shadow:0 1px 2px rgba(0,0,0,.15);
  -webkit-tap-highlight-color:transparent;user-select:none;
  font-family:-apple-system,system-ui,sans-serif;
}}
button:active{{transform:scale(.92);}}
</style></head><body>
<button id="b" type="button" title="複製韓文店名並開啟 Kakao T">T</button>
<script>
var el=document.getElementById("b");
el.addEventListener("click",async function(){{
  try{{
    if(navigator.clipboard&&window.isSecureContext){{
      await navigator.clipboard.writeText({ct});
    }} else {{
      var ta=document.createElement("textarea");
      ta.value={ct};
      ta.style.cssText="position:fixed;left:-9999px;top:0";
      document.body.appendChild(ta);ta.focus();ta.select();
      try{{document.execCommand("copy");}}catch(e){{}}
      document.body.removeChild(ta);
    }}
  }}catch(e){{}}
  el.innerText="\\u2713";
  setTimeout(function(){{el.innerText="T";}},1000);
  window.location.href={k};
}});
</script></body></html>"""
    components.html(doc, height=34, width=34)


# ================================================================
# 共用：標題列（emoji 標籤 + 店名 + ⭐）
# ================================================================
def _title_line(tag, name, star=False, small=False):
    star_html = '<span class="star"> ⭐</span>' if star else ''
    tag_html = f'<span class="tag-emoji">{tag}</span>' if tag else ''
    size = "1rem" if small else "1.05rem"
    st.markdown(
        f'<div class="stop-title" style="font-size:{size};">{tag_html}{name}{star_html}</div>',
        unsafe_allow_html=True,
    )


def _meta_line(text):
    if text:
        st.markdown(f'<div class="stop-meta">{text}</div>', unsafe_allow_html=True)


def _note_line(text):
    if text:
        st.markdown(f'<div class="stop-note">{text}</div>', unsafe_allow_html=True)


def _build_meta(place):
    name_kr = place.get("name_kr", "")
    parts = []
    if place.get("sub"): parts.append(place["sub"])
    if place.get("hours"): parts.append(place["hours"])
    m = " · ".join(parts)
    if name_kr and m: return f"{name_kr}｜{m}"
    elif name_kr: return name_kr
    elif m: return m
    return ""


# ================================================================
# 主行程：按鈕列（G | N | T 並排）
# ================================================================
def _render_buttons_for_place(p, mode="walking", show_taxi=True):
    """在地點下面排一列 G / N / T 按鈕（全部 markdown 連結，橫向 inline）。
    T 變成普通連結直接開 Kakao T；複製韓文店名功能改成「點 N 之前先長按店名複製」。
    如果想要回「點 T 自動複製」功能，把 _render_buttons_for_place 換成舊版（內含 _render_t_button）。"""
    name_kr = p.get("name_kr", p["name"])
    g = gmap_url(f"{name_kr} {p.get('address','')}", mode)
    n = naver_url(query=name_kr, lat=p.get("lat"), lng=p.get("lng"),
                  name=name_kr or p["name"], mode=mode)
    k = kakaot_url()

    parts = [
        '<div style="display:flex;gap:6px;align-items:center;margin:2px 0 6px 0;flex-wrap:wrap;">',
        f'<a href="{g}" target="_blank" rel="noopener" '
        'style="display:inline-flex;align-items:center;justify-content:center;'
        'width:30px;height:30px;border-radius:50%;background:#4285F4;color:#fff !important;'
        'font-weight:800;font-size:13.5px;text-decoration:none;box-shadow:0 1px 2px rgba(0,0,0,.15);">G</a>',
        f'<a href="{n}" '
        'style="display:inline-flex;align-items:center;justify-content:center;'
        'width:30px;height:30px;border-radius:50%;background:#03C75A;color:#fff !important;'
        'font-weight:800;font-size:13.5px;text-decoration:none;box-shadow:0 1px 2px rgba(0,0,0,.15);">N</a>',
    ]
    if show_taxi:
        parts.append(
            f'<a href="{k}" '
            'style="display:inline-flex;align-items:center;justify-content:center;'
            'width:30px;height:30px;border-radius:50%;background:#FAE100;color:#371D1E !important;'
            'font-weight:800;font-size:13.5px;text-decoration:none;box-shadow:0 1px 2px rgba(0,0,0,.15);">T</a>'
        )
        # 順便顯示韓文店名（讓使用者方便手動複製）
        parts.append(
            f'<span style="font-size:0.78rem;opacity:.6;margin-left:8px;'
            f'user-select:all;-webkit-user-select:all;cursor:text;">{name_kr}</span>'
        )
    parts.append('</div>')
    st.markdown(''.join(parts), unsafe_allow_html=True)


def _render_buttons_for_links(links):
    """custom_card / multi_card 自訂 section 的按鈕（橫向 inline）。"""
    if not links:
        return
    parts = ['<div style="display:flex;gap:6px;align-items:center;margin:2px 0 6px 0;flex-wrap:wrap;">']
    for item in links:
        label = item.get("label", "")
        cls = item.get("cls", "g")
        url = item.get("url", "#")
        target = ' target="_blank" rel="noopener"' if str(url).startswith("http") else ""
        bg = {"g": "#4285F4", "n": "#03C75A", "t": "#FAE100"}.get(cls, "#94a3b8")
        fg = "#371D1E" if cls == "t" else "#fff"
        parts.append(
            f'<a href="{url}"{target} '
            f'style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:30px;height:30px;border-radius:50%;background:{bg};color:{fg} !important;'
            f'font-weight:800;font-size:13.5px;text-decoration:none;box-shadow:0 1px 2px rgba(0,0,0,.15);">{label}</a>'
        )
    parts.append('</div>')
    st.markdown(''.join(parts), unsafe_allow_html=True)


# ================================================================
# 主行程：地點 stop
# ================================================================
def stop(tag, place_ids, others=None, notes=None, show_taxi=True, mode="walking"):
    if isinstance(place_ids, str):
        place_ids = [place_ids]
    if notes is None:
        notes = [None] * len(place_ids)
    elif isinstance(notes, str):
        notes = [notes] + [None] * (len(place_ids) - 1)

    for i, pid in enumerate(place_ids):
        if pid not in PLACES:
            st.error(f"❌ 找不到地點: {pid}")
            continue
        p = PLACES[pid]
        _title_line(
            tag if i == 0 else "",
            p["name"],
            star=p.get("priority", False),
        )
        meta = _build_meta(p)
        _meta_line(meta)
        note_text = notes[i] if i < len(notes) and notes[i] is not None else p.get("note", "")
        _note_line(note_text)
        _render_buttons_for_place(p, mode=mode, show_taxi=show_taxi)
        st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

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


# ================================================================
# 自訂卡（沒有 PLACES 對應，純文字 + 自訂連結）
# ================================================================
def custom_card(tag, title, meta=None, note=None, links=None, dashed=False):
    _title_line(tag, title, small=dashed)
    if meta:
        _meta_line(meta)
    if note:
        _note_line(note)
    if links:
        _render_buttons_for_links(links)
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)


def note(tag, title, meta=None, note=None):
    """純說明（交通/提醒）。等同於 custom_card 但用比較小的標題。"""
    custom_card(tag=tag, title=title, meta=meta, note=note, links=None, dashed=True)


# ================================================================
# 多段：合併多個主要點到同一塊
# 用標題＋一條淡淡的水平分隔線分段
# ================================================================
def multi_card(tag, sections, others=None, show_taxi=True, mode="walking"):
    place_ids = []
    for idx, s in enumerate(sections):
        if idx > 0:
            # 段落之間放一條淡分隔線（不是 st.divider 那種粗的）
            st.markdown(
                '<hr style="border:none;border-top:1px dashed rgba(128,128,128,.25);'
                'margin:0.4rem 0 0.4rem 0;">',
                unsafe_allow_html=True,
            )

        if "place_id" in s:
            pid = s["place_id"]
            if pid not in PLACES:
                st.error(f"❌ 找不到地點: {pid}")
                continue
            place_ids.append(pid)
            p = PLACES[pid]
            _title_line(tag if idx == 0 else "", p["name"], star=p.get("priority", False))
            meta = _build_meta(p)
            _meta_line(meta)
            note_text = s.get("note") if s.get("note") is not None else p.get("note", "")
            _note_line(note_text)
            _render_buttons_for_place(p, mode=mode, show_taxi=show_taxi)
        else:
            _title_line(tag if idx == 0 else "", s.get("title", ""))
            if s.get("meta"):
                _meta_line(s["meta"])
            if s.get("note"):
                _note_line(s["note"])
            if s.get("links"):
                _render_buttons_for_links(s["links"])

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    if others and place_ids:
        area = PLACES[place_ids[0]].get("area")
        cat_label = {"food": "其他吃的", "shop": "其他逛的"}.get(others, "其他")
        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            items = get_by_area(area, exclude=place_ids, cat=others)
            if not items:
                st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            else:
                _render_backup_list(items, _SCHEDULED.get(others, set()))


# ================================================================
# 下拉框（其他吃的/逛的、飯店附近）—— 一樣用純排版
# ================================================================
def _render_backup_item(pid, p, already=False):
    name = p["name"]
    star_html = '<span class="star"> ⭐</span>' if p.get("priority") else ''
    already_html = '<span class="already-tag">已排</span>' if already else ''
    name_kr = p.get("name_kr", "")
    parts = []
    if p.get("sub"): parts.append(p["sub"])
    if p.get("hours"): parts.append(p["hours"])
    m = " · ".join(parts)
    if name_kr and m: meta_line = f"{name_kr}｜{m}"
    elif name_kr: meta_line = name_kr
    elif m: meta_line = m
    else: meta_line = ""

    sched_cls = "backup-row scheduled" if already else "backup-row"
    st.markdown(
        f'<div class="{sched_cls}">'
        f'<div class="backup-name">{name}{star_html}{already_html}</div>'
        f'{f"<div class=\"backup-meta\">{meta_line}</div>" if meta_line else ""}'
        f'{f"<div class=\"backup-note\">{p.get('"'"'note'"'"', '"'"''"'"')}</div>" if p.get("note") else ""}'
        f'</div>',
        unsafe_allow_html=True,
    )
    _render_buttons_for_place(p, mode="walking", show_taxi=True)


def _render_backup_list(items, scheduled_ids):
    items_sorted = sorted(items, key=lambda x: (x[0] in scheduled_ids, x[0]))
    for pid, p in items_sorted:
        _render_backup_item(pid, p, already=(pid in scheduled_ids))


# ================================================================
# 飯店收尾
# ================================================================
def hotel_bottom(today_food=None, today_shop=None):
    food_sched = set(today_food) if today_food is not None else _SCHEDULED["food"]
    shop_sched = set(today_shop) if today_shop is not None else _SCHEDULED["shop"]

    if "hotel" in PLACES:
        p = PLACES["hotel"]
        _title_line("住", p["name"], star=p.get("priority", False))
        _meta_line(_build_meta(p))
        _note_line(p.get("note", ""))
        _render_buttons_for_place(p, mode="walking", show_taxi=True)

    food_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="food")
    with st.expander("🍽️ 吃 — 飯店附近"):
        st.caption("弘대區所有吃的清單。主行程已排的會放最下面標「已排」。")
        _render_backup_list(food_all, food_sched)

    shop_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="shop")
    with st.expander("🛍️ 逛 — 飯店附近"):
        st.caption("弘대區所有逛的清單。主行程已排的會放最下面標「已排」。")
        _render_backup_list(shop_all, shop_sched)
