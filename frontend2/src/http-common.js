// src/services/http-common.js - an axios interceptor

import axios from 'axios';
import authHeader from "@/helpers/auth-header";
import store from "@/store";
import { API_URL } from '@/config';
//import store from "./store"
/*
import jwt from 'jsonwebtoken';
*/
import * as jose from 'jose'
import {router} from "@/router";

//const API_URL = 'http://192.168.43.119:8080/api';

const http = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-type': 'application/json',
    /*...authHeader()*/
  }
});
/*
http.interceptors.request.use(config => {
  const headers = authHeader();
    if (headers.Authorization) {
      config.headers.Authorization = headers.Authorization;
    }
      return config;
    }, error => {
  return Promise.reject(error);
});*/

http.interceptors.request.use(
  async (config) => {
    const user = store.state.authStore.user;
    if (user && user.access_token) {
      const claims = jose.decodeJwt(user.access_token)
      /*const decodedToken = jwt.decode(user.access_token, {
        complete: true
      });*/
      /*const decodedToken = jwt.decode(user.access_token/!*, {
        algorithms: ["HS256"],
        complete: true
      }*!/);*/
      console.log('Heres our token!', claims)
      const currentTime = new Date().getTime() / 1000;
      const expirationTime = claims.exp;

      console.log('expirationTime diff is: ', expirationTime - currentTime)
      // Check if the access token is about to expire (e.g., within the next 60 seconds)
      if (expirationTime - currentTime < 60) {
        try {
          // Refresh the tokens
          console.log('Oh! the token has expired! Refreshing it...')
          if (!store.state.authStore.refreshing) {
            await store.dispatch('authStore/refreshTokens');
            console.log('Refreshed tokens successfully')
          }
          //config.headers.Authorization = `Bearer ${JSON.parse(localStorage.getItem('user')).access_token}`;
        } catch (error) {
          console.log('Failed to refresh tokens! Logging out...')
          // If token refresh fails, log the user out
          await store.dispatch('authStore/logout');
          await router.push('/login')
          //window.location.reload();
        }
      }
    }
    const headers = authHeader();
    console.log('sending a jwt request...')
    if (headers.Authorization) {
      config.headers.Authorization = headers.Authorization;
    }
      return config;
    }, error => {
    return Promise.reject(error);
    //return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
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
