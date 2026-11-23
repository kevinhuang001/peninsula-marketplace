import { useMemo, useState } from 'react';
import { MantineProvider, Modal, TextInput, Select, Button, Badge } from '@mantine/core';
import { ArrowUpRight, BellRing, ChevronDown, Code2, Download, Github, LayoutGrid, Search, Sparkles, X } from 'lucide-react';
import { catalog, categories } from '../catalog.js';

const base = import.meta.env.BASE_URL;
const downloadUrl = (id) => `${base}pds/${id}.pds.json`;
const categoryIcon = { '全部': LayoutGrid, 'AI': Sparkles, '开发': Code2 };

function SourceCard({ item, onOpen }) {
  return <button className="source-card" onClick={() => onOpen(item)} aria-label={`查看 ${item.name} ${item.metric} 详情`}>
    <div className="card-upper"><span className={`item-icon ${item.tone}`}>{item.logo ? <img src={`${base}logos/${item.logo}.svg`} alt="" /> : item.icon}</span><Badge variant="light" radius="xl" className="source-badge">{item.tag}</Badge></div>
    <div className="card-main"><span className="provider-label">{item.provider}</span><h3>{item.name}<br/><span>{item.metric}</span></h3><p>{item.description}</p></div>
    <div className="card-lower"><span className="category-foot"><span className="small-dot" />{item.category}</span><span className="view-detail">查看详情 <ArrowUpRight size={16}/></span></div>
  </button>;
}

function SourceDetail({ item, onClose }) {
  return <Modal opened={!!item} onClose={onClose} centered size="lg" radius="lg" withCloseButton={false} overlayProps={{ backgroundOpacity: .62, blur: 6 }} classNames={{ content: 'detail-modal', body: 'detail-body' }}>
    {item && <>
      <button className="detail-close" onClick={onClose} aria-label="关闭详情"><X size={20}/></button>
      <div className="detail-heading"><span className={`item-icon detail-icon ${item.tone}`}>{item.logo ? <img src={`${base}logos/${item.logo}.svg`} alt="" /> : item.icon}</span><div><span className="eyebrow">{item.category} / {item.tag}</span><h2>{item.name}<span> {item.metric}</span></h2></div></div>
      <p className="detail-description">{item.description}</p>
      <div className="detail-facts"><div><small>数据提供方</small><strong>{item.provider}</strong></div><div><small>认证方式</small><strong>{item.auth}</strong></div><div><small>显示单位</small><strong>{item.unit}</strong></div></div>
      {item.alert && <div className="alert-box"><BellRing size={20}/><div><strong>支持提醒</strong><p>{item.alert}。导入后可分别开关各项提醒，并设置最短提醒间隔。</p></div></div>}
      {item.note && <p className="compat-note">兼容提示：{item.note}</p>}
      <div className="detail-instructions"><span className="eyebrow">导入方法</span><ol><li>下载数据源文件</li><li>打开 Peninsula 的「数据源」，点击「导入」</li><li>{item.category === '开发' ? '填写仓库所有者和仓库名' : '填写所需参数'}，然后设置刷新间隔{item.alert ? '和提醒选项' : ''}</li></ol></div>
      <div className="detail-actions"><Button component="a" href={downloadUrl(item.id)} download={`${item.id}.pds.json`} size="md" leftSection={<Download size={17}/>} className="download-button">下载文件</Button><a className="source-link" href={item.source} target="_blank" rel="noopener noreferrer">API 文档 <ArrowUpRight size={15}/></a></div>
    </>}
  </Modal>;
}

function CategoryNav({ selected, onSelect, className = '' }) {
  return <nav className={`category-nav ${className}`} aria-label="数据源分类">{categories.map(category => {
    const Icon = categoryIcon[category.name];
    const count = category.name === '全部' ? catalog.length : catalog.filter(item => item.category === category.name).length;
    return <button key={category.name} className={`category-button ${selected === category.name ? 'active' : ''}`} onClick={() => onSelect(category.name)} aria-pressed={selected === category.name}><Icon size={17}/><span>{category.name}</span><span className="category-count">{count}</span></button>;
  })}</nav>;
}

function App() {
  const [category, setCategory] = useState('全部');
  const [search, setSearch] = useState('');
  const [sort, setSort] = useState('featured');
  const [selected, setSelected] = useState(null);
  const results = useMemo(() => {
    const query = search.trim().toLocaleLowerCase();
    const list = catalog.filter(item => (category === '全部' || item.category === category) && (!query || [item.name, item.metric, item.description, item.provider, item.category].some(value => value.toLocaleLowerCase().includes(query))));
    if (sort === 'name') list.sort((a, b) => `${a.name}${a.metric}`.localeCompare(`${b.name}${b.metric}`, 'zh-CN'));
    return list;
  }, [category, search, sort]);

  return <div className="app-shell">
    <aside className="sidebar"><a href="#top" className="brand" aria-label="Peninsula Marketplace 首页"><span className="brand-mark"><span/></span><span className="brand-name">Peninsula<small>Marketplace</small></span></a><div className="side-label">分类</div><CategoryNav selected={category} onSelect={setCategory}/><div className="sidebar-foot">选择数据源，下载后在 Peninsula 中导入。</div></aside>
    <main className="main" id="top"><header className="topbar"><span className="topbar-eyebrow">数据源目录</span><a href="https://github.com/kevinhuang001/peninsula-marketplace" target="_blank" rel="noopener noreferrer"><Github size={17}/> GitHub <ArrowUpRight size={15}/></a></header>
      <section className="collection" id="collection"><div className="section-heading"><div><h1>数据源</h1><p>下载并导入 Peninsula，可显示数值或设置提醒。</p></div><span className="result-count">{results.length} 个数据源</span></div><CategoryNav className="mobile-categories" selected={category} onSelect={setCategory}/><div className="toolbar"><TextInput aria-label="搜索数据源" placeholder="搜索数据源" leftSection={<Search size={18}/>} value={search} onChange={e => setSearch(e.currentTarget.value)} classNames={{root:'search-input',input:'search-field'}}/><Select aria-label="排序方式" data={[{ value:'featured', label:'默认排序' }, { value:'name', label:'按名称排序' }]} value={sort} onChange={value => setSort(value || 'featured')} rightSection={<ChevronDown size={16}/>} classNames={{root:'sort-select',input:'sort-field'}}/></div>
        {results.length ? <div className="card-grid">{results.map(item => <SourceCard key={item.id} item={item} onOpen={setSelected}/>)}</div> : <div className="empty-state"><Search size={32}/><h3>没有搜索结果</h3><p>可以更换关键词或清除筛选。</p><Button variant="light" onClick={() => { setSearch(''); setCategory('全部'); }}>清除筛选</Button></div>}
      </section>
      <section className="how-section"><h2>使用方法</h2><div className="steps"><div><span>1</span><strong>下载</strong><p>选择数据源，下载 .pds.json 文件。</p></div><div><span>2</span><strong>导入</strong><p>在 Peninsula 的「数据源」中导入文件。</p></div><div><span>3</span><strong>设置</strong><p>填写参数，并设置刷新和提醒选项。</p></div></div></section>
      <footer><span>© 2026 Peninsula Marketplace</span><a href="https://github.com/kevinhuang001/peninsula-marketplace" target="_blank" rel="noopener noreferrer">源代码和反馈</a></footer>
    </main><SourceDetail item={selected} onClose={() => setSelected(null)}/>
  </div>;
}

export default function Marketplace() {
  return <MantineProvider theme={{ primaryColor: 'teal', fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Noto Sans SC", "PingFang SC", sans-serif' }}><App/></MantineProvider>;
}
