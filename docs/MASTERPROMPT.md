# ROLE & AUTONOMOUS EXECUTION OBJECTIVE
Act as an elite Creative Technologist, Senior Full-Stack Developer, 3D Technical Artist (Blender Python API), and DevOps Engineer.

Your mission is to autonomously build, generate 3D assets for, version-control, and deploy a production-ready, hyper-modern web application for **"chcizahradku.cz"** – a Czech real estate & prop-tech platform selling turnkey 300 m² off-grid orchard gardens ("Ovocné sady") with Western European mobile Tiny Houses and direct 10-year Vendor Financing (7,9 % p.a., bez banky).

You must execute the entire pipeline end-to-end:
1. Generate 3D `.glb` architectural models using **Blender (headless Python `bpy` script)**.
2. Build the **React + Vite + Tailwind + Three.js (`@react-three/fiber` & `@react-three/drei`)** web application with a **BMW-style 3D Configurator**.
3. Initialize Git and create a new **GitHub repository named `zahradky-web`**.
4. Build and deploy the production app directly to **Cloudflare Pages** (`zahradky-web` / `chcizahradku.cz`).

All UI text, labels, and copy in the web application MUST be in Czech.

---

# PHASE 1: BLENDER 3D ASSET GENERATION PIPELINE (`scripts/generate_assets.py`)
Write a complete Blender Python script (`scripts/generate_assets.py`) and run it in headless mode:
`blender --background --python scripts/generate_assets.py`

### What the Blender Python (`bpy`) script must model, texture (PBR Principled BSDF), and export to `public/models/garden_assets.glb` (or individual `.glb` files):
1. **Plot Base & Fencing (`plot_base.glb`):**
   - 300 m² plot (15m × 20m) with chamfered terrain, gravel parking pad, forestry wooden post-and-wire fencing, sliding GSM entrance gate, and utility water meter shaft.
2. **Orchard Trees (`orchard_trees.glb`):**
   - Standard pack (4 young fruit trees) and XXL pack (8 mature apple/pear trees with organic icosphere/subdivided canopies and bark materials + berry bushes).
3. **4 Western European Tiny Houses on Vlemmix Trailers (with wheels, drawbar, license plate holder, and roof solar panels):**
   - `tiny_liberte.glb`: **Liberté Tiny Shell (NL)** – 20 m², vertical larch cladding, French double doors.
   - `tiny_millhome.glb`: **Mill Home Nordic (NL)** – 25 m², asymmetric roof, panoramic corner glazing, sleeping loft.
   - `tiny_baluchon.glb`: **Baluchon Cedar Edition (FR)** – 24 m², red cedar + standing seam anthracite metal, chimney stove pipe.
   - `tiny_anna.glb`: **Cabin ANNA Glamping (NL)** – 28 m², sliding glass shell and biophilic timber ribs.
4. **Outdoor & Off-Grid Add-ons (`addons.glb`):**
   - `terrace`: 18 m² larch timber deck on ground screws (`zemní vruty`).
   - `corten_beds`: 4× raised garden beds with weathered Corten steel shader (`Roughness: 0.75, Metallic: 0.3, BaseColor: #9A4624`).
   - `firepit_pergola`: Architectural timber pergola with string lights (`festony` with emissive nodes for night mode) and circular firepit with seating.
   - `offgrid_tech`: Victron Energy outdoor battery cabinet + rooftop monocrystalline solar array + underground rainwater tank hatch.

*Fallback safety:* In the React Three.js loader (`useGLTF`), implement an automatic procedural mesh fallback so if the `.glb` files are still compiling or running in a cloud container without the Blender binary, the 3D configurator renders high-detail procedural Three.js architectural meshes seamlessly without crashing.

---

