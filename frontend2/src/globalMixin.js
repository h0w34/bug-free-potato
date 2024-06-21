import store from "./store"

export default {
  beforeRouteLeave(to, from, next) {
    console.log('in here@!')
    if (store.state.layoutStore.dutyDialog) {

      // Close the dialog before navigating away
      store.commit('layoutStore/closeDutyDialog');
    }
    next();
  }
}
