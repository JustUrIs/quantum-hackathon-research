import * as svc from "ambulancia.engine";

const $=id=>document.getElementById(id);
const map=$("cityMap"),N=8;
const siteColors={normal:"#324e3c",chosen:"#b5e431"};
let currentConfig=null, currentResult=null, timer=null, spent=false, busy=false, pending=null;
const backendAvailable=()=>{try{return typeof backend!=="undefined"&&backend!==null}catch{return false}};
const py=async(name,...args)=>await svc[name].callPromising(...args);
const pct=(a,b)=>b>0?`${(100*a/b).toFixed(1)}%`:"—";

function config(){return {units:Number($("units").value),radius_km:Number($("radius").value),outage_weight:Number($("outage").value)/100,scenario:$("scenario").value}}
function labelScenario(s){return ({history:"all years",night:"night shift",recent:"2025 only",severe:"severity weighted"})[s]||s}
function cabaX(lon){return 45+(lon-currentResult.map.boundary.west)/(currentResult.map.boundary.east-currentResult.map.boundary.west)*670}
function cabaY(lat){return 28+(currentResult.map.boundary.north-lat)/(currentResult.map.boundary.north-currentResult.map.boundary.south)*470}
function heatColor(t){const hue=113-102*t;return `hsl(${hue} 56% ${84-39*t}%)`}
function renderMap(d){
  currentResult=d; const b=d.map.boundary, mask=b.mask; const w=760,h=560,x0=45,y0=28,gw=670,gh=470;
  const sx=gw/32,sy=gh/32,tx=gw/8,ty=gh/8;
  const max=Math.max(1,...d.map.grid_rows.flat().map(c=>{
    const s=d.config.scenario;return s==="night"?c.night:s==="recent"?c.recent:s==="severe"?c.serious+3*c.fatal:c.events+2*c.serious+5*c.fatal;
  }));
  let svg=`<rect x="0" y="0" width="760" height="560" fill="#e8ece6"/><defs><pattern id="uncovered" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#d3c9b6"/><line x1="0" y1="0" x2="0" y2="8" stroke="#817966" stroke-width="2"/></pattern></defs>`;
  for(let r=0;r<32;r++)for(let c=0;c<32;c++)if(mask[r*32+c])svg+=`<rect class="city-mask" x="${x0+c*sx}" y="${y0+r*sy}" width="${sx+.2}" height="${sy+.2}"/>`;
  for(let r=0;r<8;r++)for(let c=0;c<8;c++){
    if(!d.map.grid_rows[r][c].events)continue;
    const cell=d.map.grid_rows[r][c],signal=d.config.scenario==="night"?cell.night:d.config.scenario==="recent"?cell.recent:d.config.scenario==="severe"?cell.serious+3*cell.fatal:cell.events+2*cell.serious+5*cell.fatal;
    const reachable=d.map.reach_masks[r*8+c],covered=d.map.qaoa_sites.some(i=>reachable&(1<<i));
    const x=x0+c*tx,y=y0+r*ty;
    svg+=`<rect class="map-cell" x="${x}" y="${y}" width="${tx}" height="${ty}" fill="${covered?heatColor(signal/max):'url(#uncovered)'}" opacity="${signal?(.32+.68*signal/max):.1}"><title>${cell.events} historical events; ${covered?"covered in this scenario":"uncovered by the QAOA sample"}</title></rect>`;
  }
  for(let r=0;r<32;r++)for(let c=0;c<32;c++)if(mask[r*32+c]&&!(r%4)&&!(c%4))svg+=`<path d="M${x0+c*sx} ${y0+r*sy}v${sy*4} M${x0+c*sx} ${y0+r*sy}h${sx*4}" fill="none" stroke="#879183" stroke-opacity=".29" stroke-width=".65"/>`;
  const chosen=new Set(d.map.qaoa_sites);
  d.map.sites.forEach((s,i)=>{
    const x=cabaX(s.lon),y=cabaY(s.lat),active=chosen.has(i),fill=active?siteColors.chosen:siteColors.normal;
    svg+=`<circle class="map-site" cx="${x}" cy="${y}" r="${active?12:9}" fill="${fill}"><title>${s.id}, representative census radio${active?", selected by the ideal local QAOA sample":""}</title></circle><text class="map-pin" x="${x}" y="${y+3}" text-anchor="middle" fill="${active?"#192321":"#f5f4ef"}">${i+1}</text>`;
  });
  svg+=`<text class="map-axis" x="${x0}" y="520">WEST / PROVINCIA</text><text class="map-axis" x="${x0+gw}" y="520" text-anchor="end">EAST / RÍO DE LA PLATA</text><text class="map-axis" x="${x0}" y="542">Historical crash signal × selected coverage · ${labelScenario(d.config.scenario)}</text>`;
  map.innerHTML=svg;
}
function renderScores(d){
  const total=d.event_index_total,methods=[...d.methods,{method:"qaoa",score:d.qaoa.best_sample_score,normal_score:d.qaoa.normal_score,one_site_out_score:d.qaoa.one_site_out_score,sites:d.qaoa.best_sample_sites}];
  const titles={greedy:"GREEDY",local_swap:"GREEDY + SWAPS",exact:"EXACT SEARCH",qaoa:"QAOA · MOST LIKELY"};
  const badges={greedy:"Sequential add",local_swap:"1-site exchange",exact:`Checked ${d.classical_combinations} subsets`,qaoa:`${d.qaoa.layers} layers · 8 qubits`};
  $("scoreboard").innerHTML=methods.map(m=>{
    const best=m.method==="qaoa",exact=m.method==="exact",sites=m.sites.map(i=>d.map.sites[i].id).join(" · ");
    return `<article class="score-card ${best?"qaoa":exact?"exact":""}"><span class="score-kicker">${best?"MOST LIKELY BASIS STATE":exact?"LOWER-BOUND CHECK":"CLASSICAL BASELINE"}</span><h3>${titles[m.method]}</h3><div class="score-number">${pct(m.score,total)}<span class="score-unit">SIGNAL</span></div><div class="score-sub">${pct(m.normal_score,total)} normal coverage<br />${pct(m.one_site_out_score,total)} after one-site-out average</div><div class="score-badge">${best?`Ideal local P(optimum): ${pct(d.qaoa.probability_optimum,1)}`:badges[m.method]}</div><div class="score-sites">${sites||"—"}</div></article>`;
  }).join("");
  $("status").textContent=`Scenario ready · ${labelScenario(d.config.scenario)} · ${d.classical_combinations} exact subsets checked`;
}
async function refresh(){
  pending=config();if(busy)return;busy=true;
  try{while(pending){const next=pending;pending=null;currentConfig=next;$("status").textContent="Scoring the exact outage objective and optimizing a local QAOA reference…";for(const el of document.querySelectorAll(".live-state span"))el.style.background="#d59a35";
      const raw=await py("evaluate",JSON.stringify(next));const d=JSON.parse(String(raw));
      if(JSON.stringify(next)===JSON.stringify(currentConfig)){renderMap(d);renderScores(d);$("eventCount").textContent=Number(d.unweighted_events).toLocaleString("en-US");$("unitsValue").textContent=next.units;$("radiusValue").textContent=`${next.radius_km.toFixed(1)} km`;$("outageValue").textContent=`${Math.round(next.outage_weight*100)}%`;}
    }}catch(e){$("status").textContent=`Could not score this scenario: ${e.message||e}`;$("status").style.color="#9e4536"}
  finally{busy=false;for(const el of document.querySelectorAll(".live-state span"))el.style.background="#84b738";if(pending)refresh()}
}
function schedule(){clearTimeout(timer);timer=setTimeout(refresh,450)}
for(const id of ["scenario","radius","outage"])$(id).addEventListener(id==="scenario"?"change":"input",schedule);
$("unitsDown").onclick=()=>{$("units").value=Math.max(1,Number($("units").value)-1);schedule()};
$("unitsUp").onclick=()=>{$("units").value=Math.min(N,Number($("units").value)+1);schedule()};
$("runBackend").onclick=async()=>{
  const button=$("runBackend"),status=$("auditStatus");
  if(spent||busy){status.textContent=spent?"This Qollab run already used its one backend job. Restart the project to make another measurement.":"Wait for the local scenario optimization to finish.";return}
  if(!backendAvailable()){status.textContent="No Qollab backend is available in this session. The local reference remains an ideal statevector calculation.";return}
  const snapshot=currentConfig?{...currentConfig}:config();button.disabled=true;status.textContent="Building the measured QAOA circuit…";
  try{
    const circuit=await svc.audit_circuit.callPromising(JSON.stringify(snapshot));
    const name=String(backend.name||backend.backend_name||"selected backend"),shots=/ionq/i.test(name)?100:256;
    status.textContent=`Submitting one ${circuit.num_qubits}-qubit job · ${shots} shots · ${name}.`;
    spent=true;const job=await backend.run(circuit,{shots});const result=await job.result();
    const raw=result.get_counts(),v=raw&&raw.toJs?raw.toJs():raw,counts=v instanceof Map?Object.fromEntries(v):v;
    const report=JSON.parse(String(await svc.ingest_audit.callPromising(JSON.stringify(counts),JSON.stringify(snapshot),name)));
    $("auditOutput").textContent=JSON.stringify(report,null,2);const best=[...report.counts].sort((a,b)=>b.score-a.score)[0];
    status.textContent=`Measured ${report.shots} shots on ${report.backend}. ${Math.round(100*report.fixed_cardinality_rate)}% kept exactly ${snapshot.units} units. Best sampled score: ${pct(best.score,Number(currentResult?.event_index_total||1))}.`;
    button.textContent="Job used · restart Qollab to measure again";
  }catch(e){status.textContent=`Backend job failed: ${e.message||e}. Local reference remains separate.`;if(!spent)button.disabled=false;}
};
refresh();
