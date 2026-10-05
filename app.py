# -*- coding: utf-8 -*-
"""
人生决策室 - 梅花易数 AI 解卦
基于 Streamlit 构建，调用 DeepSeek API 进行专业卦理解读
"""

import streamlit as st
import streamlit as st

# ========== 这里粘贴下面这一大段CSS样式代码 ==========
st.markdown("""
<style>

/* 页面所有小标题、标签文字：起卦信息、起卦日期、起卦时辰、提示文字 */
.stMarkdown p {
    color: #f3f4f6 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* Streamlit原生组件标签（重点！起卦日期、起卦时辰这种侧边标签就是label） */
label {
    color: #f3f4f6 !important;
    font-size:16px !important;
    font-weight:600 !important;
}

/* 顶部大标题【人生决策室】保留金色不变 */
h1, h2 {
    color: #f0c868 !important;
}

/* 输入框里面用户打字的文字（白底框深色字） */
.stTextArea textarea, .stTextInput input {
    color: #1f2937 !important;
}

/* 输入框里面的提示占位文字 */
.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #4b5563 !important;
}

</style>
""", unsafe_allow_html=True)
# ========== CSS代码结束，下面是你原来所有的起卦、页面代码，不动！ ==========

# ----------------------你原来剩下所有代码都在这里，保持原样，不要改动----------------------


import requests
from datetime import datetime
import random

