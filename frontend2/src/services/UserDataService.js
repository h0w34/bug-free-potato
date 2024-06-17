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
  // Update a duty
  /*async updateDuty(dutyId, replacedId, replacingId, commentary=null, replacement_doc=null) {
    try {
      const data = {
        replaced_id: replacedId,
        replacing_id: replacingId,
      }
      if (commentary){
        data['commentary'] = commentary
      }
      else if (replacement_doc){
        data['replacement_doc'] = replacement_doc
      }
      const response = await http.put(`duties/${dutyId}`, data);

      return response.data;
    } catch (error) {
      console.error('Error updating duty!', error);
      throw error;
    }
  }

  // Delete a duty
  async deleteDuty(dutyId) {
    try {
      const response = await http.delete(`duties/${dutyId}`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  // Get suitable reserves for a duty
  async getSuitableReserves(dutyId, roleId) {  //TODO: fetch reserves along with suitable ones
    try {
      const response = await http.get(`duties/${dutyId}/reserves?role_id=${roleId}`);
      return response.data;

    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async getReplacements(dutyId){
    try {
      const response = await http.get(`duties/${dutyId}/replacements`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }*/


}

export default new UserDataService();
