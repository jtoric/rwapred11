<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiNatjecanje } from '@/services/natjecanja'
import { dohvatiPrijave } from '@/services/prijave'
import { dohvatiKlubove } from '@/services/klubovi'
import { dohvatiNatjecatelje } from '@/services/natjecatelji'
import { useFilteriPrijava, SVE_KATEGORIJE } from '@/composables/useFilteriPrijava'
import type { PrijavaProsirena } from '@/composables/useFilteriPrijava'
import type { Klub } from '@/types/klub'
import type { Natjecanje } from '@/types/natjecanje'
import StatusBadge from '@/components/StatusBadge.vue'

const route = useRoute()
const obavijesti = useObavijestiStore()
const compId = Number(route.params['compId'])

const natjecanje = ref<Natjecanje | null>(null)
const prijave = ref<PrijavaProsirena[]>([])
const klubovi = ref<Klub[]>([])
const ucitava = ref(true)

const {
  filterStatus,
  filterKlubId,
  filterLifter,
  filterKategorija,
  trenutnaStranica,
  ukupnoStranica,
  filtrirane,
  prikazane,
  prethodna,
  sljedeca,
} = useFilteriPrijava(prijave)

onMounted(async () => {
  try {
    const [nat, sveKlubove, svePrijave] = await Promise.all([
      dohvatiNatjecanje(compId),
      dohvatiKlubove(),
      dohvatiPrijave(compId),
    ])

    natjecanje.value = nat
    klubovi.value = sveKlubove

    // Dohvati liftera po klubu da bi saznali club_id za svaku prijavu
    const lifterMap = new Map<number, { klub_id: number; klub_naziv: string }>()
    await Promise.all(
      sveKlubove.map(async (k) => {
        const lifteri = await dohvatiNatjecatelje(k.id)
        for (const l of lifteri) {
          lifterMap.set(l.id, { klub_id: k.id, klub_naziv: k.name })
        }
      }),
    )

    prijave.value = svePrijave.map((p) => {
      const info = lifterMap.get(p.lifter_id)
      return {
        ...p,
        klub_id: info?.klub_id ?? 0,
        klub_naziv: info?.klub_naziv ?? '—',
      }
    })
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri dohvatu prijava.')
  } finally {
    ucitava.value = false
  }
})

function formatirajDatum(d: string | null): string {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('hr-HR')
}
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <div>
        <RouterLink to="/admin/natjecanja" class="natrag">← Natjecanja</RouterLink>
        <h1>{{ natjecanje?.name ?? 'Prijave' }}</h1>
      </div>
    </div>

    <div v-if="ucitava" class="stanje-poruka muted">Učitavanje...</div>

    <template v-else>
      <!-- Filteri -->
      <div class="filteri">
        <select v-model="filterStatus" class="select-filter">
          <option value="sve">Sve prijave</option>
          <option value="active">Aktivne</option>
          <option value="withdrawn">Odjavljene</option>
        </select>

        <select v-model="filterKlubId" class="select-filter">
          <option value="sve">Svi klubovi</option>
          <option v-for="k in klubovi" :key="k.id" :value="k.id">{{ k.name }}</option>
        </select>

        <input
          v-model="filterLifter"
          class="input-filter"
          placeholder="Traži natjecatelja..."
          type="text"
        />

        <select v-model="filterKategorija" class="select-filter">
          <option value="">Sve kategorije</option>
          <option v-for="kat in SVE_KATEGORIJE" :key="kat" :value="kat">{{ kat }} kg</option>
        </select>
      </div>

      <!-- Tablica -->
      <div v-if="filtrirane.length === 0" class="stanje-poruka muted">
        Nema prijava za odabrane filtere.
      </div>

      <template v-else>
        <table class="tablica">
          <thead>
            <tr>
              <th>Natjecatelj</th>
              <th>Klub</th>
              <th>Kategorija</th>
              <th>Total</th>
              <th>Status</th>
              <th>Prijavljeno</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in prikazane" :key="p.id">
              <td>{{ p.lifter.first_name }} {{ p.lifter.last_name }}</td>
              <td>{{ p.klub_naziv }}</td>
              <td>{{ p.category }} kg</td>
              <td>{{ p.total }} kg</td>
              <td><StatusBadge :status="p.status" /></td>
              <td class="muted">{{ formatirajDatum(p.registered_at) }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Paginacija -->
        <div class="paginacija">
          <button class="pag-gumb" :disabled="trenutnaStranica === 1" @click="prethodna">
            ← Prethodno
          </button>
          <span class="muted">Stranica {{ trenutnaStranica }} od {{ ukupnoStranica }}</span>
          <button
            class="pag-gumb"
            :disabled="trenutnaStranica === ukupnoStranica"
            @click="sljedeca"
          >
            Sljedeće →
          </button>
        </div>
      </template>
    </template>
  </div>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.zaglavlje { display: flex; align-items: flex-start; justify-content: space-between; }

.natrag {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  display: block;
  margin-bottom: 0.5rem;
}

.natrag:hover { color: var(--boja-tekst); }

.filteri {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.select-filter,
.input-filter {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.5rem 0.75rem;
  font-size: 0.8rem;
  font-family: var(--font-body);
}

.select-filter:focus,
.input-filter:focus {
  outline: none;
  border-color: var(--boja-akcent);
}

.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
}

.tablica {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.tablica th {
  text-align: left;
  padding: 0.625rem 1rem;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
  border-bottom: 2px solid var(--boja-rub);
}

.tablica td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--boja-rub);
}

.tablica tbody tr:hover td { background: var(--boja-povrsina); }

.paginacija {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  font-size: 0.8rem;
}

.pag-gumb {
  font-family: var(--font-body);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  background: none;
  border: 1px solid var(--boja-rub);
  padding: 0.375rem 0.875rem;
  cursor: pointer;
}

.pag-gumb:hover:not(:disabled) { color: var(--boja-tekst); border-color: var(--boja-tekst-mute); }
.pag-gumb:disabled { opacity: 0.35; cursor: not-allowed; }
</style>
