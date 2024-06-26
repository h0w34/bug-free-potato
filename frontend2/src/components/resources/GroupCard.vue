<template>
 <v-card
        v-if="data"
        class="mx-auto rounded-xl"
        min-width="300"
        max-width="350"
        min-height="150"
        hover
      >
      <div v-if="data">
      </div>
      <v-card-title>
        {{data['name']}} взвод
      </v-card-title>
      <v-card-subtitle>
        {{data['number_of_cadets']}} курсантов
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
  name: "GroupCard",
  props:{
    data: {
      type: Object
    }
  }


}
</script>

<style scoped>

</style>