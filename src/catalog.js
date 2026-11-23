export const catalog = [
  { id: 'opencode-go-rolling-remaining', name: 'OpenCode Go', logo: 'opencode', metric: '滚动周期剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '显示滚动周期剩余额度。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'opencode-go-weekly-remaining', name: 'OpenCode Go', logo: 'opencode', metric: '每周剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '显示本周剩余额度，低于阈值时提醒。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'opencode-go-monthly-remaining', name: 'OpenCode Go', logo: 'opencode', metric: '每月剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '显示本月剩余额度，低于阈值时提醒。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'deepseek-cny-balance', name: 'DeepSeek', logo: 'deepseek', metric: '人民币余额', category: 'AI', icon: 'D', tone: 'blue', tag: '账户余额', provider: 'DeepSeek', description: '读取 DeepSeek 官方账户余额接口中的人民币总余额。', auth: 'API Key', unit: '元', alert: '默认低于 10 元提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/deepseek_quota.rs' },
  { id: 'glm-cn-coding-remaining', name: 'GLM', logo: 'zhipu', metric: 'Coding Plan 剩余', category: 'AI', icon: 'G', tone: 'purple', tag: '编程套餐', provider: '智谱 AI', description: '显示中国区 Coding Plan 的剩余百分比。', auth: '中国区套餐 Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs', note: '如果接口返回多个 TOKENS_LIMIT 周期，Peninsula 的单值提取会报告无法唯一匹配。' },
  { id: 'minimax-cn-current-remaining', name: 'MiniMax', logo: 'minimax', metric: '当前周期剩余', category: 'AI', icon: 'M', tone: 'coral', tag: '编程套餐', provider: 'MiniMax', description: '显示中国区 Coding Plan 当前周期余量。', auth: '中国区套餐 Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs', note: '需要接口返回显式 remaining_percent；旧版计数字段暂不支持。' },
  { id: 'github-repository', name: 'GitHub 仓库', logo: 'github', metric: 'PR、Issue、Star', category: '开发', icon: 'GH', tone: 'slate', tag: '3 个指标', provider: 'GitHub', description: '同一个仓库的开放 PR、开放 Issue 和 Star 数。PR 和 Issue 增加时可分别提醒。', auth: '无需密钥（公开仓库）', unit: '个', alert: 'PR 和 Issue 数净增加时分别提醒，Star 可独立显示', source: 'https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests', note: '对公开仓库无需 Token；首次刷新只记录基准值。开放数量的变化是净增量，不等于新建事件。匿名 API 存在速率限制。' }
];

export const categories = [
  { name: '全部' },
  { name: 'AI' },
  { name: '开发' }
];
