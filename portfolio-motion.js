(() => {
 'use strict';
 if(window.__portfolioVisibilityProtected)return;
 window.__portfolioVisibilityProtected=true;
 const selector='.pm-form,.pm-action,.pm-field,.pm-field-row,.pm-control,.pm-label';
 const signatures=new WeakMap();
 const style=document.createElement('style');
 style.dataset.pmGenerated='visibility';
 style.nonce=document.currentScript?.nonce||document.querySelector('script[nonce],style[nonce]')?.nonce||'';
 style.textContent=':is(.pm-form.pm-two-fields,.pm-form,.pm-action,.pm-field,.pm-field-row,.pm-control,.pm-label)[data-pm-native-hidden]{display:none!important}.pm-action.hidden[data-pm-native-visible]{display:var(--pm-source-display,inline-flex)!important}';
 document.head.append(style);
 function reconcile(element,force=false){
  if(!(element instanceof HTMLElement)||!element.matches(selector))return;
  const motion=[...element.classList].filter(name=>name.startsWith('pm-'));
  const native=[...element.classList].filter(name=>!name.startsWith('pm-')).join(' ');
  const signature=[native,element.getAttribute('hidden'),element.style.display,element.getAttribute('aria-hidden'),element.getAttribute('data-state'),innerWidth,innerHeight].join('|');
  if(!force&&signatures.get(element)===signature)return;
  signatures.set(element,signature);
  // Read the source site's display rules without the motion classes. The
  // classes are restored synchronously, before the browser paints a frame.
  element.classList.remove(...motion);
  const display=getComputedStyle(element).display;
  element.classList.add(...motion);
  const hidden=(element.hasAttribute('hidden')&&element.getAttribute('hidden')!=='until-found')||display==='none';
  element.toggleAttribute('data-pm-native-hidden',hidden);
  element.toggleAttribute('data-pm-native-visible',!hidden);
  if(element.style.getPropertyValue('--pm-source-display')!==display)element.style.setProperty('--pm-source-display',display);
 }
 function scan(root,force=false){if(root instanceof Element){reconcile(root,force);root.querySelectorAll(selector).forEach(element=>reconcile(element,force));}}
 const options={subtree:true,childList:true,attributes:true,attributeFilter:['class','style','hidden','aria-hidden','data-state','checked','disabled']};
 function update(work){observer.disconnect();try{work();}finally{observer.observe(document.documentElement,options);}}
 const observer=new MutationObserver(records=>{
  const targets=new Set();
  for(const record of records){if(record.type==='attributes')targets.add(record.target);else for(const node of record.addedNodes)if(node instanceof Element)targets.add(node);}
  update(()=>{for(const target of targets){if(![...targets].some(other=>other!==target&&other.contains(target)))scan(target,true);}});
 });
 update(()=>scan(document.documentElement));
 addEventListener('resize',()=>update(()=>scan(document.documentElement)),{passive:true});
 document.addEventListener('change',()=>update(()=>scan(document.documentElement,true)),{passive:true});
})();

