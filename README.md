# MuscleKing - 智能健身助手

MuscleKing 是一个基于多智能体（Multi-Agent）架构的 AI 健身助手应用。通过 LangGraph 编排多个专业 Agent，结合知识图谱（Neo4j）、向量检索（Milvus）、Text2SQL 等技术，为用户提供个性化的训练计划、运动指导和健身知识问答服务。

## 项目架构

```
┌─────────────┐
│   FastAPI    │  API 层：POST /api/v1/chat
└──────┬───────┘
       │
┌──────▼───────┐
│  Service     │  服务层：会话管理、LLM 调用、知识库服务
└──────┬───────┘
       │
┌──────▼───────────────────────────────────────────────┐
│              LangGraph 多智能体引擎                     │
│                                                       │
│  ┌─────────┐    ┌────────────┐    ┌───────────────┐  │
│  │ Router  │───▶│ 通用问答    │───▶│ 直接 LLM 响应  │  │
│  │ 路由器   │───▶│ 知识库检索  │───▶│ Milvus + 重排  │  │
│  │         │───▶│ 知识图谱    │───▶│ Cypher/SQL    │  │
│  └─────────┘    └────────────┘    └───────────────┘  │
└───────────────────────────────────────────────────────┘
       │
┌──────▼───────┐
│  Persistence │  持久层：MySQL | Neo4j | Milvus
└──────────────┘
```

## 核心功能

- **智能路由**：LLM 意图识别，自动将用户问题分发到最合适的处理管线
- **知识图谱查询**：基于 Neo4j 构建健身知识图谱，支持 Text2Cypher 和预定义查询
- **知识库检索**：Milvus 向量数据库 + 交叉编码器重排序，精准匹配健身文档
- **Text2SQL**：自然语言转 SQL 查询，支持模式检索、SQL 生成与验证的完整工作流
- **LightRAG 集成**：轻量级 GraphRAG 方案，支持 local/global/hybrid 检索模式
- **会话管理**：MySQL 持久化聊天记录，支持多轮对话上下文

## 技术栈

| 类别 | 技术 |
|------|------|
| Web 框架 | FastAPI + Uvicorn |
| Agent 框架 | LangGraph + LangChain |
| LLM | OpenAI API (兼容接口) |
| 知识图谱 | Neo4j 5.27 |
| 向量数据库 | Milvus 2.3 |
| 关系数据库 | MySQL 8.0 |
| Embedding | Qwen3-Embedding-0.6B |
| Reranker | BAAI/bge-reranker-v2-m3 |
| GraphRAG | LightRAG |

## 项目结构

```
MuscleKing/
├── muscleking/
│   ├── main.py                          # FastAPI 应用入口
│   ├── config/
│   │   └── settings.py                  # Pydantic Settings 配置
│   ├── app/
│   │   ├── api/v1/
│   │   │   └── chat.py                  # 聊天 API 端点
│   │   ├── agents/                      # 多智能体工作流
│   │   │   ├── agent_state.py           # 状态类型定义
│   │   │   ├── lg_builder.py            # 主 LangGraph 构建器
│   │   │   ├── lg_prompts.py            # 系统提示词
│   │   │   ├── kb_workflow.py           # 知识库子工作流
│   │   │   ├── guardrails/              # 护栏节点（范围检查）
│   │   │   ├── planner/                 # 规划节点（任务分解）
│   │   │   ├── tool_selection/          # 工具选择节点
│   │   │   ├── cyper_tools/             # Text2Cypher 生成与执行
│   │   │   ├── predefined_cypher/       # 预定义 Cypher 查询模板
│   │   │   ├── customer/                # LightRAG 查询节点
│   │   │   ├── text2sql/                # Text2SQL 工作流
│   │   │   ├── multi_agent/             # 多工具编排
│   │   │   ├── final_answer/            # 最终答案汇总
│   │   │   ├── retrieve/                # Cypher 示例检索
│   │   │   └── models/                  # 状态/DTO 模型
│   │   ├── services/
│   │   │   ├── llm_client.py            # 异步 LLM 客户端
│   │   │   ├── service_chat.py          # 聊天会话管理
│   │   │   ├── knowledge_base_service.py# 知识库向量检索服务
│   │   │   └── vector_store.py          # Milvus 向量数据库封装
│   │   ├── persistence/
│   │   │   ├── core/
│   │   │   │   ├── database.py          # SQLAlchemy 数据库连接
│   │   │   │   └── neo4jconn.py         # Neo4j 连接
│   │   │   ├── crud/                    # 通用 CRUD 操作
│   │   │   └── db/models/               # SQLAlchemy ORM 模型
│   │   └── utils/
│   │       └── utils.py                 # Schema 提取工具
│   ├── scripts/
│   │   ├── build_exercise_kg.py         # 从本地 JSON 构建健身知识图谱
│   │   ├── wger_ingest.py               # 从 WGER API 导入数据
│   │   └── exercise_db_ingest.py        # 从 exerciseDB 导入数据
│   ├── docs/
│   │   ├── exercise_kg_schema.md        # 知识图谱 Schema 文档
│   │   └── wger_kg_schema.md            # WGER Schema 文档
│   └── kb_ingest/                       # 知识库数据导入服务（独立 FastAPI）
├── docker-compose.yml                   # MySQL 服务
├── init.sql                             # 数据库初始化脚本
├── requirements.txt                     # Python 依赖
└── pyproject.toml                       # 项目元数据
```

