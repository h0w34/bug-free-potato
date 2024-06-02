<template>
    <!--h1>MocK.</h1-->
    <!--{{h2}}-->
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
          <!--MonthTable :headers="h2" :items="getMonthData(monthData)" :title="month + '/' + year"/-->
          <m-t :headers="h2" :items="getMonthItems(monthData)" :title="month + '/' + year"/>

          <!--MonthTable
            :year_month="[year, month]"
            :headers="headers"
            :table_data="getTableData(monthData)"
            :td="getMonthData(monthData)"
            :h2="h2"
          /-->
          <hr>
        </div>
      </div>
    </div>
    </div>

</template>

<script>
// the schedule must render a list of any duties types mixed
import {createVuetify} from 'vuetify';
//import MonthTable from "@/components/MonthTable";
import MT from "@/components/MT";
//import MockTable from "@/components/MockTable";

export default {
  setup() {
    const vuetify = createVuetify();
    return { vuetify };
  },
  name: "ScheduleList",
  components: {/*MonthTable*/MT, /*MockTable*/},
  //components: {MonthTable, mockMock},
  props: {
    dutiesData: {  // duties of a concrete type
      type: Object,
      required: true
    },
    headers:{
      type: Array,
      required: true
    },
    h2:{
      type: Array,
      required: true
    }

  },
  methods: {
    /*getTableData(monthData){
      return Object.values(monthData).map(day => {
          return day['cadets_with_roles'].map(cadet => cadet[0]['surname'] + ": " + cadet[0]['group']);
      });
    },*/

    getMonthItems(monthData) {
      return Object.values(monthData).map(day => {
        const duty = {
          date: day.date,
        };
        // add roles data
        Object.keys(day.cadets_with_roles).forEach(cadetId => {
          const roleIndex = Object.keys(day.cadets_with_roles).indexOf(cadetId);
          const role = Object.values(this.headers)[roleIndex + 1];
          const cadet = day.cadets_with_roles[cadetId][0];
          duty[role] = `${cadet.surname} : ${cadet.group}`;   // cadet's surname and group as the cell contents
        });
        return duty;
      });
    }

},
  computed:{
  }
};
</script>
