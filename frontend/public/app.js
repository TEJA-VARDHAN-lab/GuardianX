(() => {
  const api = (path, options) => fetch(`/api${path}`, { headers: { 'Content-Type': 'application/json' }, ...options }).then(r => r.json());

  function setText(label, value) {
    const card = [...document.querySelectorAll('.glass-panel')].find(el => el.textContent.includes(label));
    const valueNode = card && card.querySelector('h2');
    if (valueNode) valueNode.textContent = value;
  }

  function escapeHtml(value) {
    const node = document.createElement('span');
    node.textContent = value;
    return node.innerHTML;
  }

  function renderIncidents(incidents) {
    const tbody = document.querySelector('tbody');
    if (!tbody) return;
    tbody.innerHTML = incidents.map(i => `<tr class="severity-${i.severity === 'critical' ? 'critical' : i.severity === 'warning' ? 'warning' : 'info'} hover:bg-surface-container-highest/20 transition-colors"><td class="px-6 py-4"><div class="flex items-center gap-3"><span class="font-bold">${escapeHtml(i.type)}</span></div></td><td class="px-6 py-4"><span class="bg-primary/10 text-primary px-2 py-1 rounded text-[10px] font-black uppercase tracking-widest">${escapeHtml(i.severity)}</span></td><td class="px-6 py-4 font-data-mono text-on-surface-variant">${escapeHtml(i.timestamp)}</td><td class="px-6 py-4 text-right text-primary">${escapeHtml(i.status)}</td></tr>`).join('');
  }

  async function refresh() {
    const dashboard = await api('/dashboard');
    setText('Total Incidents', dashboard.stats.totalIncidents);
    setText('Active Alerts', dashboard.stats.activeAlerts);
    setText('Resolved', dashboard.stats.resolved);
    renderIncidents(dashboard.incidents);
  }

  document.addEventListener('DOMContentLoaded', () => {
    installCyberScene();
    refresh().catch(console.error);
    const search = document.querySelector('input[placeholder^="Search"]');
    search?.addEventListener('input', async event => {
      const result = await api(`/incidents?q=${encodeURIComponent(event.target.value)}`);
      renderIncidents(result.incidents);
    });
    const deploy = [...document.querySelectorAll('button')].find(button => button.textContent.includes('Deploy Response'));
    deploy?.addEventListener('click', async () => {
      await api('/deployments', { method: 'POST', body: '{}' });
      deploy.textContent = 'Response Deployed';
    });
    const ai = [...document.querySelectorAll('button')].find(button => button.textContent.includes('Query AI System'));
    ai?.addEventListener('click', async () => {
      const query = window.prompt('Enter a command for the AI system:');
      if (query === null) return;
      const result = await api('/ai/query', { method: 'POST', body: JSON.stringify({ query }) });
      window.alert(result.reply);
    });
    addOperationsViews();
  });

  function installCyberScene() {
    const style = document.createElement('style');
    style.textContent = `
      #guardianx-cyber-layer { position: fixed; inset: 0; z-index: 1; pointer-events: none; opacity: .34; mix-blend-mode: screen; }
      .glass-panel { transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease; }
      .glass-panel:hover { transform: translateY(-3px) perspective(900px) rotateX(1deg); border-color: rgba(173,198,255,.28); box-shadow: 0 18px 45px rgba(0,90,194,.13); }
      main, aside, header { isolation: isolate; }
      @media (prefers-reduced-motion: reduce) { #guardianx-cyber-layer { display: none; } .glass-panel { transition: none; } .glass-panel:hover { transform: none; } }
    `;
    document.head.appendChild(style);

    const canvas = document.createElement('canvas');
    canvas.id = 'guardianx-cyber-layer';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.appendChild(canvas);
    const context = canvas.getContext('2d');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const particles = Array.from({ length: 46 }, () => ({ x: Math.random(), y: Math.random(), z: .2 + Math.random() * .8, speed: .00015 + Math.random() * .00055 }));

    function size() { canvas.width = window.innerWidth * devicePixelRatio; canvas.height = window.innerHeight * devicePixelRatio; context.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0); }
    function draw(time) {
      const width = window.innerWidth, height = window.innerHeight;
      context.clearRect(0, 0, width, height);
      const horizon = height * .62;
      context.lineWidth = 1;
      for (let i = 1; i < 18; i++) {
        const y = horizon + ((i / 18) ** 2) * height * .48;
        context.strokeStyle = `rgba(70, 155, 255, ${.04 + i * .006})`;
        context.beginPath(); context.moveTo(0, y); context.lineTo(width, y); context.stroke();
      }
      for (let x = -10; x <= 10; x++) {
        context.strokeStyle = 'rgba(70, 155, 255, .13)';
        context.beginPath(); context.moveTo(width / 2, horizon); context.lineTo(width / 2 + x * width * .16, height); context.stroke();
      }
      particles.forEach(particle => {
        particle.y -= particle.speed * (reducedMotion ? 0 : 1);
        if (particle.y < 0) { particle.y = 1; particle.x = Math.random(); }
        const px = particle.x * width, py = particle.y * height;
        const radius = 1 + particle.z * 2;
        context.fillStyle = particle.z > .72 ? 'rgba(173,198,255,.8)' : 'rgba(77,142,255,.45)';
        context.beginPath(); context.arc(px, py, radius, 0, Math.PI * 2); context.fill();
      });
      const scanY = ((time * .00008) % 1) * height;
      context.fillStyle = 'rgba(85, 170, 255, .045)'; context.fillRect(0, scanY, width, 2);
      if (!reducedMotion) requestAnimationFrame(draw);
    }
    size(); window.addEventListener('resize', size); requestAnimationFrame(draw);
  }

  function addOperationsViews() {
    const main = document.querySelector('main');
    const nav = [...document.querySelectorAll('nav a')];
    const byLabel = label => nav.find(link => link.textContent.includes(label));
    const view = document.createElement('section');
    view.className = 'hidden fixed inset-0 left-[280px] top-[64px] z-40 overflow-y-auto bg-background/95 backdrop-blur-sm p-6';
    document.body.appendChild(view);

    function show(content) {
      view.innerHTML = `<div class="max-w-[1400px] mx-auto">${content}</div>`;
      view.classList.remove('hidden');
      main.classList.add('opacity-20', 'pointer-events-none');
      view.querySelector('[data-close]')?.addEventListener('click', close);
    }
    function close() {
      stopCamera();
      view.classList.add('hidden');
      main.classList.remove('opacity-20', 'pointer-events-none');
    }
    function header(title, description) {
      return `<div class="flex justify-between items-start mb-6"><div><h2 class="text-headline-lg font-bold">${title}</h2><p class="text-on-surface-variant mt-1">${description}</p></div><button data-close class="border border-primary/30 text-primary px-4 py-2 rounded-lg">Close</button></div>`;
    }

    byLabel('Incidents')?.addEventListener('click', async event => {
      event.preventDefault();
      show(`${header('Incident management', 'Create, review, and track active emergency incidents.')}
        <div class="grid lg:grid-cols-[360px_1fr] gap-6"><form id="incident-form" class="glass-panel rounded-xl p-5 space-y-4"><h3 class="font-title-md">Report incident</h3><input required name="type" placeholder="Incident type" class="w-full bg-surface-container-low border-0 rounded-lg p-3"><select required name="severity" class="w-full bg-surface-container-low border-0 rounded-lg p-3"><option value="critical">Critical</option><option value="warning">Warning</option><option value="elevated">Elevated</option><option value="info">Info</option></select><button class="w-full bg-primary-container text-on-primary-container font-bold py-3 rounded-lg">Create incident</button></form><div class="glass-panel rounded-xl overflow-x-auto"><table class="w-full text-left"><thead><tr class="border-b border-outline-variant/20"><th class="p-4">ID</th><th class="p-4">Type</th><th class="p-4">Severity</th><th class="p-4">Time</th><th class="p-4">Status</th></tr></thead><tbody id="incident-list"></tbody></table></div></div>`);
      const list = view.querySelector('#incident-list');
      const load = async () => {
        const result = await api('/incidents');
        list.innerHTML = result.incidents.map(i => `<tr class="border-b border-outline-variant/10"><td class="p-4 font-data-mono">${escapeHtml(i.id)}</td><td class="p-4">${escapeHtml(i.type)}</td><td class="p-4 uppercase text-primary">${escapeHtml(i.severity)}</td><td class="p-4">${escapeHtml(i.timestamp)}</td><td class="p-4">${escapeHtml(i.status)}</td></tr>`).join('');
      };
      await load();
      view.querySelector('#incident-form').addEventListener('submit', async e => {
        e.preventDefault();
        const form = new FormData(e.currentTarget);
        await api('/incidents', { method: 'POST', body: JSON.stringify(Object.fromEntries(form)) });
        e.currentTarget.reset(); await load(); refresh();
      });
    });

    byLabel('Surveillance')?.addEventListener('click', event => {
      event.preventDefault();
      show(`${header('Surveillance', 'Use this device camera for an authorized live monitoring feed.')}
        <div class="grid lg:grid-cols-2 gap-6"><div class="glass-panel rounded-xl p-5"><h3 class="font-title-md mb-3">Live camera feed</h3><video id="camera-feed" autoplay playsinline muted class="w-full aspect-video object-cover rounded-lg bg-black"></video><p id="camera-status" class="text-on-surface-variant mt-3">Camera is off.</p><div class="flex gap-3 mt-4"><button id="start-camera" class="bg-primary-container text-on-primary-container px-4 py-2 rounded-lg font-bold">Start camera</button><button id="capture-camera" class="border border-primary/30 text-primary px-4 py-2 rounded-lg">Capture frame</button></div></div><div class="glass-panel rounded-xl p-5"><h3 class="font-title-md mb-3">Mobile camera</h3><p class="text-on-surface-variant leading-relaxed">For your phone, open this dashboard using the computer’s LAN IP (not localhost), then select Start camera. Camera permission stays in the mobile browser tab.</p><canvas id="camera-capture" class="hidden w-full mt-4 rounded-lg"></canvas></div></div>`);
      view.querySelector('#start-camera').addEventListener('click', startCamera);
      view.querySelector('#capture-camera').addEventListener('click', captureCamera);
    });

    byLabel('Map')?.addEventListener('click', async event => {
      event.preventDefault();
      show(`${header('World incident map', 'Interactive OpenStreetMap view with current incident markers.')}
        <div class="glass-panel rounded-xl p-4"><div id="world-map" class="w-full h-[620px] rounded-lg overflow-hidden" aria-label="Interactive world map"></div><div class="flex gap-6 mt-4 text-sm"><span class="text-error">● Critical</span><span class="text-tertiary">● Warning</span><span class="text-primary">● Elevated</span></div></div>`);
      try {
        await loadLeaflet();
        const map = L.map('world-map', { worldCopyJump: true }).setView([20, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(map);
        const positions = [[40.7128, -74.006], [51.5072, -0.1276], [19.076, 72.8777], [-33.8688, 151.2093]];
        const response = await api('/incidents');
        response.incidents.forEach((incident, index) => {
          const point = positions[index % positions.length];
          const color = incident.severity === 'critical' ? '#ff5c5c' : incident.severity === 'warning' ? '#ffb786' : '#adc6ff';
          L.circleMarker(point, { radius: 9, color, fillColor: color, fillOpacity: .8, weight: 2 }).addTo(map).bindPopup(`<strong>${escapeHtml(incident.type)}</strong><br>${escapeHtml(incident.severity)} · ${escapeHtml(incident.status)}`);
        });
        setTimeout(() => map.invalidateSize(), 50);
      } catch (error) {
        view.querySelector('#world-map').innerHTML = `<p class="p-6 text-error">Map could not load. Check your internet connection and try again.</p>`;
        console.error(error);
      }
    });
  }

  function loadLeaflet() {
    if (window.L) return Promise.resolve();
    if (!document.querySelector('#leaflet-css')) {
      const css = document.createElement('link');
      css.id = 'leaflet-css'; css.rel = 'stylesheet';
      css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(css);
    }
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      script.onload = resolve; script.onerror = () => reject(new Error('Leaflet failed to load'));
      document.head.appendChild(script);
    });
  }

  let activeStream;
  async function startCamera() {
    const status = document.querySelector('#camera-status');
    try {
      activeStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' } }, audio: false });
      document.querySelector('#camera-feed').srcObject = activeStream;
      status.textContent = 'Live feed active. Camera access is limited to this browser tab.';
    } catch (error) {
      status.textContent = `Unable to start camera: ${error.message}`;
    }
  }
  function stopCamera() {
    activeStream?.getTracks().forEach(track => track.stop());
    activeStream = undefined;
  }
  function captureCamera() {
    const video = document.querySelector('#camera-feed');
    const canvas = document.querySelector('#camera-capture');
    if (!video?.videoWidth) return window.alert('Start the camera first.');
    canvas.width = video.videoWidth; canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    canvas.classList.remove('hidden');
  }
})();
