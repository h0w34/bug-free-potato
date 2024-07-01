<template>
  <v-dialog
    v-model="addCadetDialog"
    max-width="650"
    min-wdth="500"
    max-height="auto"
    persistent
  >
    <v-card max-height="700px" class="rounded-xl my-4" color="grey-lighten-5">
        <v-card-title class="d-flex justify-space-between align-center mt-1">
            <div class="text-h5 font-weight-regular text-medium-emphasis p-0 ml-2">
              Добавить курсанта
            </div>
<!--            <div class="unselectable ml-2 text-h5 font-weight-medium text-medium-emphasis"  >
              Добавить курсанта
            </div>-->
          <v-btn icon="mdi-close" variant="text" @click="closeDialog"></v-btn>
        </v-card-title>


<!--        <div v-if="loading || !resourcesTree" class="mx-15 justify-content-around">
          <v-container >
            <v-skeleton-loader
              min-height="400"
              type="heading, divider, heading, heading, heading, divider, actions"
          />
          </v-container>
        </div>-->
        <div>
          <v-stepper
            v-model="step"
            show-actions
          >
            <v-stepper-header>
              <v-stepper-item
                title="Заполнить анкету"
                value="1"
                :complete="step>0"
              ></v-stepper-item>

              <v-divider></v-divider>

              <v-stepper-item
                title="Добавить данные"
                value="2"
                :complete="step>1"
              ></v-stepper-item>

              <v-divider></v-divider>

              <v-stepper-item
                :rules="[() => !this.error]"
                :subtitle= "this.error? 'Извините...' : ''"
                :title="this.error? 'Ошибка!' : 'Готово!'"
                value="3"
                :complete="step>2"
              ></v-stepper-item>

            </v-stepper-header>

            <v-stepper-window class="mb-0">
              <v-stepper-window-item value="1">
                <v-form ref="form">

                  <v-row class="justify-content-center mb-0 pb-0">
                    <v-col class="px-4 pb-0 mb-0" style="min-width: 500px;">
  <!--                      <div class="mb-3 text-h5 font-weight-medium text-medium-emphasis"  >
                          Новый курсант/слушатель
                        </div>-->

                        <div class="text-subtitle-1 text-medium-emphasis">
                          Имя
                        </div>

                        <v-text-field
                          aria-errormessage="false"
                          placeholder="Ваше имя"
                          density="compact"
                          variant="outlined"
                          class="rounded-xl"
                          v-model="name"
                          :rules="nameRules"
                        ></v-text-field>
                        <div class="text-subtitle-1 text-medium-emphasis">
                          Фамилия
                        </div>
                        <v-text-field
                          placeholder="Ваша фамилия"
                          density="compact"
                          variant="outlined"
                          class="rounded-xl"
                          v-model="surname"
                          :rules="surnameRules"
                        ></v-text-field>

                        <div class="text-subtitle-1 text-medium-emphasis">
                          Отчество
                        </div>
                        <v-text-field
                          placeholder="Ваше отчество"
                          density="compact"
                          variant="outlined"
                          class="rounded-xl"
                          v-model="patronymic"
                          :rules="patronymicRules"
                        ></v-text-field>

                        <div class="text-subtitle-1 text-medium-emphasis">
                          Пол
                        </div>
                        <v-radio-group
                            style="margin-left: -7px"
                            class=" text-light-emphasis"
                            v-model="radios"
                            inline
                        >
                          <v-radio value="M" class="mr-1">
                            <template v-slot:label>
                              <div>Мужской</div>
                            </template>
                          </v-radio>
                          <v-radio value="F">
                            <template v-slot:label>
                              <div>Женский</div>
                            </template>
                          </v-radio>
                        </v-radio-group>
                    </v-col>
                  </v-row>
                </v-form>

            </v-stepper-window-item>

            <v-stepper-window-item v-if="!loading || !resourcesTree"  value="2">
              <v-row class="justify-content-center">
                    <v-col class="px-4">
<!--                      <div class="mb-3 text-h5 font-weight-medium text-medium-emphasis"  >
                        Новый курсант/слушатель
                      </div>-->

                      <div class="text-subtitle-1 text-medium-emphasis">
                        Звание
                      </div>
                      <v-select
                        return-object
                        clearable
                        placeholder="Рядовой полиции"
                        density="compact"
                        :items="allowedRanks"
                        variant="outlined"
                        v-model="selectedRank"
                        item-title="name"
                      >
