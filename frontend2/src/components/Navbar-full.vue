<template>
<nav class="navbar navbar-expand-lg bg-body-tertiary p-3">
  <div class="container d-flex justify-content-center gap-3">
    <router-link class="navbar-brand mr-0" to="/">Мои Утки🐥</router-link>

    <form class="container m-0" role="search" style="max-width: 500px">
      <div class="input-group">
        <span class="input-group-text" id="basic-addon1">@</span>
        <input type="text" class="form-control" placeholder="Имя/дата/место" aria-label="Username" aria-describedby="basic-addon1">
      </div>
    </form>

    <template v-if="user">
      <v-avatar
          @click.prevent
          @click="openSidebar"
          image="https://randomuser.me/api/portraits/men/78.jpg"
      />
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

</nav>
</template>

<script>
import {mapActions, mapState} from 'vuex';
/*import NavbarProfile from "@/components/user/navbarProfile";*/

export default {
  name: "Navbar-full",
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

    ...mapActions('layoutStore', ['openSidebar'])
  }
}
</script>

<style scoped>

</style>