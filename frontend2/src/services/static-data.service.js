/*import http from '../http-common';*/
import { API_URL } from '@/config';

  class StaticDataService {
    /*STATIC_FOLDER_URL = API_URL+'/static'*/

    getUserAvatarUrl(username/*filename*/) {
      return API_URL + `/users/${username}/avatar`
      /*return this.STATIC_FOLDER_URL + '/img/avatars/' + filename*/
    }
      /*try {
        const response = await http.get(`static/img/avatars/${avatar_filename}`);
        return response.data;
      } catch (error) {
        console.error(error);
        throw error;
      }
    }*/
  }

  export default new StaticDataService();
