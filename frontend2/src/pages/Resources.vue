<template>

    <v-app-bar
        v-if="breadcrumbItems.length!==0"
        class="px-5 d-flex justify-content-center text-center align-center"
        color="white"
        border="1"
        flat
    >
      <v-breadcrumbs
          v-if="breadcrumbItems"
          :items="breadcrumbItems"
          class="mb-0 d-flex justify-content-center text-center align-center" >
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
          v-if="treeItems"
          :items="treeItems"
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
                      <location-card :data="locationData"/>
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
                <h3>Факультеты на {{selectedResource['name']}}</h3>
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
                    <div class="text-h5 font-weight-light">> {{courseData.id}}-й курс</div>
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
            <v-card fill-space fill-width fill-height height="100%" class="d-flex flex-column m-5"
             variant="flat"
            >
              <v-card-title>
                Группы!
              </v-card-title>
              {{selectedResource}}
            </v-card>
          </v-window-item>

          <v-window-item :key="4">
              <v-card>
                <v-card-title class="d-flex text-center align-center justify-space-between">
                  <div class="justify-content-start">
                    <h3>Личный состав {{selectedResource['name']}}-го взвода</h3>
                    <h5 class=" text-medium-emphasis">Всего {{selectedResource['number_of_cadets']}} курсантов}}</h5>
                  </div>
                  <div
                      class="rounded-4 p-2 d-flex justify-content-center text-center align-center gap-3 mr-3"
                      style="border: 2px solid #f5f5f5"
                  >
                      <button class="text-center align-center">
                        <v-icon size=small class="text-medium-emphasis">
                          mdi-pencil
                        </v-icon>
                      </button>
                      <button class=" text-center align-center">
                        <v-icon size=small class="text-medium-emphasis">
                          mdi-plus-box-outline
                        </v-icon>
                      </button>
                  </div>

                </v-card-title>
                <v-divider class="my-1"/>
                  <v-skeleton-loader>
                          <v-row v-if="selectedResource['cadets']" class="m-3 p-4 rounded-4"  style="background: rgba(0,0,0,0.02)">
                            <v-col
                              v-for="(cadetData, i) in selectedResource['cadets']"
                              :key="i"
                              md-2
                            >
                              <cadet-card :cadetData="cadetData"/>
                            </v-col>
<!--                            <v-col
                              cols="6"
                            >
                              <faculty-card :data="[]"/>
                            </v-col>-->
                          </v-row>
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

export default {
  name: "ResourcesPage",
  components: {CadetCard, GroupCard, FacultyCard, LocationCard},
  setup() {
    const route = useRoute();
    const router = useRouter();

    return {
      route,
      router,
    };
  },

  data: () => ({
    window: 0,
      items: [
        {
          title: 'Коптевская ул. 63',
          disabled: false,
          href: '#',
        },
        {
          title: 'ФПСОИБ',
          disabled: false,
          href: '#',
        },
        {
          title: '3 Курс',
          disabled: false,
          href: '#',
        },
        {
          title: '913 взвод',
          disabled: false,
          href: '#',
        }
      ],
      initiallyOpen: [],
      files: {
        html: 'mdi-language-html5',
        js: 'mdi-nodejs',
        json: 'mdi-code-json',
        md: 'mdi-language-markdown',
        pdf: 'mdi-file-pdf-box',
        png: 'mdi-file-image',
        txt: 'mdi-file-document-outline',
        xls: 'mdi-file-excel',
      },
      tree: [],
      /*breadcrumbItems: [],
      treeItems: [],*/
      items2: [
        {
          title: '.git',
        },
        {
          title: 'node_modules',
        },
        {
          title: 'public',
          children: [
            {
              title: 'static',
              children: [{
                title: 'logo.png',
                file: 'png',
              }],
            },
            {
              title: 'favicon.ico',
              file: 'png',
            },
            {
              title: 'index.html',
              file: 'html',
            },
          ],
        },
        {
          title: '.gitignore',
          file: 'txt',
        },
        {
          title: 'babel.config.js',
          file: 'js',
        },
        {
          title: 'package.json',
          file: 'json',
        },
        {
          title: 'README.md',
          file: 'md',
        },
        {
          title: 'vue.config.js',
          file: 'js',
        },
        {
          title: 'yarn.lock',
          file: 'txt',
        },
      ],
    opened: []
    }),
  computed: {
    // Implement your logic to determine the active nodes

    ...mapState('ResourcesStore', ['resourcesList', 'selectedIds', "selectedResource"]),
    ...mapGetters('ResourcesStore', ['breadcrumbItems', 'treeItems']),

    currentTitle(){
      return 1
    }

    /*breadcrumbItems() {
      return this.$store.getters['ResourcesStore/breadcrumbItems'](
        this.selectedLocationId,
        this.selectedFacultyId,
        this.selectedCourseId,
        this.selectedGroupId
      );
    },
    treeItems() {
      return this.$store.getters['ResourcesStore/treeItems'](this.selectedLocationId);
    },*/

  },
  //TODO: too long page loading each time it's opened. Do smth with this hook
  async created() {
    console.log('Created the resources Page!')
    if (!this.resourcesList) await this.fetchResourcesList();
    this.setSelectedResource(this.resourcesList['university'])
/*
    await this.fetchResourcesData();
*/
  },

  watch: {
    /*resourcesList() {
      this.updateBreadcrumbItems();
      this.updateTreeItems();
    },*/
  },

methods:{
    ...mapActions('ResourcesStore', ['fetchResourcesList', /*'fetchResourcesData',*/ 'setSelectedIds', 'setSelectedResource']),

    handleTreeItemClick(nodeItem) {
      console.log(nodeItem)
      const treeItem = this.findItemByTitle(this.treeItems, nodeItem.id);

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
        locationId: treeItem?.locationId,
        facultyId: treeItem?.facultyId,
        courseId: treeItem?.courseId,
        groupId: treeItem?.groupId
      });
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
      this.router.replace({
        query: {
          locationId,
          facultyId,
          courseId,
          groupId,
        },
      });
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