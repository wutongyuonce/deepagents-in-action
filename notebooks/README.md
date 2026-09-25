# Notebook 索引

| 章节 | Notebook | 验证内容 |
|---|---|---|
| 第 6 章 | [`ch06/01-async-subagent-lifecycle.ipynb`](ch06/01-async-subagent-lifecycle.ipynb) | 本地 Agent Server、ASGI 异步子 Agent、五个工具及清理 |

在仓库根目录使用 Python 3.12 安装依赖：

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r notebooks/ch06/requirements.txt "langgraph-cli[inmem]" python-dotenv ipykernel nbconvert
```

第 6 章 Notebook、`langgraph.json` 和 `requirements.txt` 位于 `notebooks/ch06/`；服务图脚本位于 `notebooks/ch06/graphs/`。Notebook 会自己启动、检查并关闭本地 Agent Server。可复用第 1 章的 `SILICONFLOW_API_KEY`、`SILICONFLOW_BASE_URL` 和 `MODEL_NAME`；其他 OpenAI 兼容服务可同时设置 `MODEL_API_KEY`、`MODEL_BASE_URL`、`MODEL_NAME`。密钥可放在未提交的 `.env` 或进程环境中，不要提交密钥或包含密钥的输出。所选模型须支持工具调用。`LANGSMITH_API_KEY` 对本地 in-memory Agent Server 的运行并非必需；需要 LangSmith 追踪时再设置。

没有模型密钥时，Notebook 会使用脚本模型选择 supervisor 工具，仍实际调用同一套服务、ASGI 中间件与 SDK。此模式只能验证基础设施及工具生命周期，不能证明真实模型会正确选工具。真实模型模式会访问所配置的模型 API，可能产生调用费用；本地 Agent Server 不需要远程部署。

从仓库根目录执行：

```bash
jupyter nbconvert --to notebook --execute notebooks/ch06/01-async-subagent-lifecycle.ipynb --output-dir /tmp --ExecutePreprocessor.timeout=180
```

运行过程会创建三个子任务，分别完成、更新和取消。运行失败时 Notebook 会关闭本次创建的任务与服务，并在输出中报告失败；服务启动失败或超时会给出临时日志路径。
