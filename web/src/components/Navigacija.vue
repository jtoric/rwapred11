<script setup lang="ts">
// Navigacijska traka — P7-C2 (svi linkovi, bez auth gating)
</script>

<template>
  <nav class="nav">
    <RouterLink to="/" class="brand">IRON PRESS</RouterLink>

    <div class="grupe">
      <div class="grupa">
        <span class="grupa-oznaka">Admin</span>
        <RouterLink to="/admin/pocetna" class="link">Početna</RouterLink>
        <RouterLink to="/admin/klubovi" class="link">Klubovi</RouterLink>
        <RouterLink to="/admin/natjecanja" class="link">Natjecanja</RouterLink>
      </div>
      <div class="separator" />
      <div class="grupa">
        <span class="grupa-oznaka">Klub</span>
        <RouterLink to="/klub/pocetna" class="link">Početna</RouterLink>
        <RouterLink to="/klub/natjecatelji" class="link">Natjecatelji</RouterLink>
        <RouterLink to="/klub/prijave" class="link">Prijave</RouterLink>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.nav {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 0 2rem;
  height: 56px;
  background: var(--boja-povrsina);
  border-bottom: 2px solid var(--boja-rub);
}

.brand {
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 1.25rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--boja-akcent);
  white-space: nowrap;
}

.grupe {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.grupa {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.grupa-oznaka {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--boja-tekst-mute);
  margin-right: 0.5rem;
}

.link {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  padding: 0.375rem 0.75rem;
  transition: color var(--tranzicija);
}

.link:hover,
.link.router-link-active {
  color: var(--boja-tekst);
}

.link.router-link-active {
  border-bottom: 2px solid var(--boja-akcent);
}

.separator {
  width: 1px;
  height: 24px;
  background: var(--boja-rub);
}
</style>
