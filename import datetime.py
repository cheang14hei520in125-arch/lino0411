import datetime
import json
import random
from pathlib import Path
import streamlit as st

DATA_FILE = Path(__file__).with_name("menu_data.json")

DEFAULT_MENU_DATA: dict[str, list[str]] = {
    "macau_foods": [
        "免治飯", "非洲雞", "馬介休球", "葡國雞", "薯絲炒馬介休", "咖喱牛腩配豬扒包",
        "豬扒包", "水蟹粥", "咖喱魚蛋", "牛雜", "竹昇麵", "雲吞麵", "蝦子撈麵",
        "沙丹豬扒飯", "車仔麵", "蛋球仔", "雞蛋仔", "薑汁撞奶", "雙皮奶", "木糠布甸",
        "葡撻", "花生醬西多士", "豬潤麵", "牛腩麵", "咸魚肉餅飯", "葡式燒乳豬",
        "葡式海鮮飯", "白酒煮蜆", "咖喱蟹", "胡椒蟹", "鮑魚雞粒炒飯", "臘味煲仔飯",
        "艇仔粥", "及第粥", "生滾魚片粥", "煎釀三寶", "碗仔翅", "魚翅撈飯",
        "豬腳薑", "紅豆餅", "老婆餅", "杏仁餅", "鳳凰卷", "炭燒咖喱雞", "澳門燒腩仔",
        "葡式烤鴨飯", "澳門咖喱薯仔牛腩", "水蟹蒸蛋", "馬介休炒蛋", "葡式蒜香蝦"
    ],
    "chinese_dishes": [
        "豉汁蒸排骨", "白切雞", "薑蔥白切雞", "蜜汁叉燒", "脆皮燒肉", "燒鵝",
        "豉油皇雞", "咕嚕肉", "菠蘿咕嚕肉", "XO醬炒蘿蔔糕", "清蒸海上鮮", "清蒸石斑",
        "清蒸鯪魚", "豉汁蒸倉魚", "梅菜扣肉", "芋頭扣肉", "椒鹽蝦", "白灼蝦",
        "蒜蓉粉絲蒸蝦", "避風塘炒蟹", "薑蔥炒蟹", "蒜蓉炒菜心", "腐乳炒通菜",
        "蒜蓉炒通菜", "上湯浸時蔬", "鹹蛋蒸肉餅", "冬菇蒸滑雞", "陳皮蒸牛肉",
        "黑椒牛仔骨", "京蔥爆牛肉", "西蘭花炒牛肉", "彩椒炒牛柳", "滑蛋炒蝦仁",
        "韭黃炒蛋", "番茄炒蛋", "洋蔥炒蛋", "大蔥炒蛋", "苦瓜炒蛋", "蝦仁炒蛋",
        "瑤柱蛋白炒飯", "揚州炒飯", "鹹魚雞粒炒飯", "乾炒牛河", "濕炒牛河",
        "星洲炒米", "臘味炒芥蘭", "蠔油生菜", "蝦醬通菜", "椒鹽鮮魷", "椒鹽豆腐",
        "豉汁蒸白鱔", "豆豉鯪魚炒油麥菜", "欖菜肉碎四季豆", "魚香茄子煲", "肉碎茄子煲",
        "啫啫通菜煲", "啫啫雞煲", "啫啫黃鱔煲", "啫啫生腸煲", "啫啫排骨煲", "沙爹肥牛粉絲煲",
        "金菇肥牛煲", "酸菜魚", "水煮魚", "水煮牛肉", "麻婆豆腐", "家常豆腐",
        "鐵板豆腐", "紅燒豆腐", "肉末燒豆腐", "宮保雞丁", "回鍋肉", "蒜泥白肉",
        "口水雞", "棒棒雞", "辣子雞", "歌樂山辣子雞", "夫妻肺片", "毛血旺",
        "東坡肉", "紅燒肉", "紅燒獅子頭", "紅燒排骨", "糖醋排骨", "糖醋里脊",
        "可樂雞翼", "瑞士雞翼", "豉油雞翼", "蜜汁雞翼", "蒜香雞翼", "椒鹽雞翼",
        "京醬肉絲", "青椒肉絲", "魚香肉絲", "韭菜炒肉絲", "雪菜肉絲", "榨菜肉絲",
        "芹菜炒肉絲", "蒜苔炒肉絲", "木須肉", "鍋包肉", "溜肉段", "地三鮮",
        "干煸四季豆", "干鍋花菜", "干鍋包菜", "干鍋土豆片", "干鍋肥腸", "干鍋排骨",
        "手撕包菜", "酸辣土豆絲", "青椒土豆絲", "醋溜白菜", "奶油白菜", "大白菜粉絲煲",
        "涼拌青瓜", "拍黃瓜", "涼拌木耳", "涼拌海帶絲", "涼拌皮蛋豆腐", "皮蛋瘦肉",
        "蔥爆羊肉", "孜然羊肉", "手抓羊肉", "紅燒牛腩", "蘿蔔炆牛腩", "柱侯牛腩",
        "番茄牛腩", "咖喱牛腩", "黑椒牛柳粒", "孜然牛肉", "小炒牛肉", "小炒黃牛肉",
        "酸菜炒大腸", "九轉大腸", "滷水拼盤", "滷水鴨掌", "滷水雞腳", "滷水豬手",
        "南乳炆豬手", "枝竹羊腩煲", "當歸羊肉煲", "紅燒乳鴿", "脆皮乳鴿", "鹽焗雞",
        "蔥油餅", "韭菜盒子", "鍋貼", "煎餃", "蒸餃", "小籠包",
        "生煎包", "灌湯包", "叉燒包", "奶黃包", "流沙包", "紅豆沙包",
        "芝麻球", "煎堆", "炸春卷", "芋茸酥", "蛋黃千層糕", "馬拉糕",
        "蘿蔔糕", "芋頭糕", "馬蹄糕", "紅豆糕", "桂花糕", "涼粉",
        "蒜蓉蒸勝瓜", "勝瓜炒蛋", "勝瓜煮粉絲", "冬瓜炆排骨", "冬瓜炆鴨", "節瓜炆排骨",
        "節瓜粉絲煲", "苦瓜炆排骨", "涼瓜炒牛肉", "苦瓜煎蛋", "佛手瓜炒肉片", "西葫蘆炒蛋",
        "蘆筍炒蝦仁", "蘆筍炒帶子", "西蘭花炒帶子", "蒜蓉蒸帶子", "豉汁蒸鮑魚", "紅燒鮑魚",
        "XO醬炒蝦仁帶子", "椒鹽九肚魚", "香煎馬友", "香煎黃花魚", "紅燒黃魚", "糖醋黃魚",
        "松鼠桂魚", "西湖醋魚", "龍井蝦仁", "東坡蝦仁", "叫化雞", "三杯雞",
        "麻油雞", "薑母鴨", "啤酒鴨", "北京烤鴨", "鹽水鴨", "板栗燒雞",
        "茶樹菇炒肉片", "香菇滑雞", "冬菇扒菜膽", "北菇蒸滑雞", "金針菇炒肉絲", "杏鮑菇炒牛肉",
        "黑椒杏鮑菇", "三色椒炒雞丁", "腰果炒雞丁", "核桃炒蝦仁", "西芹炒百合", "荷蘭豆炒臘肉",
        "臘味炒蒜苗", "蒜苗回鍋肉", "煙筍炒臘肉", "酸豆角炒肉末", "蒼蠅頭", "三杯中卷",
        "蔥爆魷魚", "醬爆魷魚", "鐵板魷魚", "豉汁蒸排骨配南瓜", "南瓜蒸排骨", "金瓜炒蛋",
        "鹹蛋黃炒南瓜", "椒鹽粟米", "松仁粟米", "肉末蒸蛋", "蝦仁蒸蛋", "蛤蜊蒸蛋",
        "香蔥煎蛋", "菜脯煎蛋", "蠔仔煎蛋", "芙蓉蛋", "滑蛋蝦仁飯", "豉汁排骨飯",
        "鳳爪排骨飯", "北菇滑雞飯", "窩蛋牛肉飯", "叉燒飯", "燒鴨飯", "燒肉飯",
        "油雞飯", "白切雞飯", "海南雞飯", "口水雞飯", "咖喱雞飯", "椒鹽豬扒飯",
        "黑椒豬扒飯", "洋蔥豬扒飯", "吉列豬扒飯", "瑞士汁豬扒飯", "梅菜扣肉飯", "紅燒肉飯",
        "滷肉飯", "麻婆豆腐飯", "魚香茄子飯", "宮保雞丁飯", "回鍋肉飯", "番茄炒蛋飯",
        "揚州炒飯配蝦仁", "生炒糯米飯", "臘味糯米飯", "珍珠雞", "荷葉飯", "福建炒飯",
        "鴛鴦炒飯", "豉椒炒牛肉", "豉椒炒排骨", "豉椒炒鵝腸", "豉椒炒蜆", "豉椒炒聖子",
        "蒜蓉蒸聖子", "豉汁蒸聖子", "蒜蓉粉絲蒸扇貝", "椒鹽瀨尿蝦", "白灼瀨尿蝦", "豉油皇大蝦",
        "茄汁大蝦", "油燜大蝦", "乾燒大蝦", "鳳尾蝦", "百花釀油條", "百花釀冬菇",
        "釀苦瓜", "釀節瓜", "釀豆腐", "釀茄子", "釀青椒", "客家釀豆腐",
        "梅菜蒸鯇魚", "陳皮蒸鯇魚", "豆豉蒸排骨", "蒜香骨", "京都排骨", "無錫排骨",
        "醬爆雞丁", "宮廷炒雞丁", "雪菜毛豆炒肉絲", "毛豆炒蝦仁", "雪菜炒冬筍", "油燜春筍",
        "問政山筍炒肉", "小炒肉", "湖南小炒肉", "剁椒皮蛋", "擂辣椒皮蛋", "虎皮青椒",
        "尖椒炒蛋", "青椒炒肉片", "洋蔥炒豬肝", "薑蔥炒豬肝", "韭菜炒豬肝", "酸辣豬肝",
        "爆炒腰花", "溜肝尖", "孜然肥牛", "金針菇肥牛卷", "番茄肥牛卷", "酸湯肥牛",
        "麻辣香鍋", "香辣蟹", "十三香小龍蝦", "蒜蓉小龍蝦", "麻辣小龍蝦", "口蘑炒肉片",
        "白玉菇炒肉絲", "蟹味菇炒蛋", "姬松茸炒雞肉", "竹笙釀肉", "紅燒蹄膀", "冰糖肘子",
        "醬豬蹄", "黃豆炆豬手", "花生炆豬手", "花生炆豬尾", "酸甜豬腳", "椒鹽豬手",
        "涼拌雞絲", "香辣雞絲", "椒麻雞", "大盤雞", "新疆炒米粉", "過橋米線",
        "桂林米粉", "螺螄粉", "熱乾麵", "炸醬麵", "擔擔麵", "重慶小麵",
        "蘭州牛肉麵", "陽春麵", "刀削麵", "岐山臊子麵", "油潑麵", "Biangbiang麵",
        "廣式炒麵", "豉油皇炒麵", "肉絲炒麵", "三絲炒麵", "海鮮炒麵", "福建炒麵",
        "上海粗炒", "乾燒伊麵", "薑蔥蠔仔煲", "蠔仔粥", "皮蛋瘦肉粥", "白粥配腐乳"
    ],
    "chinese_soups": [
        "粉葛鯪魚赤小豆湯", "蘋果瘦肉無花果湯", "冬瓜薏米排骨湯", "西洋菜陳腎生魚湯",
        "木瓜花生眉豆排骨湯", "老黃瓜赤小豆扁豆湯", "粟米紅蘿蔔瘦肉湯", "霸王花南北杏瘦肉湯",
        "蟲草花杞子響螺頭湯", "淮山杞子圓肉烏雞湯", "番茄蛋花湯", "紫菜肉碎湯",
        "酸辣湯", "粟米羹", "冬瓜肉丸湯", "芫荽皮蛋魚片湯", "合掌瓜粟米紅蘿蔔瘦肉湯",
        "青紅蘿蔔粟米瘦肉湯", "節瓜章魚紅蘿蔔排骨湯", "蓮藕花生眉豆章魚排骨湯",
        "蓮藕綠豆排骨湯", "椰子雞湯", "竹笙椰子雞湯", "黨參北芪紅棗烏雞湯",
        "當歸黨參北芪羊肉湯", "沙參玉竹麥冬瘦肉湯", "石斛麥冬瘦肉湯", "川貝枇杷葉燉雪梨",
        "海底椰南北杏燉雪梨", "雪耳木瓜燉冰糖", "雪耳紅棗蓮子糖水", "南北杏豬肺湯",
        "羅漢果南北杏瘦肉湯", "無花果雪梨瘦肉湯", "青欖羅漢果瘦肉湯", "金銀菜豬肝湯",
        "西洋菜豬肝湯", "芥菜鹹蛋瘦肉湯", "大芥菜豬肚湯", "胡椒豬肚湯",
        "酸菜胡椒豬肚湯", "白果胡椒豬肚湯", "淮山芡實扁豆瘦肉湯", "五指毛桃土茯苓瘦肉湯",
        "土茯苓龜苓膏湯", "生熟地土茯苓瘦肉湯", "桑寄生蛋茶", "合桃黑芝麻糊",
        "紅豆沙陳皮湯", "綠豆海帶湯", "番薯糖水", "腐竹雞蛋糖水", "芋頭西米露",
        "楊枝甘露", "木瓜雪耳燉奶", "燉花膠響螺湯", "花膠淮山杞子雞湯",
        "海參瑤柱冬瓜湯", "鮑魚冬菇雞湯", "響螺片花旗參瘦肉湯", "花旗參麥冬瘦肉湯",
        "田七丹參瘦肉湯", "黑豆合桃瘦肉湯", "黑豆眉豆花生排骨湯", "赤小豆粉葛鯪魚湯",
        "冬瓜荷葉扁豆湯", "荷葉冬瓜薏米湯", "苦瓜黃豆排骨湯", "苦瓜鹹蛋瘦肉湯",
        "勝瓜鹹蛋瘦肉湯", "勝瓜章魚瘦肉湯", "絲瓜蛋花湯", "絲瓜豆腐魚湯",
        "豆腐海帶湯", "豆腐紫菜蛋花湯", "番茄豆腐肉碎湯", "番茄牛腩湯",
        "羅宋湯", "菠菜豬紅湯", "韭菜豬紅湯", "酸菜魚湯", "鯽魚豆腐湯",
        "奶白魚頭豆腐湯", "胡椒鹹菜魚湯", "冬陰功酸辣蝦湯", "肉骨茶",
        "當歸雞湯", "人參雞湯", "天麻魚頭湯", "川芎白芷魚頭湯", "枸杞葉豬肝湯",
        "枸杞葉瘦肉蛋花湯", "咸酸菜豬肚湯", "榨菜肉絲蛋花湯", "雪菜肉絲湯",
        "竹筍鮮肉湯", "冬筍醃篤鮮", "醃篤鮮", "排骨海帶湯", "排骨蓮藕湯",
        "排骨蘿蔔湯", "白蘿蔔羊肉湯", "羊肉蘿蔔湯", "菌菇烏雞湯", "松茸雞湯",
        "羊肚菌排骨湯", "茶樹菇排骨湯", "姬松茸瘦肉湯", "猴頭菇瘦肉湯", "靈芝瘦肉湯",
        "桑葚紅棗瘦肉湯", "紅棗桂圓杞子茶湯", "陳皮紅豆綠豆湯", "馬蹄紅蘿蔔竹蔗茅根水",
        "竹蔗茅根馬蹄水", "夏枯草煲瘦肉湯", "雞骨草煲豬橫脷湯", "溪黃草煲瘦肉湯"
    ],
}


