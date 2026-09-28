// scripts/build.js — production build for KYVOREX SOUNDS.
// Copies the site to dist/, minifies JS and CSS, verifies everything
// (HTML, JS, CSS, data, audio, root files) is present and valid.
// Fails the build if any required file is missing or malformed.
'use strict';

const fs = require('fs');
const path = require('path');
const esbuild = require('esbuild');

const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');

const SOUND_IDS = [
  'ui-click-001', 'ui-confirm-001', 'alert-error-001', 'alert-success-001',
  'coin-pickup-001', 'jump-001', 'hit-impact-001', 'explosion-small-001',
  'laser-shot-001', 'power-up-001'
];

const HTML_FILES = ['index.html', 'sounds.html', 'about.html', 'license.html', '404.html'];
const ROOT_FILES = ['robots.txt', 'sitemap.xml', '_headers'];
const DIRS_COPY = ['data', 'audio', 'assets'];

const JS_FILES = [
  'app.js', 'home.js', 'sounds.js', 'player.js', 'downloads.js',
  'filters.js', 'ui.js', 'audio-engine.js', 'audio-presets.js', 'wav-renderer.js'
];
const CSS_FILES = ['base.css', 'layout.css', 'components.css', 'responsive.css'];

const PLACEHOLDER = 'REPLACE-WITH-DOMAIN';
const MIN_WAV_BYTES = 100;   // header + at least a few samples
const MIN_MP3_BYTES = 100;   // non-empty MP3

function rmrf(p) {
  if (fs.rmSync) fs.rmSync(p, { recursive: true, force: true });
  else if (fs.existsSync(p)) fs.rmdirSync(p, { recursive: true });
}

function ensure(p) { fs.mkdirSync(p, { recursive: true }); }

function copyFile(src, dst) {
  ensure(path.dirname(dst));
  fs.copyFileSync(src, dst);
}

function copyDir(src, dst) {
  ensure(dst);
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else if (entry.isFile()) copyFile(s, d);
  }
}

async function minifyJS() {
  const entryPoints = JS_FILES
    .map(f => path.join(ROOT, 'js', f))
    .filter(f => fs.existsSync(f));
  if (!entryPoints.length) throw new Error('No JS files to build');
  await esbuild.build({
    entryPoints,
    outdir: path.join(DIST, 'js'),
    bundle: false,
    minify: true,
    sourcemap: false,
    legalComments: 'none',
    logLevel: 'warning'
  });
}

async function minifyCSS() {
  const entryPoints = CSS_FILES
    .map(f => path.join(ROOT, 'css', f))
    .filter(f => fs.existsSync(f));
  if (!entryPoints.length) throw new Error('No CSS files to build');
  await esbuild.build({
    entryPoints,
    outdir: path.join(DIST, 'css'),
    bundle: false,
    minify: true,
    sourcemap: false,
    legalComments: 'none',
    logLevel: 'warning'
  });
}

function fail(msg) {
  console.error('BUILD FAILED: ' + msg);
  process.exit(1);
}

/* ---------- WAV header validation ---------- */
function validateWav(filepath) {
  const size = fs.statSync(filepath).size;
  if (size < MIN_WAV_BYTES) return 'file too small (' + size + ' bytes)';

  const fd = fs.openSync(filepath, 'r');
  const buf = Buffer.alloc(44);
  const read = fs.readSync(fd, buf, 0, 44, 0);
  fs.closeSync(fd);
  if (read < 44) return 'cannot read 44-byte header';

  if (buf.toString('ascii', 0, 4) !== 'RIFF') return 'missing RIFF signature';
  if (buf.toString('ascii', 8, 12) !== 'WAVE') return 'missing WAVE signature';
  if (buf.toString('ascii', 12, 16) !== 'fmt ') return 'missing fmt chunk';

  const audioFormat = buf.readUInt16LE(20);
  const channels = buf.readUInt16LE(22);
  const sampleRate = buf.readUInt32LE(24);
  const bitsPerSample = buf.readUInt16LE(34);

  if (audioFormat !== 1) return 'not PCM (format=' + audioFormat + ')';
  if (channels !== 1) return 'not mono (channels=' + channels + ')';
  if (sampleRate !== 44100) return 'sample rate != 44100 (got ' + sampleRate + ')';
  if (bitsPerSample !== 16) return 'not 16-bit (got ' + bitsPerSample + ')';
  return null;
}

