# Deep Agents 实战：Notebook 实验

正文解释概念，Notebook 用小实验观察机制，AgentSeek 模板提供完整应用。每份 Notebook 从第一格独立运行，不依赖另一章留下的内核状态。

## 实验索引

<!-- course-notebook-index:start -->
| 实验 | 学习证据 | 模型与服务 |
|---|---|---|
| [作者模板](_template/01-minimal-tool.ipynb) | 实际 echo 工具、调用与返回关联 | 默认脚本模型；可选真实模型 |
| [第 1 章：Agent Harness](ch01/01-agent-harness.ipynb) | echo 成功、消息循环、默认工具差异 | 默认脚本模型；可选真实模型 |
<!-- course-notebook-index:end -->

章节共建进度以 [#105](https://github.com/datawhalechina/deepagents-in-action/issues/105) 为准；目录元数据在 [catalog.json](catalog.json)。待整合的首波贡献：[第 5 章 #127](https://github.com/datawhalechina/deepagents-in-action/pull/127)、[第 6 章 #129](https://github.com/datawhalechina/deepagents-in-action/pull/129)。

## 安装与运行

本波使用 Python 3.12 和独立的 Python 子项目。先安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)，在仓库根目录运行模板确认基础环境：

```bash
uv sync --project notebooks --locked
uv run --project notebooks --locked python -m course_notebooks.run template
```

`uv.lock` 锁定实际依赖；基础版本是 deepagents 0.7.15、langchain 1.4.2、langgraph 1.2.11、langchain-openai 1.6.2。服务类实验另外安装：

```bash
uv sync --project notebooks --locked --extra server
uv run --project notebooks --locked --extra server python -m course_notebooks.run
```

执行器为每份实验创建临时工作目录，并直接使用项目 Python 创建专用内核；已有的用户 `python3` 内核不会改变执行环境。默认从第一格执行所有已登记实验，也可以在命令末尾指定一个或多个实验 ID，例如 `template`。

结果写入 `artifacts/notebooks/`：执行后的 `.ipynb`、可直接阅读的 HTML/Markdown 和 `report.json`。报告记录源码提交、单份实验源码指纹、依赖锁指纹、模式与状态。失败返回非零退出码，后续未执行项标为 `not_run`。导出链接指向对应源码提交；未提交的新文件需提交后重新导出。

在 VS Code/Jupyter 中逐格学习时，选择 `notebooks/.venv/bin/python`（Windows 为 `notebooks/.venv/Scripts/python.exe`）对应的内核。也可显式注册：

```bash
uv run --project notebooks --locked python -m ipykernel install --user --name deepagents-course --display-name "Deep Agents course"
```

## 脚本模型与真实模型

默认 `offline`：不读取 `.env` 里的模型配置，不向模型供应商发送请求。脚本模型按公开规则产生工具调用，框架、工具函数、状态变化仍真实执行。这个模式验证机制，不证明真实模型会正确选工具；服务类实验仍需要本机启动真实服务。

需要真实模型时，把 [`.env.example`](../.env.example) 复制为仓库根目录未提交的 `.env`，再明确选择 `live`：

```bash
uv run --project notebooks --locked python -m course_notebooks.run template --mode live
```

默认提供商使用 `SILICONFLOW_API_KEY`，可选 `SILICONFLOW_BASE_URL`、`MODEL_NAME`。其他 OpenAI 兼容提供商必须同时设置 `MODEL_API_KEY`、`MODEL_BASE_URL`、`MODEL_NAME`。模型必须支持工具调用；实际网络请求可能收费。复杂实验需要更可靠的工具调用能力，不能由入门实验的结果推断所有模型均适用。

交互式内核可在创建模型前设置 `os.environ["COURSE_MODE"] = "live"`；重跑时重新选择模式。仅仅存在 Key 或 `.env` 不会启用真实模型。明确选择 live 后缺配置、认证失败或调用失败都会报错，不自动退回脚本模型。LangSmith 追踪为可选项，本地 in-memory Agent Server 不要求 LangSmith Key。

## 验证与贡献

```bash
uv run --project notebooks --locked --extra server pytest notebooks/tests
uv run --project notebooks --locked --extra server python -m course_notebooks.run --check-only
uv run --project notebooks --locked --extra server python -m course_notebooks.run --write-back
```

`--write-back` 只将成功执行的本次输出写回源 Notebook；默认不会改写源文件。保存输出时同时记录模式，真实模型输出与无 Key 结果分别报告。贡献步骤和教学标准见 [CONTRIBUTING.md](CONTRIBUTING.md)。