(() => {
 'use strict';
 const script=document.currentScript||document.querySelector('script[data-portfolio-site]');
 const site=script?.getAttribute('data-portfolio-site');
 const kind=script?.getAttribute('data-portfolio-kind');
 if(!site||window.__portfolioMotionLoaded)return;
 window.__portfolioMotionLoaded=true;
 const graphic=site==='suisy.ch'||site==='epargne-suisse.ch';
 const canvas=document.createElement('canvas');canvas.width=canvas.height=1;
 const painter=canvas.getContext('2d');
 if(!painter)return;
 const rgba=color=>{painter.clearRect(0,0,1,1);painter.fillStyle=color;painter.fillRect(0,0,1,1);return [...painter.getImageData(0,0,1,1).data];};
 const lum=color=>{const a=rgba(color);return a[0]*.2126+a[1]*.7152+a[2]*.0722;};
 const transparent=color=>!color||rgba(color)[3]===0;
 const visible=el=>{const r=el.getBoundingClientRect(),c=getComputedStyle(el);return r.width>35&&r.height>15&&c.display!=='none'&&c.visibility!=='hidden'&&!el.closest('[hidden],[aria-hidden=true],[role=dialog],[aria-modal=true]');};
 const en=()=>document.documentElement.lang.startsWith('en');
 const activePath=()=>graphic?(site==='suisy.ch'?location.pathname.endsWith('/calcul-interets-composes.html'):/\/calculateurs\/3a\/?$/.test(location.pathname)):/^\/(?:fr|en|de|it|nl)?\/?(?:index\.html)?$/.test(location.pathname);
 const actionCopy=el=>el.textContent.replace(/\s+/g,' ').trim();
 const isCTA=el=>!(/politique|confidential|privacy|terms|désabonn/i.test(actionCopy(el)))&&(el.type==='submit'||/audit|démo|demo|devis|réserv|contact|comparer|calculer|réinitialiser|besoin|estimer|explorer|articles|services|obtenir|envoyer|recevoir|abonner|rechercher|demander|inscrire|parler|commencer|download|receive|get the|get started|read articles/i.test(actionCopy(el)));
 let selected=null,timer=null,serial=0;
 const optionSyncs=new WeakMap();
 const guideUpdates=new WeakMap();
 function theme(root,primary){
  const p=getComputedStyle(primary||root),r=getComputedStyle(root);
  let accent=p.backgroundColor;
  if(transparent(accent))accent=p.backgroundImage.match(/(?:rgba?|oklab|oklch|lab|lch|color)\([^)]*\)/)?.[0]||p.color;
  const a=rgba(accent),fg=rgba(p.color);
  if(Math.max(...a.slice(0,3))-Math.min(...a.slice(0,3))<20&&Math.max(...fg.slice(0,3))-Math.min(...fg.slice(0,3))>60)accent=p.color;
  let bg=r.backgroundColor,parent=root.parentElement;
  while(transparent(bg)&&parent){bg=getComputedStyle(parent).backgroundColor;parent=parent.parentElement;}
  if(transparent(bg))bg='rgb(255,255,255)';
  const ink=lum(bg)<115?'rgb(248,250,252)':'rgb(17,24,39)';
  root.style.setProperty('--pm-accent',accent);root.style.setProperty('--pm-background',bg);root.style.setProperty('--pm-ink',ink);
  root.style.setProperty('--pm-action-ink',lum(accent)>150?'rgb(17,24,39)':'rgb(255,255,255)');
  if(r.borderRadius!=='0px')root.style.setProperty('--pm-radius',r.borderRadius);
  return {accent,bg,ink};
 }
 function reveal(el,index){if(el.dataset.pmReveal)return;el.dataset.pmReveal='1';el.style.setProperty('--pm-delay',Math.min(index*65,390)+'ms');el.classList.add('pm-reveal');}
 function decorateAction(el,primary){
  if(el.dataset.pmAction)return;
  const paint=getComputedStyle(el);
  for(const [key,value]of Object.entries({background:paint.backgroundColor,image:paint.backgroundImage,ink:paint.color,border:paint.borderColor}))el.style.setProperty('--pm-native-'+key,value);
  el.dataset.pmAction='1';el.classList.add('pm-action',primary?'pm-primary':'pm-secondary');
  if(kind?.startsWith('bouton')&&!el.closest('form'))el.classList.add('pm-action-card');
 }
 function safeForm(form){return !form.querySelector('input[type=password],input[autocomplete="cc-number"],[data-stripe],iframe[src*="stripe"]')&&!/checkout|payment|billing|stripe/i.test(form.action+' '+form.id+' '+form.className);}
 function choose(){
  if(graphic)return site==='suisy.ch'?document.querySelector('#interets-result'):document.querySelector('[data-testid=capital-start]')?.closest('[aria-live]');
  if(site==='xn--factureimpaye-mhb.fr')return [...document.querySelectorAll('details')].find(visible)?.parentElement;
  const forms=kind==='formulaire'?[...document.forms].filter(visible).filter(safeForm).filter(f=>f.querySelector('input:not([type=hidden]),select,textarea')):[];
  forms.sort((a,b)=>score(b)-score(a));
  if(forms[0])return forms[0];
  const buttons=[...document.querySelectorAll('main a,main button,section a,section button')].filter(visible).filter(el=>!el.closest('header,nav,footer')&&actionCopy(el).length<110&&isCTA(el));
  const button=site==='boursier.be'?buttons.find(x=>/^Explorer les outils/.test(actionCopy(x)))||buttons[0]:buttons[0];
  if(!button)return null;
  const parent=button.parentElement,r=parent.getBoundingClientRect();
  return r.width<1150&&r.height<450&&!parent.querySelector('h1,h2,h3,p')&&parent.querySelectorAll('a,button').length<7?parent:button;
 }
 function score(f){return f.querySelectorAll('input:not([type=hidden]),select,textarea').length*10+(f.querySelector('textarea')?20:0)-(f.closest('footer')?40:0);}
 function enhanceForm(form){
  const actions=[...form.querySelectorAll('a,button')].filter(visible).filter(isCTA);
  const primary=actions.find(x=>x.type==='submit')||actions[0];
  if(site==='agentic-whatsup.com'){
   const microphone=[...form.querySelectorAll('button')].at(-1);theme(form,microphone);form.classList.add('pm-chat');microphone?.classList.add('pm-microphone');return;
  }
  const colors=theme(form,primary);
  form.classList.add('pm-form');
  const fields=[...form.querySelectorAll('input,select,textarea')].filter(visible).filter(x=>!['hidden','checkbox','radio','submit','button','range','color','file'].includes(x.type));
  let direct=0;
  fields.forEach((input,index)=>{
   if(input.dataset.pmField)return;
   input.dataset.pmField='1';const original=getComputedStyle(input),color=original.color,bg=original.backgroundColor;
   const alpha=rgba(bg)[3]/255,base=rgba(colors.bg),a=rgba(bg);const mixed=a.slice(0,3).map((v,i)=>v*alpha+base[i]*(1-alpha));
   const fillLum=mixed[0]*.2126+mixed[1]*.7152+mixed[2]*.0722;
   const text=fillLum>150&&lum(color)>180?'rgb(17,24,39)':fillLum<90&&lum(color)<70?'rgb(248,250,252)':color;
   input.style.setProperty('--pm-input-bg',transparent(bg)?`color-mix(in srgb,${colors.bg} 95%,${colors.accent} 5%)`:bg);
   input.style.setProperty('--pm-input-ink',text);
   let label=input.labels?.[0],parent=input.parentElement;
   if(!label){
    if(!input.id)input.id='portfolio-field-'+(++serial);
    label=document.createElement('label');label.htmlFor=input.id;label.dataset.pmGenerated='1';
    const hint=input.getAttribute('aria-label')||input.placeholder||input.name;
    const english=en()||/your@|download|receive insights|get the tips/i.test(hint+' '+actionCopy(primary||form));
    label.textContent=input.type==='email'||/@|email|e-mail/i.test(hint)?(english?'Email address':'Adresse e-mail'):input.tagName==='TEXTAREA'?(english?'Your message':'Votre message'):hint;
    parent.insertBefore(label,input);
   }
   if(label!==parent)label.classList.add('pm-label');
   input.classList.add('pm-control');
   if(parent!==form&&parent.querySelector('svg'))input.classList.add('pm-icon-control');
   if(parent!==form&&parent!==label){parent.classList.add(parent.querySelector('button')?'pm-field-row':'pm-field');if(parent.parentElement===form)direct++;reveal(parent,index);}
  });
  if(fields.length===2&&direct===2)form.classList.add('pm-two-fields');
  actions.forEach(x=>decorateAction(x,x===primary));
  improveNativeForm(form,fields,primary);
 }
 function improveNativeForm(form,fields,primary){
  if(!form.dataset.pmGuide&&fields.length){
   form.dataset.pmGuide='1';
   const guide=generated('div','pm-form-guide');guide.setAttribute('role','status');guide.setAttribute('aria-live','polite');
   const heading=generated('div','pm-guide-title');heading.textContent=en()?'Your request':'Votre demande';
   const count=generated('span','pm-guide-count');const track=generated('div','pm-guide-track');track.setAttribute('aria-hidden','true');track.append(generated('div','pm-guide-fill'));
   guide.append(heading,count,track);form.prepend(guide);
   let previous='';
   const update=()=>{
    const current=[...form.querySelectorAll('.pm-control')].filter(n=>!n.matches(':disabled')&&visible(n));
    const completed=current.filter(n=>n.value.trim()&&n.validity.valid).length;
    track.firstChild.style.transform='scaleX('+(current.length?completed/current.length:0)+')';
    const key=completed+'/'+current.length;
    if(key!==previous){count.textContent=completed+' / '+current.length+(en()?' fields completed':' champs renseignés');previous=key;}
   };
   form.addEventListener('input',update);form.addEventListener('change',update);form.addEventListener('reset',()=>setTimeout(update,0));update();
   guideUpdates.set(form,update);
  }
  guideUpdates.get(form)?.();
  for(const select of fields.filter(n=>n.tagName==='SELECT')){
   const signature=JSON.stringify([...select.options].map(o=>[o.value,o.textContent,o.disabled,!!o.closest('optgroup[disabled]')]));
   const existing=optionSyncs.get(select);
   if(existing?.signature===signature){existing.sync();continue;}
   if(existing){existing.group.remove();optionSyncs.delete(select);delete select.dataset.pmOptions;}
   const options=[...select.options].filter(o=>o.value&&!o.closest('optgroup[disabled]'));
   if(options.length<2||options.length>7)continue;
   select.dataset.pmOptions='1';
   const group=generated('div','pm-service-options');group.setAttribute('role','group');group.setAttribute('aria-label',select.labels?.[0]?.textContent||select.getAttribute('aria-label')||(en()?'Available options':'Choix disponibles'));
   const buttons=options.map((option,i)=>{
    const button=generated('button','pm-service-card');button.type='button';
    const art=generated('span','pm-service-art');art.setAttribute('aria-hidden','true');
    for(let j=0;j<3;j++){const line=generated('i','pm-art-line');line.style.setProperty('--pm-line',j);art.append(line);}
    const text=generated('span','pm-service-name');text.textContent=option.textContent.trim();
    const check=generated('span','pm-service-check');check.textContent='✓';check.setAttribute('aria-hidden','true');
    button.append(art,text,check);button.dataset.pmOptionValue=option.value;
    button.addEventListener('click',()=>{
     const current=[...select.options].find(o=>o.value===option.value);
     if(!current||select.matches(':disabled')||current.disabled||current.closest('optgroup[disabled]'))return;
     // Use the native setter and the original events; keep the real select visible and validatable.
     Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set.call(select,option.value);
     select.dispatchEvent(new Event('input',{bubbles:true}));select.dispatchEvent(new Event('change',{bubbles:true}));
     requestAnimationFrame(sync);
    });
    group.append(button);return button;
   });
   function sync(){buttons.forEach(b=>{const current=[...select.options].find(o=>o.value===b.dataset.pmOptionValue);b.setAttribute('aria-pressed',String(b.dataset.pmOptionValue===select.value));b.disabled=select.matches(':disabled')||!current||current.disabled||!!current.closest('optgroup[disabled]');});}
   optionSyncs.set(select,{sync,group,signature});
   select.parentElement.insertBefore(group,select);select.addEventListener('change',sync);form.addEventListener('reset',()=>setTimeout(sync,0));sync();
  }
  if(primary&&fields.length<4&&!form.querySelector('h2,h3,.pm-intent')){
   const intent=generated('div','pm-intent'),art=generated('span','pm-document');art.setAttribute('aria-hidden','true');
   for(let i=0;i<3;i++)art.append(generated('i',''));
   const title=generated('strong','');title.textContent=actionCopy(primary);intent.append(art,title);form.insertBefore(intent,form.firstChild);
  }
 }
 function parseNumber(node){return Number(node?.textContent.replace(/[^\d.,-]/g,'').replace(',','.'));}
 function generated(tag,className){const n=document.createElement(tag);n.className=className;n.dataset.pmGenerated='1';return n;}
 function updateCapital(root){
  const start=root.querySelector('[data-testid=capital-start]'),end=root.querySelector('[data-testid=capital-end]');
  const values=[parseNumber(start),parseNumber(end)],max=Math.max(...values);
  if(!start||!end||!Number.isFinite(max)||max<=0)return;
  [start,end].forEach((node,i)=>{
   node.classList.add('pm-capital');let track=node.parentElement.querySelector('.pm-track');
   if(!track){track=generated('div','pm-track');const bar=generated('div','pm-bar'+(i?' pm-bar-secondary':''));bar.style.setProperty('--pm-delay',i*160+'ms');track.append(bar);node.parentElement.append(track);}
   const bar=track.firstElementChild,ratio=(values[i]/max*100).toFixed(3)+'%';if(bar.style.getPropertyValue('--pm-ratio')!==ratio)bar.style.setProperty('--pm-ratio',ratio);
  });
  let summary=root.querySelector('.pm-summary');
  if(!summary){summary=generated('div','pm-summary');const axis=generated('div','pm-axis');axis.append(generated('span','pm-zero'),generated('span','pm-maximum'));summary.append(axis,generated('div','pm-difference'),generated('div','pm-caption'));root.append(summary);reveal(summary,2);}
  const format=n=>new Intl.NumberFormat(en()?'en-CH':'fr-CH').format(n);
  const texts=[['.pm-zero',en()?'Bars start at 0 CHF':'Base des barres : 0 CHF'],['.pm-maximum',format(max)+' CHF'],['.pm-difference',(en()?'Difference: ':'Écart : ')+format(Math.abs(values[0]-values[1]))+' CHF'],['.pm-caption',en()?'Between the two projected capitals shown':'Entre les deux capitaux projetés affichés']];
  for(const [selector,text]of texts){const n=summary.querySelector(selector);if(n.textContent!==text)n.textContent=text;}
 }
 function updateDonut(root){
  const donut=root.querySelector('.calc-donut');if(!donut)return;donut.classList.add('pm-donut');
  const value=root.querySelector('.calc-kpi:last-child strong')?.textContent;if(!value)return;
  let center=donut.querySelector('[data-pm-center]');
  if(!center){center=document.createElementNS('http://www.w3.org/2000/svg','text');center.dataset.pmGenerated='1';center.dataset.pmCenter='1';center.setAttribute('x','60');center.setAttribute('y','64');center.setAttribute('text-anchor','middle');center.setAttribute('fill','currentColor');center.style.font='700 15px '+getComputedStyle(root).fontFamily;donut.append(center);}
  if(center.textContent!==value)center.textContent=value;
  [...donut.querySelectorAll('.seg')].forEach((arc,i)=>{if(arc.dataset.pmArc)return;arc.dataset.pmArc='1';arc.style.setProperty('--pm-dash',arc.getAttribute('stroke-dasharray'));arc.style.setProperty('--pm-circumference',String(2*Math.PI*Number(arc.getAttribute('r'))));arc.style.setProperty('--pm-delay',i*160+'ms');arc.classList.add('pm-donut-segment');});
  [...root.querySelectorAll('.calc-kpi')].forEach((k,i)=>{k.classList.add('pm-kpi');reveal(k,i+2);});
  const legend=[...root.querySelectorAll('.calc-legend li')],arcs=[...donut.querySelectorAll('.seg')];
  if(legend.length>1&&legend.length===arcs.length){
   let stack=root.querySelector('.pm-share-stack');if(!stack){stack=generated('div','pm-share-stack');stack.setAttribute('aria-hidden','true');root.append(stack);}
   const selected=Math.min(Number(root.dataset.pmSelectedShare)||0,legend.length-1);
   legend.forEach((li,i)=>{
    const percentage=li.querySelector('b')?.textContent.match(/([\d.,]+)\s*%/)?.[1]?.replace(',','.');
    if(!percentage)return;
    let part=stack.children[i];if(!part){part=generated('i','pm-share-part');stack.append(part);}
    part.style.flex=percentage;part.style.background=arcs[i].getAttribute('stroke');
    li.classList.add('pm-share-option');li.setAttribute('role','button');li.setAttribute('tabindex','0');li.setAttribute('aria-pressed',String(i===selected));
    arcs[i].classList.toggle('pm-muted-arc',i!==selected);
    if(i===selected)center.textContent=percentage+'%';
    if(!li.dataset.pmSelection){
     li.dataset.pmSelection='1';const chooseShare=()=>{root.dataset.pmSelectedShare=String(i);updateDonut(root);};
     li.addEventListener('click',chooseShare);li.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();chooseShare();}});
    }
   });
   while(stack.children.length>legend.length)stack.lastElementChild.remove();
  }
 }
 function apply(){
  if(!activePath())return;
  if(!selected?.isConnected)selected=choose();
  if(!selected)return;
  if(graphic){site==='suisy.ch'?updateDonut(selected):updateCapital(selected);return;}
  if(selected.tagName==='FORM'){enhanceForm(selected);return;}
  if(selected.querySelector('details')){selected.classList.add('pm-faq');[...selected.querySelectorAll('details')].forEach(reveal);return;}
  const actions=[...(selected.matches('a,button')?[selected]:[]),...selected.querySelectorAll('a,button')].filter(visible).filter(isCTA);
  if(!actions.length)return;theme(selected,actions[0]);if(actions.length>1)selected.classList.add('pm-actions');actions.forEach((x,i)=>decorateAction(x,i===0));
 }
 function schedule(){clearTimeout(timer);timer=setTimeout(apply,140);}
 const observer=new MutationObserver(records=>{if(records.some(r=>!r.target.parentElement?.closest('[data-pm-generated]')&&!r.target.closest?.('[data-pm-generated]')))schedule();});
 function start(){apply();observer.observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['disabled','stroke-dasharray','stroke-dashoffset']});window.addEventListener('popstate',schedule);}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else setTimeout(start,250);
})();

