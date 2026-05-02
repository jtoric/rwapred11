<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiNatjecatelje, obrisiNatjecatelja } from '@/services/natjecatelji'
import type { Natjecatelj } from '@/types/natjecatelj'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const auth = useAuthStore()
const obavijesti = useObavijestiStore()
const natjecatelji = ref<Natjecatelj[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')

async function ucitaj(): Promise<void> {
  const clubId = auth.user?.club_id
  if (!clubId) return
  stanje.value = 'ucitavanje'
  try {
    const podaci = await dohvatiNatjecatelje(clubId)
    natjecatelji.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu.'
  }
}

async function obrisi(id: number): Promise<void> {
  if (!confirm('Obrisati natjecatelja?')) return
  const clubId = auth.user?.club_id
  if (!clubId) return
  try {
    await obrisiNatjecatelja(clubId, id)
    obavijesti.uspjeh('Natjecatelj obrisan.')
    await ucitaj()
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri brisanju.')
  }
}

onMounted(ucitaj)

function formatirajDatum(datum: string): string {
  return new Date(datum).toLocaleDateString('hr-HR')
}
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <h1>Natjecatelji</h1>
      <RouterLink to="/klub/natjecatelji/novi" class="gumb-dodaj">+ Dodaj</RouterLink>
    </div>

    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>

    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">
      {{ porukaGreske }}
    </div>

    <div v-else-if="stanje === 'prazno'" class="stanje-poruka muted">
      Nema natjecatelja. Dodajte prvog natjecatelja.
    </div>

    <table v-else class="tablica">
      <thead>
        <tr>
          <th>Ime</th>
          <th>Prezime</th>
          <th>Datum rođenja</th>
          <th>Spol</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="n in natjecatelji" :key="n.id">
          <td>{{ n.first_name }}</td>
          <td>{{ n.last_name }}</td>
          <td>{{ formatirajDatum(n.birth_date) }}</td>
          <td>{{ n.gender }}</td>
          <td class="akcije-celija">
            <RouterLink :to="`/klub/natjecatelji/${n.id}/uredi`" class="akcija">Uredi</RouterLink>
            <button class="akcija akcija--brisanje" @click="obrisi(n.id)">Obriši</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.zaglavlje {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.gumb-dodaj {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 0.5rem 1.25rem;
  background: var(--boja-akcent);
  color: var(--boja-tekst);
}

.gumb-dodaj:hover {
  background: var(--boja-tekst);
  color: var(--boja-pozadina);
}

.akcije-celija {
  display: flex;
  gap: 0.75rem;
}

.akcija {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  transition: color var(--tranzicija);
}

.akcija:hover {
  color: var(--boja-tekst);
}

.akcija--brisanje:hover {
  color: var(--boja-akcent);
}

.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
}

.stanje-poruka.greska {
  border-color: var(--boja-akcent);
  color: var(--boja-akcent);
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

.tablica tbody tr:hover td {
  background: var(--boja-povrsina);
}
</style>
