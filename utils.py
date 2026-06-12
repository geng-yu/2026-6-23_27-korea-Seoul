"""v10 verbatim from user"""
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import html as html_lib
import json
from places import PLACES, get_by_area, AREA_HONGDAE

_SCHEDULED = {"food": set(), "shop": set()}
def set_scheduled(today_food=None, today_shop=None):
    _SCHEDULED["food"] = set(today_food or [])
    _SCHEDULED["shop"] = set(today_shop or [])

_TAG_ACCENT_HEX = {"早":"#f59e0b","午":"#f97316","晚":"#ef4444","宵":"#6366f1","點":"#ec4899","逛":"#a855f7","買":"#a855f7","景":"#10b981","住":"#3b82f6"}
def _accent_hex(tag): return _TAG_ACCENT_HEX.get(tag, "#94a3b8")

_CSS = """
<style>
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMainBlockContainer"]{ gap:0 !important; }
[data-testid="stIFrame"],
[data-testid="stCustomComponentV1"],
iframe{ display:block !important; margin:0 !important; padding:0 !important; border:none !important; }
div.element-container,
div[data-testid="element-container"],
[data-testid="stElementContainer"]{ margin:0 0 0.3rem 0 !important; padding:0 !important; }
div[data-testid="stExpander"]{ margin:0.18rem 0 0.34rem 0 !important; }
div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
div[data-testid="stExpander"] details > div{
  max-height:320px; overflow-y:auto; -webkit-overflow-scrolling:touch;
  padding:4px 6px 4px 0 !important;
}
div[data-testid="stExpander"] [data-testid="stVerticalBlock"],
div[data-testid="stExpander"] [data-testid="stVerticalBlockBorderWrapper"]{ gap:0 !important; }
div[data-testid="stExpander"] div.element-container,
div[data-testid="stExpander"] div[data-testid="element-container"],
div[data-testid="stExpander"] [data-testid="stElementContainer"]{ margin:0 0 0.2rem 0 !important; padding:0 !important; }
div[data-testid="stExpander"] div.element-container:last-child,
div[data-testid="stExpander"] div[data-testid="element-container"]:last-child,
div[data-testid="stExpander"] [data-testid="stElementContainer"]:last-child{ margin-bottom:0 !important; }
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
"""


# 全域 height-fix：在主畫面執行，定時抓每個卡片 iframe 內 .card 的真實高度，
# 直接寫回 iframe 元素的 height 屬性。不依賴 Streamlit 的 postMessage 協議。
_HEIGHT_FIX_PARENT = """
<script>
(function(){
  if(window.__cardHeightFix)return; window.__cardHeightFix=true;
  function fixOne(f){
    try{
      var d=f.contentDocument; if(!d||!d.body)return;
      var card=d.querySelector('.card'); if(!card)return;
      var h=Math.ceil(card.getBoundingClientRect().height)+4;
      if(h>10 && Math.abs(f.offsetHeight-h)>2){
        f.style.height=h+'px';
        f.setAttribute('height',h);
      }
    }catch(e){}
  }
  function tick(){
    var ifs=document.querySelectorAll('iframe');
    for(var i=0;i<ifs.length;i++) fixOne(ifs[i]);
  }
  tick();
  setInterval(tick, 200);
  [50,150,300,600,1000,1500,2500].forEach(function(t){ setTimeout(tick,t); });
  var mo=new MutationObserver(tick);
  mo.observe(document.body,{childList:true,subtree:true});
})();
</script>
"""

def _inject_height_fix():
    """注入主畫面 JS：定時抓每張卡片 iframe 內 .card 真實高度，直接寫回 iframe 元素。
    用 components.html 確保 <script> 真的執行；script 內透過 window.parent 操作主畫面。"""
    components.html("""
<script>
(function(){
  var W = window.parent;
  if(W.__cardHeightFix) return;
  W.__cardHeightFix = true;
  function fixOne(f){
    try{
      var d=f.contentDocument; if(!d||!d.body) return;
      var card=d.querySelector('.card'); if(!card) return;
      var h=Math.ceil(card.getBoundingClientRect().height)+4;
      if(h>10 && Math.abs(f.offsetHeight-h)>2){
        f.style.height=h+'px';
        f.setAttribute('height',h);
      }
    }catch(e){}
  }
  function tick(){
    var D = W.document;
    var ifs = D.querySelectorAll('iframe');
    for(var i=0;i<ifs.length;i++) fixOne(ifs[i]);
  }
  tick();
  setInterval(tick, 200);
  [50,150,300,600,1000,1500,2500].forEach(function(t){ setTimeout(tick,t); });
  var mo = new W.MutationObserver(tick);
  mo.observe(W.document.body, {childList:true, subtree:true});
})();
</script>
""", height=0)

