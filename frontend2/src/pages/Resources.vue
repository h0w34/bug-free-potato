<template>

    <v-app-bar
        v-if="breadcrumbItems.length!==0"
        class="px-5 d-flex justify-content-center text-center align-center"
        color="white"
        border="1"
        flat
    >
      <v-breadcrumbs
          return-object
          v-if="breadcrumbItems"
          :items="breadcrumbItems"
          class="mb-0 d-flex justify-content-center text-center align-center"
      >
        <template v-slot:item="{ item }">
          <v-breadcrumbs-item
            :to="item.href"
            :disabled="item.disabled"
            @click.prevent="navigateToBreadcrumbItem(item)"
            style="text-decoration: none; color: black;"
          >
            {{ item.title }}
          </v-breadcrumbs-item>
        </template>
        <template v-slot:divider>
          <v-icon icon="mdi-chevron-right"></v-icon>
        </template>
      </v-breadcrumbs>
    </v-app-bar>

    <v-navigation-drawer
        class="p-2 pr-4"
        location="left"
        permanent
        width="315"
      >
        <v-treeview
          class="unselectable custom-treeview pr-3"
          v-if="treeviewItems"
          :items="treeviewItems"
          item-value="title"
          :opened="initiallyOpen"
          @click:open="handleTreeItemClick"
          @click:select="handleTreeItemClick"
        >

          <template v-slot:prepend="{ item }">
            <v-icon v-if="item.kind === 'location'">mdi-map-marker</v-icon>
            <v-icon v-if="item.kind === 'faculty'">mdi-school</v-icon>
            <v-icon v-if="item.kind === 'course'">mdi-book-open-variant</v-icon>
            <v-icon v-if="item.kind === 'group'">mdi-account-group</v-icon>
            <v-icon v-if="item.kind === 'student'">mdi-account</v-icon>
            <v-icon v-if="item.kind === 'university'">mdi-domain</v-icon>

          </template>
        </v-treeview>
      </v-navigation-drawer>

      <div
        class=" justify-content-start m-0 p-3"
      >
        <v-window
          v-model="window"
        >
          <AddCadetDialog/>

          <v-window-item :key="0">
            <v-card>
              <v-card-title>
                <h3>Локации</h3>
              </v-card-title>
              <v-divider class="my-1"/>
              <v-card-text>
                <v-skeleton-loader>
                  <v-row v-if="selectedResource">
                    <v-col
                      v-for="(locationData, i) in selectedResource['locations']"
                      :key="i"
                      md-2
                    >
                      <location-card :data="locationData" @click="handleResourceCardClick"/>
                    </v-col>
                    <v-col
                      cols="6"
                    >
                      <location-card :data="[]"/>
                    </v-col>
                  </v-row>
                </v-skeleton-loader>
              </v-card-text>
            </v-card>
          </v-window-item>

          <v-window-item :key="1">
            <v-card>
              <v-card-title>
                <h3 class="text-light-emphasis">Факультеты на {{selectedResource['name']}}</h3>
              </v-card-title>
              <v-divider class="my-1"/>
              <v-card-text>
                <v-skeleton-loader>
                  <v-row v-if="selectedResource">
                    <v-col
                      v-for="(facultyData, i) in selectedResource['faculties']"
                      :key="i"
                      md-2
                    >
                      <faculty-card :data="facultyData"/>
                    </v-col>
                    <v-col
                      cols="6"
                    >
                      <faculty-card :data="[]"/>
                    </v-col>
                  </v-row>
                </v-skeleton-loader>
              </v-card-text>
            </v-card>
          </v-window-item>


          <v-window-item :key="2">
            <v-card>
              <v-card-title>
                <h3> Курсы на {{selectedResource['name']}}</h3>
              </v-card-title>
              <v-divider class="my-1"/>
              <v-card-text>
                <v-card
                    class="rounded-4 mb-4"
                    style="border: 2px solid #f5f5f5;"
                    v-for="(courseData, i) in selectedResource['courses']"
                    :key="i"
                    flat
                >
                  <v-card-title>
                    <div class="text-h5 font-weight-light">> {{courseData.name}}-й курс</div>
                  </v-card-title>
                  <v-divider class="my-0"/>
                  <v-card-text class="py-3 px-4">
                    <v-row class="d-flex justify-content-start">
                      <v-col
                        v-for="(groupData, i) in courseData['groups']"
                        :key="i"
                        cols="auto"
                      >
                        <group-card :data="groupData"/>
                      </v-col>
                    </v-row>
                  </v-card-text>

                </v-card>
