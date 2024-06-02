<template>
  <v-dialog v-model="localDialog" max-width="500px">
    <v-card>
      <v-card-title>{{ formTitle }}</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <template v-for="header in headers" :key="header.value">
              <v-col cols="12" >
                <v-text-field
                  v-model="localEditedItem[header.value]"
                  :label="header.title"
                  required
                ></v-text-field>
              </v-col>
            </template>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'EditItemDialog',
  props: {
    headers: {
      type: Array,
      required: true
    },
    editedItem: {
      type: Object,
      required: true,
    },
    dialog: {
      type: Boolean,
      required: true,
    }
  },
  data() {
    return {
      localEditedItem: this.editedItem,
      //localDialog: this.dialog
      //dialog: false
    }
  },
  computed: {
    localDialog: {
      get() {
        return this.dialog;
      },
      set(value) {
        this.$emit('update:dialog', value);
      }
    },
    formTitle() {
      return this.editedItem.id ? 'Edit Item' : 'New Item'
    }
  },
  methods: {

    close() {
      this.$emit('close')
    },
    save() {
      this.$emit('save')
    }
  },
  mounted() {
    console.log('MOUNTED!')
  },
  watch: {
    /*dialog(val) {
      this.localDialog = val
    },
    localDialog(val) {
      this.$emit('input', val)
    }*/
  }
}
</script>
