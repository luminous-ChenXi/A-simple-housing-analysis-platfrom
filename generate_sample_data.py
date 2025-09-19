# generate_sample_data.py
import os
import pandas as pd
import numpy as np

# 自动创建data目录（如果不存在）
os.makedirs('data', exist_ok=True)

np.random.seed(42)
num_samples = 1000

# 模拟区域
districts = ['锦江区', '青羊区', '金牛区', '武侯区', '成华区', '高新区', '天府新区', '龙泉驿区', '温江区', '双流区']
# 模拟装修情况
decoration = ['精装', '简装', '毛坯']
# 模拟朝向
orientation = ['南', '北', '东', '西', '东南', '西南', '东北', '西北']
# 模拟是否有电梯
has_elevator = ['有', '无']

data = {
    'title': [f'房源{i}' for i in range(num_samples)],
    'total_price': np.random.normal(200, 60, num_samples).round(1),
    'price_per_sqm': np.random.normal(18000, 5000, num_samples).round(0),
    'district': np.random.choice(districts, num_samples),
    'area': np.random.uniform(50, 200, num_samples).round(1),
    'layout': [f"{np.random.randint(1, 5)}室{np.random.randint(1, 3)}厅{np.random.randint(1, 3)}卫" for _ in range(num_samples)],
    'floor': [f"{np.random.randint(1, 30)}/{np.random.randint(1, 30)}" for _ in range(num_samples)],
    'year_built': np.random.randint(1990, 2023, num_samples),
    'decoration': np.random.choice(decoration, num_samples),
    'orientation': np.random.choice(orientation, num_samples),
    'has_elevator': np.random.choice(has_elevator, num_samples, p=[0.7, 0.3]),
    'subway_distance': np.random.exponential(1000, num_samples).round(0),
}

df = pd.DataFrame(data)
df['total_price'] = (df['price_per_sqm'] * df['area'] / 10000).round(1)

# 引入一些缺失值
df.loc[df.sample(frac=0.05).index, 'subway_distance'] = np.nan
df.loc[df.sample(frac=0.03).index, 'year_built'] = np.nan

# 保存到CSV文件 - 这里修正了拼写错误
df.to_csv('data/chengdu_second_hand_housing_sample.csv', index=False, encoding='utf-8-sig')
print("模拟数据已生成并保存到 'data/chengdu_second_hand_housing_sample.csv'")