<template>
  <v-layout>
    <v-navigation-drawer
      class="rounded-start-4"
      v-model="sidebar"
      location="right"
      temporary
    >
      <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
      >
          <div
            class="mt-2 d-flex text-align align-center justify-space-between"
          >
            <h5>John Leider</h5>
            <v-btn icon="mdi-close" variant="text" @click="closeSidebar"/>
          </div>

      </v-list-item>

      <v-divider
        class="mx-2"
      />

      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Home" value="home"></v-list-item>
        <v-list-item prepend-icon="mdi-forum" title="About" value="about"></v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-layout>
</template>

<script>
import {mapActions, mapState} from 'vuex';
// TODO: make this use vuex
export default {
  // eslint-disable-next-line
  name: "Sidebar",
  computed: {
    ...mapState('layoutStore', ['sidebar']),
    ...mapState('authStore', ['user']),

  },
  methods: {
      ...mapActions('layoutStore', ['closeSidebar']),

  },

}
</script>

<style scoped>

</style>