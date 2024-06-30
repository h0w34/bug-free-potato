<template>
<!--        <v-treeview :items="items"></v-treeview>-->

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
      items: [
        {
          id: 1,
          title: 'Applications :',
          children: [
            { id: 2, title: 'Calendar : app' },
            { id: 3, title: 'Chrome : app' },
            { id: 4, title: 'Webstorm : app' },
          ],
        },
        {
          id: 5,
          title: 'Documents :',
          children: [
            {
              id: 6,
              title: 'vuetify :',
              children: [
                {
                  id: 7,
                  title: 'src :',
                  children: [
                    { id: 8, title: 'index : ts' },
                    { id: 9, title: 'bootstrap : ts' },
                  ],
                },
              ],
            },
            {
              id: 10,
              title: 'material2 :',
              children: [
                {
                  id: 11,
                  title: 'src :',
                  children: [
                    { id: 12, title: 'v-btn : ts' },
                    { id: 13, title: 'v-card : ts' },
                    { id: 14, title: 'v-window : ts' },
                  ],
                },
              ],
            },
          ],
        },
        {
          id: 15,
          title: 'Downloads :',
          children: [
            { id: 16, title: 'October : pdf' },
            { id: 17, title: 'November : pdf' },
            { id: 18, title: 'Tutorial : html' },
          ],
        },
        {
          id: 19,
          title: 'Videos :',
          children: [
            {
              id: 20,
              title: 'Tutorials :',
              children: [
                { id: 21, title: 'Basic layouts : mp4' },
                { id: 22, title: 'Advanced techniques : mp4' },
                { id: 23, title: 'All about app : dir' },
              ],
            },
            { id: 24, title: 'Intro : mov' },
            { id: 25, title: 'Conference introduction : avi' },
          ],
        },
      ],
    }),
  components: {
    HeaderFull, Sidebar
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
  .unselectable {
    -webkit-user-select: none; /* Safari */
    -ms-user-select: none; /* IE 10 and IE 11 */
    user-select: none; /* Standard syntax */
  }

  /*.v-tooltip__content {
     color: #FFFFFF !important; !* Set the tooltip text color to white *!
  }*/
</style>
