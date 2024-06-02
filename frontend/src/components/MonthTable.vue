
<!-- encapsulates single month data for a specific location-->
<template>
    <EditableTable
    :headers="headerss"
    :items="duties"
    :edit-mode="true"
    />

  <div class="container-fluid align-content-center p-5">
    <div class="d-flex justify-content-center">
      <div class="col-auto">
        <h3>{{ year_month[1] + "/" + year_month[0] }}</h3>
        <div class="card">
         <table class="table">
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
      headerss: [
        { text: 'Name', value: 'name' },
        { text: 'Description', value: 'description' },
        { text: 'Date', value: 'date' },
        { text: 'Time', value: 'time' },
      ],
      duties: [
        {
          id: 1,
          name: 'Duty 1',
          description: 'This is duty 1',
          date: '2024-06-01',
          time: '08:00',
        },
        // Add more duties
      ],
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
.card {
  border: 1px solid #dee2e6;
}
</style>
