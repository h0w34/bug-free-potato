
<!-- encapsulates single month data for a specific location-->
<template>

  <v-data-table width="500px" :headers="h2" :items="td" class="elevation-1" >
  </v-data-table>
  <div class="container align-content-center p-5">
    <div class="d-flex justify-content-center">
      <div class="col-auto">
        <h3>{{ year_month[1] + "/" + year_month[0] }}</h3>
        <div class="card">
         <table class="table table-striped table-bordered">
            <thead>
              <tr>
                <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in table_data" :key="index">
                <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
//import { EditableTable } from 'vuetify-editable-table';

export default {
  data() {
    return {
    };
  },
  name: "MonthTable",
  props: {
    year_month: {
      type: Array,
      required: true
    },
    headers: {  // must include those that are present for each duty in the json
      type: Array,
      required: true
    },
    td: {
      type: Array
    },
    h2:{
      type: Array
    },
    /*


    */

    table_data: {
      type: Array,
      required: true
    },
    table_items: {
      type: Array
    }
  }
}

</script>

<style scoped>

</style>
