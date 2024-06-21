import store from './store';

export const beforeLeaveGuard = (to, from, next) => {
  if (store.state.layoutStore.dutyDialog) {
    console.log('in here!');
    // Close the dialog before navigating away
    store.commit('layoutStore/closeDutyDialog');
  }
  next();
};