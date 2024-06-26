import http from '../http-common';
/*import store from '@/store'*/


class ResourcesService {
  async getResourcesList() {
   try {
      const response = await http.get(`resources/list`);
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
