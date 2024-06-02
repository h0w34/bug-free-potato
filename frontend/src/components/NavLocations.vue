<template>
  <ul class="nav nav-tabs">
    <!--Locations: -->

    <li class="nav-item" v-for="(locationName, index) in locationNames" :key="index">
      <a class="nav-link" :class="{ active: index === activeIndex }" @click="setActiveIndex(index)">{{ locationName }}</a>
    </li>
    <li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" role="button" aria-expanded="false">Тип суток</a>
    <ul class="dropdown-menu">
      <li v-for="(name, index) in dutyTypeNames" :key="index">
        <a class="dropdown-item">{{name}}</a>
      </li>
      <li><a class="dropdown-item" href="#">Action</a></li>
      <li><a class="dropdown-item" href="#">Another action</a></li>
      <li><a class="dropdown-item" href="#">Something else here</a></li>
      <li><hr class="dropdown-divider"></li>
      <li><a class="dropdown-item" href="#">Separated link</a></li>
    </ul>
  </li>
  </ul>



</template>

<script>
export default {
  name: "NavLocations",
  props: {
    locationNames: {
      type: Array,
      required: true
    },
    dutyTypeNames:{
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
      this.$emit('selectLocation', this.activeIndex);
    }
  }
}
</script>

<style scoped>

</style>