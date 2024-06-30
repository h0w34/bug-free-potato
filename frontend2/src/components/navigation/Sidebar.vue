<template>
    <v-navigation-drawer
      width="350"
      class="rounded-start-4"
      v-model="sidebar"
      location="right"
      temporary
    >
      <v-list-item
        class="mt-3"
        :prepend-avatar="getUserAvatarUrl(user['username'])"
      >
          <div
            class="d-flex text-align align-center justify-space-between"
          >
            <div class="text-align align-center">
              <h5 class="mb-0">{{ user['cadet']['name'] + ' ' + user['cadet']['surname'] }}</h5>
              <div class="text-medium-emphasis mb-2 font-weight-light" >
                <div style="margin-left: 2px;"   v-if="user['email']">
                  {{user['email']}}
                </div>
                <div class="text-medium-emphasis text-body-2 font-weight-light" v-else>
                  Без привязанной почты
                </div>
              </div>
            </div>
            <v-btn icon="mdi-close" variant="text" @click="closeSidebar"/>
          </div>
      </v-list-item>



      <v-list density="compact" nav class="unselectable mx-3 pt-0">
        <v-divider class="mx-2 mt-1 mb-2" />

        <v-list-item class="rounded mb-0 py-0" @click="navigateToProfile">
          <div class="d-inline-flex gap-2 text-center align-center">
            <v-icon size="small">
              mdi-account
            </v-icon>
            <div class="text-light-emphasis">
              Мой профиль
            </div>
          </div>
        </v-list-item>

        <v-list-item class="rounded py-0">
          <div class="d-inline-flex gap-2 text-center align-center">
            <v-icon size="small">
              mdi-account-group
            </v-icon>
            <div class="text-light-emphasis">
              Ваша группа
            </div>
          </div>
        </v-list-item>

        <v-divider class="mb-2"/>

        <v-list-item  class="rounded mb-0 py-0" >
          <div class="d-inline-flex gap-2 text-center align-center">
            <v-icon size="small">
              mdi-cog
            </v-icon>
            <div class="text-light-emphasis">
              Настройки
            </div>
          </div>
        </v-list-item>

        <v-list-item  class="rounded py-0" @click="logoutAndRedirect">
          <div class="d-inline-flex gap-2 text-center align-center">
            <v-icon size="small">
              mdi-logout
            </v-icon>
            <div class="text-light-emphasis">
              Выйти
            </div>
          </div>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
</template>

<script>
import {mapActions, mapState} from 'vuex';
import StaticDataService from "@/services/static-data.service";

// TODO: make this use vuex
export default {
  // eslint-disable-next-line
  name: "Sidebar",
  computed: {
    ...mapState('layoutStore', ['sidebar']),
    ...mapState('authStore', ['user']),

  },
  methods: {
    navigateToProfile() {
      // Check if the sidebar is open
      if (this.$store.state.layoutStore.sidebar) {
        // Dispatch the action to close the sidebar
        this.$store.dispatch('layoutStore/closeSidebar');
      }
      // Navigate to the user profile page
       this.$router.push({ name: 'user', params: { username: this.user.username } });
    },

    async logoutAndRedirect(){
      this.$router.push('/login');
      this.logout()
    },

    ...mapActions('layoutStore', ['closeSidebar']),
    ...mapActions('authStore', ['logout']),
    getUserAvatarUrl(username) {
      return StaticDataService.getUserAvatarUrl(username);
    },
  },

}
</script>

<style scoped>
  .unselectable {
    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none;   /* Chrome/Safari/Opera */
    -khtml-user-select: none;    /* Konqueror */
    -moz-user-select: none;      /* Firefox */
    -ms-user-select: none;       /* Internet Explorer/Edge */
    user-select: none;           /* Non-prefixed version, currently
                                  not supported by any browser */
  }
</style>