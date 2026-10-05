"""梅花易数起卦引擎 — 支持时间起卦和铜钱起卦。

Usage:
    from meihua_yi import qigua_time, qigua_coin, compute_hexagrams, get_gua_name

    # 时间起卦
    lines, moving = qigua_time()
    result = compute_hexagrams(lines, moving)

    # 铜钱起卦
    lines, moving, details = qigua_coin()
    result = compute_hexagrams(lines, moving)
"""

from meihua_yi.engine import (
    qigua_time,
    qigua_coin,
    compute_hexagrams,
    get_gua_name,
    format_hexagram_text,
    BAGUA,
    XIAN_TIAN,
    GUA_NAMES,
)

__version__ = "0.1.0"
__author__ = "maolige"
__all__ = [
    "qigua_time",
    "qigua_coin",
    "compute_hexagrams",
    "get_gua_name",
    "format_hexagram_text",
    "BAGUA",
    "XIAN_TIAN",
    "GUA_NAMES",
]
