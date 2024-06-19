import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import {router} from './router.js'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import store from "./store"
//import { createI18n } from 'vue-i18n'


loadFonts()

const app = createApp(App)
app.component('VueDatePicker', VueDatePicker);
app.use(router)
app.use(vuetify)
app.use(store)

app.mount('#app')