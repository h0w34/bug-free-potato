/*import router from '@/router'*/
import AuthService from "@/services/auth.service";

const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };

export const authStore = {
  namespaced: true,
  state: initialState,
  // async funcs, used to commit mutations
  actions: {
    login({ commit }, {login_input, password}) {
      return AuthService.login(login_input, password).then(
        // here we get the user object from api response
        // below are two funcs for the fulfilled and rejected cases of the Promise
        user => {
          commit('loginSuccess', user);
          return Promise.resolve(user);
        },
        error => {
          commit('loginFailure');
          return Promise.reject(error);
        }
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    signup({ commit }, username, email, password) {
      return AuthService.signup(username, email, password).then(
        user => {
          commit('registerSuccess');
          return Promise.resolve(user);
        },
        error => {
          commit('registerFailure');
          return Promise.reject(error);
        }
      );
    },
    async refreshTokens({ commit }) {
      try {
        const user = await AuthService.refreshTokens();
        commit("setAccessToken", user.access_token);
        commit("setRefreshTokenJti", user.refresh_token_jti);
        return Promise.resolve(user);
      } catch (error) {
        //warn: bug: fix: todo: pass the error up to the interceptor -- this will logout the user!

        //commit("loginFailure", error);
        return Promise.reject(error);
      }
    },
  },
  // mutations -- sync funcs, the only way to change the state of the store
  mutations: {
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
      console.log('User successfully logged in!')
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    },
    setAccessToken(state, accessToken) {
      state.user.access_token = accessToken;
    },
    setRefreshTokenJti(state, refreshTokenJti) {
      state.user.refresh_token_jti = refreshTokenJti;
    },
  }
};