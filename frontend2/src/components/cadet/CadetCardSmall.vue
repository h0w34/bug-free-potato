<template>
  <v-card
    class="mx-auto rounded-xl"
    max-width="237"
    hover
  >
    <v-card-title>
      {{ cadetData['raw']['name'] + ' ' + cadetData['raw']['surname'] }}
    </v-card-title>
    <v-card-subtitle>
      <div class="text-h8">
        @sobakayasobaka
      </div>
      {{ cadetData['raw']['group'] + ' взвод | ячейка: ' + cadetData['raw']['pm_cell_id'] }}
    </v-card-subtitle>
    <v-divider />
    <template v-slot:actions>
      <v-spacer />
      <v-btn
        @click="this.$emit('select', cadetData)"
        class="text-none"
        color="medium-emphasis"
        min-width="64"
        variant="outlined"
        rounded
      >
        Выбрать
      </v-btn>
      <v-spacer />
    </template>
  </v-card>
</template>

<script>
export default {
  name: "CadetCardSmall",
  props: {
    cadetData: {
      type: Object
    }
  },
  data() {
    return {
      selected: false
    }
  }
}
</script>

<style scoped>
.selected {
  border: 1px solid #4CAF50;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>
