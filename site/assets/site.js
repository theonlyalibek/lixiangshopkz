(function(){
var $=function(s){return document.querySelector(s)};
var WA=document.body.getAttribute('data-wa');
function wa(t){return 'https://wa.me/'+WA+'?text='+encodeURIComponent(t)}
function store(k,v){try{if(v===undefined)return sessionStorage.getItem(k);sessionStorage.setItem(k,v)}catch(e){return null}}

/* intro: home only, once per visit */
var intro=$('#intro');
function ready(){document.body.classList.add('ready')}
if(intro){
  var hero=$('.hero img');
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(store('introSeen')){intro.remove();ready()}
  else{
    var MIN=reduce?300:3000,MAX=7000,t0=performance.now(),done=false;
    document.documentElement.style.overflow='hidden';
    var finish=function(){if(done)return;done=true;store('introSeen','1');intro.classList.add('gone');document.documentElement.style.overflow='';ready();setTimeout(function(){intro.remove()},1200)};
    var tick=function(){if(done)return;var t=performance.now()-t0;if((t>=MIN&&(!hero||hero.complete))||t>=MAX)finish();else requestAnimationFrame(tick)};
    $('#skip').addEventListener('click',finish);requestAnimationFrame(tick);
  }
}else ready();

/* header on home */
var top_=$('#top');
if(document.body.classList.contains('home')){
  addEventListener('scroll',function(){top_.classList.toggle('solid',scrollY>40)},{passive:true});
  var cta=$('#heroCta'),fab=$('#fab');
  if(cta&&'IntersectionObserver' in window)new IntersectionObserver(function(e){fab.classList.toggle('show',!e[0].isIntersecting)}).observe(cta);
}

/* menu */
var menu=$('#menu'),mb=$('#menuBtn');
function setMenu(o){menu.classList.toggle('open',o);menu.setAttribute('aria-hidden',!o);mb.setAttribute('aria-expanded',o);document.documentElement.style.overflow=o?'hidden':'';top_.classList.toggle('solid',o||scrollY>40||!document.body.classList.contains('home'))}
if(mb){mb.addEventListener('click',function(){setMenu(!menu.classList.contains('open'))});
  menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setMenu(false)})});
  addEventListener('keydown',function(e){if(e.key==='Escape')setMenu(false)})}

/* WhatsApp mini form: model, part or symptom, optional VIN */
document.querySelectorAll('[data-waf]').forEach(function(f){
  var vin=f.querySelector('[name=vin]'),need=f.querySelector('[name=need]'),err=f.querySelector('.err'),cnt=f.querySelector('.cnt');
  var pre=f.getAttribute('data-m');if(!pre){try{pre=localStorage.getItem('myLi')}catch(e){}}
  if(pre){var r=f.querySelector('input[name=m][value="'+pre+'"]');if(r)r.checked=true}
  vin.addEventListener('input',function(){var v=vin.value.toUpperCase().replace(/[^A-Z0-9]/g,'').replace(/[OQ]/g,'0').replace(/I/g,'1').slice(0,17);
    if(vin.value!==v)vin.value=v;cnt.textContent=v.length+'/17';err.textContent=''});
  need.addEventListener('input',function(){err.textContent=''});
  f.addEventListener('submit',function(e){e.preventDefault();
    var m=f.querySelector('input[name=m]:checked'),v=vin.value,n=need.value.trim();
    if(v&&!/^[A-HJ-NPR-Z0-9]{17}$/.test(v)){err.textContent='В VIN 17 символов, сейчас '+v.length;vin.focus();return}
    if(!n&&!v){err.textContent='Напишите деталь или симптом, или добавьте VIN';need.focus();return}
    var t='Здравствуйте!'+(m?' Li L'+m.value+'.':'')+(n?' Нужно: '+n.replace(/[.\s]+$/,'')+'.':'')+(v?' VIN: '+v+'.':'');
    var a=document.createElement('a');a.href=wa(t);a.target='_blank';a.rel='noopener';document.body.appendChild(a);a.click();a.remove()});
});

