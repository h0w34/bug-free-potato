<template>
    <!--h1>MocK.</h1-->
    <!--{{h2}}-->
  <hr>
    <div v-if="!dutiesDataByYears">
      {{'Uh! Something went wrong when fetching the duties...'}}
    </div>
    <div v-else>
        <div v-for="(yearData, year) in dutiesDataByYears['duties']" :key="year">
          <div>
            <div  class="text-h3 text-medium-emphasis font-weight-light justify-space-between ps-2">Год {{year}}</div>
        <div v-for="(monthData, month) in yearData" :key="month">

            <month-table :headers="headers" :monthData="monthData" :title="month + '/' + year"/>

          <hr>
        </div>
      </div>
    </div>
    </div>
</template>

<script>
// the schedule must render a list of any duties types mixed
//import MonthTable from "@/components/MonthTable";
import MonthTable from "@/components/MonthTable";
//import MockTable from "@/components/MockTable";

export default {
  name: "ScheduleList",
  components: {/*MonthTable*/MonthTable, /*MockTable*/},
  //components: {MonthTable, mockMock},
  data(){
    return{
    }
  },
  props: {
    dutiesData: {  // duties of a concrete type
      type: Object,
      required: true
    },
    headers:{
      type: Array,
      required: true
    },
    selectedTypeId:{
      type: Number,
      required: true
    },
    selectedLocationId:{
      type: Number,
      required: true
    }
  },
  methods: {
    arr(){
      console.log('LOCATION CHANGED'),
      console.log(this.selectedLocationId)
    }
    /*getTableData(monthData){
      return Object.values(monthData).map(day => {
          return day['cadets_with_roles'].map(cadet => cadet[0]['surname'] + ": " + cadet[0]['group']);
      });
    },*/
  },
  computed:{
    dutiesDataByYears() {
      return this.dutiesData[this.selectedLocationId]['duty_types'][this.selectedTypeId]
    }
  },
  watch: {
    selectedLocationId: {
      handler: 'arr',
      immediate: true
    }
  }
}
</script>
