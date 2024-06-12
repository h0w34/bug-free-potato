// src/services/http-common.js
import axios from 'axios';

const API_URL = 'http://localhost:8080/api';

const http = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-type': 'application/json'
  }
});

export default http;
