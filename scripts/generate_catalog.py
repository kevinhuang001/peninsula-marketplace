import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "pds"
LOGOS = ROOT / "scripts" / "logos"
OUT.mkdir(parents=True, exist_ok=True)

# Logos are monochrome path/shape SVGs with a 24x24 viewBox. Peninsula renders them with
# resvg, which does not rasterize `<text>`, so every icon must be drawn with paths/shapes.

def _logo_markup(name):
    text = (LOGOS / f"{name}.svg").read_text()
    start = text.index(">", text.index("<svg")) + 1
    inner = text[start:text.rindex("</svg>")]
    return re.sub(r"<title>.*?</title>", "", inner, flags=re.S).strip()


def icon(logo, bg, fg="#ffffff"):
    attributes = f'fill="{fg}" fill-rule="evenodd"'
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
        f'<rect width="64" height="64" rx="19" fill="{bg}"/>'
        f'<g transform="translate(14 14) scale(1.5)" {attributes}>{_logo_markup(logo)}</g>'
        "</svg>"
    )
    return {"mime": "image/svg+xml", "base64": base64.b64encode(svg.encode()).decode()}


def threshold(label, default):
    return {"type": "number", "label": label, "default": default, "required": True, "min": 0}


def api_key(label):
    return {"type": "string", "label": label, "required": True}


def source(id, name, description, logo, color, method, url, path, *, headers=None, query=None,
           inputs=None, multiply=1, offset=0, decimals=0, suffix="", alert=None):
    d = {
        "schema": "peninsula.datasource/v1", "id": id, "name": name,
        "description": description, "icon": icon(logo, color),
        "inputs": inputs or {},
        "request": {"method": method, "url": url, "headers": headers or {}, "query": query or {}, "timeout_ms": 10000},
        "value": {"path": path, "type": "number", "multiply": multiply, "divide": 1,
                  "offset": offset, "decimals": decimals, "separator": decimals == 0,
                  "prefix": "", "suffix": suffix}
    }
    if isinstance(alert, dict):
        d["alert"] = alert
    elif alert:
        d["alert"] = {"operator": "lt", "threshold": "${input.alert_threshold}",
                      "title": f"{name}偏低", "message": "剩余 ${value}，已低于提醒阈值。"}
    return d


ai = []
for period, title, color in [
    ("rolling", "滚动周期", "#0B766F"), ("weekly", "每周", "#216A70"), ("monthly", "每月", "#365B75")
]:
    ai.append(source(
        f"opencode-go-{period}-remaining", f"OpenCode Go {title}剩余",
        "显示 OpenCode Go 套餐的剩余百分比，需填写套餐 API Key。",
        "opencode", color, "GET", "https://opencode.ai/zen/go/v1/usage",
        f"$.usage.{period}.percent", headers={"Authorization": "Bearer ${input.api_key}", "Accept": "application/json"},
        inputs={"api_key": api_key("OpenCode Go 套餐 API Key"),
                "alert_threshold": threshold("低额度提醒阈值（%）", 15)},
        multiply=-1, offset=100, suffix="%", alert=True))

ai.append(source(
    "deepseek-cny-balance", "DeepSeek 人民币余额",
    "显示 DeepSeek 账户的人民币余额，需填写 API Key。",
    "deepseek", "#3469B2", "GET", "https://api.deepseek.com/user/balance",
    "$.balance_infos[?(@.currency=='CNY')].total_balance",
    headers={"Authorization": "Bearer ${input.api_key}", "Accept": "application/json"},
    inputs={"api_key": api_key("DeepSeek API Key"),
            "alert_threshold": threshold("低余额提醒阈值（元）", 10)},
    decimals=2, suffix=" 元", alert=True))

ai.append(source(
    "glm-cn-coding-remaining", "GLM Coding Plan 剩余",
    "显示中国区 Coding Plan 剩余百分比，需填写中国区套餐 Key。",
    "zhipu", "#6153AF", "GET", "https://open.bigmodel.cn/api/monitor/usage/quota/limit",
    "$.data.limits[?(@.type=='TOKENS_LIMIT')].percentage",
    headers={"Authorization": "${input.api_key}", "Accept": "application/json"},
    inputs={"api_key": api_key("GLM 中国区 Coding Plan Key"),
            "alert_threshold": threshold("低额度提醒阈值（%）", 15)},
    multiply=-1, offset=100, suffix="%", alert=True))

