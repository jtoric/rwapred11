# Frontend — Iron Press

Vue 3 + TypeScript + Vite SPA za sustav prijave na powerlifting natjecanja.

## Struktura

```
src/
├── main.ts                  # Bootstrap: Pinia + Router + mount
├── App.vue                  # Layout switcher (route.meta.layout)
├── router/index.ts          # Rute s meta: { layout, javno, uloga }
├── stores/                  # Pinia storeovi
│   ├── auth.ts              # Autentikacija (token, korisnik)
│   └── obavijesti.ts        # Toast notifikacije
├── services/                # API pozivi po domeni
│   ├── api.ts               # Bazni HTTP klijent (fetch wrapper)
│   ├── natjecatelji.ts
│   ├── natjecanja.ts
│   ├── prijave.ts
│   └── klubovi.ts
├── types/                   # TypeScript tipovi/interfejsi
│   ├── api.ts               # ApiGreska, ZahtjevOpcije
│   ├── auth.ts              # TokenOdgovor, KorisnikPodaci
│   ├── natjecatelj.ts
│   ├── natjecanje.ts
│   ├── prijava.ts
│   └── index.ts             # Re-exporti
├── utils/
│   ├── faza.ts              # izracunajFazu(), dozvoljeno()
│   ├── validacija.ts        # neprazno(), validanDatumProslost()
│   └── csv.ts               # uCsv(), preuzmiCsv()
├── composables/
│   └── useFilteriPrijava.ts # Client-side filteri + paginacija
├── layouts/
│   ├── LayoutGost.vue       # Za javne stranice (login, 404)
│   └── LayoutAplikacija.vue # Sa navigacijom
├── components/
│   ├── Navigacija.vue
│   ├── Obavijest.vue        # Jedna toast poruka
│   ├── Obavijesti.vue       # Kontejner za toastove
│   ├── Tablica.vue          # Generic tablica s loading/error/empty
│   ├── FormaPolje.vue       # Input wrapper s labelom i greškom
│   ├── Gumb.vue             # Gumb s loading/disabled stanjima
│   ├── Modal.vue            # Teleport-based modal
│   └── StatusBadge.vue      # Badge za status prijave
├── views/
│   ├── PrijavaView.vue
│   ├── NadzornaPlocaView.vue
│   ├── NepoznatoView.vue
│   ├── admin/
│   │   ├── AdminPocetnaView.vue
│   │   ├── AdminKluboviView.vue
│   │   ├── AdminNatjecanjaView.vue
│   │   ├── NatjecanjaFormaView.vue
│   │   └── AdminPrijaveView.vue
│   └── klub/
│       ├── KlubPocetnaView.vue
│       ├── KlubNatjecateljiView.vue
│       ├── NatjecateljFormaView.vue
│       ├── NatjecanjaView.vue
│       ├── PrijavaFormaView.vue
│       └── KlubPrijaveView.vue
└── styles/
    ├── tokens.css           # CSS custom properties (boje, fontovi)
    ├── reset.css            # Normalizacija
    └── globalno.css         # Globalni stilovi + import tokena
```

## Konvencije

### Imenovanje
- Identifikatori i komentari: **hrvatski**
- Public API storeova: **engleski** (`isAuthenticated`, `isAdmin`, `user`, `logout`)
- Komponente: PascalCase, `.vue`
- Viewovi: sufiks `View` (npr. `PrijavaView.vue`)

### Komponente
- Composition API, `<script setup lang="ts">` u svakom fileoviu
- Strict TypeScript: `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`
- Nema UI biblioteka — custom CSS s design tokenima

### CSS strategija
- Design tokeni u `styles/tokens.css` (CSS custom properties)
- Scoped stilovi u komponentama
- Nema globalnih klasa osim utility-ja (`.muted`, `.akcent`, `.uspjeh`)
- Hover na gumbima: instant snap (bez `transition`)

### Routing
- `route.meta.layout`: `'gost'` | `'aplikacija'` — `App.vue` bira layout
- `route.meta.javno`: `true` za rute bez autentikacije
- `route.meta.uloga`: `'admin'` | `'klub'` za route guards

### Pinia storeovi
- `auth.ts`: privatno stanje na hrvatskom, public API na engleskom
- `obavijesti.ts`: `dodaj(poruka, vrsta)`, `ukloni(id)`

### API servis
- `services/api.ts`: fetch wrapper s Authorization headerom
- Token se čita direktno iz `localStorage` (izbjegava circular import s auth storeom)
- 401 → singleton refresh → retry
- Non-OK odgovor → baci `ApiGreska`

## Aesthetic: Iron Press

Brutalistički dizajn inspiriran powerlifting plakatima 70-ih.

| Token | Vrijednost |
|---|---|
| `--boja-pozadina` | `#0e0e0e` |
| `--boja-povrsina` | `#1a1a1a` |
| `--boja-rub` | `#2e2e2e` |
| `--boja-tekst` | `#ede6d3` |
| `--boja-tekst-mute` | `#8a8579` |
| `--boja-akcent` | `#c8451a` |
| `--boja-uspjeh` | `#7a8c3a` |

- **Display font:** Big Shoulders Display 700/900
- **Body font:** JetBrains Mono 400/700
- **Tranzicija:** `160ms cubic-bezier(0.2, 0.8, 0.2, 1)`
- **Hover na gumbima:** instant snap (bez tranzicije)

## Pokretanje

```bash
cd web
npm install
npm run dev          # http://localhost:5173
npm run typecheck    # provjera tipova
npm run lint         # ESLint
npm run format       # Prettier
npm run build        # produkcijski build
```
