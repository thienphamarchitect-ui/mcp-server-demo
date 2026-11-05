// Chụp từng khung hình của <project>/render.html bằng Playwright.
//   node render.js <projectDir> preview 3.5 14.9 29.2   -> <project>/prev/t*.jpg
//   node render.js <projectDir> full [fromFrame] [toFrame] -> <project>/frames/f00000.jpg ...
// Luôn ghi <project>/sfx.json (danh sách cue SFX do render.html khai báo) để audio.py dùng.
// Render song song: chạy 3 tiến trình với các khoảng frame khác nhau.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(process.argv[2] || '.');
const mode = process.argv[3] || 'preview';
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 })).newPage();
  p.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await p.goto('file://' + path.join(DIR, 'render.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  await p.evaluate(() => window.fit && window.fit());
  fs.writeFileSync(path.join(DIR, 'sfx.json'), JSON.stringify(await p.evaluate(() => window.SFX_LIST)));
  if (mode === 'preview') {
    const ts = process.argv.slice(4).map(Number);
    fs.mkdirSync(path.join(DIR, 'prev'), { recursive: true });
    for (const t of ts) {
      await p.evaluate(t => window.render(t), t);
      await p.screenshot({ path: path.join(DIR, 'prev', `t${t.toFixed(2)}.jpg`), type: 'jpeg', quality: 80 });
    }
  } else {
    const total = await p.evaluate(() => TL.total), fps = await p.evaluate(() => TL.fps || 30), N = Math.round(total * fps);
    const out = path.join(DIR, 'frames'); fs.mkdirSync(out, { recursive: true });
    const from = +(process.argv[4] || 0), to = Math.min(N, +(process.argv[5] || N));
    for (let f = from; f < to; f++) {
      await p.evaluate(t => window.render(t), f / fps);
      await p.screenshot({ path: path.join(out, `f${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 90 });
      if (f % 150 === 0) console.log('frame', f, '/', N);
    }
  }
  await b.close();
})();
