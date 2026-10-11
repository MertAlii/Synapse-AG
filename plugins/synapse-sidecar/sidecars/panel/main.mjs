import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';
import { SidecarApp, Response } from 'sidecar_sdk';

const here = dirname(fileURLToPath(import.meta.url));
const app = new SidecarApp();

function resolveVaultRoot(data = {}) {
  if (process.env.SYNAPSE_AG_ROOT && existsSync(process.env.SYNAPSE_AG_ROOT)) {
    return process.env.SYNAPSE_AG_ROOT;
  }
  if (data.workspaceUri) {
    try {
      const p = fileURLToPath(data.workspaceUri);
      if (existsSync(join(p, '.beyin-version'))) return p;
    } catch (_) {}
  }
  const defaultPath = join(homedir(), '.gemini', 'antigravity', 'scratch', 'synapse-ag');
  if (existsSync(defaultPath)) return defaultPath;
  return process.cwd();
}

function getVaultStatus(data) {
  const root = resolveVaultRoot(data);
  const kurallarPath = join(root, '850-Companion', 'Kurallar.md');
  const sessionPath = join(root, '850-Companion', 'Last-Session.md');
  const threadsPath = join(root, '850-Companion', 'Threads.md');
  const cognitivePath = join(root, '.agents', 'scripts', '.state', 'cognitive_state.json');

  let budgetUsed = 0;
  const budgetLimit = 9500;

  if (existsSync(kurallarPath)) budgetUsed += statSync(kurallarPath).size;
  if (existsSync(sessionPath)) budgetUsed += Math.min(statSync(sessionPath).size, 3000);
  if (existsSync(threadsPath)) budgetUsed += statSync(threadsPath).size;

  let cognitive = { hippocampus: 10, neocortex: 7, avgRetention: 0.88 };
  if (existsSync(cognitivePath)) {
    try {
      const cogData = JSON.parse(readFileSync(cognitivePath, 'utf8'));
      const items = Object.values(cogData.items || {});
      const hippo = items.filter(i => i.layer === 'hippocampus');
      const neo = items.filter(i => i.layer === 'neocortex');
      cognitive = {
        hippocampus: hippo.length,
        neocortex: neo.length,
        avgRetention: items.length > 0 ? (items.reduce((a, b) => a + (b.retention_score || 0), 0) / items.length) : 0.85
      };
    } catch (_) {}
  }

  // Yakala queue count
  let yakalaPending = 0;
  let yakalaProcessed = 0;
  const yakalaDir = join(root, '000-Inbox', 'Yakala');
  if (existsSync(yakalaDir)) {
    try {
      const files = readdirSync(yakalaDir).filter(f => f.endsWith('.md'));
      for (const f of files) {
        const txt = readFileSync(join(yakalaDir, f), 'utf8');
        if (txt.includes('status: islenmeyi_bekliyor') || txt.includes('durum: bekliyor')) {
          yakalaPending++;
        } else {
          yakalaProcessed++;
        }
      }
    } catch (_) {}
  }

  return {
    root,
    version: existsSync(join(root, '.beyin-version')) ? readFileSync(join(root, '.beyin-version'), 'utf8').trim() : '3.1.0',
    budgetUsed: Math.min(budgetUsed, budgetLimit),
    budgetLimit,
    budgetPercent: Math.min(100, Math.round((budgetUsed / budgetLimit) * 100)),
    cognitive,
    yakala: {
      pending: yakalaPending,
      processed: yakalaProcessed
    },
    online: true,
    timestamp: new Date().toISOString()
  };
}

function getRules(data) {
  const root = resolveVaultRoot(data);
  const kurallarPath = join(root, '850-Companion', 'Kurallar.md');
  const rules = [];

  if (existsSync(kurallarPath)) {
    const content = readFileSync(kurallarPath, 'utf8');
    const lines = content.split('\n');
    let currentCategory = 'Genel';

    for (const line of lines) {
      if (line.startsWith('## ')) {
        currentCategory = line.replace('## ', '').trim();
      } else if (line.match(/^(\d+\.|\-|\*)\s+/)) {
        const text = line.replace(/^(\d+\.|\-|\*)\s+/, '').trim();
        if (text && text.length > 5) {
          rules.push({ category: currentCategory, rule: text });
        }
      }
    }
  }

  return { rules: rules.slice(0, 15) };
}

function getGraphData(data) {
  const root = resolveVaultRoot(data);
  const nodes = [];
  const links = [];

  const categories = [
    { name: 'Kumanda', color: '#f8fafc', group: 'center' },
    { name: 'Alkan Hafıza', color: '#a855f7', group: 'companion' },
    { name: 'Projeler', color: '#06b6d4', group: 'projects' },
    { name: 'Kalıcı Bilgi', color: '#10b981', group: 'knowledge' },
    { name: 'Günlük Loglar', color: '#3b82f6', group: 'daily' },
    { name: 'Gelen Kutusu', color: '#f59e0b', group: 'inbox' }
  ];

  nodes.push({ id: 'Center', name: 'Synapse-AG Hub', category: 'Kumanda', color: '#f8fafc', val: 20 });

  categories.forEach((cat, idx) => {
    if (cat.name === 'Kumanda') return;
    const catId = `cat_${idx}`;
    nodes.push({ id: catId, name: cat.name, category: cat.name, color: cat.color, val: 12 });
    links.push({ source: 'Center', target: catId });

    for (let i = 1; i <= 3; i++) {
      const leafId = `${catId}_leaf_${i}`;
      nodes.push({ id: leafId, name: `${cat.name} #${i}`, category: cat.name, color: cat.color, val: 6 });
      links.push({ source: catId, target: leafId });
    }
  });

  return { nodes, links };
}

// Routes
app.page('/', () => readFileSync(join(here, 'index.html'), 'utf8'));
app.page('/app.js', () => readFileSync(join(here, 'app.js'), 'utf8'));
app.api('/styles.css', () =>
  new Response(readFileSync(join(here, 'styles.css'), 'utf8'), { contentType: 'text/css' }),
  'GET'
);

app.api('/api/status', (data) => getVaultStatus(data), 'POST');
app.api('/api/status', (data) => getVaultStatus(data), 'GET');
app.api('/api/rules', (data) => getRules(data), 'POST');
app.api('/api/rules', (data) => getRules(data), 'GET');
app.api('/api/graph', (data) => getGraphData(data), 'POST');
app.api('/api/graph', (data) => getGraphData(data), 'GET');

app.run();