def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)
    _inject_height_fix()

def gmap_url(query, mode="walking"):
    q = urllib.parse.quote(str(query))
    return f"https://www.google.com/maps/dir/?api=1&destination={q}&travelmode={mode}"
def naver_url(query=None, lat=None, lng=None, name=None, mode="walking"):
    appname = "seoul_trip_2026"; nm = {"walking":"walk","driving":"car","transit":"public"}.get(mode,"walk")
    if lat is not None and lng is not None:
        dn = urllib.parse.quote(str(name or "목적지"))
        return f"nmap://route/{nm}?dlat={lat}&dlng={lng}&dname={dn}&appname={appname}"
    if query:
        q = urllib.parse.quote(str(query))
        return f"nmap://search?query={q}&appname={appname}"
    return f"nmap://map?appname={appname}"
def kakaot_url(): return "kakaot://home"
def _safe_href(url): return html_lib.escape(url, quote=True)
def _build_meta_line(place):
    nk = place.get("name_kr",""); parts=[]
    if place.get("sub"): parts.append(place["sub"])
    if place.get("hours"): parts.append(place["hours"])
    m=" · ".join(parts)
    if nk and m: return f"{nk}｜{m}"
    elif nk: return nk
    elif m: return m
    return ""

_IFRAME_STYLE = """
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:transparent;overflow:hidden;}
body{font-family:-apple-system,BlinkMacSystemFont,system-ui,"Noto Sans TC","Noto Sans KR",sans-serif;}
:root{ --bg:#f0f2f6;--text:#1a1a1a; --border:rgba(128,128,128,.16); --border-dash:rgba(128,128,128,.35); --section-line:rgba(128,128,128,.22); }
@media(prefers-color-scheme:dark){:root{ --bg:#262730;--text:#fafafa; --border:rgba(250,250,250,.16); --border-dash:rgba(250,250,250,.30); --section-line:rgba(250,250,250,.20); }}
.card{ position:relative;background:var(--bg);border:1px solid var(--border);border-radius:14px;padding:12px 14px 14px 12px;display:flex;align-items:flex-start;gap:11px;box-shadow:0 1px 4px rgba(0,0,0,.05);overflow:visible; }
.card.dashed{ background:transparent;border:1.5px dashed var(--border-dash);box-shadow:none; }
.card::before{ content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent,#94a3b8); }
.card.dashed::before{display:none;}
.chip{ flex-shrink:0;width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:#fff;background:var(--accent,#94a3b8);margin-top:1px; }
.chip.dashed{background:rgba(128,128,128,.14);color:var(--text);}
.chip.ghost{background:transparent;color:transparent;}
.body{ flex-grow:1;min-width:0;padding-bottom:2px; }
.section{ padding:6px 0 2px 0;margin-top:6px; }
.section:first-child{ margin-top:0;padding-top:0; }
.title-row{ display:flex;align-items:flex-start;justify-content:space-between;gap:8px; }
h4{ font-size:15.5px;font-weight:700;color:var(--text);line-height:1.35;word-break:break-word;flex:1;min-width:0;margin:0; }
h5{ font-size:14.5px;font-weight:700;color:var(--text);line-height:1.35;word-break:break-word;flex:1;min-width:0;margin:0; }
.meta{ font-size:12px;color:var(--text);opacity:.62;margin-top:4px;line-height:1.45; }
.note{ font-size:12.5px;color:var(--text);opacity:.88;margin-top:5px;line-height:1.5; }
.star{color:#ff4b4b;font-size:13px;}
.btns{ display:flex;gap:6px;flex-shrink:0;align-items:center;padding-top:1px; }
.b{ width:30px;height:30px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:13.5px;text-decoration:none;border:none;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,.15);-webkit-tap-highlight-color:transparent;user-select:none;font-family:-apple-system,system-ui,sans-serif; }
.b:active{transform:scale(.92);}
.b.g{background:#4285F4;color:#fff;}
.b.n{background:#03C75A;color:#fff;}
.b.t{background:#FAE100;color:#371D1E;}
"""

