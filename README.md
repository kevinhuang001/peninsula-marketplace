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
