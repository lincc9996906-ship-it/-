#!/usr/bin/env python3
"""梅花易数 CLI 工具。

用法:
    meihua --question "近期投资怎么样"
    meihua --question "明天能涨吗" --method coin
    meihua --json --question "项目能成功吗" --method coin
"""

import argparse
import json
import sys
from datetime import datetime

from meihua_yi.engine import (
    qigua_time,
    qigua_coin,
    compute_hexagrams,
    get_gua_name,
    print_hexagrams,
    analyze_ti_yong,
)


def main():
    parser = argparse.ArgumentParser(
        description="梅花易数起卦工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  meihua --question "近期投资怎么样"              # 时间起卦
  meihua --question "明天能涨吗" --method coin     # 铜钱起卦
  meihua --json --question "项目能成功吗"           # JSON 输出
  meihua --coins "6,7,8,9,7,6"                     # 指定铜钱结果
        """,
    )
    parser.add_argument("--question", "-q", type=str, help="求问的问题")
    parser.add_argument(
        "--method", "-m",
        choices=["time", "coin"],
        default="time",
        help="起卦方法: time=时间起卦(默认), coin=铜钱起卦",
    )
    parser.add_argument(
        "--coins", "-c",
        type=str,
        help="铜钱投掷结果(逗号分隔的6个数字, 6/7/8/9)。不指定则随机",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()
    now = datetime.now()

    if args.method == "coin":
        if args.coins:
            coin_results = [int(x.strip()) for x in args.coins.split(",")]
        else:
            coin_results = None

        main_lines, moving_indices, details = qigua_coin(coin_results)
    else:
        main_lines, moving_indices = qigua_time(now)
        details = None

    hg = compute_hexagrams(main_lines, moving_indices)
    m, mu, c = hg["main"], hg["mutual"], hg["changed"]

    if args.json:
        result = {
            "method": args.method,
            "time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "question": args.question,
            "main_gua": {
                "name": get_gua_name(main_lines),
                "top": m["top"],
                "bot": m["bot"],
                "lines": main_lines,
            },
            "mutual_gua": {
                "name": get_gua_name(mu["lines"]),
                "top": mu["top"],
                "bot": mu["bot"],
                "lines": mu["lines"],
            },
            "changed_gua": {
                "name": get_gua_name(c["lines"]),
                "top": c["top"],
                "bot": c["bot"],
                "lines": c["lines"],
            },
            "moving_lines": [i + 1 for i in moving_indices],
            "ti": hg["ti"],
            "yong": hg["yong"],
        }
        if details:
            result["coin_details"] = details

        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n起卦时间: {now.strftime('%Y年%m月%d日 %H:%M')}")
        print(f"起卦方法: {'铜钱起卦（3枚硬币抛6次）' if args.method == 'coin' else '梅花易数时间起卦'}")
        if args.question:
            print(f"问题: {args.question}")

        if details:
            print("\n【投掷详情】")
            for d in details:
                mark = " ← 动爻" if d["moving"] else ""
                print(f"  第{d['yao']}爻: {d['name']} (和={d['sum']}) = {d['line']}爻{mark}")

        print_hexagrams(main_lines, moving_indices)

        print(f"\n主卦名: {get_gua_name(main_lines)}")
        print(f"互卦名: {get_gua_name(mu['lines'])}")
        print(f"变卦名: {get_gua_name(c['lines'])}")

        rel, fortune = analyze_ti_yong(hg["ti"]["element"], hg["yong"]["element"])
        print(f"\n体卦: {hg['ti']['name']}({hg['ti']['element']})")
        print(f"用卦: {hg['yong']['name']}({hg['yong']['element']})")
        print(f"关系: {rel} → {fortune}")


if __name__ == "__main__":
    main()
