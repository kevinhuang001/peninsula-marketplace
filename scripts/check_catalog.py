import base64
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted((root / 'public' / 'pds').glob('*.pds.json'))
assert len(files) == 9, f'Expected 9 sources, got {len(files)}'
for file in files:
    data = json.loads(file.read_text())
    assert data['schema'] == 'peninsula.datasource/v1'
    assert file.name == data['id'] + '.pds.json'
    assert ' · ' not in data['name'], f'{file.name}: names must not use middle dots'
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
        assert 'description' not in data['inputs']['api_key']
        assert 'description' not in data['inputs']['alert_threshold']
    if data['id'] in {'github-open-prs', 'github-open-issues'}:
        assert data['request']['url'] == 'https://api.github.com/search/issues'
        assert data['value']['path'] == '$.total_count'
        assert data['alert']['operator'] == 'gt'
        assert data['alert']['threshold'] == '${input.alert_threshold}'
        assert data['inputs']['owner']['required'] and data['inputs']['repo']['required']
        assert 'is:pr' in data['request']['query']['q'] if data['id'] == 'github-open-prs' else 'is:issue' in data['request']['query']['q']
    if data['id'] == 'github-repository-stars':
        assert data['value']['path'] == '$.stargazers_count'
        assert 'alert' not in data

assert {file.stem.removesuffix('.pds') for file in files} == {
    'opencode-go-rolling-remaining', 'opencode-go-weekly-remaining',
    'opencode-go-monthly-remaining', 'deepseek-cny-balance',
    'glm-cn-coding-remaining', 'minimax-cn-current-remaining',
    'github-open-prs', 'github-open-issues', 'github-repository-stars',
}
print(f'Checked {len(files)} data sources, GitHub counts, and image icons')