_HEIGHT_REPORTER = """
(function(){
  function getHeight(){
    const body=document.body, html=document.documentElement;
    return Math.ceil(Math.max(body.scrollHeight,body.offsetHeight,body.getBoundingClientRect().height,html.scrollHeight,html.offsetHeight,html.clientHeight,html.getBoundingClientRect().height))+6;
  }
  function report(){window.parent.postMessage({isStreamlitMessage:true,type:"streamlit:setFrameHeight",height:getHeight()},"*");}
  if(window.ResizeObserver){const ro=new ResizeObserver(report);ro.observe(document.body);ro.observe(document.documentElement);}
  if(document.fonts&&document.fonts.ready){document.fonts.ready.then(report).catch(function(){});}
  window.addEventListener("load",report); window.addEventListener("resize",report);
  requestAnimationFrame(function(){report();requestAnimationFrame(function(){report();requestAnimationFrame(report);});});
  setTimeout(report,50);setTimeout(report,120);setTimeout(report,250);setTimeout(report,400);
})();
"""

def _btns_html_for_place(p, mode, show_taxi, uid):
    name=p["name"]; name_kr=p.get("name_kr",name)
    g=_safe_href(gmap_url(f"{name_kr} {p.get('address','')}", mode))
    n=_safe_href(naver_url(query=name_kr,lat=p.get("lat"),lng=p.get("lng"),name=name_kr or name,mode=mode))
    parts=[f'<a class="b g" href="{g}" target="_blank" rel="noopener" title="Google Maps">G</a>',
           f'<a class="b n" href="{n}" title="NAVER">N</a>']
    if show_taxi:
        parts.append(f'<button class="b t" id="t_{uid}" type="button" title="複製韓文店名並開啟 Kakao T">T</button>')
    return '<div class="btns">'+''.join(parts)+'</div>'

def _btns_html_for_links(links):
    if not links: return ""
    parts=[]
    for item in links:
        label=html_lib.escape(item.get("label",""))
        cls=html_lib.escape(item.get("cls","g"))
        raw_url=item.get("url","#"); url=_safe_href(raw_url)
        target=' target="_blank" rel="noopener"' if str(raw_url).startswith("http") else ""
        parts.append(f'<a class="b {cls}" href="{url}"{target} title="{label}">{label}</a>')
    return '<div class="btns">'+''.join(parts)+'</div>'

def _t_script(uid, copy_text):
    ct=json.dumps(str(copy_text)); k=json.dumps(kakaot_url())
    return (f'(function(){{var el=document.getElementById("t_{uid}");if(!el)return;'
            f'el.addEventListener("click",async function(){{try{{'
            f'if(navigator.clipboard&&window.isSecureContext){{await navigator.clipboard.writeText({ct});}}'
            f'else{{var ta=document.createElement("textarea");ta.value={ct};ta.style.cssText="position:fixed;left:-9999px;top:0";document.body.appendChild(ta);ta.focus();ta.select();try{{document.execCommand("copy");}}catch(e){{}}document.body.removeChild(ta);}}'
            f'}}catch(e){{}}el.innerText="\\u2713";setTimeout(function(){{el.innerText="T";}},1000);window.location.href={k};}});}})();')

def _emit_card(accent_hex, inner_html, t_scripts, est_height):
    all_scripts=''.join(t_scripts)+_HEIGHT_REPORTER
    doc=('<!DOCTYPE html><html><head><meta charset="utf-8">'
         '<meta name="viewport" content="width=device-width,initial-scale=1">'
         f'<style>{_IFRAME_STYLE}:root{{--accent:{accent_hex};}}</style>'
         '</head><body>'+inner_html+f'<script>{all_scripts}</script></body></html>')
    components.html(doc, height=est_height, scrolling=False)

