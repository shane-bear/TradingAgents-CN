# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 项目概览

TradingAgents-CN 是基于多智能体大语言模型的中文金融交易决策框架，专为中文用户优化，提供完整的A股/港股/美股分析能力。

## 🚀 开发命令

### 安装依赖
```bash
# 使用 pip (推荐)
pip install -e .

# 使用 uv
uv pip install -e .

# 安装百度千帆支持 (可选)
pip install -e .[qianfan]
```

### Docker 部署 (生产环境推荐)
```bash
# 一键构建启动
docker-compose up -d --build

# 分步构建
docker build -t tradingagents-cn:latest .
docker-compose up -d
```

### Web 应用启动
```bash
# 使用启动脚本 (推荐)
python start_web.py

# 直接启动 Streamlit
streamlit run web/app.py --server.port 8501
```

### 测试运行
```bash
# 运行单个测试文件
python tests/test_akshare_functionality.py

# 运行 CLI 测试
python -m tradingagents.cli.main --stock 601127 --date 2024-05-10
```

## 🏗️ 架构概览

### 核心模块结构
```
tradingagents/
├── agents/           # 智能体系统
│   ├── analysts/     # 分析师 (市场、新闻、基本面、社交媒体)
│   ├── managers/     # 管理角色 (研究、风险)
│   ├── researchers/  # 研究员 (多头、空头)
│   └── risk_mgmt/    # 风险辩论器
├── dataflows/        # 数据流管理
│   ├── cache_manager.py     # 缓存管理
│   ├── data_source_manager.py # 数据源管理
│   └── *utils.py           # 各数据源工具 (akshare, tushare, finnhub等)
├── graph/            # 图执行引擎
│   ├── trading_graph.py    # 主图类
│   ├── propagation.py      # 传播逻辑
│   └── reflection.py       # 反思机制
├── llm_adapters/     # LLM 适配器
│   ├── openai_compatible_base.py # 基础适配器
│   ├── dashscope_adapter.py      # 阿里通义千问
│   ├── google_openai_adapter.py  # Google AI
│   ├── deepseek_adapter.py       # 深度求索
│   └── baidu_qianfan_adapter.py  # 百度千帆 (新增)
└── utils/            # 工具类
    ├── logging_manager.py  # 日志管理
    └── config_manager.py    # 配置管理
```

### 关键配置文件
- `.env` - 环境变量配置 (从 `.env.example` 复制)
- `pyproject.toml` - 项目依赖配置 (主配置文件)
- `requirements.txt` - 遗留依赖文件 (已弃用)
- `default_config.py` - 默认运行时配置

## 🔧 开发工作流

### 1. 环境设置
```bash
# 复制环境配置
cp .env.example .env
# 编辑 .env 文件填入 API 密钥
```

### 2. 依赖管理
- 使用 `pyproject.toml` 管理主要依赖
- 可选依赖在 `[project.optional-dependencies]` 中定义
- 使用 `uv` 或 `pip` 进行安装

### 3. 测试策略
- 测试文件位于 `tests/` 目录
- 每个功能模块都有对应的测试脚本
- 测试覆盖数据源、LLM适配器、智能体等功能

## 🌐 API 集成

### 支持的 LLM 提供商
- OpenAI (原生支持)
- Google AI (Gemini 2.5/2.0)
- 阿里通义千问 (DashScope)
- 深度求索 (DeepSeek)
- 百度千帆 (ERNIE, 可选)

### 数据源集成
- **A股**: AKShare, Tushare, Baostock
- **港股**: EODHD, Finnhub
- **美股**: Yahoo Finance, Finnhub
- **新闻**: Google News, Reddit, Finnhub News

## 📊 监控与日志

### 日志系统
- 统一日志管理在 `utils/logging_manager.py`
- 支持分级日志和上下文信息
- Token 使用跟踪和成本计算

### 数据库
- MongoDB 用于用户管理和 Token 记录
- Redis 用于缓存和会话管理
- 配置在 `.env` 中设置

## 🐳 Docker 部署

### 服务组成
- **Web 应用**: Streamlit (端口 8501)
- **数据库**: MongoDB (端口 27017)
- **缓存**: Redis (端口 6379)
- **管理界面**: Mongo Express (端口 8081)

### 开发模式
```bash
# 开发环境启动
docker-compose -f docker-compose.yml up --build
```

## 🧪 测试策略

### 功能测试
- 数据源连通性测试
- LLM 适配器集成测试
- 智能体工作流测试
- 用户权限系统测试

### 性能测试
- 缓存性能测试
- 并发处理测试
- 内存使用监控

## 🔐 安全配置

- API 密钥通过环境变量管理
- 用户认证和权限控制
- 数据库连接加密
- 输入验证和清理

## 📈 性能优化

### 缓存策略
- 多级缓存系统 (内存、Redis、数据库)
- 自适应缓存过期策略
- 数据预处理和索引优化

### 并发处理
- 异步数据获取
- 批量请求处理
- 连接池管理

## 🔄 版本管理

- 版本号在 `VERSION` 文件中定义
- 遵循语义化版本控制
- Docker 镜像标签与版本号同步

## 📚 文档资源

- `README.md` - 项目主文档
- `QUICKSTART.md` - 快速开始指南
- `docs/` - 详细技术文档
- 学术论文和研究成果在 `docs/` 目录

## 🆘 故障排除

### 常见问题
1. **模块导入错误**: 确保已安装依赖 `pip install -e .`
2. **API 连接失败**: 检查 `.env` 文件中的密钥配置
3. **数据库连接问题**: 确认 MongoDB/Redis 服务运行状态

### 调试工具
- 丰富的测试脚本在 `tests/` 和 `scripts/` 目录
- 日志分析工具 `scripts/log_analyzer.py`
- Docker 调试脚本 `scripts/debug_docker.*`

## 🎯 开发重点

### 核心功能优先级
1. LLM 适配器兼容性和性能
2. 数据源稳定性和数据质量
3. 用户权限和安全管理
4. 缓存和性能优化
5. 文档和测试覆盖

### 扩展方向
- 新增国产大模型支持
- 更多数据源集成
- 高级分析功能
- 移动端适配
- 企业级部署方案