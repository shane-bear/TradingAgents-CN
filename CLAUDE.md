# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. High-level Code Architecture and Structure

This project, `TradingAgents-CN`, is a multi-agent large language model-based financial trading decision framework, optimized for Chinese users and supporting A-share/Hong Kong stock/US stock analysis.

### Core Technologies
- **Backend**: Python 3.10+, LangChain, Streamlit, MongoDB, Redis.
- **AI Models**: Integrates DeepSeek, Alibaba Cloud DashScope, Google AI (Gemini), OpenRouter (aggregates 60+ models), and OpenAI.
- **Data Sources**: Utilizes Tushare, AkShare, FinnHub, and Yahoo Finance for financial data.
- **Deployment**: Supports Docker, Docker Compose, and local deployment.

### Multi-Agent System
The framework employs a multi-agent collaborative architecture:
- **Analyst Team**: Specializes in market, fundamental, news, and social media analysis.
- **Research Team**: Consists of bullish and bearish researchers who conduct in-depth analysis and debate, leading to trading decisions.
- **Management**: Includes a Risk Manager and Research Supervisor for oversight and coordination.

### Data Flow and Persistence
- **Data Management**: Leverages MongoDB for persistent data storage (e.g., historical data, analysis results, user configurations) and Redis for high-speed caching of hot data and real-time prices.
- **Smart Degradation**: Implements a multi-layer data source degradation strategy: Redis Cache → MongoDB Storage → API Call → Local File Cache to ensure high availability and reduce API call costs.

### User Interfaces
- **Web Interface**: A responsive web application built with Streamlit, offering an intuitive stock analysis experience with real-time progress tracking, professional report generation, and multi-LLM model management.
- **CLI**: An interactive command-line interface for direct analysis and user management.

## 2. Commonly Used Commands

### Build and Installation
- **Install dependencies (local development)**: `pip install -e .`
- **Docker build and run**: `docker-compose up -d --build`
- **Docker run (if images exist)**: `docker-compose up -d`

### Running the Application
- **Start Web UI (local)**: `python start_web.py` or `streamlit run web/app.py`
- **Start Interactive CLI**: `python -m cli.main`

### Testing
- **Run all tests**: `pytest` (assuming pytest is installed and configured)
- **Test fundamentals analysis**: `python tests/test_fundamentals_analysis.py`
- **Test DeepSeek Token tracking**: `python tests/test_deepseek_token_tracking.py`

### Linting
- No explicit linting command was found in `pyproject.toml` or the provided documentation.

### Other Useful Commands
- **User Management (CLI)**:
    - List users: `python scripts/user_password_manager.py list`
    - Change user password: `python scripts/user_password_manager.py change-password <username>`
    - Create new user: `python scripts/user_password_manager.py create <username> --role <role>`
    - Delete user: `python scripts/user_password_manager.py delete <username>`
- **Data Directory Configuration (CLI)**:
    - Show current config: `python -m cli.main data-config --show`
    - Set custom directory: `python -m cli.main data-config --set /path/to/your/data`
    - Reset to default: `python -m cli.main data-config --reset`