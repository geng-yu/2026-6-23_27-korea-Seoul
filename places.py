"""
首爾旅遊地點資料中心。
所有店家/景點集中在這裡，每天的行程都從這裡撈資料。
這樣修改一次到處更新，新增也方便。

每個地點的欄位:
- name      : 中文名稱
- name_kr   : 韓文名稱
- area      : 區域 (用來決定備案清單)
- cat       : 主分類 food / shop / sight / cafe / hotel
- sub       : 子分類 (例如 燒烤 / 蔘雞湯 / 美妝 / 百貨...)
- address   : 韓文地址
- lat, lng  : 座標
- hours     : 營業時間文字
- phone     : 電話 (選填)
- note      : 備註
- priority  : ⭐ 是否優先 (使用者清單粉紅色標的)
"""

# 區域常數
AREA_HONGDAE = "弘대"
AREA_YEONNAM = "延南"
AREA_MANGWON = "望遠"
AREA_SEONGSU = "聖水"
AREA_DONGDAEMUN = "東大門"
AREA_GWANGJANG = "廣藏"
AREA_ANGUK = "安國"
AREA_IKSEON = "益善"
AREA_MYEONGDONG = "明洞"


PLACES = {
    # ==============================
    # 飯店
    # ==============================
    "hotel": {
        "name": "9 Brick Hotel", "name_kr": "나인브릭 호텔",
        "area": AREA_HONGDAE, "cat": "hotel",
        "address": "서울 마포구 홍익로5길 32",
        "lat": 37.5537661, "lng": 126.9205306,
        "hours": "Check-in 15:00 / Check-out 11:00",
        "phone": "+82-2-3141-8800",
        "note": "弘대입구站 9 號出口走 6 分鐘",
    },

    # ==============================
    # Day 1 主行程 — 弘대 (使用者清單)
    # ==============================
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
    "olive_young_hongdae": {
        "name": "Olive Young 弘대旗艦", "name_kr": "올리브영 홍대타운",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "美妝",
        "address": "57 홍익로6길, 마포구, 서울",
        "lat": 37.5565733, "lng": 126.9243823,
        "hours": "週一-四 10:00-22:30 / 週五六 10:00-23:00",
        "phone": "1577-4887",
        "note": "三層樓，美妝藥妝旗艦店",
    },

    # ==============================
    # Day 2 主行程 — 聖水 + 東大門 (使用者清單)
    # ==============================
    "gamjatang": {
        "name": "祖傳三代馬鈴薯排骨湯", "name_kr": "소문난성수감자탕",
        "area": AREA_SEONGSU, "cat": "food", "sub": "湯飯",
        "address": "서울 성동구 연무장길 45",
        "lat": 37.5428241, "lng": 127.0543732,
        "hours": "24h",
        "phone": "02-465-6580",
        "note": "排骨煮到骨肉分離，24h 不打烊",
        "priority": True,
    },
    "maman_gelato": {
        "name": "Maman Gelato 聖水", "name_kr": "마망젤라또 성수점",
        "area": AREA_SEONGSU, "cat": "food", "sub": "甜點",
        "address": "서울 성동구 연무장9길 8 1층",
        "lat": 37.5429349, "lng": 127.0559738,
        "hours": "11:30-21:00",
        "phone": "02-466-3373",
        "note": "Pistachiotella 開心果義式冰淇淋",
        "priority": True,
    },
    "lcdc": {
        "name": "LCDC Seoul", "name_kr": "엘씨디씨 서울",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "選物百貨",
        "address": "서울 성동구 연무장17길 10",
        "lat": 37.5415795, "lng": 127.0614594,
        "hours": "10:00-20:00",
        "note": "四層樓文青百貨，潮品+咖啡+展覽",
    },
    "ddp": {
        "name": "DDP 東大門設計廣場", "name_kr": "동대문디자인플라자",
        "area": AREA_DONGDAEMUN, "cat": "sight",
        "address": "서울 중구 을지로 281",
        "lat": 37.5665256, "lng": 127.0092236,
        "hours": "10:00-20:00",
        "note": "Zaha Hadid 建築，外觀必拍",
    },
    "jin_okhwa": {
        "name": "陳玉華一隻雞", "name_kr": "진옥화할매원조닭한마리",
        "area": AREA_DONGDAEMUN, "cat": "food", "sub": "一隻雞",
        "address": "서울 종로구 종로40가길 18",
        "lat": 37.5703627, "lng": 127.0057612,
        "hours": "10:30-01:00",
        "phone": "02-2275-9666",
        "note": "東大門一隻雞老店",
        "priority": True,
    },
    "kyochon": {
        "name": "橋村炸雞 弘대점", "name_kr": "교촌치킨 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "炸雞",
        "address": "서울 마포구 양화로16길 6",
        "lat": 37.5535944, "lng": 126.9201354,
        "hours": "12:00-01:30",
        "phone": "02-338-1300",
        "note": "醬油蒜味/紅辣味",
    },

    # ==============================
    # Day 3 主行程 — 安國/北村/明洞
    # ==============================
    "cafe_onion_anguk": {
        "name": "Cafe Onion Anguk", "name_kr": "어니언 안국점",
        "area": AREA_ANGUK, "cat": "food", "sub": "咖啡早餐",
        "address": "서울 종로구 계동길 5",
        "lat": 37.5776235, "lng": 126.9865541,
        "hours": "週一-五 07:00-22:00 / 週末 09:00-22:00",
        "phone": "070-7543-2123",
        "note": "韓屋風咖啡店",
    },
    "gwanghwamun": {
        "name": "光化門", "name_kr": "광화문",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 사직로 161",
        "lat": 37.5760111, "lng": 126.9768611,
        "hours": "24h (景福宮 09:00-17:00)",
        "phone": "02-3700-3900",
        "note": "11:00 守門將交班儀式必看",
        "priority": True,
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
    "muguok": {
        "name": "無垢屋蔘雞湯", "name_kr": "무구옥",
        "area": AREA_ANGUK, "cat": "food", "sub": "蔘雞湯",
        "address": "서울 종로구 율곡로1길 7 지상1층",
        "lat": 37.5763898, "lng": 126.9799003,
        "hours": "11:30-14:00 / 17:30-20:00",
        "note": "⚠️ 限定時段，catchtable 登記，下午 14-17 不開",
        "priority": True,
    },
    "bukchon": {
        "name": "北村韓屋村", "name_kr": "북촌 한옥마을",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 계동길 37",
        "lat": 37.5814696, "lng": 126.9849519,
        "hours": "10:00-17:00 (居民區，請輕聲)",
        "phone": "02-2133-1371",
        "note": "傳統韓屋拍照景點，超過 17 點請離開",
        "priority": True,
    },
    "london_bagel": {
        "name": "倫敦貝果博物館 安國", "name_kr": "런던베이글뮤지엄 안국",
        "area": AREA_ANGUK, "cat": "food", "sub": "甜點麵包",
        "address": "서울 종로구 북촌로4길 20",
        "lat": 37.5791826, "lng": 126.9861520,
        "hours": "07:00-18:00",
        "note": "⚠️ Catchtable 抽號碼牌，可能等 2 小時",
    },
    "ikseondong": {
        "name": "益善洞韓屋村", "name_kr": "익선동 한옥마을",
        "area": AREA_IKSEON, "cat": "sight",
        "address": "서울 종로구 익선동",
        "lat": 37.5737132, "lng": 126.9901271,
        "hours": "10:00-21:00 (店家各異)",
        "phone": "02-2148-5243",
        "note": "韓屋變咖啡街，韓劇鬼怪取景",
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

    # ==============================
    # Day 4 主行程 — 望遠/延南/弘대採買
    # ==============================
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
    "jo_dawson": {
        "name": "JO & DAWSON 法式吐司", "name_kr": "조앤도슨 연남본점",
        "area": AREA_YEONNAM, "cat": "food", "sub": "甜點",
        "address": "서울 마포구 동교로41길 31 지층",
        "lat": 37.5636203, "lng": 126.9232494,
        "hours": "10:00-20:00",
        "note": "首爾最強法式吐司，茶葉自己烘",
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

    # ==============================
    # Day 5 主行程 — 回程
    # ==============================
    "baeknyeon": {
        "name": "百年百歲土種蔘雞湯", "name_kr": "백년토종삼계탕",
        "area": AREA_HONGDAE, "cat": "food", "sub": "蔘雞湯",
        "address": "서울 마포구 양화로 118 1층",
        "lat": 37.5538158, "lng": 126.9202046,
        "hours": "09:00-22:00",
        "phone": "02-325-3399",
        "note": "2017 米其林，09:00 就開",
        "priority": True,
    },

    # ==============================
    # 備案 — 弘대美食 (使用者清單 + 增補)
    # ==============================
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
        "note": "可選辣度，吃完用剩醬做炒飯必點，小菜無限續。",
    },
    "vanga_dakgalbi": {
        "name": "Vanga 炭火雞排", "name_kr": "반가 숯불닭갈비 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "炭火雞排",
        "address": "서울 마포구 어울마당로 147-1",
        "lat": 37.5567023, "lng": 126.9262810,
        "hours": "11:00-01:00",
        "phone": "02-337-3545",
        "note": "紫蘇葉+蒜柚子醬包著吃，員工幫烤",
    },
        "myeongryun_jinsa": {
        "name": "二代祖馬鈴薯排骨湯", "name_kr": "이대조뼈다귀 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "馬鈴薯排骨湯",
        "address": "서울 마포구 동교로 196",
        "lat": 37.5570, "lng": 126.9250,
        "hours": "10:00-23:00",
        "phone": None,
        "note": "人氣排骨湯，適合早午餐或晚餐",
    },
    "solsot_hongdae": {
        "name": "Solsot 釜飯 弘大延南", "name_kr": "솔솥 홍대연남점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "釜飯",
        "address": "서울 마포구 동교로38길 35",
        "lat": 37.5620, "lng": 126.9250,
        "hours": "11:30-21:00",
        "phone": "070-8822-5846",
        "note": "延南洞人氣釜飯，適合午餐或早點晚餐",
    },
    "yetnaljip": {
        "name": "老房子木炭燒肉", "name_kr": "옛날집 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "木炭燒肉",
        "address": "서울 마포구 동교동 169-6",
        "lat": 37.5549, "lng": 126.9228,
        "hours": "16:00-05:00",
        "phone": "02-3141-9608",
        "note": "老字號木炭烤肉，平價飽足，可網路訂位，越晚越熱鬧",
        "priority": True,
    },
    "hongdae_chungmu": {
        "name": "弘大忠武飯捲", "name_kr": "홍대충무김밥 홍대본점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "飯捲",
        "address": "서울 마포구 어울마당로 79 1층",
        "lat": 37.5545, "lng": 126.9235,
        "hours": "24h",
        "phone": None,
        "note": "弘大24小時人氣飯捲，弘大入口站9號出口附近",
    },
    "sulbing_hongdae": {
        "name": "雪冰 弘大店", "name_kr": "설빙 홍대입구역점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "韓式刨冰",
        "address": "서울 마포구 홍익로6길 15 2F",
        "lat": 37.5543, "lng": 126.9241,
        "hours": "11:00-22:30",
        "phone": "02-323-3287",
        "note": "飯後甜點首選，招牌黃豆粉年糕雪花冰必點",
    },

    # ==============================
    # 備案 — 弘대 PTT/Dcard 加碼
    # ==============================
    "isaac_toast": {
        "name": "Isaac Toast 弘대", "name_kr": "이삭토스트 홍대점",
        "area": AREA_HONGDAE, "cat": "food", "sub": "早餐",
        "address": "弘대입구역周邊",
        "lat": 37.5555, "lng": 126.9225,
        "hours": "07:00-22:00",
        "note": "韓式吐司早餐連鎖",
    },

    # ==============================
    # 備案 — 弘대購物 (使用者清單 + 增補)
    # ==============================
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
        "note": "",
    },
    "hongdae_street": {
        "name": "弘대商店街", "name_kr": "홍대 쇼핑거리",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "商圈",
        "address": "弘대 弘益路",
        "lat": 37.5550, "lng": 126.9225,
        "hours": "10:00-24:00 (店家各異)",
        "note": "",
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
        "note": "Oversized 剪裁＋標語設計，帽子、包包",
    },
    "wacky_willy": {
        "name": "Wacky WiLLy 弘大", "name_kr": "와키윌리 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國本土潮牌",
        "address": "서울 마포구 잔다리로 26",
        "lat": 37.5512, "lng": 126.9245,
        "hours": "11:00-22:00",
        "phone": "070-8848-3316",
        "note": "前身 what it isn't，塗鴉插畫印花",
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
        "note": "Lee",
    },
    "worksout": {
        "name": "WORKSOUT 弘大", "name_kr": "웍스아웃 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "聯合進口潮牌",
        "address": "서울 마포구 양화로 130",
        "lat": 37.5557, "lng": 126.9222,
        "hours": "12:00-21:00",
        "phone": "02-337-8334",
        "note": "品牌集合，服裝鞋子配件生活用品都有",
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
        "phone": None,
        "note": "塗鴉插畫風滑板系潮牌",
    },
    "nerdy": {
        "name": "NERDY 弘大旗艦店", "name_kr": "너디 홍대 플래그십",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國本土潮牌",
        "address": "서울 마포구 어울마당로 94-12",
        "lat": 37.5525, "lng": 126.9234,
        "hours": "11:00-22:00",
        "phone": None,
        "note": "韓系插畫風 LOGO 潮牌，帽子短T",
    },
    "wonder_place": {
        "name": "Wonder Place 弘大", "name_kr": "원더플레이스 홍대",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "潮牌集合店",
        "address": "서울 마포구 양화로 176 스타피카소 1층",
        "lat": 37.5562, "lng": 126.9237,
        "hours": "11:00-22:00",
        "phone": None,
        "note": "韓國本土潮牌多品牌集合，帽子包包",
    },
     "hongik_pharmacy": {
        "name": "弘益藥局", "name_kr": "홍익약국",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "藥妝",
        "address": "서울 마포구 양화로18길 7 1층",
        "lat": 37.5563, "lng": 126.9229,
        "hours": "09:00-23:30",
        "phone": "02-337-5414",
        "note": "弘大最知名藥妝藥局，有中文服務、即時退稅，醫療級保養品齊全",
        "priority": True,
    },
    "nerdy_hongdae": {
        "name": "NERDY 弘大旗艦", "name_kr": "널디 플래그쉽 홍대점",
        "area": AREA_HONGDAE, "cat": "shop", "sub": "韓國運動潮牌",
        "address": "서울 마포구 홍익로6길 27",
        "lat": 37.5543, "lng": 126.9241,
        "hours": "12:00-21:00",
        "phone": "02-332-9466",
        "note": "韓國人氣潮牌，紫色室內設計打卡感強，IU、APINK成員都在穿",
        "priority": True,
    },

    # ==============================
    # 備案 — 聖水 (PTT/Dcard 加碼)
    # ==============================
    "cafe_onion_seongsu": {
        "name": "Cafe Onion 聖水", "name_kr": "어니언 성수",
        "area": AREA_SEONGSU, "cat": "food", "sub": "咖啡",
        "address": "서울 성동구 아차산로9길 8",
        "lat": 37.5447328, "lng": 127.0582091,
        "hours": "週一-五 08:00-22:00 / 週末 09:00-22:00",
        "note": "工業風咖啡店元老，週末排 30 min",
    },
    "point_of_view": {
        "name": "Point of View 聖水", "name_kr": "포인트오브뷰 성수",
        "area": AREA_SEONGSU, "cat": "shop", "sub": "文具",
        "address": "서울 성동구 연무장길 18",
        "lat": 37.5434188, "lng": 127.051374,
        "hours": "12:00-20:00",
        "note": "高質感文具/生活雜貨選物店",
    },

    # ==============================
    # 備案 — 廣藏市場
    # ==============================
    "gwangjang": {
        "name": "廣藏市場", "name_kr": "광장시장",
        "area": AREA_DONGDAEMUN, "cat": "sight",
        "address": "서울 종로구 청계천로 88",
        "lat": 37.5700398, "lng": 126.9996036,
        "hours": "09:00-22:30",
        "phone": "02-2267-0291",
        "note": "麻藥飯捲、綠豆煎餅、生牛肉",
    },

    # ==============================
    # 備案 — 益善洞 (PTT/Dcard)
    # ==============================
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
        "note": "手撕吐司，可愛包裝",
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

    # ==============================
    # 備案 — 明洞
    # ==============================
    "myeongdong_kyoja": {
        "name": "明洞餃子 (米其林)", "name_kr": "명동교자",
        "area": AREA_MYEONGDONG, "cat": "food", "sub": "刀削麵",
        "address": "서울 중구 명동10길 29",
        "lat": 37.5625266, "lng": 126.985609,
        "hours": "10:30-21:30",
        "phone": "02-776-5348",
        "note": "米其林必比登",
    },
    "myungdong_chicken": {
        "name": "明洞一隻雞", "name_kr": "명동닭한마리 본점",
        "area": AREA_DONGDAEMUN, "cat": "food", "sub": "一隻雞",
        "address": "서울 종로구 종로40가길 14",
        "lat": 37.5703, "lng": 127.0057,
        "hours": "10:00-00:30",
        "phone": "02-2266-8249",
        "note": "",
    },

    # ==============================
    # 備案 — 安國/北村
    # ==============================
    "insadong": {
        "name": "仁寺洞", "name_kr": "인사동",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 인사동",
        "lat": 37.5720, "lng": 126.9858,
        "hours": "10:00-22:00 (店家各異)",
        "note": "傳統工藝品/紀念品街，益善洞走 5 min",
    },
    "samcheongdong": {
        "name": "三清洞", "name_kr": "삼청동",
        "area": AREA_ANGUK, "cat": "sight",
        "address": "서울 종로구 삼청동",
        "lat": 37.5827, "lng": 126.9817,
        "hours": "全天 (店家不一)",
        "note": "藍瓶咖啡三清店在此，文青小路",
    },

    # ==============================
    # 備案 — 延南洞咖啡
    # ==============================
    "camellia_yeonnam": {
        "name": "Camellia 延南", "name_kr": "카멜리아 연남",
        "area": AREA_YEONNAM, "cat": "food", "sub": "早午餐",
        "address": "서울 마포구 동교로45길 8 1층",
        "lat": 37.5645, "lng": 126.9225,
        "hours": "10:00-20:00",
        "note": "歐洲風早午餐，餐盤超美",
    },
    "gyeongui_park": {
        "name": "京義線林蔭道", "name_kr": "경의선숲길",
        "area": AREA_YEONNAM, "cat": "sight",
        "address": "서울 마포구 연남동",
        "lat": 37.5610, "lng": 126.9230,
        "hours": "24h",
        "note": "廢棄鐵道改的線狀公園，連接弘대-延南",
    },

    # ==============================
    # 飛行 / 交通 (Day 1 / Day 5 用)
    # ==============================
    "icn_t2": {
        "name": "仁川 T2 (入境/出境)", "name_kr": "인천공항 제2터미널",
        "area": "機場", "cat": "transit",
        "address": "인천국제공항 제2여객터미널",
        "lat": 37.4691, "lng": 126.4505,
        "hours": "24h",
        "note": "Jin Air LJ736/LJ737 都在 T2",
    },
    "rmq": {
        "name": "台中國際機場 RMQ", "name_kr": "타이중공항",
        "area": "機場", "cat": "transit",
        "address": "台中市沙鹿區中航路一段168號",
        "lat": 24.2664, "lng": 120.6212,
        "hours": "24h",
        "note": "起飛前 2 小時抵達",
    },
}


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
