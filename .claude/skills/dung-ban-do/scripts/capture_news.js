// Cắt ảnh bài báo để làm "báo chứng" trong video.
//   node capture_news.js <news.json> <outDir>
// news.json: [{"id":"cafef","url":"https://...","keys":["Ngũ Hành Sơn","40%"],"nimg":1,"tag":"CAFEF · 25/10/2026"}]
// Tạo cho mỗi bài:
//   <id>_head.png   tiêu đề + ngày + sapo (dùng làm thẻ báo trượt vào)
//   <id>_quote.png  đoạn chứa từ khoá đầu tiên tìm thấy, được tô vàng + nền vàng nhạt
//   <id>_img0..N.png  ảnh lớn trong bài (chỉ dùng làm nền demo, xem ghi chú bản quyền)
// Luôn kiểm tra lại bằng mắt: một số trang có h1 là logo (head hỏng) hoặc quảng cáo đè lên ảnh -> cắt lại thủ công bằng PIL.
const { chromium } = require('playwright');
const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')).map(j => [j.id, j.url, j.keys || [], j.nimg ?? 1]);
const OUT = process.argv[3]; fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  for (const [id,url,keys,nimg] of jobs) {
    const ctx = await b.newContext({ viewport:{width:1000,height:1400}, deviceScaleFactor:2, locale:'vi-VN' });
    const p = await ctx.newPage();
    try {
      await p.goto(url,{waitUntil:'domcontentloaded',timeout:45000}); await p.waitForTimeout(3000);
      await p.evaluate(()=>{for(const el of document.querySelectorAll('body *')){const s=getComputedStyle(el);if(s.position==='fixed'||s.position==='sticky')el.style.setProperty('display','none','important');}document.querySelectorAll('iframe,ins,[class*="banner"],[class*="ads"],[id*="ads"]').forEach(e=>e.style.setProperty('display','none','important'));});
      const box = await p.evaluate(()=>{const h=[...document.querySelectorAll('h1')].find(e=>e.innerText.trim().length>20); if(!h) return null;
        h.scrollIntoView({block:'center'}); const r=h.getBoundingClientRect();
        let bottom=r.bottom; const cands=[...document.querySelectorAll('h2,p,div')].filter(e=>{const q=e.getBoundingClientRect();return q.top>=r.bottom-2&&q.top<r.bottom+260&&e.innerText&&e.innerText.trim().length>80&&q.height<420&&q.left>=r.left-40});
        if(cands.length){ bottom=cands[0].getBoundingClientRect().bottom; }
        const sy=window.scrollY; const x=Math.max(0,r.left-28);
        return {x, y:r.top-70+sy, w:Math.min(r.width+56,1000-x), h:Math.min(bottom-r.top+100,900)};});
      if(box){ await p.screenshot({path:`${OUT}/${id}_head.png`, clip:{x:box.x,y:box.y,width:box.w,height:box.h}, fullPage:true}); }
      const q = await p.evaluate((keys)=>{const ps=[...document.querySelectorAll('p,h2')].filter(x=>x.innerText&&x.innerText.length>60&&x.getBoundingClientRect().width>300);
        for(const k of keys){const t=ps.find(x=>x.innerText.includes(k)); if(t){
          const esc=k.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
          t.innerHTML=t.innerHTML.replace(new RegExp(esc,'g'),'<mark style="background:#ffe600;color:#000;padding:0 4px;border-radius:3px">'+k+'</mark>');
          t.style.background='#fff8c4'; t.style.padding='14px'; t.scrollIntoView({block:'center'}); const r=t.getBoundingClientRect(); const sy=window.scrollY; const x=Math.max(0,r.left-24);
          return {x,y:r.top-24+sy,w:Math.min(r.width+48,1000-x),h:Math.min(r.height+48,700)};}} return null;},keys);
      if(q){ await p.screenshot({path:`${OUT}/${id}_quote.png`, clip:{x:q.x,y:q.y,width:q.w,height:q.h}, fullPage:true}); }
      const imgs = await p.$$('img');
      let n=0; const seen=new Set();
      for (const im of imgs) { if(n>=nimg) break;
        try{
          const pre = await im.evaluate(e=>{const r=e.getBoundingClientRect();return r.width>=450 && !/logo|banner|ads|qc/i.test((e.src||'')+e.className);});
          if(!pre) continue;
          await im.scrollIntoViewIfNeeded({timeout:2000}); await p.waitForTimeout(800);
          const ok = await im.evaluate(e=>{const r=e.getBoundingClientRect();return e.complete&&e.naturalWidth>=700&&r.height>=250?e.currentSrc||e.src:null;});
          if(ok && !seen.has(ok)){ seen.add(ok); await im.screenshot({path:`${OUT}/${id}_img${n}.png`}); n++; } }catch(e){}
      }
      console.log('OK',id,!!box,!!q,n);
    } catch(e){ console.log('FAIL',id,e.message.split('\n')[0]); }
    await ctx.close();
  }
  await b.close();
})();
