<template>
  <v-app>
    <Sidebar v-if="status.loggedIn"/>
    <HeaderFull v-if="$route.meta.navbar"/>
<!--
    <Navbar/>
-->
    <v-main>
    <v-fade-transition >
      <router-view/>
    </v-fade-transition>
      </v-main>
  </v-app>

  <!--nav-main/-->
</template>

<script>

import HeaderFull from "@/components/navigation/HeaderFull";
import Sidebar from "@/components/navigation/Sidebar";
import {mapState, mapActions} from "vuex";
/*
import Navbar from "@/components/navigation/Navbar";
*/
//import NavMain from "@/components/NavMain";

export default {
  name: 'App',
  data: () => ({
  }),
  components: {
/*
    Navbar,
*/
    Sidebar,
    HeaderFull: HeaderFull,
  //  NavMain
  },
  computed: {
    ...mapState('authStore', ['status']),
    ...mapState('layoutStore', ['sidebar']),

  },
  methods:{
    ...mapActions('layoutStore', ['closeSidebar']),
    closeLayout(){
      if(this.sidebar){
        this.closeSidebar()
      }
    }
  }

}
</script>

<style>

</style>