# PHASE 2: DESIGN SYSTEM ("BIOPHILIC LUXURY MEETS BMW CONFIGURATOR")
- **Aesthetic:** Ultra-clean architectural minimalism (Penta Real Estate / Bjarke Ingels Group vibe) combined with the interactive dark-glass HUD of the BMW Individual 3D Configurator.
- **Color Palette:**
  - Deep Forest Obsidian: `#0B1310` (Primary dark background)
  - Architectural Pine: `#14261F` (Cards & panels)
  - Warm Cedar / Corten Accent: `#D49A6A` (Primary luxury CTA buttons & highlights)
  - Emerald Signal: `#10B981` (Available plots, active states)
  - Glass HUD: `bg-black/60 backdrop-blur-xl border border-white/10`

---

# PHASE 3: APPLICATION STRUCTURE & BMW-STYLE 3D CONFIGURATOR

## 1. Header & Hero Section (`chcizahradku.cz`)
- Sticky glass top bar with brand **CHCI ZAHRÁDKU.cz** | *Soukromé sady & Off-Grid Glamping*.
- Headline: **"Vlastní 300 m² sad a moderní Tiny House. 6 minut od vašeho bytu. Bez banky."**
- Subheadline: *"Přeměňujeme půdu u 10 okresních měst na privátní oplocené oázy s vlastní vodou, ostrovní solární elektrárnou a financováním na 10 let přímo od developera (7,9 % p.a.)."*
- Key badges: `300 m² parcela` | `30 zahrad na 1 ha` | `Akontace od 180 000 Kč` | `100 % Legální sadový model + Tiny House na SPZ`.

## 2. Interactive 3D Viewport (Left/Center 70% screen)
- Loads the Blender `.glb` collections (or procedural fallback) with realistic shadows, HDRI environment lighting, and smooth `OrbitControls` + camera `lerp` transitions.
- **Top Floating Camera & Lighting Bar:**
  - Camera Presets: `1. Pohled z dronu (Celek)` | `2. Detail Tiny Housu` | `3. Pohled z terasy do sadu` | `4. Masterplan areálu (30 parcel)`.
  - Lighting Toggle: `☀️ Denní slunce` vs. `🌙 Večerní glamping (rozsvícené festony, ohniště a teplé světlo v okně Tiny Housu)`.

## 3. Right-Hand Configurator HUD (5 Sequential Steps)

### KROK 1: Výběr lokality (Top 10 okresních měst) & Parcely (1–30)
Include this exact dataset of 10 Czech locations:
1. **Kladno (Vinařická hora / Pletený Újezd)** – 5 min od sídlišť Kročehlavy a Rozdělov | Půda III.–IV. tř. | Základní cena: `1 200 000 Kč`
2. **Mladá Boleslav (Bradlec / Kosmonosy)** – 6 min od Severního sídliště | Základní cena: `1 200 000 Kč`
3. **Kolín (Jižní svahy – Pašinka)** – 7 min z centra a sídliště | Základní cena: `1 150 000 Kč`
4. **Příbram (Podbrdské svahy)** – 5 min od sídliště Drkolnov | Základní cena: `990 000 Kč`
5. **Chomutov & Jirkov (Podkrušnohoří)** – 6 min od sídlišť | Základní cena: `890 000 Kč`
6. **Most (Jižní rekultivované sady)** – 5 min z města | Základní cena: `850 000 Kč`
7. **Karviná & Havířov (Těšínská pahorkatina)** – 7 min od Šumbarku a Ráje | Základní cena: `950 000 Kč`
8. **Teplice (Krupka / Modlany svahy)** – 6 min ze sídliště Trnovany | Základní cena: `950 000 Kč`
9. **Přerov (Severní svahy – Čekyně)** – 6 min z Předmostí | Základní cena: `990 000 Kč`
10. **Sokolov (Západní terasy)** – 5 min ze sídliště Michal | Základní cena: `820 000 Kč`

*Interactive 30-Plot Masterplan Selector:* Inside Step 1, render an interactive grid of **30 plots (Parcela č. 1 až 30, each 300 m²)** along a central backbone road. Color-code them: `Volná` (Emerald), `Rezervovaná` (Amber), `Prodaná` (Muted). Clicking any free plot selects it and updates the 3D scene and summary.

