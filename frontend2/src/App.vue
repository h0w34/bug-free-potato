<template>
  <navbar-full/>
  <nav-main/>
  <router-view/>
</template>

<script>

import NavbarFull from "@/components/Navbar-full";
import NavMain from "@/components/NavMain";

export default {
  name: 'App',
  components: {
    NavbarFull,
    NavMain
  },
  data() {
    return {}
  }
}
</script>

<style>

</style>
