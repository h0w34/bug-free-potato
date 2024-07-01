<template>
      <!--v-card
        class="mx-auto rounded-xl"
        max-width="344"
        :hover="!selected"
        :elevation="selected ? 5 : false"
      -->
      <v-card
        class="mx-auto rounded-xl"
        max-width="344"
        hover
      >

        <v-card-title class="d-flex justify-content-between">
            <!--div class="mr-1 mt-1" :style="{ whiteSpace: 'pre-wrap', textOverflow: 'ellipsis', lineHeight: '1.2em'}">
              {{cadetData['name'] + ' ' + cadetData['surname']}}
            </div-->
            <div class="mr-1 mt-1" :style="{ whiteSpace: 'pre-wrap', textOverflow: 'ellipsis', lineHeight: '1.2em'}">
              <div>{{ cadetData['name'] }}</div>
              <div>{{ cadetData['surname'] }}</div>
            </div>

            <div v-if="cadetData['priority']">
            <v-badge color="grey-darken-1" inline :content="cadetData['priority']+'-й'"></v-badge>
            </div>
            <div v-else>
              <v-chip
                size="x-small"
                color="secondary"
                label
                variant="outlined"
              >
                {{cadetData['faculty']['name']}}
              </v-chip>
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

          <div>{{cadetData['group']['name'] + ' ' +  'взвод' + ' | ячейка: ' + cadetData['pm_cell_id']}}</div>
          <v-avatar
            class="ma-3"
           size="55"
           >
            <!--v-img
              alt="doggy"
              :src="`https://thispersondoesnotexist.com/?${Date.now() + Math.random()}`"
            ></v-img-->

              <v-img
                alt="doggy"
                :src="getUserAvatarUrl(cadetData['user']['username']/*['avatar']['url']*/)"
              ></v-img>

          </v-avatar>
        </v-card-subtitle>

        <v-divider class="mx-2 mb-2"/>
          <template v-slot:actions>
           <v-spacer />
            <!--v-btn selected-class="bg-primary"
                @click="toggleCard"
                class="text-none"
                color="medium-emphasis"
                min-width="92"
                variant="outlined"
                rounded
             -->
            <v-btn
                @click="toggleCard"
                class="text-none mb-1"
                color="medium-emphasis"
                min-width="92"
                variant="outlined"
                rounded
             >
               Выбрать
             </v-btn>
           <v-spacer />
          </template>
      </v-card>
    </template>

  <script>
  //import editRoleDialog from "@/components/EditRoleDialog";
  import StaticDataService from "@/services/static-data.service";

  export default {
    name: "ButtonCadetCard",
    //components:{editRoleDialog}
      props:{
        cadetData:{
          type: Object,
          required: true
        }
      },
      data(){
        return {
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
  </style>