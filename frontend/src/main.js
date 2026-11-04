import './index.css'

// The student portal is Persian-first in this fork.
document.documentElement.lang = 'fa'
document.documentElement.dir = 'rtl'

import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import { createPinia } from 'pinia'
// import '../polyfills'

import {
  Button,
  Card,
  Input,
  setConfig,
  frappeRequest,
  resourcesPlugin,
} from 'frappe-ui'

// create a pinia instance
let pinia = createPinia()

let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)

app.use(pinia)
app.use(router)
app.use(resourcesPlugin)

app.component('Button', Button)
app.component('Card', Card)
app.component('Input', Input)

router.isReady().then(() => {
  app.mount('#app')
})
