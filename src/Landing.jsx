import React, { useEffect, useRef, useState } from 'react';
import { ChevronDown, ChevronLeft, ChevronRight, Expand, House, MapPin, SlidersHorizontal, X } from 'lucide-react';
import { houses } from './catalog.js';
import AreaMap, { firstStageCities } from './AreaMap.jsx';

import { Contact } from './Offers.jsx';

const nova = houses.find(house => house.id === 'nova');
const reasons = [
  ['Vyberete si oblast', 'Porovnejte na mapě Mladou Boleslav, Kladno a Příbram podle toho, odkud budete na zahrádku jezdit.'],
  ['Sestavíte si zahrádku', 'K sadu můžete přidat domek, modřínovou terasu nebo vyvýšené záhony.'],
  ['Projdete si návrh ve 3D', 'Otočte si scénu, přibližte si domek a přepněte z denního světla na večerní.'],
  ['Poptáte vybranou sestavu', 'Před odesláním nezávazné poptávky uvidíte zvolené vybavení i rozpis orientační ceny.']
];
const scenes = [
  {id:'kolonie', title:'Kolonie mezi poli', caption:'Pohled shora na sady a společnou cestu.', alt:'Pohled z výšky na oplocené zahrádky, ovocné stromy a malé domky u polí.'},
  {id:'pesina', title:'Po hlavní pěšině', caption:'Štěrková pěšina spojuje vstupy do jednotlivých zahrádek.', alt:'Štěrková cesta mezi drátěnými ploty a ovocnými stromy u zahradních branek.'},
  {id:'nova', title:'Domek mezi stromy', caption:'Hybridní dům NOVA v základní variantě 4 × 3 m.', alt:'Pohled ze zahrádky na dřevěné čelo domku NOVA s prosklenými dveřmi a antracitovou střechou.'},
  {id:'zahony', title:'Zelenina na dosah', caption:'Pěstitelský kout se čtyřmi volitelnými záhony z cortenu.', alt:'Čtyři vyvýšené záhony z rezavě zbarvené oceli osázené zeleninou.'},
  {id:'posezeni', title:'Ve stínu pergoly', caption:'Posezení, pergola se světly a ohniště z doplňku Večery u ohně.', alt:'Dřevěná pergola s posezením kolem nízkého kruhového ohniště.'},
  {id:'terasa', title:'Zápraží a terasa', caption:'Čelo z Thermowoodu navazuje na volitelnou modřínovou terasu o 18 m².', alt:'Detail dřevěných prken modřínové terasy u proskleného vstupu do domku NOVA.'}
];
const imagePath = (id, width) => '/images/galerie/' + id + '-' + width + '.webp';
function Photo({scene, hero=false, expanded=false}) {
  return <img src={imagePath(scene.id, 960)}
    srcSet={[480, 960, 1536].map(width => imagePath(scene.id, width) + ' ' + width + 'w').join(', ')}
    sizes={hero ? '(max-width: 630px) 960px, 100vw' : expanded ? '100vw' : '(max-width: 630px) 94vw, 46vw'}
    width="1536" height="1024" loading={hero || expanded ? 'eager' : 'lazy'}
    fetchPriority={hero ? 'high' : undefined} decoding="async" alt={scene.alt}/>;
}

function Gallery() {
  const [index, setIndex] = useState(0);
  const dialog = useRef(null);
  const [open, setOpen] = useState(false);
  const move = delta => setIndex(value => (value + delta + scenes.length) % scenes.length);
  useEffect(() => {
    if (!open) return;
    const modal = dialog.current;
    modal.showModal();
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = previous; };
  }, [open]);
  return <section className="gallery-section content-section" id="galerie" aria-labelledby="gallery-title">
    <div className="section-heading"><span className="section-kicker">Galerie vizualizací</span><h2 id="gallery-title">Ze života zahrádky</h2></div>
    <div className="garden-gallery">{scenes.map((scene, i) => <figure key={scene.id}>
      <button className="photo-frame" aria-label={'Zvětšit snímek – ' + scene.title} aria-haspopup="dialog" onClick={() => { setIndex(i); setOpen(true); }}>
        <Photo scene={scene}/><span className="photo-label">Vizualizace</span><span className="expand-icon"><Expand size={16}/></span>
      </button>
      <figcaption><h3>{scene.title}</h3><p>{scene.caption}</p></figcaption>
    </figure>)}</div>
    <a className="garden-button gallery-cta" href="/#konfigurator">Navrhnout si vlastní zahrádku</a>
    {open && <dialog className="lightbox" ref={dialog} aria-labelledby="lightbox-title"
      onClose={() => setOpen(false)} onClick={e => {if (e.target === dialog.current) dialog.current.close();}}
      onKeyDown={e => {if (e.key === 'ArrowLeft') move(-1); if (e.key === 'ArrowRight') move(1);}}>
      <div className="lightbox-content">
        <button className="close-image" autoFocus aria-label="Zavřít snímek" onClick={() => dialog.current.close()}><X/></button>
        <Photo scene={scenes[index]} expanded/>
        <div className="image-controls">
          <div aria-live="polite"><small>Vizualizace · {index + 1} / {scenes.length}</small><h3 id="lightbox-title">{scenes[index].title}</h3><p>{scenes[index].caption}</p></div>
          <button aria-label="Předchozí snímek" onClick={() => move(-1)}><ChevronLeft/></button>
          <button aria-label="Další snímek" onClick={() => move(1)}><ChevronRight/></button>
        </div>
      </div>
    </dialog>}
  </section>;
}

