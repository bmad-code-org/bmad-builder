#!/usr/bin/env node
// Render an .excalidraw file to PNG via headless Chromium.
// Usage: node excalidraw_to_png.mjs <input.excalidraw> <output.png> [scale]

import { chromium } from 'playwright';
import { readFileSync, writeFileSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const [, , inPathArg, outPathArg, scaleArg] = process.argv;
if (!inPathArg || !outPathArg) {
  console.error('usage: excalidraw_to_png.mjs <input.excalidraw> <output.png> [scale]');
  process.exit(2);
}
const inPath = resolve(inPathArg);
const outPath = resolve(outPathArg);
const scale = parseFloat(scaleArg || '2');
statSync(inPath);

const sceneJson = JSON.parse(readFileSync(inPath, 'utf-8'));

const htmlPath = resolve(fileURLToPath(import.meta.url), '..', 'excalidraw_render.html');
const htmlUrl = pathToFileURL(htmlPath).href;

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 2400, height: 1800 } });
const page = await ctx.newPage();
page.on('console', (msg) => {
  const t = msg.type();
  if (t === 'error' || t === 'warning') console.error(`[browser:${t}]`, msg.text());
});
page.on('pageerror', (err) => console.error('[pageerror]', err.message));

await page.addInitScript(
  ({ scene, scale }) => {
    window.__scene = scene;
    window.__scale = scale;
  },
  { scene: sceneJson, scale },
);

console.error('loading:', htmlUrl);
await page.goto(htmlUrl, { waitUntil: 'domcontentloaded' });

await page.waitForFunction(() => window.__done === true, { timeout: 90_000 });

const err = await page.evaluate(() => window.__error);
if (err) {
  console.error('render error:', err);
  await browser.close();
  process.exit(1);
}

const dataUrl = await page.evaluate(() => window.__pngDataUrl);
if (!dataUrl || !dataUrl.startsWith('data:image/png;base64,')) {
  console.error('no png produced; got:', String(dataUrl).slice(0, 64));
  await browser.close();
  process.exit(1);
}

const b64 = dataUrl.split(',', 2)[1];
writeFileSync(outPath, Buffer.from(b64, 'base64'));
const { size } = statSync(outPath);
console.error(`wrote ${outPath} (${size.toLocaleString()} bytes)`);

await browser.close();
