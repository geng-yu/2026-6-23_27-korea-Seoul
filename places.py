"""
首爾旅遊地點資料中心
=====================================
所有店家/景點集中在這裡，每天的行程都從這裡撈資料。

欄位:
- name      : 中文名稱
- name_kr   : 韓文名稱
- area      : 區域 (用來決定備案清單)
- cat       : 主分類 food / shop / sight / hotel / transit
- sub       : 子分類 (例如 燒烤 / 蔘雞湯 / 美妝 / 百貨...)
- address   : 韓文地址
- lat, lng  : 座標
- hours     : 營業時間文字
- phone     : 電話 (選填)
- note      : 備註
- priority  : ⭐ 是否優先

整理紀錄 (v15)：
  ✅ 拿掉重複 key: hyodam_dakhanmari (出現 2 次)、menten_ramen (出現 2 次)
  ✅ 補上 day1.py 引用但缺的: ak_plaza
  ✅ 統一縮排和分組註解
  ✅ 132 個有效條目 (不含台中 RMQ 統計)
"""

# ================================================================
# 區域常數
# ================================================================
AREA_HONGDAE = "弘대"
AREA_YEONNAM = "延南"
AREA_MANGWON = "望遠"
AREA_SEONGSU = "聖水"
AREA_DONGDAEMUN = "東大門"
AREA_GWANGJANG = "廣藏"
AREA_ANGUK = "安國"
AREA_IKSEON = "益善"
AREA_MYEONGDONG = "明洞"
AREA_AIRPORT = "機場"


