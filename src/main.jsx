import React, { lazy, Suspense, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Leaf, Menu, X } from 'lucide-react';
import Landing from './Landing.jsx';
import './style.css';
import './landing.css';

import {SiteDetail} from './Offers.jsx';
import {sites, sitePath, contact} from './offer.js';
const Configurator = lazy(() => import('./App.jsx'));
const links = [
  ['Úvod', 'uvod'], ['Lokality', 'lokality'], ['Konfigurátor', 'konfigurator'], ['Galerie', 'galerie'], ['O nás', 'o-nas']
];

function Header({ section, isConfig, detail }) {
  const [open, setOpen] = useState(false);
  const [atTop, setAtTop] = useState(() => window.scrollY < 16);
  useEffect(() => {
    const update = () => setAtTop(window.scrollY < 16);
    update();
    window.addEventListener('scroll', update, { passive: true });
    return () => window.removeEventListener('scroll', update);
  }, []);
  const toggle = React.useRef(null);
  const header = React.useRef(null);
  useEffect(() => {
    if (!open) return;
    function dismiss(event) {
      if (event.key === 'Escape') {
        setOpen(false);
        toggle.current?.focus();
      }
    }
    function outside(event) {
      if (!header.current?.contains(event.target)) setOpen(false);
    }
    window.addEventListener('keydown', dismiss);
    window.addEventListener('pointerdown', outside);
    window.addEventListener('focusin', outside);
    return () => {
      window.removeEventListener('keydown', dismiss);
      window.removeEventListener('pointerdown', outside);
      window.removeEventListener('focusin', outside);
    };
  }, [open]);
  return <header className={'garden-header' + (!isConfig && !detail ? ' on-landing' : '') + (atTop && !open ? ' at-top' : '')} ref={header}>
    <div className="header-content">
      <a className="brand" href="/#uvod" aria-label="CHCI ZAHRÁDKU.cz – úvod" onClick={() => setOpen(false)}>
        <span className="brand-mark"><Leaf size={25} strokeWidth={1.4}/></span>
        <span>CHCI ZAHRÁDKU<span className="brand-cz">.cz</span></span>
      </a>
      <nav id="hlavni-menu" className={open ? 'is-open' : ''} aria-label="Hlavní navigace">
        {links.map(([title, id]) => <a key={id} href={'/#' + id}
          aria-current={(isConfig ? id === 'konfigurator' : id === section) ? 'location' : undefined}
          onClick={() => setOpen(false)}>{title}</a>)}
      </nav>
      <a className="garden-button nav-cta" href="/#konfigurator" onClick={() => setOpen(false)}>Navrhnout zahrádku</a>
      <button ref={toggle} className="menu-toggle" aria-label={open ? 'Zavřít menu' : 'Otevřít menu'}
        aria-controls="hlavni-menu" aria-expanded={open} onClick={() => setOpen(!open)}>
        {open ? <X/> : <Menu/>}
      </button>
    </div>
  </header>;
}

function Site() {
  const [url, setUrl] = useState(() => new URL(location.href));
  useEffect(() => {
    const changed = () => setUrl(new URL(location.href));
    window.addEventListener('hashchange', changed);
    window.addEventListener('popstate', changed);
    return () => {
      window.removeEventListener('hashchange', changed);
      window.removeEventListener('popstate', changed);
    };
  }, []);
  const site = sites.find(item => sitePath(item) === url.pathname.replace(/\/$/, ''));
  const anchor = url.hash.slice(1);
  const isConfig = ['konfigurator', 'otazky', 'jak-to-funguje'].includes(anchor) ||
    (!anchor && ['navrh', 'dum'].some(key => url.searchParams.has(key)));
  useEffect(() => {
    document.title = (site ? site.name + ' · zahrádky a prohlídky' : isConfig ? 'Konfigurátor zahrádky' : 'Zahrádkářské kolonie Střední Čechy') + ' | CHCI ZAHRÁDKU.cz';
    // A deep link can arrive before React or the configurator chunk has mounted its target.
    if (!anchor) return;
    function scroll() {
      const target = document.getElementById(anchor);
      if (!target) return false;
      target.scrollIntoView({behavior: 'instant'});
      return true;
    }
    if (scroll()) return;
    const observer = new MutationObserver(() => { if (scroll()) observer.disconnect(); });
    observer.observe(document.getElementById('root'), { childList: true, subtree: true });
    return () => observer.disconnect();
  }, [isConfig, anchor, site]);
  return <>
    <Header key={url.href} detail={!!site} section={site ? 'lokality' : anchor || 'uvod'} isConfig={isConfig}/>
    {isConfig ? <Suspense fallback={<main className="config-loading">Načítání konfigurátoru…</main>}><Configurator/></Suspense> : site ? <SiteDetail site={site}/> : <Landing/>}
    <footer className="garden-footer"><a href="/#uvod"><Leaf size={18}/> CHCI ZAHRÁDKU.cz</a><a href="/#lokality">Lokality</a><a href="/#konfigurator">Konfigurátor</a><a href={"mailto:"+contact.email}>{contact.email}</a></footer>
  </>;
}

createRoot(document.getElementById('root')).render(<React.StrictMode><Site/></React.StrictMode>);
