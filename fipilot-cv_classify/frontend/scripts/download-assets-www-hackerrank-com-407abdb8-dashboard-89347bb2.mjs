import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const ASSET_ROOT = `${ROOT}public/sites/www.hackerrank.com-407abdb8/shared`;
const PAGE_ROOT = `${ROOT}public/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2`;

const FONT_BASE = 'https://cdn.hackerrank.com/fonts/satoshi/fonts';
const ICON_BASE = 'https://hrcdn.net/s3_pub/hr-assets/dashboard';

const assets = [
  [`${FONT_BASE}/Satoshi-Regular.woff2`, `${ASSET_ROOT}/fonts/Satoshi-Regular.woff2`],
  [`${FONT_BASE}/Satoshi-Medium.woff2`, `${ASSET_ROOT}/fonts/Satoshi-Medium.woff2`],
  [`${FONT_BASE}/Satoshi-Bold.woff2`, `${ASSET_ROOT}/fonts/Satoshi-Bold.woff2`],
  [`${FONT_BASE}/Satoshi-Italic.woff2`, `${ASSET_ROOT}/fonts/Satoshi-Italic.woff2`],
  [`${FONT_BASE}/Satoshi-MediumItalic.woff2`, `${ASSET_ROOT}/fonts/Satoshi-MediumItalic.woff2`],
  [`${FONT_BASE}/Satoshi-BoldItalic.woff2`, `${ASSET_ROOT}/fonts/Satoshi-BoldItalic.woff2`],
  ['https://hrcdn.net/hrc/_next/static/next_assets/brand/logo-light.svg', `${PAGE_ROOT}/logo-light.svg`],
  ['https://hrcdn.net/hrc/_next/static/next_assets/brand/favicon.png', `${PAGE_ROOT}/favicon.png`],
  ['https://hrcdn.net/og/default.jpg', `${PAGE_ROOT}/og-default.jpg`],
  [`${ICON_BASE}/Algorithm.svg`, `${PAGE_ROOT}/icons/Algorithm.svg`],
  [`${ICON_BASE}/DataStructure.svg`, `${PAGE_ROOT}/icons/DataStructure.svg`],
  [`${ICON_BASE}/Mathematics.svg`, `${PAGE_ROOT}/icons/Mathematics.svg`],
  [`${ICON_BASE}/AI.svg`, `${PAGE_ROOT}/icons/AI.svg`],
  [`${ICON_BASE}/C.svg`, `${PAGE_ROOT}/icons/C.svg`],
  [`${ICON_BASE}/C++.svg`, `${PAGE_ROOT}/icons/C++.svg`],
  [`${ICON_BASE}/Java.svg`, `${PAGE_ROOT}/icons/Java.svg`],
  [`${ICON_BASE}/Python.svg`, `${PAGE_ROOT}/icons/Python.svg`],
  [`${ICON_BASE}/Ruby.svg`, `${PAGE_ROOT}/icons/Ruby.svg`],
  [`${ICON_BASE}/SQL.svg`, `${PAGE_ROOT}/icons/SQL.svg`],
  [`${ICON_BASE}/DataBase.svg`, `${PAGE_ROOT}/icons/DataBase.svg`],
  [`${ICON_BASE}/LinuxShell.svg`, `${PAGE_ROOT}/icons/LinuxShell.svg`],
  [`${ICON_BASE}/FunctionalProgramming.svg`, `${PAGE_ROOT}/icons/FunctionalProgramming.svg`],
  [`${ICON_BASE}/regex.svg`, `${PAGE_ROOT}/icons/regex.svg`],
  ['https://hr-assets.s3.amazonaws.com/jobs/react.svg', `${PAGE_ROOT}/icons/react.svg`],
];

async function download(url, dest) {
  await mkdir(dirname(dest), { recursive: true });
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  const buf = Buffer.from(await res.arrayBuffer());
  await writeFile(dest, buf);
  return buf.length;
}

let ok = 0;
let fail = 0;
const queue = [...assets];
async function worker() {
  while (queue.length) {
    const [url, dest] = queue.shift();
    try {
      const bytes = await download(url, dest);
      console.log(`OK ${bytes} ${url.split('/').pop()} -> ${dest}`);
      ok++;
    } catch (e) {
      console.error(`FAIL ${url}: ${e.message}`);
      fail++;
    }
  }
}
await Promise.all(Array.from({ length: 4 }, worker));
console.log(`\nDone: ${ok} ok, ${fail} failed`);
process.exit(fail ? 1 : 0);