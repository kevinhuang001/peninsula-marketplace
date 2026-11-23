# Peninsula Marketplace

Peninsula 数据源目录。下载 `.pds.json`，在 Peninsula 的「数据源」页面导入。

当前有 6 个 AI 额度数据源和 1 个 GitHub 仓库数据源。

## 使用

```sh
npm ci
npm run dev
```

```sh
npm run generate
python3 scripts/check_catalog.py
npm run build
```

静态网站输出到 `docs/`，GitHub Pages 使用 `main` 下的 `/docs`。

## GitHub 仓库

- **一个数据源、三个数值**：开放 PR、开放 Issue、Star 总数，一次 GraphQL 请求读取。
- 输入 GitHub 仓库所有者、仓库名和 Token。导入后显示名称可用仓库名 `${input.repo}`，修改参数后同步变更。
- 每个指标分别控制胶囊。PR 和 Issue 还可分别开关通知，并设置最短提醒间隔。
- PR/Issue 默认仅在开放数量**净增加**时提醒。首次成功刷新仅建立基准值，不产生变化提醒。两次刷新之间创建又关闭的项目无法通过净数量识别；不是 GitHub Webhook。
- GitHub GraphQL API **必须使用 Token**。对公开仓库只需能够查询公开仓库的凭证；私有仓库需要账户和凭证具备相应权限。
- 多指标文件使用 `peninsula.datasource/v2`。请使用包含多指标功能的新版 Peninsula。

AI 单值数据源仍使用 `peninsula.datasource/v1`。

## 密钥

Key 使用普通 `string` 参数，可以填写明文，或通过 `$名称$` 引用 Peninsula「秘密」页面中保存的条目。定义文件中使用 `${input.api_key}`，不使用 `${secret.api_key}`。

## 图标

数据源图标是嵌入的 SVG 路径图形；商城卡片展示厂商 Logo，不再使用单字母占位。SVG 路径来自 Simple Icons（CC0）和 LobeHub Icons（MIT）等开源图标集合；商标权归各自所有者。
