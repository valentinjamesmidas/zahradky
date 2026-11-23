# CHCI ZAHRÁDKU.cz

Český konfigurátor soukromého sadu o rozloze 300 m² s Tiny Housem a přímým financováním. React 19, Vite, Tailwind 4, Three.js, React Three Fiber a Drei. Hosting: Cloudflare Pages, poptávky: Cloudflare D1 v EU.

## Spuštění

Node.js 24+, npm, pro regeneraci modelů Blender 4.3+.

```sh
npm ci
npm run dev
npm run build
npm test
```

Vite obsluhuje frontend. Poptávkové API vyžaduje Pages runtime. Pro lokální běh celé aplikace po sestavení:

```sh
npx wrangler d1 migrations apply zahradky-leads --local
npx wrangler pages dev dist
```

Lokální D1 je oddělená od produkce. Testy běží v izolovaném Miniflare/SQLite runtime a nevkládají data do produkční databáze.

## 3D pipeline

```sh
blender --background --python scripts/generate_assets.py
blender --background --python scripts/render_preview.py
```

Pipeline je deterministická. Exportuje 15 GLB souborů s PBR materiály do `public/models/`: parcelu, dvě varianty sadu, čtyři Tiny Housy, hybridní domek NOVA, jednotlivé doplňky, samostatnou solární a vodní technologii a společný model doplňků. Výchozí souřadnice jsou v metrech; Y směřuje vzhůru. Model domu je umístěn samostatně, ostatní kolekce sdílejí souřadnice parcely. GLB soubory jsou součástí repozitáře; Blender není nutný k běžnému sestavení.

Každý GLB má vlastní hranici chyby a procedurální náhradu. Při chybě GLB se zachovává ovladatelná scéna. Při nedostupnosti WebGL aplikace zobrazí lokální render a zachová výběry i cenový výpočet. Prostředí a osvětlení se generují lokálně, bez externího HDRI. Všechny fonty a modely jsou hostovány společně s aplikací.

`work/garden-preview.png` z renderu lze převést do `public/images/garden-preview.webp` pomocí libovolného WebP encoderu. Dodaný WebP je již připraven.

## Konfigurace a ceny

`src/catalog.js` obsahuje všech 10 zadaných lokalit, domy, doplňky a společnou kalkulaci pro klienta i server. Financování používá přesný anuitní vzorec se sazbou 0,079 / 12, akontací 15–70 % a splatností 36–120 měsíců. Výpočet pracuje s nezaokrouhlenou splátkou; zobrazení je zaokrouhlené na celé Kč. U platby v hotovosti je úrok i splátka nulová.

Návrh se ukládá do localStorage. Tlačítko Sdílet návrh kopíruje odkaz s kompletní konfigurací v parametru `navrh`; neobsahuje kontaktní údaje. V poptávce lze návrh stáhnout jako JSON.

## Poptávky a data

`POST /api/leads` validuje kontakt, souhlas, dostupnost ukázkové parcely i celou konfiguraci. Cena se vždy vypočítá na serveru. Kontakt není veřejně čitelný. Databáze má unikátní idempotentní klíč, ochranu proti opakovanému vložení a omezení na šest nových poptávek z jedné adresy za hodinu. Identifikátor pro omezení je jednosměrný hash adresy a hodinového okna; IP se do poptávek neukládá. Požadavky z cizích originů a těla přes 10 kB se odmítají. Starší poptávky se při nové poptávce po 90 dnech mažou; pro garantovanou údržbu bez nových poptávek spusťte následující SQL pravidelně:

```sql
DELETE FROM leads WHERE created_at < unixepoch() - 90*86400;
DELETE FROM rate_limits WHERE window < CAST(unixepoch()/3600 AS INTEGER) - 24;
```

Prohlížení a vyřízení poptávek: Cloudflare dashboard → D1 → zahradky-leads → Console. Poptávka zaznamená požadavek na sedmidenní rezervaci; automaticky neblokuje skutečnou parcelu. Aplikace neposílá e-maily ani SMS. Potvrzení v rozhraní znamená úspěšný zápis do D1.

## Nasazení

Projekt Cloudflare Pages: `zahradky-web`. Konfigurace `wrangler.toml` používá výstup `dist` a vazbu `DB` na EU databázi `zahradky-leads`. Build zabalí API do Pages Advanced Mode `_worker.js`; `_routes.json` směruje na Worker pouze `/api/*`. Statické soubory nevyužívají Function požadavky.

```sh
npm run build
npm test
npx wrangler pages deploy dist --project-name zahradky-web --branch main
```

Použijte Cloudflare přihlášení nebo úzce omezený token s oprávněním Pages Write. Žádná hesla ani API tokeny nepatří do repozitáře. Přímý upload přes připojený Cloudflare nástroj může také využít `scripts/prepare-upload.mjs` a `scripts/upload-assets.py`; krátkodobý upload JWT se zadává skrytě přes stdin. GitHub Actions ověřuje build a testy; automatické publikování vyžaduje samostatné nastavení účtu nebo CI credentials.

