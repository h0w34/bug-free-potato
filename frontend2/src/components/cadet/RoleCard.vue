<template>
  <v-card
    class="mx-auto rounded-xl pb-3"
    max-width="240"
    variant="elevated"
    hover
  >
    <v-card-title class="pb-1">
      <!--v-chip
          color="secondary"
          variant="tonal"
          density="comfortable"
          label
          class="my-0"
        >
          <div class="my-0">{{cadetData['role']['name']}}</div>
        </v-chip-->
      <div class="my-0">{{cadetData['role']['name']}}</div>
    </v-card-title>
    <v-divider class="my-0 mx-2"/>


<!--    <v-card-subtitle class="my-2 mb-0">
        <div>{{cadetData['cadet']['group'] + ' ' +  'взвод' + ' | ячейка: ' + cadetData['cadet']['pm_cell_id']}}</div>
    </v-card-subtitle>

    <v-card-text class="pt-0 pb-0">
      &lt;!&ndash;h6 class="ma-0">{{cadetData['cadet']['name'] + ' ' + cadetData['cadet']['surname']}}</h6>
      <div class="text-medium-emphasis">
            {{"@obormotik"}}
      </div&ndash;&gt;
      <div class="d-flex align-center justify-content-start py-0">
        <v-avatar
          class="ml-1 my-3 mr-4"
          size="55"
        >
          &lt;!&ndash;v-img
            alt="doggy"
            :src="`https://thispersondoesnotexist.com/?${Date.now() + Math.random()}`"
          ></v-img&ndash;&gt;

            <v-img
              style="opacity: 0.85"
              alt="doggy"
              :src="getUserAvatarUrl(cadetData['cadet']['user']['username']/*['avatar']['url']*/)"
            ></v-img>

        </v-avatar>
        <div>
          <h5 class="ma-0">
            <div class="" :style="{ whiteSpace: 'pre-wrap', textOverflow: 'ellipsis', lineHeight: '1.2em'}">
              <div>{{ cadetData['cadet']['name'] }}</div>
              <div>{{ cadetData['cadet']['surname'] }}</div>
            </div>
          </h5>
        </div>
      </div>
    </v-card-text>
    <v-card-subtitle class="mb-1">
      <router-link :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '100%'}"
            :to="{ name: 'user', params: { username: cadetData['cadet']['username'] } }" style="color:#00406b; text-decoration: none"
            @click="navigateToUserPage"
      >
        <div v-if="cadetData['cadet']['user']['username']">
          {{'@'+ cadetData['cadet']['user']['username']}}
        </div>
        <div v-else>
          @yasobakayasobaka
        </div>
      </router-link>
      <div class="d-flex justify-content-start">
        <div>{{ cadetData['cadet']['course'] + '-й курс ' + cadetData['cadet']['faculty']}}</div>

      </div>

    </v-card-subtitle>-->

    <v-card-subtitle class="my-2 mb-1">
<!--      <div>{{cadetData['cadet']['group']['name'] + ' взвод' + ' | ' +  cadetData['cadet']['course']['name'] + '-й курс'}}</div>
      <div>{{ 'Ячейка: ' + cadetData['cadet']['pm_cell_id'] }}</div>-->
      <div>{{cadetData['cadet']['group']['name'] + ' ' +  'взвод' + ' | ячейка: ' + cadetData['cadet']['pm_cell_id']}}</div>
      <div>{{ cadetData['cadet']['course']['name'] + '-й курс'}}</div>
    </v-card-subtitle>

    <v-card-text class="pt-0 mt-0">
      <!--h6 class="ma-0">{{cadetData['cadet']['name'] + ' ' + cadetData['cadet']['surname']}}</h6>
      <div class="text-medium-emphasis">
            {{"@obormotik"}}
      </div-->
      <div class="d-flex align-center justify-content-start py-0">
        <v-avatar
          class="ml-1 my-3 mr-4"
          size="55"
        >
          <!--v-img
            alt="doggy"
            :src="`https://thispersondoesnotexist.com/?${Date.now() + Math.random()}`"
          ></v-img-->

            <v-img
                style="opacity: 0.95"
              alt="doggy"
              :src="getUserAvatarUrl(cadetData['cadet']['user']['username']/*['avatar']['url']*/)"
            ></v-img>

        </v-avatar>
        <div>
          <h5 class="ma-0 text-light-emphasis">
            {{cadetData['cadet']['name'] + ' ' + cadetData['cadet']['surname']}}
          </h5>
          <router-link :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '100%'}"
            :to="{ name: 'user', params: { username: cadetData['cadet']['username'] } }" style="color:#00406b; text-decoration: none; opacity:0.8"
            @click="navigateToUserPage"
                       class="font-weight-light"
          >
            <div v-if="cadetData['cadet']['user']['username']">
              {{'@'+ cadetData['cadet']['user']['username']}}
            </div>
            <div v-else>
              @yasobakayasobaka
            </div>
          </router-link>
        </div>
      </div>
    </v-card-text>



      <v-divider class="mx-3 mt-0 mb-0 pb-3"/>
      <v-expand-transition>
        <div
          v-show="editeMode"
          class="m-0 p-0 text-center"
          >
              <v-btn
              @click="this.$emit('edit', cadetData)"
              class="text-none"
              color="medium-emphasis"
              min-width="92"
              variant="outlined"
              rounded
              :disabled="disabled"
           >
             Замена
           </v-btn>
        </div>
    </v-expand-transition>


  </v-card>
</template>

<script>
//import editRoleDialog from "@/components/EditRoleDialog";
/*
import router from "@/router";
*/
import StaticDataService from "@/services/static-data.service";
/*
import {mapActions} from "vuex";
*/

export default {
  name: "RoleCard",
  //components:{editRoleDialog}
  props:{
    cadetData:{
      type: Object,
      required: true
    },
    disabled: {
      type: Boolean,
      required: true
    },
    editeMode:{
      type: Boolean
    }
  },
  computed: {

  },
  methods: {
    /*...mapActions('layoutStore', ['closeDutyDialog']),*/
    // WARNING: do not close the dialog directly as it needs to send
    // unlock request when closed. Emit closeDialog event instead!

    getUserAvatarUrl(username) {
      return StaticDataService.getUserAvatarUrl(username);
    },
    navigateToUserPage() {
      this.$emit('closeDutyDialog')
      this.$router.push({ name: 'user', params: { username: this.cadetData['cadet']['user']['username'].toString() } });
    }
  }
}
</script>

<style scoped>
  .underline {
    text-decoration: none;
  }
  .underline:hover {
    text-decoration: underline;
  }
</style>