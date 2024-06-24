<template>
  <v-app-bar
      class="navbar navbar-expand-lg bg-body-tertiary p-0"
      flat
      border="1"
      scroll-behavior="fade-image"
      scroll-threshold="30"
  >
  <div class="container d-flex justify-content-center gap-3 align-center">
    <router-link class="navbar-brand mr-0" to="/">Мои Утки🐥</router-link>
    <div>
      <v-btn class=" mt-1 mr-1" to="/" @click="goHome">Главная</v-btn>
      <v-btn class="mt-1 mr-1"  to="/resources" @click="goAbout">Ресурсы</v-btn>
     <v-btn class="mt-1" @click="goContact">Редактор</v-btn>
    </div>

    <form class="container m-0" role="search" style="max-width: 500px">
      <div class="input-group">
        <span class="input-group-text" id="basic-addon1">@</span>
        <input type="text" class="form-control" placeholder="Имя/дата/место" aria-label="Username" aria-describedby="basic-addon1">
      </div>
    </form>

    <template v-if="user">
      <button
        class="d-flex text-center align-center"
        @click="openSidebar"
      >
        <v-avatar
          class="mr-2"
          @click.prevent
          :image="getUserAvatarUrl(user['username'])"
        />
        <v-icon class="text-medium-emphasis">
          mdi-chevron-down
        </v-icon>
      </button>

<!--      <navbarProfile user="user"/>-->
   </template>
    <template v-else>
      <div class="d-inline-flex gap-2">
      <router-link to="/login" class="btn btn-sm btn-outline-secondary">
        Войти
      </router-link>
      <router-link to="/signup" class="btn btn-sm btn-outline-secondary">
        Зарегистрироваться
      </router-link>
    </div>
    </template>
  </div>
    </v-app-bar>
</template>

<script>
import {mapActions, mapState} from 'vuex';
/*import NavbarProfile from "@/components/user/navbarProfile";*/
import StaticDataService from "@/services/static-data.service";

export default {
  name: "HeaderFull",
  components: {/*NavbarProfile*/},
  computed: {
    ...mapState('authStore', ['user']),

  },
  data: () => ({
      fav: true,
      menu: false,
      message: false,
      hints: true,
    }),
  methods:{
    ...mapActions('layoutStore', ['openSidebar']),
    getUserAvatarUrl(username) {
        return StaticDataService.getUserAvatarUrl(username);
    },
  }
}
</script>

<style scoped>

</style>