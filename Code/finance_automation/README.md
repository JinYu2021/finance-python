# 财务自动化项目

这个项目实现了你要求的 4 个功能：

1. 读取 Excel
2. 计算项目现金流
3. 生成预测表
4. 输出 Power BI 数据

## 目录结构

- `run_finance_pipeline.py`：主程序
- `input/`：放置 Excel 输入文件
- `output/`：程序输出目录（自动生成）
- `requirements.txt`：依赖

## 输入 Excel 格式

默认读取第一个 Sheet，需要以下列（大小写不敏感）：

- `Project`：项目名称
- `Period`：期间（日期，例如 `2026-01-01`）
- `Revenue`：收入
- `OperatingCost`：运营成本
- `Capex`：资本开支
- `Tax`：税费
- `WorkingCapitalDelta`：营运资金变化（增加为现金流出，减少为现金流入）

## 快速开始

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 生成示例输入（可选）

```bash
python run_finance_pipeline.py --create-sample --input input/sample_projects.xlsx
```

3. 运行管道

```bash
python run_finance_pipeline.py --input input/sample_projects.xlsx --output output --forecast-periods 12
```

## 输出文件

运行后会在输出目录生成：

- `cashflow_actual.csv`：历史现金流
- `cashflow_forecast.csv`：预测现金流
- `powerbi_fact_cashflow.csv`：Power BI 事实表（历史+预测）
- `powerbi_dim_project.csv`：Power BI 维度表（项目）

## 现金流计算逻辑

每期净现金流：

```text
NetCashFlow = Revenue - OperatingCost - Capex - Tax - WorkingCapitalDelta
```

并按项目计算累计现金流 `CumulativeCashFlow`。

## 预测逻辑（简化版）

- 收入与运营成本：按历史平均环比增长率外推
- 资本开支、税费、营运资金变化：按最近 3 期均值外推
- 预测期间默认按月递增

你后续可以把预测逻辑替换为更复杂模型（回归、季节性、预算输入等）。
