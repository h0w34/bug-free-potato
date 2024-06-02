<template>
  <ul class="nav nav-tabs">
    <li class="nav-item" v-for="(location, index) in locations" :key="index">
      <a class="nav-link" :class="{ active: index === activeIndex }" @click="setActiveIndex(index)">{{ location }}</a>
    </li>
  </ul>
</template>

<script>
export default {
  name: "LocationsTabs",
  props: {
    locations: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      activeIndex: 0
    }
  },
  methods: {
    setActiveIndex(index) {
      this.activeIndex = index;
    }
  }
}
</script>

<style scoped>
.nav-link {
  cursor: pointer;
}
</style>
