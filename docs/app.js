const state={data:null,channel:'import',day:null,points:[],hover:-1};
const $=s=>document.querySelector(s), fmt=v=>`${Number(v).toFixed(2)}p`, dt=(s,o={})=>new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/London',...o}).format(new Date(s*1000));
const time=s=>dt(s,{hour:'2-digit',minute:'2-digit'}), dayLabel=d=>new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/London',weekday:'short',day:'numeric',month:'short'}).format(new Date(`${d}T12:00:00Z`));

async function load(){
 try{const r=await fetch('data/north-west.json',{cache:'no-store'});if(!r.ok)throw Error(`HTTP ${r.status}`);state.data=await r.json();setup();render()}
 catch(e){$('#freshness').textContent='Price data is temporarily unavailable';document.body.classList.add('load-error')}
}
function setup(){
 const d=$('#day');state.data.days.forEach(x=>d.add(new Option(dayLabel(x),x)));const today=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/London'}).format(new Date());state.day=state.data.days.includes(today)?today:state.data.days.at(-1);d.value=state.day;d.onchange=()=>{state.day=d.value;render()};
 document.querySelectorAll('[data-channel]').forEach(b=>b.onclick=()=>{state.channel=b.dataset.channel;document.querySelectorAll('[data-channel]').forEach(x=>x.classList.toggle('active',x===b));render()});
 const observed=new Date(state.data.observed_at);$('#freshness').textContent=`Observed ${new Intl.DateTimeFormat('en-GB',{dateStyle:'medium',timeStyle:'short',timeZone:'Europe/London'}).format(observed)}`;
 window.addEventListener('resize',draw);const c=$('#price-chart');c.addEventListener('mousemove',move);c.addEventListener('mouseleave',()=>{$('#tooltip').hidden=true;state.hover=-1;draw()});
}
function render(){
 state.points=state.data.channels[state.channel].filter(x=>x.day===state.day).sort((a,b)=>a.start-b.start);$('#chart-title').textContent=`${state.channel[0].toUpperCase()+state.channel.slice(1)} · ${dayLabel(state.day)}`;renderCurrent();renderStats();renderTable();renderRevisions();draw();
}
function renderCurrent(){
 const now=Date.now()/1000;for(const ch of ['import','export']){const p=state.data.channels[ch].find(x=>x.start<=now&&x.end>now);$(`#current-${ch}`).textContent=p?fmt(p.latest):'—'}const p=state.data.channels.import.find(x=>x.start<=now&&x.end>now);$('#current-period').textContent=p?`${time(p.start)}–${time(p.end)} · fixed/current observation`:'No current slot in the published window';
}
function renderStats(){
 const a=state.points;if(!a.length){$('#stats').innerHTML='';return}const vals=a.map(x=>x.latest),changed=a.filter(x=>x.changes>0);const cards=[['Daily average',fmt(vals.reduce((x,y)=>x+y,0)/vals.length)],['Lowest slot',`${fmt(Math.min(...vals))} · ${time(a[vals.indexOf(Math.min(...vals))].start)}`],['Highest slot',`${fmt(Math.max(...vals))} · ${time(a[vals.indexOf(Math.max(...vals))].start)}`],['Revised slots',`${changed.length} of ${a.length}`]];$('#stats').innerHTML=cards.map(([k,v])=>`<div class="stat"><span>${k}</span><strong>${v}</strong></div>`).join('')
}
function renderTable(){
 $('#price-table').innerHTML=state.points.map(p=>`<tr><td>${time(p.start)}</td><td><strong>${fmt(p.latest)}</strong></td><td>${fmt(p.first)}</td><td>${p.low===p.high?'—':`${fmt(p.low)} – ${fmt(p.high)}`}</td><td class="${p.changes?'changed':''}">${p.changes||'—'}</td></tr>`).join('')||'<tr><td colspan="5">No observations for this day.</td></tr>'
}
function renderRevisions(){
 const items=[];for(const channel of ['import','export'])for(const p of state.data.channels[channel])if(p.changes>0)items.push({...p,channel});items.sort((a,b)=>Math.max(...b.history.map(x=>x[0]))-Math.max(...a.history.map(x=>x[0])));$('#revision-list').innerHTML=items.slice(0,9).map(p=>`<article class="revision"><time>${dayLabel(p.day)} · ${time(p.start)} · ${p.channel}</time><strong>${fmt(p.first)} → ${fmt(p.latest)}</strong><p>${p.changes} ${p.changes===1?'change':'changes'} recorded · range ${fmt(p.low)}–${fmt(p.high)}</p></article>`).join('')||'<div class="empty">No price revisions have been recorded in this window.</div>'
}
function dims(){const c=$('#price-chart'),r=c.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);c.width=Math.round(r.width*d);c.height=Math.round((innerWidth<600?310:380)*d);return{c,x:c.getContext('2d'),w:c.width,h:c.height,d,p:{l:56*d,r:18*d,t:20*d,b:44*d}}}
function draw(){if(!state.data)return;const {c,x,w,h,d,p}=dims();x.clearRect(0,0,w,h);const a=state.points;if(!a.length)return;let lo=Math.min(0,...a.map(v=>v.low)),hi=Math.max(0,...a.map(v=>v.high));let pad=Math.max(2,(hi-lo)*.12);lo-=pad;hi+=pad;const px=i=>p.l+i*(w-p.l-p.r)/Math.max(1,a.length-1),py=v=>p.t+(hi-v)*(h-p.t-p.b)/(hi-lo);
 x.font=`${11*d}px system-ui`;x.textAlign='right';x.textBaseline='middle';x.strokeStyle='#e4e9e3';x.fillStyle='#738079';x.lineWidth=d;for(let i=0;i<=5;i++){let v=lo+(hi-lo)*i/5,y=py(v);x.beginPath();x.moveTo(p.l,y);x.lineTo(w-p.r,y);x.stroke();x.fillText(`${v.toFixed(0)}p`,p.l-9*d,y)}
 x.textAlign='center';x.textBaseline='top';for(let i=0;i<a.length;i+=Math.max(1,Math.ceil(a.length/8))){x.fillText(time(a[i].start),px(i),h-p.b+12*d)}
 a.forEach((v,i)=>{if(v.high!==v.low){x.strokeStyle='rgba(79,121,232,.38)';x.lineWidth=5*d;x.lineCap='round';x.beginPath();x.moveTo(px(i),py(v.low));x.lineTo(px(i),py(v.high));x.stroke()}});
 const grad=x.createLinearGradient(0,p.t,0,h-p.b);grad.addColorStop(0,'rgba(20,95,74,.20)');grad.addColorStop(1,'rgba(20,95,74,.01)');x.beginPath();a.forEach((v,i)=>i?x.lineTo(px(i),py(v.latest)):x.moveTo(px(i),py(v.latest)));x.lineTo(px(a.length-1),h-p.b);x.lineTo(px(0),h-p.b);x.closePath();x.fillStyle=grad;x.fill();x.beginPath();a.forEach((v,i)=>i?x.lineTo(px(i),py(v.latest)):x.moveTo(px(i),py(v.latest)));x.strokeStyle='#145f4a';x.lineWidth=3*d;x.lineJoin='round';x.stroke();
 a.forEach((v,i)=>{x.beginPath();x.arc(px(i),py(v.latest),(i===state.hover?6:3)*d,0,Math.PI*2);x.fillStyle=i===state.hover?'#f4775c':'#fff';x.fill();x.strokeStyle='#145f4a';x.lineWidth=2*d;x.stroke()})
}
function move(e){const c=e.currentTarget,r=c.getBoundingClientRect(),i=Math.round((e.clientX-r.left-56)/(r.width-74)*Math.max(1,state.points.length-1));if(i<0||i>=state.points.length)return;state.hover=i;draw();const p=state.points[i],t=$('#tooltip');t.innerHTML=`<strong>${time(p.start)} · ${fmt(p.latest)}</strong><br>${p.changes?`Recorded range ${fmt(p.low)}–${fmt(p.high)}`:p.quality}`;t.hidden=false;let left=e.clientX-r.left+12,top=e.clientY-r.top-50;if(left+180>r.width)left-=190;t.style.left=`${left}px`;t.style.top=`${Math.max(8,top)}px`}
load();
