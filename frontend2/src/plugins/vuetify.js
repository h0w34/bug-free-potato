// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'

import { ru } from 'vuetify/locale'

export default createVuetify(
{
      locale: {
        locale: 'ru',
        fallback: 'ru',
        messages: { ru}
      }
    }
)

  // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides

