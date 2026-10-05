---
name: meihua-yi
description: 梅花易数起卦工具。用于用户要求起卦、算卦、易经分析时调用。
---

# 梅花易数起卦

## 触发

用户说"起卦"、"算卦"、"梅花易数"、"解卦"或用易经分析问题。

## 命令

```bash
# 铜钱起卦（推荐）
python -m meihua_yi.cli --json --method coin --question "问题"

# 时间起卦
python -m meihua_yi.cli --json --method time --question "问题"
```

## 解卦

从 JSON 输出提取：
- main_gua.name / top / bot
- mutual_gua.name
- changed_gua.name
- ti / yong 五行
- moving_lines

按体用生克分析：用生体大吉 > 比和 > 体克用 > 体生用 > 用克体大凶。

输出包含卦象摘要 + 解卦结论。
