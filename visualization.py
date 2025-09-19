# visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
sns.set_style("whitegrid")


def create_static_plots(df):
    """
    创建静态图表 (Matplotlib/Seaborn)
    """
    print("生成静态图表...")

    # 1. 各区域房价分布箱线图
    plt.figure(figsize=(12, 8))
    # 按平均单价排序区域
    order = df.groupby('district')['price_per_sqm'].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x='district', y='price_per_sqm', order=order)
    plt.title('成都市各区域二手房单价分布')
    plt.xlabel('区域')
    plt.ylabel('单价 (元/平米)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/district_price_boxplot.png', dpi=300)
    plt.close()

    # 2. 房价与面积的关系散点图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='area', y='price_per_sqm', hue='district', alpha=0.6, palette='viridis')
    plt.title('二手房面积与单价关系')
    plt.xlabel('面积 (平米)')
    plt.ylabel('单价 (元/平米)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/area_vs_price_scatter.png', dpi=300)
    plt.close()

    # 3. 房龄与单价的关系
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='house_age', y='price_per_sqm', scatter_kws={'alpha': 0.3}, line_kws={"color": "red"})
    plt.title('房龄对单价的影响')
    plt.xlabel('房龄 (年)')
    plt.ylabel('单价 (元/平米)')
    plt.tight_layout()
    plt.savefig('plots/age_vs_price_regplot.png', dpi=300)
    plt.close()

    # 4. 相关性热力图
    numeric_features = ['price_per_sqm', 'area', 'house_age', 'subway_distance', 'rooms', 'floor_ratio']
    plt.figure(figsize=(10, 8))
    corr = df[numeric_features].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, square=True)
    plt.title('特征相关性热力图')
    plt.tight_layout()
    plt.savefig('plots/correlation_heatmap.png', dpi=300)
    plt.close()

    print("静态图表已保存至 'plots/' 目录")


def create_interactive_plots(df):
    """
    创建交互式图表 (Plotly)
    """
    print("生成交互式图表...")

    # 1. 各区域平均单价柱状图
    district_avg = df.groupby('district')['price_per_sqm'].mean().sort_values().reset_index()
    fig1 = px.bar(district_avg, x='price_per_sqm', y='district', orientation='h',
                  title='成都市各区域二手房平均单价',
                  labels={'price_per_sqm': '平均单价 (元/平米)', 'district': '区域'})
    fig1.write_html('plots/interactive_district_price.html')

    # 2. 房价与面积、房龄的交互散点图
    fig2 = px.scatter(df, x='area', y='price_per_sqm', color='district',
                      size='house_age', hover_data=['layout', 'decoration'],
                      title='面积、区域、房龄与单价的关系',
                      labels={'area': '面积 (平米)', 'price_per_sqm': '单价 (元/平米)', 'district': '区域',
                              'house_age': '房龄'})
    fig2.write_html('plots/interactive_bubble_chart.html')

    # 3. 房价分布直方图
    fig3 = px.histogram(df, x='price_per_sqm', nbins=50, marginal='box',
                        title='成都市二手房单价分布',
                        labels={'price_per_sqm': '单价 (元/平米)', 'count': '房源数量'})
    fig3.write_html('plots/interactive_price_distribution.html')

    # 4. 平行坐标图 (展示多变量关系)
    fig4 = px.parallel_categories(df, dimensions=['district', 'decoration', 'has_elevator'],
                                  color='price_per_sqm', color_continuous_scale=px.colors.sequential.Inferno,
                                  title='区域、装修、电梯与房价的关系')
    fig4.write_html('plots/interactive_parallel_categories.html')

    print("交互式图表 (HTML) 已保存至 'plots/' 目录")


if __name__ == "__main__":
    # 确保有plots目录
    import os

    if not os.path.exists('plots'):
        os.makedirs('plots')

    df = pd.read_csv('data/chengdu_housing_cleaned.csv')
    create_static_plots(df)
    create_interactive_plots(df)