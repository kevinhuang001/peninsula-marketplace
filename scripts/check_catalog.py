import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted((root / 'public' / 'pds').glob('*.pds.json'))
assert len(files) == 10, f'Expected 10 sources, got {len(files)}'
for file in files:
    data = json.loads(file.read_text())
    assert data['schema'] == 'peninsula.datasource/v1'
    assert file.name == data['id'] + '.pds.json'
    assert set(data) <= {'schema', 'id', 'name', 'description', 'icon', 'inputs', 'request', 'value', 'alert'}
    assert data['request']['method'] in {'GET', 'POST', 'PUT', 'PATCH'}
    assert data['request']['url'].startswith('https://')
    assert data['value']['type'] == 'number' and data['value']['path'].startswith('$')
    assert 'interval' not in data['request']
    if data['id'].startswith(('opencode-', 'deepseek-', 'glm-', 'minimax-')):
        assert data['alert']['operator'] == 'lt'
        assert data['alert']['threshold'] == '${input.alert_threshold}'
        assert data['inputs']['alert_threshold']['type'] == 'number'
        assert data['inputs']['api_key']['type'] == 'secret'
print(f'Checked {len(files)} data sources and all AI low-quota alerts')
