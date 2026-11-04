<script>
/* TDSC International city search + city banner (v1). Index: GeoNames cities >= 50k (CC BY 4.0). */
(function(){
var d=document,IDX=null,loading=null,URL_IDX='https://cdn.jsdelivr.net/gh/elijahbuffinv-sudo/tdsc-international@c43442900177/sq/assets/search-index.json';
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
function norm(s){return (s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9 ]+/g,' ').replace(/\s+/g,' ').trim()}
function load(){if(IDX)return Promise.resolve(IDX);if(loading)return loading;
 loading=fetch(URL_IDX).then(function(r){return r.json()}).then(function(j){
  j.n=j.t.map(function(c){return [norm(c[0]),norm(c[1])]});j.cn={};for(var k in j.c){j.cn[k]=norm(j.c[k][0])}
  IDX=j;return j});return loading}
function target(c,j){var hub=c[4];
 if(hub&&j.h[hub])return j.h[hub];
 var cj=j.c[j.t2[c[2]]||c[2]];
 if(cj&&cj[1])return cj[1]+'?city='+encodeURIComponent(c[0]);
 return '/international?city='+encodeURIComponent(c[0])}
function search(q,j){q=norm(q);if(q.length<2)return [];var out=[],i,n;
 for(var k in j.c){if(j.c[k][1]&&j.cn[k].indexOf(q)===0)out.push({s:3e9,label:j.c[k][0],sub:'Jurisdiction',href:j.c[k][1],hub:1})}
 for(i=0;i<j.t.length;i++){n=j.n[i];var c=j.t[i],sc=-1;
  if(n[0]===q||n[1]===q)sc=2e9;else if(n[0].indexOf(q)===0||n[1].indexOf(q)===0)sc=1e9;else if(q.length>3&&n[0].indexOf(' '+q)>-1)sc=0;
  if(sc>-1)out.push({s:sc+c[3],label:c[0],sub:(j.c[c[2]]?j.c[c[2]][0]:c[2]),href:target(c,j),hub:!!(c[4]&&j.h[c[4]])})}
 out.sort(function(a,b){return b.s-a.s});return out.slice(0,9)}
function wire(box){var inp=box.querySelector('input'),ul=box.querySelector('.v-results'),sel=-1,res=[];
 function close(){ul.hidden=true;inp.setAttribute('aria-expanded','false');sel=-1}
 function draw(){ul.innerHTML='';res.forEach(function(r,i){var li=d.createElement('li'),a=d.createElement('a');a.href=r.href;a.setAttribute('role','option');a.id=inp.id+'-o'+i;
   if(r.hub)a.className='v-hub';a.appendChild(d.createTextNode(r.label));var s=d.createElement('span');s.textContent=r.sub;a.appendChild(s);li.appendChild(a);ul.appendChild(li)});
  if(!res.length&&inp.value.trim().length>1){var li=d.createElement('li'),a=d.createElement('a');a.href='/international';a.textContent='No city of 50,000+ found \u2014 browse jurisdictions';li.appendChild(a);ul.appendChild(li)}
  ul.hidden=!ul.children.length;inp.setAttribute('aria-expanded',ul.hidden?'false':'true')}
 function mark(){[].forEach.call(ul.querySelectorAll('a'),function(a,i){a.setAttribute('aria-selected',i===sel?'true':'false')});if(sel>-1)inp.setAttribute('aria-activedescendant',inp.id+'-o'+sel)}
 inp.addEventListener('focus',load);
 inp.addEventListener('input',function(){var v=inp.value;load().then(function(j){if(inp.value!==v)return;res=search(v,j);sel=-1;draw()})});
 inp.addEventListener('keydown',function(ev){if(ev.key==='ArrowDown'){sel=Math.min(sel+1,res.length-1);mark();ev.preventDefault()}
  else if(ev.key==='ArrowUp'){sel=Math.max(sel-1,0);mark();ev.preventDefault()}
  else if(ev.key==='Enter'){var r=res[sel>-1?sel:0];if(r){location.href=r.href;ev.preventDefault()}}
  else if(ev.key==='Escape'){close()}});
 d.addEventListener('click',function(ev){if(!box.contains(ev.target))close()})}
ready(function(){
 d.querySelectorAll('[data-search]').forEach(wire);
 var qs=new URLSearchParams(location.search),city=qs.get('city'),bar=d.querySelector('[data-citybar]');
 if(city&&bar){city=city.slice(0,80);var w=bar.firstElementChild,b=d.createElement('b');b.textContent=city;
  w.appendChild(d.createTextNode('Matters involving '));w.appendChild(b);
  w.appendChild(d.createTextNode(/^\/international\/?$/.test(location.pathname)?': a dedicated profile for this jurisdiction is in research. Contact TDSC to discuss the matter directly.':' are scoped under the jurisdictional framework set out on this page.'));
  bar.hidden=false}
});
})();
</script>