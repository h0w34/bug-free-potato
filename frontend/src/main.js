import { createApp } from 'vue'
import App from './App.vue'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import router from './routers.js'
//import { createVuetify } from 'vuetify'
//import 'vuetify/dist/vuetify.min.css'


//const vuetify = createVuetify()

const app = createApp(App)
app.use(router)
//app.use(vuetify)
app.mount('#app')
