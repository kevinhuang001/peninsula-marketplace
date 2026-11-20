import { useMemo, useState } from 'react';
import { MantineProvider, Modal, TextInput, Select, Button, Badge } from '@mantine/core';
import { ArrowDown, ArrowUpRight, BellRing, ChevronDown, CloudSun, Coins, Download, Github, Search, Sparkles, X } from 'lucide-react';
import { catalog, categories } from '../catalog.js';

const base = import.meta.env.BASE_URL;
const downloadUrl = (id) => `${base}pds/${id}.pds.json`;
const categoryIcon = { '全部': Sparkles, 'AI': Sparkles, '天气': CloudSun, '市场': Coins };

function SourceCard({ item, onOpen }) {
  return <button className="source-card" onClick={() => onOpen(item)} aria-label={`查看 ${item.name} ${item.metric} 详情`}>
    <div className="card-upper"><span className={`item-icon ${item.tone}`}>{item.icon}</span><Badge variant="light" radius="xl" className="source-badge">{item.tag}</Badge></div>
    <div className="card-main"><span className="provider-label">{item.provider}</span><h3>{item.name}<br/><span>{item.metric}</span></h3><p>{item.description}</p></div>
    <div className="card-lower"><span className="category-foot"><span className="small-dot" />{item.category}</span><span className="view-detail">查看详情 <ArrowUpRight size={16}/></span></div>
  </button>;
}

function SourceDetail({ item, onClose }) {
  return <Modal opened={!!item} onClose={onClose} centered size="lg" radius="lg" withCloseButton={false} overlayProps={{ backgroundOpacity: .62, blur: 6 }} classNames={{ content: 'detail-modal', body: 'detail-body' }}>
    {item && <>
      <button className="detail-close" onClick={onClose} aria-label="关闭详情"><X size={20}/></button>
      <div className="detail-heading"><span className={`item-icon detail-icon ${item.tone}`}>{item.icon}</span><div><span className="eyebrow">{item.category} / {item.tag}</span><h2>{item.name}<span> · {item.metric}</span></h2></div></div>
      <p className="detail-description">{item.description}</p>
      <div className="detail-facts"><div><small>数据提供方</small><strong>{item.provider}</strong></div><div><small>认证方式</small><strong>{item.auth}</strong></div><div><small>显示单位</small><strong>{item.unit}</strong></div></div>
      {item.alert && <div className="alert-box"><BellRing size={20}/><div><strong>低额度预警已配置</strong><p>{item.alert}。导入后可修改阈值，并设置刷新间隔和提醒冷却。</p></div></div>}
      {item.note && <p className="compat-note">兼容提示：{item.note}</p>}
      <div className="detail-instructions"><span className="eyebrow">如何使用</span><ol><li>下载 <code>.pds.json</code> 定义文件</li><li>在 Peninsula 的「数据源」中选择导入</li><li>填写{item.auth === '无需密钥' ? '参数' : '明文密钥或 $名称$，并设置提醒阈值'}，设置刷新间隔</li></ol></div>
      <div className="detail-actions"><Button component="a" href={downloadUrl(item.id)} download={`${item.id}.pds.json`} size="md" leftSection={<Download size={17}/>} className="download-button">下载 pds.json</Button><a className="source-link" href={item.source} target="_blank" rel="noopener noreferrer">查看接口来源 <ArrowUpRight size={15}/></a></div>
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
    <aside className="sidebar"><a href="#top" className="brand" aria-label="Peninsula Marketplace 首页"><span className="brand-mark"><span/></span><span className="brand-name">peninsula<small>marketplace</small></span></a><div className="side-label">探索</div><CategoryNav selected={category} onSelect={setCategory}/><div className="sidebar-foot"><span className="foot-mark">◌</span><div><strong>为 Peninsula 而造</strong><span>一个文件，即刻接入数据。</span></div></div></aside>
    <main className="main" id="top"><header className="topbar"><span className="topbar-eyebrow"><span className="online-dot"/> PENINSULA DATA SOURCE LIBRARY</span><a href="https://github.com/kevinhuang001/peninsula-marketplace" target="_blank" rel="noopener noreferrer"><Github size={17}/> GitHub <ArrowUpRight size={15}/></a></header>
      <section className="hero"><div className="hero-copy"><span className="hero-kicker"><Sparkles size={16}/> 扩展你的桌面视野</span><h1>你关心的数据，<br/><em>就在眼前。</em></h1><p>发现专为 Peninsula 设计的数据源。选一个喜欢的，下载并导入，让重要数字在桌面上持续可见。</p><a href="#collection" className="hero-button">探索数据源 <ArrowDown size={18}/></a></div><div className="hero-visual" aria-hidden="true"><div className="visual-orbit orbit-a"/><div className="visual-orbit orbit-b"/><div className="hero-island"><span className="island-face"><i/><i/></span><span className="island-meter"><Sparkles size={14}/> 额度剩余 <strong>82%</strong></span></div><div className="floating-label float-top">↗ &nbsp; 实时数据</div><div className="floating-label float-bottom">◌ &nbsp; 轻松导入</div><span className="decor-star star-a">✧</span><span className="decor-star star-b">✦</span></div></section>
      <section className="collection" id="collection"><div className="section-heading"><div><span className="eyebrow">THE COLLECTION</span><h2>数据源精选</h2><p>从 AI 额度到天气行情，为你的桌面找到刚好的信息。</p></div><span className="result-count">{results.length} 个数据源</span></div><CategoryNav className="mobile-categories" selected={category} onSelect={setCategory}/><div className="toolbar"><TextInput aria-label="搜索数据源" placeholder="搜索数据源、服务或关键词..." leftSection={<Search size={18}/>} value={search} onChange={e => setSearch(e.currentTarget.value)} classNames={{root:'search-input',input:'search-field'}}/><Select aria-label="排序方式" data={[{ value:'featured', label:'精选推荐' }, { value:'name', label:'按名称' }]} value={sort} onChange={value => setSort(value || 'featured')} rightSection={<ChevronDown size={16}/>} classNames={{root:'sort-select',input:'sort-field'}}/></div>
        {results.length ? <div className="card-grid">{results.map(item => <SourceCard key={item.id} item={item} onOpen={setSelected}/>)}</div> : <div className="empty-state"><Search size={32}/><h3>没有找到匹配的数据源</h3><p>试试其他关键词，或切换分类。</p><Button variant="light" onClick={() => { setSearch(''); setCategory('全部'); }}>清除筛选</Button></div>}
      </section>
      <section className="how-section"><div><span className="eyebrow">SIMPLE BY DESIGN</span><h2>从发现到展示，<br/>只需三步。</h2></div><div className="steps"><div><span>01</span><strong>挑选数据源</strong><p>按分类浏览，找到想持续关注的数字。</p></div><div><span>02</span><strong>下载定义文件</strong><p>每个数据源都有可直接导入的 .pds.json。</p></div><div><span>03</span><strong>导入 Peninsula</strong><p>填写参数，设置刷新与提醒。</p></div></div></section>
      <footer><span>© 2026 Peninsula Marketplace</span><span>为你的桌面，留住重要的数。</span></footer>
    </main><SourceDetail item={selected} onClose={() => setSelected(null)}/>
  </div>;
}

export default function Marketplace() {
  return <MantineProvider theme={{ primaryColor: 'teal', fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Noto Sans SC", "PingFang SC", sans-serif' }}><App/></MantineProvider>;
}
