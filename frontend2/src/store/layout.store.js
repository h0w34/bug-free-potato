  const initialState = {
    sidebar: false,
    dutyDialog: false,
    addCadetDialog: true,
  }

  export const layoutStore = {
    namespaced: true,
    state: { ...initialState },
    // async funcs, used to commit mutations
    actions: {
      resetLayout({ commit }){
        console.log('resettting the layput!')
        commit('resetLayout');
      },
      openDutyDialog({ commit }){
        commit('openDutyDialog');
      },
      closeDutyDialog({ commit }){
        commit('closeDutyDialog');
      },
      /*  Sidebar  */
      closeSidebar({ commit }) {
        commit('closeSidebar');
      },
      openSidebar({ commit }) {
        console.log('in openSIdebar action...')
        commit('openSidebar');
      },
      openAddCadetDialog({ commit }){
        commit('openAddCadetDialog')
      },
      closeAddCadetDialog({ commit }){
        commit('closeAddCadetDialog')
      }
    },

  mutations: {
    resetLayout(state) {
      state.dutyDialog = false;
      state.sidebar = false;
    },
    openDutyDialog(state) {
      state.dutyDialog = true;
    },
    closeDutyDialog(state) {
      state.dutyDialog = false;
    },
    openSidebar(state) {
      console.log('in openSIdebar mutation...')
      state.sidebar = true;
    },
    closeSidebar(state) {
      state.sidebar = false;
    },
    openAddCadetDialog(state) {
      state.addCadetDialog = true;
    },
    closeAddCadetDialog(state) {
      state.addCadetDialog = false;
    }
  }
};