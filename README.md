# Peninsula Marketplace

Peninsula 数据源目录。浏览并下载 `.pds.json`，在 Peninsula 的「数据源」页面导入。

目前提供 AI 套餐额度、GitHub 开放 PR 数、开放 Issue 数和仓库 Star 数。

## 本地开发

```sh
npm ci
npm run dev
```

运行检查和构建：

```sh
npm run generate
python3 scripts/check_catalog.py
npm run build
```

网站静态文件输出到 `docs/`，GitHub Pages 使用 `main` 分支下的 `/docs`。推送 `main` 后的 GitHub Actions 会自动重新构建网站。

## 数据源

- AI：OpenCode Go、DeepSeek、GLM、MiniMax 的额度或余额。
- 开发：GitHub 开放 PR、开放 Issue 和 Star 数。可配置仓库所有者和仓库名，默认示例为 `kevinhuang001/peninsula`。
- GitHub PR 与 Issue 提醒基于**当前开放数量**判断，默认数量大于 0 时提醒。刷新由 Peninsula 管理，不是 GitHub Webhook 或事件推送；通知还会遵守最短提醒间隔。
- GitHub 数据源使用公开 API，无需 Token，只适用于公开仓库。匿名 API 有速率限制，建议不要把刷新间隔设得过短。

数据源文件由 `scripts/generate_catalog.py` 生成到 `public/pds/`。刷新间隔和提醒冷却在 Peninsula 导入后配置，不写入定义文件。

## 密钥

API Key 使用普通 `string` 参数。可以填写明文，或填写 `$名称$` 引用 Peninsula「秘密」页面中保存的条目。定义文件使用 `${input.api_key}`，不支持 `${secret.api_key}`。

## 图标

`scripts/logos` 内使用 SVG 路径，不使用 `<text>`。图标参考 Simple Icons（CC0）、LobeHub Icons（MIT）和 Lucide（ISC）；GitHub 图标采用 GitHub 的矢量标记。
