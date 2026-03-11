from dataclasses import dataclass
from math import isfinite

import matplotlib

matplotlib.use('Agg')  # 使用非交互式后端，适合脚本/服务器环境
import matplotlib.pyplot as plt
from matplotlib import font_manager


@dataclass(frozen=True)
class FinancialData:
    """财务输入数据（单位：万元）。"""

    quarters: list[str]
    revenue: list[float]
    cost: list[float]


def load_financial_data() -> FinancialData:
    """加载示例季度、收入、成本数据。"""
    return FinancialData(
        quarters=['Q1', 'Q2', 'Q3', 'Q4'],
        revenue=[120, 150, 180, 160],
        cost=[80, 90, 110, 100],
    )


def validate_financial_data(data: FinancialData) -> None:
    """对输入数据做完整校验，发现问题立即抛错。"""
    if not data.quarters:
        raise ValueError("quarters 不能为空")

    if not (len(data.quarters) == len(data.revenue) == len(data.cost)):
        raise ValueError("quarters、revenue、cost 的长度必须一致")

    for i, quarter in enumerate(data.quarters):
        if not isinstance(quarter, str) or not quarter.strip():
            raise ValueError(f"quarters[{i}] 必须是非空字符串")

    for name, values in (("revenue", data.revenue), ("cost", data.cost)):
        for i, value in enumerate(values):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{name}[{i}] 必须是数值类型")
            if not isfinite(value):
                raise ValueError(f"{name}[{i}] 不能是 NaN 或无穷大")
            if value < 0:
                raise ValueError(f"{name}[{i}] 不能为负数")


def calculate_profit(data: FinancialData) -> list[float]:
    """计算各季度利润：收入 - 成本。"""
    return [r - c for r, c in zip(data.revenue, data.cost)]


def find_best_quarter(quarters: list[str], profits: list[float]) -> tuple[str, float]:
    """返回利润最高季度及对应利润。"""
    best_idx = max(range(len(profits)), key=profits.__getitem__)
    return quarters[best_idx], profits[best_idx]


def configure_chinese_font() -> str:
    """配置支持中文的字体，返回实际使用的字体名。"""
    preferred_fonts = [
        'Microsoft YaHei',
        'SimHei',
        'Noto Sans CJK SC',
        'Source Han Sans SC',
        'WenQuanYi Micro Hei',
        'Arial Unicode MS',
    ]

    available_fonts = {f.name for f in font_manager.fontManager.ttflist}
    selected_font = next((name for name in preferred_fonts if name in available_fonts), None)
    if selected_font is None:
        raise RuntimeError(
            "未找到可用中文字体。请先安装 Microsoft YaHei、SimHei 或 Noto Sans CJK SC。"
        )

    plt.rcParams['font.sans-serif'] = [selected_font]
    plt.rcParams['axes.unicode_minus'] = False
    return selected_font


def plot_profit_chart(
    quarters: list[str], profits: list[float], output_path: str = 'profit_chart.png'
) -> None:
    """绘制并保存季度利润柱状图。"""
    plt.figure(figsize=(8, 6))
    plt.bar(quarters, profits, color='skyblue')
    plt.title('Quarterly Profit')
    plt.xlabel('Quarter')
    plt.ylabel('Profit (万元)')
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()


def main() -> None:
    # 1) 数据准备与校验
    data = load_financial_data()
    print("数据加载成功！")
    validate_financial_data(data)

    # 2) 计算与结果输出
    profits = calculate_profit(data)
    print("各季度利润:", profits)
    best_quarter, best_profit = find_best_quarter(data.quarters, profits)
    print(f"利润最高季度: {best_quarter}（{best_profit} 万元）")

    # 3) 可视化输出
    font_name = configure_chinese_font()
    print(f"已配置中文字体: {font_name}")
    plot_profit_chart(data.quarters, profits)
    print("图表已保存为 profit_chart.png")
    print("脚本执行完成！")


if __name__ == '__main__':
    main()


