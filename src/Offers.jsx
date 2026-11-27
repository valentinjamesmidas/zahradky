import React, {useRef, useState} from 'react';
import {ArrowUpRight, ChevronLeft, Download, MapPin} from 'lucide-react';
import {calculate, money} from './catalog.js';
import {contact, sites, sitePath, weekendConfig, receiptText, offerDate, registry, buildingGuide} from './offer.js';
import './offers.css';

function SitePhoto({site, hero=false}) {
  const path = '/images/lokality/' + site.slug + '-';
  return <figure className="site-photo"><img src={path + '960.webp'} alt={site.alt}
    srcSet={[480,960,1536].map(w => path + w + '.webp ' + w + 'w').join(', ')}
    sizes={hero ? '(max-width: 760px) 100vw, 56vw' : '(max-width: 700px) 90vw, 32vw'}
    width="1536" height="1024" loading={hero ? 'eager' : 'lazy'} fetchPriority={hero ? 'high' : undefined}/>
    <figcaption>Vizualizace · {site.caption}</figcaption></figure>;
}
export function SiteCards() {
  return <div className="site-cards">{sites.map(site => <a href={sitePath(site)} key={site.id}>
    <SitePhoto site={site}/><div className="site-card-text"><h3>{site.name}</h3><ArrowUpRight size={21}/>
    <p>{site.area}</p><small>Detail lokality a prohlídky</small></div></a>)}</div>;
}
export function Contact() {
  return <address className="offer-contact"><strong>{contact.name}</strong><a href={'mailto:' + contact.email}>{contact.email}</a>
    <span>Kontakt pro zahrádky · {contact.company}</span><span>{contact.address}</span>
    <a href={registry} target="_blank" rel="noreferrer">IČO {contact.ico} · ověřit v ARES</a></address>;
}
export function Receipt({code,config,reserve=false,visit=false,details}) {
  const text = receiptText({code,config,reserve,visit,details});
  function save() {
    const url = URL.createObjectURL(new Blob(['\uFEFF',text],{type:'text/plain;charset=utf-8'}));
    const link = document.createElement('a'); link.href=url; link.download=code+'.txt'; link.click();
    setTimeout(() => URL.revokeObjectURL(url),1000);
  }
  return <div className="offer-receipt"><p>Vyřizuje {contact.name}. Při další komunikaci uveďte kód <strong>{code}</strong>.</p>
    <button type="button" className="garden-button" onClick={save}><Download size={15}/> Stáhnout kopii</button>
    <a href={'mailto:'+contact.email+'?subject='+encodeURIComponent('Zahrádky · '+code)+'&body='+encodeURIComponent('Dobrý den, pane Voborníku,\nnavazuji na '+(visit?'žádost o prohlídku':'poptávku')+' '+code+'.\n')}>Napsat Petrovi</a></div>;
}
function VisitForm({site}) {
  const requestId=useRef(null);
  const [state,setState]=useState('idle'), [error,setError]=useState(''), [result,setResult]=useState(null);
  async function submit(event) {
    event.preventDefault();
    if(state==='sending') return;
    const form = new FormData(event.currentTarget);
    const email = form.get('email');
    requestId.current ||= crypto.randomUUID();
    setState('sending'); setError('');
    try {
      const r=await fetch('/api/leads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
        requestId:requestId.current,intent:'visit',location:site.id,email,website:form.get('website'),consent:form.has('consent')
      })});
      const data=await r.json();
      if(!r.ok) throw new Error(data.error);
      setResult({code:data.code,email}); setState('success');
    } catch(e) {setState('idle'); setError(e.message || 'Zájem se nepodařilo uložit. Zkuste to znovu.');}
  }
  return <section className="visit-section" id="prohlidka"><div><span className="section-kicker">Prohlídky · {site.name}</span>
    <h2>Chcete se sem podívat?</h2><p>Termín zatím není vypsán. Zanechte e-mail a Petr Voborník vám dá vědět, až se otevřou prohlídky v této oblasti.</p></div>
    {result ? <div role="status"><h3>Zájem o prohlídku je uložený.</h3><Receipt visit code={result.code} config={weekendConfig(site.id)} details={{email:result.email}}/></div> :
      <form onSubmit={submit}><label htmlFor="visit-email">Váš e-mail</label><input id="visit-email" name="email" required maxLength="200" autoComplete="email" type="email" placeholder="vas@email.cz"/>
      <label className="honeypot" aria-hidden="true">Web<input name="website" tabIndex="-1" autoComplete="off"/></label>
      <label className="visit-consent"><input name="consent" type="checkbox" required/>Souhlasím, aby mě ALBET servis s.r.o. kontaktovala k prohlídce v této lokalitě.</label>
      <small>Žádosti starší 90 dní se mažou při přijetí dalších požadavků. Žádost o výmaz můžete poslat na {contact.email}.</small>
      {error&&<p role="alert">{error}</p>}<button className="garden-button" disabled={state==='sending'}>{state==='sending'?'Ukládáme…':'Upozornit na prohlídku'} <ArrowUpRight size={16}/></button></form>}</section>;
}
export function CostNotes() {
  return <p className="cost-notes">K dokončení může přibýt doprava domku, založení, montáž a napojení. Cenu těchto prací, spotřeby vody a sezónní správy upřesní nabídka konkrétní parcely.</p>;
}
const rules = [
  ['Domek a územní plán','Před objednávkou je třeba znát parcelní číslo, využití plochy podle územního plánu, rozměry a účel domku. Z nich vychází posouzení stavebního úřadu. Stejnou kontrolu vyžaduje i mobilní domek.'],
  ['Voda, toaleta a odpady','Vrt je v návrhu zdrojem užitkové vody. Zdroj pitné vody, nakládání s odpadní vodou i podmínky použití toalety se musí doložit pro konkrétní místo.'],
  ['Přespávání a pronájem','Přípustnost nocování, bydlení nebo rekreačního pronájmu závisí na povoleném účelu stavby, místních podmínkách a smlouvě. Projekt tyto způsoby užívání dosud nepotvrdil.']
];
export function SiteDetail({site}) {
  const example = weekendConfig(site.id), sum=calculate(example);
  return <main className="site-detail"><a className="return-map" href="/#lokality"><ChevronLeft size={16}/> Zpět na mapu lokalit</a>
    <header className="site-hero"><div><span className="section-kicker">Etapa I · v přípravě</span><h1>{site.name}</h1>
      <p className="site-area"><MapPin size={17}/>{site.area}</p><p>Jak by mohl vypadat víkend v sadu o 300 m² a kolik vyjde sestava s domkem NOVA?</p>
      <a className="garden-button" href="#prohlidka">Mám zájem o prohlídku <ArrowUpRight size={16}/></a></div><SitePhoto site={site} hero/></header>
    <div className="offer-spread"><section><span className="section-kicker">Stav podkladů k {offerDate}</span><h2>Co víme o místě</h2>
      <dl className="offer-facts">{[
        ['Ukázková parcela č. 14','300 m² v modelovém plánu. Skutečná výměra a dostupnost čekají na potvrzení.'],
        ['Vlastník a právní titul','Parcelní číslo, list vlastnictví ani podmínky převodu či nájmu zatím nejsou zveřejněny.'],
        ['Přístup a parkování','Návrh počítá se společnou štěrkovou cestou a bránou. Právo průjezdu, parkování a pěší vzdálenost od brány je potřeba ověřit.'],
        ['Pozemek a společné části','Na zahrádce model počítá se čtyřmi mladými stromy a vodoměrnou šachtou. V návrhu areálu je společné oplocení, cesta, brána a vrt. Rozsah předání upřesní smlouva.']
      ].map(([a,b])=><div key={a}><dt>{a}</dt><dd>{b}</dd></div>)}</dl>
      <a className="section-link" href={'https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(site.name+', Česko')} target="_blank" rel="noreferrer">Trasa do města <ArrowUpRight size={14}/></a></section>
    <section className="budget-card"><span className="section-kicker">Modelový rozpočet · 300 m²</span><h2>Sad s domkem NOVA</h2>
      <p>Domek 4 × 3 m, modřínová terasa 18 m² a čtyři vyvýšené záhony.</p>
      <dl>{sum.items.map(item=><div key={item.name}><dt>{item.name}</dt><dd>{money(item.price)}</dd></div>)}
      <div className="budget-total"><dt>Naceněné položky</dt><dd>{money(sum.total)}</dd></div>
      <div><dt>Dokončení a napojení</dt><dd>K nacenění</dd></div><div><dt>Voda a správa za sezónu</dt><dd>K potvrzení</dd></div></dl>
      <p>V rozpočtu 2 000 000 Kč po těchto položkách zbývá <strong>{money(2000000-sum.total)}</strong> na další výdaje.</p><CostNotes/><p>Výdaj do předání ani za první sezónu zatím nelze sečíst. Správce, způsob rozúčtování vody a roční sazby budou součástí nabídky.</p>
      <a className="garden-button" href={'/?lokalita='+site.id+'&sestava=vikend#konfigurator'}>Upravit tuto sestavu <ArrowUpRight size={15}/></a></section></div>
    <section className="site-rules"><div><span className="section-kicker">Před podpisem</span><h2>Co na zahrádce můžete dělat?</h2></div><div>{rules.map(([title,detail])=><details key={title}><summary>{title}</summary><p>{detail}</p></details>)}
      <a className="section-link" href={buildingGuide} target="_blank" rel="noreferrer">Metodika MMR k mobilním domům <ArrowUpRight size={14}/></a></div></section>
    <VisitForm site={site}/><section className="site-rules"><div><span className="section-kicker">Kontakt pro projekt</span><h2>Kdo vám odpoví</h2><Contact/></div>
      <div><h3>Kdo dodává domek</h3><p>Modelem NOVA se zabývá výrobce TŘY D, DOMY Dřevostavby Development s.r.o. Kontakt v Rakovníku vyřizuje zájem o zahrádky. Prodávajícího pozemku, smluvního dodavatele montáže, rozsah dodávky a záruky určí individuální nabídka.</p><a className="section-link" href={sum.house.source} target="_blank" rel="noreferrer">NOVA u výrobce <ArrowUpRight size={14}/></a></div></section></main>;
}
