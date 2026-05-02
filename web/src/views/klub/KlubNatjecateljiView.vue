<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { dohvatiNatjecatelje } from '@/services/natjecatelji'
import type { Natjecatelj } from '@/types/natjecatelj'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const auth = useAuthStore()
const natjecatelji = ref<Natjecatelj[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')

onMounted(async () => {
  const clubId = auth.user?.club_id
  if (!clubId) return

  try {
    const podaci = await dohvatiNatjecatelje(clubId)
    natjecatelji.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu natjecatelja.'
  }
})

function formatirajDatum(datum: string): string {
  return new Date(datum).toLocaleDateString('hr-HR')
}
</script>

<template>
  <div class="pogled">
    <h1>Natjecatelji</h1>

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
        </tr>
      </thead>
      <tbody>
        <tr v-for="n in natjecatelji" :key="n.id">
          <td>{{ n.first_name }}</td>
          <td>{{ n.last_name }}</td>
          <td>{{ formatirajDatum(n.birth_date) }}</td>
          <td>{{ n.gender }}</td>
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
