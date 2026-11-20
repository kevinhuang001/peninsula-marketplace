# Peninsula Marketplace

基于 Astro、React 和 Mantine 的 Peninsula 数据源目录。站点提供分类、搜索、详情和 `.pds.json` 下载。AI 类数据源含可调整的低额度预警阈值。

## 本地开发

```sh
npm ci
npm run dev
```

## 构建与部署

```sh
npm run build
```

构建产物直接保存在根目录 `docs`。GitHub Pages 使用 **Deploy from a branch**、`main`、`/docs`。

数据源定义由 `scripts/generate_catalog.py` 生成至 `public/pds`，更新后运行 `npm run build`。Peninsula 只支持一次请求提取一个数值，因此每个额度周期有独立文件。刷新间隔和提醒冷却在 Peninsula 导入后配置。

## 密钥约定

PDS 里的密钥只是普通 `string` 参数，不声明“secret”类型。用户在参数中填写：

- 明文 Key：保存在 Peninsula 本机实例配置中；或
- `$名称$`：引用 Peninsula 的「秘密」页中保存的同名条目，发送请求时解析。

因此定义文件里使用 `${input.api_key}`，不要使用 `${secret.api_key}`。

## 图标

`scripts/logos` 中的品牌图标来自 [Simple Icons](https://simpleicons.org/)（CC0）、[LobeHub Icons](https://github.com/lobehub/lobe-icons)（MIT）和 [Lucide](https://lucide.dev/)（ISC）。生成器会把它们组合成带品牌色背景的 64×64 SVG。图标必须是路径/形状图形，不能使用 SVG `<text>`，因为 Peninsula 的渲染器不会把文字栅格化。
