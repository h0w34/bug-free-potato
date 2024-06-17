<template>
  <v-card
    class="mx-auto rounded-xl pb-3"
    max-width="344"
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
    <v-card-subtitle class="my-2 mb-1">
      <div>{{cadetData['cadet']['group'] + ' ' +  'взвод' + ' | ячейка: ' + cadetData['cadet']['pm_cell_id']}}</div>
      <div>{{ cadetData['cadet']['course'] + '-й курс'}}</div>
    </v-card-subtitle>

    <v-card-text class="pt-0 mt-0">
      <!--h6 class="ma-0">{{cadetData['cadet']['name'] + ' ' + cadetData['cadet']['surname']}}</h6>
      <div class="text-medium-emphasis">
            {{"@obormotik"}}
      </div-->
      <div class="d-flex align-center justify-content-between py-0">
        <div>
          <h6 class="ma-0">{{cadetData['cadet']['name'] + ' ' + cadetData['cadet']['surname']}}</h6>
          <div class="text-medium-emphasis">
            <router-link
                :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '100%'}"
                :to="{ name: 'user', params: { username: 'johndoe' } }" style="color:#00406b; text-decoration: none">
              {{"@obormotik"}}
            </router-link>
          </div>
        </div>
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
            :src="require('../../../public/default_avatar.gif')"
          ></v-img>
        </v-avatar>
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
import router from "@/routers";

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
    navigateToUserPage() {
         router.push({ name: 'home', params: { username: 'johndoe' } });
    }
  }
}
</script>

<style scoped>

</style>