def load_menu_data() -> dict[str, list[str]]:
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        merged: dict[str, list[str]] = {}
        for key in ("macau_foods", "chinese_dishes", "chinese_soups"):
            combined = DEFAULT_MENU_DATA[key] + raw.get(key, [])
            merged[key] = list(dict.fromkeys(x.strip() for x in combined if x and x.strip()))
        return merged

    save_menu_data(DEFAULT_MENU_DATA)
    return {k: list(v) for k, v in DEFAULT_MENU_DATA.items()}


def save_menu_data(data: dict[str, list[str]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def pick_menu(
    data: dict[str, list[str]],
    count: int,
    mode: str,
    seed_salt: int,
    exclude_keywords: list[str],
    target_date: datetime.date,
) -> list[tuple[str, str]]:
    def valid(name: str) -> bool:
        return not any(kw in name for kw in exclude_keywords)

    macau = [("🇲🇴 澳門嘢食", x) for x in data["macau_foods"] if valid(x)]
    dishes = [("🥘 中國餸菜", x) for x in data["chinese_dishes"] if valid(x)]
    soups = [("🍲 煲湯", x) for x in data["chinese_soups"] if valid(x)]

    rng = random.Random(f"{target_date.isoformat()}-{mode}-{count}-{seed_salt}")

    if mode == "macau":
        return rng.sample(macau, min(count, len(macau)))
    if mode == "dish":
        return rng.sample(dishes, min(count, len(dishes)))
    if mode == "soup":
        return rng.sample(soups, min(count, len(soups)))

    if mode == "balanced":
        selected: list[tuple[str, str]] = []
        for pool in (macau, dishes, soups):
            if pool:
                selected.append(rng.choice(pool))

        selected_set = set(selected)
        remaining = [x for x in (macau + dishes + soups) if x not in selected_set]
        extra = max(0, count - len(selected))
        if extra > 0 and remaining:
            selected.extend(rng.sample(remaining, min(extra, len(remaining))))
        rng.shuffle(selected)
        return selected

    all_items = macau + dishes + soups
    return rng.sample(all_items, min(count, len(all_items)))


st.set_page_config(page_title="每日食乜好｜澳門＋中國菜＋煲湯", page_icon="🍜", layout="centered")

data = load_menu_data()
today = datetime.date.today()

if "reroll_count" not in st.session_state:
    st.session_state.reroll_count = 0

st.title("🍜 今日食乜好？")
st.caption(
    f"📅 {today.strftime('%Y-%m-%d')} ｜ 澳門嘢食 **{len(data['macau_foods'])}** 款、"
    f"中國餸菜 **{len(data['chinese_dishes'])}** 款、煲湯 **{len(data['chinese_soups'])}** 款"
)

with st.sidebar:
    st.header("⚙️ 抽籤設定")
    mode = st.selectbox(
        "抽籤模式",
        options=["balanced", "mixed", "macau", "dish", "soup"],
        format_func=lambda m: {
            "balanced": "均衡配搭（每類至少 1 款）",
            "mixed": "全體混合隨機",
            "macau": "只抽澳門嘢食",
            "dish": "只抽中國餸菜",
            "soup": "只抽煲湯",
        }[m],
    )

    count = st.slider("每日抽幾款", min_value=1, max_value=10, value=4)

    exclude_raw = st.text_input("排除關鍵字（逗號分隔）", placeholder="例如：牛, 辣, 羊")
    exclude_keywords = [k.strip() for k in exclude_raw.split(",") if k.strip()]

    st.divider()
    st.subheader("➕ 新增菜式／湯水")
    new_cat = st.selectbox(
        "分類",
        options=["macau_foods", "chinese_dishes", "chinese_soups"],
        format_func=lambda c: {
            "macau_foods": "澳門嘢食",
            "chinese_dishes": "中國餸菜",
            "chinese_soups": "煲湯",
        }[c],
    )
    new_item = st.text_input("名稱", placeholder="例如：黑椒牛柳絲")
    if st.button("加入並儲存", use_container_width=True):
        clean_name = new_item.strip()
        if not clean_name:
            st.warning("請輸入名稱。")
        elif clean_name in data[new_cat]:
            st.info("呢款已經喺清單入面。")
        else:
            data[new_cat].append(clean_name)
            save_menu_data(data)
            st.success(f"已加入：{clean_name}")
            st.rerun()

col1, col2 = st.columns(2)
with col1:
    if st.button("🎲 重新抽籤", type="primary", use_container_width=True):
        st.session_state.reroll_count += 1
with col2:
    if st.button("🔄 恢復今日預設", use_container_width=True):
        st.session_state.reroll_count = 0

picks = pick_menu(
    data=data,
    count=count,
    mode=mode,
    seed_salt=st.session_state.reroll_count,
    exclude_keywords=exclude_keywords,
    target_date=today,
)

st.divider()

if not picks:
    st.warning("搵唔到符合條件嘅選項，試下減少排除關鍵字。")
else:
    for idx, (category, name) in enumerate(picks, start=1):
        with st.container(border=True):
            st.markdown(f"**{idx}. {name}**")
            st.caption(category)

with st.expander("📋 瀏覽完整清單"):
    tab1, tab2, tab3 = st.tabs([
        f"澳門嘢食 ({len(data['macau_foods'])})",
        f"中國餸菜 ({len(data['chinese_dishes'])})",
        f"煲湯 ({len(data['chinese_soups'])})",
    ])
    with tab1:
        st.write("、".join(data["macau_foods"]))
    with tab2:
        st.write("、".join(data["chinese_dishes"]))
    with tab3:
        st.write("、".join(data["chinese_soups"]))