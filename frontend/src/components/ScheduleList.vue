<template>
    <!--h1>MocK.</h1-->
    <!--{{headers}}-->
    <hr>
    <div v-if="!dutiesData">
        LOADING...
    </div>
    <div v-else>
        <div v-for="(yearData, year) in dutiesData['duties']" :key="year">
          <div>
            <h1>Год {{year}}</h1>
        <div v-for="(monthData, month) in yearData" :key="month">
          <div v-if="monthData">
            <!--{{month}}-->
          </div>
            <!--{{monthData}}-->
          <MonthTable
            :year_month="[year, month]"
            :headers="headers"
            :table_data="getTableData(monthData)"
          />
          <hr>
        </div>
      </div>
    </div>
    </div>

</template>

<script>
// the schedule must render a list of any duties types mixed
import MonthTable from "@/components/MonthTable";
import { createVuetify } from 'vuetify';

export default {
  setup() {
    const vuetify = createVuetify();
    return { vuetify };
  },
  name: "ScheduleList",
  components: {MonthTable},
  props: {
    dutiesData: {  // duties of a concrete type
      type: Object,
      required: true
    },
    headers:{
      type: Array,
      required: true
    }
  },
  methods: {
    getTableData(monthData){
      return Object.values(monthData).map(day => {
          let dayData = day['cadets_with_roles'].map(cadet => cadet[0]['surname'] + ": " + cadet[0]['group']);
          return [day['date']].concat(dayData);
      });
    }
  },
  computed:{
  }
};
</script>
