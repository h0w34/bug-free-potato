import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

import router from './routers.js'

loadFonts()

const app = createApp(App)
app.use(router)
app.use(vuetify)
//app.use(vuetify)
app.mount('#app')