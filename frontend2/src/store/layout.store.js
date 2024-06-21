const initialState = {
  sidebar: false,
  dutyDialog: false
}

export const layoutStore = {
  namespaced: true,
  state: initialState,
  // async funcs, used to commit mutations
  actions: {
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
    }
  },

  mutations: {
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
    }
  }
};