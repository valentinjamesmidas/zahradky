export const locations = [
 {id:'KLD',name:'Kladno',area:'Vinařická hora / Pletený Újezd',distance:'5 min od sídlišť Kročehlavy a Rozdělov',soil:'Půda III.–IV. třídy',price:1200000},
 {id:'MBL',name:'Mladá Boleslav',area:'Bradlec / Kosmonosy',distance:'6 min od Severního sídliště',price:1200000},
 {id:'KOL',name:'Kolín',area:'Jižní svahy – Pašinka',distance:'7 min z centra a sídliště',price:1150000},
 {id:'PRI',name:'Příbram',area:'Podbrdské svahy',distance:'5 min od sídliště Drkolnov',price:990000},
 {id:'CHO',name:'Chomutov & Jirkov',area:'Podkrušnohoří',distance:'6 min od sídlišť',price:890000},
 {id:'MOS',name:'Most',area:'Jižní rekultivované sady',distance:'5 min z města',price:850000},
 {id:'KAR',name:'Karviná & Havířov',area:'Těšínská pahorkatina',distance:'7 min od Šumbarku a Ráje',price:950000},
 {id:'TEP',name:'Teplice',area:'Krupka / Modlany svahy',distance:'6 min ze sídliště Trnovany',price:950000},
 {id:'PRE',name:'Přerov',area:'Severní svahy – Čekyně',distance:'6 min z Předmostí',price:990000},
 {id:'SOK',name:'Sokolov',area:'Západní terasy',distance:'5 min ze sídliště Michal',price:820000}
];
export const houses=[
 {id:'none',name:'Pouze váš sad',country:'Bez Tiny Housu',area:0,price:0,description:'Připravený soukromý sad o rozloze 300 m². Prostor pro všechny vaše plány.'},
 {id:'liberte',name:'Liberté Tiny Shell',country:'Nizozemsko',area:20,price:790000,description:'Svislý modřínový obklad, francouzská dvoukřídlá okna a podvozek Vlemmix s SPZ.'},
 {id:'millhome',name:'Mill Home Nordic',country:'Nizozemsko',area:25,price:1190000,description:'Asymetrická střecha, rohové prosklení, spací loft, koupelna a kuchyně.'},
 {id:'baluchon',name:'Baluchon Cedar Edition',country:'Francie',area:24,price:1390000,description:'Červený cedr, antracitový falcovaný plech a krbová kamna.'},
 {id:'anna',name:'Cabin ANNA Glamping',country:'Nizozemsko',area:28,price:1690000,description:'Posuvné prosklené stěny, biofilní dřevěná žebra a kontakt s přírodou.'},
 {id:'nova',name:'Hybridní dům NOVA',country:'Česko · TŘY D',area:12,price:376298,model:'house_nova',type:'garden',dimensions:'4 × 3 m',source:'https://tryd.cz/hybridni-dum-nova/',sourcePrice:310990,vat:21,preview:'/images/nova-preview.webp',description:'Zateplený zahradní domek s půdorysem 4 × 3 m, sedlovou střechou, antracitovým opláštěním Classic click a zapuštěným čelem z Thermowoodu. Čtyřdílné prosklení v antracitových rámech. Bez podvozku a SPZ.',pricingNote:'Orientační základ 310 990 Kč + 21 % DPH = 376 298 Kč. Doprava, montáž, založení a další výbava se naceňují zvlášť. Ověřeno u výrobce 9. 11. 2026.'}
];
export const gardenOptions=[
 {id:'orchardXXL',name:'Vzrostlý ovocný sad XXL',detail:'8 vzrostlých stromů + jedlé keře',price:45000,icon:'trees'},
 {id:'terrace',name:'Modřínová terasa',detail:'18 m² na zemních vrutech',price:85000,icon:'terrace'},
 {id:'beds',name:'Vyvýšené záhony Corten',detail:'4 záhony včetně substrátu',price:38000,icon:'sprout'},
 {id:'firepit',name:'Večery u ohně',detail:'Ohniště, posezení a pergola s festony',price:62000,icon:'flame'}
];
export const techOptions=[
 {id:'solar',name:'Vlastní solární energie',detail:'Victron Energy · 3 kWp + 5 kWh LiFePO₄',price:95000,icon:'sun'},
 {id:'toilet',name:'Eko-toaleta Cinderella Freedom',detail:'Spalovací / separační řešení bez jímky',price:89000,icon:'leaf'},
 {id:'water',name:'Dešťovka pro váš sad',detail:'Nádrž 4 000 l + automatická závlaha',price:68000,icon:'water'}
];
export const defaultConfig={location:'KLD',plot:14,house:'liberte',orchardXXL:true,terrace:true,beds:false,firepit:false,solar:false,toilet:false,water:false,payment:'finance',downPercent:15,years:10};
export const money=(value)=>new Intl.NumberFormat('cs-CZ',{style:'currency',currency:'CZK',maximumFractionDigits:0}).format(value);
export function plotStatus(n){return [3,8,19,24,29].includes(n)?'sold':[5,11,17,26].includes(n)?'reserved':'free'}
export function validateConfig(c){
 if(!c||!locations.some(l=>l.id===c.location)||!houses.some(h=>h.id===c.house))return false;
 if(!Number.isInteger(c.plot)||c.plot<1||c.plot>30||plotStatus(c.plot)!=='free')return false;
 if(!['finance','cash'].includes(c.payment)||!Number.isInteger(c.downPercent)||c.downPercent<15||c.downPercent>70||!Number.isInteger(c.years)||c.years<3||c.years>10)return false;
 return [...gardenOptions,...techOptions].every(o=>typeof c[o.id]==='boolean');
}
export function calculate(c){
 const location=locations.find(l=>l.id===c.location),house=houses.find(h=>h.id===c.house);
 const items=[{name:`Sad 300 m² · ${location.name}`,price:location.price},...(house.price?[{name:house.name,price:house.price}]:[]),...[...gardenOptions,...techOptions].filter(o=>c[o.id]).map(({name,price})=>({name,price}))];
 const total=items.reduce((sum,item)=>sum+item.price,0),down=c.payment==='cash'?total:Math.round(total*c.downPercent/100),principal=total-down,n=c.years*12,r=.079/12,power=Math.pow(1+r,n);
 const monthly=c.payment==='cash'?0:principal*(r*power)/(power-1);
 return {location,house,items,total,down,principal,monthly,n,repayment:monthly*n,interest:monthly*n-principal,paidTotal:down+monthly*n};
}
export function serializableConfig(c){return Object.fromEntries(Object.keys(defaultConfig).map(k=>[k,c[k]]))}
