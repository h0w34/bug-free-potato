<template>
  <v-data-table
    :headers="headers"
    :items="items"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-toolbar-title>Month Table</v-toolbar-title>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
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
  </v-data-table>

  <edit-duty-dialog
    v-model="dialog"
    :selected-item="editedItem"
    @save="saveItem"
  ></edit-duty-dialog>

</template>

<script>
import EditDutyDialog from "@/components/schedule/DutyDialog";

export default {
  components: {
    EditDutyDialog
  },
  props: {
    headers: {
      type: Array,
      required: true
    },
    items: {
      type: Array,
      required: true
    }
  },
  methods: {
    editItem(item) {
      // Call API to fetch the item details
      this.$axios.get(`api/items/${item.id}`)
        .then(response => {
          // Update the item details in the component
          this.editedItem = response.data;
          this.dialog = true;
        })
        .catch(error => {
          console.error(error);
        });
    },
    deleteItem(item) {
      // Call API to delete the item
      this.$axios.delete(`api/items/${item.id}`)
        .then(response => {
          // Remove the item from the items array
          this.items.splice(this.items.indexOf(item), 1);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>