<!--                <v-skeleton-loader>
                  <v-row v-if="selectedResource">
                    <v-col
                      v-for="(courseData, i) in selectedResource['faculties']"
                      :key="i"
                      md-2
                    >
                      <course-card :data="facultyData"/>
                    </v-col>
                    <v-col
                      cols="6"
                    >
                      <faculty-card :data="[]"/>
                    </v-col>
                  </v-row>
                </v-skeleton-loader>-->
              </v-card-text>
            </v-card>
          </v-window-item>

          <v-window-item
              :key="3"
          >
            <v-card fill-space fill-width fill-height height="100%" class="d-flex flex-column m-5" variant="flat">
              <v-card-title>
                Группы!
              </v-card-title>
            </v-card>
          </v-window-item>

          <v-window-item :key="4">
              <DeleteCadetDialog
                  :cadet-data="currentCadetData"
                  @close="localCloseDeleteCadetDialog"
              />
              <v-card>
                <v-card-title class="d-flex align-center justify-space-between">
                  <div class="justify-content-start">
                    <div class="d-flex align-center text-center justify-content-start">
                      <h3>Личный состав {{selectedResource['name']}}-го взвода</h3>
                      <h5 class="ml-2 text-medium-emphasis">({{selectedResource['number_of_cadets']}} курсантов)</h5>
                    </div>
                    <h5 class=" text-medium-emphasis">
                      Направление обучения: {{selectedResource?.['specialization']?.['name'] || 'не указано'}}
                    </h5>
                  </div>
                  <div
                    class="rounded-4 p-2 d-flex justify-content-center text-center align-center gap-3 mr-3"
                    style="border: 2px solid #f5f5f5"
                  >
                      <button
                        class="text-center align-center"
                      >
                        <v-icon size=small class="text-medium-emphasis"
                            @click="editGroupMode=true">
                          mdi-pencil
                        </v-icon>
                        <v-tooltip activator="parent" location="left">
                          Редактировать группу
                        </v-tooltip>
                      </button>
                      <button
                        class="text-center align-center"
                      >
                        <v-icon
                          size=small
                          class="text-medium-emphasis"
                          @click="openAddCadetDialog"
                        >
                          mdi-plus-box-outline
                        </v-icon>
                        <v-tooltip activator="parent" location="bottom">
                          Добавить курсанта
                        </v-tooltip>
                      </button>
                  </div>

                </v-card-title>
                <v-divider class="my-1"/>
                  <v-skeleton-loader class="p-2">
                        <v-row
                            justify="space-evenly"
                            class="m-2 p-4 rounded-4" style="background: rgba(0,0,0,0.02)"
                            v-for="(positionCadets, position_id) in groupGroupedByPositions"
                            :key="position_id"
                        >
                          <v-col
                              cols="auto"
                              v-for="(cadetData, i) in positionCadets['cadets']"
                              :key="i"
                            >
                              <cadet-card :cadetData="cadetData" @openDeleteCadetDialog="localOpenDeleteCadetDialog"/>
                          </v-col>
                        </v-row>
<!--                          <v-row v-if="selectedResource['cadets']" class="m-3 p-4 rounded-4"  style="background: rgba(0,0,0,0.02)">
                            <v-col
                              v-for="(cadetData, i) in selectedResource['cadets']"
                              :key="i"
                              md-2
                            >
                              <cadet-card :cadetData="cadetData" @openDeleteCadetDialog="localOpenDeleteCadetDialog"/>
                            </v-col>
&lt;!&ndash;                            <v-col
                              cols="6"
                            >
                              <faculty-card :data="[]"/>
                            </v-col>&ndash;&gt;
                          </v-row>-->
                  </v-skeleton-loader>

              </v-card>
          </v-window-item>
        </v-window>
      </div>

</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import { useRoute, useRouter } from 'vue-router';

import LocationCard from "@/components/resources/LocationCard";
import FacultyCard from "@/components/resources/FacultyCard";
import GroupCard from "@/components/resources/GroupCard";
import CadetCard from "@/components/cadet/CadetCard";

