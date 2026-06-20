"""
渲染共用函式（v13 名古屋風排版 + T 複製修正版）：

設計
--------------------------------------------------------------
* 主行程：用 Streamlit 原生元件「一行一行往下排」+ 大區塊方形編號標題
* G / N / T 按鈕：用一個 36px 高的 iframe 容納三個按鈕
  - G / N 是普通連結
  - T 是 button + JS：先複製韓文店名 → 再開 Kakao T (kakaot://home)
  - iframe 是必要的，因為 Streamlit markdown 不允許 JavaScript 執行
* 下拉框（其他吃的/逛的、飯店附近）：跟主行程同套排版，每項用 markdown 列出
  - 已排項目沉到最下面 + 標「已排」徽章
* set_scheduled / stop / note / custom_card / multi_card / hotel_bottom
  API 全部保留，day1~5.py 不用改

T 功能說明
- 點 T 會：(1) 複製韓文店名到剪貼簿 (2) 開 Kakao T (kakaot://home)
- 在 https/https 環境用 navigator.clipboard，舊瀏覽器 fallback 用 textarea+execCommand
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
_SECTION_NO = [0]  # 主行程區塊計數，每次 set_scheduled() 重新從 1 開始


def set_scheduled(today_food=None, today_shop=None):
    _SCHEDULED["food"] = set(today_food or [])
    _SCHEDULED["shop"] = set(today_shop or [])
    _SECTION_NO[0] = 0   # 切換 Day 時計數歸零


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
/* expander 內容區域：固定高度 + 上下滑動 */
div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
div[data-testid="stExpander"] details > div{
  max-height:360px;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
}

/* ===== 大區塊標題 (方形編號 + tag + 店名) ===== */
.section-anchor{
  display:flex;
  align-items:center;
  gap:12px;
  margin:1.2rem 0 0.4rem 0;
  padding:0;
}
.section-anchor .num{
  flex-shrink:0;
  width:36px; height:36px;
  border-radius:8px;             /* 方底（圓角矩形）跟 GNT 的圓形按鈕區分 */
  display:inline-flex; align-items:center; justify-content:center;
  font-weight:800; font-size:1.05rem;
  color:#fff !important;
  background:#475569 !important;  /* 統一深灰底色，看到就知道是大標題 */
  box-shadow:0 1px 3px rgba(0,0,0,.2);
}
.section-anchor .stop-title{
  margin:0 !important;
  flex:1;
  min-width:0;
}

/* ===== 主行程文字 ===== */
.stop-title{
  font-size:1.05rem;
  font-weight:700;
  margin:0.25rem 0 0.15rem 0;
}
.stop-meta{
  font-size:0.82rem;
  opacity:.62;
  margin:0 0 0.15rem 0;
  line-height:1.5;
}
.stop-note{
  font-size:0.86rem;
  opacity:.92;
  margin:0.1rem 0 0.35rem 0;
  line-height:1.55;
}
.tag-emoji{
  font-size:1.05rem;
  margin-right:6px;
}
.star{color:#ff4b4b;}

/* ===== G / N / T 按鈕 ===== */
/* 用高權重選擇器 + !important 蓋過 Streamlit 深色主題對 <a> 的全域著色 */
.gnt-row{
  display:flex;
  gap:6px;
  align-items:center;
  margin:2px 0 8px 0;
  flex-wrap:nowrap;
}
a.gnt-btn,
a.gnt-btn:link,
a.gnt-btn:visited,
a.gnt-btn:hover,
a.gnt-btn:active{
  display:inline-flex !important;
  align-items:center !important;
  justify-content:center !important;
  width:30px !important;
  height:30px !important;
  border-radius:50% !important;
  font-weight:800 !important;
  font-size:13.5px !important;
  text-decoration:none !important;
  box-shadow:0 1px 2px rgba(0,0,0,.15);
  -webkit-tap-highlight-color:transparent;
  user-select:none;
  border:none !important;
}
a.gnt-btn.gnt-g,
a.gnt-btn.gnt-g:link,
a.gnt-btn.gnt-g:visited,
a.gnt-btn.gnt-g:hover{ background:#4285F4 !important; color:#ffffff !important; }
a.gnt-btn.gnt-n,
a.gnt-btn.gnt-n:link,
a.gnt-btn.gnt-n:visited,
a.gnt-btn.gnt-n:hover{ background:#03C75A !important; color:#ffffff !important; }
a.gnt-btn.gnt-t,
a.gnt-btn.gnt-t:link,
a.gnt-btn.gnt-t:visited,
a.gnt-btn.gnt-t:hover{ background:#FAE100 !important; color:#371D1E !important; }

/* ===== 已排徽章 ===== */
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

/* ===== 備案清單項目 ===== */
.backup-row{
  padding:0.3rem 0;
  border-bottom:1px dashed rgba(128,128,128,.18);
}
.backup-row:last-child{ border-bottom:none; }
.backup-row.scheduled{ opacity:.6; }
.backup-name{ font-weight:700; font-size:0.92rem; }
.backup-meta{ font-size:0.78rem; opacity:.66; margin-top:2px; line-height:1.45; }
.backup-note{ font-size:0.8rem; opacity:.86; margin-top:3px; line-height:1.5; }

/* st.divider 在新版有大圓圈編號的設計裡顯得多餘，藏起來 */
hr[data-testid="stDivider"],
[data-testid="stHorizontalDivider"]{
  display:none !important;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


# ================================================================
# 共用：標題列（emoji 標籤 + 店名 + ⭐）
# ================================================================
# 類別 → 大圓圈底色（深淺色都看得清楚）
_NUM_BG = {
    "早": "#f59e0b", "午": "#f97316", "晚": "#ef4444",
    "宵": "#6366f1", "點": "#ec4899", "逛": "#a855f7",
    "買": "#a855f7", "景": "#10b981", "住": "#3b82f6",
}


def _section_anchor(tag, name, star=False):
    """主行程區塊的大標題：左側方形編號（統一深灰）+ tag emoji + 店名。
    每呼叫一次計數 +1。"""
    _SECTION_NO[0] += 1
    no = _SECTION_NO[0]
    star_html = '<span class="star"> ⭐</span>' if star else ''
    tag_html = f'<span class="tag-emoji">{tag}</span>' if tag else ''
    st.markdown(
        f'<div class="section-anchor">'
        f'<span class="num">{no}</span>'
        f'<div class="stop-title">{tag_html}{name}{star_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _title_line(tag, name, star=False, small=False):
    """子標題（multi_card 第 2、3 段、自訂卡的小標）— 沒有圓圈，純文字。"""
    star_html = '<span class="star"> ⭐</span>' if star else ''
    tag_html = f'<span class="tag-emoji">{tag}</span>' if tag else ''
    size = "1rem" if small else "1.02rem"
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
    """G / N / T 三按鈕在同一個 iframe，T 點下去先複製韓文店名再開 Kakao T。
    用 iframe 是為了讓 JavaScript 能執行 (Streamlit markdown 不能跑 JS)。"""
    name_kr = p.get("name_kr") or p["name"]
    g = html_lib.escape(gmap_url(f"{name_kr} {p.get('address','')}", mode), quote=True)
    n = html_lib.escape(naver_url(query=name_kr, lat=p.get("lat"), lng=p.get("lng"),
                                  name=name_kr, mode=mode), quote=True)
    ct = json.dumps(str(name_kr))
    k = json.dumps(kakaot_url())

    t_btn = ""
    t_script = ""
    if show_taxi:
        t_btn = '<button id="tb" class="b t" type="button" title="複製韓文店名並開啟 Kakao T">T</button>'
        t_script = (
            f'(function(){{'
            f'var el=document.getElementById("tb");if(!el)return;'
            f'el.addEventListener("click",async function(){{'
            f'try{{'
            f'if(navigator.clipboard&&window.isSecureContext){{await navigator.clipboard.writeText({ct});}}'
            f'else{{'
            f'var ta=document.createElement("textarea");ta.value={ct};'
            f'ta.style.cssText="position:fixed;left:-9999px;top:0";'
            f'document.body.appendChild(ta);ta.focus();ta.select();'
            f'try{{document.execCommand("copy");}}catch(e){{}}'
            f'document.body.removeChild(ta);'
            f'}}}}catch(e){{}}'
            f'el.innerText="\\u2713";'
            f'setTimeout(function(){{el.innerText="T";}},1000);'
            f'window.location.href={k};'
            f'}});'
            f'}})();'
        )

    doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{background:transparent;overflow:hidden;}}
.row{{display:flex;gap:6px;align-items:center;}}
.b{{
  width:30px;height:30px;border-radius:50%;
  display:inline-flex;align-items:center;justify-content:center;
  font-weight:800;font-size:13.5px;
  text-decoration:none;border:none;cursor:pointer;
  box-shadow:0 1px 2px rgba(0,0,0,.15);
  -webkit-tap-highlight-color:transparent;user-select:none;
  font-family:-apple-system,system-ui,sans-serif;
}}
.b:active{{transform:scale(.92);}}
.b.g{{background:#4285F4;color:#fff;}}
.b.n{{background:#03C75A;color:#fff;}}
.b.t{{background:#FAE100;color:#371D1E;}}
</style></head><body>
<div class="row">
  <a class="b g" href="{g}" target="_blank" rel="noopener">G</a>
  <a class="b n" href="{n}">N</a>
  {t_btn}
</div>
<script>{t_script}</script>
</body></html>"""
    components.html(doc, height=36, scrolling=False)


