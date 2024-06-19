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
                :dialog="roleDialog" @close="closeRoleDialog" @update="updateLayout" :selectedDutyData="dutyData"/>

    <v-card class="rounded-xl my-4"
      :disabled="saving"
      :loading="saving"
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
            :disabled="saving"
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
      <v-alert
            v-if="beingEdited"
            closable
            type="warning"
            variant="tonal"
            class="mx-5 text-center"
          >
            <v-alert-title>Ошибка</v-alert-title>
            <h5>Эти сутки сейчас кто-то редактирует.</h5>
            <h5>Возвращайтесь попозже.</h5>
      </v-alert>
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
              <role-card :cadet-data="cadet_data" :disabled="beingEdited" @edit="openRoleDialog"/>
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
          <v-btn v-if="!error && !beingEdited" class="text-none"
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
import RoleCard from "@/components/cadet/RoleCard";
import EditRoleDialog from "@/components/schedule/EditRoleDialog";
import MoveCadetsDialog from "@/components/MoveCadetsDialog";
import ReplacementsHistoryDialog from "@/components/schedule/ReplacementsHistoryDialog";
import DutyDataService from "@/services/duty-data.service";
//import EditRoleDialog from "@/components/EditRoleDialog";


export default {
  name: 'DutyInfoDialog',
  components: {ReplacementsHistoryDialog, MoveCadetsDialog, EditRoleDialog, RoleCard},
  props: {
    /*headers: {
      type: Array,
      required: true
    },*/
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
      //localSelectedDuty: this.selectedDuty,
      dutyData: null,
      saving: false,
      error: false,
      beingEdited: false,
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
      this.beingEdited=false
      this.saving = false
      this.roleDialog = false
      this.movingDialog = false
      this.replacementHistoryDialog = false
    },
    async updateLayout(isUpdated){
      if(isUpdated){
        this.saving = true;
        const loadingStartTime = performance.now();
        await this.fetchDutyData();
        // Set a minimum delay of 500ms before setting loading to false
        await new Promise(resolve => setTimeout(resolve, Math.max(800 - (performance.now() - loadingStartTime), 0)));
        this.saving = false;
      }
    },
    closeDialog() {
      this.saving = false;
      this.clearDialogData()
      this.unlockDuty();
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
      this.saving = true;

      // TODO: some hard logic to update the schedule table layout
      setTimeout(() => {
        this.$emit('save');
        this.saving = false;
        this.unlockDuty();
      }, 1000);
    },

    async fetchDutyData() {
      if (this.selectedDutyId) {
        try {
          const response = await DutyDataService.getDutyById(this.selectedDutyId);
          console.log('response code when fetching a duty: ', response.status)
          this.dutyData = response
        } catch (error) {
           if (error.response && error.response.status === 423) {
            this.beingEdited = true;
            this.dutyData = error.response.data
          } else {
            this.error = true;
          }
          console.error(error.response.status);

        }
      }
    },
    async unlockDuty(){
      if(this.selectedDutyId){
        try {
          await DutyDataService.unlockDutyById(this.selectedDutyId)
        } catch (error) {
          // TODO
        }
      }
    }
  },
  watch: {
    selectedDutyId: {
      handler(){
        this.dutyData = null;
        console.log('selectedDutyId:', JSON.stringify(this.selectedDutyId ))
        this.fetchDutyData();
      } ,
      immediate: true
    }
  }
}
</script>