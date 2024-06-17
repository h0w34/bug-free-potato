import http from '../http-common';

class AuthService {

  async login(login_input, password) {
    try {
      const response = await http.post(`auth/login`, {
          'login_input': login_input,
          'password': password
      });
      response.data
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async signup(username, email, password) {
    try {
      const response = await http.post(`auth/signup`, {
          'username': username,
          'email': email,
          'password': password
      });
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

}

export default new AuthService();
