const { chromium } = require('playwright');
const OUT = process.argv[2];
const jobs = [
 ['vnf','https://vietnamfinance.vn/da-nang-chot-bang-gia-dat-moi-co-noi-tang-manh-toi-70-d145539.html',['tăng từ 9% đến 70%','70%'],2],
 ['tt_bg','https://tuoitre.vn/nld/da-nang-thong-qua-bang-gia-dat-cac-dia-phuong-ven-bien-phia-nam-bien-dong-manh-196260530161513408.htm',['70%'],3],
 ['cafef','https://cafef.vn/nguon-cung-so-cap-can-ho-tai-da-nang-giam-14-trong-quy-iii-2026-188261025063317834.chn',['Ngũ Hành Sơn'],1],
 ['bdt','https://baodautu.vn/thi-truong-dat-nen-can-ho-da-nang-quy-iii2026-dong-tien-chon-loc-d729484.html',['chủ đầu tư uy tín'],1],
 ['tt_ifc','https://tuoitre.vn/da-nang-keu-goi-dau-tu-trung-tam-tai-chinh-quoc-te-tai-5-khu-dat-vang-20260313182451685.htm',['Võ Văn Kiệt'],2],
 ['dantri','https://dantri.com.vn/bat-dong-san/phat-trien-trung-tam-tai-chinh-quoc-te-viet-nam-tai-da-nang-quy-mo-300ha-20261022073313815.htm',['300 ha'],1],
 ['cafeland','https://cafeland.vn/tin-tuc/da-nang-duyet-khu-chuc-nang-3525-ty-dong-tai-khu-thuong-mai-tu-do-156021.html',['3.525'],1],
 ['tt_regal','https://tuoitre.vn/du-an-to-hop-2-toa-thap-regal-complex-1500-ti-o-da-nang-duoc-phep-mo-ban-100260626145723728.htm',['683'],3],
 ['palace','https://regalgroup.vn/news/cat-noc-dinh-thu-the-palace-bieu-tuong-song-thuong-luu-ben-song-co-co-dan-hien-huu/',['Low-E'],3],
 ['tcct','https://tapchicongthuong.vn/regal-group-ra-mat-bo-suu-tap-dinh-thu-doc-ban-the-palace-ben-song-267272.htm',['Studi8'],3],
];
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
