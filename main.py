# main.py
"""
成都市二手房房价数据分析与可视化主程序
执行顺序：
1. 生成模拟数据 (如果还没有数据)
2. 数据清洗与分析
3. 创建可视化图表
4. 启动Dash交互式仪表盘
"""

import os
import subprocess
import sys


def main():
    print("=== 成都市二手房房价数据分析与可视化项目 ===")

    # 检查数据文件是否存在
    data_file = "data/chengdu_second_hand_housing_sample.csv"
    if not os.path.exists(data_file):
        print("未找到数据文件，正在生成模拟数据...")
        # 运行数据生成脚本
        subprocess.run([sys.executable, "generate_sample_data.py"], check=True)

    # 数据清洗与分析
    print("\n1. 正在执行数据清洗与分析...")
    subprocess.run([sys.executable, "data_cleaning_analysis.py"], check=True)

    # 创建可视化图表
    print("\n2. 正在创建可视化图表...")
    # 确保plots目录存在
    if not os.path.exists('plots'):
        os.makedirs('plots')
    subprocess.run([sys.executable, "visualization.py"], check=True)

    # 启动Dash应用
    print("\n3. 启动Dash交互式仪表盘...")
    print("请访问 http://127.0.0.1:8050 查看交互式仪表盘")
    subprocess.run([sys.executable, "app.py"], check=True)


if __name__ == "__main__":
    main()