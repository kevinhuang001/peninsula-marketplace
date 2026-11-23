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
    assert data["request"]["method"] in {"GET", "POST", "PUT", "PATCH"}
    assert data["request"]["url"].startswith("https://")
    assert "interval" not in data["request"]
    assert all(entry["type"] != "secret" for entry in data["inputs"].values())

    request_text = json.dumps(data["request"], ensure_ascii=False)
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
        assert data["request"]["url"] == "https://api.github.com/graphql"
        assert data["request"]["method"] == "POST"
        assert data["request"]["headers"]["Authorization"] == "Bearer ${input.api_key}"
        assert set(data["values"]) == {"pull_requests", "issues", "stars"}
        assert data["values"]["pull_requests"]["value"]["path"] == "$.data.repository.pullRequests.totalCount"
        assert data["values"]["issues"]["value"]["path"] == "$.data.repository.issues.totalCount"
        assert data["values"]["stars"]["value"]["path"] == "$.data.repository.stargazerCount"
        for metric in ("pull_requests", "issues"):
            alert = data["values"][metric]["alert"]
            assert alert["mode"] == "change"
            assert alert["operator"] == "gt" and alert["threshold"] == 0
            assert "${delta}" in alert["message"]
        assert "alert" not in data["values"]["stars"]

for brand in ("opencode", "deepseek", "zhipu", "minimax", "github"):
    assert (root / "public" / "logos" / f"{brand}.svg").exists()

print(f"Checked {len(files)} data sources and brand icons")
