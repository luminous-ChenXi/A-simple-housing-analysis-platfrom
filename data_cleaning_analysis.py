# data_cleaning_analysis.py
import pandas as pd
import numpy as np


def load_and_clean_data(filepath):
    """
    加载并清洗数据
    """
    df = pd.read_csv(filepath)

    print("原始数据形状:", df.shape)
    print("\n原始数据前5行:")
    print(df.head())
    print("\n原始数据信息:")
    print(df.info())
    print("\n原始数据描述性统计:")
    print(df.describe())

    # 1. 处理缺失值
    # 对于数值型特征，用中位数填充
    numeric_cols = ['subway_distance', 'year_built']
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"已用中位数 {median_val} 填充 {col} 的缺失值")

    # 2. 处理异常值 (以单价为例，使用IQR方法)
    Q1 = df['price_per_sqm'].quantile(0.25)
    Q3 = df['price_per_sqm'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df['price_per_sqm'] < lower_bound) | (df['price_per_sqm'] > upper_bound)]
    print(f"\n检测到单价异常值 {len(outliers)} 个")
    # 通常可以选择移除或盖帽处理，这里选择移除
    df_cleaned = df[(df['price_per_sqm'] >= lower_bound) & (df['price_per_sqm'] <= upper_bound)].copy()
    print(f"移除异常值后数据形状: {df_cleaned.shape}")

    # 3. 从户型字符串中提取房间数、厅数、卫数
    df_cleaned[['rooms', 'halls', 'baths']] = df_cleaned['layout'].str.extract(r'(\d+)室(\d+)厅(\d+)卫')
    df_cleaned[['rooms', 'halls', 'baths']] = df_cleaned[['rooms', 'halls', 'baths']].astype(float)

    # 4. 从楼层字符串中提取当前楼层和总楼层
    df_cleaned[['current_floor', 'total_floors']] = df_cleaned['floor'].str.split('/', expand=True)
    df_cleaned[['current_floor', 'total_floors']] = df_cleaned[['current_floor', 'total_floors']].astype(float)
    # 计算楼层比率
    df_cleaned['floor_ratio'] = df_cleaned['current_floor'] / df_cleaned['total_floors']

    # 5. 计算房龄
    current_year = 2024
    df_cleaned['house_age'] = current_year - df_cleaned['year_built']

    # 6. 将分类变量转换为类别类型
    categorical_cols = ['district', 'decoration', 'orientation', 'has_elevator']
    for col in categorical_cols:
        df_cleaned[col] = df_cleaned[col].astype('category')

    print("\n清洗后数据信息:")
    print(df_cleaned.info())

    return df_cleaned


def perform_analysis(df):
    """
    执行数据分析
    """
    print("\n=== 描述性统计分析 ===")
    # 按区域分组分析
    district_stats = df.groupby('district')['price_per_sqm'].agg(['mean', 'median', 'count', 'std']).round(2)
    district_stats.columns = ['平均单价', '单价中位数', '房源数量', '单价标准差']
    print("各区域房价统计:")
    print(district_stats)

    print("\n全市房价描述:")
    print(df['price_per_sqm'].describe())

    print("\n=== 相关性分析 ===")
    # 选择数值型特征进行相关性分析
    numeric_features = ['price_per_sqm', 'area', 'house_age', 'subway_distance', 'rooms', 'halls', 'baths',
                        'floor_ratio']
    correlation_matrix = df[numeric_features].corr()
    print("相关系数矩阵:")
    print(correlation_matrix['price_per_sqm'].sort_values(ascending=False))

    return district_stats, correlation_matrix


if __name__ == "__main__":
    file_path = "data/chengdu_second_hand_housing_sample.csv"
    cleaned_df = load_and_clean_data(file_path)
    district_stats, corr_matrix = perform_analysis(cleaned_df)
    # 保存清洗后的数据
    cleaned_df.to_csv('data/chengdu_housing_cleaned.csv', index=False, encoding='utf-8-sig')
    print("\n清洗后的数据已保存到 'data/chengdu_housing_cleaned.csv'")