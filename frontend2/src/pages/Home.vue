<template>
  <!-- add a simple table here -->
  <NavLocations :locationNames="locationNames" @selectLocation="selectLocation"
                :dutyTypeNames="dutyTypeNames" @selectDutyType="selectDutyType"/>


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


  <!---v-data-table :headers="tableHeaders" :items="tableItems" class="elevation-1">
  </v-data-table--->
</template>

<script>
import NavLocations from "@/components/NavLocations";
import ScheduleList from "@/components/ScheduleList";
//import mockMock from "@/components/mock";

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
      loading: true,
      tableHeaders: [
        { text: 'Date', value: 'date' },
        { text: 'Duty Role', value: 'duty_role' },
      ],
      tableItems: [],
      locationsData : {}
    }
  },
  async mounted() {
    await this.fetchDuties();
    //await this.fetchDutyTypes(this.dutyTypes)
  },

  methods: {
    selectLocation(location) {
      console.log(location)
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

    async fetchDuties() {   // TODO: fetch data location by location --> refactor the api's json
      try {
        const params = new URLSearchParams();
        this.user_locations.forEach(id => params.append('location_ids', id.toString()));
        const response = await fetch(`http://localhost:8080/api/duties?${params}`,
      {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        this.dutiesWithLocations = await response.json()
        this.dutiesWithLocations = this.dutiesWithLocations['locations']

        this.loading = false
      } catch (error) {
        console.error('Error fetching duties:', error);
        return {'error': 'sorry network error.'}
      }
      this.initializeSelectors();
    },

    async fetchDutyTypes(dutyTypeIds) {
      const queryParams = new URLSearchParams();
      dutyTypeIds.forEach(id => queryParams.append('duty_type_ids', id));

      fetch(`https://localhost:8080/api/duty_types?${queryParams}`)
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

      fetch(`https://localhost:8080/api/locations?${queryParams}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          }
      )
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
      let headers = [
        { title: 'Дата', value: 'date' },
      ].concat(
        this.dutiesWithLocations[this.selectedLocation][
          'duty_types'
        ][this.selectedDutyType]['duty_roles']
        .map(obj => ({
          title: obj.name,
          // value: obj.name, for the bootstrap tables
          key: obj.name, // for vuetify tables
          sortable: false
        }))
     );
    headers.push({title: 'Действия', key: 'actions', sortable: false})
      return headers
},
  }
}
</script>