/* catalog search */
var q=$('#q'),res=$('#results');
if(q&&window.SEARCH){
  var base=location.pathname.indexOf('.html')>-1?'zapchasti/':'/zapchasti/';
  var suffix=location.pathname.indexOf('.html')>-1?'.html':'/';
  var esc=function(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  q.addEventListener('input',function(){
    var t=q.value.trim().toLowerCase(),tn=t.replace(/[\s-]/g,'');
    if(t.length<2){res.hidden=true;res.innerHTML='';return}
    var hits=window.SEARCH.filter(function(r){return r[0].toLowerCase().indexOf(t)>-1||(tn&&r[1].toLowerCase().replace(/[\s-]/g,'').indexOf(tn)>-1)||r[4].toLowerCase().indexOf(t)>-1}).slice(0,30);
    res.hidden=false;
    res.innerHTML=hits.length?hits.map(function(r){var ms=r[2]?r[2].split('').map(function(d){return 'L'+d}).join(', '):'по VIN';
      return '<li><a href="'+base+r[3]+suffix+'"><span>'+esc(r[0])+'</span><small>'+ms+'</small>'+(r[1]?'<code>'+esc(r[1])+'</code>':'')+'</a></li>'}).join('')
      :'<li class="empty">Не нашли. Пришлите фото детали или VIN в WhatsApp.</li>';
  });
}
/* my Li: remember the owner's model */
(function(){
  var KEY='myLi',MS=['6','7','8','9'];
  function get(){try{return localStorage.getItem(KEY)}catch(e){return null}}
  function set(v){try{v?localStorage.setItem(KEY,v):localStorage.removeItem(KEY)}catch(e){}}
  var links={};try{links=JSON.parse(document.body.getAttribute('data-models')||'{}')}catch(e){}
  function plural(n,a,b,c){var n1=n%10,n2=n%100;return n1==1&&n2!=11?a:n1>=2&&n1<=4&&!(n2>=12&&n2<=14)?b:c}
  function apply(){
    var m=get();
    document.body.classList.toggle('has-myli',!!m);
    var chip=document.getElementById('mychip');
    if(chip){chip.textContent=m?'Li L'+m:'Li';chip.href=m&&links[m]?links[m]:'#';chip.setAttribute('aria-label',m?'Моя машина: Li L'+m:'')}
    document.querySelectorAll('[data-myli]').forEach(function(box){
      box.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-v')===m)})});
    document.querySelectorAll('.car[data-m],.mod[data-m]').forEach(function(c){c.classList.toggle('on',c.getAttribute('data-m')===m)});
    var rows=document.querySelectorAll('.plist li[data-m], .tbl tr[data-m], .prow li[data-m]'),fit=document.getElementById('fit'),hit=0,tot=0;
    rows.forEach(function(r){var ok=!m||r.getAttribute('data-m').indexOf(m)>-1;tot++;if(m&&ok)hit++;
      r.classList.toggle('off',!!m&&!ok);if(r.tagName==='TR'||r.parentNode.classList.contains('prow'))r.classList.toggle('me',!!m&&ok)});
    document.querySelectorAll('[data-fitm]').forEach(function(f){var fm=f.getAttribute('data-fitm');if(!f.hasAttribute('data-t0'))f.setAttribute('data-t0',f.textContent);
      f.classList.toggle('no',!!m&&fm.indexOf(m)<0);f.classList.toggle('yes',!!m&&fm.indexOf(m)>-1);
      f.textContent=!m?f.getAttribute('data-t0'):fm.indexOf(m)>-1?'Подходит для вашей L'+m:'Для вашей L'+m+' другой номер, смотрите ниже'});
    /* matching rows first, original order otherwise */
    document.querySelectorAll('.prow, .plist, .tbl tbody').forEach(function(list){
      var items=[].filter.call(list.children,function(x){return x.hasAttribute('data-m')});if(items.length<2)return;
      var ref=items[items.length-1].nextSibling;
      items.forEach(function(x,i){if(!x.hasAttribute('data-i'))x.setAttribute('data-i',i)});
      items.sort(function(a,b){var fa=m&&a.getAttribute('data-m').indexOf(m)>-1?0:1,fb=m&&b.getAttribute('data-m').indexOf(m)>-1?0:1;return (fa-fb)||(a.getAttribute('data-i')-b.getAttribute('data-i'))});
      items.forEach(function(x){list.insertBefore(x,ref)})});
    if(fit){fit.textContent=!m?'':fit.getAttribute('data-scope')==='part'
      ?(hit?'Для вашей L'+m+': '+hit+' из '+tot+' '+plural(tot,'позиции','позиций','позиций')+'.':'Для L'+m+' в каталоге нет. Уточним по VIN.')
      :'Показываем детали для L'+m+'.'}
    document.querySelectorAll('a[href^="https://wa.me/"]').forEach(function(a){
      var u=a.getAttribute('data-wa0')||a.href;a.setAttribute('data-wa0',u);
      if(!m){a.href=u;return}
      var q=u.split('?text=');if(q.length<2){a.href=u;return}
      var t=decodeURIComponent(q[1]);if(t.indexOf('Li L'+m)<0)t=t.replace(/\s*$/,'')+' Моя машина: Li L'+m+'.';
      a.href=q[0]+'?text='+encodeURIComponent(t)});
  }
  document.querySelectorAll('[data-myli]').forEach(function(box){
    var pick=box.getAttribute('data-pick');
    box.innerHTML='<span>'+(pick?'Это ваша машина?':'Моя Li:')+'</span>'+(pick?[pick]:MS).map(function(v){return '<button type="button" data-v="'+v+'">'+(pick?'Да, моя L'+v:'L'+v)+'</button>'}).join('');
    box.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var v=b.getAttribute('data-v');set(get()===v?null:v);apply()});
  });
  apply();
})();
/* model page: system sheet */
(function(){
  var sh=document.getElementById('sheet');if(!sh)return;
  var panel=sh.querySelector('.sheet-panel'),body=sh.querySelector('.sbody'),title=document.getElementById('sheetT'),img=sh.querySelector('.simg'),all=sh.querySelector('.sfoot [data-all]'),last=null;
  function open(id,from){var src=document.getElementById('src-'+id);if(!src)return;last=from;
    title.textContent=src.getAttribute('data-title');img.src=src.getAttribute('data-img');all.href=src.getAttribute('data-all');
    body.innerHTML=src.innerHTML;body.scrollTop=0;sh.style.setProperty('--drag','0px');
    sh.classList.add('open');sh.setAttribute('aria-hidden','false');document.documentElement.style.overflow='hidden';
    try{history.pushState({sheet:id},'')}catch(_){}setTimeout(function(){var b=sh.querySelector('.shead .ib');b&&b.focus({preventScroll:true})},60)}
  function close(fromPop){if(!sh.classList.contains('open'))return;sh.classList.remove('open');sh.setAttribute('aria-hidden','true');document.documentElement.style.overflow='';sh.style.setProperty('--drag','0px');
    try{if(!fromPop&&history.state&&history.state.sheet)history.back()}catch(_){}if(last)last.focus({preventScroll:true})}
  document.querySelectorAll('[data-sheet]').forEach(function(t){t.addEventListener('click',function(e){if(e.metaKey||e.ctrlKey)return;e.preventDefault();open(t.getAttribute('data-sheet'),t)})});
  sh.querySelectorAll('[data-close]').forEach(function(b){b.addEventListener('click',function(){close()})});
  addEventListener('keydown',function(e){if(e.key==='Escape')close()});
  addEventListener('popstate',function(){close(true)});
  var y0=null,dy=0;
  panel.addEventListener('touchstart',function(e){if(body.contains(e.target)&&body.scrollTop>0)return;y0=e.touches[0].clientY;dy=0},{passive:true});
  panel.addEventListener('touchmove',function(e){if(y0===null)return;dy=Math.max(0,e.touches[0].clientY-y0);if(dy>4){sh.classList.add('dragging');sh.style.setProperty('--drag',dy+'px')}},{passive:true});
  panel.addEventListener('touchend',function(){if(y0===null)return;sh.classList.remove('dragging');if(dy>90)close();else sh.style.setProperty('--drag','0px');y0=null;dy=0});
})();
/* open now: Almaty is UTC+5, open every day 09:30-19:00 */
(function(){
  var els=document.querySelectorAll('[data-open]');if(!els.length)return;
  function upd(){var d=new Date(),t=((d.getUTCHours()+5)%24)*60+d.getUTCMinutes(),o=t>=570&&t<1140;
    var s=o?'открыто до 19:00':t<570?'откроемся в 09:30':'откроемся завтра в 09:30';
    els.forEach(function(el){el.textContent=s;el.classList.toggle('is-open',o)})}
  upd();setInterval(upd,60000);
})();
/* cart: collect parts across pages, send one WhatsApp message */
(function(){
  var KEY='cart',X='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>',
      BAG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M5 8h14l-1 12H6L5 8Z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8" stroke-linecap="round"/></svg>',
      WAI='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg>';
  function load(){try{var c=JSON.parse(localStorage.getItem(KEY)||'[]');return Array.isArray(c)?c:[]}catch(e){return []}}
  function save(c){try{c.length?localStorage.setItem(KEY,JSON.stringify(c)):localStorage.removeItem(KEY)}catch(e){}}
  function myli(){try{return localStorage.getItem('myLi')}catch(e){return null}}
  function money(v){return String(v).replace(/\B(?=(\d{3})+(?!\d))/g,' ')+' ₸'}
  function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function plural(n,a,b,c){var n1=n%10,n2=n%100;return n1==1&&n2!=11?a:n1>=2&&n1<=4&&!(n2>=12&&n2<=14)?b:c}
  var cart=load(),ADD='.prow li[data-id] .pa, [data-id] [data-add]';

  var bar=document.createElement('div');bar.className='cbar';bar.hidden=true;
  bar.innerHTML='<button type="button" class="btn pri">'+BAG+'<span class="cb-t"></span><span class="cb-s"></span></button>';
  document.body.appendChild(bar);
  var sh=document.createElement('div');sh.className='sheet cart';sh.id='cart';sh.setAttribute('aria-hidden','true');sh.setAttribute('role','dialog');sh.setAttribute('aria-modal','true');sh.setAttribute('aria-labelledby','cartT');
  sh.innerHTML='<div class="sheet-bg" data-cx></div><div class="sheet-panel"><div class="grab"></div>'+
    '<div class="shead"><h2 id="cartT">Корзина</h2><div class="chd"><button type="button" class="cclr" data-clear>Очистить</button><button type="button" class="ib" data-cx aria-label="Закрыть">'+X+'</button></div></div>'+
    '<div class="sbody"><ul class="clist"></ul><p class="ctot"><span>Итого</span><b></b></p>'+
    '<label class="fld"><span>VIN <small>по желанию</small></span><input class="vinf" maxlength="17" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="17 символов из техпаспорта"></label>'+
    '<p class="err"></p><p class="snote">Наличие и итоговую цену подтверждаем по VIN.</p></div>'+
    '<div class="sfoot"><button type="button" class="btn pri" data-send>'+WAI+'Отправить в WhatsApp</button></div></div>';
  document.body.appendChild(sh);
  var list=sh.querySelector('.clist'),tot=sh.querySelector('.ctot b'),vin=sh.querySelector('.vinf'),err=sh.querySelector('.err'),panel=sh.querySelector('.sheet-panel'),body=sh.querySelector('.sbody');

  function count(){return cart.reduce(function(a,x){return a+x.q},0)}
  function sum(){return cart.reduce(function(a,x){return a+x.p*x.q},0)}
  function has(id){return cart.some(function(x){return x.id===id})}
  function render(){
    var n=count();
    document.body.classList.toggle('has-cart',n>0);bar.hidden=!n;
    bar.querySelector('.cb-t').textContent='Корзина · '+n+' '+plural(n,'деталь','детали','деталей');
    bar.querySelector('.cb-s').textContent=sum()?money(sum()):'';
    list.innerHTML=cart.map(function(x){return '<li data-id="'+x.id+'"><div><b>'+esc(x.n)+'</b><span>'+esc([x.l,x.o].filter(Boolean).join(' · '))+'</span></div>'+
      '<div class="cq"><button type="button" data-d="-1" aria-label="Меньше">−</button><output>'+x.q+'</output><button type="button" data-d="1" aria-label="Больше">+</button></div>'+
      '<em>'+(x.p?money(x.p*x.q):'по запросу')+'</em><button type="button" class="crm" data-rm aria-label="Убрать: '+esc(x.n)+'">'+X+'</button></li>'}).join('');
    tot.textContent=sum()?money(sum()):'—';
    document.querySelectorAll(ADD).forEach(function(a){var on=has(+a.closest('[data-id]').getAttribute('data-id'));
      if(!a.hasAttribute('data-t0'))a.setAttribute('data-t0',a.textContent);
      a.textContent=on?'✓ В корзине':a.getAttribute('data-t0');a.classList.toggle('in',on)});
  }
  function add(li){var id=+li.getAttribute('data-id');if(has(id))return;
    cart.push({id:id,n:li.getAttribute('data-n'),o:li.getAttribute('data-o'),l:li.getAttribute('data-l'),p:+li.getAttribute('data-p')||0,q:1});save(cart);render();
    bar.classList.remove('pop');void bar.offsetWidth;bar.classList.add('pop')}
  document.querySelectorAll(ADD).forEach(function(a){
    a.removeAttribute('target');a.setAttribute('role','button');
    a.addEventListener('click',function(e){e.preventDefault();var li=a.closest('[data-id]');if(has(+li.getAttribute('data-id')))open();else add(li)})});

  var last=null;
  function open(){last=document.activeElement;render();body.scrollTop=0;sh.style.setProperty('--drag','0px');sh.classList.add('open');sh.setAttribute('aria-hidden','false');document.documentElement.style.overflow='hidden';
    try{history.pushState({cart:1},'')}catch(_){}}
  function close(fromPop){if(!sh.classList.contains('open'))return;sh.classList.remove('open');sh.setAttribute('aria-hidden','true');document.documentElement.style.overflow='';
    try{if(!fromPop&&history.state&&history.state.cart)history.back()}catch(_){}if(last&&last.focus)last.focus({preventScroll:true})}
  bar.querySelector('button').addEventListener('click',open);
  sh.querySelectorAll('[data-cx]').forEach(function(b){b.addEventListener('click',function(){close()})});
  addEventListener('keydown',function(e){if(e.key==='Escape')close()});
  addEventListener('popstate',function(){close(true)});
  addEventListener('storage',function(e){if(e.key===KEY){cart=load();render()}});
  list.addEventListener('click',function(e){var li=e.target.closest('li');if(!li)return;var id=+li.getAttribute('data-id'),i=-1;
    cart.forEach(function(x,k){if(x.id===id)i=k});if(i<0)return;
    var d=e.target.closest('[data-d]');
    if(d){cart[i].q=Math.max(1,Math.min(20,cart[i].q+(+d.getAttribute('data-d'))))}
    else if(e.target.closest('[data-rm]'))cart.splice(i,1);
    else return;
    save(cart);render();if(!cart.length)close()});
  sh.querySelector('[data-clear]').addEventListener('click',function(){cart=[];save(cart);render();close()});
  vin.addEventListener('input',function(){var v=vin.value.toUpperCase().replace(/[^A-Z0-9]/g,'').replace(/[OQ]/g,'0').replace(/I/g,'1').slice(0,17);if(vin.value!==v)vin.value=v;err.textContent=''});
  sh.querySelector('[data-send]').addEventListener('click',function(){
    var v=vin.value;if(v&&!/^[A-HJ-NPR-Z0-9]{17}$/.test(v)){err.textContent='В VIN 17 символов, сейчас '+v.length;vin.focus();return}
    var m=myli(),t='Здравствуйте! Хочу заказать:\n'+cart.map(function(x,i){return (i+1)+'. '+x.n+(x.o?' ('+x.o+')':'')+(x.l?', '+x.l:'')+(x.q>1?', '+x.q+' шт.':'')+(x.p?' — '+money(x.p*x.q).replace(/ | /g,' '):'')}).join('\n')+
      (sum()?'\nИтого по сайту: '+money(sum()).replace(/ | /g,' '):'')+(m?'\nМоя машина: Li L'+m+'.':'')+(v?'\nVIN: '+v:'')+'\nЕсть в наличии?';
    var a=document.createElement('a');a.href='https://wa.me/'+document.body.getAttribute('data-wa')+'?text='+encodeURIComponent(t);a.target='_blank';a.rel='noopener';document.body.appendChild(a);a.click();a.remove()});
  var y0=null,dy=0;
  panel.addEventListener('touchstart',function(e){if(body.contains(e.target)&&body.scrollTop>0)return;if(e.target.closest('input,button'))return;y0=e.touches[0].clientY;dy=0},{passive:true});
  panel.addEventListener('touchmove',function(e){if(y0===null)return;dy=Math.max(0,e.touches[0].clientY-y0);if(dy>4){sh.classList.add('dragging');sh.style.setProperty('--drag',dy+'px')}},{passive:true});
  panel.addEventListener('touchend',function(){if(y0===null)return;sh.classList.remove('dragging');if(dy>90)close();else sh.style.setProperty('--drag','0px');y0=null;dy=0});
  render();
})();
})();
