// src/services/http-common.js - an axios interceptor

import axios from 'axios';
import authHeader from "@/helpers/auth-header";
//import store from "./store"
//import jwt from 'jsonwebtoken';

//const API_URL = 'http://192.168.43.119:8080/api';
const API_URL = 'http://localhost:8080/api';

const http = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-type': 'application/json',
    ...authHeader()
  }
});
/*

// Request interceptor to check and refresh tokens
http.interceptors.request.use(
  async (config) => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.access_token) {
      const decodedToken = jwt.decode(user.access_token, {
        algorithms: ["HS256"],
        complete: true
      });
      console.log('Heres our token!', decodedToken)
      const currentTime = new Date().getTime() / 1000;
      const expirationTime = decodedToken.exp;

      // Check if the access token is about to expire (e.g., within the next 60 seconds)
      if (expirationTime - currentTime < 60) {
        try {
          // Refresh the tokens
          await store.dispatch('authStore/refreshTokens');
          //config.headers.Authorization = `Bearer ${JSON.parse(localStorage.getItem('user')).access_token}`;
        } catch (error) {
          // If token refresh fails, log the user out
          await store.dispatch('authStore/logout');
          window.location.reload();
        }
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
*/

export default http;
