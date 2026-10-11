// Synapse-AG Live Companion Panel Frontend Logic
(function () {
  const sidecar = window.sidecar || {
    fetch: (url, opts) => window.fetch(url, opts),
    conversationId: null,
    agent: {
      sendMessage: (msg) => console.log('Simulated Agent Message:', msg)
    }
  };

  let graphNodes = [];
  let graphLinks = [];
  let angleX = 0;
  let angleY = 0;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;

  // DOM Elements
  const budgetLabel = document.getElementById('budgetLabel');
  const budgetPercent = document.getElementById('budgetPercent');
  const gaugeFill = document.getElementById('gaugeFill');
  const hippoCount = document.getElementById('hippoCount');
  const neoCount = document.getElementById('neoCount');
  const yakalaPending = document.getElementById('yakalaPending');
  const retentionAvg = document.getElementById('retentionAvg');
  const rulesList = document.getElementById('rulesList');
  const refreshBtn = document.getElementById('refreshBtn');
  const canvas = document.getElementById('graphCanvas');
  const ctx = canvas ? canvas.getContext('2d') : null;

  async function loadStatus() {
    try {
      const res = await sidecar.fetch('/api/status', { method: 'POST', body: JSON.stringify({}) });
      const data = await res.json();

      budgetLabel.textContent = `Kullanılan: ${data.budgetUsed.toLocaleString()} / ${data.budgetLimit.toLocaleString()} Karakter`;
      budgetPercent.textContent = `%${data.budgetPercent}`;
      gaugeFill.style.width = `${data.budgetPercent}%`;

      if (data.budgetPercent > 80) {
        gaugeFill.style.background = 'linear-gradient(90deg, #f59e0b, #ef4444)';
      } else {
        gaugeFill.style.background = 'linear-gradient(90deg, #06b6d4, #a855f7)';
      }

      hippoCount.textContent = data.cognitive.hippocampus || 0;
      neoCount.textContent = data.cognitive.neocortex || 0;
      yakalaPending.textContent = data.yakala.pending || 0;
      retentionAvg.textContent = `%${Math.round((data.cognitive.avgRetention || 0.85) * 100)}`;
    } catch (err) {
      console.error('Error loading status:', err);
    }
  }

  async function loadRules() {
    try {
      const res = await sidecar.fetch('/api/rules', { method: 'POST', body: JSON.stringify({}) });
      const data = await res.json();

      rulesList.innerHTML = '';
      if (!data.rules || data.rules.length === 0) {
        rulesList.innerHTML = '<li class="rule-item">Henüz kural kaydedilmemiş.</li>';
        return;
      }

      data.rules.forEach((r) => {
        const li = document.createElement('li');
        li.className = 'rule-item';
        li.innerHTML = `
          <span class="rule-category">${r.category}</span>
          <span class="rule-text">${r.rule}</span>
        `;
        rulesList.appendChild(li);
      });
    } catch (err) {
      console.error('Error loading rules:', err);
    }
  }

  async function loadGraphData() {
    try {
      const res = await sidecar.fetch('/api/graph', { method: 'POST', body: JSON.stringify({}) });
      const data = await res.json();

      // Convert nodes to 3D sphere coordinates
      const N = data.nodes.length;
      graphNodes = data.nodes.map((n, i) => {
        const phi = Math.acos(-1 + (2 * i) / N);
        const theta = Math.sqrt(N * Math.PI) * phi;
        const radius = n.id === 'Center' ? 0 : 65;
        return {
          ...n,
          x: radius * Math.cos(theta) * Math.sin(phi),
          y: radius * Math.sin(theta) * Math.sin(phi),
          z: radius * Math.cos(phi)
        };
      });

      graphLinks = data.links;
    } catch (err) {
      console.error('Error loading graph:', err);
    }
  }

  // 3D Canvas Rendering
  function resizeCanvas() {
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  function render3DGraph() {
    if (!ctx || !canvas) return;
    const w = canvas.getBoundingClientRect().width;
    const h = canvas.getBoundingClientRect().height;
    ctx.clearRect(0, 0, w, h);

    if (!isDragging) {
      angleY += 0.006;
      angleX += 0.002;
    }

    const cosY = Math.cos(angleY);
    const sinY = Math.sin(angleY);
    const cosX = Math.cos(angleX);
    const sinX = Math.sin(angleX);

    const projected = graphNodes.map((n) => {
      // Rotation Y
      let x1 = n.x * cosY - n.z * sinY;
      let z1 = n.z * cosY + n.x * sinY;
      // Rotation X
      let y2 = n.y * cosX - z1 * sinX;
      let z2 = z1 * cosX + n.y * sinX;

      const fov = 160;
      const scale = fov / (fov + z2 + 80);
      return {
        ...n,
        px: w / 2 + x1 * scale,
        py: h / 2 + y2 * scale,
        scale: Math.max(0.2, scale),
        depth: z2
      };
    });

    // Links
    ctx.lineWidth = 1;
    graphLinks.forEach((l) => {
      const s = projected.find((p) => p.id === l.source);
      const t = projected.find((p) => p.id === l.target);
      if (s && t) {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
        ctx.beginPath();
        ctx.moveTo(s.px, s.py);
        ctx.lineTo(t.px, t.py);
        ctx.stroke();
      }
    });

    // Sort by depth
    projected.sort((a, b) => a.depth - b.depth);

    // Nodes
    projected.forEach((n) => {
      const r = (n.val || 8) * n.scale;
      ctx.fillStyle = n.color || '#06b6d4';
      ctx.shadowBlur = 8 * n.scale;
      ctx.shadowColor = n.color || '#06b6d4';
      ctx.beginPath();
      ctx.arc(n.px, n.py, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;

      // Label for center or main nodes
      if (n.val >= 12 && n.scale > 0.8) {
        ctx.fillStyle = '#ffffff';
        ctx.font = '9px sans-serif';
        ctx.fillText(n.name, n.px + r + 3, n.py + 3);
      }
    });

    requestAnimationFrame(render3DGraph);
  }

  // Mouse Interaction for 3D rotation
  if (canvas) {
    canvas.addEventListener('mousedown', (e) => {
      isDragging = true;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    });

    window.addEventListener('mouseup', () => {
      isDragging = false;
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const dx = e.clientX - lastMouseX;
      const dy = e.clientY - lastMouseY;
      angleY += dx * 0.01;
      angleX += dy * 0.01;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    });
  }

  // Quick Action Buttons
  function setupActions() {
    const actYakala = document.getElementById('actProcessYakala');
    const actDevil = document.getElementById('actDevilCheck');
    const actDoctor = document.getElementById('actRunDoctor');
    const actCompile = document.getElementById('actCompile');

    const sendMsg = (msg) => {
      if (sidecar.agent && sidecar.agent.sendMessage) {
        sidecar.agent.sendMessage(msg);
      } else {
        alert(`Ajan Komutu Gönderildi: "${msg}"`);
      }
    };

    if (actYakala) actYakala.addEventListener('click', () => sendMsg('yakalananları işle'));
    if (actDevil) actDevil.addEventListener('click', () => sendMsg('Şeytanın avukatı gözüyle son aldığımız kararı analiz et'));
    if (actDoctor) actDoctor.addEventListener('click', () => sendMsg('beyin doktor'));
    if (actCompile) actCompile.addEventListener('click', () => sendMsg('hafızayı derle'));

    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        loadStatus();
        loadRules();
        loadGraphData();
      });
    }
  }

  // Initialization
  window.addEventListener('DOMContentLoaded', () => {
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    loadStatus();
    loadRules();
    loadGraphData();
    setupActions();
    requestAnimationFrame(render3DGraph);

    // Auto-refresh every 20 seconds
    setInterval(() => {
      loadStatus();
      loadRules();
    }, 20000);
  });
})();
