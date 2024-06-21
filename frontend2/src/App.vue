<template>

  <navbar-full v-if="$route.meta.navbar"/>
  <Sidebar
  />

  <v-fade-transition mode="out-in">
    <router-view/>
  </v-fade-transition>

  <!--nav-main/-->
</template>

<script>

import NavbarFull from "@/components/Navbar-full";
import Sidebar from "@/components/user/Sidebar";
import {mapActions} from "vuex";
//import NavMain from "@/components/NavMain";

export default {
  name: 'App',
  data: () => ({
  }),
  components: {
    Sidebar,
    NavbarFull,
  //  NavMain
  },
  computed: {

  },
  methods:{
    ...mapActions('layoutStore', ['closeSidebar'])

  }

}
</script>

<style>

</style>
