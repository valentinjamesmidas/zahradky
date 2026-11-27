import {locations, defaultConfig, calculate, money} from './catalog.js';

export const contact = {name: 'Petr Voborník', email: 'zahradky@albetservis.cz', company: 'ALBET servis s.r.o.', ico: '17856361', address: 'Sadová 2447, Rakovník II, 269 01 Rakovník'};
export const offerDate = '27. 11. 2026';
export const sites = [
  {id:'MBL', slug:'mlada-boleslav', caption:'Branka do sadu mezi ovocnými stromy', alt:'Kovová branka v pletivovém plotě a štěrková cesta pod jabloněmi.'},
  {id:'KLD', slug:'kladno', caption:'Pěšky mezi zahrádkami', alt:'Štěrková cesta mezi zahrádkami s lavičkou ve stínu stromu.'},
  {id:'PRI', slug:'pribram', caption:'Víkend u zahradního domku', alt:'Dřevěné čelo zahradního domku, terasa a zeleninový záhon ve stínu jabloně.'}
].map(site => ({...locations.find(location => location.id === site.id), ...site}));

export function weekendConfig(location) {
  return {...defaultConfig, location, house:'nova', orchardXXL:false, terrace:true, beds:true, payment:'cash'};
}
export const sitePath = site => '/lokality/' + site.slug;
export const registry = 'https://ares.gov.cz/ekonomicke-subjekty/res/17856361';
export const buildingGuide = 'https://mmr.gov.cz/cs/ministerstvo/stavebni-pravo/pravo-a-legislativa/novy-stavebni-zakon/metodiky/mobilni-domy';

export function receiptText({code,config,reserve,visit,details}) {
  const sum = calculate(config);
  return ['CHCI ZAHRÁDKU.cz', visit ? 'Zájem o termín prohlídky' : 'Kopie nezávazné poptávky',code,
    sum.location.name, ...(visit ? [] : [
      'Modelová parcela č. ' + config.plot + ' · 300 m²',
      ...sum.items.map(item => item.name + ' — ' + (item.price == null ? 'k nacenění' : money(item.price))),
      'Součet naceněných položek — ' + money(sum.total),
      'Doprava, osazení, napojení a roční provoz se ověřují zvlášť.',
      ...(config.payment === 'finance' ? ['Model splátek: akontace ' + money(sum.down) + ', ' + sum.n + ' × ' + money(sum.monthly) + ', celkem včetně akontace ' + money(sum.paidTotal) + '.'] : []),
      reserve ? 'Žádost o blokaci na sedm dní čeká na výslovné potvrzení.' : 'Bez žádosti o rezervaci.'
    ]), ...(details ? [details.name,details.email,details.phone,details.note].filter(Boolean) : []),
    visit ? 'Termín zatím není vypsán. Jakmile bude znám, kontaktuje vás Petr Voborník.' : 'Petr Voborník ověří dostupnost a podmínky zvolené sestavy.',
    contact.company + ' · IČO ' + contact.ico, contact.name + ' · ' + contact.email].join('\n');
}
