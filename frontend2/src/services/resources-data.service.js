import http from '../http-common';
/*import store from '@/store'*/


class ResourcesService {
  async getResourcesTree() {
   try {
      const response = await http.get(`resources/tree`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
  async getPositions() {
   try {
      const response = await http.get(`resources/positions`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
  async getResourcesData() {
   try {
      const response = await http.get(`resources/data`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}

export default new ResourcesService();
