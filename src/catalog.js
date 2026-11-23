export const catalog = [
  { id: 'opencode-go-rolling-remaining', name: 'OpenCode Go', metric: '滚动周期剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '显示滚动周期剩余额度。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'opencode-go-weekly-remaining', name: 'OpenCode Go', metric: '每周剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '显示本周剩余额度，低于阈值时提醒。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'opencode-go-monthly-remaining', name: 'OpenCode Go', metric: '每月剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '显示本月剩余额度，低于阈值时提醒。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'deepseek-cny-balance', name: 'DeepSeek', metric: '人民币余额', category: 'AI', icon: 'D', tone: 'blue', tag: '账户余额', provider: 'DeepSeek', description: '读取 DeepSeek 官方账户余额接口中的人民币总余额。', auth: 'API Key', unit: '元', alert: '默认低于 10 元提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/deepseek_quota.rs' },
  { id: 'glm-cn-coding-remaining', name: 'GLM', metric: 'Coding Plan 剩余', category: 'AI', icon: 'G', tone: 'purple', tag: '编程套餐', provider: '智谱 AI', description: '显示中国区 Coding Plan 的剩余百分比。', auth: '中国区套餐 Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs', note: '如果接口返回多个 TOKENS_LIMIT 周期，Peninsula 的单值提取会报告无法唯一匹配。' },
  { id: 'minimax-cn-current-remaining', name: 'MiniMax', metric: '当前周期剩余', category: 'AI', icon: 'M', tone: 'coral', tag: '编程套餐', provider: 'MiniMax', description: '显示中国区 Coding Plan 当前周期余量。', auth: '中国区套餐 Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs', note: '需要接口返回显式 remaining_percent；旧版计数字段暂不支持。' },
  { id: 'github-open-prs', name: 'GitHub', metric: '开放 PR', category: '开发', icon: 'GH', tone: 'slate', tag: '可提醒', provider: 'GitHub', description: '显示公开仓库当前未关闭的 Pull Request 数量。数量超过阈值时提醒。', auth: '无需密钥（公开仓库）', unit: '个', alert: '数量大于默认阈值 0 时提醒', source: 'https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests', note: '提醒按刷新周期检查，并受 Peninsula 的最短提醒间隔限制。它不是 GitHub 事件推送。' },
  { id: 'github-open-issues', name: 'GitHub', metric: '开放 Issue', category: '开发', icon: 'GH', tone: 'slate', tag: '可提醒', provider: 'GitHub', description: '显示公开仓库当前未关闭的 Issue 数量。数量超过阈值时提醒。', auth: '无需密钥（公开仓库）', unit: '个', alert: '数量大于默认阈值 0 时提醒', source: 'https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests', note: '统计不包含 PR。GitHub 匿名搜索接口有限流，建议设置较长的刷新间隔。' },
  { id: 'github-repository-stars', name: 'GitHub', metric: '仓库 Star 数', category: '开发', icon: 'GH', tone: 'slate', tag: '无需密钥', provider: 'GitHub', description: '显示公开 GitHub 仓库的 Star 总数。', auth: '无需密钥（公开仓库）', unit: '个', source: 'https://docs.github.com/en/rest/repos/repos#get-a-repository', note: '使用 GitHub 公开 API，匿名调用有速率限制。' }
];

export const categories = [
  { name: '全部' },
  { name: 'AI' },
  { name: '开发' }
];
