import base64
import json
import re
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
    assert all(definition['type'] != 'secret' for definition in data['inputs'].values())

    request_text = json.dumps(data['request'], ensure_ascii=False)
    input_refs = set(re.findall(r'\$\{input\.([A-Za-z0-9_]+)\}', request_text))
    assert input_refs <= set(data['inputs']), f'{file.name}: undeclared input placeholder'
    # Secret values only travel through string inputs as `$名称$`; PDS files never name them.
    assert '${secret.' not in request_text, f'{file.name}: ${{secret.*}} is not part of the schema'

    svg = base64.b64decode(data['icon']['base64']).decode()
    assert '<text' not in svg.lower(), f'{file.name}: icon text does not render in Peninsula'
    assert any(tag in svg for tag in ('<path', '<rect', '<circle', '<polygon')), \
        f'{file.name}: icon needs path geometry'

    if data['id'].startswith(('opencode-', 'deepseek-', 'glm-', 'minimax-')):
        assert data['alert']['operator'] == 'lt'
        assert data['alert']['threshold'] == '${input.alert_threshold}'
        assert data['inputs']['alert_threshold']['type'] == 'number'
        assert data['inputs']['api_key']['type'] == 'string'
        assert '$名称$' in data['inputs']['api_key']['description']
print(f'Checked {len(files)} data sources, string-only API keys, and path-based icons')
