<template>
 <v-card
        @click="$emit('click', data)"
        v-if="data"
        class="mx-auto rounded-xl"
        min-width="300"
        min-height="150"
        hover
      >
      <div v-if="data">
      </div>
      <v-card-title>
        {{data['name']}}
      </v-card-title>
      <v-card-subtitle>
        {{data['address']}}
      </v-card-subtitle>
  </v-card>
  <v-skeleton-loader v-else
        type="card"
        class="mx-auto rounded-xl"
        min-width="500"
        min-height="150"
        hover
  />
</template>

<script>
export default {
  name: "LocationCard",
  props:{
    data: {
      type: Object
    }
  }


}
</script>

<style scoped>

</style>