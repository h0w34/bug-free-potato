<template>
  <navbar-full v-if="$route.meta.navbar"/>
  <!--nav-main/-->
  <router-view/>
</template>

<script>

import NavbarFull from "@/components/Navbar-full";
//import NavMain from "@/components/NavMain";

export default {
  name: 'App',
  components: {
    NavbarFull,
  //  NavMain
  },
  data() {
    return {}
  }
}
</script>

<style>
.navbar-full {
  position: sticky;
  top: 0;
  z-index: 1;
}
</style>
