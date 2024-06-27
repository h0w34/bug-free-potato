// Styles
import '@mdi/font/css/materialdesignicons.css'
import '@mdi/light-font/css/materialdesignicons-light.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'
import {VTreeview} from "vuetify/labs/VTreeview";

import { ru } from 'vuetify/locale'

export default createVuetify(
{
     components: {
        VTreeview,
     },
      locale: {
        locale: 'ru',
        fallback: 'ru',
        messages: { ru}
      }
}
)

  // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides

