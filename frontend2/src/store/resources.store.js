/*import store from '@/store/index'*/
import ResourcesService from "@/services/resources-data.service";

const initialState = {
    resourcesList: null,
    resourcesData: null
}

export const ResourcesStore = {
  namespaced: true,
  state: initialState,
  getters: {
    breadcrumbItems: (state) => (locationId, facultyId, courseId, groupId) => {
      if (!state.resourcesList) {
        console.log('the resourceList is empty! returning []')
        return [];
      }

      const breadcrumbItems = [];
      let currentLocation = null;
      let currentFaculty = null;
      let currentCourse = null;
      let currentGroup = null;

      for (const location of state.resourcesList.locations) {
        if (location.id === locationId) {
          currentLocation = location;
          for (const faculty of location.faculties) {
            if (faculty.id === facultyId) {
              currentFaculty = faculty;
              for (const course of faculty.courses) {
                if (course.id === courseId) {
                  currentCourse = course;
                  for (const group of course.groups) {
                    if (group.id === groupId) {
                      currentGroup = group;
                      break;
                    }
                  }
                  if (currentGroup) break;
                }
              }
              if (currentGroup) break;
            }
          }
          if (currentGroup) break;
        }
      }

      if (currentLocation) {
        breadcrumbItems.push({
          title: currentLocation.name,
          disabled: false,
          href: '#',
          locationId: currentLocation.id,
        });
      }
      if (currentFaculty) {
        breadcrumbItems.push({
          title: currentFaculty.name,
          disabled: false,
          href: '#',
          facultyId: currentFaculty.id,
        });
      }
      if (currentCourse) {
        breadcrumbItems.push({
          title: `${currentCourse.id} Курс`,
          disabled: false,
          href: '#',
          courseId: currentCourse.id,
        });
      }
      if (currentGroup) {
        breadcrumbItems.push({
          title: `${currentGroup.name} взвод`,
          disabled: false,
          href: '#',
          groupId: currentGroup.id,
        });
      }
      return breadcrumbItems;
    },
    treeItems: (state) => (locationId) => {
      console.log('PASSED LOCATION ID: ', locationId)
      if (!state.resourcesList) {
        console.log('the resourceList is empty! returning []')
        return [];
      }
      console.log('resource list in vue treeItems action:', state.resourcesList)
      const treeItems = [];
      for (const location of state.resourcesList.locations) {
        console.log('LOCATIONS: ',location)

        if (location.id === locationId) {
          const locationItem = {
            title: location.name,
            locationId: location.id,
            children: [],
          };

          for (const faculty of location.faculties) {
            console.log('Faculties: ', faculty)
            const facultyItem = {
              title: faculty.name,
              facultyId: faculty.id,
              children: [],
            };

            for (const course of faculty.courses) {
              console.log('COURSES: ', course)
              const courseItem = {
                title: `${course.id} Курс`,
                courseId: course.id,
                children: [],
              };

              for (const group of course.groups) {
                console.log('GROUPS: ', group)
                const groupItem = {
                  title: group.name,
                  id: group.id,
                  children: group.cadets.map((cadet) => ({
                    title: `${cadet.name} ${cadet.surname}`,
                  })),
                };
                courseItem.children.push(groupItem);
              }
              facultyItem.children.push(courseItem);
            }
            locationItem.children.push(facultyItem);
          }
          treeItems.push(locationItem);
          break;
        }
      }
      console.log('the tree items before sending the back: ', JSON.stringify(treeItems))
      return treeItems;
    },

  },

  actions: {
    async fetchResourcesList({commit}) {
      try {
        const resourcesList = await ResourcesService.getResourcesList();
        commit('setResourcesList', resourcesList);
        console.log(resourcesList)
      } catch (error) {
        return Promise.reject(error);
      }
    },
  },
  mutations: {
    setResourcesList(state, resourcesList) {
      state.resourcesList = resourcesList;
      console.log('Resources list set on.')
    },
  }
};