;(() => { const source=document.currentScript||document.querySelector('script[data-portfolio-site]');if(!source||window.__portfolioDesignLoader)return;window.__portfolioDesignLoader=true;const css=document.createElement('link');css.rel='stylesheet';css.href='/portfolio-design-v3.css';document.head.append(css);const js=document.createElement('script');js.src='/portfolio-design-v3.js';js.dataset.portfolioSite=source.dataset.portfolioSite||"agents-ia.pro";js.nonce=source.nonce;js.defer=true;css.addEventListener('load',()=>document.body.append(js),{once:true});css.addEventListener('error',()=>console.error('Portfolio styles unavailable'),{once:true});})(); /* design-five-v3-loader */

;(()=>{const src=document.currentScript;if(!src)return;const css=document.createElement('link');css.rel='stylesheet';css.href='/portfolio-design-v10.css';const js=document.createElement('script');js.src='/portfolio-design-v10.js';js.dataset.portfolioSite=src.dataset.portfolioSite||"agents-ia.pro";js.nonce=src.nonce;js.defer=true;css.addEventListener('load',()=>document.body.append(js),{once:true});document.head.append(css);})(); /* five-v10-loader */

;(()=>{if(document.querySelector('script[data-megadesign28]'))return;const s=document.createElement('script');s.src='/megadesign-v28/boot.js';s.dataset.megadesign28='true';s.dataset.site='agents-ia.pro';document.head.appendChild(s)})();
