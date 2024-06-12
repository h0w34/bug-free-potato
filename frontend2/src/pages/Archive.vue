<template>
  <div v-if="loading">
    <v-skeleton-loader type="button"/>
    <v-row justify="center">
      <v-col cols="12" md="8">

        <v-skeleton-loader type="text"/>
        <v-skeleton-loader
          type="table-heading, table-thead, table-row-divider@20"
          elevation="2" class=" rounded-xl"
        />
      </v-col>
    </v-row>
  </div>
  <div v-else>
    <ScheduleList v-if="dutiesWithLocations[selectedLocation]"
      :dutiesData="dutiesWithLocations" :selectedLocationId="selectedLocation"
                  :selectedTypeId="selectedDutyType" :headers="tableHeadersForLocation">
   </ScheduleList>
  </div>
</template>

<script>
import ScheduleList from "@/components/ScheduleList";

export default {
  name: "ArchivePage",
  components: {ScheduleList}
}
</script>

<style scoped>

</style>