def _render_buttons_for_links(links):
    """custom_card / multi_card 自訂 section 的按鈕（純 HTML class）。"""
    if not links:
        return
    parts = ['<div class="gnt-row">']
    for item in links:
        label = item.get("label", "")
        cls = item.get("cls", "g")
        url = item.get("url", "#")
        target = ' target="_blank" rel="noopener"' if str(url).startswith("http") else ""
        parts.append(f'<a class="gnt-btn gnt-{cls}" href="{url}"{target}>{label}</a>')
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
        if i == 0:
            _section_anchor(tag, p["name"], star=p.get("priority", False))
        else:
            _title_line("", p["name"], star=p.get("priority", False))
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
    # 自訂卡（如 RMQ、飛機）= 主行程的一格 → 用大圓圈編號
    # dashed=True 的是 note()（純說明，例如「弘대→聖水洞 Taxi」），維持小標
    if dashed:
        _title_line(tag, title, small=True)
    else:
        _section_anchor(tag, title)
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
            if idx == 0:
                _section_anchor(tag, p["name"], star=p.get("priority", False))
            else:
                _title_line("", p["name"], star=p.get("priority", False))
            meta = _build_meta(p)
            _meta_line(meta)
            note_text = s.get("note") if s.get("note") is not None else p.get("note", "")
            _note_line(note_text)
            _render_buttons_for_place(p, mode=mode, show_taxi=show_taxi)
        else:
            if idx == 0:
                _section_anchor(tag, s.get("title", ""))
            else:
                _title_line("", s.get("title", ""))
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
def _render_backup_item(pid, p, already=False, is_last=False):
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

    note_text = p.get("note", "")
    sched_cls = "backup-row scheduled" if already else "backup-row"

    # 把店名 / meta / note 一次組好
    html_parts = [f'<div class="{sched_cls}">']
    html_parts.append(f'<div class="backup-name">{name}{star_html}{already_html}</div>')
    if meta_line:
        html_parts.append(f'<div class="backup-meta">{meta_line}</div>')
    if note_text:
        html_parts.append(f'<div class="backup-note">{html_lib.escape(note_text)}</div>')
    html_parts.append('</div>')
    st.markdown(''.join(html_parts), unsafe_allow_html=True)

    # 按鈕列
    _render_buttons_for_place(p, mode="walking", show_taxi=True)

    # 分隔線：放在按鈕「下方」，這樣排序變成 名稱 → meta → note → GNT → ─── → 下一個
    if not is_last:
        st.markdown(
            '<hr style="border:none;border-top:1px dashed rgba(128,128,128,.25);'
            'margin:0.4rem 0 0.5rem 0;">',
            unsafe_allow_html=True,
        )


