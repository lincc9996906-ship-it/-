#!/usr/bin/env python3
"""基础用法示例：时间起卦 + 铜钱起卦"""

from meihua_yi import (
    qigua_time,
    qigua_coin,
    compute_hexagrams,
    get_gua_name,
    format_hexagram_text,
    analyze_ti_yong,
)

print("=" * 50)
print("示例 1: 时间起卦")
print("=" * 50)

lines, moving = qigua_time()
result = compute_hexagrams(lines, moving)

print(f"六爻: {lines}")
print(f"动爻: 第{moving[0]+1}爻")
print(f"主卦: {get_gua_name(lines)}")
print(f"互卦: {get_gua_name(result['mutual']['lines'])}")
print(f"变卦: {get_gua_name(result['changed']['lines'])}")

rel, fortune = analyze_ti_yong(result["ti"]["element"], result["yong"]["element"])
print(f"体卦: {result['ti']['name']}({result['ti']['element']})")
print(f"用卦: {result['yong']['name']}({result['yong']['element']})")
print(f"关系: {rel} → {fortune}")

print("\n" + "=" * 50)
print("示例 2: 铜钱起卦")
print("=" * 50)

lines2, moving2, details = qigua_coin()
result2 = compute_hexagrams(lines2, moving2)

print(f"投掷详情:")
for d in details:
    mark = " ← 动爻" if d["moving"] else ""
    print(f"  第{d['yao']}爻: {d['name']} (和={d['sum']}) = {d['line']}爻{mark}")

print(f"主卦: {get_gua_name(lines2)}")
print(f"互卦: {get_gua_name(result2['mutual']['lines'])}")
print(f"变卦: {get_gua_name(result2['changed']['lines'])}")

rel2, fortune2 = analyze_ti_yong(result2["ti"]["element"], result2["yong"]["element"])
print(f"关系: {rel2} → {fortune2}")

print("\n" + "=" * 50)
print("示例 3: LLM 解卦文本")
print("=" * 50)
print(format_hexagram_text(lines2, moving2))
