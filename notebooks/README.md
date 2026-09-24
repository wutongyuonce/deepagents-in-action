# Notebook 索引

本目录收录《Deep Agents 实战》各章的配套 Notebook。每个 Notebook 聚焦一个可以独立验证的主题，读者可以从第一格顺序执行、查看中间状态，并保留经过清理的运行结果。

## 目录结构约定

```
notebooks/
├── README.md                 # 本文件：索引、运行说明和完成状态
├── chXX/
│   └── NN-short-name.ipynb   # 两位序号 + 简短英文名
└── ...
```

- 一份 Notebook 只讲一个可独立验证的主题；内容较多的章节可拆成多个文件。
- 文件名使用两位序号和简短英文名称，例如 `01-agent-harness.ipynb`。

## 已完成 / 进行中

| 章节 | Notebook | 主题 | 状态 |
|---|---|---|---|
| 第 1 章 | [`ch01/01-agent-harness.ipynb`](ch01/01-agent-harness.ipynb) | Agent Harness 与最小运行结构 | ✅ 已收录 |
| 第 2 章 | — | 快速上手与自定义工具 | ⬜ 待认领 |
| 第 3 章 | — | 虚拟文件系统与各类存储后端 | ⬜ 待认领 |
| 第 5 章 | [`ch05/01-subagent-delegation.ipynb`](ch05/01-subagent-delegation.ipynb) | 子 Agent 委派与上下文隔离 | ✅ 已收录 |

## 环境与依赖

- 支持平台：macOS、Linux 与 WSL（Windows 原生未验证）
- Python 3.11+（本目录示例在 Python 3.12 下验证）
- 主要依赖：`deepagents>=0.7,<0.8`、`langchain`、`langgraph`、`langchain-openai`
- 作者与本地验证还需要：`ipykernel`、`nbconvert`

安装示例（推荐 `uv`）：

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install "deepagents>=0.7,<0.8" langchain langgraph langchain-openai python-dotenv ipykernel nbconvert
```

各 Notebook 开头都会列出它实际验证过的完整依赖版本。

## 环境变量与密钥

- 模型名请通过 `MODEL_NAME` 等环境变量配置，密钥从环境变量或本地 `.env` 读取。
- **禁止**把真实密钥、Token、个人路径写进 Notebook 或提交到仓库。`.env`、`.venv/` 已在 `.gitignore` 中。
- 课程默认使用硅基流动（SiliconFlow，兼容 OpenAI 接口）：`SILICONFLOW_API_KEY`，可选 `MODEL_NAME`、`SILICONFLOW_BASE_URL`。

仓库根目录提供了 `.env.example`，复制后填入自己的密钥即可：

```bash
cp .env.example .env
# 编辑 .env，把 SILICONFLOW_API_KEY 换成自己的 Key
```

## 运行方式

**方式一：VS Code（推荐）**

1. 安装两个扩展：**Python**（`ms-python.python`）与 **Jupyter**（`ms-toolsai.jupyter`）。
   打开 Notebook 时 VS Code 可能直接提示安装，点 Install 即可。
2. 打开仓库根目录作为工作区，确认已信任该文件夹。
3. 打开 `.ipynb`，点右上角选择内核（Select Kernel），指向本仓库虚拟环境里的解释器：
   - 一般会自动列出 `.venv`；
   - 若没有，选 **Enter interpreter path...**，填相对路径 `.venv/bin/python`（Windows 为 `.venv\Scripts\python.exe`）。
4. 从上到下依次运行，或点 **Run All**。

> 选内核前请确认 `.venv` 里已安装 `ipykernel`（见上文安装命令），否则可能找不到可用内核。

**方式二：命令行执行（用于干净环境验证）**

```bash
jupyter nbconvert \
  --to notebook \
  --execute notebooks/chXX/<文件名>.ipynb \
  --output-dir /tmp \
  --ExecutePreprocessor.timeout=600
```

Notebook 需要能在干净环境中从第一格运行到最后一格，不依赖上一次运行残留的变量、文件或内核状态。

## 贡献说明

认领与完成状态见长期共建 issue。提交前请：

1. 确认 Notebook 与课程正文使用的概念和 API 一致；
2. 在说明的依赖版本下从头到尾顺序执行成功；
3. 清理密钥、Token、个人路径和大段无关输出；
4. 在本文件中更新索引、依赖说明和完成状态。