Pro vlastní doménu nejprve přidejte doménu v Pages → Custom domains. Apex `chcizahradku.cz` musí mít aktivní Cloudflare DNS zónu; přidání samotného názvu v aplikaci nebo CNAME u jiného poskytovatele připojení apex domény nezajistí. Potom ověřte HTTPS a stav Active.

## Obsah před spuštěním prodeje

Masterplan, stav parcel i architektonické modely jsou ilustrativní a takto označené. Ceny vycházejí ze zadání a nejsou ověřenou nabídkou výrobců. Homologaci, dodavatele, využití pozemku, územní plán, vodní zdroj a pravidla umístění každého mobilního domu je nutné ověřit jednotlivě. SPZ sama o sobě nepovoluje umístění. Nahraďte ukázkovou dostupnost skutečnou evidencí a doplňte právní identitu provozovatele a kompletní informační povinnost ke zpracování údajů před skutečným prodejem.

Font Manrope je dostupný pod SIL Open Font License, viz `public/fonts/OFL.txt`.

## Hybridní dům NOVA — TŘY D

Pátá varianta domu vychází z podkladů https://tryd.cz/hybridni-dum-nova/ ověřených 9. 11. 2026. Půdorys základní varianty je 4 × 3 m; výšky, zapuštění průčelí a členění otvorů jsou odhadnuté z ilustrací výrobce. Jde o zahradní stavbu bez přívěsu a SPZ. Model má sedlovou střechu se stojatými drážkami, tři antracitové stěny, čelo z Thermowoodu, dřevěné zápraží, čtyřdílné průhledné prosklení a otevřený interiér. Dřevo má zabalenou rastrovou texturu, materiály používají Principled BSDF. Nejde o prováděcí dokumentaci.

```sh
blender --background --python scripts/generate_nova.py
blender --background --python scripts/generate_nova.py -- --render
```

Výstupy: `public/models/house_nova.glb` pro web a `public/models/nova.blend` pro další úpravy. Volitelný render vzniká v `work/nova/nova-preview.png`; web používá připravený `public/images/nova-preview.webp`. Kompletní `npm run assets` spouští i tuto pipeline. Ostatní domy zůstávají beze změn. NOVA má vlastní procedurální náhradu pro případ chyby GLB a vlastní statický náhled bez WebGL. Při výběru solární technologie se pro tento sedlový domek zobrazuje samostatný pozemní panelový rám.

Katalogový základ stránky je 310 990 Kč. Zdrojový formulář počítá DPH samostatně. Orientační kalkulace konfigurátoru připočítává 21 % a zaokrouhluje na 376 298 Kč. Doprava, montáž, založení a další dodavatelské příplatky nejsou zahrnuté. Tento základ a vyloučené položky se zobrazují u výběru i v rekapitulaci poptávky. Nejde o závaznou nabídku ani potvrzenou spolupráci s výrobcem.

## Rozšíření vizuálního katalogu (listopad 2026)

Původní zadání je uchováno beze změn v `docs/MASTERPROMPT.md`. Dodaný text končí konfigurací Wrangleru; další část původního chatu nebyla dodána.

Katalog přidává **20 volitelných konceptů**: čtyři autorské domky a šestnáct zahradních doplňků. Nej­de o modely konkrétních dodavatelů ani potvrzené nabídky. Neznámá cena má hodnotu `null`; klient i server ji zahrnou do seznamu položek k nacenění, nikoli do splátky. Rekapitulace a export zachovávají všechny výběry. Starší konfigurace v odkazu a localStorage získají nové přepínače vypnuté.

Doplňky mají vyhrazená místa. Volba jiné varianty ve stejném místě nahradí předchozí; např. bazén nahradí saunu. Terasový nábytek automaticky zapne terasu a vypnutí terasy odebere nábytek. Kontrola na serveru odmítne kolidující výběry. Výsadba se při použití rozšířených doplňků rozmístí po obvodu; jde o ilustrativní kompozici, nikoli projektovou dokumentaci.

Generování (Blender 4.3+, pro WebP Python s Pillow):

```sh
blender -b -t 6 --python scripts/generate_expanded_assets.py
blender -b -t 4 --python scripts/optimize_models.py
blender -b -t 4 --python scripts/render_catalog.py
python scripts/encode_catalog.py
npm run build
npm test
```

Nové GLB jsou v `public/models/expanded`, optimalizované původní modely v `public/models/optimized`, náhledy ve `public/images/options`. Pro běžný build se negenerují znovu. Blender je příprava assetů; v prohlížeči je vykresluje Three.js. Geometrie původních modelů se slučuje podle materiálů: výchozí parcela, sad, domek a terasa mají dohromady 31 mesh primitives místo 689. Číselný report je v `docs/model-optimization.json`. Nejde o tvrzení o konkrétním FPS na všech zařízeních.

Scéna používá vykreslování na vyžádání (`frameloop="demand"`), nejvýše 1,5násobný pixel ratio a jednorázový kontaktní stín pro zvolenou konfiguraci. Modely se načítají až při výběru. Náhledy WebP se načítají postupně. Při výpadku modelu zůstává dostupný náhradní náhled; při nedostupném WebGL funguje statický obrázek a veškerá konfigurace.
