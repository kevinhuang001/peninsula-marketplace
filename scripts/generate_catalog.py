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
STROKE_LOGOS = {"open-meteo", "frankfurter"}


def _logo_markup(name):
    text = (LOGOS / f"{name}.svg").read_text()
    start = text.index(">", text.index("<svg")) + 1
    inner = text[start:text.rindex("</svg>")]
    return re.sub(r"<title>.*?</title>", "", inner, flags=re.S).strip()


def icon(logo, bg, fg="#ffffff"):
    attributes = (
        f'fill="none" stroke="{fg}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
        if logo in STROKE_LOGOS
        else f'fill="{fg}" fill-rule="evenodd"'
    )
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
    if alert:
        d["alert"] = {"operator": "lt", "threshold": "${input.alert_threshold}",
                      "title": f"{name}偏低", "message": "当前剩余 ${value}，低于设定阈值，请检查额度。"}
    return d


ai = []
for period, title, color in [
    ("rolling", "滚动周期", "#0B766F"), ("weekly", "每周", "#216A70"), ("monthly", "每月", "#365B75")
]:
    ai.append(source(
        f"opencode-go-{period}-remaining", f"OpenCode Go · {title}剩余",
        "通过官方套餐 Usage API 读取已使用百分比，并换算为剩余百分比。需要 OpenCode Go 套餐 API Key；未知或无限额度不会伪装成数值。",
        "opencode", color, "GET", "https://opencode.ai/zen/go/v1/usage",
        f"$.usage.{period}.percent", headers={"Authorization": "Bearer ${input.api_key}", "Accept": "application/json"},
        inputs={"api_key": api_key("OpenCode Go 套餐 API Key"),
                "alert_threshold": threshold("低额度提醒阈值（%）", 15)},
        multiply=-1, offset=100, suffix="%", alert=True))

ai.append(source(
    "deepseek-cny-balance", "DeepSeek · 人民币余额",
    "通过官方余额 API 读取 CNY 账户总余额。仅适用于返回人民币余额的账户；需要 DeepSeek API Key。",
    "deepseek", "#3469B2", "GET", "https://api.deepseek.com/user/balance",
    "$.balance_infos[?(@.currency=='CNY')].total_balance",
    headers={"Authorization": "Bearer ${input.api_key}", "Accept": "application/json"},
    inputs={"api_key": api_key("DeepSeek API Key"),
            "alert_threshold": threshold("低余额提醒阈值（元）", 10)},
    decimals=2, suffix=" 元", alert=True))

ai.append(source(
    "glm-cn-coding-remaining", "GLM · Coding Plan 剩余",
    "中国区 Coding Plan 编程额度的剩余百分比。读取第一个 TOKENS_LIMIT 周期；需使用中国区套餐 Key。",
    "zhipu", "#6153AF", "GET", "https://open.bigmodel.cn/api/monitor/usage/quota/limit",
    "$.data.limits[?(@.type=='TOKENS_LIMIT')].percentage",
    headers={"Authorization": "${input.api_key}", "Accept": "application/json"},
    inputs={"api_key": api_key("GLM 中国区 Coding Plan Key"),
            "alert_threshold": threshold("低额度提醒阈值（%）", 15)},
    multiply=-1, offset=100, suffix="%", alert=True))

ai.append(source(
    "minimax-cn-current-remaining", "MiniMax · 当前周期剩余",
    "中国区 Coding Plan 的 general 额度池当前周期剩余百分比。仅支持返回显式 remaining_percent 的套餐响应。",
    "minimax", "#D86B48", "GET", "https://api.minimax.cn/v1/token_plan/remains",
    "$.model_remains[?(@.model_name=='general')].current_interval_remaining_percent",
    headers={"Authorization": "Bearer ${input.api_key}", "Accept": "application/json"},
    inputs={"api_key": api_key("MiniMax 中国区 Coding Plan Key"),
            "alert_threshold": threshold("低额度提醒阈值（%）", 15)},
    suffix="%", alert=True))

others = [
    source("open-meteo-shanghai-temperature", "上海实时气温", "Open-Meteo 当前 2 米气温。经纬度可在导入后调整，默认上海。", "open-meteo", "#D88B42", "GET", "https://api.open-meteo.com/v1/forecast", "$.current.temperature_2m", query={"latitude": "${input.latitude}", "longitude": "${input.longitude}", "current": "temperature_2m", "timezone": "auto"}, inputs={"latitude": {"type": "number", "label": "纬度", "default": 31.2304, "required": True, "min": -90, "max": 90}, "longitude": {"type": "number", "label": "经度", "default": 121.4737, "required": True, "min": -180, "max": 180}}, decimals=1, suffix=" °C"),
    source("open-meteo-shanghai-humidity", "上海实时湿度", "Open-Meteo 当前相对湿度。经纬度可在导入后调整，默认上海。", "open-meteo", "#467B9F", "GET", "https://api.open-meteo.com/v1/forecast", "$.current.relative_humidity_2m", query={"latitude": "${input.latitude}", "longitude": "${input.longitude}", "current": "relative_humidity_2m", "timezone": "auto"}, inputs={"latitude": {"type": "number", "label": "纬度", "default": 31.2304, "required": True, "min": -90, "max": 90}, "longitude": {"type": "number", "label": "经度", "default": 121.4737, "required": True, "min": -180, "max": 180}}, suffix="%"),
    source("coingecko-bitcoin-usd", "Bitcoin · 美元报价", "CoinGecko 公共 Simple Price API 返回的比特币美元现价。公共接口可能限流。", "bitcoin", "#BD8B39", "GET", "https://api.coingecko.com/api/v3/simple/price", "$.bitcoin.usd", query={"ids": "bitcoin", "vs_currencies": "usd"}, decimals=2, suffix=" USD"),
    source("frankfurter-usd-cny", "美元兑人民币汇率", "Frankfurter 最新 USD/CNY 参考汇率，数据按其公布频率更新。", "frankfurter", "#3C8A72", "GET", "https://api.frankfurter.dev/v1/latest", "$.rates.CNY", query={"base": "USD", "symbols": "CNY"}, decimals=4, suffix=" CNY")
]

for d in ai + others:
    (OUT / f"{d['id']}.pds.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

print(f"Generated {len(ai) + len(others)} Peninsula data sources")
