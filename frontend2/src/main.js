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

router.beforeEach((to, from, next) => {
  // Check the state of the dutyDialog variable in the Vuex store
  console.log('before the request!))')
  if (store.state.layoutStore.dutyDialog) {
    // Close the dialog before navigating to the new route
    store.commit('layoutStore/closeDutyDialog', false)
  }
  next()
})

app.mount('#app')