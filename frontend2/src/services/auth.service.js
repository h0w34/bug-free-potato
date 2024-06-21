import http from '../http-common';
import Fingerprint2 from 'fingerprintjs2';
/*import jwt from 'jsonwebtoken';*/
import store from '@/store'
// the auth header is in http-common.js

class AuthService {
  async getFingerprint() {
    return new Promise((resolve) => {
      Fingerprint2.get(/*{
        excludes: {
          'canvas':true,
          'webgl':true
        },
      }, */function(components) {
        const hashedFingerprint = String(Fingerprint2.x64hash128(JSON.stringify(components), 31));
          resolve(hashedFingerprint);
      });
    });
  }

  async login(login_input, password) {
    try {
      const fingerprint = await this.getFingerprint();
      console.log(fingerprint)
      const response = await http.post(`auth/login`, {
          'login_input': login_input,
          'password': password,
          'fingerprint': fingerprint
      });
      if(response.data.user.access_token){
          /*console.log(response.data.user)
          console.log(JSON.stringify(response.data.user))*/
          localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      /*localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token_jti', response.data.refresh_token_jti);*/
      return response.data.user;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  /*async */logout(){
    localStorage.removeItem('user')
  }

  async signup(username, email, password) {
    try {
      const fingerprint = await this.getFingerprint();
      const response = await http.post(`auth/signup`, {
          'username': username,
          'email': email,
          'password': password,
          'fingerprint': fingerprint,
      });
      const user = response.data.user;
      /*const user = {
        access_token: response.data.access_token,
        refresh_token_jti: response.data.refresh_token_jti,
      };*/
      localStorage.setItem('user', JSON.stringify(user));

      return user/*response*//*.data;*/
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async refreshTokens() {
    try {
      console.log('in auth service refreshTokens')
      const fingerprint = await this.getFingerprint();
      const user = store.state.authStore.user/*JSON.parse(localStorage.getItem('user'));*/
      const response = await http.post(`auth/refresh`, {
          'fingerprint': fingerprint,
          'refresh_token_jti': user.refresh_token_jti
      });

      const newUser = response.data.user
      localStorage.setItem('user', JSON.stringify(newUser));
      return newUser;
      /*const user = {
        access_token: response.data.access_token,
        refresh_token_jti: response.data.refresh_token_jti,
      };*/
      /*localStorage.setItem('user', JSON.stringify(user));

      return user;*/
    } catch (error) {
        console.log('Oh!... FAILED in auth service refreshTokens!')

      console.error(error);
      throw error;
    }
  }

  /*isTokenExpired(token) {
    try {
      const decoded = jwt.decode(token);
      return decoded.exp < Date.now() / 1000;
    } catch (error) {
      console.error(error);
      return true;
    }
  }*/

  async handleResponse(response) {
      return response.text().then(text => {
          const data = text && JSON.parse(text);
          if (!response.ok) {
              if (response.status === 401) {
                  // auto logout if 401 response returned from api
                  this.logout();
                  location.reload(true);
              }

              const error = (data && data.message) || response.statusText;
              return Promise.reject(error);
          }

          return data;
      });
  }
}

export default new AuthService();
