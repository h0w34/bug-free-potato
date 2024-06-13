<template>
  <v-dialog v-model="localDialog" max-width="800" max-height="auto" persistent>

    <v-dialog v-model="movingDialog">
        <move-cadets-dialog/>
    </v-dialog>

    <v-dialog max-width="700" max-height="auto" v-model="replacementHistoryDialog">
      <replacements-history-dialog
          @close="closeHistoryDialog"
          :selectedDutyId="selectedDutyId"
          :selectedDuty="selectedDuty"
      />
    </v-dialog>

    <edit-role-dialog :selected-cadet-data="selectedCadetData" :selectedDutyId="selectedDutyId"
                      :dialog="roleDialog" @close="closeRoleDialog" @update="updateLayout"/>

    <v-card class="rounded-xl my-4"
      :disabled="loading"
      :loading="loading"
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
        <div>
          <v-btn
            variant="tonal"
            class="text-none text-center font-weight-light text-medium-emphasis rounded mr-1"
            @click="openHistoryDialog"
            :disabled="loading"
          >
              История замен
              <v-icon
                  class="text-medium-emphasis ml-2"
                  size="large"
                >
                mdi-history
            </v-icon>
          </v-btn>

          <v-btn icon="mdi-close" variant="text" @click="closeDialog"/>
        </div>
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
            <v-container class="text-medium-emphasis text-center">
                <h5>Упс! Не удалось загрузить сутки.</h5>
                <h5>Перезагрузите страницу.</h5>
              </v-container>
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
          >
            {{error ? 'Отмена' : 'Выйти'}}
          </v-btn>
          <v-btn v-if="!error" class="text-none"
            color="medium-emphasis"
            variant="outlined"
            @click="saveAndShowLoader"
          >Сохранить
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import RoleCard from "@/components/RoleCard";
import EditRoleDialog from "@/components/EditRoleDialog";
import MoveCadetsDialog from "@/components/MoveCadetsDialog";
import ReplacementsHistoryDialog from "@/components/ReplacementsHistoryDialog";
import DutyDataService from "@/services/DutyDataService";
//import EditRoleDialog from "@/components/EditRoleDialog";


export default {
  name: 'EditDutyDialog',
  components: {ReplacementsHistoryDialog, MoveCadetsDialog, EditRoleDialog, RoleCard},
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
      loading: false,
      error: false,

      roleDialog: false,
      movingDialog: false,
      replacementHistoryDialog: false,

      selectedCadetData: {},

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
    clearDialogData(){
      this.error = false
      this.loading = false
      this.dutyData = false
      this.roleDialog = false
      this.movingDialog=  false
      this.replacementHistoryDialog = false
    },
    async updateLayout(isUpdated){
      if(isUpdated){
        this.loading = true;
        this.loadingStartTime = performance.now();
        await this.fetchDutyData();
        // Set a minimum delay of 500ms before setting loading to false
        await new Promise(resolve => setTimeout(resolve, Math.max(800 - (performance.now() - this.loadingStartTime), 0)));
        this.loading = false;
      }
    },
    closeDialog() {
      this.loading = false;
      this.$emit('close');
    },
    closeRoleDialog(){
      this.roleDialog = false
    },
    openRoleDialog(cadet_data){
        console.log('SELECTED CADET DATA:')
        console.log(cadet_data)
        this.selectedCadetData = cadet_data;
        this.roleDialog = true;
    },
    openHistoryDialog(){
      this.replacementHistoryDialog = true;
    },
    closeHistoryDialog(){
      this.replacementHistoryDialog = false;
    },
    saveAndShowLoader() {
      this.loading = true;
      setTimeout(() => {
        this.$emit('save');
        this.loading = false;
      }, 1000);
    },
    async fetchDutyData() {
      if (this.selectedDutyId) {
        try {
          this.dutyData = await DutyDataService.getDutyById(this.selectedDutyId);
        } catch (error) {
          this.error = true;
          console.error(error);
        }
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