<!--                        <template v-slot:selection="{ item }">
                          {{ item.title }}
                        </template>-->
                        <template v-slot:item="{ props, item }">
                          <v-list-item
                            v-bind="props"
                            :disabled="item.raw.disabled"
                            :value="item"
                          />
                        </template>
                      </v-select>

                      <div class="text-subtitle-1 text-medium-emphasis">
                        Должность
                      </div>
                      <v-select
                        return-object
                        clearable
                        placeholder="Курсант"
                        density="compact"
                        :items="resourcesTree['university']?.['positions'] ?? []"
                        variant="outlined"
                        v-model="selectedPosition"
                        item-title="name"
                      ></v-select>

                      <div class="text-subtitle-1 text-medium-emphasis">
                          Положение
                        </div>
                      <div class="d-flex align-center justify-content-start gap-2">

                        <v-select
                          density="compact"
                          label="Факультет"
                          :items="facultySelectItems"
                          variant="outlined"
                          v-model="selectedFaculty"
                          item-title="name"
                          return-object
                          :disabled="!resourcesTree || resourcesTree['university']['locations'].length === 0"
                          @change="clearCourseAndGroup"
                        ></v-select>

                        <v-select
                          density="compact"
                          label="Курс"
                          :items="courseSelectItems"
                          variant="outlined"
                          item-title="name"
                          v-model="selectedCourse"
                          return-object
                          :disabled="!selectedFaculty || facultySelectItems.length===0"
                          @change="clearGroup"
                        ></v-select>

                        <v-select
                          density="compact"
                          label="Группа"
                          :items="groupSelectItems"
                          variant="outlined"
                          v-model="selectedGroup"
                          item-title="name"
                          return-object
                          :disabled="!selectedCourse || courseSelectItems.length===0 || groupSelectItems.length===0"
                        ></v-select>
                      </div>

                      <div class="text-subtitle-1 text-medium-emphasis">
                          Ячейки
                        </div>
                      <div class="d-flex align-center justify-content-start gap-2">
                        <v-select
                          return-object
                          density="compact"
                          v-model="selectedPMCell"
                          label="Макаров"
                          :items="pmCellSelectItems"
                          item-title="id"
                          :disabled="!selectedFaculty || pmCellSelectItems.length===0"
                          variant="outlined"
                        ></v-select>
                        <v-select
                          return-object
                          density="compact"
                          v-model="selectedAKCell"
                          label="Калашников"
                          :items="akCellSelectItems"
                          item-title="id"
                          :disabled="!selectedFaculty || akCellSelectItems.length===0"
                          variant="outlined"
                        ></v-select>
                      </div>
                    </v-col>
                  </v-row>
            </v-stepper-window-item>

            <v-stepper-window-item v-if="!loading || !resourcesTree" value="3">
              <v-container>
                <div v-if="error">
                  <div class="text-h8 font-weight-regular text-medium-emphasis text-center mb-2">
                    Ой! ＞︿＜<br>
                    Возникла ошибка при добавлении д/л.<br>
                    Перепроверьте данные или попробуйте позже.
                  </div>
                </div>
                <div v-else>
                  <div class="text-h8 font-weight-regular text-medium-emphasis text-center">

                    Все сделано!<br>
                    Не забудьте сохранить логин и пароль. <br>

                  </div>
                  <v-divider/>
                  <div  class=" d-flex justify-content-center ">
                    <CadetCard :cadet-data="createdCadet? createdCadet : null" :menu-disabled="true"/>
                  </div>
                  <v-divider/>
                  <div class="text-h8 font-weight-regular text-medium-emphasis text-center">
                    Логин: {{createdCadet['user']['username']}}<br>
                    Пароль: {{createdCadetPassword}}
                  </div>
                  </div>
              </v-container>
            </v-stepper-window-item>
          </v-stepper-window>

          <v-divider class="mt-0 mb-3"></v-divider>

          <v-stepper-actions>
            <template v-slot:prev>
              <v-btn
                color="primary"
                variant="text"
                @click="handlePrevClick"
                :disabled="step === 0 || step===2"
              >
                Назад
              </v-btn>
            </template>

            <template v-slot:next>
              <v-btn
                color="primary"
                variant="text"
                @click="handleNextClick"
                :disabled="nextStepDisabled"
              >
                {{ step === 0 ? 'Далее' : (step === 1 ? 'Сохранить' : (error? 'Понятно' : 'Отлично')) }}
              </v-btn>
            </template>
          </v-stepper-actions>


        </v-stepper>
      </div>

    </v-card>
  </v-dialog>
