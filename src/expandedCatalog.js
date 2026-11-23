// Original Blender concepts. No supplier price or availability is implied.
const entry=(id,name,category,detail,zone,position)=>({id:`extra_${id}`,asset:id,name,category,detail,zone,position,price:null,concept:true,icon:'leaf',preview:`/images/options/${id}.webp`,model:`expanded/${id}`});
export const expandedOptions=[
 entry('pergola','Pergola Lounge','Odpočinek','Lamely, křesla a teplé festony.','lounge',[-3,.12,6]),
 entry('greenhouse','Skleník Atelier','Pěstování','Prosklený skleník s antracitovými profily.','garden',[4.5,.12,0]),
 entry('shed','Zahradní sklad','Vybavení','Dřevěný domek na nářadí.','utility',[4.5,.12,-6]),
 entry('sauna','Sauna Cedar','Wellness','Dřevěná sauna s teráskou.','utility',[4.5,.12,-6]),
 entry('tub','Koupací sud','Wellness','Dřevěný sud, kamna a schůdky.','utility',[4.5,.12,-6]),
 entry('pool','Ochlazovací bazén','Wellness','Bazén s dřevěným lemem a žebříkem.','utility',[4.5,.12,-6]),
 entry('kitchen','Venkovní kuchyň','Odpočinek','Gril, pracovní plocha a dřez.','terrace',[-2.7,.4,1.8]),
 entry('dining','Jídelní sestava','Odpočinek','Stůl a čtyři čalouněná křesla.','terrace',[-2.7,.4,1.8]),
 entry('lounge','Lehátka a slunečník','Odpočinek','Dvě lehátka s přírodním čalouněním.','terrace',[-3.4,.4,1.8]),
 entry('swing','Zahradní houpačka','Odpočinek','Závěsná dřevěná lavice pro dva.','lounge',[-3,.12,6]),
 entry('bikes','Stojan na kola','Vybavení','Čtyři místa pro jízdní kola.','utility',[4.5,.12,-6]),
 entry('compost','Dvoukomorový kompostér','Pěstování','Provětrávaná dřevěná sestava.','garden',[4.5,.12,0]),
 entry('barrel','Nádrž na dešťovku','Technologie','Nadzemní nádrž s dřevěným obkladem.','utility',[4.5,.12,-6]),
 entry('beds','Cortenová zahrádka','Pěstování','Čtveřice záhonů s osázením.','garden',[4.5,.12,0]),
 entry('canopy','Solární přístřešek','Technologie','Osm panelů a bateriová skříň.','lounge',[-3,.12,6]),
 entry('lights','Osvětlení cesty','Technologie','Čtyři sloupky s teplým světlem.','path',[-3,.12,9]),
];
export const expandedHouses=[
 ['studio','Studio Solar','Kompaktní domek se střešními panely.'],
 ['panorama','Panorama','Široké čelní prosklení a propojení se zahradou.'],
 ['nordic','Nordic Loft','Sedlová střecha, přírodní obklad a komín.'],
 ['pavilion','Zahradní pavilon','Prosklený prostor s výraznými dřevěnými žebry.'],
].map(([id,name,description])=>({id,name,description,price:null,country:'Autorský koncept',area:0,concept:true,model:`expanded/${id}`,preview:`/images/options/${id}.webp`,type:id==='pavilion'?'garden':'concept',pricingNote:'Koncept k individuálnímu nacenění. Cena domku není zahrnutá v mezisoučtu ani ve splátce.'}));

export function setOption(config,key,value){
 const next={...config,[key]:value};
 const chosen=expandedOptions.find(o=>o.id===key);
 if(chosen&&value){
  for(const o of expandedOptions)if(o.zone===chosen.zone&&o.id!==key)next[o.id]=false;
  if(chosen.zone==='garden')next.beds=false;
  if(chosen.zone==='lounge')next.firepit=false;
  if(chosen.zone==='terrace')next.terrace=true;
 }
 if((key==='beds'||key==='firepit')&&value){
  const zone=key==='beds'?'garden':'lounge';
  for(const o of expandedOptions)if(o.zone===zone)next[o.id]=false;
 }
 if(key==='terrace'&&!value)for(const o of expandedOptions)if(o.zone==='terrace')next[o.id]=false;
 return next;
}
export function validLayout(c){
 const chosen=expandedOptions.filter(o=>c[o.id]);
 if(new Set(chosen.map(o=>o.zone)).size!==chosen.length)return false;
 return !chosen.some(o=>(o.zone==='garden'&&c.beds)||(o.zone==='lounge'&&c.firepit)||(o.zone==='terrace'&&!c.terrace));
}
