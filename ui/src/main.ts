import { createApp } from 'vue'

import 'vfonts/Lato.css'
// Monospace Font
import 'vfonts/FiraCode.css'
import '@/scss/app.scss'

import naive  from 'naive-ui'

import axios from "@/utils/api"

import App from './App.vue'
import router from './router'
import store from './store'

createApp(App).use(axios).use(naive).use(store).use(router).mount('#app')
