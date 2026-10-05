---
name: meihua-yi
description: 梅花易数起卦 + 卦象分析。支持时间起卦和铜钱起卦两种方法，计算主卦、互卦、变卦、体用关系和五行生克。适用于用户问"起卦"、"算卦"、"梅花易数"、"解卦"或提出具体问题要求用易经分析。
---

# 梅花易数起卦

基于梅花易数的 Python 起卦工具，纯算法，零网络请求。

## 触发条件

- 用户问 "起卦"、"算卦"、"梅花易数"、"解卦"
- 用户提出具体问题并要求用易经/梅花易数分析
- 用户说 "帮我算一卦"

## 前置要求

确保 `meihua-yi` 已安装：

```bash
pip install meihua-yi
```

可选：安装农历支持 `pip install meihua-yi[lunar]`

## 工作流

### 1. 运行起卦

**铜钱起卦（推荐，每次结果不同）：**

```bash
python -m meihua_yi.cli --json --method coin --question "用户的问题"
```

**时间起卦（同一时辰结果相同）：**

```bash
python -m meihua_yi.cli --json --method time --question "用户的问题"
```

如果用户连续问不同问题，优先用铜钱起卦。

### 2. 解析 JSON 输出

引擎输出 JSON，包含：

- `method`: "time" 或 "coin"
- `main_gua`: 主卦（上卦、下卦、卦名、六爻）
- `mutual_gua`: 互卦
- `changed_gua`: 变卦（所有动爻变化后）
- `moving_lines`: 动爻位置列表
- `ti`: 体卦（不变的卦）
- `yong`: 用卦（有动爻的卦）
- `coin_details`: 铜钱法才有，每次投掷详情

### 3. 解卦分析

用当前 Agent 的上下文直接解卦，无需外部 API。

**解卦分析框架：**

从 JSON 提取信息后，按以下结构解卦：

1. **主卦含义** — 说明主卦的基本象征
2. **体用关系** — 分析五行生克：
   - 用生体 → 得助（大吉）
   - 体用比和 → 平顺（中性）
   - 体克用 → 可成但费力（中性偏吉）
   - 体生用 → 泄气（不利）
   - 用克体 → 被压制（大凶）
3. **互卦分析** — 事情发展过程
4. **变卦分析** — 最终走向
5. **动爻解读** — 多个动爻时分别解读
6. **综合建议** — 给出 actionable 的建议

### 4. 输出格式

```
🔮 梅花易数解卦
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【起卦时间】YYYY年MM月DD日 HH:MM

【卦象】
主卦: XXX — 上X(X) 下X(X)
互卦: XXX — 上X(X) 下X(X)
变卦: XXX — 上X(X) 下X(X)
动爻: 第N爻
体卦: X(X)，用卦: X(X)

【解卦】
(解卦内容)
```

## 关键规则

- 体卦 = 动爻所在卦的对侧卦（动爻在下卦则上卦为体，动爻在上卦则下卦为体）
- 多个动爻时，以第一个动爻确定体用
- 五行相生：金→水→木→火→土→金
- 五行相克：金→木→土→水→火→金

## Python API 用法

```python
from meihua_yi import qigua_coin, compute_hexagrams, get_gua_name, analyze_ti_yong

# 铜钱起卦
lines, moving, details = qigua_coin()

# 计算卦象
result = compute_hexagrams(lines, moving)

# 获取卦名
print(get_gua_name(lines))  # 天水讼

# 分析体用
rel, fortune = analyze_ti_yong(result["ti"]["element"], result["yong"]["element"])
print(f"{rel} → {fortune}")  # 体生用（泄气） → 不利
```