</template>

<script>


import {mapActions, mapState} from "vuex";
import CadetCard from "@/components/cadet/CadetCard";
import ResourcesService from "@/services/resources-data.service";

export default {
  name: 'EditDutyDialog',
  components: {CadetCard},
  props: {
/*    dialog: {
      type: Boolean,
      required: true
    }*/
  },
  data() {
    return {
      createdCadet: null,
      createdCadetPassword: null,

      name: null,
      surname: null,
      patronymic: null,
      radios: null,

      selectedFaculty: null,
      selectedCourse: null,
      selectedGroup: null,
      selectedPosition: null,
      selectedRank: null,
      selectedPMCell: null,
      selectedAKCell: null,

      RankItems: [],
      PositionItems: [],

      saving: false,
      error: false,
      loading: false,
      step: 0,

      nameRules: [
        value => {
          if (typeof value !== 'string') return 'Имя должно быть строкой'
          if (!/^[А-ЯЁ][а-яё]+$/.test(value)) return 'Имя должно начинаться с заглавной буквы и содержать только кириллицу'
          return true
        }
      ],
      surnameRules: [
        value => {
          if (typeof value !== 'string') return 'Фамилия должна быть строкой'
          if (!/^[А-ЯЁ][а-яё]+$/.test(value)) return 'Фамилия должна начинаться с заглавной буквы и содержать только кириллицу'
          return true
        }
      ],
      patronymicRules: [
        value => {
          if (typeof value !== 'string') return 'Отчество должно быть строкой'
          if (!/^[А-ЯЁ][а-яё]+$/.test(value)) return 'Отчество должно начинаться с заглавной буквы и содержать только кириллицу'
          return true
        }
      ]
    }
  },

  async beforeMount() {
      if(!this.resourcesTree) {
        await this.fetchResourcesTree()
      }
      this.loading = false;
  },

  computed: {
    ...mapState('layoutStore', ['addCadetDialog']),
    ...mapState('ResourcesStore', ['resourcesTree', 'selectedIds']),
    ...mapState('authStore', ['user']),

    allowedRanks(){
      if(this.resourcesTree['university']){
        return this.resourcesTree['university']['ranks'].map(rank => ({
          ...rank,
          disabled: this.user['cadet']['rank']['id'] < rank.id
        }))
      }
      else return []
    },

    /*stepperItems(){
      return [
        'Заполнить анкету',
        'Добавить данные',
        //'Привязать пользователя',
        this.error ? 'Ошибка!' : 'Готово!'
      ]
    },*/

    nextStepDisabled(){
      if (this.step===0 && (!this.radios || !this.name || !this.surname)){
        return true
      }
      else if (this.step===1 && (!this.selectedRank || !this.selectedPosition ||
          !this.selectedFaculty || !this.selectedCourse || !this.selectedGroup ||
          (this.selectedPMCell && this.pmCellSelectItems.length===0) ||
            (this.selectedAKCell && this.akCellSelectItems.length===0))){
        return true
      }
      else return false;
    },

    selectedLocation(){
      return this.getLocationForFaculty(this.selectedFaculty, this.resourcesTree)
    },

    facultySelectItems() {
      const faculties = [];
      for (const location of this.resourcesTree['university']['locations']) {
        faculties.push(...location.faculties)}
      return faculties;
    },

    courseSelectItems(){
      /*const location = this.resourcesTree['university']['locations'].find(
          loc => loc.id === this.selectedIds.locationId)*/
      /*const faculty = location['faculties'].find(fac => fac.id === this.selectedIds.facultyId)*/
      if (this.facultySelectItems){
        if (this.selectedFaculty){
          console.log('selected faculty is...', this.selectedFaculty)
          const faculty = this.facultySelectItems.find(fac => fac.id === this.selectedFaculty.id)
          if (faculty) return faculty.courses; else return []
        }
      }
      return [];
    },
    groupSelectItems(){
      /*const location = this.resourcesTree['university']['locations'].find(
          loc => loc.id === this.selectedIds.locationId)*/
      if (this.courseSelectItems){
        if (this.selectedCourse){
          const course = this.courseSelectItems.find(course => course.id === this.selectedCourse.id)
          if (course) return course.groups; else return []
        }
      }
      return [];
    },
    pmCellSelectItems(){
      if (this.selectedFaculty) {
        if (this.selectedLocation) {
          return this.selectedLocation.pm_cells
        }
      }
      return [];
    },
    akCellSelectItems(){
      if (this.selectedFaculty) {
        if (this.selectedLocation) {
          return this.selectedLocation.ak_cells
        }
      }
      return [];
    },

    /*currentSubTitle() {
      if (this.dutyData) {
        const date = new Date(this.dutyData['date']);
        const day = date.getDate();
        const month = date.getMonth();
        const address = this.dutyData['location']['address'];
        const infoString = `${day} ${this.monthNames[month]}, ${address}`
        return this.editeMode ? `Изменение суток на ${infoString}` : `Информация о сутках на ${infoString}`
      } else return '';
    },*/

  },
  methods: {
    ...mapActions('layoutStore', ['closeAddCadetDialog']),
    ...mapActions('ResourcesStore', ['fetchResourcesTree']),

    async handleNextClick(){
      switch (this.step){
        case 1: {
          console.log('here we are at the NEXTH CLICK!!!!!!')
          //start timer
          try {
            const response_data = await this.sendCadetData()
            this.createdCadet = await response_data.cadet
            this.createdCadetPassword = await response_data.password
            this.step++;
            break;
          } catch (error) {
            console.log(error)
            this.error = true;
            this.step++;
            break;
          }
        }
        case 2: {
          this.closeDialog();
          break;
        }
        default: this.step++;
      }
    },

    async sendCadetData(){
      console.log('trying to AWAIT!!!!')
      console.log('seleted ranka and position' ,this.selectedPosition.id, this.selectedRank.id, this.selectedGroup.id)
      return await ResourcesService.createCadet(
          {
            name: this.name,
            surname: this.surname,
            patronymic: this.patronymic,
            sex: this.radios,
            rank_id: this.selectedRank.id,
            position_id: this.selectedPosition.id,
            group_id: this.selectedGroup.id,
            pm_cell_id: this.selectedPMCell.id,
            ak_cell_id: this.selectedAKCell
          });
    },

    handlePrevClick(){
      this.step--;
    },

    clearCourseAndGroup() {
      this.selectedCourse = null;
      this.selectedGroup = null;
    },
    clearGroup() {
      this.selectedGroup = null;
    },

    getLocationForFaculty(faculty, resourcesTree) {
      return resourcesTree?.university?.locations?.find(loc => loc.id === faculty.location_id) || null;
    },


    closeDialog(){
      this.closeAddCadetDialog();
      this.resetDialogSate();
    },

    resetDialogSate(){
      this.createdCadet = null;
      this.createdCadetPassword = null;

      this.name = null;
      this.surname = null;
      this.patronymic = null;
      this.radios = null;

      this.selectedFaculty = null;
      this.selectedCourse = null;
      this.selectedGroup = null;
      this.selectedPosition = null;
      this.selectedRank = null;
      this.selectedPMCell = null;
      this.selectedAKCell = null;

      this.RankItems = [];
      this.PositionItems = [];

      this.error = false;
      this.loading = true;
      this.step = 0;
    }
    /*...mapActions('layoutStore', ['closeDutyDialog']),
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
    },*/
    /*closeDialog() {
      this.saving = false;
        if (this.editeMode) this.unlockDuty();
        this.clearDialogData()
        //layout action
        this.closeDutyDialog();
        /!*this.$emit('close');*!/
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
    }*/

  },

  watch: {

    /*dutyDialog:{
      handler(){
        // i.e. on the dialog opening
        if(this.dutyDialog){
          this.fetchDutyData();
        }
      },
      immediate: true
    },*/
  }
}
</script>