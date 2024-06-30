<template>
<!--      <v-card
        class="mx-auto rounded-xl hover"
        min-width="200"
        max-width="250"
        hover
      >

        <v-card-title >
          <div class="mt-1 d-flex justify-space-between align-center">
&lt;!&ndash;            <div class=" text-caption text-medium-emphasis ">
                  13-й
                </div>&ndash;&gt;
            <v-chip
              size="x-small"
              color="grey"
              label
              variant="outlined"
            >
              <div class="text-caption text-medium-emphasis  font-weight-light">
                {{ cadetData['position'] }}
              </div>
            </v-chip>
&lt;!&ndash;          <v-badge
                v-if="cadetData['priority']"
                color="grey-darken-1"
                class="align-self-center"
                :content="cadetData['priority']+'-й'"
            />
            <v-chip
              v-else
              size="x-small"
              color="secondary"
              label
              variant="outlined"
            >
              {{cadetData['faculty']}}
            </v-chip>&ndash;&gt;


          </div>
          <v-divider class="mt-2 mb-3"/>
          <div class="d-flex align-center">
            <v-avatar
              class="ma-1 mr-3"
             size="55"
             >
                <v-img
                  alt="doggy"
                  :src="getUserAvatarUrl(cadetData['user']['username']/*['avatar']['url']*/)"
                ></v-img>

            </v-avatar>
            <div class="" :style="{ whiteSpace: 'pre-wrap', textOverflow: 'ellipsis', lineHeight: '1.2em'}">
              <div>{{ cadetData['name'] }}</div>
              <div>{{ cadetData['surname'] }}</div>
            </div>
          </div>
        </v-card-title>

        <v-card-subtitle>
          <router-link v-if="cadetData['username'] !== undefined && cadetData['username']"
            :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '100%'}"
            :to="{ name: 'user', params: { username: cadetData['username'] } }" style="color:#00406b; text-decoration: none">
            {{'@'+cadetData['username']}}
          </router-link>
          <div v-else class="text-h8" :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '100%'}">
            {{"@sobakayasobaka"}}
          </div>
          <div>{{cadetData['group'] + ' ' +  'взвод' + ' | ячейка: ' + cadetData['pm_cell_id']}}</div>
        </v-card-subtitle>
        <v-card-text class="mt-0 pt-2">

        </v-card-text>

        <v-divider class=" mx-4 mt-0 mb-3"/>

      </v-card>-->

      <v-card
        v-if="cadetData"
        class="mx-auto rounded-xl"
        width="250"
        hover
      >
        <v-card-title

        >
          <div class="d-flex align-center justify-space-between " style="min-height: 35px">
            <v-chip
                  class="pl-1 pr-2 mt-1"
                  size="x-small"
                  color="grey"
                  label
                  variant="outlined"
                >
                  <div class="text-caption text-medium-emphasis  font-weight-light">
                      {{(cadetData['position']==='Замком взвода'? '🚨' :
                      (cadetData['position']==='Командир отделения'? '⚡' : '🧃')) + cadetData['position']}}
                  </div>
            </v-chip>
            <v-menu
              v-if="!menuDisabled"
              v-model="menu"
              :close-on-content-click="false"
              location="end"
            >
              <template v-slot:activator="{ props }">
                <v-btn flat icon="mdi-dots-vertical" size="small" class="py-1" v-bind="props"></v-btn>
              </template>

                <v-card
                  class="mx-auto rounded-4"
                  elevation="1"
                  width="145"
                >
                  <v-list
                    density="compact"
                    class="mb-0 pb-1"
                    nav
                  >
                    <v-list-item
                        @click="deleteUser"
                        class=" rounded-4 my-0 py-0"
                        :value="1"

                    >
                      <div class="d-inline-flex text-medium-emphasis">
                        <v-icon color="red" class="mr-3" size="small" :style="{ opacity: 0.7 }">mdi-trash-can</v-icon>
                        <div class="mr-2 text-body-2">Удалить</div>
                      </div>
                    </v-list-item>

                    <v-list-item
                        @click="editUser"
                        :value="2"
                        class=" rounded-4 my-0 py-0"
                    >
                      <div class="d-inline-flex text-medium-emphasis">
                        <v-icon class="mr-3" size="small" :style="{ opacity: 0.7 }">mdi-pencil</v-icon>
                        <div class="mr-2 text-body-2">Изменить</div>
                      </div>
                    </v-list-item>
                  </v-list>

  <!--                <v-list>
                    <v-list-item
                      prepend-avatar="https://cdn.vuetifyjs.com/images/john.jpg"
                      subtitle="Founder of Vuetify"
                      title="John Leider"
                    >
                      <template v-slot:append>
                        <v-btn
                          :class="fav ? 'text-red' : ''"
                          icon="mdi-heart"
                          variant="text"
                          @click="fav = !fav"
                        ></v-btn>
                      </template>
                    </v-list-item>
                  </v-list>

                  <v-divider></v-divider>

                  <v-list>
                    <v-list-item>
                      <v-switch
                        v-model="message"
                        color="purple"
                        label="Enable messages"
                        hide-details
                      ></v-switch>
                    </v-list-item>

                    <v-list-item>
                      <v-switch
                        v-model="hints"
                        color="purple"
                        label="Enable hints"
                        hide-details
                      ></v-switch>
                    </v-list-item>
                  </v-list>

                  <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                      variant="text"
                      @click="menu = false"
                    >
                      Cancel
                    </v-btn>
                    <v-btn
                      color="primary"
                      variant="text"
                      @click="menu = false"
                    >
                      Save
                    </v-btn>
                  </v-card-actions>-->
              </v-card>
            </v-menu>



          </div>
          <v-divider class="my-1 "/>
          <div class="d-flex align-center">
              <v-avatar
            class="ma-1 mr-3"
           size="55"
           >
              <v-img
                alt="doggy"
                :src="getUserAvatarUrl(cadetData['user']['username']/*['avatar']['url']*/)"
              ></v-img>
          </v-avatar>
            <div class="" :style="{ whiteSpace: 'pre-wrap', textOverflow: 'ellipsis', lineHeight: '1.2em'}">
              <div>{{ cadetData['name'] }}</div>
              <div>{{ cadetData['surname'] }}</div>
            </div>
          </div>
        </v-card-title>

        <v-card-subtitle>
          <router-link v-if="cadetData['username'] !== undefined && cadetData['username']"
            :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '100%'}"
            :to="{ name: 'user', params: { username: cadetData['username'] } }" style="color:#00406b; text-decoration: none">
            {{'@'+cadetData['username']}}
          </router-link>
          <div v-else class="text-h8" :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '100%'}">
            {{"@sobakayasobaka"}}
          </div>
