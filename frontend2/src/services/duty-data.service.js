// src/services/duty.service.js
import http from '../http-common';

class DutyDataService {

  async actionOnDutyById(dutyId, action) {
    try {
      const response = await http.patch(`duties/${dutyId}`, {'action': action});
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  // Get duties for a specified location
  async getDutiesByLocations(locationIds) {
    try {
      const params = new URLSearchParams();
      locationIds.forEach(id => params.append('location_ids', id.toString()));
      const response = await http.get(`duties?${params}`);
      return response.data;

    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  // Create a duty
  async createDuty(dutyDate, dutyTypeId, cadetRolesIds) {
    try {
      const response = await http.post('duties', {
        date: dutyDate,
        duty_type_id: dutyTypeId,
        cadet_roles_ids: cadetRolesIds,
      });
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  // Get a single duty
  async   getDutyById(dutyId) {
    try {
      const response = await http.get(`duties/${dutyId}`);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  // Update a duty
  async updateDuty(dutyId, replacedId, replacingId, commentary=null, replacement_doc=null) {
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
  }


}

export default new DutyDataService();