def _render_backup_list(items, scheduled_ids):
    items_sorted = sorted(items, key=lambda x: (x[0] in scheduled_ids, x[0]))
    total = len(items_sorted)
    for i, (pid, p) in enumerate(items_sorted):
        _render_backup_item(pid, p, already=(pid in scheduled_ids), is_last=(i == total - 1))


# ================================================================
# 飯店收尾
# ================================================================
def hotel_bottom(today_food=None, today_shop=None):
    food_sched = set(today_food) if today_food is not None else _SCHEDULED["food"]
    shop_sched = set(today_shop) if today_shop is not None else _SCHEDULED["shop"]

    if "hotel" in PLACES:
        p = PLACES["hotel"]
        _section_anchor("🏠", p["name"], star=p.get("priority", False))
        _meta_line(_build_meta(p))
        _note_line(p.get("note", ""))
        _render_buttons_for_place(p, mode="walking", show_taxi=True)

    food_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="food")
    with st.expander("🍽️ 吃 — 飯店附近"):
        st.caption(" ")
        _render_backup_list(food_all, food_sched)

    shop_all = get_by_area(AREA_HONGDAE, exclude=["hotel"], cat="shop")
    with st.expander("🛍️ 逛 — 飯店附近"):
        st.caption(" ")
        _render_backup_list(shop_all, shop_sched)
