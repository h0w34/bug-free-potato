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
          <v-btn icon="mdi-close" variant="text" @click="closeAddCadetDialog"></v-btn>
        </v-card-title>

        <div v-if="loading" class="mx-15 justify-content-around">
          <v-container >
            <v-skeleton-loader
              min-height="600"
              type=" text, list-item, list-item, article, actions"
          />
          </v-container>
        </div>
        <div v-else>
          <v-stepper
            v-model="step"
            :items="stepperItems"
            show-actions
          >
            <template v-slot:[`item.1`]>
                  <v-row class="justify-content-center">
                    <v-col class="px-4" style="min-width: 500px;">
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
                        v-model="firstname"
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
                        :rules="nameRules"
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
                        :rules="nameRules"
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
                        <v-radio value="male" class="mr-1">
                          <template v-slot:label>
                            <div>Мужской</div>
                          </template>
                        </v-radio>
                        <v-radio value="female">
                          <template v-slot:label>
                            <div>Женский</div>
                          </template>
                        </v-radio>
                      </v-radio-group>
                    </v-col>
                  </v-row>
            </template>

            <template v-slot:[`item.2`]>
              <v-row class="justify-content-center">
                    <v-col class="px-4">
<!--                      <div class="mb-3 text-h5 font-weight-medium text-medium-emphasis"  >
                        Новый курсант/слушатель
                      </div>-->

                      <div class="text-subtitle-1 text-medium-emphasis">
                        Звание
                      </div>
                      <v-select
                        clearable
                        placeholder="Рядовой полиции"
                        density="compact"
                        :items="resourcesTree['university']?.['ranks'] ?? []"
                        variant="outlined"
                        v-model="selectedRank"
                        item-title="name"
                      ></v-select>

                      <div class="text-subtitle-1 text-medium-emphasis">
                        Должность
                      </div>
                      <v-select
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
                          :disabled="!selectedFaculty"
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
                          :disabled="!selectedCourse"
                        ></v-select>
                      </div>

                      <div class="text-subtitle-1 text-medium-emphasis">
                          Ячейки
                        </div>
                      <div class="d-flex align-center justify-content-start gap-2">
                        <v-select
                          density="compact"
                          label="Макаров"
                          :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
                          variant="outlined"
                        ></v-select>
                        <v-select
                          density="compact"
                          label="Калашников"
                          :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
                          variant="outlined"
                        ></v-select>
                      </div>
                    </v-col>
                  </v-row>
            </template>

            <template v-slot:[`item.3`]>
              <v-container class="text-center">
                <div class="text-h8 font-weight-regular text-medium-emphasis">
                  Все сделано!<br>
                  Не забудьте сохранить логин и пароль.
                </div>
                <v-divider/>
                <div  class=" d-flex justify-content-center ">
                  <CadetCard :cadet-data="null"/>
                </div>
              </v-container>
            </template>

            <template v-slot:actions>
              <v-divider class="mt-0 pt-0"/>
              <v-stepper-actions
                :disabled="disabled"
                @click:next="step++"
                @click:prev="step--"
             ></v-stepper-actions>
            </template>


        </v-stepper>
      </div>

    </v-card>
  </v-dialog>
</template>

<script>


import {mapState, mapActions} from "vuex";
import CadetCard from "@/components/cadet/CadetCard";

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
      name: null,
      surname: null,
      patronymic: null,
      radios: null,

      selectedFaculty: null,
      selectedCourse: null,
      selectedGroup: null,
      selectedPosition: null,
      selectedRank: null,

      RankItems: [],
      PositionItems: [],

      saving: false,
      error: false,
      loading: false,
      stepperItems: [
        'Заполнить анкету',
        'Добавить данные',
        //'Привязать пользователя',
        'Готово!',
      ],
      step: 1
    }
  },
  async beforeMount() {
      if(!this.resourcesTree){
        await this.fetchResourcesTree()
      }

  },

  computed: {
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

    disabled(){
      return false
    },

    ...mapState('layoutStore', ['addCadetDialog']),
    ...mapState('ResourcesStore', ['resourcesTree', 'selectedIds']),

    currentSubTitle() {
      if (this.dutyData) {
        const date = new Date(this.dutyData['date']);
        const day = date.getDate();
        const month = date.getMonth();
        const address = this.dutyData['location']['address'];
        const infoString = `${day} ${this.monthNames[month]}, ${address}`
        return this.editeMode ? `Изменение суток на ${infoString}` : `Информация о сутках на ${infoString}`
      } else return '';
    }
  },
  methods: {
    ...mapActions('layoutStore', ['closeAddCadetDialog']),
    ...mapActions('ResourcesStore', ['fetchResourcesTree']),

    clearCourseAndGroup() {
      this.selectedCourse = null;
      this.selectedGroup = null;
    },
    clearGroup() {
      this.selectedGroup = null;
    },
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