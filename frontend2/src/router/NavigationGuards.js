import store from '../store';

export default {
  beforeLeaveGuard: (to, from, next) => {
    if (store.state.layoutStore.dutyDialog) {
      store.dispatch('layoutStore/closeDutyDialog');
    }
    if (store.state.layoutStore.sidebar) {
      store.dispatch('layoutStore/closeSidebar');
    }
    next();
  },
  authGuard: (to, from, next) => {
    console.log('In auth guard!')
    if (to.meta.requiresAuth) {
      if (store.state.authStore.status.loggedIn) {
        next();
      } else {
        next('/login');
      }
    } else {
      next();
    }
  },
  /*guestGuard: (to, from, next) => {
    if (!to.meta.requiresAuth) {
      next();
    } else {
      next('/login');
    }
  },
  adminGuard: (to, from, next) => {
    if (to.meta.requiresAdmin) {
      if (isAuthenticated() && isUserAdmin()) {
        next();
      } else {
        next('/login');
      }
    } else {
      next();
    }
  },*/

};
