import { createRouter, createWebHistory } from 'vue-router'
import PrijavaView from '@/views/PrijavaView.vue'
import NadzornaPlocaView from '@/views/NadzornaPlocaView.vue'
import NepoznatoView from '@/views/NepoznatoView.vue'
import AdminPocetnaView from '@/views/admin/AdminPocetnaView.vue'
import AdminKluboviView from '@/views/admin/AdminKluboviView.vue'
import AdminNatjecanjaView from '@/views/admin/AdminNatjecanjaView.vue'
import KlubPocetnaView from '@/views/klub/KlubPocetnaView.vue'
import KlubNatjecateljiView from '@/views/klub/KlubNatjecateljiView.vue'
import KlubPrijaveView from '@/views/klub/KlubPrijaveView.vue'

declare module 'vue-router' {
  interface RouteMeta {
    layout?: 'gost' | 'aplikacija'
    javno?: boolean
    uloga?: 'admin' | 'klub'
  }
}

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

export default router
