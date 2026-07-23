const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const PORT = Number(process.env.PORT || 3000);
const FRONTEND_FILE = process.env.FRONTEND_FILE || 'C:\\Program Files\\Notepad++\\RenenewdFronted.html';
const DB_FILE = path.join(__dirname, 'data.json');

const seed = {
  incidents: [
    { id: 'INC-1042', type: 'Structural Fire', severity: 'critical', timestamp: '14:24:02', status: 'active' },
    { id: 'INC-1041', type: 'Medical Emergency', severity: 'warning', timestamp: '14:18:55', status: 'active' },
    { id: 'INC-1040', type: 'Intrusion Alert', severity: 'elevated', timestamp: '13:55:10', status: 'active' },
    { id: 'INC-1039', type: 'Grid Flux', severity: 'info', timestamp: '13:42:30', status: 'resolved' }
  ],
  logs: [],
  deployments: []
};

function loadData() {
  try { return { ...seed, ...JSON.parse(fs.readFileSync(DB_FILE, 'utf8')) }; }
  catch { return structuredClone(seed); }
}
let data = loadData();

function saveData() {
  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

function send(res, status, payload, type = 'application/json; charset=utf-8') {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(typeof payload === 'string' ? payload : JSON.stringify(payload));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 1_000_000) reject(new Error('Request body is too large'));
    });
    req.on('end', () => {
      try { resolve(body ? JSON.parse(body) : {}); }
      catch { reject(new Error('Body must be valid JSON')); }
    });
  });
}

function timeNow() {
  return new Date().toLocaleTimeString('en-GB', { hour12: false });
}

function dashboard() {
  const active = data.incidents.filter(i => i.status === 'active');
  return {
    stats: {
      totalIncidents: data.incidents.length + 20,
      activeAlerts: active.length,
      resolved: 142 + data.incidents.filter(i => i.status === 'resolved').length,
      aiConfidence: 98.4
    },
    incidents: data.incidents.slice(0, 20),
    logs: data.logs.slice(-30)
  };
}

const clientScript = fs.readFileSync(path.join(__dirname, 'public', 'app.js'), 'utf8');

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  try {
    if (req.method === 'GET' && url.pathname === '/api/dashboard') return send(res, 200, dashboard());
    if (req.method === 'GET' && url.pathname === '/api/incidents') {
      const query = (url.searchParams.get('q') || '').toLowerCase();
      const incidents = query ? data.incidents.filter(i => `${i.id} ${i.type} ${i.severity}`.toLowerCase().includes(query)) : data.incidents;
      return send(res, 200, { incidents });
    }
    if (req.method === 'POST' && url.pathname === '/api/incidents') {
      const input = await readBody(req);
      if (!input.type || !input.severity) return send(res, 400, { error: 'type and severity are required' });
      const incident = { id: `INC-${1043 + data.incidents.length}`, type: String(input.type), severity: String(input.severity), timestamp: timeNow(), status: 'active' };
      data.incidents.unshift(incident);
      data.logs.push({ time: incident.timestamp, message: `New ${incident.severity} incident recorded: ${incident.type}` });
      saveData();
      return send(res, 201, { incident });
    }
    if (req.method === 'POST' && url.pathname === '/api/deployments') {
      const deployment = { id: `DEP-${Date.now()}`, deployedAt: new Date().toISOString(), status: 'dispatched' };
      data.deployments.unshift(deployment);
      data.logs.push({ time: timeNow(), message: 'Response deployment authorized and dispatched.' });
      saveData();
      return send(res, 201, { deployment });
    }
    if (req.method === 'POST' && url.pathname === '/api/ai/query') {
      const { query = '' } = await readBody(req);
      const reply = query.trim() ? `Command analysis received: ${query.trim()}. Monitor active incidents and confirm field-unit status.` : 'AI briefing: three active alerts require continued monitoring.';
      data.logs.push({ time: timeNow(), message: reply });
      saveData();
      return send(res, 200, { reply });
    }
    if (req.method === 'GET' && url.pathname === '/app.js') return send(res, 200, clientScript, 'application/javascript; charset=utf-8');
    if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
      const html = fs.readFileSync(FRONTEND_FILE, 'utf8').replace('</body>', '<script src="/app.js"></script></body>');
      return send(res, 200, html, 'text/html; charset=utf-8');
    }
    return send(res, 404, { error: 'Not found' });
  } catch (error) {
    console.error(error);
    return send(res, error.message === 'Body must be valid JSON' || error.message === 'Request body is too large' ? 400 : 500, { error: error.message || 'Server error' });
  }
});

server.listen(PORT, () => console.log(`GuardianX backend running at http://localhost:${PORT}`));