### KROK 2: Sad & Venkovní Architektura
- **Standard v ceně pozemku (0 Kč):** Oplocení sadu proti zvěří, příjezd po štěrkové cestě s GSM bránou, vodoměrná šachta (užitková voda z vrtu), 4 ks mladých ovocných stromů.
- **Volitelné 3D doplňky:**
  - `Vzrostlý ovocný sad XXL (8 vzrostlých stromů + jedlé keře)` (+45 000 Kč)
  - `Modřínová terasa na zemních vrutech (18 m²)` (+85 000 Kč)
  - `Sada 4× vyvýšený záhon z Corten oceli vč. substrátu` (+38 000 Kč)
  - `Designové ohniště s dřevěným posezením a pergolou s festony` (+62 000 Kč)

### KROK 3: Západoevropský Off-Grid Tiny House (S homologací a SPZ)
- `Bez Tiny Housu (Pouze připravený sad 300 m²)` (+0 Kč)
- `Liberté Tiny Shell (Nizozemsko) – 20 m², modřín, francouzská okna, podvozek Vlemmix s SPZ` (+790 000 Kč)
- `Mill Home Nordic (Nizozemsko) – 25 m², rohové prosklení, spací loft, koupelna, kuchyně` (+1 190 000 Kč)
- `Baluchon Cedar Edition (Francie) – 24 m², červený cedr, falcovaný plech, krbová kamna` (+1 390 000 Kč)
- `Cabin ANNA Glamping (Nizozemsko) – 28 m², posuvné prosklené stěny, biofilní design` (+1 690 000 Kč)

### KROK 4: Off-Grid Technologie & Autonomie
- `Základní přípojka užitkové vody z centrálního vrtu` (V ceně – 0 Kč)
- `Ostrovní solární elektrárna Victron Energy (3 kWp panely + 5 kWh LiFePO4 baterie)` (+95 000 Kč)
- `Spalovací / separační eko-toaleta Cinderella Freedom (bez nutnosti jímky)` (+89 000 Kč)
- `Podzemní retenční nádrž na dešťovou vodu 4 000 l s automatickou závlahou sadu` (+68 000 Kč)

### KROK 5: Kalkulačka Vendor Financingu (10 let, 7,9 % p.a.)
- Toggle: `Splátky přímo od developera (7,9 % p.a.)` vs `Platba v hotovosti`.
- **Akontace (při podpisu):** Slider `15 %` až `70 %` (Default `15 %` = `180 000 Kč` při ceně 1,2 mil. Kč).
- **Doba splácení:** Slider `3 roky` až `10 let` (Default `10 let / 120 měsíců`).
- **Pevný úrok:** `7,9 % p.a.` (Bez banky, bez dokládání příjmů, zajištěno výhradou vlastnického práva v katastru).
- **Exact Annuity Formula:**
  `M = P * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)` where `P = TotalPrice - DownPayment`, `r = 0.079 / 12`, `n = Years * 12`.

## 4. Sticky BMW Summary Dock & Lead Capture Modal
- Bottom dock shows: `Lokalita + Číslo parcely (300 m²)` | `Celková cena` | `Akontace dnes` | `Měsíční splátka` | CTA: **"Dokončit konfiguraci a odeslat poptávku"**.
- Clicking CTA opens the **Rezervační & Poptávkový Modal** with complete configuration recap, contact inputs (`Jméno a příjmení`, `Telefon`, `E-mail`, `Poznámka`), a 7-day reservation checkbox, and generates a unique configuration code (e.g. `#CZ-KLD-14-892`).

---

# PHASE 4: GITHUB REPOSITORY (`zahradky-web`) & CLOUDFLARE PAGES DEPLOYMENT
After generating all files and verifying `npm run build` succeeds with zero errors, execute these exact DevOps steps:

1. **Create Cloudflare Configuration (`wrangler.toml`):**
   ```toml
   name = "zahradky-web"
   compatibility_date = "2026-11-01"
   pages_build_output_dir = "dist"