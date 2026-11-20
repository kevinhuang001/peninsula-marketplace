export const catalog = [
  { id: 'opencode-go-rolling-remaining', name: 'OpenCode Go', metric: '滚动周期剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '把官方套餐的滚动周期使用率转换为剩余百分比。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'opencode-go-weekly-remaining', name: 'OpenCode Go', metric: '每周剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '查看本周套餐余量，方便在周额度耗尽前收到提醒。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'opencode-go-monthly-remaining', name: 'OpenCode Go', metric: '每月剩余', category: 'AI', icon: 'O', tone: 'teal', tag: '订阅额度', provider: 'OpenCode', description: '查看每月套餐余量，并可自定义低额度提醒线。', auth: '套餐 API Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs' },
  { id: 'deepseek-cny-balance', name: 'DeepSeek', metric: '人民币余额', category: 'AI', icon: 'D', tone: 'blue', tag: '账户余额', provider: 'DeepSeek', description: '读取 DeepSeek 官方账户余额接口中的人民币总余额。', auth: 'API Key', unit: '元', alert: '默认低于 10 元提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/deepseek_quota.rs' },
  { id: 'glm-cn-coding-remaining', name: 'GLM', metric: 'Coding Plan 剩余', category: 'AI', icon: 'G', tone: 'purple', tag: '编程套餐', provider: '智谱 AI', description: '从中国区 Coding Plan 读取编程额度使用率，显示剩余百分比。', auth: '中国区套餐 Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs', note: '如果接口返回多个 TOKENS_LIMIT 周期，Peninsula 的单值提取会报告无法唯一匹配。' },
  { id: 'minimax-cn-current-remaining', name: 'MiniMax', metric: '当前周期剩余', category: 'AI', icon: 'M', tone: 'coral', tag: '编程套餐', provider: 'MiniMax', description: '读取中国区 Coding Plan 中 general 额度池的当前周期剩余百分比。', auth: '中国区套餐 Key', unit: '%', alert: '默认低于 15% 提醒', source: 'https://github.com/Renly1994/xiaotang-daozai/blob/main/src/plan_quota.rs', note: '需要接口返回显式 remaining_percent；旧版计数字段暂不支持。' },
  { id: 'open-meteo-shanghai-temperature', name: 'Open-Meteo', metric: '实时气温', category: '天气', icon: '☀', tone: 'amber', tag: '无需密钥', provider: 'Open-Meteo', description: '当前气温一眼可见。默认上海，导入后可改经纬度。', auth: '无需密钥', unit: '°C', source: 'https://open-meteo.com/en/docs' },
  { id: 'open-meteo-shanghai-humidity', name: 'Open-Meteo', metric: '实时湿度', category: '天气', icon: '≈', tone: 'sky', tag: '无需密钥', provider: 'Open-Meteo', description: '显示当前位置的实时相对湿度。默认上海。', auth: '无需密钥', unit: '%', source: 'https://open-meteo.com/en/docs' },
  { id: 'coingecko-bitcoin-usd', name: 'Bitcoin', metric: '美元报价', category: '市场', icon: '₿', tone: 'gold', tag: '无需密钥', provider: 'CoinGecko', description: '从 CoinGecko 公共接口获取 BTC 的美元现价。', auth: '无需密钥', unit: 'USD', source: 'https://docs.coingecko.com/reference/simple-price' },
  { id: 'frankfurter-usd-cny', name: 'USD / CNY', metric: '参考汇率', category: '市场', icon: '¥', tone: 'green', tag: '无需密钥', provider: 'Frankfurter', description: '查看最新公布的美元兑人民币参考汇率。', auth: '无需密钥', unit: 'CNY', source: 'https://frankfurter.dev/' }
];

export const categories = [
  { name: '全部', icon: '◈' },
  { name: 'AI', icon: '✦' },
  { name: '天气', icon: '☁' },
  { name: '市场', icon: '↗' }
];
