<template>
  <v-row justify="center">
    <v-col cols="12" md="8">
      <v-card elevation="2" class="pa-4 rounded-xl">
        <v-data-table-virtual
          :headers="headers"
          :items="items"
          class="justify-content-center"
          :items-per-page="-1"
          hide-default-footer
        >
          <template v-slot:top>
            <v-toolbar
              flat
            >
              <v-toolbar-title>
                <div class="text-h5 text-medium-emphasis ps-2"> {{ title || 'Июнь 2007' }} </div>
              </v-toolbar-title>

              <!--v-divider
                class="mx-4"
                inset
                vertical
              ></v-divider-->
              <edit-duty-dialog
                :headers="headers"
                :selected-duty-id="selectedDutyId"
                :selected-duty="selectedDuty"
                :dialog="dialogVisible"
                @close="dialogVisible = false"
                @save="saveItem"
              ></edit-duty-dialog>

              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancel</v-btn>
                    <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>

            </v-toolbar>
          </template>

          <template v-slot:[`item.actions`]="{ item }">
            <v-icon
              class="me-2"
              size="small"
              @click="editItem(item)"
            >
              mdi-pencil
            </v-icon>
            <v-icon
              size="small"
              @click="deleteItem(item)"
            >
              mdi-delete
            </v-icon>
          </template>
          <template v-slot:no-data>
            <v-btn
              color="primary"
              @click="initialize"
            >
              Reset
            </v-btn>
          </template>
        </v-data-table-virtual>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import EditDutyDialog from "@/components/EditDutyDialog";

export default {
  components: {EditDutyDialog},
  name: 'MonthTable',
  props: {
    title: {
      type: String
    },
    headers: { // passed all along the home page since they're the same for the whole location tab
      type: Array,
      required: true
    },
    monthData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      dialogVisible: false,
      dialogDelete: false,
      selectedDuty: {},
      selectedDutyId: null
    }
  },
  computed: {
    formTitle() {
      return this.selectedDuty.id ? 'Edit Item' : 'New Item'
    },
    items() {
      console.log('RECOMPUTING THE ITEMS OF MONTH')
      return this.getMonthItems(this.monthData);
    }
  },
  methods: {
    getMonthItems(monthData) {
      return Object.values(monthData).map(day => {
        const duty = {
          id: day.id, // will pass this to dialog to fetch duty data
          date: day.date,
        };
        // add roles data
        Object.keys(day['cadets_with_roles']).forEach(cadetId => {
          const roleIndex = Object.keys(day['cadets_with_roles']).indexOf(cadetId);
          const role = Object.values(this.headers)[roleIndex + 1]['key'];
          const cadet = day['cadets_with_roles'][cadetId]['cadet'];
          duty[role] = `${cadet['surname']} : ${cadet.group}`;   // cadet's surname and group as the cells content
        });
        return duty;
      });
    },

    editItem(item) {
      this.selectedDuty = { ...item }
      console.log('THE SELECTED ITEM IS:::::')
      console.log(JSON.stringify(item))
      this.selectedDutyId = item.id; // store the item ID
      //console.log(JSON.stringify(this.selectedItemId))
      //console.log(JSON.stringify(this.selectedItem))
      this.dialogVisible = true
    },
    deleteItem(item) {
      this.selectedDuty = { ...item }
      this.dialogDelete = true
    },
    saveItem() {
      // Call the API to save the edited item
      // Update the items array with the edited item
      this.dialogVisible = false
    }
  }
}
</script>