PLACES = {

    # ================================================================
    # 飯店
    # ================================================================
    "hotel": {
        "name": "9 Brick Hotel", "name_kr": "나인브릭 호텔",
        "area": AREA_HONGDAE, "cat": "hotel",
        "address": "서울 마포구 홍익로5길 32",
        "lat": 37.5537661, "lng": 126.9205306,
        "hours": "Check-in 15:00 / Check-out 11:00",
        "phone": "+82-2-3141-8800",
        "note": "弘대입구站 9 號出口走 6 分鐘",
    },

    # ================================================================
    # 弘대 — 食 (food)
    # ================================================================
    "yukmong": {
        "name": "肉夢", "name_kr": "육몽 홍대본점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "燒烤",
        "address": "서울 마포구 양화로16길 19 1-3층",
        "lat": 37.5532162, "lng": 126.9206942,
        "hours": "11:30-24:00 (週五六到 01:00)",
        "phone": "02-338-1142",
        "note": "三層樓燒烤",
        "priority": True,
    },
    "bhc": {
        "name": "BHC 弘대점", "name_kr": "BHC치킨 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "炸雞",
        "address": "서울 마포구 홍익로6길 10 2층",
        "lat": 37.5550616, "lng": 126.9226060,
        "hours": "12:00-23:30 (週五六到 24:00)",
        "phone": "02-325-3112",
        "note": "起司炸雞，飯店走路 3 min",
    },
    "kyochon": {
        "name": "橋村炸雞 弘대점", "name_kr": "교촌치킨 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "炸雞",
        "address": "서울 마포구 양화로16길 6",
        "lat": 37.5535944, "lng": 126.9201354,
        "hours": "12:00-01:30",
        "phone": "02-338-1300",
        "note": "醬油蒜味/紅辣味，走路 3 min",
    },
    "baeknyeon": {
        "name": "百年百歲土種蔘雞湯", "name_kr": "백년토종삼계탕",
        "area": AREA_HONGDAE, "cat": "food", "sub": "蔘雞湯",
        "address": "서울 마포구 양화로 118 1층",
        "lat": 37.5538158, "lng": 126.9202046,
        "hours": "09:00-22:00",
        "phone": "02-325-3399",
        "note": "2017 米其林，09:00 開",
        "priority": True,
    },
    "bongsan": {
        "name": "鳳山精肉", "name_kr": "봉산정육 홍대본점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "燒烤",
        "address": "서울 마포구 양화로16길 30 1층",
        "lat": 37.5529244, "lng": 126.9211367,
        "hours": "12:00-23:00",
        "phone": "010-2816-5144",
        "note": "牛豬精肉燒烤",
        "priority": True,
    },
    "myth_jokbal": {
        "name": "豬腳小姐", "name_kr": "미쓰족발 홍대본점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "豬腳",
        "address": "서울 마포구 어울마당로 123-1",
        "lat": 37.5556851, "lng": 126.9237421,
        "hours": "12:30-24:00",
        "phone": "02-337-2111",
        "note": "醬燒豬腳，配辣泡菜湯麵",
        "priority": True,
    },
    "ungteori": {
        "name": "荒謬的生肉 (吃到飽)", "name_kr": "엉터리생고기 무한리필 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "燒烤吃到飽",
        "address": "서울 마포구 어울마당로 118",
        "lat": 37.5550467, "lng": 126.9235304,
        "hours": "11:00-23:00",
        "phone": "02-324-9588",
        "note": "燒烤吃到飽",
    },
    "ilpyeon_eel": {
        "name": "一片鰻魚", "name_kr": "일편장어 홍대본점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "鰻魚",
        "address": "서울 마포구 양화로16길 15 2층 201호",
        "lat": 37.5534238, "lng": 126.9205212,
        "hours": "12:00-23:00 (週五六到 24:00)",
        "phone": "02-336-6716",
        "note": "活鰻現烤",
    },
    "ilpyeon_beef": {
        "name": "一片里脊韓牛", "name_kr": "일편등심 홍대본점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "韓牛",
        "address": "서울 마포구 홍익로6길 52 2,3층",
        "lat": 37.5550, "lng": 126.9230,
        "hours": "12:00-24:00 (15:00-17:00 休息)",
        "phone": "0507-1403-1092",
        "note": "高級韓牛里脊",
    },
    "donsubaek": {
        "name": "豚百壽", "name_kr": "돈수백 홍대직영점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "豬肉湯飯",
        "address": "서울 마포구 홍익로6길 74",
        "lat": 37.5568766, "lng": 126.9252693,
        "hours": "24h",
        "phone": "02-324-3131",
        "note": "豬肉湯飯，平板點餐多語言，24h",
    },
    "donjunam": {
        "name": "給豚的男人", "name_kr": "돈주는남자 본점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "燒烤",
        "address": "서울 마포구 잔다리로6길 34-9",
        "lat": 37.5519052, "lng": 126.9210800,
        "hours": "13:00-24:00",
        "phone": "0507-1359-0499",
        "note": "巷弄燒烤，老闆親自烤",
    },
    "throat": {
        "name": "喉嚨水芹菜烤肉", "name_kr": "목구멍 홍대입구역점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "燒烤",
        "address": "弘대입구역附近",
        "lat": 37.5560, "lng": 126.9230,
        "hours": "查詢中",
        "note": "水芹菜+烤肉",
    },
    "hongs_jjukkumi": {
        "name": "Hong's 辣炒章魚", "name_kr": "홍스쭈꾸미 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "辣炒章魚",
        "address": "서울 마포구 어울마당로 146",
        "lat": 37.556165, "lng": 126.9260901,
        "hours": "11:30-02:00",
        "phone": "02-325-7943",
        "note": "可選辣度，吃完用剩醬做炒飯，小菜無限續",
    },
    "vanga_dakgalbi": {
        "name": "Vanga 炭火雞排", "name_kr": "반가 숯불닭갈비 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "炭火雞排",
        "address": "서울 마포구 어울마당로 147-1",
        "lat": 37.5567023, "lng": 126.9262810,
        "hours": "11:00-01:00",
        "phone": "02-337-3545",
        "note": "紫蘇葉+蒜柚子醬包著吃",
    },
    "myeongryun_jinsa": {
        "name": "二代祖馬鈴薯排骨湯", "name_kr": "이대조뼈다귀 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "馬鈴薯排骨湯",
        "address": "서울 마포구 동교로 196",
        "lat": 37.5570, "lng": 126.9250,
        "hours": "10:00-23:00",
        "note": "人氣排骨湯，適合早午餐或晚餐",
    },
    "solsot_hongdae": {
        "name": "Solsot 釜飯 弘大延南", "name_kr": "솔솥 홍대연남점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "釜飯",
        "address": "서울 마포구 동교로38길 35",
        "lat": 37.5620, "lng": 126.9250,
        "hours": "11:30-21:00",
        "phone": "070-8822-5846",
        "note": "延南洞人氣釜飯",
    },
    "yetnaljip": {
        "name": "老房子木炭燒肉", "name_kr": "옛날집 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "木炭燒肉",
        "address": "서울 마포구 동교동 169-6",
        "lat": 37.5549, "lng": 126.9228,
        "hours": "16:00-05:00",
        "phone": "02-3141-9608",
        "note": "老字號木炭烤肉，平價飽足",
    },
    "hongdae_chungmu": {
        "name": "弘大忠武飯捲", "name_kr": "홍대충무김밥 홍대본점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "飯捲",
        "address": "서울 마포구 어울마당로 79 1층",
        "lat": 37.5545, "lng": 126.9235,
        "hours": "24h",
        "note": "弘大24小時人氣飯捲",
    },
    "sulbing_hongdae": {
        "name": "雪冰 弘大店", "name_kr": "설빙 홍대입구역점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "韓式刨冰",
        "address": "서울 마포구 홍익로6길 15 2F",
        "lat": 37.5543, "lng": 126.9241,
        "hours": "11:00-22:30",
        "phone": "02-323-3287",
        "note": "招牌黃豆粉年糕雪花冰必點",
    },
    "isaac_toast": {
        "name": "Isaac Toast 弘대", "name_kr": "이삭토스트 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "早餐",
        "address": "弘대입구역周邊",
        "lat": 37.5555, "lng": 126.9225,
        "hours": "07:00-22:00",
        "note": "韓式吐司早餐連鎖",
    },
    "eggdrop": {
        "name": "Egg Drop 弘대입구", "name_kr": "에그드랍 홍대입구점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "早餐",
        "address": "서울 마포구 홍익로 15 1층4호",
        "lat": 37.5537548, "lng": 126.9229814,
        "hours": "08:30-22:00",
        "phone": "02-6085-4371",
        "note": "韓式吐司早餐",
    },

    "moment_coffee": {
        "name": "Moment Coffee 二號", "name_kr": "모멘트커피 2호점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "咖啡早餐",
        "address": "서울 마포구 월드컵북로4길 29",
        "lat": 37.5576362, "lng": 126.9210313,
        "hours": "10:00-22:00",
        "phone": "070-8860-5287",
        "note": "自己烤吐司套餐 ₩14,000，巷弄咖啡店",
    },
    "knotted_hongdae": {
        "name": "Cafe Knotted 弘대", "name_kr": "카페 노티드 홍대",
        "area": AREA_HONGDAE, "cat": "food", "sub": "甜甜圈/早餐",
        "address": "서울 마포구 양화로 162-1",
        "lat": 37.5566, "lng": 126.9224,
        "hours": "10:00-22:00",
        "note": "弘대區內版本，10:00 開。Vanilla Cream / Milk Tea 必點",
    },

    # ================================================================
    # 弘대 — 逛 (shop)
    # ================================================================
    "olive_young_hongdae": {
        "name": "Olive Young 弘대旗艦", "name_kr": "올리브영 홍대타운",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "美妝",
        "address": "서울 마포구 홍익로6길 57",
        "lat": 37.5565733, "lng": 126.9243823,
        "hours": "週一-四 10:00-22:30 / 週五六 10:00-23:00",
        "phone": "1577-4887",
        "note": "三層樓，美妝藥妝旗艦店",
    },
    "ak_plaza": {
        "name": "AK& 弘대 (AK Plaza)", "name_kr": "AK& 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "百貨",
        "address": "서울 마포구 양화로 188",
        "lat": 37.5566, "lng": 126.9241,
        "hours": "11:00-22:00",
        "phone": "02-789-9800",
        "note": "弘대入口站 1 號出口正上方百貨，7F 是 Musinsa Terrace。"
                "B1 美食街、F2-F6 服飾品牌、F8 美食/咖啡",
    },
    "hongdae_street": {
        "name": "弘대商店街", "name_kr": "홍대 쇼핑거리",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "商圈",
        "address": "弘대 弘益路",
        "lat": 37.5550, "lng": 126.9225,
        "hours": "10:00-24:00 (店家各異)",
        "note": "弘대主街商圈，兩側全是潮店",
    },
    "musinsa_terrace_hongdae": {
        "name": "Musinsa Terrace 弘대", "name_kr": "무신사 테라스 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓本土集合品牌",
        "address": "서울 마포구 양화로 188 AK& 7층",
        "lat": 37.5566, "lng": 126.9241,
        "hours": "11:00-22:00",
        "note": "Musinsa 旗下複合店，AK& 7F。集結 100+ 韓本土小眾品牌",
    },
    "spao_hongdae": {
        "name": "SPAO 弘대旗艦", "name_kr": "SPAO 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓本土快時尚",
        "address": "서울 마포구 양화로 162",
        "lat": 37.5570, "lng": 126.9230,
        "hours": "11:00-22:00",
        "note": "韓本土 UNIQLO，弘대店 4 樓全品項，常 K-pop 聯名",
    },
    "stylenanda_hongdae": {
        "name": "Stylenanda 弘대 Pink Pool 旗艦", "name_kr": "스타일난다 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "女裝/3CE",
        "address": "서울 마포구 어울마당로 41",
        "lat": 37.5538, "lng": 126.9230,
        "hours": "11:00-22:00",
        "note": "Pink Pool Cafe + Stylenanda 服飾 + 3CE 全品項",
    },
    "abc_mart_gs": {
        "name": "ABC-MART Grand Stage", "name_kr": "ABC-MART GS 홍대 홍익로점",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "球鞋",
        "address": "홍대 홍익로",
        "lat": 37.5560, "lng": 126.9225,
        "hours": "11:00-22:00",
        "note": "GS 限定特別款",
    },
    "musinsa_hongdae": {
        "name": "MUSINSA 弘대", "name_kr": "무신사 스토어 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "潮服",
        "address": "홍대",
        "lat": 37.5560, "lng": 126.9225,
        "hours": "11:00-22:00",
        "note": "韓國版 UNIQLO / GU",
    },
    "covernat": {
        "name": "COVERNAT 弘대旗艦", "name_kr": "커버낫 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "潮服",
        "address": "서울 마포구 잔다리로 24 1F, B1F",
        "lat": 37.5520, "lng": 126.9215,
        "hours": "11:00-22:00",
        "note": "韓系街頭潮牌",
    },
    "gentle_monster": {
        "name": "GENTLE MONSTER 弘대", "name_kr": "젠틀몬스터 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "潮牌",
        "address": "서울 마포구 동막로7길 54",
        "lat": 37.5500531, "lng": 126.9200835,
        "hours": "12:00-22:00",
        "phone": "02-3144-0864",
        "note": "墨鏡",
    },
    "lmc": {
        "name": "LMC 弘大", "name_kr": "엘엠씨 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國本土潮牌",
        "address": "서울 마포구 잔다리로 27",
        "lat": 37.5511, "lng": 126.9246,
        "hours": "11:00-22:00",
        "phone": "02-336-7338",
        "note": "Oversized 剪裁 + 標語設計，帽子、包包",
    },
    "wacky_willy": {
        "name": "Wacky WiLLy 弘大", "name_kr": "와키윌리 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國本土潮牌",
        "address": "서울 마포구 잔다리로 26",
        "lat": 37.5512, "lng": 126.9245,
        "hours": "11:00-22:00",
        "phone": "070-8848-3316",
        "note": "塗鴉插畫印花",
        "priority": True,
    },
    "thisisneverthat": {
        "name": "thisisneverthat® 弘大", "name_kr": "디스이즈네버댓 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國本土潮牌",
        "address": "서울 마포구 잔다리로 32 1층 101호",
        "lat": 37.5508, "lng": 126.9248,
        "hours": "11:00-22:00",
        "phone": "070-8817-0170",
        "note": "低調酷感，T恤外套男女皆可駕馭",
    },
    "oy": {
        "name": "OY (Open Yard) 弘大", "name_kr": "오와이 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國本土潮牌",
        "address": "서울 마포구 잔다리로2길 20",
        "lat": 37.5509, "lng": 126.9250,
        "hours": "11:00-22:00",
        "phone": "0507-1378-4140",
        "note": "黑白灰基礎色調，寬版剪裁",
    },
    "yeseyesee": {
        "name": "YESEYESEE 弘大", "name_kr": "예스아이씨 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國本土潮牌",
        "address": "서울 마포구 독막로7길 47 1층",
        "lat": 37.5498, "lng": 126.9198,
        "hours": "11:00-21:00",
        "phone": "070-7500-3407",
        "note": "BTS 成員穿過，oversized 塗鴉帽T",
    },
    "lee_jeans": {
        "name": "LEE Jeans 弘大", "name_kr": "리 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "美式丹寧",
        "address": "서울 마포구 잔다리로2길 8 1F",
        "lat": 37.5513, "lng": 126.9249,
        "hours": "11:00-22:00",
        "phone": "0507-1431-8560",
        "note": "Lee 美式丹寧",
    },
    "worksout": {
        "name": "WORKSOUT 弘大", "name_kr": "웍스아웃 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "聯合進口潮牌",
        "address": "서울 마포구 양화로 130",
        "lat": 37.5557, "lng": 126.9222,
        "hours": "12:00-21:00",
        "phone": "02-337-8334",
        "note": "品牌集合，服裝鞋子配件",
    },
    "turtle_glass": {
        "name": "TURTLE GLASS 弘大", "name_kr": "터틀글래스 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "男裝",
        "address": "서울 마포구 양화로15길 17 5층",
        "lat": 37.5540, "lng": 126.9186,
        "hours": "12:00-22:00",
        "phone": "0507-1465-0626",
        "note": "成熟簡約男裝",
    },
    "mark_gonzales": {
        "name": "MARK GONZALES 弘大", "name_kr": "마크 곤잘레스 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "滑板潮牌",
        "address": "서울 마포구 어울마당로 133",
        "lat": 37.5531, "lng": 126.9238,
        "hours": "11:00-22:00",
        "note": "塗鴉插畫風滑板系潮牌",
    },
    "nerdy": {
        "name": "NERDY 弘大旗艦店", "name_kr": "너디 홍대 플래그십",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國本土潮牌",
        "address": "서울 마포구 어울마당로 94-12",
        "lat": 37.5525, "lng": 126.9234,
        "hours": "11:00-22:00",
        "note": "韓系插畫風 LOGO 潮牌，帽子短T",
    },
    "nerdy_hongdae": {
        "name": "NERDY 弘大旗艦 (新版)", "name_kr": "널디 플래그쉽 홍대점",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國運動潮牌",
        "address": "서울 마포구 홍익로6길 27",
        "lat": 37.5543, "lng": 126.9241,
        "hours": "12:00-21:00",
        "phone": "02-332-9466",
        "note": "韓國人氣潮牌，紫色室內設計打卡感強，IU、APINK成員都在穿",
    },
    "wonder_place": {
        "name": "Wonder Place 弘大", "name_kr": "원더플레이스 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "潮牌集合店",
        "address": "서울 마포구 양화로 176 스타피카소 1층",
        "lat": 37.5562, "lng": 126.9237,
        "hours": "11:00-22:00",
        "note": "韓國本土潮牌多品牌集合，帽子包包",
    },
    "hongik_pharmacy": {
        "name": "弘益藥局", "name_kr": "홍익약국",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "藥妝",
        "address": "서울 마포구 양화로18길 7 1층",
        "lat": 37.5563, "lng": 126.9229,
        "hours": "09:00-23:30",
        "phone": "02-337-5414",
        "note": "弘大最知名藥妝藥局，有中文服務、即時退稅",
    },

    # ================================================================
    # 延南洞 — 食 (food)
    # ================================================================
    "jo_dawson": {
        "name": "JO & DAWSON 法式吐司", "name_kr": "조앤도슨 연남본점",
        "area": AREA_YEONNAM, "cat": "food", "sub": "甜點",
        "address": "서울 마포구 동교로41길 31 지층",
        "lat": 37.5636203, "lng": 126.9232494,
        "hours": "10:00-20:00",
        "note": "首爾最強法式吐司，茶葉自己烘",
        "priority": True,
    },
    "pungcheon": {
        "name": "風川鰻魚", "name_kr": "풍천장어 연남점",
        "area": AREA_YEONNAM, "cat": "food", "sub": "鰻魚",
        "address": "서울 마포구 동교로27길 39 1층",
        "lat": 37.5595384, "lng": 126.9215438,
        "hours": "11:30-15:30 / 16:30-22:20",
        "phone": "02-332-8361",
        "note": "炭火鰻魚，菜單只有一道",
        "priority": True,
    },
    "tongin_donkatsu_yeonnam": {
        "name": "Tongin 豬排 延南本店", "name_kr": "카츠몬스터 연남본점",
        "area": AREA_YEONNAM, "cat": "food", "sub": "日式豬排",
        "address": "서울 마포구 동교로38길 42-6 1층",
        "lat": 37.561017, "lng": 126.92549,
        "hours": "10:30-21:00",
        "phone": "070-7604-1382",
        "note": "延南洞日式豬排排隊店，三層厚切 ₩18,000",
    },
    "cafe_le_nuage_yeonnam": {
        "name": "Cafe Le Nuage 延南", "name_kr": "르 누아주 카페",
        "area": AREA_YEONNAM, "cat": "food", "sub": "法式甜點",
        "address": "서울 마포구 동교로46길 42-9",
        "lat": 37.5617296, "lng": 126.926669,
        "hours": "週三休 / 平日 12:00-21:00, 週末 11:00-21:00",
        "phone": "010-8989-7396",
        "note": "手工法式甜點，藝術品級的可頌/塔",
    },
    "knotted_yeonnam": {
        "name": "Cafe Knotted 延南", "name_kr": "카페 노티드 연남",
        "area": AREA_YEONNAM, "cat": "food", "sub": "甜甜圈/早餐",
        "address": "서울 마포구 동교로 250-1",
        "lat": 37.5634216, "lng": 126.9245378,
        "hours": "11:00-22:00",
        "note": "韓國奶油甜甜圈元祖。Vanilla Cream / Milk Tea 必點",
    },
    "nognog_yeonnam": {
        "name": "Cafe Nognog 延南", "name_kr": "녹녹 연남",
        "area": AREA_YEONNAM, "cat": "food", "sub": "咖啡/麵包",
        "address": "서울 마포구 성미산로 139 1층",
        "lat": 37.5638331, "lng": 126.9219365,
        "hours": "08:30-01:00",
        "phone": "010-2533-5953",
        "note": "延南洞早餐救星 08:30 開。兩層樓 + 大量插座 + 平價咖啡",
    },
    "camellia_yeonnam": {
        "name": "Camellia 延南", "name_kr": "카멜리아 연남",
        "area": AREA_YEONNAM, "cat": "food", "sub": "早午餐",
        "address": "서울 마포구 동교로45길 8 1층",
        "lat": 37.5645, "lng": 126.9225,
        "hours": "10:00-20:00",
        "note": "歐洲風早午餐，餐盤超美",
    },

    # ================================================================
    # 延南洞 — 逛 / 景 (shop / sight)
    # ================================================================
    "yeon_throughvintage": {
        "name": "연트럴빈티지 (Yeon Through Vintage)", "name_kr": "연트럴빈티지",
        "area": AREA_YEONNAM, "cat": "shop", "sub": "二手丹寧/Polo",
        "address": "서울 마포구 연남동 259-5",
        "lat": 37.561024, "lng": 126.9241166,
        "hours": "24h 開",
        "phone": "010-9518-2864",
        "note": "延南洞最大 vintage 店。Ralph Lauren / Tommy / Champion 二手丹寧均一 ₩10,000 起",
        "priority": True,
    },
    "yeonnam_vintage": {
        "name": "延南 Vintage Sky", "name_kr": "연남 빈티지",
        "area": AREA_YEONNAM, "cat": "shop", "sub": "復古二手",
        "address": "서울 마포구 양화로21길 37",
        "lat": 37.5597525, "lng": 126.9242805,
        "hours": "00:00-21:00 (週六日到 22:00)",
        "phone": "010-3078-0650",
        "note": "巷弄裡的二手店，復古夾克 / 工裝褲 ₩30,000~",
    },
    "some_store_yeonnam": {
        "name": "Some Store 延南", "name_kr": "섬스토어 (Some Store)",
        "area": AREA_YEONNAM, "cat": "shop", "sub": "選物vintage",
        "address": "서울 마포구 성미산로 155 2층",
        "lat": 37.5644905, "lng": 126.9235681,
        "hours": "週末為主，依 Instagram 公告",
        "note": "極簡店主精選 vintage，襯衫 / 工裝褲 / 包品質好",
    },
    "gyeongui_park": {
        "name": "京義線林蔭道", "name_kr": "경의선숲길",
        "area": AREA_YEONNAM, "cat": "sight",
        "address": "서울 마포구 연남동",
        "lat": 37.5610, "lng": 126.9230,
        "hours": "24h",
        "note": "廢棄鐵道改的線狀公園，連接弘대-延南",
    },

    # ================================================================
    # 望遠 — 食 / 景
    # ================================================================
    "mangwon_market": {
        "name": "望遠市場", "name_kr": "망원시장",
        "area": AREA_MANGWON, "cat": "sight",
        "address": "서울 마포구 망원동",
        "lat": 37.5559018, "lng": 126.9062854,
        "hours": "09:00-21:00",
        "phone": "02-335-3591",
        "note": "弘대走路 20min / 6 號線 1 站",
    },
    "uirak": {
        "name": "雨耳樂炸辣椒", "name_kr": "우이락 망원본점",
        "area": AREA_MANGWON, "cat": "food", "sub": "小吃",
        "address": "서울 마포구 포은로8길 22",
        "lat": 37.556453, "lng": 126.9059867,
        "hours": "11:00-22:00",
        "note": "炸辣椒配啤酒，望遠市場名店",
    },
    "matjib": {
        "name": "好吃的店 (血腸/年糕)", "name_kr": "맛있는집",
        "area": AREA_MANGWON, "cat": "food", "sub": "小吃",
        "address": "서울 마포구 망원로8길 30",
        "lat": 37.5561438, "lng": 126.906064,
        "hours": "10:00-22:00 (週一公休)",
        "phone": "02-326-2143",
        "note": "炸魷魚飯捲、辣炒年糕、魚板湯",
    },
    "mangwon_croquette": {
        "name": "Mangwon Croquette 望遠可樂餅", "name_kr": "망원 고로케",
        "area": AREA_MANGWON, "cat": "food", "sub": "炸物可樂餅",
        "address": "서울 마포구 망원로 80",
        "lat": 37.5573301, "lng": 126.9056676,
        "hours": "09:00-21:00 (週六日休)",
        "phone": "02-336-7412",
        "note": "望遠市場地標。馬鈴薯沙拉可樂餅，10:00 出爐最熱",
    },
    "kyuseu_chicken": {
        "name": "Kyuseu 炸雞 望遠", "name_kr": "큐스 치킨 망원",
        "area": AREA_MANGWON, "cat": "food", "sub": "市場炸雞",
        "address": "서울 마포구 망원로8길 27",
        "lat": 37.5562557, "lng": 126.9062372,
        "hours": "10:00-20:30",
        "phone": "02-3143-5577",
        "note": "炸雞排隊店，多口味混搭 ₩3,000 起",
    },
    "kimchi_wang_mandu": {
        "name": "傳說的王餃子 望遠", "name_kr": "전설의 왕만두 망원시장",
        "area": AREA_MANGWON, "cat": "food", "sub": "蒸餃",
        "address": "57-300 망원동",
        "lat": 37.555484, "lng": 126.9077308,
        "hours": "週二休 / 09:30-22:30",
        "note": "市場入口的招牌蒸餃，泡菜豬肉口味必點",
    },
    "yeon_mandu": {
        "name": "Yeon Mandu 望遠手工蒸餃", "name_kr": "연만두",
        "area": AREA_MANGWON, "cat": "food", "sub": "手工蒸餃",
        "address": "486-8 망원동 1층",
        "lat": 37.5566483, "lng": 126.9061569,
        "hours": "週日休 / 11:00-19:00",
        "phone": "02-332-5555",
        "note": "薄皮 + 紮實餡，⚠️ 只外帶",
    },

    # ================================================================
    # 聖水 — 食 (food)
    # ================================================================
    "gamjatang": {
        "name": "聖水馬鈴薯排骨湯", "name_kr": "소문난성수감자탕",
        "area": AREA_SEONGSU, "cat": "food", "sub": "馬鈴薯排骨湯",
        "address": "서울 성동구 연무장길 45",
        "lat": 37.5428241, "lng": 127.0543732,
        "hours": "24h 不打烊",
        "phone": "02-465-6580",
        "note": "吃到一半丟手打麵下湯",
        "priority": True,
    },
    "maman_gelato": {
        "name": "Maman Gelato 聖水", "name_kr": "마망 젤라또 성수",
        "area": AREA_SEONGSU, "cat": "food", "sub": "義式冰淇淋",
        "address": "서울 성동구 연무장9길 8 1층",
        "lat": 37.5429349, "lng": 127.0559738,
        "hours": "11:30-21:00",
        "phone": "02-466-3373",
        "note": "Pistachiotella 開心果＋Nutella ₩9,000",
        "priority": True,
    },
    "somunnan_byeolgwan": {
        "name": "聲名遠播聖水馬鈴薯排骨 別館", "name_kr": "소문난 성수 감자탕 별관",
        "area": AREA_SEONGSU, "cat": "food", "sub": "馬鈴薯排骨湯",
        "address": "서울 성동구 연무장7길 4",
        "lat": 37.5429616, "lng": 127.0545924,
        "hours": "11:00-22:00",
        "phone": "02-499-2500",
        "note": "本店隔壁。等不到本店就來這間。湯底一樣，最後用紫蘇葉炒飯收尾",
    },
    "knotted_seongsu": {
        "name": "Cafe Knotted 聖水", "name_kr": "카페 노티드 성수",
        "area": AREA_SEONGSU, "cat": "food", "sub": "甜甜圈",
        "address": "서울 성동구 성수동2가 316-5",
        "lat": 37.5435787, "lng": 127.0526642,
        "hours": "11:00-21:00",
        "phone": "070-8834-9377",
        "note": "Knotted 帶起韓國奶油甜甜圈熱潮的元祖。聖水店主打外帶",
    },
    "cafe_onion_seongsu": {
        "name": "Cafe Onion 聖水", "name_kr": "카페 어니언 성수",
        "area": AREA_SEONGSU, "cat": "food", "sub": "咖啡/烘焙",
        "address": "서울 성동구 아차산로9길 8",
        "lat": 37.5447328, "lng": 127.0582091,
        "hours": "平日 08:00-22:00 / 週末 09:00-22:00",
        "note": "Onion 元祖店，工廠改裝廢墟風。麵包選擇多 (Pandoro 招牌)",
    },
    "nudake_teahouse": {
        "name": "Nudake Teahouse 聖水", "name_kr": "누데이크 티하우스",
        "area": AREA_SEONGSU, "cat": "food", "sub": "下午茶/甜點",
        "address": "서울 성동구 뚝섬로 433 5층",
        "lat": 37.5381263, "lng": 127.0588978,
        "hours": "11:00-21:00",
        "phone": "1660-1010",
        "note": "Gentle Monster 旗下，藝術系下午茶",
    },
    "maple_top_pancake": {
        "name": "Maple Top Pancake Club", "name_kr": "메이플탑 팬케이크 클럽",
        "area": AREA_SEONGSU, "cat": "food", "sub": "美式早餐",
        "address": "서울 성동구 성수이로14길 14",
        "lat": 37.5415153, "lng": 127.0569694,
        "hours": "平日 09:00-18:00 / 週末 09:00-19:00",
        "phone": "02-3789-4427",
        "note": "美式早午餐風格，鬆餅+楓糖+培根",
    },
    "song_gye_ok_seongsu": {
        "name": "松溪屋 聖水店", "name_kr": "송계옥 성수점",
        "area": AREA_SEONGSU, "cat": "food", "sub": "炭火烤雞",
        "address": "서울 성동구 아차산로11길 11",
        "lat": 37.5447394, "lng": 127.0593341,
        "hours": "平日 16:00-22:00 / 週末 15:00-22:00",
        "note": "炭火烤雞老店，雞心特推。建議先用 Catchtable 取號",
    },
    "ssoc_restaurant": {
        "name": "SSOC", "name_kr": "쏙",
        "area": AREA_SEONGSU, "cat": "food", "sub": "韓式法餐",
        "address": "서울 성동구 광나루로4가길 12-7",
        "lat": 37.5491463, "lng": 127.0543631,
        "hours": "週一公休｜其他 11:30-15:00 / 17:00-22:00",
        "phone": "02-6212-1195",
        "note": "前米其林一星主廚，韓食 + 法式技巧。建議訂位",
    },

    # ================================================================
    # 聖水 — 逛 (shop)
    # ================================================================
    "blue_elephant_seongsu": {
        "name": "BLUE ELEPHANT 聖水旗艦", "name_kr": "블루엘리펀트 성수 플래그십",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "墨鏡/眼鏡",
        "address": "서울 성동구 연무장길 13 2-3층",
        "lat": 37.5437612, "lng": 127.0511603,
        "hours": "12:00-22:00",
        "note": "首爾最大間，鏡框均一價 ~₩49,000，設計類似 Gentle Monster 但價格 1/3",
        "priority": True,
    },
    "musinsa_standard_seongsu": {
        "name": "Musinsa Standard 聖水", "name_kr": "무신사 스탠다드 성수",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "韓系基本款衣服",
        "address": "서울 성동구 성수이로 12",
        "lat": 37.5415471, "lng": 127.058537,
        "hours": "11:00-22:00",
        "phone": "0507-1872-3708",
        "note": "韓版 UNIQLO/GU，極簡乾淨風",
    },
    "kasina_seongsu": {
        "name": "Kasina 聖水", "name_kr": "카시나 성수",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "球鞋選物",
        "address": "서울 성동구 성수이로7길 41",
        "lat": 37.5425947, "lng": 127.0531067,
        "hours": "11:00-20:00",
        "phone": "070-7777-1771",
        "note": "1F 球鞋 (Nike / Adidas / Salomon 限定款少見配色)，2F 服裝",
    },
    "covernat_seongsu": {
        "name": "Covernat 聖水旗艦", "name_kr": "커버낫 성수 플래그십",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "街頭潮牌",
        "address": "서울 성동구 연무장길 37",
        "lat": 37.5430829, "lng": 127.0536515,
        "hours": "11:00-21:00",
        "phone": "070-4176-5041",
        "note": "潮牌",
    },
    "kodak_corner_shop": {
        "name": "Kodak Apparel Corner Shop", "name_kr": "코닥 코너샵 성수",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "復古衣著",
        "address": "서울 성동구 성수동2가 316-62",
        "lat": 37.5431112, "lng": 127.0543075,
        "hours": "10:30-20:30",
        "phone": "0507-1354-7297",
        "note": "Kodak Apparel 旗艦店，兩層樓。T-shirt / 帽子 / 帽 T 為主",
    },
    "thisisneverthat_seongsu": {
        "name": "thisisneverthat 聖水旗艦", "name_kr": "디스이즈네버댓 성수",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "街頭潮牌",
        "address": "서울 성동구 성수동2가 277-121 3층",
        "lat": 37.5431463, "lng": 127.0616649,
        "hours": "11:00-20:00",
        "phone": "010-5697-0170",
        "note": "T 恤 / 帽 T / 夾克 / 工裝褲",
    },
    "matin_kim_seongsu": {
        "name": "Matin Kim 聖水旗艦", "name_kr": "마뗑킴 성수 플래그십",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "韓系女裝",
        "address": "서울 성동구 성수동2가 301-16",
        "lat": 37.5445496, "lng": 127.051323,
        "hours": "11:00-20:00",
        "phone": "070-4128-0703",
        "note": "明星愛用韓系設計師品牌。後方有 outlet 折扣區",
    },
    "ader_error_seongsu": {
        "name": "ADER ERROR 聖水", "name_kr": "아더에러 성수",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "前衛潮牌",
        "address": "서울 성동구 성수이로 82",
        "lat": 37.5422211, "lng": 127.0565311,
        "hours": "11:00-21:00",
        "phone": "02-2039-0334",
        "note": "店面當代藝術裝置概念，T-shirt / 衛衣 ₩90,000+ 偏貴一階",
    },

    # ================================================================
    # 東大門 / 廣藏 — 食 / 景
    # ================================================================
    "jin_okhwa": {
        "name": "陳玉華一隻雞 元祖", "name_kr": "진옥화할매원조닭한마리",
        "area": AREA_DONGDAEMUN, "cat": "food", "sub": "一隻雞",
        "address": "서울 종로구 종로40가길 18",
        "lat": 37.5703627, "lng": 127.0057612,
        "hours": "10:30-01:00",
        "phone": "02-2275-9666",
        "note": "Tip：先丟馬鈴薯+蒜+蔥，最後加手打麵",
        "priority": True,
    },
    "myungdong_chicken": {
        "name": "明洞一隻雞", "name_kr": "명동닭한마리 본점",
        "area": AREA_DONGDAEMUN, "cat": "food", "sub": "一隻雞",
        "address": "서울 종로구 종로40가길 14",
        "lat": 37.5703, "lng": 127.0057,
        "hours": "10:00-00:30",
        "phone": "02-2266-8249",
        "note": "陳玉華隔壁的姊妹店",
    },
    "gwangjang": {
        "name": "廣藏市場", "name_kr": "광장시장",
        "area": AREA_DONGDAEMUN, "cat": "sight",
        "address": "서울 종로구 청계천로 88",
        "lat": 37.5700398, "lng": 126.9996036,
        "hours": "09:00-22:30",
        "phone": "02-2267-0291",
        "note": "麻藥飯捲、綠豆煎餅、生牛肉",
    },

    # ================================================================
    # 安國 / 北村 / 西村 — 景 + 食
    # ================================================================
    "gwanghwamun": {
        "name": "光化門", "name_kr": "광화문",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 사직로 161",
        "lat": 37.5760111, "lng": 126.9768611,
        "hours": "24h (景福宮 09:00-17:00)",
        "phone": "02-3700-3900",
        "note": "11:00 守門將交班儀式必看",
    },
    "gyeongbokgung": {
        "name": "景福宮", "name_kr": "경복궁",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 사직로 161",
        "lat": 37.579617, "lng": 126.977041,
        "hours": "09:00-17:00 (週二公休)",
        "phone": "02-3700-3900",
        "note": "穿韓服免門票 ₩3,000",
    },
    "bukchon": {
        "name": "北村韓屋村", "name_kr": "북촌 한옥마을",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 계동길 37",
        "lat": 37.5814696, "lng": 126.9849519,
        "hours": "10:00-17:00 (居民區，請輕聲)",
        "phone": "02-2133-1371",
        "note": "傳統韓屋拍照景點，超過 17 點請離開",
    },
    "insadong": {
        "name": "仁寺洞", "name_kr": "인사동",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 인사동",
        "lat": 37.5720, "lng": 126.9858,
        "hours": "10:00-22:00 (店家各異)",
        "note": "傳統工藝品/紀念品街",
    },
    "samcheongdong": {
        "name": "三清洞", "name_kr": "삼청동",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 삼청동",
        "lat": 37.5827, "lng": 126.9817,
        "hours": "全天 (店家不一)",
        "note": "藍瓶咖啡三清店在此",
    },
    "cafe_onion_anguk": {
        "name": "Cafe Onion Anguk", "name_kr": "어니언 안국점",
        "area": AREA_ANGUK, "cat": "food", "sub": "咖啡早餐",
        "address": "서울 종로구 계동길 5",
        "lat": 37.5776235, "lng": 126.9865541,
        "hours": "週一-五 07:00-22:00 / 週末 09:00-22:00",
        "phone": "070-7543-2123",
        "note": "韓屋風咖啡店",
    },
    "muguok": {
        "name": "無垢屋蔘雞湯", "name_kr": "무구옥",
        "area": AREA_ANGUK, "cat": "food", "sub": "蔘雞湯",
        "address": "서울 종로구 율곡로1길 7 지상1층",
        "lat": 37.5763898, "lng": 126.9799003,
        "hours": "11:30-14:00 / 17:30-20:00",
        "note": "Catchtable 登記，下午 14-17 不開",
        "priority": True,
    },
    "tosokchon": {
        "name": "土俗村蔘雞湯", "name_kr": "토속촌삼계탕",
        "area": AREA_ANGUK, "cat": "food", "sub": "蔘雞湯",
        "address": "서울 종로구 자하문로5길 5",
        "lat": 37.5777786, "lng": 126.9715909,
        "hours": "10:00-22:00",
        "phone": "02-737-7444",
        "note": "無垢屋備案，黑骨雞蔘雞湯為招牌",
    },
    "rafre_fruit_seochon": {
        "name": "Rafre Fruit 西村", "name_kr": "라프레 프루트 서촌",
        "area": AREA_ANGUK, "cat": "food", "sub": "草莓/水果甜點",
        "address": "서울 종로구 필운대로 53-30 2층",
        "lat": 37.5807919, "lng": 126.9679653,
        "hours": "12:30-18:30 (週六日到 19:30)",
        "phone": "0507-1387-7415",
        "note": "草莓蛋糕、濟州蘋果芒果刨冰、新鮮草莓拿鐵。"
                "Catchtable 抽號碼。從景福宮西邊走 11 min",
        "priority": True,
    },
    "tongin_market": {
        "name": "通仁市場 銅板便當", "name_kr": "통인시장 도시락카페",
        "area": AREA_ANGUK, "cat": "food", "sub": "傳統市場",
        "address": "서울 종로구 자하문로15길 18",
        "lat": 37.5807649, "lng": 126.9706756,
        "hours": "07:00-21:00 (便當咖啡週二休)",
        "phone": "02-722-0911",
        "note": "在 Rafre 隔壁巷子。₩10,000 換 20 個銅板，拿便當盒去攤位用銅板換菜",
    },
    "london_bagel": {
        "name": "倫敦貝果博物館 安國", "name_kr": "런던베이글뮤지엄 안국",
        "area": AREA_ANGUK, "cat": "food", "sub": "甜點麵包",
        "address": "서울 종로구 북촌로4길 20",
        "lat": 37.5791826, "lng": 126.9861520,
        "hours": "07:00-18:00",
        "note": "⚠️ Catchtable 抽號碼牌，可能等 2 小時",
    },

    # ================================================================
    # 益善洞 — 食 / 景
    # ================================================================
    "ikseondong": {
        "name": "益善洞韓屋村", "name_kr": "익선동 한옥마을",
        "area": AREA_IKSEON, "cat": "sight",
        "address": "서울 종로구 익선동",
        "lat": 37.5737132, "lng": 126.9901271,
        "hours": "10:00-21:00 (店家各異)",
        "phone": "02-2148-5243",
        "note": "韓屋變咖啡街，韓劇鬼怪取景",
    },
    "soha_salt": {
        "name": "小夏鹽田鹽可頌", "name_kr": "소하염전소금빵 익선동",
        "area": AREA_IKSEON, "cat": "food", "sub": "麵包",
        "address": "서울 종로구 수표로28길 21-5",
        "lat": 37.5730739, "lng": 126.9896949,
        "hours": "09:00-20:30",
        "note": "鹽可頌，建議早上去",
    },
    "mil_toast": {
        "name": "Mil Toast 益善", "name_kr": "밀토스트 익선",
        "area": AREA_IKSEON, "cat": "food", "sub": "甜點",
        "address": "서울 종로구 수표로28길 30-3",
        "lat": 37.5731192, "lng": 126.9903425,
        "hours": "08:00-22:00",
        "phone": "02-766-0627",
        "note": "手撕吐司",
    },
    "solsot": {
        "name": "Solsot 釜飯 益善", "name_kr": "솔솥 익선동",
        "area": AREA_IKSEON, "cat": "food", "sub": "韓食",
        "address": "서울 종로구 삼일대로30길 46 1층",
        "lat": 37.5742323, "lng": 126.9901823,
        "hours": "11:00-21:00",
        "phone": "010-9960-7113",
        "note": "釜飯名店，鰻魚/牛排/鯛魚口味",
    },
    "hanok_langsom_ikseon": {
        "name": "Hanok Langsom 益善", "name_kr": "한옥낭솜 익선",
        "area": AREA_IKSEON, "cat": "food", "sub": "韓屋咖啡",
        "address": "서울 종로구 수표로28길 21-6 1층",
        "lat": 37.5731833, "lng": 126.9898614,
        "hours": "10:30-22:00 (週六 9:00 開)",
        "note": "韓屋庭院咖啡。推 Cafe Vienna (奶霜不甜，記得攪)",
    },

    # ================================================================
    # 明洞 — 食 (food)
    # ================================================================
    "myeongdong_kyoja": {
        "name": "明洞餃子 (米其林)", "name_kr": "명동교자",
        "area": AREA_MYEONGDONG, "cat": "food", "sub": "刀削麵",
        "address": "서울 중구 명동10길 29",
        "lat": 37.5625266, "lng": 126.985609,
        "hours": "10:30-21:30",
        "phone": "02-776-5348",
        "note": "米其林必比登",
    },
    "hyodam_dakhanmari": {
        "name": "孝潭刀削麵一隻雞 明洞", "name_kr": "효담칼국수닭한마리 명동",
        "area": AREA_MYEONGDONG, "cat": "food", "sub": "一隻雞",
        "address": "서울 중구 명동3길 12 B1",
        "lat": 37.5642308, "lng": 126.9835303,
        "hours": "10:30-22:15",
        "phone": "02-318-2468",
        "note": "刀削麵 + 一隻雞鍋",
    },
    "menten_ramen": {
        "name": "Menten 拉麵", "name_kr": "멘텐 라멘",
        "area": AREA_MYEONGDONG, "cat": "food", "sub": "日式拉麵",
        "address": "서울 중구 삼일대로 305",
        "lat": 37.5619547, "lng": 126.9885760,
        "hours": "週一、日休 / 平日 11:40-14:30, 17:40-19:30",
        "note": "明洞 8 席拉麵秘藏，醬油拉麵主推，要兩顆蛋",
    },
    "myeongdong_hotteok": {
        "name": "明洞糖餅小推車", "name_kr": "명동 호떡 (수제)",
        "area": AREA_MYEONGDONG, "cat": "food", "sub": "街頭糖餅",
        "address": "서울 중구 명동 25-11",
        "lat": 37.5611754, "lng": 126.9818543,
        "hours": "12:00-21:00",
        "note": "明洞街頭老奶奶家傳糖餅，鐵盤烤不油炸",
    },
    "hwa_tteok_gopchang": {
        "name": "和炒章魚血腸炒年糕", "name_kr": "화떡 곱창떡볶이 명동",
        "area": AREA_MYEONGDONG, "cat": "food", "sub": "辣炒年糕",
        "address": "서울 중구 명동4길 15",
        "lat": 37.5630129, "lng": 126.9838039,
        "hours": "週一休｜其他 11:00-22:00",
        "note": "辣炒年糕",
    },

    # ================================================================
    # 明洞 — 逛 (shop)
    # ================================================================
    "shinsegae_main": {
        "name": "新世界百貨 本店", "name_kr": "신세계백화점 본점",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "百貨/免稅",
        "address": "서울 중구 소공로 63",
        "lat": 37.5609223, "lng": 126.9811389,
        "hours": "10:30-20:00 (週五六到 20:30)",
        "phone": "1588-1234",
        "note": "3 棟相連 25 層 (Estate / Reserve / Heritage)。"
                "8-11F 免稅店 (要先在 app 預約)。B1 美食街 / 巴黎可頌排隊名店。退稅 1F 服務中心",
        "priority": True,
    },
    "abc_mart_grand_myeongdong": {
        "name": "ABC-MART Grand Stage 明洞", "name_kr": "ABC마트 GS 명동본점",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "球鞋",
        "address": "서울 중구 명동8나길 21",
        "lat": 37.5611017, "lng": 126.9838034,
        "hours": "10:30-22:00",
        "phone": "02-2088-0981",
        "note": "Grand Stage 旗艦 (弘대那家是普通 GS 店)",
    },
    "nike_myeongdong": {
        "name": "NIKE 明洞 (樂天百貨 6F)", "name_kr": "나이키 명동 (롯데백화점 6층)",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "運動服飾",
        "address": "서울 중구 남대문로 73 6층",
        "lat": 37.5641503, "lng": 126.9816366,
        "hours": "10:30-20:00 (週五六到 20:30)",
        "phone": "02-772-3689",
        "note": "Nike By You 客製化體驗",
    },
    "adidas_brand_myeongdong": {
        "name": "adidas Brand Flagship Seoul", "name_kr": "아디다스 브랜드 플래그십 서울",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "運動服飾",
        "address": "서울 중구 명동8길 27",
        "lat": 37.5624994, "lng": 126.9851619,
        "hours": "10:30-22:00",
        "phone": "02-779-9834",
        "note": "Made For You 客製化，現場印製 20 min 內取貨",
    },
    "zara_myeongdong": {
        "name": "ZARA 明洞 Noon Square 旗艦", "name_kr": "ZARA 명동 눈스퀘어",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "快時尚",
        "address": "서울 중구 명동길 14",
        "lat": 37.5635068, "lng": 126.9825028,
        "hours": "10:30-22:00",
        "note": "旗艦三層樓，有限定款",
    },
    "hm_myeongdong": {
        "name": "H&M 明洞中央街", "name_kr": "H&M 명동중앙길",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "快時尚",
        "address": "서울 중구 명동8길 3",
        "lat": 37.5635451, "lng": 126.9848038,
        "hours": "10:30-22:30",
        "note": "4 層樓全品項",
    },
    "uniqlo_myeongdong": {
        "name": "UNIQLO 明洞中央店", "name_kr": "유니클로 명동중앙점",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "基本款",
        "address": "서울 중구 명동8나길 38",
        "lat": 37.5615693, "lng": 126.9826829,
        "hours": "11:00-21:00",
        "phone": "02-755-1215",
        "note": "韓國 UNIQLO 跟日本一樣有 UT 聯名 (BTS / 跑跑卡丁車韓限)",
    },
    "spao_myeongdong": {
        "name": "SPAO 明洞旗艦", "name_kr": "SPAO 명동 플래그십",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "韓本土快時尚",
        "address": "서울 중구 명동8나길 15",
        "lat": 37.5612589, "lng": 126.9841176,
        "hours": "10:00-22:00",
        "phone": "02-319-3850",
        "note": "韓國本土 UNIQLO，常有 K-pop / 韓劇聯名",
    },
    "eightseconds_myeongdong": {
        "name": "8 Seconds 明洞旗艦", "name_kr": "에잇세컨즈 명동 플래그십",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "韓本土快時尚",
        "address": "서울 중구 명동길 32",
        "lat": 37.5636186, "lng": 126.9840524,
        "hours": "10:30-22:00",
        "phone": "070-7090-2272",
        "note": "Samsung 集團韓本土快時尚，常 K-pop 聯名",
    },
    "doota_mall": {
        "name": "DOOTA Mall 東大門", "name_kr": "두타몰",
        "area": AREA_MYEONGDONG, "cat": "shop", "sub": "潮牌賣場",
        "address": "서울 중구 장충단로 275",
        "lat": 37.5691608, "lng": 127.0090397,
        "hours": "10:30-24:00",
        "phone": "02-3398-3333",
        "note": "從明洞搭 4 號線 1 站到東大門。外國人退稅快、Olive Young 超大間",
    },

    # ================================================================
    # 機場 — Day 5 用
    # ================================================================
    "icn_t2_checkin_lj": {
        "name": "ICN T2 真航空報到櫃台", "name_kr": "진에어 체크인 카운터",
        "area": AREA_AIRPORT, "cat": "sight", "sub": "報到櫃台",
        "address": "인천공항 T2 3F 출국장",
        "lat": 37.4602, "lng": 126.4407,
        "hours": "起飛前 2.5h 開放，前 40 min 截止",
        "note": "⭐ LJ737 → F 或 H 區櫃台。12:50 開放、14:10 截止。建議 13:00 前到櫃台",
        "priority": True,
    },
    "icn_t2_taxrefund_kiosk_landside": {
        "name": "ICN T2 退稅 KIOSK (報到前)", "name_kr": "택스 리펀드 (출국장)",
        "area": AREA_AIRPORT, "cat": "sight", "sub": "退稅自助機",
        "address": "인천공항 T2 3F 출국장 F/H 카운터 옆",
        "lat": 37.4602, "lng": 126.4407,
        "hours": "24h 自助機 / 人工 7:00-21:30",
        "note": "🚨 報到前先來這裡。3F F 或 H 櫃台旁。掃護照 → 掃退稅單 → 若顯示「需海關檢查」帶商品去海關蓋章",
    },
    "icn_t2_taxrefund_cash_249": {
        "name": "ICN T2 退稅領現金 Gate 249", "name_kr": "택스 환급 현금 수령 249",
        "area": AREA_AIRPORT, "cat": "sight", "sub": "退稅領錢",
        "address": "인천공항 T2 3F 면세구역 249번 게이트 부근",
        "lat": 37.4603, "lng": 126.4413,
        "hours": "24h 自助機 / 人工 7:00-21:30",
        "note": "⭐ 過安檢後最重要的一站。自助機掃退稅單 → 選「現金」或「退信用卡」",
        "priority": True,
    },
    "icn_t2_duty_pickup": {
        "name": "ICN T2 免稅品提貨 (整合取號機)", "name_kr": "면세품 인도장",
        "area": AREA_AIRPORT, "cat": "sight", "sub": "免稅品提貨",
        "address": "인천공항 T2 3F 면세구역 248-253번 게이트 부근",
        "lat": 37.4603, "lng": 126.4415,
        "hours": "06:30-21:30",
        "note": "⭐ 出境後找「自動取號機」掃護照 → 印出整合號碼牌 (樂天/新羅/新世界/SM 共用)",
        "priority": True,
    },
    "shake_shack_t2": {
        "name": "Shake Shack 仁川 T2", "name_kr": "쉐이크쉑 인천공항 T2",
        "area": AREA_AIRPORT, "cat": "food", "sub": "美式漢堡",
        "address": "인천공항 T2 3F 면세구역 (Gate 28 附近)",
        "lat": 37.4604, "lng": 126.4419,
        "hours": "06:00-21:00",
        "phone": "032-743-0100",
        "note": "免稅區內。Smoke Shack 漢堡 + 起司薯條 ~₩20,000。早班限定餐點 06:00-10:00",
    },
    "gentle_monster_t2": {
        "name": "Gentle Monster T2", "name_kr": "젠틀몬스터 인천공항 T2",
        "area": AREA_AIRPORT, "cat": "shop", "sub": "墨鏡",
        "address": "인천공항 T2 3F 면세구역 28번 게이트 부근",
        "lat": 37.4603, "lng": 126.4413,
        "hours": "07:00-21:30",
        "note": "免稅區墨鏡買最划算 (比市區便宜 10-20%)",
    },
    "paris_baguette_t2": {
        "name": "Paris Baguette T2 仁川你好餅乾", "name_kr": "파리바게뜨 인천공항 T2",
        "area": AREA_AIRPORT, "cat": "food", "sub": "餅乾伴手禮",
        "address": "인천공항 T2 3F 면세구역 12번 게이트 부근",
        "lat": 37.4605, "lng": 126.4400,
        "hours": "06:00-21:00",
        "note": "「仁川你好」奶油餅乾 機場限定，每人限購 2 盒。建議過安檢後就先來買",
    },
    "olive_young_t2_b1": {
        "name": "Olive Young T2 B1", "name_kr": "올리브영 인천공항 T2",
        "area": AREA_AIRPORT, "cat": "shop", "sub": "韓妝補貨",
        "address": "인천공항 T2 B1 교통센터",
        "lat": 37.4607, "lng": 126.4408,
        "hours": "06:00-22:00",
        "note": "B1 交通中心。最後補美妝/面膜的地方 (管制區外)",
    },
    "cu_airport": {
        "name": "CU 便利商店 T2 9 號登機口", "name_kr": "CU 인천공항 T2",
        "area": AREA_AIRPORT, "cat": "food", "sub": "便利商店",
        "address": "인천공항 T2 3F 9번 게이트 부근",
        "lat": 37.4604, "lng": 126.4426,
        "hours": "06:00-22:00",
        "note": "T-money 用掉的好地方。餘額 ≤ ₩20,000 可在這裡退現金 (扣 ₩500 手續費)",
    },
    "bistro_la_grillia_t2": {
        "name": "Bistro Bar La Grillia T2", "name_kr": "비스트로 바 라 그릴리아 T2",
        "area": AREA_AIRPORT, "cat": "food", "sub": "義式餐酒",
        "address": "인천공항 T2 3F 면세구역",
        "lat": 37.4603, "lng": 126.4420,
        "hours": "24h",
        "note": "24 小時義式酒吧。披薩 / 義大利麵 ₩20,000~",
    },
    "dunkin_t2": {
        "name": "DUNKIN' Donuts T2", "name_kr": "던킨도너츠 T2",
        "area": AREA_AIRPORT, "cat": "food", "sub": "甜甜圈/咖啡",
        "address": "인천공항 T2 3F 면세구역 (多家分店)",
        "lat": 37.4604, "lng": 126.4416,
        "hours": "06:00-21:30",
        "note": "美式咖啡 + 韓限定口味甜甜圈 (草莓奶油 / 抹茶)",
    },
    "foodgarden_t1": {
        "name": "Food Garden T1 美食街 (24h)", "name_kr": "푸드 가든 T1",
        "area": AREA_AIRPORT, "cat": "food", "sub": "韓食美食街",
        "address": "인천공항 T1 1F 12번 출구 부근",
        "lat": 37.4530, "lng": 126.4408,
        "hours": "24h",
        "note": "⚠️ 在 T1 不是 T2，要從 T2 搭穿梭巴士 (15 min, 免費)",
    },
    "t2_observation_deck": {
        "name": "T2 5F 觀景台/咖啡", "name_kr": "T2 5층 전망대",
        "area": AREA_AIRPORT, "cat": "sight", "sub": "觀景咖啡",
        "address": "인천공항 T2 5F 중앙",
        "lat": 37.4609, "lng": 126.4408,
        "hours": "06:00-22:00",
        "note": "5F 中央展望台，免費進，咖啡座可看飛機起降",
    },
    "walker_hill_capsule_t2": {
        "name": "Walker Hill 過境膠囊旅館 T2", "name_kr": "다락휴 캡슐호텔 T2",
        "area": AREA_AIRPORT, "cat": "sight", "sub": "膠囊旅館",
        "address": "인천공항 T2 3F 252번 게이트 부근",
        "lat": 37.4604, "lng": 126.4422,
        "hours": "24h",
        "note": "免稅區內 (Gate 252 附近)。過夜 ₩55,000、3h 短休 ~₩30,000",
    },

    # ================================================================
    # 交通樞紐 (Day 1 / Day 5)
    # ================================================================
    "icn_t2": {
        "name": "仁川 T2 (入境/出境)", "name_kr": "인천공항 제2터미널",
        "area": AREA_AIRPORT, "cat": "transit",
        "address": "인천국제공항 제2여객터미널",
        "lat": 37.4691, "lng": 126.4505,
        "hours": "24h",
        "note": "Jin Air LJ736/LJ737 都在 T2",
    },
    "rmq": {
        "name": "台中國際機場 RMQ", "name_kr": "타이중공항",
        "area": AREA_AIRPORT, "cat": "transit",
        "address": "台中市沙鹿區中航路一段168號",
        "lat": 24.2664, "lng": 120.6212,
        "hours": "24h",
        "note": "起飛前 2 小時抵達",
    },
}


# ================================================================
# 工具函式
# ================================================================
def get_by_area(area, exclude=None, cat=None, sub=None):
    """取得某區所有地點，可以排除某些 id 或限定分類。"""
    exclude = exclude or []
    if isinstance(exclude, str):
        exclude = [exclude]
    result = []
    for pid, p in PLACES.items():
        if pid in exclude:
            continue
        if p.get("area") != area:
            continue
        if cat and p.get("cat") != cat:
            continue
        if sub and p.get("sub") != sub:
            continue
        result.append((pid, p))
    return result
