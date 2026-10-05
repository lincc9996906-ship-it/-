"""梅花易数引擎单元测试。"""

import pytest
from meihua_yi.engine import (
    qigua_time,
    qigua_coin,
    compute_hexagrams,
    get_gua_name,
    analyze_ti_yong,
    BAGUA,
    GUA_NAMES,
)


class TestQiguaCoin:
    """铜钱起卦测试"""

    def test_all_yin(self):
        """全老阴 → 六爻全阴"""
        lines, moving, details = qigua_coin([6, 6, 6, 6, 6, 6])
        assert lines == [0, 0, 0, 0, 0, 0]
        assert moving == [0, 1, 2, 3, 4, 5]

    def test_all_yang(self):
        """全老阳 → 六爻全阳"""
        lines, moving, details = qigua_coin([9, 9, 9, 9, 9, 9])
        assert lines == [1, 1, 1, 1, 1, 1]
        assert moving == [0, 1, 2, 3, 4, 5]

    def test_no_moving(self):
        """全静爻 → 无动爻"""
        lines, moving, details = qigua_coin([7, 8, 7, 8, 7, 8])
        assert moving == []
        assert lines == [1, 0, 1, 0, 1, 0]

    def test_qian_tian(self):
        """乾为天：少阳少阳少阳少阳少阳少阳"""
        lines, moving, details = qigua_coin([7, 7, 7, 7, 7, 7])
        assert lines == [1, 1, 1, 1, 1, 1]
        assert get_gua_name(lines) == "乾为天"

    def test_kun_wei_di(self):
        """坤为地：少阴少阴少阴少阴少阴少阴"""
        lines, moving, details = qigua_coin([8, 8, 8, 8, 8, 8])
        assert lines == [0, 0, 0, 0, 0, 0]
        assert get_gua_name(lines) == "坤为地"

    def test_invalid_sum(self):
        """无效总和应报错"""
        with pytest.raises(ValueError):
            qigua_coin([5, 7, 8, 9, 7, 6])

    def test_wrong_count(self):
        """非6次应报错"""
        with pytest.raises(ValueError):
            qigua_coin([6, 7, 8])

    def test_random(self):
        """随机生成应返回6次结果"""
        lines, moving, details = qigua_coin()
        assert len(lines) == 6
        assert len(details) == 6
        assert all(l in [0, 1] for l in lines)


class TestQiguaTime:
    """时间起卦测试"""

    def test_returns_valid_lines(self):
        """应返回6个爻"""
        from datetime import datetime
        dt = datetime(2026, 5, 13, 18, 3)
        lines, moving = qigua_time(dt)
        assert len(lines) == 6
        assert all(l in [0, 1] for l in lines)

    def test_single_moving(self):
        """时间起卦只有一个动爻"""
        from datetime import datetime
        dt = datetime(2026, 5, 13, 18, 3)
        lines, moving = qigua_time(dt)
        assert len(moving) == 1
        assert 0 <= moving[0] <= 5

    def test_same_shichen_same_result(self):
        """同一时辰结果相同（19:00 和 20:00 都是亥时）"""
        from datetime import datetime
        dt1 = datetime(2026, 5, 13, 19, 0)
        dt2 = datetime(2026, 5, 13, 20, 59)
        lines1, moving1 = qigua_time(dt1)
        lines2, moving2 = qigua_time(dt2)
        assert lines1 == lines2
        assert moving1 == moving2


class TestComputeHexagrams:
    """卦象计算测试"""

    def test_qian_mutual_qian(self):
        """乾为天的互卦是乾为天"""
        lines = [1, 1, 1, 1, 1, 1]
        result = compute_hexagrams(lines, [0])
        assert get_gua_name(result["mutual"]["lines"]) == "乾为天"

    def test_kun_mutual_kun(self):
        """坤为地的互卦是坤为地"""
        lines = [0, 0, 0, 0, 0, 0]
        result = compute_hexagrams(lines, [0])
        assert get_gua_name(result["mutual"]["lines"]) == "坤为地"

    def test_changed_flips_moving(self):
        """变卦翻转动爻"""
        lines = [1, 0, 1, 0, 1, 0]
        result = compute_hexagrams(lines, [1, 3])
        # 第2爻(0→1)和第4爻(0→1)翻转
        assert result["changed"]["lines"] == [1, 1, 1, 1, 1, 0]

    def test_ti_yong_lower_moving(self):
        """动爻在下卦，上卦为体"""
        lines = [0, 1, 0, 1, 1, 1]  # 坎下乾上 = 讼
        result = compute_hexagrams(lines, [1])
        assert result["ti"]["name"] == "乾"  # 上卦为体
        assert result["yong"]["name"] == "坎"  # 下卦为用

    def test_ti_yong_upper_moving(self):
        """动爻在上卦，下卦为体"""
        lines = [0, 1, 0, 1, 1, 1]  # 坎下乾上 = 讼
        result = compute_hexagrams(lines, [4])
        assert result["ti"]["name"] == "坎"  # 下卦为体
        assert result["yong"]["name"] == "乾"  # 上卦为用


class TestGuaName:
    """卦名测试"""

    def test_known_guas(self):
        """已知卦象名称正确"""
        assert get_gua_name([1, 1, 1, 1, 1, 1]) == "乾为天"
        assert get_gua_name([0, 0, 0, 0, 0, 0]) == "坤为地"
        assert get_gua_name([0, 1, 0, 1, 1, 1]) == "天水讼"
        assert get_gua_name([0, 0, 0, 0, 1, 0]) == "水地比"
        assert get_gua_name([0, 0, 0, 0, 0, 1]) == "山地剥"

    def test_all_64(self):
        """所有64卦都有名称"""
        combos = [
            [0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1],
            [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1],
        ]
        for bot in combos:
            for top in combos:
                name = get_gua_name(bot + top)
                assert name != "未知", f"{bot}+{top} 没有卦名"


class TestAnalyzeTiYong:
    """体用五行生克测试"""

    def test_yong_sheng_ti(self):
        """用生体 → 大吉"""
        rel, fortune = analyze_ti_yong("木", "水")
        assert rel == "用生体（得助）"
        assert fortune == "大吉"

    def test_ti_sheng_yong(self):
        """体生用 → 不利"""
        rel, fortune = analyze_ti_yong("水", "木")
        assert rel == "体生用（泄气）"
        assert fortune == "不利"

    def test_ti_ke_yong(self):
        """体克用 → 可成但费力"""
        rel, fortune = analyze_ti_yong("金", "木")
        assert rel == "体克用"
        assert fortune == "可成但费力"

    def test_yong_ke_ti(self):
        """用克体 → 大凶"""
        rel, fortune = analyze_ti_yong("木", "金")
        assert rel == "用克体"
        assert fortune == "大凶"

    def test_bihe(self):
        """体用比和 → 平顺"""
        rel, fortune = analyze_ti_yong("金", "金")
        assert rel == "体用比和"
        assert fortune == "平顺"
