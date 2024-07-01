<template>
  <div
    style="border: 3px solid #eaebf1; width: 180px"
    class="rounded-xl p-3  pb-2 text-truncate gap-2 align-center text-wrap d-flex justify-content-center"
  >
    <h5>{{emoji ? emoji : '❓'}}</h5>
    <h6  >{{ text+':' }}</h6>
    <h3 class="mr-2">{{num}}</h3>
  </div>
</template>

<script>
export default {
  name: "StatsChip",
  props: {
    emoji:{
      type: String,
      required: false
    },
    text:{
      type: String,
      required: true
    },
    num:{
      type: Number,
      required: true
    },
  }
}
</script>

<style scoped>

</style>