function validateMp3(filepath) {
  const size = fs.statSync(filepath).size;
  if (size < MIN_MP3_BYTES) return 'file too small (' + size + ' bytes)';
  return null;
}

function verify() {
  for (const f of HTML_FILES) {
    if (!fs.existsSync(path.join(DIST, f))) fail('missing ' + f);
  }
  for (const f of ROOT_FILES) {
    if (!fs.existsSync(path.join(DIST, f))) fail('missing ' + f);
  }
  for (const f of JS_FILES) {
    if (!fs.existsSync(path.join(DIST, 'js', f))) fail('missing js/' + f);
  }
  for (const f of CSS_FILES) {
    if (!fs.existsSync(path.join(DIST, 'css', f))) fail('missing css/' + f);
  }
  if (!fs.existsSync(path.join(DIST, 'data', 'sounds.json'))) {
    fail('missing data/sounds.json');
  }

  for (const id of SOUND_IDS) {
    const wav = path.join(DIST, 'audio', 'wav', id + '.wav');
    const mp3 = path.join(DIST, 'audio', 'mp3', id + '.mp3');

    if (!fs.existsSync(wav)) fail('missing audio/wav/' + id + '.wav');
    const wavErr = validateWav(wav);
    if (wavErr) fail('invalid WAV ' + id + '.wav: ' + wavErr);

    if (!fs.existsSync(mp3)) fail('missing audio/mp3/' + id + '.mp3');
    const mp3Err = validateMp3(mp3);
    if (mp3Err) fail('invalid MP3 ' + id + '.mp3: ' + mp3Err);
  }

  for (const sub of ['js', 'css']) {
    const dir = path.join(DIST, sub);
    for (const f of fs.readdirSync(dir)) {
      if (f.endsWith('.map')) fail('source map present: ' + sub + '/' + f);
    }
  }
}

function warnPlaceholders() {
  const filesToScan = HTML_FILES
    .map(f => path.join(DIST, f))
    .concat([path.join(DIST, 'robots.txt'), path.join(DIST, 'sitemap.xml')]);

  let found = false;
  for (const f of filesToScan) {
    if (!fs.existsSync(f)) continue;
    const content = fs.readFileSync(f, 'utf8');
    if (content.indexOf(PLACEHOLDER) !== -1) {
      console.warn('WARNING: placeholder "' + PLACEHOLDER + '" still present in ' +
        path.relative(ROOT, f) + ' — replace before publishing.');
      found = true;
    }
  }
  if (found) {
    console.warn('WARNING: the site is not ready for public publication until the ' +
      'placeholder domain is replaced in canonical/og:url/sitemap/robots.');
  }
}

async function main() {
  console.log('Building KYVOREX SOUNDS...');
  rmrf(DIST);
  ensure(DIST);

  for (const f of HTML_FILES) copyFile(path.join(ROOT, f), path.join(DIST, f));
  for (const f of ROOT_FILES) {
    const src = path.join(ROOT, f);
    if (fs.existsSync(src)) copyFile(src, path.join(DIST, f));
  }
  for (const d of DIRS_COPY) {
    const src = path.join(ROOT, d);
    if (fs.existsSync(src)) copyDir(src, path.join(DIST, d));
  }

  await minifyJS();
  await minifyCSS();
  verify();
  warnPlaceholders();

  console.log('Build OK -> ' + DIST);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});