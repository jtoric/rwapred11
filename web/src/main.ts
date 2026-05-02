import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/globalno.css'

const pinia = createPinia()
const aplikacija = createApp(App)
aplikacija.use(pinia)
aplikacija.use(router)

// Ako postoji token, dohvati korisnika PRIJE mounta da guard nikad ne vidi
// nedefiniranog usera — token u localStorage, korisnik još nije učitan
if (localStorage.getItem('access_token')) {
  const { useAuthStore } = await import('./stores/auth')
  try {
    await useAuthStore().dohvatiMene()
  } catch {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
}

aplikacija.mount('#app')