ai.append(source(
    "minimax-cn-current-remaining", "MiniMax 当前周期剩余",
    "显示中国区 Coding Plan 当前周期剩余百分比，需填写中国区套餐 Key。",
    "minimax", "#D86B48", "GET", "https://api.minimax.cn/v1/token_plan/remains",
    "$.model_remains[?(@.model_name=='general')].current_interval_remaining_percent",
    headers={"Authorization": "Bearer ${input.api_key}", "Accept": "application/json"},
    inputs={"api_key": api_key("MiniMax 中国区 Coding Plan Key"),
            "alert_threshold": threshold("低额度提醒阈值（%）", 15)},
    suffix="%", alert=True))

def github_source():
    # One imported source can read several independent public REST URLs.
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Peninsula-Marketplace",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    return {
        "schema": "peninsula.datasource/v2",
        "id": "github-repository",
        "name": "GitHub 仓库",
        "name_template": "${input.repo}",
        "description": "一个数据源分别读取开放 PR、开放 Issue 和 Star 数，PR/Issue 净增加时可提醒。",
        "icon": icon("github", "#374654"),
        "inputs": {
            "owner": {"type": "string", "label": "仓库所有者",
                      "default": "kevinhuang001", "required": True},
            "repo": {"type": "string", "label": "仓库名",
                     "default": "peninsula", "required": True},
        },
        "requests": {
            "pull_requests": {
                "method": "GET",
                "url": "https://api.github.com/search/issues",
                "headers": headers,
                "query": {
                    "q": "repo:${input.owner}/${input.repo} is:pr is:open",
                    "per_page": "1",
                },
                "timeout_ms": 10000,
            },
            "issues": {
                "method": "GET",
                "url": "https://api.github.com/search/issues",
                "headers": headers,
                "query": {
                    "q": "repo:${input.owner}/${input.repo} is:issue is:open",
                    "per_page": "1",
                },
                "timeout_ms": 10000,
            },
            "repository": {
                "method": "GET",
                "url": "https://api.github.com/repos/${input.owner}/${input.repo}",
                "headers": headers,
                "timeout_ms": 10000,
            },
        },
        "values": {
            "pull_requests": {
                "name": "开放 PR",
                "request": "pull_requests",
                "value": {"path": "$.total_count", "type": "number",
                          "decimals": 0, "separator": True, "suffix": " 个"},
                "alert": {"mode": "change", "operator": "gt", "threshold": 0,
                          "title": "${input.repo} PR 增加",
                          "message": "开放 PR 净增 ${delta} 个，目前 ${value}。"},
            },
            "issues": {
                "name": "开放 Issue",
                "request": "issues",
                "value": {"path": "$.total_count", "type": "number",
                          "decimals": 0, "separator": True, "suffix": " 个"},
                "alert": {"mode": "change", "operator": "gt", "threshold": 0,
                          "title": "${input.repo} Issue 增加",
                          "message": "开放 Issue 净增 ${delta} 个，目前 ${value}。"},
            },
            "stars": {
                "name": "Star 数",
                "request": "repository",
                "value": {"path": "$.stargazers_count", "type": "number",
                          "decimals": 0, "separator": True, "suffix": " 个"},
            },
        },
    }


development = [github_source()]

# Remove files no longer listed in the catalog, including the three former GitHub entries.
for obsolete in (
    "open-meteo-shanghai-temperature", "open-meteo-shanghai-humidity",
    "coingecko-bitcoin-usd", "frankfurter-usd-cny",
    "github-open-prs", "github-open-issues", "github-repository-stars"
):
    (OUT / f"{obsolete}.pds.json").unlink(missing_ok=True)

# Official brand marks used by the website, rather than letter avatars.
WEB_LOGOS = ROOT / "public" / "logos"
WEB_LOGOS.mkdir(parents=True, exist_ok=True)
for brand in ("opencode", "deepseek", "zhipu", "minimax", "github"):
    logo_svg = (LOGOS / f"{brand}.svg").read_text()
    (WEB_LOGOS / f"{brand}.svg").write_text(logo_svg.replace('fill="currentColor"', 'fill="#ffffff"'))


for d in ai + development:
    (OUT / f"{d['id']}.pds.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

print(f"Generated {len(ai) + len(development)} Peninsula data sources")
