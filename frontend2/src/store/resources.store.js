/*import store from '@/store/index'*/
import ResourcesService from "@/services/resources-data.service";
/*import resources from "@/pages/Resources";*/


const initialState = {
  resourcesList: null,
  resourcesData: null,
  cachedBreadcrumbItems: null,
  cachedTreeItems: null,
  selectedIds: {
    selectedLocationId: null,
    selectedFacultyId: null,
    selectedCourseId: null,
    selectedGroupId: null
  },
  /*selectedItems: {
    selectedLocation: null,
    selectedFaculty: null,
    selectedCourse: null,
    selectedGroup: null
  },*/
  selectedResource: null
};

export const ResourcesStore = {
  namespaced: true,
  state: initialState,
  getters: {
    breadcrumbItems(state) {
      const items = [];

        if (state.resourcesList) {
          const university = state.resourcesList.university;
          items.push({ title: university.name, disabled: false, href: '#' });

          if (state.selectedIds.selectedLocationId !== null) {
            const location = state.resourcesList.university.locations.find((l) => l.id === state.selectedIds.locationId);
            if (location) {
              items.push({ title: location.name, disabled: false, href: '#' });
              if (state.selectedFacultyId !== null) {
                const faculty = location.faculties.find((f) => f.id === state.selectedIds.facultyId);
                if (faculty) {
                  items.push({ title: faculty.name, disabled: false, href: '#' });
                  if (state.selectedCourseId !== null) {
                    const course = faculty.courses.find((c) => c.id === state.selectedIds.courseId);
                    if (course) {
                      items.push({ title: `${course.id} курс`, disabled: false, href: '#' });
                      if (state.selectedGroupId !== null) {
                        const group = course.groups.find((g) => g.id === state.selectedIds.groupId);
                        if (group) {
                          items.push({ title: `${group.name} взвод`, disabled: false, href: '#' });
                        }
                      }
                    }
                  }
                }
              }
            }
          }
          else {
            items.push({ title: 'локации', disabled: false, href: '#' });
          }
        }
        console.log('the bread i got is: ', items)
        return items;
      },
    treeItems(state) {
      // we save the raw item self additionally with its treeItem
      console.log('in the store tree!')
      if (state.cachedTreeItems) {
        return state.cachedTreeItems;
      }
      const treeItems = [];
      if (state.resourcesList) {
        const university =  {
          raw: state.resourcesList.university,
          title: state.resourcesList.university.name,
          children: [],
          kind: 'university'
        }
        treeItems.push(university)
        state.resourcesList.university.locations.forEach((location) => {
          const locationItem = {
            raw: location,
            title: location.name,
            locationId: location.id,
            children: [],
            kind: 'location'
          };
          location.faculties.forEach((faculty) => {
            const facultyItem = {
              raw: faculty,
              title: faculty.name,
              facultyId: faculty.id,
              children: [],
              locationId: location.id,
              kind: 'faculty'
            };
            faculty.courses.forEach((course) => {
              const courseItem = {
                raw: course,
                title: `${course.id} курс`,
                courseId: course.id,
                children: [],
                locationId: location.id,
                facultyId: faculty.id,
                kind: 'course'
              };
              course.groups.forEach((group) => {
                /*console.log('cadets: ', group.cadets)*/
                const groupItem = {
                  raw: group,
                  title: `${group.name} взвод`,
                  groupId: group.id,
                  locationId: location.id,
                  courseId: course.id,
                  facultyId: faculty.id,
                  kind: 'group'
                };
                courseItem.children.push(groupItem);
              });
              facultyItem.children.push(courseItem);
            });
            locationItem.children.push(facultyItem);
          });
          treeItems[0].children.push(locationItem);
        });
      }
      console.log('here are новиспеченные treeItems: ', treeItems)
      if (treeItems.length !== 0) state.cachedTreeItems = treeItems;
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

    async fetchResourcesData({commit}){
      try {
        const resourcesData = await ResourcesService.getResourcesData();
        commit('setResourcesData', resourcesData);
      } catch (error) {
        return Promise.reject(error);
      }
    },

    setSelectedIds({ commit }, { locationId, facultyId, courseId, groupId }) {
      console.log('changing the selevted ids to:',locationId, facultyId, courseId, groupId )
      commit('setSelectedLocationId', locationId);
      /*commit('setSelectedLocation', locationId)*/
      commit('setSelectedFacultyId', facultyId);
      commit('setSelectedCourseId', courseId);
      commit('setSelectedGroupId', groupId);
    },
    setSelectedResource({ commit }, resource) {
      console.log('setting resource...', resource)
      commit('setSelectedResource', resource)
    },

  },
  mutations: {
    setResourcesList(state, resourcesList) {
      state.resourcesList = resourcesList;
      console.log('Resources list is set.')
    },
    setResourcesData(state, resourcesData) {
      state.resourcesData = resourcesData;
      console.log('Resources data is set.')
    },
    setSelectedResource(state, resource) {
      state.selectedResource = resource;
      console.log('Selected resource is set.')
    },

    setSelectedLocationId(state, locationId) {
      state.selectedIds.locationId = locationId;
      /*state.selectedLocation = state.resourcesList.locations.find((l) => l.id === locationId)*/
    },
    setSelectedFacultyId(state, facultyId) {
      state.selectedIds.facultyId = facultyId;
      /*state.selectedFaculty = state.selectedLocation.faculties.find((f) => f.id === facultyId)*/
    },
    setSelectedCourseId(state, courseId) {
      state.selectedIds.courseId = courseId;
      /*state.selectedFaculty = state.selectedFaculty.courses.find((c) => c.id === courseId)*/
    },
    setSelectedGroupId(state, groupId) {
      state.selectedIds.groupId = groupId;
/*
      state.selectedFaculty = state.selectedGroup.groups.find((g) => g.id === groupId)
*/
    },
  }
};