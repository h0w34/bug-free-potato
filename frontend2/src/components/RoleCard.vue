<template>
  <v-card
    class="mx-auto rounded-xl"
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
    <v-card-subtitle class="my-2">
      {{cadetData['cadet']['group'] + ' ' +  'взвод' + ' | ячейка: ' + cadetData['cadet']['pm_cell_id']}}
    </v-card-subtitle>

    <v-card-text>
      <!--h6 class="ma-0">{{cadetData['cadet']['name'] + ' ' + cadetData['cadet']['surname']}}</h6>
      <div class="text-medium-emphasis">
            {{"@obormotik"}}
      </div-->
      <div class="d-flex align-center justify-content-between py-0">
        <div>
          <h6 class="ma-0">{{cadetData['cadet']['name'] + ' ' + cadetData['cadet']['surname']}}</h6>
          <div class="text-medium-emphasis">
            <router-link
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
            :src="`https://steamuserimages-a.akamaihd.net/ugc/1483325328769942736/3A592FE50FDB0010B49C7D86777B0CC1D7510276/`"
          ></v-img>
        </v-avatar>
      </div>

    </v-card-text>

    <v-divider class="ma-2 mb-0"/>
      <template v-slot:actions>
       <v-spacer/>
        <!--v-btn
            @click="this.$emit('edit', cadetData)" -->
         <v-btn
            @click="this.$emit('edit', cadetData)"
            class="text-none mt-2 mb-1"
            color="medium-emphasis"
            min-width="92"
            variant="outlined"
            rounded
            :disabled="disabled"
         >
           Замена
         </v-btn>
       <v-spacer />
      </template>
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