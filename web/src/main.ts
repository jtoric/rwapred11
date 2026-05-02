import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/globalno.css'

const aplikacija = createApp(App)
aplikacija.use(createPinia())
aplikacija.use(router)
aplikacija.mount('#app')
