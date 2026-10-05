#!/usr/bin/env python3
"""LLM 解卦示例：将卦象文本发送给 LLM 进行解卦。

用法:
    # 设置环境变量
    export LLM_URL="http://localhost:8888/v1/chat/completions"
    export LLM_API_KEY="your-api-key"
    export LLM_MODEL="your-model-name"

    python examples/llm_decode.py --question "近期投资怎么样"
"""

import argparse
import json
import os
import sys

from meihua_yi import (
    qigua_coin,
    compute_hexagrams,
    get_gua_name,
    format_hexagram_text,
)


SYSTEM_PROMPT = """你是一位精通易经和梅花易数的解卦大师。以下是通过梅花易数铜钱起卦法得出的卦象：

{hexagram_text}

请根据以上卦象，结合梅花易数的体用关系、五行生克、卦辞爻辞，为求问者详细解卦。要求：
1. 说明主卦的基本含义
2. 分析体卦与用卦的五行生克关系
3. 结合互卦分析事情发展过程
4. 结合变卦分析最终走向
5. 解读动爻爻辞（多个动爻时分别解读）
6. 给出综合建议"""


def ask_llm(question, hexagram_text):
    """发送卦象给 LLM 并流式输出解卦结果。

    需要设置环境变量:
        LLM_URL: LLM API 地址
        LLM_API_KEY: API Key
        LLM_MODEL: 模型名称
    """
    import requests

    url = os.environ.get("LLM_URL", "http://localhost:8888/v1/chat/completions")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "default")

    system = SYSTEM_PROMPT.format(hexagram_text=hexagram_text)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"我的问题是：{question}"},
        ],
        "temperature": 0.7,
        "max_tokens": 8192,
        "stream": True,
    }

    print("\n正在解卦...\n")
    print("=" * 50)

    full_response = ""
    with requests.post(url, headers=headers, json=payload, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            decoded = raw_line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue
            data = decoded[6:]
            if data == "[DONE]":
                break
            try:
                chunk = json.loads(data)
                content = chunk["choices"][0].get("delta", {}).get("content", "")
                if content:
                    print(content, end="", flush=True)
                    full_response += content
            except (json.JSONDecodeError, KeyError, IndexError):
                continue

    print("\n" + "=" * 50)
    return full_response


def main():
    parser = argparse.ArgumentParser(description="梅花易数 LLM 解卦")
    parser.add_argument("--question", "-q", type=str, required=True, help="求问的问题")
    args = parser.parse_args()

    # 铜钱起卦
    lines, moving, details = qigua_coin()
    result = compute_hexagrams(lines, moving)

    # 打印卦象
    print(f"\n问题: {args.question}")
    print(f"主卦: {get_gua_name(lines)}")

    # 生成 LLM prompt
    hexagram_text = format_hexagram_text(lines, moving)

    # 调用 LLM
    try:
        ask_llm(args.question, hexagram_text)
    except requests.exceptions.RequestException as e:
        print(f"\n解卦失败，无法连接 LLM 服务: {e}")
        print("\n请设置环境变量:")
        print("  export LLM_URL='http://your-llm:8888/v1/chat/completions'")
        print("  export LLM_API_KEY='your-key'")
        print("  export LLM_MODEL='your-model'")
        sys.exit(1)


if __name__ == "__main__":
    main()
