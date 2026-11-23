import base64
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted((root / "public" / "pds").glob("*.pds.json"))
expected = {
    "opencode-go-rolling-remaining", "opencode-go-weekly-remaining",
    "opencode-go-monthly-remaining", "deepseek-cny-balance",
    "glm-cn-coding-remaining", "minimax-cn-current-remaining",
    "github-repository",
}
assert {file.name.removesuffix(".pds.json") for file in files} == expected
for file in files:
    data = json.loads(file.read_text())
    assert file.name == f"{data['id']}.pds.json"
    assert data["schema"] in {"peninsula.datasource/v1", "peninsula.datasource/v2"}
    assert " · " not in data["name"]
    requests = [data["request"]] if "request" in data else list(data["requests"].values())
    assert requests
    for request in requests:
        assert request["method"] in {"GET", "POST", "PUT", "PATCH"}
        assert request["url"].startswith("https://")
        assert "interval" not in request
    assert all(entry["type"] != "secret" for entry in data["inputs"].values())

    request_text = json.dumps(requests, ensure_ascii=False)
    used = set(re.findall(r"\$\{input\.([A-Za-z0-9_]+)\}", request_text))
    assert used <= set(data["inputs"]), f"{file.name}: undeclared input"
    assert "${secret." not in request_text

    svg = base64.b64decode(data["icon"]["base64"]).decode()
    assert "<text" not in svg.lower()
    assert any(mark in svg for mark in ("<path", "<rect", "<circle", "<polygon"))

    if data["schema"] == "peninsula.datasource/v1":
        assert data["value"]["type"] == "number" and data["value"]["path"].startswith("$")
        assert data["alert"]["operator"] == "lt"
        assert data["inputs"]["api_key"]["type"] == "string"
        assert data["inputs"]["alert_threshold"]["type"] == "number"
    else:
        assert data["id"] == "github-repository"
        assert "value" not in data and "alert" not in data
        assert data["name_template"] == "${input.repo}"
        assert "request" not in data
        assert set(data["requests"]) == {"pull_requests", "issues", "repository"}
        for request in data["requests"].values():
            assert request["method"] == "GET"
            assert request["url"].startswith("https://api.github.com/")
        assert data["requests"]["pull_requests"]["url"] == "https://api.github.com/search/issues"
        assert data["requests"]["issues"]["url"] == "https://api.github.com/search/issues"
        assert data["requests"]["repository"]["url"] == "https://api.github.com/repos/${input.owner}/${input.repo}"
        assert "is:pr is:open" in data["requests"]["pull_requests"]["query"]["q"]
        assert "is:issue is:open" in data["requests"]["issues"]["query"]["q"]
        assert set(data["values"]) == {"pull_requests", "issues", "stars"}
        assert data["values"]["pull_requests"]["request"] == "pull_requests"
        assert data["values"]["issues"]["request"] == "issues"
        assert data["values"]["stars"]["request"] == "repository"
        assert data["values"]["pull_requests"]["value"]["path"] == "$.total_count"
        assert data["values"]["issues"]["value"]["path"] == "$.total_count"
        assert data["values"]["stars"]["value"]["path"] == "$.stargazers_count"
        for metric in ("pull_requests", "issues"):
            alert = data["values"][metric]["alert"]
            assert alert["mode"] == "change"
            assert alert["operator"] == "gt" and alert["threshold"] == 0
            assert "${delta}" in alert["message"]
        assert "alert" not in data["values"]["stars"]
        for metric, label in {"pull_requests": "PR", "issues": "Issue", "stars": "Star"}.items():
            assert data["values"][metric]["capsule_text"] == f"{label}: ${{value}}"
            assert data["values"][metric]["capsule_layout"] == "two_line"


for brand in ("opencode", "deepseek", "zhipu", "minimax", "github"):
    assert (root / "public" / "logos" / f"{brand}.svg").exists()

print(f"Checked {len(files)} data sources and brand icons")
