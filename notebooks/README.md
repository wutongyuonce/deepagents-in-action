# Notebook 索引

本目录收录《Deep Agents 实战》的配套 Notebook。每份 Notebook 聚焦一个可独立验证的主题，并可从第一格顺序执行。

| 章节 | Notebook | 主题 | 状态 |
|---|---|---|---|
| 第 5 章 | [`ch05/01-subagent-delegation.ipynb`](ch05/01-subagent-delegation.ipynb) | 子 Agent 委派与上下文隔离 | ✅ 已收录 |

## 运行环境

支持 Python 3.11+；本 Notebook 按 Python 3.12 和 `deepagents==0.7.15` 编写。其他主要依赖版本及操作系统说明见 Notebook 开头。在仓库根目录安装：

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install "deepagents==0.7.15" "langchain==1.4.2" "langgraph==1.2.11" "langchain-openai==1.6.2" python-dotenv ipykernel nbconvert
```

需要支持工具调用的模型 API。默认使用 SiliconFlow；也可在仓库根目录未提交的 `.env` 中设置 `DEEPSEEK_API_KEY`，使用 DeepSeek API（默认模型 `deepseek-flash`）。模型名可通过 `MODEL_NAME` 覆盖；其他 OpenAI 兼容服务可同时设置 `MODEL_API_KEY`、`MODEL_BASE_URL` 和 `MODEL_NAME`。不要提交真实密钥或含密钥的输出。

从仓库根目录运行：

```bash
jupyter nbconvert --to notebook --execute notebooks/ch05/01-subagent-delegation.ipynb --output-dir /tmp --ExecutePreprocessor.timeout=600
```

提交前请在干净环境中运行，并检查输出中没有密钥、Token、个人路径或过长日志。