def _render_card(tag, place_id, note_override=None, show_taxi=True, mode="walking", accent_override_hex=None):
    if place_id not in PLACES: st.error(f"❌ 找不到地點: {place_id}"); return
    p=PLACES[place_id]; accent=accent_override_hex or _accent_hex(tag)
    chip=f'<div class="chip">{html_lib.escape(tag)}</div>' if tag else '<div class="chip ghost">·</div>'
    name=html_lib.escape(p["name"]); star='<span class="star"> ⭐</span>' if p.get("priority") else ''
    meta=_build_meta_line(p); meta_html=f'<p class="meta">{html_lib.escape(meta)}</p>' if meta else ''
    note=note_override if note_override is not None else p.get("note","")
    note_html=f'<p class="note">{html_lib.escape(note)}</p>' if note else ''
    uid=place_id.replace("-","_"); btns=_btns_html_for_place(p,mode,show_taxi,uid)
    inner=f'<div class="card">{chip}<div class="body"><div class="title-row"><h4>{name}{star}</h4>{btns}</div>{meta_html}{note_html}</div></div>'
    t_scripts=[_t_script(uid,p.get("name_kr") or p["name"])] if show_taxi else []
    est=62+(18 if meta else 0)+(38 if note else 0)
    _emit_card(accent,inner,t_scripts,est)

def custom_card(tag, title, meta=None, note=None, links=None, dashed=False):
    accent=_accent_hex(tag); tag_e=html_lib.escape(tag) if tag else "·"
    if dashed: chip=f'<div class="chip dashed">{tag_e}</div>'; card_cls="card dashed"; title_tag="h5"
    elif tag: chip=f'<div class="chip">{tag_e}</div>'; card_cls="card"; title_tag="h4"
    else: chip='<div class="chip ghost">·</div>'; card_cls="card"; title_tag="h4"
    title_e=html_lib.escape(title); meta_html=f'<p class="meta">{html_lib.escape(meta)}</p>' if meta else ''
    note_html=f'<p class="note">{html_lib.escape(note)}</p>' if note else ''; btns=_btns_html_for_links(links)
    inner=f'<div class="{card_cls}">{chip}<div class="body"><div class="title-row"><{title_tag}>{title_e}</{title_tag}>{btns}</div>{meta_html}{note_html}</div></div>'
    est=58+(18 if meta else 0)+(38 if note else 0)
    _emit_card(accent,inner,[],est)

def _render_backup_item(pid, p, already=False):
    accent="#94a3b8"; name=html_lib.escape(p["name"])
    star='<span class="star"> ⭐</span>' if p.get("priority") else ''
    already_tag=(' <span style="font-size:10px;font-weight:700;background:rgba(255,75,75,.13);color:#ff4b4b;padding:2px 7px;border-radius:99px;white-space:nowrap;">已排</span>') if already else ''
    name_kr=p.get("name_kr",""); parts=[]
    if p.get("sub"): parts.append(p["sub"])
    if p.get("hours"): parts.append(p["hours"])
    meta=" · ".join(parts)
    if name_kr and meta: meta_line=f"{name_kr}｜{meta}"
    elif name_kr: meta_line=name_kr
    elif meta: meta_line=meta
    else: meta_line=""
    meta_html=f'<p class="meta">{html_lib.escape(meta_line)}</p>' if meta_line else ''
    note_html=f'<p class="note">{html_lib.escape(p.get("note",""))}</p>' if p.get("note") else ''
    uid=("bk_"+pid).replace("-","_"); btns=_btns_html_for_place(p,"walking",True,uid)
    opacity=' style="opacity:.62"' if already else ''
    inner=f'<div class="card"{opacity}><div class="chip ghost">·</div><div class="body"><div class="title-row"><h4 style="font-size:13.5px;">{name}{star}{already_tag}</h4>{btns}</div>{meta_html}{note_html}</div></div>'
    t_scripts=[_t_script(uid,p.get("name_kr") or p["name"])]
    est=56+(16 if meta_line else 0)+(36 if p.get("note") else 0)
    _emit_card(accent,inner,t_scripts,est)

def _render_backup_list(items, scheduled_ids):
    items_sorted=sorted(items,key=lambda x:(x[0] in scheduled_ids,x[0]))
    for pid,p in items_sorted: _render_backup_item(pid,p,already=(pid in scheduled_ids))

