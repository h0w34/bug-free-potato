<template>
  <v-row justify="center">
    <v-col cols="12" md="8">
      <v-card elevation="2" class="pa-4 rounded-xl">
        <v-data-table
          :headers="headers"
          :items="items"
          class="justify-content-center"
          hide-default-footer
        >
          <template v-slot:top>
            <v-toolbar
              flat
            >
              <v-toolbar-title>{{ title || 'Июнь 2007' }}</v-toolbar-title>
              <!--v-divider
                class="mx-4"
                inset
                vertical
              ></v-divider-->

              <edit-item-dialog
                :headers="headers"
                :edited-item="editedItem"
                :dialog="dialog"
                @close="dialog = false"
                @save="saveItem"
              ></edit-item-dialog>

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
        </v-data-table>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import EditItemDialog from "@/components/EditDutyDialog";

export default {
  components: {EditItemDialog},
  name: 'MonthTable',
  props: {
    title: {
      type: String
    },
    headers: {
      type: Array,
      required: true
    },
    items: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      dialog: false,
      dialogDelete: false,
      editedItem: {}
    }
  },
  computed: {
    formTitle() {
      return this.editedItem.id ? 'Edit Item' : 'New Item'
    }
  },
  methods: {
    editItem(item) {
      this.editedItem = { ...item }
      this.dialog = true
    },
    deleteItem(item) {
      this.editedItem = { ...item }
      this.dialogDelete = true
    },
    saveItem() {
      // Call the API to save the edited item
      // Update the items array with the edited item
      this.dialog = false
    }
  }
}
</script>
