import { createStore } from "vuex";
import { authStore } from "./auth.store";
import {layoutStore} from "./layout.store";

// can add any number of store modules
const store = createStore({
  modules: {
    authStore,
    layoutStore
  },
});

export default store;