# 梅花易数 (meihua-yi)

[![PyPI version](https://img.shields.io/pypi/v/meihua-yi.svg)](https://pypi.org/project/meihua-yi/)
[![Python](https://img.shields.io/pypi/pyversions/meihua-yi.svg)](https://pypi.org/project/meihua-yi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于梅花易数的 Python 起卦工具。支持**时间起卦**和**铜钱起卦**，纯算法零依赖，可对接任何 LLM 做解卦。

```bash
pip install meihua-yi
```

## 快速开始

### CLI

```bash
# 铜钱起卦（推荐，每次结果不同）
meihua -q "近期投资怎么样" -m coin

# 时间起卦
meihua -q "明天能涨吗"

# JSON 输出（供程序调用）
meihua --json -q "项目能成功吗" -m coin
```

### Python API

```python
from meihua_yi import qigua_coin, compute_hexagrams, analyze_ti_yong

lines, moving, _ = qigua_coin()
result = compute_hexagrams(lines, moving)

rel, fortune = analyze_ti_yong(result["ti"]["element"], result["yong"]["element"])
print(f"{rel} → {fortune}")  # 用生体（得助） → 大吉
```

## 特性

- **两种起卦法**：时间起卦（同一时辰结果相同）、铜钱起卦（每次随机不同）
- **完整卦象计算**：主卦、互卦、变卦、体用关系、五行生克判断
- **64 卦全名表**：内置完整六十四卦名映射
- **LLM 友好**：`format_hexagram_text()` 输出专为 LLM prompt 设计的格式
- **Agent Skills**：内置 Hermes / Claude Code / OpenClaw 技能文件，Agent 开箱即用
- **纯 Python**：零网络请求，无外部依赖（lunardate 可选）

## 输出示例

```
起卦时间: 2026年05月13日 18:03
起卦方法: 铜钱起卦（3枚硬币抛6次）
问题: 近期投资怎么样

【投掷详情】
  第1爻: 老阴 (和=6) = 阴爻 ← 动爻
  第2爻: 少阳 (和=7) = 阳爻
  第3爻: 老阴 (和=6) = 阴爻 ← 动爻
  第4爻: 老阳 (和=9) = 阳爻 ← 动爻
  第5爻: 少阳 (和=7) = 阳爻
  第6爻: 少阳 (和=7) = 阳爻

================ 起卦结果 ================

      【主卦】          【互卦】          【变卦】
上卦: 乾(金) ☰     上卦: 巽(木) ☴     上卦: 乾(金) ☰
下卦: 坎(水) ☵     下卦: 离(火) ☲     下卦: 巽(木) ☴

第6爻: ▅▅▅▅▅       ▅▅▅▅▅       ▅▅▅▅▅
第5爻: ▅▅▅▅▅       ▅▅  ▅▅       ▅▅  ▅▅
第4爻: ▅▅  ▅▅ (动)  ▅▅▅▅▅       ▅▅▅▅▅
第3爻: ▅▅▅▅▅       ▅▅  ▅▅       ▅▅▅▅▅
第2爻: ▅▅  ▅▅       ▅▅▅▅▅       ▅▅▅▅▅
第1爻: ▅▅  ▅▅ (动)  ▅▅  ▅▅       ▅▅▅▅▅

==========================================

主卦名: 天水讼
互卦名: 风火家人
变卦名: 天风姤

体卦: 乾(金)
用卦: 坎(水)
关系: 体生用（泄气） → 不利
```

## 体用五行生克

| 关系 | 含义 | 吉凶 |
|------|------|------|
| 用生体 | 得助 | 大吉 |
| 体用比和 | 平顺 | 中性 |
| 体克用 | 可成但费力 | 中性偏吉 |
| 体生用 | 泄气 | 不利 |
| 用克体 | 被压制 | 大凶 |

五行相生：金→水→木→火→土→金
五行相克：金→木→土→水→火→金

## 与 LLM 结合

`format_hexagram_text()` 输出专为 LLM 设计的 prompt 格式：

```python
from meihua_yi import qigua_coin, format_hexagram_text

lines, moving, _ = qigua_coin()
text = format_hexagram_text(lines, moving)
# 将 text 发送给任何 LLM，配合解卦 prompt 即可
```

完整示例见 [examples/llm_decode.py](examples/llm_decode.py)。

## Agent Skills

内置三大 Agent 平台的技能文件，Agent 看到"起卦"关键词自动调用：

| 平台 | 安装方式 |
|------|----------|
| **Hermes Agent** | `cp skills/hermes/SKILL.md ~/.hermes/skills/meihua-yi/` |
| **Claude Code** | `cp skills/claude-code/CLAUDE.md your-project/` |
| **OpenClaw** | 按平台 skill 目录规则放置 |

## API 参考

### `qigua_time(dt=None)` — 时间起卦

```python
lines, moving = qigua_time()
# lines: [0, 1, 0, 1, 1, 1]  # 0=阴, 1=阳
# moving: [2]  # 第3爻动
```

### `qigua_coin(coin_results=None)` — 铜钱起卦

```python
# 随机生成
lines, moving, details = qigua_coin()

# 指定结果
lines, moving, details = qigua_coin([6, 7, 8, 9, 7, 6])
```

铜钱规则：正面(字)=2，反面(花)=3，每次3枚总和：

| 总和 | 名称 | 爻型 | 动静 |
|------|------|------|------|
| 6 | 老阴 | 阴爻 | 动 |
| 7 | 少阳 | 阳爻 | 静 |
| 8 | 少阴 | 阴爻 | 静 |
| 9 | 老阳 | 阳爻 | 动 |

### `compute_hexagrams(lines, moving)` — 卦象计算

返回 dict：`main`, `mutual`, `changed`, `ti`, `yong`, `moving_indices`。

### `get_gua_name(lines)` — 获取卦名

```python
get_gua_name([0, 1, 0, 1, 1, 1])  # "天水讼"
```

### `analyze_ti_yong(ti_element, yong_element)` — 五行生克

```python
rel, fortune = analyze_ti_yong("木", "水")  # ("用生体（得助）", "大吉")
```

## 原理

### 时间起卦

1. 取农历（或公历）年、月、日之和，除以 8 取余 → 上卦
2. 加上时辰数，除以 8 取余 → 下卦
3. 总和除以 6 取余 → 动爻

### 铜钱起卦

1. 3 枚硬币各掷 6 次，记录每次 3 枚之和
2. 和为 6/9 为动爻，和为 7/8 为静爻
3. 老阴(6)为阴爻动，老阳(9)为阳爻动

### 体用规则

- 动爻在下卦（1-3爻），上卦为体，下卦为用
- 动爻在上卦（4-6爻），下卦为体，上卦为用
- 多动爻时以第一个动爻确定体用

## 开发

```bash
git clone https://github.com/handsomejustin/meihua-yi.git
cd meihua-yi
pip install -e ".[dev]"
pytest
```

## License

[MIT](LICENSE)
