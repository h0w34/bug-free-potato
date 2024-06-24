import { createStore } from "vuex";
import { authStore } from "./auth.store";
import { layoutStore } from "./layout.store";
import { ResourcesStore } from "@/store/resources.store";

// can add any number of store modules
const store = createStore({
  modules: {
    authStore,
    layoutStore,
    ResourcesStore
  },
});

export default store;