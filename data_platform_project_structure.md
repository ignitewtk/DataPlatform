# 企业级数据平台项目结构说明文档

## 📁 项目总览

本项目用于构建并维护企业级数据平台，覆盖 ETL 数据处理、自动化调度、云服务集成、基础设施管理、数据埋点、监控告警及可视化分析等全链路能力。

---

## 📂 项目目录结构

```
data_platform_project/
├── README.md                        # 项目总览说明
├── .gitignore                       # Git 忽略文件
├── requirements.txt                # Python 项目依赖
├── environments/                   # 环境配置（dev/test/prod）
│   ├── dev/
│   └── prod/
├── infrastructure/                 # 基础设施代码（Terraform）
│   ├── terraform/
│   │   ├── modules/
│   │   └── main.tf, variables.tf
│   └── scripts/
├── dags/                           # Airflow DAG 工作流调度
├── etl_jobs/                       # ETL 脚本目录
│   ├── ingestion/
│   ├── processing/
│   ├── reporting/
│   └── utils/
├── notebooks/                      # Databricks 分析笔记本
├── functions/                      # Azure Functions 脚本
├── configs/                        # 配置文件目录
├── monitoring/                     # 监控与告警配置
├── tests/                          # 自动化测试脚本
├── ci_cd/                          # CI/CD 脚本与部署配置
└── docs/                           # 项目文档（可选）
```

---

## 📌 各目录功能说明

### `environments/`
- 存放 dev/prod 环境相关变量与配置，适配多环境部署。
- 示例：Airflow 变量、Terraform tfvars 配置。

### `infrastructure/`
- 使用 Terraform 编写的基础设施代码。
- 支持模块化：storage, databricks, kafka, keyvault, app service 等。
- 推荐目录结构：modules/、env-specific 文件夹、outputs.tf。

### `dags/`
- 存放 Airflow DAG 定时任务。
- 示例 DAG: daily_etl_pipeline, kafka_ingestion_dag。

### `etl_jobs/`
- 编写 ETL 数据处理脚本（PySpark 为主）。
- ingestion: 数据埋点采集
- processing: 清洗、转换、特征构建等
- reporting: 聚合分析与指标构建
- utils: 工具函数封装

### `notebooks/`
- Databricks 数据探索分析笔记本。
- 建议使用 `.dbc` 或 `.ipynb` 格式管理。

### `functions/`
- Serverless 函数，如告警推送等功能使用 Azure Functions 实现。

### `configs/`
- 配置文件统一管理，可用 yaml/json 格式。
- 示例：pipeline_config.yaml, kafka_config.yaml。

### `monitoring/`
- Grafana Dashboard 配置文件、Airflow 告警模板等。
- 支持日志聚合与任务状态监控。

### `tests/`
- 包含单元测试、数据质量测试（建议集成 Great Expectations）。

### `ci_cd/`
- CI/CD 自动化部署脚本。
- 示例：GitHub Actions 中 airflow_deploy.yml、terraform_apply.yml。

### `docs/`
- 架构图、贡献指南、开发规范文档等（可选但推荐）。

         ┌───────────────┐
         │  Data Source  │ ← 模拟用户行为日志 (CSV/API)
         └──────┬────────┘
                ↓
        ┌────────────┐
        │   Kafka    │ ← 流式数据入口（日志/事件）
        └────┬───────┘
             ↓ (消息队列)
       ┌──────────────┐
       │  Airflow DAG │ ← 定时监听数据/调度ETL任务
       └────┬─────────┘
            ↓ Trigger scripts
        ┌───────────────────────┐
        │  ETL 脚本 / Notebooks │ ← PySpark/SQL 清洗处理
        └────┬────────────┬─────┘
            ↓            ↓
        ┌─────────┐   ┌─────────────┐
        │ Raw/    │   │ Processed   │ ← Parquet/Delta/SQLite 表
        │ Staging │   └─────────────┘
        └─────────┘
            ↓
        ┌────────────────────┐
        │  Power BI / Superset│ ← 可视化报表连接数据仓库
        └────────────────────┘

        （可选） ↓
            Azure Function ← 处理某些触发型任务（如报警、通知）




---

## 🧠 最佳实践建议

- 使用 `.env` 或 Azure Key Vault 统一管理变量。
- 引入 Great Expectations 做数据质量校验。
- 加入 Docker 容器模拟本地环境。
- 日志结构化，便于追踪调试。
- 编写每个模块 README.md，提高协作效率。
- 构建数据血缘图与数据目录（Amundsen/DataHub）。


---

## 📅 文档更新记录
- 初始版本：2025-03-18
