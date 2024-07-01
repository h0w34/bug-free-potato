<template>
  <v-dialog
    v-model="deleteCadetDialog"
    max-width="650"
    min-wdth="500"
    max-height="auto"
    persistent
  >

  </v-dialog>
</template>

<script>


import {mapState, mapActions} from "vuex";
import CadetCard from "@/components/cadet/CadetCard";
import ResourcesService from "@/services/resources-data.service";

export default {
  name: 'DeleteCadetDialog',
  components: {CadetCard},
  props: {
    cadetData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      loading: false,

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
    ...mapState('layoutStore', ['deleteCadetDialog']),
    ...mapState('ResourcesStore', ['resourcesTree', 'selectedIds']),
    ...mapState('authStore', ['user']),

    allowedRanks(){
      if(this.resourcesTree['university']){
          const ranks = this.resourcesTree['university']['ranks'].map(rank => ({
            ...rank,
            disabled: this.user['cadet']['rank']['id'] < rank.id
          }))
        console.log(ranks)
          return  ranks
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

    nextButtonText(){
      return false
    }
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
            console.log('trying to AWAIT!!!!')
            console.log('seleted ranka and position' ,this.selectedPosition.id, this.selectedRank.id, this.selectedGroup.id)
            const response_data = await ResourcesService.createCadet(
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