def stop(tag, place_ids, others=None, notes=None, show_taxi=True, mode="walking"):
    if isinstance(place_ids,str): place_ids=[place_ids]
    if notes is None: notes=[None]*len(place_ids)
    elif isinstance(notes,str): notes=[notes]+[None]*(len(place_ids)-1)
    accent=_accent_hex(tag)
    for i,pid in enumerate(place_ids):
        _render_card(tag=tag if i==0 else "",place_id=pid,note_override=notes[i] if i<len(notes) else None,show_taxi=show_taxi,mode=mode,accent_override_hex=accent)
    if others:
        first_p=PLACES[place_ids[0]]; area=first_p.get("area")
        cat_label={"food":"其他吃的","shop":"其他逛的"}.get(others,"其他")
        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            items=get_by_area(area,exclude=place_ids,cat=others)
            if not items: st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            else: _render_backup_list(items,_SCHEDULED.get(others,set()))

def note(tag, title, meta=None, note=None):
    custom_card(tag=tag,title=title,meta=meta,note=note,links=None,dashed=True)

def hotel_bottom(today_food=None, today_shop=None):
    food_sched=set(today_food) if today_food is not None else _SCHEDULED["food"]
    shop_sched=set(today_shop) if today_shop is not None else _SCHEDULED["shop"]
    _render_card(tag="住",place_id="hotel",show_taxi=True)
    food_all=get_by_area(AREA_HONGDAE,exclude=["hotel"],cat="food")
    with st.expander("🍽️ 吃 — 飯店附近"):
        st.caption("弘대區所有吃的清單。主行程已排的會放最下面標「已排」。")
        _render_backup_list(food_all,food_sched)
    shop_all=get_by_area(AREA_HONGDAE,exclude=["hotel"],cat="shop")
    with st.expander("🛍️ 逛 — 飯店附近"):
        st.caption("弘대區所有逛的清單。主行程已排的會放最下面標「已排」。")
        _render_backup_list(shop_all,shop_sched)

def multi_card(tag, sections, others=None, show_taxi=True, mode="walking"):
    accent=_accent_hex(tag); place_ids=[]; sec_parts=[]; t_scripts=[]
    for idx,s in enumerate(sections):
        if "place_id" in s:
            pid=s["place_id"]
            if pid not in PLACES: st.error(f"❌ 找不到地點: {pid}"); continue
            place_ids.append(pid); p=PLACES[pid]
            title_html=html_lib.escape(p["name"])+('<span class="star"> ⭐</span>' if p.get("priority") else '')
            meta=_build_meta_line(p); note_txt=s.get("note") if s.get("note") is not None else p.get("note","")
            uid=("m_"+pid+"_"+str(idx)).replace("-","_"); btns=_btns_html_for_place(p,mode,show_taxi,uid)
            if show_taxi: t_scripts.append(_t_script(uid,p.get("name_kr") or p["name"]))
        else:
            title_html=html_lib.escape(s.get("title",""))
            meta=s.get("meta",""); note_txt=s.get("note","")
            btns=_btns_html_for_links(s.get("links"))
        meta_html=f'<p class="meta">{html_lib.escape(meta)}</p>' if meta else ''
        note_html=f'<p class="note">{html_lib.escape(note_txt)}</p>' if note_txt else ''
        sec_parts.append(f'<div class="section"><div class="title-row"><h4>{title_html}</h4>{btns}</div>{meta_html}{note_html}</div>')
    chip=f'<div class="chip">{html_lib.escape(tag)}</div>' if tag else '<div class="chip ghost">·</div>'
    inner=f'<div class="card">{chip}<div class="body">'+''.join(sec_parts)+'</div></div>'
    est=108
    _emit_card(accent,inner,t_scripts,est)
    if others and place_ids:
        area=PLACES[place_ids[0]].get("area")
        cat_label={"food":"其他吃的","shop":"其他逛的"}.get(others,"其他")
        with st.expander(f"🔄 {cat_label}（{area}附近）"):
            items=get_by_area(area,exclude=place_ids,cat=others)
            if not items: st.caption(f"({area} 沒有其他 {cat_label} 資料)")
            else: _render_backup_list(items,_SCHEDULED.get(others,set()))
