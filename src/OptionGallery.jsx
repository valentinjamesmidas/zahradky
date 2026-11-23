import React,{useState} from 'react';
import {Check,Plus,Search,X} from 'lucide-react';
import {money} from './catalog.js';

export default function OptionGallery({options,config,update}){
 const [category,setCategory]=useState('Vše'),[query,setQuery]=useState('');
 const categories=['Vše',...new Set(options.map(o=>o.category||'Základní výbava'))];
 const normalized=s=>s.normalize('NFD').replace(/\p{Diacritic}/gu,'').toLowerCase();
 const visible=options.filter(o=>(category==='Vše'||(o.category||'Základní výbava')===category)&&normalized(`${o.name} ${o.detail}`).includes(normalized(query)));
 return <section className="option-library" aria-label="Knihovna vybavení">
  <div className="library-heading"><strong>Vyberte podle svého stylu</strong><span>{options.filter(o=>config[o.id]).length} vybráno</span></div>
  <label className="library-search"><Search size={16}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Hledat vybavení…" aria-label="Hledat vybavení"/>{query&&<button type="button" aria-label="Vymazat hledání" onClick={()=>setQuery('')}><X size={14}/></button>}</label>
  <div className="library-filters" aria-label="Kategorie vybavení">{categories.map(c=><button type="button" key={c} aria-pressed={category===c} onClick={()=>setCategory(c)}>{c}</button>)}</div>
  <p className="library-note">Koncepty naceníme individuálně. Výběr jiné varianty ve stejné části zahrady nahradí předchozí vybavení.</p>
  <div className="visual-options">{visible.map(o=><button type="button" key={o.id} className={`visual-option ${config[o.id]?'selected':''}`} aria-pressed={!!config[o.id]} onClick={()=>update(o.id,!config[o.id])}>
   <div className="visual-option-image"><img src={o.preview} alt="" loading="lazy" decoding="async" width="480" height="360"/>{o.concept&&<span className="concept-badge">KONCEPT</span>}<span className="visual-check">{config[o.id]?<Check size={15}/>:<Plus size={15}/>}</span></div>
   <div className="visual-option-copy"><strong>{o.name}</strong><small>{o.detail}</small><b>{o.price===null?'Cena na poptávku':`+ ${money(o.price)}`}</b></div>
  </button>)}</div>
  {!visible.length&&<div className="library-empty">Nic jsme nenašli. Zkuste jiné slovo nebo kategorii.</div>}
 </section>;
}
