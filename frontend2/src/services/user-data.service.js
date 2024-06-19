import http from '../http-common';

class UserDataService {
  async getUserByUsername(username) {
    try {
      const response = await http.get(`users/${username}`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async getUserStatistics(username) {
    try {
      const response = await http.get(`users/${username}/statistics`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async deleteUser(username) {
    try {
      const response = await http.get(`users/${username}/statistics`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async createUser(username) {
    try {
      const response = await http.get(`users/${username}/statistics`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}

export default new UserDataService();
