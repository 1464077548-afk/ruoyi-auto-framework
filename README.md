# RuoYi Auto Framework

RuoYi自动化测试框架，包含API测试、UI测试和E2E测试

## 功能特性

- **API测试**：基于requests库的API自动化测试
- **UI测试**：基于Playwright的UI自动化测试
- **E2E测试**：端到端测试场景
- **数据驱动**：支持YAML和CSV数据文件
- **报告生成**：集成Allure报告
- **日志系统**：完善的日志记录
- **异常处理**：智能的异常捕获和处理

## 目录结构

```
ruoyi-auto-framework/
├── config/           # 配置文件
├── data/             # 测试数据
├── src/              # 源代码
│   ├── api/          # API测试相关
│   ├── core/         # 核心功能
│   ├── services/     # 业务服务
│   ├── tests/        # 测试用例
│   └── web/          # UI测试相关
├── logs/             # 日志文件
├── reports/          # 测试报告
├── screenshots/      # 截图
├── .gitignore        # Git忽略文件
├── pytest.ini        # pytest配置
├── requirements.txt  # 依赖管理
└── run_test.py       # 运行脚本
```

## 安装依赖

```bash
pip install -r requirements.txt
playwright install
```

## 运行测试

```bash
# 运行所有测试
python run_test.py

# 运行API测试
pytest src/tests/integration/api/

# 运行UI测试
pytest src/tests/integration/ui/

# 运行E2E测试
pytest src/tests/e2e/

# 生成Allure报告
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## 配置说明

- **config/ruoyi_config.yaml**：系统配置
- **config/test_env.yaml**：测试环境配置
- **data/**：测试数据文件

## 测试数据

- **data/yaml/**：YAML格式的测试数据
- **data/login_test_data.csv**：CSV格式的登录测试数据

## 报告查看

测试完成后，会在 `allure-results` 目录生成测试结果，使用Allure命令生成并查看报告：

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## 注意事项

1. 运行测试前确保RuoYi系统已启动
2. 确保配置文件中的base_url正确
3. 首次运行需要安装Playwright浏览器
4. 测试过程中会自动截图保存到screenshots目录

## 开发规范

- 测试用例遵循Pytest规范
- 代码风格保持一致
- 测试数据与测试逻辑分离
- 异常处理和日志记录完善

## 维护者

- 作者：AI Assistant
- 版本：1.0.0
- 日期：2026-03-13