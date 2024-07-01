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

  async createCadet({name, surname, patronymic, sex, rank_id, position_id, group_id, pm_cell_id, ak_cell_id}){
      console.log('Before the TRY!!!!!!!!1')
   try {
       console.log('in the create cadet resource!!!!!Ё')
      const response = await http.post(`resources/cadets`, {
        name: name,
        surname: surname,
        patronymic: patronymic,
        sex: sex,
        rank_id: rank_id,
        position_id: position_id,
        group_id: group_id,
        pm_cell_id: pm_cell_id,
        ak_cell_id: ak_cell_id
      });
      return response.data;
    } catch (error) {
      alert(error.message)
      alert(error.data)
      console.error(error);
      throw error;
    }
  }

  async deleteCadet(cadetId){
    try {
      const response = await http.delete(`resources/cadets/${cadetId}`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async getCadetStatistics(cadetId, params = {}) {
    try {
      const response = await http.get(`resources/cadets/${cadetId}/statistics`, {params: params});
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  // No need for now as positions are send with the resources tree
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
