<template>
  <v-dialog v-model="localDialog" max-width="800" max-height="auto" persistent>

    <v-dialog v-model="isMovingCadets" max-width="750px">
        <move-cadets-dialog/>
    </v-dialog>

    <edit-role-dialog :selected-cadet-data="selectedCadetData" :selectedDutyId="selectedDutyId"
                      :dialog="isEditingRole" @close="closeRoleDialog" @update="updateEditDialogLayout"/>

    <v-card class="rounded-xl my-4"
      :disabled="loadingEditDialog"
      :loading="loadingEditDialog"
    >
      <template v-slot:loader="{ isActive }">
        <v-progress-linear
          :active="isActive "
          color="deep-purple"
          height="4"
          indeterminate
        ></v-progress-linear>
      </template>

      <v-card-title class="d-flex justify-space-between align-center">
        <div class="text-h5 text-medium-emphasis ps-3">
          {{ currentTitle }}
        </div>
        <v-btn icon="mdi-close" variant="text" @click="closeDialog"></v-btn>
      </v-card-title>

      <v-card-subtitle class="d-flex justify-space-between align-center">
        <div class="text-medium-emphasis ps-3">
          <h6>{{currentSubTitle}}</h6>
        </div>
      </v-card-subtitle>

      <v-divider class="mx-10"></v-divider>

      <v-card-text>
        <v-container class="py-0" >
          <div v-if="dutyData">
            <v-row class="justify-content-center">
              <v-col
                v-for="(cadet_data, i) in dutyData['cadets_with_roles']"
                :key="i"
                cols="auto"
                md="4"
              >
              <role-card :cadet-data="cadet_data" @edit="openRoleDialog"/>
              </v-col>
            </v-row>
          </div>
          <div v-else-if="error">
            <v-row align="center" justify="center" dense>
              <v-col cols="12"  class="text-center">
                <h6>Упс! Не удалось загрузить сутки.</h6>
                <br>
                <h6>Перезагрузите страницу.</h6>
              </v-col>
            </v-row>
          </div>
          <div v-else>
              <v-row align="center" justify="center" dense>
                <v-col
                  v-for="i in 3"
                  :key="i"
                  cols="12"
                  md="4"
                >
                  <v-skeleton-loader type="card@2"/>
                </v-col>
              </v-row>
            <!--v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular-->
          </div>
        </v-container>
      </v-card-text>
      <v-divider class="mx-10 my-2"></v-divider>
      <v-card-actions class="mx-3">
        <v-spacer></v-spacer>
          <div class="my-2">
            <v-btn class="text-none"
              color="medium-emphasis"
              variant="outlined"
              @click="closeDialog"
          >Отмена</v-btn>

          <v-btn class="text-none"
              color="medium-emphasis"
              variant="outlined"
              @click="saveAndShowLoader"
          >Сохранить</v-btn>
        </div>

      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import RoleCard from "@/components/RoleCard";
import EditRoleDialog from "@/components/EditRoleDialog";
import MoveCadetsDialog from "@/components/MoveCadetsDialog";
//import EditRoleDialog from "@/components/EditRoleDialog";


export default {
  name: 'EditDutyDialog',
  components: {MoveCadetsDialog, EditRoleDialog, RoleCard},
  props: {
    headers: {
      type: Array,
      required: true
    },
    selectedDuty: {
      type: Object,
      required: true,
    },
    dialog: {
      type: Boolean,
      required: true,
    },
    selectedDutyId: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      localSelectedDuty: this.selectedDuty,
      dutyData: null,
      loadingEditDialog: false,

      isEditingRole: false,
      isMovingCadets:false,

      selectedCadetData: {},
      error: false,

      monthNames: [
          'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
      ]

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
    currentTitle () {
      return 'Редактировать сутки'
    },
    currentSubTitle() {
      if (this.dutyData) {
        const date = new Date(this.dutyData['date']);
        const day = date.getDate();
        const month = date.getMonth();
        const address = this.dutyData['location']['address'];
        return `Изменение суток на ${day} ${this.monthNames[month]}, ${address}`;
      } else return '';
    }
  },
  methods: {
    showError(){
      this.error = true
    },
    updateEditDialogLayout(isUpdated){
      if(isUpdated){
        this.loadingEditDialog = true
      setTimeout(()=>this.loadingEditDialog = false, 500)
       this.fetchDutyData();
      }

    },
    closeDialog() {
      this.loadingEditDialog = false;
      this.$emit('close');
    },
    closeRoleDialog(){
      this.isEditingRole = false
    },
    openRoleDialog(cadet_data){
        console.log('SELECTED CADET DATA:')
        console.log(cadet_data)
        this.selectedCadetData = cadet_data;
        this.isEditingRole = true;
    },

    saveAndShowLoader() {
      this.loadingEditDialog = true;
      setTimeout(() => {
        this.$emit('save');
        this.loadingEditDialog = false;
      }, 1000);
    },
    async updateLayout(isUpdated){
      if(isUpdated){
        this.loading = true;
        this.loadingStartTime = performance.now();
        await this.fetchDutyData();
        // Set a minimum delay of 500ms before setting loading to false
        await new Promise(resolve => setTimeout(resolve, Math.max(500 - (performance.now() - this.loadingStartTime), 0)));
        this.loading = false;
    }
}
  },
  watch: {
    selectedDutyId: {
      handler(){
        this.dutyData = null
        console.log('selectedDutyId:', JSON.stringify(this.selectedDutyId ))
        this.fetchDutyData();
      } ,
      immediate: true
    }
  }
}
</script>

<template>


</template>

<script>
export default {
  name: "DutyInfoDialog"
}
</script>

<style scoped>

</style>