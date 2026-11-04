// Paste into the Squarespace admin tab (config/pages/code-injection) via javascript_tool.
// Creates the hidden file input (aria-label "tdsc loader") and window.TDSC page upserter.
let i=document.querySelector('input[aria-label="tdsc loader"]'); if(!i){i=document.createElement('input');i.type='file';i.multiple=true;i.setAttribute('aria-label','tdsc loader');i.style.cssText='position:fixed;top:0;left:0;width:20px;height:20px;opacity:0.01;z-index:99999';document.body.appendChild(i);}
window.__files=window.__files||{}; i.onchange=async()=>{for(const f of i.files){window.__files[f.name]=await f.text()}};
window.TDSC={
 crumb(){return (document.cookie.match(/crumb=([^;]+)/)||[])[1]},
 H(){return {'X-CSRF-Token':this.crumb(),'Accept':'application/json','Content-Type':'application/json'}},
 async cols(){const j=await (await fetch('/api/commondata/GetCollections')).json(); return Object.values(j.collections)},
 async copy(src){const r=await fetch('/api/content/copy/collection?sourceId='+src,{method:'POST',headers:this.H()}); if(!r.ok) throw 'copy '+r.status; return r.json()},
 async setHtml(id,h){const pg=await (await fetch('/api/pages/by-collection-id/'+id,{headers:this.H()})).json(); let f=null; JSON.stringify(pg,(k,v)=>{if(v&&typeof v==='object'&&v.value&&v.value.wysiwyg&&!f)f=v;return v}); if(!f) throw 'no code block '+id; f.value.html=h; f.value.wysiwyg.source=h; const r=await fetch('/api/pages/by-collection-id/'+id,{method:'PUT',headers:this.H(),body:JSON.stringify(pg)}); if(!r.ok) throw 'put '+r.status},
 async settings(c,m){const keep=['id','websiteId','backgroundSource','enabled','starred','type','ordering','title','navigationTitle','urlId','itemCount','deleted','updatedOn','description','folder','dropdown','homepage','typeName','regionName','synchronizing','iTunesEnabled','seoData','revalidateBefore','categoryPagesSeoHidden','tagPagesSeoHidden','headerFooterVisibilitySettings','qrCodeEnabled','pagePermissionType','typeLabel','fullUrl','passwordProtected','draft','password'];
  const cd={}; keep.forEach(k=>{if(k in c)cd[k]=c[k]}); cd.collectionId=c.id; cd.enabled=true; cd.title=m.nav; cd.navigationTitle=m.nav; cd.urlId=m.path.replace(/^\//,''); cd.fullUrl=m.path; cd.seoData={seoTitle:m.title,seoDescription:m.desc,seoHidden:false}; cd.password=''; cd.passwordProtected=false; cd.draft=false;
  const r=await fetch('/api/commondata/SaveCollectionSettings',{method:'POST',headers:this.H(),body:JSON.stringify({collectionData:cd,memberAreaData:{}})}); if(!r.ok) throw 'settings '+r.status},
 async run(keys,template){window.__prog={done:[],err:[],running:true}; const man=JSON.parse(window.__files['manifest.json']); const by={}; (await this.cols()).forEach(c=>by[c.urlId]=c);
  for(const m of man){ if(keys&&!keys.includes(m.key)) continue; try{ const h=window.__files[m.key+'.html']; if(!h) continue;
     let c=by[m.path.replace(/^\//,'')]; if(!c){ c=await this.copy(template); }
     await this.setHtml(c.id,h); await this.settings(c,m); window.__prog.done.push(m.key);}catch(e){window.__prog.err.push(m.key+': '+e)} }
  window.__prog.running=false}
};
'loader ready';
