# app.py
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
import json
import re
from datetime import datetime

# 加载清洗后的数据
df = pd.read_csv('data/chengdu_housing_cleaned.csv')

# 初始化Dash应用
app = dash.Dash(__name__)
server = app.server  # 用于部署

# 获取唯一值用于下拉菜单
districts = sorted(df['district'].unique())
decorations = sorted(df['decoration'].unique())

# 自定义CSS样式
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                background-attachment: fixed;
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
            }
            
            .main-container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                margin: 20px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                animation: fadeInUp 1s ease-out;
            }
            
            .header {
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                animation: slideInDown 1s ease-out;
            }
            
            .filter-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                align-items: start;
            }
            
            
            .slider-container {
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
                grid-column: 1 / -1;
            }
            
            .filter-label {
                font-weight: bold;
                font-size: 1.1em;
                margin-bottom: 10px;
                display: block;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            
            /* 响应式设计 */
            @media (max-width: 1000px) {
                .filter-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
            
            @media (max-width: 768px) {
                .filter-grid {
                    grid-template-columns: 1fr;
                }
            }
            
            .chart-panel {
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                animation: fadeInRight 1s ease-out 0.6s both;
            }
            
            .table-panel {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                animation: fadeInUp 1s ease-out 0.9s both;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: 1.2fr 1fr;
                gap: 30px;
                align-items: start;
            }
            
            @media (max-width: 1024px) {
                .stats-grid {
                    grid-template-columns: 1fr;
                }
            }
                margin-bottom: 20px;
            }
            
            # .stats-panel {
            #     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            #     padding: 20px;
            #     border-radius: 15px;
            #     color: white;
            #     width: 100%;
            #     box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            #     height: 500px;
            #     display: flex;
            #     flex-direction: column;
            # }

            .filter-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 10px;
                align-items: start;
                flex: 1;
            }

            .stats-panel {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                text-align: center;
                height: 500px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            }
            
            # .stats-item {
            #     background: rgba(255, 255, 255, 0.15);
            #     padding: 16px;
            #     border-radius: 10px;
            #     backdrop-filter: blur(10px);
            #     border: 1px solid rgba(255, 255, 255, 0.9);
            #     min-height: 50px;
            # }
            
            .slider-container {
                background: rgba(255, 255, 255, 0.1);
                padding: 10px;
                border-radius: 10px;
                margin-top: 5px;
                grid-column: 1 / -1;
            }
            
            .stats-content {
                display: grid;
                grid-template-columns: 1fr;
                gap: 12px;
                padding: 5px;
            }
            
            .stats-item {
                background: rgba(255, 255, 255, 0.2);
                padding: 12px;
                border-radius: 8px;
                backdrop-filter: blur(5px);
                border: 1px solid rgba(255, 255, 255, 0.3);
                min-height: 60px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            @media (max-width: 1200px) {
                .stats-grid {
                    grid-template-columns: 1fr;
                    gap: 20px;
                }
                
                .filter-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
            
            @media (max-width: 900px) {
                .filter-grid {
                    grid-template-columns: 1fr;
                }
                
                .stats-content {
                    grid-template-columns: repeat(2, 1fr);
                    gap: 10px;
                }
            }
            
            # @media (max-width: 600px) {
            #     .stats-content {
            #         grid-template-columns: 1fr;
            #     }
                
            #     .stats-panel, .stats-panel {
            #         padding: 15px;
            #         min-height: 200px;
            #     }
            # }
            
            .stats-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 25px;
                align-items: start;
            }
            
            @media (max-width: 1024px) {
                .stats-grid {
                    grid-template-columns: 1fr;
                }
            }
            
            /* 动画定义 */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInDown {
                from {
                    opacity: 0;
                    transform: translateY(-50px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-50px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes fadeInRight {
                from {
                    opacity: 0;
                    transform: translateX(50px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes pulse {
                0% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.05);
                }
                100% {
                    transform: scale(1);
                }
            }
            
            /* 悬停效果 */
            .stats-panel:hover, .stats-panel:hover {
                transform: translateY(-5px);
                transition: transform 0.3s ease;
            }
            
            /* 下拉菜单样式 */
            .Select-control {
                background: rgba(255, 255, 255, 0.9) !important;
                border-radius: 8px !important;
            }
            
            /* 滑块样式 */
            .rc-slider-track {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            }
            
            .rc-slider-handle {
                border: 2px solid #667eea !important;
                background: white !important;
            }
            
            /* AI助手样式 */
            .ai-assistant-panel {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
                height: 500px;
                display: flex;
                flex-direction: column;
            }
            
            .ai-chat-container {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px;
                height: 320px;
                overflow-y: auto;
                margin-bottom: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                flex: 1;
            }
            
            .chat-message {
                margin-bottom: 15px;
                padding: 12px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
            }
            
            .user-message {
                background: rgba(255, 255, 255, 0.9);
                color: #333;
                margin-left: auto;
                text-align: right;
                border-bottom-right-radius: 5px;
            }
            
            .ai-message {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                margin-right: auto;
                border-bottom-left-radius: 5px;
            }
            
            .ai-input-container {
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            .ai-input {
                flex: 1;
                padding: 12px 15px;
                border: none;
                border-radius: 25px;
                background: rgba(255, 255, 255, 0.9);
                color: #333;
                font-size: 14px;
                outline: none;
            }
            
            .ai-send-btn {
                background: white;
                color: #ff6b6b;
                border: none;
                border-radius: 50%;
                width: 45px;
                height: 45px;
                cursor: pointer;
                font-size: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
            }
            
            .ai-send-btn:hover {
                background: #ff6b6b;
                color: white;
                transform: scale(1.1);
            }
            
            .ai-suggestions {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 10px;
                margin-top: 15px;
            }
            
            .suggestion-btn {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 8px 12px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 12px;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .suggestion-btn:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# 应用布局
app.layout = html.Div(className='main-container', children=[
    html.Div(className='header', children=[
        html.H1("成都市二手房房价数据分析与可视化", style={'margin': '0', 'fontSize': '2.5em', 'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'}),
        html.P("探索成都各区域房价趋势与分布", style={'margin': '10px 0 0 0', 'fontSize': '1.2em', 'opacity': '0.9'})
    ]),

    html.Div([
        # 筛选控件、AI助手和统计信息并列布局
        html.Div(className='stats-grid', children=[
            # 左边 - 筛选面板
            html.Div(className='stats-panel', children=[
                html.Div(className='filter-grid', children=[
                    # 区域选择
                    html.Div(className='stats-item', children=[
                        html.Label("选择区域:", className='filter-label'),
                        dcc.Dropdown(
                            id='district-dropdown',
                            options=[{'label': i, 'value': i} for i in districts],
                            value=districts,
                            multi=True,
                            style={'color': '#333', 'backgroundColor': 'rgba(255,255,255,0.9)'}
                        )
                    ]),

                    # 装修情况选择
                    html.Div(className='stats-item', children=[
                        html.Label("选择装修情况:", className='filter-label'),
                        dcc.Dropdown(
                            id='decoration-dropdown',
                            options=[{'label': i, 'value': i} for i in decorations],
                            value=decorations,
                            multi=True,
                            style={'color': '#333', 'backgroundColor': 'rgba(255,255,255,0.9)'}
                        )
                    ]),

                    # 面积范围滑块
                    html.Div(className='slider-container', children=[
                        html.Label("面积范围 (平米):", className='filter-label'),
                        dcc.RangeSlider(
                            id='area-slider',
                            min=df['area'].min(),
                            max=df['area'].max(),
                            step=10,
                            value=[df['area'].min(), df['area'].max()],
                            marks={int(i): str(int(i)) for i in np.linspace(df['area'].min(), df['area'].max(), 5)},
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        )
                    ]),

                    # 单价范围滑块
                    html.Div(className='slider-container', children=[
                        html.Label("单价范围 (元/平米):", className='filter-label'),
                        dcc.RangeSlider(
                            id='price-slider',
                            min=df['price_per_sqm'].min(),
                            max=df['price_per_sqm'].max(),
                            step=1000,
                            value=[df['price_per_sqm'].min(), df['price_per_sqm'].max()],
                            marks={int(i): f"{int(i // 1000)}k" for i in
                                   np.linspace(df['price_per_sqm'].min(), df['price_per_sqm'].max(), 5)},
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        )
                    ])
                ])
            ]),

            # 中间 - AI助手面板
            html.Div(className='ai-assistant-panel', children=[
                html.H3("🤖 AI数据分析助手", style={'textAlign': 'center', 'marginBottom': '20px', 'fontSize': '1.8em'}),
                
                html.Div(className='ai-chat-container', id='ai-chat-messages', children=[
                    html.Div(className='chat-message ai-message', children=[
                        html.P("您好！我是您的数据分析助手。我可以帮您："),
                        html.Ul(children=[
                            html.Li("分析房价趋势和分布"),
                            html.Li("解释数据图表含义"),
                            html.Li("提供购房建议"),
                            html.Li("回答关于成都房价的问题")
                        ]),
                        html.P("请选择下面的快捷问题或直接输入您的问题：")
                    ])
                ]),
                
                html.Div(className='ai-input-container', children=[
                    dcc.Input(
                        id='ai-input',
                        type='text',
                        placeholder='请输入您的问题...',
                        className='ai-input',
                        n_submit=0
                    ),
                    html.Button('➤', id='ai-send-btn', className='ai-send-btn', n_clicks=0)
                ]),
                
                html.Div(className='ai-suggestions', children=[
                    html.Button('哪个区域房价最贵？', className='suggestion-btn', id='suggestion-1'),
                    html.Button('装修情况对价格影响大吗？', className='suggestion-btn', id='suggestion-2'),
                    html.Button('推荐性价比高的房源', className='suggestion-btn', id='suggestion-3'),
                    html.Button('分析当前筛选结果', className='suggestion-btn', id='suggestion-4')
                ])
            ]),

            # 右边 - 统计信息面板
            html.Div(className='stats-panel', children=[
                html.H4("实时统计", style={'margin': '0 0 15px 0', 'fontSize': '1.4em', 'textShadow': '1px 1px 2px rgba(0,0,0,0.3)'}),
                html.Div(className='stats-content', id='summary-stats')
            ])
        ]),

        # 图表区域
        html.Div([
            html.Div(className='chart-panel', children=[
                dcc.Graph(id='price-by-district', style={'height': '400px'})
            ]),
            
            html.Div(className='chart-panel', children=[
                dcc.Graph(id='scatter-plot', style={'height': '400px'})
            ]),
            
            html.Div(className='chart-panel', children=[
                dcc.Graph(id='price-distribution', style={'height': '400px'})
            ])
        ], style={'width': '100%', 'marginTop': '20px'}),
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px'}),

    # 数据表
    html.Div(className='table-panel', children=[
        html.H3("筛选后的房源数据", style={'textAlign': 'center', 'color': '#333', 'marginBottom': '20px'}),
        dash_table.DataTable(
            id='house-table',
            columns=[{"name": i, "id": i} for i in df.columns if
                     i not in ['floor_ratio', 'current_floor', 'total_floors']],
            page_size=10,
            style_table={'overflowX': 'auto', 'borderRadius': '10px'},
            style_cell={
                'height': 'auto',
                'minWidth': '80px', 'width': '120px', 'maxWidth': '180px',
                'whiteSpace': 'normal',
                'textAlign': 'center',
                'border': '1px solid #eee'
            },
            style_header={
                'backgroundColor': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_data={
                'backgroundColor': 'rgba(255, 255, 255, 0.9)',
                'color': '#333'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgba(102, 126, 234, 0.1)'
                }
            ]
        )
    ])
])

# 回调函数：更新图表和数据
@app.callback(
    [Output('price-by-district', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('price-distribution', 'figure'),
     Output('summary-stats', 'children'),
     Output('house-table', 'data')],
    [Input('district-dropdown', 'value'),
     Input('decoration-dropdown', 'value'),
     Input('area-slider', 'value'),
     Input('price-slider', 'value')]
)
def update_figures(selected_districts, selected_decorations, area_range, price_range):
    # 应用筛选条件
    filtered_df = df[
        (df['district'].isin(selected_districts)) &
        (df['decoration'].isin(selected_decorations)) &
        (df['area'] >= area_range[0]) & (df['area'] <= area_range[1]) &
        (df['price_per_sqm'] >= price_range[0]) & (df['price_per_sqm'] <= price_range[1])
        ]

    # 计算一些基本统计量
    avg_price = filtered_df['price_per_sqm'].mean()
    median_price = filtered_df['price_per_sqm'].median()
    total_houses = len(filtered_df)
    min_price = filtered_df['price_per_sqm'].min()
    max_price = filtered_df['price_per_sqm'].max()

    stats_text = html.Div(className='stats-content', children=[
        html.Div(className='stats-item', children=[
            html.H4("🏠 房源总数", style={'margin': '0', 'fontSize': '1.1em'}),
            html.P(f"{total_houses} 套", style={'margin': '5px 0', 'fontSize': '1.3em', 'fontWeight': 'bold'})
        ]),
        html.Div(className='stats-item', children=[
            html.H4("💰 平均单价", style={'margin': '0', 'fontSize': '1.1em'}),
            html.P(f"{avg_price:.2f} 元/平米", style={'margin': '5px 0', 'fontSize': '1.1em'})
        ]),
        html.Div(className='stats-item', children=[
            html.H4("📈 单价中位数", style={'margin': '0', 'fontSize': '1.1em'}),
            html.P(f"{median_price:.2f} 元/平米", style={'margin': '5px 0', 'fontSize': '1.1em'})
        ]),
        html.Div(className='stats-item', children=[
            html.H4("📊 价格范围", style={'margin': '0', 'fontSize': '1.1em'}),
            html.P(f"{min_price:.0f} - {max_price:.0f} 元/平米", style={'margin': '5px 0', 'fontSize': '1em'})
        ])
    ])

    # 更新各区域平均单价柱状图
    district_avg = filtered_df.groupby('district')['price_per_sqm'].mean().sort_values().reset_index()
    fig1 = px.bar(district_avg, x='price_per_sqm', y='district', orientation='h',
                  title='各区域平均单价',
                  labels={'price_per_sqm': '平均单价 (元/平米)', 'district': '区域'},
                  color='price_per_sqm',
                  color_continuous_scale='Viridis')
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

    # 更新散点图
    fig2 = px.scatter(filtered_df, x='area', y='price_per_sqm', color='district',
                      hover_data=['layout', 'decoration', 'year_built'],
                      title='面积与单价关系',
                      labels={'area': '面积 (平米)', 'price_per_sqm': '单价 (元/平米)', 'district': '区域'})
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

    # 更新价格分布图
    fig3 = px.histogram(filtered_df, x='price_per_sqm', nbins=30, marginal='box',
                        title='单价分布',
                        labels={'price_per_sqm': '单价 (元/平米)', 'count': '房源数量'},
                        color_discrete_sequence=['#667eea'])
    fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

    # 准备表格数据
    table_data = filtered_df.to_dict('records')

    return fig1, fig2, fig3, stats_text, table_data

# AI助手回调函数
@app.callback(
    Output('ai-chat-messages', 'children'),
    [Input('ai-send-btn', 'n_clicks'),
     Input('ai-input', 'n_submit'),
     Input('suggestion-1', 'n_clicks'),
     Input('suggestion-2', 'n_clicks'),
     Input('suggestion-3', 'n_clicks'),
     Input('suggestion-4', 'n_clicks')],
    [dash.dependencies.State('ai-input', 'value'),
     dash.dependencies.State('district-dropdown', 'value'),
     dash.dependencies.State('decoration-dropdown', 'value'),
     dash.dependencies.State('area-slider', 'value'),
     dash.dependencies.State('price-slider', 'value'),
     dash.dependencies.State('ai-chat-messages', 'children')]
)
def update_ai_chat(send_clicks, submit_clicks, sug1_clicks, sug2_clicks, sug3_clicks, sug4_clicks,
                   user_input, selected_districts, selected_decorations, area_range, price_range, current_messages):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_messages
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # 获取当前筛选后的数据
    filtered_df = df[
        (df['district'].isin(selected_districts)) &
        (df['decoration'].isin(selected_decorations)) &
        (df['area'] >= area_range[0]) & (df['area'] <= area_range[1]) &
        (df['price_per_sqm'] >= price_range[0]) & (df['price_per_sqm'] <= price_range[1])
    ]
    
    # 处理用户输入
    if trigger_id in ['ai-send-btn', 'ai-input'] and user_input:
        user_message = html.Div(className='chat-message user-message', children=[
            html.P(user_input)
        ])
        
        # 生成AI回复
        ai_response = generate_ai_response(user_input, filtered_df)
        ai_message = html.Div(className='chat-message ai-message', children=[
            html.P(ai_response)
        ])
        
        return current_messages + [user_message, ai_message]
    
    # 处理快捷问题
    elif trigger_id == 'suggestion-1':
        return current_messages + [generate_suggestion_response('哪个区域房价最贵？', filtered_df)]
    elif trigger_id == 'suggestion-2':
        return current_messages + [generate_suggestion_response('装修情况对价格影响大吗？', filtered_df)]
    elif trigger_id == 'suggestion-3':
        return current_messages + [generate_suggestion_response('推荐性价比高的房源', filtered_df)]
    elif trigger_id == 'suggestion-4':
        return current_messages + [generate_suggestion_response('分析当前筛选结果', filtered_df)]
    
    return current_messages

# AI回复生成函数
def generate_ai_response(user_input, filtered_df):
    # 简单的关键词匹配回复
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ['贵', '价格高', '最贵', 'expensive']):
        return analyze_expensive_districts(filtered_df)
    elif any(word in input_lower for word in ['便宜', '性价比', '划算', 'cheap']):
        return analyze_cheap_districts(filtered_df)
    elif any(word in input_lower for word in ['装修', 'decoration']):
        return analyze_decoration_impact(filtered_df)
    elif any(word in input_lower for word in ['推荐', '建议', 'recommend']):
        return generate_recommendations(filtered_df)
    elif any(word in input_lower for word in ['趋势', '分析', 'trend']):
        return analyze_trends(filtered_df)
    else:
        return "感谢您的提问！我可以帮您分析成都房价数据。请尝试问我关于房价趋势、区域比较、装修影响或推荐房源等问题。"

def generate_suggestion_response(question, filtered_df):
    if question == '哪个区域房价最贵？':
        return html.Div(className='chat-message ai-message', children=[
            html.P(analyze_expensive_districts(filtered_df))
        ])
    elif question == '装修情况对价格影响大吗？':
        return html.Div(className='chat-message ai-message', children=[
            html.P(analyze_decoration_impact(filtered_df))
        ])
    elif question == '推荐性价比高的房源':
        return html.Div(className='chat-message ai-message', children=[
            html.P(generate_recommendations(filtered_df))
        ])
    elif question == '分析当前筛选结果':
        return html.Div(className='chat-message ai-message', children=[
            html.P(analyze_current_selection(filtered_df))
        ])

# 具体分析函数
def analyze_expensive_districts(df):
    if len(df) == 0:
        return "当前筛选条件下没有房源数据。"
    
    district_avg = df.groupby('district')['price_per_sqm'].mean().sort_values(ascending=False)
    top_district = district_avg.index[0]
    top_price = district_avg.iloc[0]
    
    return f"根据当前数据，{top_district}区域的房价最高，平均单价为{top_price:.2f}元/平米。前五名区域为：{', '.join([f'{d}({p:.0f}元/平米)' for d, p in list(district_avg.head().items())])}"

def analyze_cheap_districts(df):
    if len(df) == 0:
        return "当前筛选条件下没有房源数据。"
    
    district_avg = df.groupby('district')['price_per_sqm'].mean().sort_values()
    cheap_district = district_avg.index[0]
    cheap_price = district_avg.iloc[0]
    
    return f"根据当前数据，{cheap_district}区域的房价相对较低，平均单价为{cheap_price:.2f}元/平米。性价比高的区域包括：{', '.join([f'{d}({p:.0f}元/平米)' for d, p in list(district_avg.head().items())])}"

def analyze_decoration_impact(df):
    if len(df) == 0:
        return "当前筛选条件下没有房源数据。"
    
    decoration_avg = df.groupby('decoration')['price_per_sqm'].mean().sort_values(ascending=False)
    impact_text = "装修情况对房价确实有显著影响：\n"
    for deco, price in decoration_avg.items():
        impact_text += f"• {deco}: {price:.2f}元/平米\n"
    
    return impact_text + "\n精装修的房源通常价格较高，而简装修或毛坯房价格相对较低。"

def generate_recommendations(df):
    if len(df) == 0:
        return "当前筛选条件下没有房源数据。"
    
    # 计算性价比（单价/面积）
    df['value_ratio'] = df['area'] / df['price_per_sqm']
    recommendations = df.nlargest(3, 'value_ratio')
    
    rec_text = "根据性价比推荐以下房源：\n"
    for _, row in recommendations.iterrows():
        rec_text += f"• {row['district']}区 {row['layout']} {row['area']}平米，单价{row['price_per_sqm']:.0f}元/平米\n"
    
    return rec_text

def analyze_trends(df):
    if len(df) == 0:
        return "当前筛选条件下没有房源数据。"
    
    avg_price = df['price_per_sqm'].mean()
    median_price = df['price_per_sqm'].median()
    price_range = f"{df['price_per_sqm'].min():.0f}-{df['price_per_sqm'].max():.0f}"
    
    return f"当前筛选条件下的房价分析：\n• 平均单价: {avg_price:.2f}元/平米\n• 单价中位数: {median_price:.2f}元/平米\n• 价格范围: {price_range}元/平米\n• 房源数量: {len(df)}套"

def analyze_current_selection(df):
    if len(df) == 0:
        return "当前筛选条件下没有房源数据，请调整筛选条件。"
    
    return analyze_trends(df) + "\n\n" + generate_recommendations(df)

if __name__ == '__main__':
    app.run(debug=True)