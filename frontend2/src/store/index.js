import { createStore } from "vuex";
import { authStore } from "./auth.store";

// can add any number of store modules
const store = createStore({
  modules: {
    authStore,
  },
});

export default store;