## 快速开始

### 环境要求

- Python 3.12
- Docker & Docker Compose
- Neo4j 5.x
- Milvus 2.3+

### 1. 克隆项目

```bash
git clone https://github.com/KAI3zZ/MuscleKing.git
cd MuscleKing
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env` 文件并填写配置：

```bash
cp .env.example .env
```

关键配置项：

```env
# LLM 配置
LLM_BASE_URL=https://your-llm-proxy/v1
LLM_API_KEY=your-api-key
LLM_MODEL=gpt-4o-mini

# MySQL
MYSQL_URL=mysql+pymysql://muscleking_user:musclepass@localhost:3306/muscleking_db

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=muscleking

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### 4. 启动 MySQL

```bash
docker-compose up -d mysql
```

### 5. 构建知识图谱（可选）

使用内置演示数据：

```bash
python -m muscleking.scripts.build_exercise_kg --demo
```

从外部数据源导入：

```bash
# 从 WGER API 导入
python -m muscleking.scripts.wger_ingest

# 从 exerciseDB 导入
python -m muscleking.scripts.exercise_db_ingest
```

### 6. 启动服务

```bash
# 开发模式
python -m muscleking.main

# 或使用 uvicorn
uvicorn muscleking.main:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后访问 `http://localhost:8000/docs` 查看 API 文档。

## API 使用

### 聊天接口

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "深蹲练哪些肌肉？",
    "session_id": "your-session-id"
  }'
```

### 知识库导入接口（独立服务）

```bash
# 启动知识库导入服务
python -m muscleking.kb_ingest.main

# 导入 Excel 文件
curl -X POST http://localhost:8001/api/ingest/excel \
  -F "file=@your_fitness_data.xlsx"
```

## 测试

```bash
# 运行全部测试
pytest

# 运行特定测试
pytest test_exercise_kg.py
pytest test_workflow_full.py
pytest test_workflow_nodes.py
```

## 工作流说明

系统采用 LangGraph 状态图编排多智能体工作流，核心流程如下：

1. **路由（Router）**：LLM 分析用户意图，分发到对应处理管线
2. **护栏（Guardrails）**：检查问题是否在健身领域范围内
3. **规划（Planner）**：将复杂问题分解为子任务
4. **工具选择（Tool Selection）**：为每个子任务选择最优工具：
   - **Cypher Query**：动态生成 Cypher 查询 Neo4j 知识图谱
   - **Predefined Cypher**：匹配预定义的高频查询模板
   - **LightRAG**：基于图结构的轻量级 RAG 检索
   - **Text2SQL**：自然语言转 SQL 查询
5. **汇总（Summarize）**：整合多工具返回的结果
6. **最终答案（Final Answer）**：生成自然语言回复

## 知识图谱 Schema

Neo4j 中包含以下核心节点类型：

| 节点 | 说明 |
|------|------|
| Exercise | 运动动作（深蹲、卧推、硬拉等） |
| Muscle | 肌肉群（股四头肌、胸大肌等） |
| Equipment | 器械（杠铃、哑铃等） |
| Difficulty | 难度等级 |
| TrainingGoal | 训练目标（增肌、减脂等） |
| ExerciseStep | 动作步骤 |
| InjuryRisk | 受伤风险提示 |
| Benefit | 训练收益 |

详细的 Schema 定义参见 [docs/exercise_kg_schema.md](muscleking/docs/exercise_kg_schema.md)。

## License

MIT
