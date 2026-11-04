const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const DIR = __dirname;
const mode = process.argv[2] || 'preview';
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 })).newPage();
  await p.goto('file://' + path.join(DIR, 'render.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800); await p.evaluate(()=>window.fit());
  fs.writeFileSync(path.join(DIR, 'sfx.json'), JSON.stringify(await p.evaluate(() => window.SFX_LIST)));
  if (mode === 'preview') {
    const ts = process.argv.slice(3).map(Number);
    fs.mkdirSync(path.join(DIR, 'prev'), { recursive: true });
    for (const t of ts) { await p.evaluate(t => window.render(t), t); await p.screenshot({ path: path.join(DIR, 'prev', `t${t.toFixed(2)}.jpg`), type: 'jpeg', quality: 80 }); }
  } else {
    const total = await p.evaluate(() => TL.total), fps = 30, N = Math.round(total * fps);
    const out = path.join(DIR, 'frames'); fs.mkdirSync(out, { recursive: true });
    const from = +(process.argv[3] || 0), to = Math.min(N, +(process.argv[4] || N));
    for (let f = from; f < to; f++) {
      await p.evaluate(t => window.render(t), f / fps);
      await p.screenshot({ path: path.join(out, `f${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 90 });
      if (f % 150 === 0) console.log('frame', f, '/', N);
    }
  }
  await b.close();
})();
