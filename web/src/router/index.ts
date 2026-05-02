import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PrijavaView from '@/views/PrijavaView.vue'
import NadzornaPlocaView from '@/views/NadzornaPlocaView.vue'
import NepoznatoView from '@/views/NepoznatoView.vue'
import AdminPocetnaView from '@/views/admin/AdminPocetnaView.vue'
import AdminKluboviView from '@/views/admin/AdminKluboviView.vue'
import AdminNatjecanjaView from '@/views/admin/AdminNatjecanjaView.vue'
import KlubPocetnaView from '@/views/klub/KlubPocetnaView.vue'
import KlubNatjecateljiView from '@/views/klub/KlubNatjecateljiView.vue'
import KlubPrijaveView from '@/views/klub/KlubPrijaveView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/prijava',
    },
    {
      path: '/prijava',
      component: PrijavaView,
      meta: { layout: 'gost', javno: true },
    },
    {
      path: '/pocetna',
      component: NadzornaPlocaView,
      meta: { layout: 'aplikacija' },
    },
    {
      path: '/admin',
      meta: { layout: 'aplikacija', uloga: 'admin' },
      children: [
        { path: 'pocetna', component: AdminPocetnaView },
        { path: 'klubovi', component: AdminKluboviView },
        { path: 'natjecanja', component: AdminNatjecanjaView },
      ],
    },
    {
      path: '/klub',
      meta: { layout: 'aplikacija', uloga: 'klub' },
      children: [
        { path: 'pocetna', component: KlubPocetnaView },
        { path: 'natjecatelji', component: KlubNatjecateljiView },
        { path: 'prijave', component: KlubPrijaveView },
      ],
    },
    {
      path: '/:catchAll(.*)*',
      component: NepoznatoView,
      meta: { layout: 'gost', javno: true },
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.javno) return true

  if (!auth.isAuthenticated) return '/prijava'

  // Prijavljeni korisnik na login stranici → preusmjeri na svoju početnu
  if (to.path === '/prijava') {
    return auth.isAdmin ? '/admin/pocetna' : '/klub/pocetna'
  }

  // Provjera uloge za zaštićene sekcije
  if (to.meta.uloga === 'admin' && !auth.isAdmin) return '/klub/pocetna'
  if (to.meta.uloga === 'klub' && !auth.isClub) return '/admin/pocetna'

  return true
})

export default router