<!--          <div>
            {{cadetData['pm_cell_id']+ '-я ячейка' }}
          </div>-->
          <div>{{cadetData['group'] + ' ' +  'взвод' + ' | ячейка: ' + cadetData['pm_cell_id']}}</div>
        </v-card-subtitle>
        <v-card-text class="mt-0 pt-2">
          <div
              :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '75%'}"
          >
            {{ '🎖️ '+ cadetData['rank']+' полиции' }}
          </div>
<!--          <div>{{'🫂 '+ cadetData['group'] +' взвод'}}</div>-->
          <div>{{'⚓ '+ cadetData['course'] +'-й курс'}}</div>
          <div class="mb-2">{{ '👨‍💻 ' + cadetData['faculty'] }}</div>
        </v-card-text>

        <v-divider class=" mx-4 mt-0 mb-3"/>

      </v-card>
      <v-skeleton-loader
        v-else
        type="card, paragraph"
        class="rounded-4"
        width="230"
        :loading="!cadetData"
      />
    </template>

  <script>
  //import editRoleDialog from "@/components/EditRoleDialog";
  import StaticDataService from "@/services/static-data.service";

  export default {
    name: "CadetCard",
    //components:{editRoleDialog}
      props:{
        cadetData:{
          type: Object,
          required: true
        },
        menuDisabled: {
          type: Boolean,
          required: false,
          default: false
        }
      },
      data(){
        return {
          menu: false,
          selected: false
        }
      },
      methods:{
        toggleCard(){
          this.$emit('select', this.cadetData)
          /*if(this.selected === false) this.$emit('select', this.cadetData)
          this.selected = !this.selected*/
        },
        getUserAvatarUrl(username) {
          return StaticDataService.getUserAvatarUrl(username);
        },
      }
  }
  </script>

  <style scoped>
    .selected {
      border: 2px solid #4CAF50;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
    }
    .hover {
      box-shadow: 0px 1px 1px rgba(0, 0, 0, 0.3);
      transition: box-shadow 0.3s ease, transform 0.2s ease;
    }

    .hover:hover {
      box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
      transform: translateY(1px);
    }
  </style>