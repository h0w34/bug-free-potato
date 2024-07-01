  import store from "../store"
  /*import { mapState } from 'vuex';*/

  export default function authHeader() {
    const user = store.state.authStore.user;
    //let user = JSON.parse(localStorage.getItem('user'));

    if (user && user.access_token) {
      console.log('From header: appending the token:', user.token)
      return { Authorization: 'Bearer ' + user.access_token };
    } else {
      console.log('From header: not found user entry in the storage!')
      return {};
    }
  }