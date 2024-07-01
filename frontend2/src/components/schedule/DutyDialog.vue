<template>
  <v-dialog
    v-model="dutyDialog"
    max-width="850"
    max-height="auto"
    persistent
  >

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

<!--
      <v-card-title
          class="d-flex justify-space-between align-center mt-2 pb-0"
      >
        <div class="text-h5 text-medium-emphasis ps-3">
          {{ currentTitle }}
        </div>
        <div>

          <v-btn
            variant="flat"
            base-color="grey-lighten-4"
            class="text-none text-center font-weight-light text-medium-emphasis rounded mr-1"
            @click="openHistoryDialog"

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

      <div class=" pb-0 mt-1 pr-15 d-flex justify-space-between">
        <div class="pl-8" style="opacity: 0.5">
          <v-chip
              variant="outlined"
              label
              color="secondary"
              class="text-center align-center mr-0">
            <h6 class="m-0 p-0 font-weight-regular">{{ currentDayMonth }}</h6>
          </v-chip>
          <v-chip
              label
              variant="text"
              class="text-center align-center">
            <h6 class="m-0 p-0 font-weight-regular">{{dutyData?.location.address}}</h6>
          </v-chip>


&lt;!&ndash;          <h5 class="font-weight-light mt-0 pt-0">{{currentSubTitle}}</h5>&ndash;&gt;
        </div>

        <v-btn
            width="170"
            variant="flat"
            base-color="grey-lighten-4"
            class="text-none text-center font-weight-light text-medium-emphasis rounded mr-2"
            @click="toggleEditeMode"
            :disabled="!dutyData || beingEdited"
          >
              Редактировать
              <v-icon
                  class="text-medium-emphasis ml-2"
                  size="large"
              >
              mdi-pencil
            </v-icon>
          </v-btn>
      </div>
-->

      <v-card-title
          class="d-flex justify-space-between align-center mt-2 pb-0"
      >
        <div class="text-h5 text-medium-emphasis ps-3">
          {{ currentTitle }}
        </div>
        <div>
          <v-btn
            width="170"
            variant="flat"
            base-color="grey-lighten-4"
            class="text-none text-center font-weight-light text-medium-emphasis rounded mr-2"
            @click="toggleEditeMode"
            :disabled="!dutyData || beingEdited"
          >
              Редактировать
              <v-icon
                  class="text-medium-emphasis ml-2"
                  size="large"
              >
              mdi-pencil
            </v-icon>
          </v-btn>
          <v-btn
            variant="flat"
            base-color="grey-lighten-4"
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

      <v-card-subtitle class=" pb-0 mt-1">
        <div class="text-medium-emphasis ps-3">
          <v-chip
              variant="outlined"
              label
              color="secondary"
              class="text-center align-center mr-0">
            <h6 class="m-0 p-0 font-weight-regular">{{ currentDayMonth }}</h6>
          </v-chip>
          <v-chip
              label
              variant="text"
              class="text-center align-center">
            <h6 class="m-0 p-0 font-weight-regular">{{dutyData?.location.address}}</h6>
          </v-chip>


<!--          <h5 class="font-weight-light mt-0 pt-0">{{currentSubTitle}}</h5>-->
        </div>
      </v-card-subtitle>

      <v-divider class="mx-3"></v-divider>
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
            <v-row justify="space-evenly">
              <v-col
                v-for="(cadet_data, i) in dutyData['cadets_with_roles']"
                :key="i"
                cols="4"
              >
              <role-card
                  :cadet-data="cadet_data"
                  :disabled="beingEdited"
                  @edit="openRoleDialog"
                  :edite-mode="editeMode"
                  @closeDutyDialog="closeDialog"
              />
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
      <v-divider class="mx-3 my-2"></v-divider>
      <v-card-actions class="mx-3 pr-5">
        <v-spacer></v-spacer>
        <div class="my-2">
          <v-btn
            class="text-none px-3"
            color="medium-emphasis"
            variant="outlined"
            @click="closeDialog"
          >
            {{error ? 'Отмена' : 'Выйти'}}
          </v-btn>
          <v-btn v-if="!error && !beingEdited && editeMode" class="text-none"
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
import {mapState, mapActions} from "vuex";

export default {
  name: 'EditDutyDialog',
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
    },

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
      editeMode: false,
      selectedCadetData: {},

        monthNames: [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ]

    }
  },
  computed: {
    ...mapState('layoutStore', ['dutyDialog']),

    localDialog: {
      get() {
        return this.dialog;
      },
      set(value) {
        this.$emit('update:dialog', value);
      }
    },
    currentTitle () {
      return this.editeMode ? 'Редактировать сутки' : 'Информация о сутках'
    },
    currentSubTitle() {
      if (this.dutyData) {
        const date = new Date(this.dutyData['date']);
        const day = date.getDate();
        const month = date.getMonth();
        const address = this.dutyData['location']['address'];
        const infoString = `${day} ${this.monthNames[month]}, ${address}`
        return this.editeMode ? /*`Изменение суток на */`${infoString}` : `${infoString}`
      } else return '';
    },
    currentDayMonth(){
      if(this.dutyData){
        const date = new Date(this.dutyData['date']);
        const day = date.getDate();
        const month = date.getMonth();
        return `${day} ${this.monthNames[month]}`
      } else return ''
    }
  },
  methods: {
    ...mapActions('layoutStore', ['closeDutyDialog']),
    ...mapActions('layoutStore', ['openDutyDialog']),

    toggleEditeMode(){
      if (this.editeMode){
        this.saving = true;
        setTimeout(()=>this.saving = false, 700)
        this.editeMode = false;
        this.unlockDuty();
      }
      else {
        this.saving = true;
        setTimeout(()=>this.saving = false, 700)
        this.editeMode = true; // now cards will show the 'edite' buttons
        this.lockDuty();
      }

    },
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
      this.editeMode = false
      this.dutyData = null
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
      if (this.editeMode) this.unlockDuty();
      this.clearDialogData()
      //layout action
      this.closeDutyDialog();
      /*this.$emit('close');*/
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
    async saveAndShowLoader() {
      this.saving = true;
      const loadingStartTime = performance.now();

      // TODO: some hard logic to update the schedule table layout

      this.$emit('save');
      await this.unlockDuty();
      await new Promise(resolve => setTimeout(resolve, Math.max(1000 - (performance.now() - loadingStartTime), 0)));
      this.saving = false;
      this.closeDialog()
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
          await DutyDataService.actionOnDutyById(this.selectedDutyId, 'unlock')
        } catch (error) {
          // TODO
          console.log('ERROR UNLOCKING DUTY')
          this.error=true;
        }
      }
    },
    async lockDuty(){
      if(this.selectedDutyId){
        try {
          await DutyDataService.actionOnDutyById(this.selectedDutyId, 'lock')
        } catch (error) {
          console.log('ERROR LOCKING DUTY')
          // TODO
          this.error=true;
        }
      }
    }

  },
  watch: {
    dutyDialog:{
      handler(){
        // i.e. on the dialog opening
        if(this.dutyDialog){
          this.fetchDutyData();
        }
      },
      immediate: true
    },
    /*selectedDutyId: {
      handler(){

        console.log('selectedDutyId:', JSON.stringify(this.selectedDutyId ))
/!*        if (this.editeMode){
          this.lockDuty()
        }*!/
        this.fetchDutyData();
      } ,
      immediate: true
    }*/
  }
}
</script>