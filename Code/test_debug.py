#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("开始测试...")

try:
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    revenue = [120, 150, 180, 160]
    cost = [80, 90, 110, 100]
    print("数据加载成功！")
    
    profit = []
    for i in range(len(quarters)):
        p = revenue[i] - cost[i]
        profit.append(p)
    
    print(f"各季度利润: {profit}")
    print(f"各季度: {quarters}")
    
    print("即将导入matplotlib...")
    import matplotlib
    print(f"matplotlib版本: {matplotlib.__version__}")
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    print("matplotlib导入成功")
    
    plt.figure(figsize=(8, 6))
    plt.bar(quarters, profit, color='skyblue')
    plt.title('Quarterly Profit')
    plt.xlabel('Quarter')
    plt.ylabel('Profit (万元)')
    plt.savefig('profit_chart.png', dpi=100, bbox_inches='tight')
    print("图表已保存为 profit_chart.png")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("测试完成！")
