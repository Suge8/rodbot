import json
import re
from pathlib import Path

from rodbot.config.schema import Config

_JSONC_TEMPLATE = """\
{
  // ═══════════════════════════════════════════════════════════
  // 🤖 Agent 配置
  // ═══════════════════════════════════════════════════════════
  "agents": {
    "defaults": {
      "workspace": "~/.rodbot/workspace",
      // 主模型：用于对话和工具调用
      "model": "anthropic/claude-opus-4-5",
      // 轻量模型（可选）：用于经验提取和记忆整合等后台任务，节省主模型开销
      // 推荐: "openrouter/google/gemini-flash-1.5" 或 "deepseek/deepseek-chat"
      "utilityModel": "",
      // 经验/轨迹压缩使用的模型："utility"(默认,用轻量模型) | "main"(用主模型) | "none"(零成本规则,不调LLM)
      "experienceModel": "utility",
      // 可切换的模型列表，运行时用 /model 命令切换
      "models": [],
      "maxTokens": 8192,
      "temperature": 0.7,
      // 单次对话最大工具调用轮数
      "maxToolIterations": 20,
      // 记忆窗口：保留最近多少条消息在上下文中
      "memoryWindow": 50
    }
  },

  // ═══════════════════════════════════════════════════════════
  // 🔑 LLM Providers — 填入你使用的 Provider 的 API Key
  // ═══════════════════════════════════════════════════════════
  "providers": {
    "openrouter": { "apiKey": "" },
    "anthropic": { "apiKey": "" },
    "openai": { "apiKey": "" },
    "deepseek": { "apiKey": "" },
    "gemini": { "apiKey": "" },
    "groq": { "apiKey": "" }
  },

  // ═══════════════════════════════════════════════════════════
  // 💬 聊天渠道 — 按需启用
  // ═══════════════════════════════════════════════════════════
  "channels": {
    "telegram": { "enabled": false, "token": "", "allowFrom": [] }
  },

  // ═══════════════════════════════════════════════════════════
  // 🔧 工具配置
  // ═══════════════════════════════════════════════════════════
  "tools": {
    "web": { "search": { "braveApiKey": "" } },
    "exec": { "timeout": 60 },
    // 向量嵌入（可选）：启用后记忆和经验支持语义搜索
    // model: OpenAI 兼容的 embedding 模型名
    // apiKey: 对应 Provider 的 API Key
    // baseUrl: 非 OpenAI 官方时需填自定义端点
    "embedding": { "model": "", "apiKey": "", "baseUrl": "" },
    "restrictToWorkspace": false,
    // MCP 服务器，格式兼容 Claude Desktop / Cursor
    "mcpServers": {}
  }
}
"""


def get_config_path() -> Path:
    base = Path.home() / ".rodbot"
    jsonc = base / "config.jsonc"
    if jsonc.exists():
        return jsonc
    return base / "config.json"


def get_data_dir() -> Path:
    from rodbot.utils.helpers import get_data_path

    return get_data_path()


def load_config(config_path: Path | None = None) -> Config:
    path = config_path or get_config_path()

    if path.exists():
        try:
            text = path.read_text(encoding="utf-8")
            text = _strip_jsonc_comments(text)
            data = json.loads(text)
            data = _migrate_config(data)
            return Config.model_validate(data)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Failed to load config from {path}: {e}")
            print("Using default configuration.")

    return Config()


def save_config(config: Config, config_path: Path | None = None) -> None:
    path = config_path or get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix != ".jsonc" and not path.exists():
        path = path.with_suffix(".jsonc")

    if path.suffix == ".jsonc" and not path.exists():
        path.write_text(_JSONC_TEMPLATE, encoding="utf-8")
    else:
        data = config.model_dump(by_alias=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def _strip_jsonc_comments(text: str) -> str:
    return re.sub(
        r'"(?:[^"\\]|\\.)*"|//[^\n]*|/\*[\s\S]*?\*/',
        lambda m: m.group() if m.group().startswith('"') else "",
        text,
    )


def _migrate_config(data: dict) -> dict:
    tools = data.get("tools", {})
    exec_cfg = tools.get("exec", {})
    if "restrictToWorkspace" in exec_cfg and "restrictToWorkspace" not in tools:
        tools["restrictToWorkspace"] = exec_cfg.pop("restrictToWorkspace")
    search = tools.get("web", {}).get("search", {})
    if "apiKey" in search and "braveApiKey" not in search:
        search["braveApiKey"] = search.pop("apiKey")
    return data
