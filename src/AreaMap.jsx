import React, { useState } from 'react';
import { ArrowUpRight, ChevronRight, LocateFixed, MapPin, RotateCcw } from 'lucide-react';
import { locations } from './catalog.js';

export const firstStageCities = [
  {id: 'MBL', lat: 50.412, lng: 14.904},
  {id: 'KLD', lat: 50.148, lng: 14.106},
  {id: 'PRI', lat: 49.690, lng: 14.011}
].map(point => {
  // Same local equirectangular projection as the 760 × 500 vector sheet.
  const x = ((380 + (point.lng - 14.48) * 232) / 760 * 100) + '%';
  const y = ((250 - (point.lat - 50.045) * 360) / 500 * 100) + '%';
  return {...locations.find(item => item.id === point.id), x, y};
});

function CompassRose() {
  return <svg className="atlas-compass" viewBox="0 0 40 58" aria-label="Sever" role="img">
    <text x="20" y="9" textAnchor="middle" fill="currentColor" fontSize="10">S</text>
    <circle cx="20" cy="33" r="12" fill="none" stroke="currentColor" strokeWidth=".65"/>
    <path d="m20 13 4 16 12 4-12 3-4 16-4-16-12-3 12-4Z" fill="#faf7e9" stroke="currentColor" strokeWidth="1"/>
    <path d="m20 13 0 20-4-4Zm0 20v19l4-16Zm0 0h16l-12-4Zm0 0H4l12 3Z" fill="currentColor"/>
  </svg>;
}

export default function AreaMap() {
  const [city, setCity] = useState(null);
  return <section className="area-section content-section" id="lokality" aria-labelledby="area-title">
    <div className="section-heading"><span className="section-kicker"><MapPin size={15}/> Lokality</span><h2 id="area-title">Tři města první etapy</h2></div>
    <div className="area-layout">
      <div className="area-list">
        <p>Vyberte město na mapě nebo v seznamu.</p>
        <div className="atlas-options" role="group" aria-label="Lokality první etapy">
          {firstStageCities.map(item => <button className="atlas-option" type="button" key={item.id} aria-pressed={city?.id === item.id} onClick={() => setCity(item)}>
            <span className="atlas-option-icon"><MapPin size={18} strokeWidth={1.5}/></span>
            <span><strong>{item.name}</strong><small>{item.area}</small></span><ChevronRight size={17}/>
          </button>)}
        </div>
        {city && <div className="atlas-actions">
          <a className="garden-button city-config" href={'/?lokalita=' + city.id + '#konfigurator'}>Vybrat v konfigurátoru <ArrowUpRight size={16}/></a>
          <a className="atlas-directions" href={'https://www.google.com/maps/dir/?api=1&destination=' + encodeURIComponent(city.name + ', Česko')} target="_blank" rel="noreferrer">Trasa do města <ArrowUpRight size={13}/></a>
        </div>}
      </div>
      <figure className="atlas-figure">
        <div className="atlas-window" role="group" aria-label="Interaktivní mapa středních Čech">
          <div className={'atlas-plate' + (city ? ' is-zoomed' : '')} style={{transformOrigin: city ? city.x + ' ' + city.y : 'center'}}>
            <img src="/images/stredni-cechy.svg" width="760" height="500" loading="lazy" alt="Hranice Středočeského kraje, Praha a řeky Vltava a Labe."/>
            {firstStageCities.map(item => <button key={item.id} type="button" className={'atlas-site site-' + item.id} style={{left: item.x, top: item.y}}
              aria-label={'Vybrat na mapě – ' + item.name} aria-pressed={city?.id === item.id} onClick={() => setCity(item)}>
              <span className="atlas-dot"/><span className="atlas-tag">{item.name}</span>
            </button>)}
          </div>
          <span className="atlas-map-title">Střední Čechy</span><CompassRose/>
          {city && <button type="button" className="atlas-reset" onClick={() => setCity(null)}><RotateCcw size={13}/> Celá mapa</button>}
        </div>
        <figcaption className="atlas-caption"><LocateFixed size={15}/><span aria-live="polite">{city ? city.name + ' · ' : ''}Mapa zobrazuje orientační polohu měst.</span></figcaption>
      </figure>
    </div>
  </section>;
}
