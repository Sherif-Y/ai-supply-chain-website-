// Captures recorder.html frame by frame (deterministic render(t)) into PNGs using Chrome's DevTools Protocol.
// Usage: node linkedin/capture.mjs <framesDir> [fps]
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { pathToFileURL, fileURLToPath } from 'node:url';
import path from 'node:path';

const outDir = process.argv[2];
const fps = Number(process.argv[3] || 30);
mkdirSync(outDir, { recursive: true });
const page = pathToFileURL(path.join(path.dirname(fileURLToPath(import.meta.url)), 'recorder.html')).href + '?record';
const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const port = 9400 + Math.floor(Math.random() * 400);
setTimeout(() => { console.error('capture timed out'); try { chrome.kill(); } catch {} process.exit(1); }, 480000).unref();
const chrome = spawn(chromePath, ['--headless=new', `--remote-debugging-port=${port}`, '--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=1080,1080', `--user-data-dir=${outDir}/.profile`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let targets;
for (let i = 0; i < 50; i++) { try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0; const pending = new Map();
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expr) => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;

await send('Emulation.setDeviceMetricsOverride', { width: 1080, height: 1080, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: page });
for (let i = 0; i < 100 && !(await evaluate('window.ready === true')); i++) await sleep(150);
const duration = await evaluate('window.DURATION');
const frames = Math.round(duration * fps);
for (let f = 0; f < frames; f++) {
  await evaluate(`render(${f / fps}); new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))`);
  const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: 1080, height: 1080, scale: 1 } });
  writeFileSync(path.join(outDir, `f${String(f).padStart(5, '0')}.png`), Buffer.from(shot.result.data, 'base64'));
  if (f % 150 === 0) console.log(`frame ${f}/${frames}`);
}
ws.close(); chrome.kill();
console.log(`captured ${frames} frames at ${fps} fps`);