function DesignPicker() {
  const [city, setCity] = useState('');
  const [house, setHouse] = useState('');
  const params = new URLSearchParams();
  if (city) params.set('lokalita', city);
  if (house) params.set('dum', house);
  const href = '/' + (params.size ? '?' + params : '') + '#konfigurator';
  return <div className="design-picker" role="group" aria-label="Výchozí nastavení konfigurátoru">
    <label><MapPin aria-hidden="true"/><span>Lokalita
      <select aria-label="Lokalita" value={city} onChange={event => setCity(event.target.value)}>
        <option value="">Vybrat později</option>
        {firstStageCities.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}
      </select></span><ChevronDown className="select-chevron" aria-hidden="true"/></label>
    <label><House aria-hidden="true"/><span>Domek
      <select aria-label="Domek" value={house} onChange={event => setHouse(event.target.value)}>
        <option value="">Vybrat později</option>
        {houses.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}
      </select></span><ChevronDown className="select-chevron" aria-hidden="true"/></label>
    <a className="garden-button picker-cta" href={href}><SlidersHorizontal size={17} aria-hidden="true"/> Otevřít konfigurátor</a>
  </div>;
}

const heroScenes = [scenes[0], scenes[2], scenes[4]];
function Welcome() {
  const [active, setActive] = useState(0);
  function changeScene(direction) {
    setActive(index => (index + direction + heroScenes.length) % heroScenes.length);
  }
  return <section id="uvod" className="garden-hero" aria-labelledby="welcome-title">
    <Photo scene={heroScenes[active]} hero/>
    <div className="hero-inner">
      <span className="hero-kicker">Soukromé ovocné sady</span>
      <h1 id="welcome-title">Vlastní zahrádka <strong>ve středních Čechách.</strong></h1>
      <p>Vyberte si lokalitu pro svůj sad o rozloze 300 m².<br/> Domek, terasu i záhony si pak sestavíte ve 3D.</p>
      <DesignPicker/>
    </div>
    <div className="hero-controls">
      <a className="hero-more" href="/#lokality"><ChevronDown aria-hidden="true"/> Prohlédnout lokality</a>
      <div className="scene-strip">
        <span aria-live="polite">Vizualizace · {heroScenes[active].title}</span>
        <button type="button" aria-label="Předchozí pohled na zahrádku" onClick={() => changeScene(-1)}><ChevronLeft/></button>
        <button type="button" aria-label="Další pohled na zahrádku" onClick={() => changeScene(1)}><ChevronRight/></button>
      </div>
    </div>
  </section>;
}

export default function Landing() {
  return <main className="landing">
    <Welcome/>
    <section className="benefits content-section" aria-labelledby="benefits-title">
      <div className="benefit-intro"><span className="section-kicker">O zahrádkách</span>
        <h2 id="benefits-title">Od první volby<br/>k vlastnímu sadu.</h2>
        <a className="section-link" href="/#lokality">Prohlédnout lokality</a>
      </div>
      <ol>{reasons.map(([title, detail], i) => <li key={title} id={i===0 ? "prvni-duvod" : undefined}><h3>{title}</h3><p>{detail}</p></li>)}</ol>
    </section>
    <AreaMap/><Gallery/>
    <section id="o-nas" className="about-section content-section"><div className="about-photo"><Photo scene={scenes[5]}/></div><div><span className="section-kicker">O nás</span><h2>Zahrádky mezi sady</h2>
      <p>CHCI ZAHRÁDKU.cz představuje koncept soukromých sadů o rozloze 300 m². V konfigurátoru si sestavíte návrh a předáte ho k ověření dostupnosti a podmínek pro konkrétní parcelu.</p>
      <p>Podkladem pro model NOVA je zahradní domek značky TŘY D společnosti DOMY Dřevostavby Development s.r.o. Galerie ukazuje, jak může domek v zahradě vypadat.</p>
      <Contact/><a href={nova.source} target="_blank" rel="noreferrer">Domek NOVA u výrobce</a>
    </div></section>
  </main>;
}
