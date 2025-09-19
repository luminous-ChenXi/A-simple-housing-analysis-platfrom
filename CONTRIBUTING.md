# 贡献指南

感谢您有兴趣为成都二手房房价数据分析项目做出贡献！

## 如何贡献

### 报告问题

如果您发现任何问题或有改进建议，请：
1. 在GitHub Issues中搜索是否已有相关报告
2. 如果没有，请创建一个新的Issue
3. 提供详细的问题描述、复现步骤和预期行为

### 提交代码

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

### 开发环境设置

1. 克隆项目
```bash
git clone https://github.com/your-username/chengdu-housing-analysis.git
cd chengdu-housing-analysis
```

2. 创建虚拟环境
```bash
python -m venv .venv
```

3. 激活虚拟环境
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

4. 安装依赖
```bash
pip install -r requirements.txt
```

5. 运行应用
```bash
python app.py
```

## 代码规范

### Python代码风格
- 遵循PEP 8规范
- 使用有意义的变量名
- 添加适当的注释

### 提交信息规范
- 使用英文撰写提交信息
- 遵循Conventional Commits规范
- 示例：
  - `feat: 添加新的图表类型`
  - `fix: 修复数据筛选bug`
  - `docs: 更新README文档`

### 测试要求
- 为新功能添加相应的测试
- 确保所有测试通过
- 维护测试覆盖率

## 项目结构

```
chengdu-housing-analysis/
├── app.py                 # 主应用文件
├── data_cleaning_analysis.py  # 数据清洗和分析
├── visualization.py       # 可视化函数
├── requirements.txt       # 依赖包
├── README.md             # 项目说明
├── LICENSE               # 许可证
├── CONTRIBUTING.md       # 贡献指南
├── .gitignore           # Git忽略文件
├── data/               # 数据文件目录
└── plots/              # 生成的图表文件
```

## 功能开发指南

### 添加新的图表类型
1. 在 `visualization.py` 中添加新的图表函数
2. 在 `app.py` 中添加相应的回调函数
3. 更新布局以包含新图表

### 扩展AI助手功能
1. 在 `app.py` 中的AI回调函数中添加新的处理逻辑
2. 更新快捷问题按钮（如果需要）
3. 测试自然语言理解功能

### 数据预处理
1. 在 `data_cleaning_analysis.py` 中添加新的数据处理函数
2. 确保数据质量检查
3. 添加相应的测试用例

## 代码审查流程

1. 所有Pull Request都需要至少一名维护者审查
2. 确保代码符合项目规范
3. 通过所有测试
4. 更新相关文档

## 沟通渠道

- GitHub Issues: 用于问题跟踪和功能请求
- Pull Requests: 用于代码贡献和讨论
- 项目Wiki: 用于详细文档和教程

## 行为准则

请遵守项目的行为准则，保持友好和尊重的沟通环境。

感谢您的贡献！🎉