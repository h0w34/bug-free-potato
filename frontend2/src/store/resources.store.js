/*import store from '@/store/index'*/
import ResourcesService from "@/services/resources-data.service";
/*import resources from "@/pages/Resources";*/


const initialState = {
  resourcesTree: null,
/*  resourcesData: null,*/
/*  cachedBreadcrumbItems: null,*/
  cachedTreeItems: null,
  selectedIds: {
    locationId: null,
    facultyId: null,
    courseId: null,
    groupId: null
  },
  selectedResource: null,
};

export const ResourcesStore = {
  namespaced: true,
  state: initialState,
  getters: {
    breadcrumbItems(state) {
      console.log('!Here we updating our breadcrumbs!')
      if (!state.resourcesTree) {
        console.log('the resourceList is empty! returning []')
        return [];
      }
      const items = [];

        if (state.resourcesTree) {
          const university = state.resourcesTree.university;
          items.push({ title: university.name, disabled: false, href: '#' });
          console.log('For now selectedIds are... ', JSON.stringify(state.selectedIds))
          if (state.selectedIds.locationId !== null) {
            console.log('One down...')
            console.log('university is... ', university)
            console.log('selectedIds are...', state.selectedIds)
            const location = university.locations.find((l) => l.id === state.selectedIds.locationId);
            if (location) {
              console.log('Two down...')
              items.push({ title: location.name, disabled: false, href: '#' });
              if (state.selectedIds.facultyId !== null) {
                const faculty = location.faculties.find((f) => f.id === state.selectedIds.facultyId);
                if (faculty) {
                  console.log('Three down...')
                  items.push({ title: faculty.name, disabled: false, href: '#' });
                  if (state.selectedIds.courseId !== null) {
                    const course = faculty.courses.find((c) => c.id === state.selectedIds.courseId);
                    if (course) {
                      items.push({ title: `${course.name} курс`, disabled: false, href: '#' });
                      if (state.selectedIds.groupId !== null) {
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
            items.push({ title: 'Локации', disabled: false, href: '#' });
          }
        }
        console.log('the bread i got is: ', items)
        return items;
      },
    treeviewItems(state) {
      // we save the raw item self additionally with its treeItem
      console.log('in the store tree!')
      if (state.cachedTreeItems) {
        return state.cachedTreeItems;
      }
      const treeviewItems = [];
      if (state.resourcesTree) {
        const university =  {
          raw: state.resourcesTree.university,
          title: state.resourcesTree.university.name,
          children: [],
          kind: 'university'
        }
        treeviewItems.push(university)
        state.resourcesTree.university.locations.forEach((location) => {
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
                title: `${course.name} курс`,
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
          treeviewItems[0].children.push(locationItem);
        });
      }
      console.log('here are новоиспеченные treeviewItems: ', treeviewItems)
      if (treeviewItems.length !== 0) state.cachedTreeItems = treeviewItems;
      return treeviewItems;
    },
  },

  actions: {
    async fetchResourcesTree({commit}) {
      try {
        const resourcesList = await ResourcesService.getResourcesTree();
        commit('setResourcesTree', resourcesList);
        console.log(resourcesList)
      } catch (error) {
        return Promise.reject(error);
      }
    },

    /*async fetchLocations({commit}) {
      try {
        const locations = await ResourcesService.getLocations();
        commit('setResourcesTree', resourcesList);
        console.log(resourcesList)
      } catch (error) {
        return Promise.reject(error);
      }
    },
    async fetchFaculties({commit}) {
      try {
        const faculties = await ResourcesService.getFaculties();
        commit('setResourcesTree', resourcesList);
        console.log(resourcesList)
      } catch (error) {
        return Promise.reject(error);
      }
    },
    async fetchCourses({commit}) {
      try {
        const courses = await ResourcesService.getCourses();
        commit('setResourcesTree', resourcesList);
        console.log(resourcesList)
      } catch (error) {
        return Promise.reject(error);
      }
    },
    async fetchGroups({commit}) {
      try {
        const groups = await ResourcesService.getGroups();
        commit('setResourcesTree', resourcesList);
        console.log(resourcesList)
      } catch (error) {
        return Promise.reject(error);
      }
    },*/

/*    async fetchResourcesData({commit}){
      try {
        const resourcesData = await ResourcesService.getResourcesData();
        commit('setResourcesData', resourcesData);
      } catch (error) {
        return Promise.reject(error);
      }
    },*/

    setSelectedIds({ commit }, { locationId, facultyId, courseId, groupId }) {
      console.log('changing the selevted ids to:', locationId, facultyId, courseId, groupId )
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
    setResourcesTree(state, resourcesList) {
      state.resourcesTree = resourcesList;
      console.log('Resources list is set.')
    },
    /*setResourcesData(state, resourcesData) {
      state.resourcesData = resourcesData;
      console.log('Resources data is set.')
    },*/
    setSelectedResource(state, resource) {
      state.selectedResource = resource;
      console.log('Selected resource is set.')
    },
    setSelectedLocationId(state, locationId) {
      state.selectedIds.locationId = locationId;
      /*state.selectedIds.locationId = {
        ...state.selectedIds.locationId,
        [locationId]: locationId
      }*/
/*      console.log('the resource tree in FIRST mutation is... ', JSON.stringify(state.resourcesTree.university.locations))
      console.log('and the locationId is...', locationId)
      state.selectedLocation = state.resourcesTree.university.locations.find((l) => l.id === locationId)*/

    },
    setSelectedFacultyId(state, facultyId) {
      state.selectedIds.facultyId = facultyId;
/*      state.selectedIds.facultyId = {
        ...state.selectedIds.facultyId,
        [facultyId]: facultyId
      }*/
/*
      state.selectedFaculty = state.selectedLocation.faculties.find((f) => f.id === facultyId)
*/
    },
    setSelectedCourseId(state, courseId) {
      state.selectedIds.courseId = courseId;
/*      state.selectedIds.courseId = {
        ...state.selectedIds.courseId,
        [courseId]: courseId
      };*/
/*
      state.selectedFaculty = state.selectedFaculty.courses.find((c) => c.id === courseId)
*/
    },
    setSelectedGroupId(state, groupId) {
      console.log('just before...', JSON.stringify(state.selectedIds))
      state.selectedIds.groupId = groupId;
/*      state.selectedIds.groupId = {
        ...state.selectedIds.groupId,
        [groupId]: groupId
      };*/
      /*state.selectedGroup = state.selectedCourse.groups.find((g) => g.id === groupId)*/
    }
  }
};