import AddCadetDialog from "@/components/cadet/AddCadetDialog";
import DeleteCadetDialog from "@/components/cadet/DeleteCadetDialog";

export default {
  name: "ResourcesPage",
  components: {CadetCard, GroupCard, FacultyCard, LocationCard, AddCadetDialog, DeleteCadetDialog},
  setup() {
    const route = useRoute();
    const router = useRouter();

    return {
      route,
      router,
    };
  },

  data: () => ({
    /*addCadetDialog: false,*/
    window: 0,
    initiallyOpen: [],
    opened: [],
    currentCadetData: null,

    }),
  computed: {
    // Implement your logic to determine the active nodes

    ...mapState('ResourcesStore', ['resourcesTree', 'selectedIds', 'selectedResource']),
    ...mapState('layoutStore', ['addCadetDialog']),
    ...mapGetters('ResourcesStore', ['breadcrumbItems', 'treeviewItems']),

    groupGroupedByPositions() {
      if (this.selectedResource?.cadets) {
        return this.selectedResource.cadets.reduce((groups, cadet) => {
          if (!groups[cadet.position.id]) {
            groups[cadet.position.id] = {
              position_id: cadet.position.id,
              cadets: []
            };
          }
          groups[cadet.position.id].cadets.push(cadet);
          return groups;
        }, {});
      } else {
        return [];
      }
    },


    currentTitle(){
      return 1
    }

  },
  //TODO: too long page loading each time it's opened. Do smth with this hook
  async beforeMount() {
    if (!this.resourcesTree) await this.fetchResourcesTree();
    await this.updateSelectedResource();
  },

  /*beforeRouteUpdate(to, from, next) {
    this.updateSelectedResource().then(() => {
      next();
    });
  },*/

  watch: {
    '$route.query': {
      handler: async function() {
        await this.updateSelectedResource();
      },
      deep: true
    }
    /*'$route.query': {
      handler: async function(newQuery, oldQuery) {
        const { locationId, facultyId, courseId, groupId } = newQuery;

        this.setSelectedIds({
          locationId: locationId ? parseInt(locationId) : null,
          facultyId: facultyId ? parseInt(facultyId) : null,
          courseId: courseId ? parseInt(courseId) : null,
          groupId: groupId ? parseInt(groupId) : null,
        });

        await this.setSelectedResourceFromIds();
        await this.setWindowFromSelectedResource();
      },
      immediate: true,
    },*/
  },

methods:{
    ...mapActions('ResourcesStore', ['fetchResourcesTree', /*'fetchResourcesData',*/ 'setSelectedIds', 'setSelectedResource']),
    ...mapActions('layoutStore', ['openAddCadetDialog', 'openDeleteCadetDialog', 'closeDeleteCadetDialog']),


    localOpenDeleteCadetDialog(cadetData){
      if(cadetData) this.currentCadetData = cadetData;
      this.openDeleteCadetDialog()
    },
    localCloseDeleteCadetDialog(){
      this.currentCadetData = null;
      this.closeDeleteCadetDialog();
    },

    navigateToBreadcrumbItem(item) {
      /*alert('the bread clikced item is...' + JSON.stringify(item))*/
      const treeItem = this.findItemByTitle(this.treeviewItems, item.title);
      /*alert(JSON.stringify(treeItem))*/
      this.updateUrl(
        treeItem.locationId,
        treeItem.facultyId,
        treeItem.courseId,
        treeItem.groupId
      );
      this.updateSelectedResource();
    },

    async updateSelectedResource(){
      const { locationId, facultyId, courseId, groupId } = this.$route.query;

      console.log('QUERY IDs: ', locationId, facultyId, courseId, groupId)

      this.setSelectedIds({
        locationId: locationId ? parseInt(locationId) : null,
        facultyId: facultyId ? parseInt(facultyId) : null,
        courseId: courseId ? parseInt(courseId) : null,
        groupId: groupId ? parseInt(groupId) : null,
      });

      console.log('Just set the ids from the query.')

      if(!locationId){
        console.log('whoops! no location id provided! Setting to university...')
        this.setSelectedResource(this.resourcesTree['university'])
      } else {
        console.log('Gotcha! the location id is provided! Setting it to...', this.selectedResource)
        await this.setSelectedResourceFromIds();
      }

      console.log('Setting the windows...')
      await this.setWindowFromSelectedResource();

      console.log('Created the resources Page!')
    },

    async setSelectedResourceFromIds() {
      const { locationId, facultyId, courseId, groupId } = this.selectedIds;

      // Find the corresponding resource based on the selected IDs
      let selectedResource = this.resourcesTree.university;
      if (locationId) {
        const location = this.resourcesTree.university.locations.find((l) => l.id === locationId);
        if (location) {
          selectedResource = location;
          if (facultyId) {
            const faculty = location.faculties.find((f) => f.id === facultyId);
            if (faculty) {
              selectedResource = faculty;
              if (courseId) {
                const course = faculty.courses.find((c) => c.id === courseId);
                if (course) {
                  selectedResource = course;
                  if (groupId) {
                    const group = course.groups.find((g) => g.id === groupId);
                    if (group) {
                      selectedResource = group;
                    } else {
                      this.router.replace({});

                    }
                  }
                  else {
                    //TODO:
                    // this is because we have no separate window for courses and must ignore when one is selected
                    // instead it must roll down to the anchor corresponding to this course at the faculty window
                    selectedResource = faculty;
                  }
                } else {
                                        this.router.replace({});

                }
              }
            } else {
                                    this.router.replace({});

            }
          }
        } else {
                                this.router.replace({});

        }
      }
      // Set the selectedResource in the store
      this.setSelectedResource(selectedResource);
    },

    setWindowFromSelectedResource() {
      if (this.selectedResource['faculties']){
        this.window = 1;
      } else if (this.selectedResource['courses']){
        this.window = 2;
      } else if (this.selectedResource['groups']){
        this.window = 2;
      } else if (this.selectedResource['cadets']){
        this.window = 4;
      } else this.window = 0;
    },

    handleResourceCardClick(cardData){
      console.log(cardData)
    },

    handleTreeItemClick(nodeItem) {
      console.log(nodeItem)
      const treeItem = this.findItemByTitle(this.treeviewItems, nodeItem.id);

      if (treeItem.kind === 'location'){
        this.window = 1;
      }
      else if (treeItem.kind === 'faculty'){
        this.window = 2;
      }
      else if (treeItem.kind === 'course'){
        console.log('nah! no such window for you!')
      }
      else if (treeItem.kind === 'group'){
        this.window = 4;
      }
      else if (treeItem.kind === 'university'){
        this.window = 0;
      }
      else {
        this.window = 0;
      }
      console.log('the tree item i found after clicking the node:', treeItem)
      this.setSelectedIds({
        locationId: treeItem?.locationId ?? null,
        facultyId: treeItem?.facultyId ?? null,
        courseId: treeItem?.courseId ?? null,
        groupId: treeItem?.groupId ?? null
      });
      this.updateUrl(
        treeItem?.locationId ?? null,
        treeItem?.facultyId ?? null,
        treeItem?.courseId ?? null,
        treeItem?.groupId ?? null
      );
      // simply pass the whole selected item, item.raw is a proxy to the original item in resourceList
      if(treeItem.kind !== 'course') this.setSelectedResource(treeItem.raw);
    },

    findItemByTitle(items, title) {
      for (const i of items) {
        if (i.title === title) return i;
        if (i.children) {
          const found = this.findItemByTitle(i.children, title);
          if (found) return found;
        }
      }
      return null;
    },

    updateUrl(locationId, facultyId, courseId, groupId) {
      const query = {};
      if (locationId) query.locationId = locationId;
      if (facultyId) query.facultyId = facultyId;
      if (courseId) query.courseId = courseId;
      if (groupId) query.groupId = groupId;
      this.router.replace({ query });
    },
  }
}
</script>

<style scoped>
  .v-appbar {
    border-width: 1px;
    border-style: solid;
    border-color: #d7d7d7;
  }
  .unselectable {
    -webkit-user-select: none; /* Safari */
    -ms-user-select: none; /* IE 10 and IE 11 */
    user-select: none; /* Standard syntax */
  }

  .v-list-item--active {
    background-color: transparent !important;
    color: inherit !important;
  }


</style>