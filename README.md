<div align="center">

<br>

# 🤘 rodbot

### **Ride or Die** — 你的 AI，永远记得你，永远站你这边。

<br>

[![PyPI](https://img.shields.io/pypi/v/rodbot-ai?style=flat-square&color=00d4ff)](https://pypi.org/project/rodbot-ai/)
[![Downloads](https://static.pepy.tech/badge/rodbot-ai?style=flat-square)](https://pepy.tech/project/rodbot-ai)
![Python](https://img.shields.io/badge/python-≥3.11-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/MnCvHqpUGB)

**~4,100 行核心代码** · 记忆会留下 · 经验会积累 · 智能会进化

[快速开始](#-快速开始) · [为什么选 rodbot？](#为什么选-rodbot) · [架构](#-架构) · [English](#-english-documentation)

</div>

<br>

## 名字的含义

**rod** = **R**ide **o**r **D**ie — 生死之交。

不是一个你对着说话的聊天机器人，而是一个 **记得你在乎什么、学会什么对你有用、不会犯同样错误** 的伙伴。用得越久，它越懂你。

<p align="center"><img src="docs/features.svg" width="800" alt="核心特性"></p>

## 为什么选 rodbot？

大多数 AI 助手都有"失忆症"——每次对话从零开始，反复犯同样的错，忘了你的偏好，永远不会进步。

rodbot 不一样。它 **记得**、**反思**、**进化**。

### 🧠 记忆系统

基于 **LanceDB** 的持久化记忆，**向量搜索 + 关键词降级**——有没有 embedding 模型都能用。

你的 agent 会记住你的偏好、你的项目、你的习惯。自动整合旧上下文，保留重要的，主动清理过时的。跨会话，跨重启，永远在线。

### 📚 经验学习（ExperienceLoop）

受微软 [RE-TRAC](https://arxiv.org/abs/2602.02486) 启发，rodbot 实现了一个 **闭环经验引擎**：

- 每次任务完成后 → 自动提取教训、策略和失败模式
- 遇到类似任务时 → 检索相关经验注入到 prompt 中
- **置信度校准** — 追踪每条经验的成功率，自动调整质量分
- **冲突检测** — 发现矛盾的经验时标记提醒
- **负面学习** — 过去的失败变成警告，不再重蹈覆辙
- **主动遗忘** — 过期和低质量的经验自动清理

别的 agent 重复犯错。**rodbot 从错误中学习。**

### 🔄 深度思考 + 自我纠错

- **Thinking Protocol** — System Prompt 内置深度推理，零额外 API 调用，回答质量显著提升
- **Retry/Reflection** — 自动检测工具错误，连续 3 次失败后升级为深度反思策略
- **Tool Strategy** — 根据实际可用性动态启停工具提示，防止幻觉调用

### ⚡ 极致轻量

**~4,100 行核心代码。** 运行 `bash core_agent_lines.sh` 自行验证。

启动快、占用低、代码清晰易读。基于 [nanobot](https://github.com/HKUDS/nanobot) 构建，完全兼容上游所有功能。

## 🆚 对比

rodbot 占据最佳位置：**OpenClaw 的野心，nanobot 的简洁，以及两者都没有的智能。**

| | OpenClaw | nanobot | **rodbot** |
|---|---|---|---|
| 语言 | TypeScript | Python | **Python** |
| 核心代码 | 430,000+ 行 | ~3,800 行 | **~4,100 行** |
| 记忆 | 仅会话内 | 文件系统 | **LanceDB 向量+关键词** |
| 经验学习 | ❌ | ❌ | **ExperienceLoop** |
| 自我反思 | ❌ | ❌ | **Thinking Protocol + Retry** |
| Open Issues | 8,400+ | — | **稳定可控** |
| 上手时间 | 复杂向导 | 2 分钟 | **2 分钟** |

> OpenClaw 有庞大的社区——但 430K 行 TypeScript 意味着深度依赖树、复杂的调试和 8,400+ 个未关闭 issue。nanobot 证明了只需 ~4,000 行就够。**rodbot 在此基础上加了大脑**——记忆、经验和自我纠错——只多了 300 行。

<p align="center"><img src="docs/architecture.svg" width="800" alt="系统架构"></p>

## 🚀 快速开始

```bash
pip install rodbot-ai
rodbot onboard
```

在 `~/.rodbot/config.json` 中设置 API Key：

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  }
}
```

开始对话：

```bash
rodbot agent
```

**就这样。2 分钟，你的 AI 助手就位。**

可选：配置 **Utility Model** 处理后台任务（经验提取、记忆整合），节省成本：

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-sonnet-4-20250514",
      "utilityModel": "openrouter/google/gemini-flash-1.5"
    }
  }
}
```

## 💬 9 大平台

一个配置，一条命令：`rodbot gateway`

| 平台 | 准备 |
|------|------|
| **Telegram** | @BotFather 获取 Token |
| **Discord** | Bot Token + Message Content Intent |
| **WhatsApp** | 扫描二维码 |
| **飞书** | App ID + App Secret |
| **Slack** | Bot Token + App-Level Token |
| **Email** | IMAP/SMTP 凭证 |
| **QQ** | App ID + App Secret |
| **钉钉** | App Key + App Secret |
| **Mochat** | Claw Token（支持自动配置） |

## 🤖 16+ LLM Provider

OpenRouter · Anthropic · OpenAI · DeepSeek · Gemini · Groq · MiniMax · SiliconFlow · VolcEngine · DashScope · Moonshot · Zhipu · AIHubMix · vLLM · OpenAI Codex · GitHub Copilot · 自定义端点

新增 Provider？**2 步，~10 行代码。**

## 🔌 MCP 支持

Model Context Protocol，接入任何工具生态。配置 **兼容 Claude Desktop 和 Cursor**：

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
      }
    }
  }
}
```

## 🐳 Docker

```bash
docker compose run --rm rodbot-cli onboard
vim ~/.rodbot/config.json
docker compose up -d rodbot-gateway
```

## 🖥️ CLI

| 命令 | 说明 |
|------|------|
| `rodbot onboard` | 初始化 |
| `rodbot agent` | 交互对话 |
| `rodbot agent -m "..."` | 单条消息 |
| `rodbot gateway` | 启动所有平台 |
| `rodbot status` | 查看状态 |
| `rodbot cron list` | 定时任务 |

## 📁 项目结构

```
rodbot/
├── agent/          # 核心 Agent 逻辑
│   ├── loop.py     # Agent 循环（思考 + 重试 + 经验）
│   ├── context.py  # Prompt 构建 + 经验注入
│   ├── memory.py   # LanceDB 持久记忆
│   ├── subagent.py # 后台任务执行
│   └── tools/      # 内置工具（Shell, 文件, Web, MCP）
├── skills/         # GitHub, 天气, Cron, Tmux
├── channels/       # 9 大平台接入
├── providers/      # 16+ LLM Provider
├── bus/            # 异步消息路由
├── cron/           # 定时任务
└── cli/            # 命令行
```

## 🤝 贡献

欢迎 PR。代码库刻意保持精简可读。

- [ ] 多模态 — 图片、语音、视频
- [x] ~~长期记忆~~ — LanceDB
- [x] ~~更好的推理~~ — Thinking Protocol + Retry/Reflection
- [x] ~~自我进化~~ — ExperienceLoop
- [ ] 更多集成 — 日历等

<br>

---

<br>

<details open>
<summary><h2>🇺🇸 English Documentation</h2></summary>

### What is rodbot?

**rod** = **R**ide **o**r **D**ie — your partner that remembers what you care about, learns what works, and never makes the same mistake twice.

**~4,100 lines of core code**, with built-in persistent memory, experience learning, and self-reflection. Built on [nanobot](https://github.com/HKUDS/nanobot).

### Why rodbot?

**Memory** — LanceDB-powered persistent memory with vector + keyword search. Remembers across sessions, consolidates automatically, forgets stale knowledge.

**Experience Learning** — Closed-loop experience engine inspired by Microsoft RE-TRAC. Auto-extracts lessons after tasks, injects relevant experience before similar tasks. Confidence calibration, conflict detection, negative learning, active forgetting.

**Thinking + Self-Correction** — Deep reasoning via Thinking Protocol (zero latency cost), auto-retry with reflection escalation on tool errors.

**Lightweight** — ~4,100 lines. 99% smaller than OpenClaw (430K+ lines). 2-minute setup. Fully compatible with nanobot.

### How rodbot Compares

| | OpenClaw | nanobot | **rodbot** |
|---|---|---|---|
| Language | TypeScript | Python | **Python** |
| Core code | 430,000+ lines | ~3,800 lines | **~4,100 lines** |
| Memory | Session-only | File-based | **LanceDB (vector + keyword)** |
| Experience learning | ❌ | ❌ | **ExperienceLoop** |
| Self-reflection | ❌ | ❌ | **Thinking Protocol + Retry** |
| Open issues | 8,400+ | — | **Stable** |
| Setup time | Complex wizard | 2 min | **2 min** |

### Quick Start

```bash
pip install rodbot-ai
rodbot onboard
# Set API key in ~/.rodbot/config.json
rodbot agent
```

**9 Chat Platforms** — Telegram, Discord, WhatsApp, Feishu, Slack, Email, QQ, DingTalk, Mochat

**16+ LLM Providers** — OpenRouter, Anthropic, OpenAI, DeepSeek, Gemini, Groq, and more. Adding a new provider takes 2 steps.

**MCP Support** — Model Context Protocol, compatible with Claude Desktop and Cursor configs.

**Docker** — `docker compose up -d rodbot-gateway`

</details>

<br>

<div align="center">

### Star History

<a href="https://star-history.com/#Suge8/rodbot&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Suge8/rodbot&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Suge8/rodbot&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Suge8/rodbot&type=Date" />
  </picture>
</a>

<br><br>

<sub>Ride or Die. 🤘</sub>

</div>
