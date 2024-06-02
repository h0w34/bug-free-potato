<template>
  <!-- add a simple table here -->
  <NavLocations :locationNames="locationNames" @selectLocation="selectLocation"
                :dutyTypeNames="dutyTypeNames" @selectDutyType="selectDutyType"/>
  <ScheduleList v-if="dutiesWithLocations[selectedLocation]"
                :dutiesData="dutiesWithLocations[selectedLocation]['duty_types'][selectedDutyType]"  :headers="tableHeadersForLocation">
  </ScheduleList>
  <v-data-table :headers="tableHeaders" :items="tableItems" class="elevation-1">
  </v-data-table>
</template>

<script>
import NavLocations from "@/components/NavLocations";
import ScheduleList from "@/components/ScheduleList";

export default {
  name: "HomePage",
  components: {NavLocations, ScheduleList},
  data() {
    return {
      user_locations: [1, 2],  //assume these are obtained  via JWT
      user_duty_types: [1,2],
      selectedLocation: null,
      selectedDutyType: null,
      dutiesWithLocations: {},
      tableHeaders: [
        { text: 'Date', value: 'date' },
        { text: 'Duty Role', value: 'duty_role' },
      ],
      tableItems: []
    }
  },
  async mounted() {
    await this.fetchDuties();
    //await this.fetchDutyTypes(this.dutyTypes)
  },

  methods: {
    selectLocation(location) {
      this.selectedLocation = location;
      //this.fetchDuties(location);
    },
    selectDutyType(duty_type) {
      this.selectedDutyType = duty_type;
      //this.fetchDuties(location);
    },

    initializeSelectors(){
      if(this.dutiesWithLocations){
        this.selectedLocation = 0;
        this.selectedDutyType = 0;
      }
    },

    async fetchDuties() {
      try {
        const response = await fetch('http://localhost:5000/duties');
        const parsed  = await response.json();
        this.dutiesWithLocations = parsed['locations']
      } catch (error) {
        console.error('Error fetching duties:', error);
        return {'error': 'sorry network error.'}
      }
      this.initializeSelectors();
    },

    async fetchDutyTypes(dutyTypeIds) {
      const queryParams = new URLSearchParams();
      dutyTypeIds.forEach(id => queryParams.append('duty_type_ids', id));

      fetch(`https://localhost:5000/duty_types?${queryParams}`)
        .then(response => response.json())
        .then(data => {
          this.dutyTypes = data;
        })
        .catch(error => {
          console.error(error);
        });
    },

    async fetchLocations(locationIds) {
      const queryParams = new URLSearchParams();
      locationIds.forEach(id => queryParams.append('location_ids', id));

      fetch(`https://localhost:5000/locations?${queryParams}`)
        .then(response => response.json())
        .then(data => {
          this.locations = data;
          console.log(this.locations)
        })
        .catch(error => {
          console.error(error);
        });
    },

    dutiesDataPerLocation(){
        if (this.selectedLocation) {
          return this.dutiesWithLocations[this.selectedLocation]["0"];
        } else if (this.dutiesWithLocations) {
          return 'Loading...';
        } else {
          return 'No locations loaded!';
        }
    }
  },
  computed: {
    locationNames(){
      return Object.values(this.dutiesWithLocations).map(item => item.name);
    },
    tableHeadersForLocation() {
      return ['Дата'].concat(
          this.dutiesWithLocations[this.selectedLocation][
              'duty_types'][this.selectedDutyType]['duty_roles'
              ].map(obj => obj.name))
    },
    dutyTypeNames(){

      return 1;
    }
  }
}
</script>