# ============================================================
# 页面基础配置
# ============================================================
st.set_page_config(
    page_title="人生决策室",
    page_icon="☯️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 东方道家国风样式（B级：适中偏强符令感，暗青底）
# ============================================================
st.markdown("""
<style>
/* 全局背景：暗青黛色，不压抑 */
.stApp {
    background: linear-gradient(135deg, #1a2733 0%, #0f1c26 50%, #16242f 100%);
    color: #e8e4d9;
}

/* 隐藏 Streamlit 默认元素 */
#MainMenu, footer, header {visibility: hidden;}

/* 主容器 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

/* 标题样式 */
h1 {
    font-family: "STKaiti", "KaiTi", "SimSun", serif;
    text-align: center;
    color: #d4af37 !important;
    text-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    letter-spacing: 0.5em;
    margin-bottom: 0.5rem !important;
}

/* 副标题/分隔符 */
.divider {
    text-align: center;
    color: #8b7355;
    margin: 1rem 0;
    font-size: 0.9rem;
    letter-spacing: 0.3em;
}

/* 输入区卡片 */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: #e8e4d9 !important;
    border: 1px solid rgba(212, 175, 55, 0.3) !important;
    border-radius: 4px;
}

/* 按钮 */
.stButton > button {
    background: linear-gradient(135deg, #8b2500 0%, #6b1d00 100%);
    color: #f0e6d3;
    border: 1px solid #d4af37;
    border-radius: 4px;
    padding: 0.6rem 3rem;
    font-family: "STKaiti", "KaiTi", serif;
    font-size: 1.1rem;
    letter-spacing: 0.3em;
    width: 100%;
    transition: all 0.3s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #a82e00 0%, #8b2500 100%);
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    transform: translateY(-1px);
}

/* 卦象展示卡片 */
.gua-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(212, 175, 55, 0.2);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    text-align: center;
}

/* 卦画样式 */
.gua-symbol {
    font-size: 3rem;
    color: #d4af37;
    margin: 0.5rem 0;
    letter-spacing: 0.2em;
}

/* 标签 */
.section-label {
    color: #8b9dc3;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

/* 结果区 */
.ai-result {
    background: rgba(212, 175, 55, 0.05);
    border-left: 3px solid #d4af37;
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 0 8px 8px 0;
    line-height: 1.8;
}

/* 免责声明 */
.disclaimer {
    text-align: center;
    color: #6b7b8c;
    font-size: 0.8rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* 太极装饰 */
.taiji {
    text-align: center;
    font-size: 2rem;
    margin: 1rem 0;
    opacity: 0.6;
}
</style>

<!-- 背景符纹暗纹 -->
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; opacity: 0.03; font-size: 10rem; text-align: center; padding-top: 20vh;">
    ☰ ☱ ☲ ☳ ☴ ☵ ☶ ☷
</div>
""", unsafe_allow_html=True)

# ============================================================
# 梅花易数排盘引擎
# ============================================================

# 八卦基础数据：(卦名, 卦画二进制, 五行, 自然象)
BAGUA = {
    1: {"name": "乾", "symbol": "☰", "wuxing": "金", "nature": "天"},
    2: {"name": "兑", "symbol": "☱", "wuxing": "金", "nature": "泽"},
    3: {"name": "离", "symbol": "☲", "wuxing": "火", "nature": "火"},
    4: {"name": "震", "symbol": "☳", "wuxing": "木", "nature": "雷"},
    5: {"name": "巽", "symbol": "☴", "wuxing": "木", "nature": "风"},
    6: {"name": "坎", "symbol": "☵", "wuxing": "水", "nature": "水"},
    7: {"name": "艮", "symbol": "☶", "wuxing": "土", "nature": "山"},
    8: {"name": "坤", "symbol": "☷", "wuxing": "土", "nature": "地"},
}

# 五行生克关系
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

def get_bagua(num):
    """数字转八卦，0 当 8 用"""
    n = num % 8
    if n == 0:
        n = 8
    return BAGUA[n]

def meihua_qigua(year, month, day, hour):
    """
    梅花易数时间起卦法
    上卦 = (年+月+日) % 8
    下卦 = (年+月+日+时) % 8
    动爻 = (年+月+日+时) % 6
    """
    upper_num = (year + month + day) % 8
    lower_num = (year + month + day + hour) % 8
    dong_yao = (year + month + day + hour) % 6
    
    if upper_num == 0:
        upper_num = 8
    if lower_num == 0:
        lower_num = 8
    if dong_yao == 0:
        dong_yao = 6
    
    upper = get_bagua(upper_num)
    lower = get_bagua(lower_num)
    
    # 本卦名
    ben_gua = f"{upper['name']}{lower['name']}"
    
    # 体用判断：动爻在上卦则下卦为体，动爻在下卦则上卦为体
    if dong_yao <= 3:
        ti = lower  # 下卦为体
        yong = upper  # 上卦为用
        ti_position = "下卦"
        yong_position = "上卦"
    else:
        ti = upper
        yong = lower
        ti_position = "上卦"
        yong_position = "下卦"
    
    # 互卦（本卦二三四爻为下互，三四五爻为上互）
    # 简化处理：用上下卦组合的互卦逻辑
    hu_upper_num = (upper_num + lower_num) % 8 or 8
    hu_lower_num = (upper_num * 2 + lower_num) % 8 or 8
    hu_upper = get_bagua(hu_upper_num)
    hu_lower = get_bagua(hu_lower_num)
    hu_gua = f"{hu_upper['name']}{hu_lower['name']}"
    
    # 变卦：动爻阴阳互变
    # 简化：根据动爻数改变对应卦
    bian_upper_num = (upper_num + dong_yao) % 8 or 8
    bian_lower_num = (lower_num + dong_yao) % 8 or 8
    bian_upper = get_bagua(bian_upper_num)
    bian_lower = get_bagua(bian_lower_num)
    bian_gua = f"{bian_upper['name']}{bian_lower['name']}"
    
    # 体用生克判断
    ti_wx = ti["wuxing"]
    yong_wx = yong["wuxing"]
    
    if ti_wx == yong_wx:
        relation = "体用比和"
        luck = "吉"
    elif WUXING_SHENG.get(ti_wx) == yong_wx:
        relation = "体生用"
        luck = "耗"
    elif WUXING_SHENG.get(yong_wx) == ti_wx:
        relation = "用生体"
        luck = "益"
    elif WUXING_KE.get(ti_wx) == yong_wx:
        relation = "体克用"
        luck = "胜"
    elif WUXING_KE.get(yong_wx) == ti_wx:
        relation = "用克体"
        luck = "凶"
    else:
        relation = "未知"
        luck = "平"
    
    return {
        "ben_gua": ben_gua,
        "ben_upper": upper,
        "ben_lower": lower,
        "hu_gua": hu_gua,
        "hu_upper": hu_upper,
        "hu_lower": hu_lower,
        "bian_gua": bian_gua,
        "bian_upper": bian_upper,
        "bian_lower": bian_lower,
        "dong_yao": dong_yao,
        "ti": ti,
        "yong": yong,
        "ti_position": ti_position,
        "yong_position": yong_position,
        "ti_wuxing": ti_wx,
        "yong_wuxing": yong_wx,
        "relation": relation,
        "luck": luck,
    }

# ============================================================
# DeepSeek API 调用
# ============================================================

SYSTEM_PROMPT = """你是一位专业的梅花易数研究者与传统文化解卦师。请严格基于梅花易数体系进行解读，围绕本卦、互卦、变卦、体用五行生克、动爻变化展开分析。

解读必须紧扣用户所问之事与当前卦象信息，不得脱离卦理自由发挥，不得写成夸张江湖断语，不得作出确定性预测。语言应稳重、专业、克制、有逻辑，结构清晰。

请按以下结构输出，总字数控制在300-600字：
1. 卦象总断
2. 本卦、互卦、变卦关系分析
3. 体用五行生克判断
4. 动爻变化与吉凶指向
5. 针对当前问题的具体建议

最后必须附加：声明：以上为梅花易数传统文化框架下的卦理解读，仅供文化研究与决策参考，不构成对现实事件的确定性预测。"""

def call_deepseek(api_key, api_url, model_name, question, gua_data):
    """调用 DeepSeek API 解卦"""
    
    user_content = f"""
【用户所问】：{question}

【起卦时间】：{gua_data.get('time_str', '未知')}

【本卦】：{gua_data['ben_gua']}（上卦{gua_data['ben_upper']['name']}{gua_data['ben_upper']['nature']}，下卦{gua_data['ben_lower']['name']}{gua_data['ben_lower']['nature']}）

【互卦】：{gua_data['hu_gua']}

【变卦】：{gua_data['bian_gua']}

【动爻】：第{gua_data['dong_yao']}爻

【体卦】：{gua_data['ti']['name']}（{gua_data['ti_position']}，五行属{gua_data['ti_wuxing']}）
【用卦】：{gua_data['yong']['name']}（{gua_data['yong_position']}，五行属{gua_data['yong_wuxing']}）

【体用关系】：{gua_data['relation']}（{gua_data['luck']}）

请根据以上卦象信息，对用户的问题进行专业解读。
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"API 请求失败：{str(e)}"
    except (KeyError, IndexError) as e:
        return f"API 返回格式异常：{str(e)}"

# ============================================================
# 页面渲染
# ============================================================

# 读取 API 配置
try:
    API_KEY = st.secrets["LLM_API_KEY"]
    API_URL = st.secrets["LLM_API_URL"]
    MODEL_NAME = st.secrets["LLM_MODEL"]
    HAS_API = True
except Exception:
    HAS_API = False

# 标题区
st.markdown('<div class="taiji">☯</div>', unsafe_allow_html=True)
st.markdown("# 人生决策室")
st.markdown('<div class="divider">— 梅 花 易 数 · AI 解 卦 —</div>', unsafe_allow_html=True)

if not HAS_API:
    st.warning("⚠️ 未配置 API Key，请在 .streamlit/secrets.toml 中配置 LLM_API_KEY")
    st.stop()

# 输入区
st.markdown('<p class="section-label">◆ 起 卦 信 息 ◆</p>', unsafe_allow_html=True)

# 时间输入
col1, col2 = st.columns(2)
with col1:
    input_date = st.date_input("起卦日期", value=datetime.now())
with col2:
    input_hour = st.selectbox("起卦时辰", 
        options=list(range(24)),
        index=datetime.now().hour,
        format_func=lambda x: f"{x:02d}:00 - {x:02d}:59")

# 问题输入
question = st.text_area("请默念所问之事，写下你的问题：", 
                        placeholder="例如：这份工作offer要不要接？",
                        height=100)

# 起卦按钮
if st.button("⚜️ 起 卦 ⚜️"):
    if not question.strip():
        st.error("请输入您想问的问题")
        st.stop()
    
    # 执行起卦
    year = input_date.year
    month = input_date.month
    day = input_date.day
    
    gua = meihua_qigua(year, month, day, input_hour)
    gua["time_str"] = f"{year}年{month}月{day}日 {input_hour:02d}时"
    
    # 展示卦象
    st.markdown("---")
    st.markdown('<p class="section-label">◆ 卦 象 排 盘 ◆</p>', unsafe_allow_html=True)
    
    col_ben, col_hu, col_bian = st.columns(3)
    
    with col_ben:
        st.markdown(f"""
        <div class="gua-card">
            <p class="section-label">本 卦</p>
            <p class="gua-symbol">{gua['ben_upper']['symbol']}{gua['ben_lower']['symbol']}</p>
            <p style="font-size:1.2rem; color:#d4af37;">{gua['ben_gua']}</p>
            <p style="font-size:0.85rem; color:#8b9dc3;">上{gua['ben_upper']['name']}·下{gua['ben_lower']['name']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_hu:
        st.markdown(f"""
        <div class="gua-card">
            <p class="section-label">互 卦</p>
            <p class="gua-symbol">{gua['hu_upper']['symbol']}{gua['hu_lower']['symbol']}</p>
            <p style="font-size:1.2rem; color:#8b9dc3;">{gua['hu_gua']}</p>
            <p style="font-size:0.85rem; color:#8b9dc3;">过程·潜藏</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_bian:
        st.markdown(f"""
        <div class="gua-card">
            <p class="section-label">变 卦</p>
            <p class="gua-symbol">{gua['bian_upper']['symbol']}{gua['bian_lower']['symbol']}</p>
            <p style="font-size:1.2rem; color:#c0392b;">{gua['bian_gua']}</p>
            <p style="font-size:0.85rem; color:#8b9dc3;">结果·走向</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 体用信息
    st.markdown(f"""
    <div class="gua-card">
        <p style="font-size:0.95rem; line-height:2;">
            <span style="color:#8b9dc3;">动爻：</span>第 <span style="color:#d4af37; font-weight:bold;">{gua['dong_yao']}</span> 爻<br>
            <span style="color:#8b9dc3;">体卦：</span>{gua['ti']['name']}（{gua['ti_position']}，{gua['ti_wuxing']}）　
            <span style="color:#8b9dc3;">用卦：</span>{gua['yong']['name']}（{gua['yong_position']}，{gua['yong_wuxing']}）<br>
            <span style="color:#8b9dc3;">体用关系：</span>
            <span style="color:#{'#27ae60' if gua['luck'] in ['吉','益','胜'] else '#c0392b' if gua['luck']=='凶' else '#f39c12'};">
                {gua['relation']}（{gua['luck']}）
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI 解读
    st.markdown("---")
    st.markdown('<p class="section-label">◆ 卦 理 解 读 ◆</p>', unsafe_allow_html=True)
    
    with st.spinner("☯ 推演卦象中..."):
        result = call_deepseek(API_KEY, API_URL, MODEL_NAME, question, gua)
        
        st.markdown(f'<div class="ai-result">{result}</div>', unsafe_allow_html=True)

# 底部免责
st.markdown("""
<div class="disclaimer">
    声明：本站为梅花易数传统文化研究演示，卦象解读仅供文化参考，不构成任何决策依据。
</div>
""", unsafe_allow_html=True)
#（注：内容由AI生成）
