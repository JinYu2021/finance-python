quarters = ['Q1', 'Q2', 'Q3', 'Q4']
revenue = [120, 150, 180, 160]
cost = [80, 90, 110, 100]

profit = []
for i in range(len(quarters)):
    p = revenue[i] - cost[i]
    profit.append(p)

# 输出结果
print(f"季度: {quarters}")
print(f"收入: {revenue}")
print(f"成本: {cost}")
print(f"利润: {profit}")

# 最高利润的季度
max_profit_index = profit.index(max(profit))
print(f"\n最高利润: {max(profit)} 万元 ({quarters[max_profit_index]})")
