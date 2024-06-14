  <template>
    <v-dialog
      v-model="localDialog"
      max-width="750px"
      max-height="auto"
    >
      <v-card max-height="700px" class="rounded-xl my-4" color="grey-lighten-5">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="d-flex align-center gap-3">
            <div class="text-h5 font-weight-regular text-medium-emphasis ps-3">Заменить курсанта</div>
            <v-chip
              color="secondary"
              variant="tonal"
              label
            >
              {{selectedCadetData['role']['name'] }}
            </v-chip>
          </div>
          <v-btn icon="mdi-close" variant="text" @click="closeDialog(false)"></v-btn>
        </v-card-title>

        <v-card-subtitle v-if="this.step!==1" class=" d-flex ma-0 justify-space-between align-center">
          <div class="text-light-emphasis px-3 py-1" >
            <h6>{{formSubTitle}}</h6>
          </div>
        </v-card-subtitle>

        <div v-if="loading" class="mx-15 justify-content-around">
          <v-container >
            <v-skeleton-loader
              type=" text, list-item, list-item, article, actions"
          />
          </v-container>

        </div>

        <div v-else>
          <v-stepper
            v-model="step"
            :items="items"
            show-actions
          >
           <template v-slot:prev="{on, attrs}">
              <v-btn
                color="primary"
                variant="text"
                v-bind="attrs"
                v-on="on"
                @click="handlePrevClick"
                :disabled="step === 3"
              >
                Назад
              </v-btn>
            </template>

            <template v-slot:next="{ on, attrs }">
              <v-btn
                color="primary"
                variant="text"
                v-bind="attrs"
                v-on="on"
                @click="handleNextClick"
                :disabled="step === 1 && !confirmedCadet || step===2 && selectedDocType in [1,2] && !startDate"
                :key="step === items.length - 1 ? 'confirm' : 'next'"
              >
               {{ confirmButtonLabel }}
              </v-btn>
            </template>

          <template v-slot:[`item.1`]>
          <div class="text-h6 text-medium-emphasis font-weight-regular">
            Из резерва:
          </div>

          <div v-if="reserveCadets.length === 0 || !reserveCadets" >
            <v-container class=" text-center">
              <div class="text-h8 font-weight-regular text-medium-emphasis">
                Ой! Для этого курсанта нет резервов.<br>
                Попросите администратора их добавить.
              </div>
            </v-container>
          </div>
          <div v-else>
            <v-container>
              <v-row class="justify-content-center">
                <v-col
                  v-for="(reserve_cadet_data, i) in reserveCadets"
                  :key="i"
                  cols="auto"
                  md="4"
                >
                  <cadet-card :cadet-data="reserve_cadet_data" @select="confirmCadet"/>
                </v-col>
              </v-row>
            </v-container>
          </div>


          <v-divider></v-divider>

          <div class="text-h6 text-medium-emphasis font-weight-regular">
            Свободные курсанты:
          </div>

          <div v-if="!suitableCadets || suitableCadets.length===0">
            <v-container class=" text-center">
              <div class="text-h8 font-weight-regular text-medium-emphasis">
                Для этого курсанта не нашлось подходящих замен.<br>
                Попросите администратора проверить, что там не так.
              </div>
            </v-container>
          </div>
        <div v-else>
          <v-container class="pa-2">
            <v-data-iterator
              :items="suitableCadets"
              :items-per-page="3"
              :search="search"
            >
              <template v-slot:header >
                <v-toolbar class="p-4 rounded" color="grey-lighten-5">
                  <v-text-field
                    v-model="search"
                    density="default"
                    placeholder="Имя/взвод/факультет"
                    prepend-inner-icon="mdi-magnify"
                    variant="solo"
                    clearable
                    hide-details
                  ></v-text-field>
                </v-toolbar>
              </template>


              <template v-slot:default="{ items }">
                <div v-if="suitableCadets">
                  <v-container class="py-3" fluid>
                    <v-row>
                      <v-col
                        v-for="item in items"
                        :key="item.id"
                        cols="auto"
                        md="4"
                      >
                      <cadet-card
                        :cadet-data="item.raw"
                        @select="confirmCadet"
                      />
                      </v-col>
                    </v-row>
                  </v-container>
                </div>
                <div v-else>
                  <v-container class="py-3">
                    <v-row>
                      <v-col
                        v-for="i in 3"
                        :key="i"
                        cols="auto"
                        md="4"
                      >
                        <v-skeleton-loader type="card" class="rounded"/>
                      </v-col>
                    </v-row>
                  </v-container>
                </div>
              </template>

              <template v-slot:footer="{ page, pageCount, prevPage, nextPage }">
                <v-divider />
                <div class="d-flex align-center justify-center " >
                  <v-btn
                    :disabled="page === 1"
                    density="comfortable"
                    icon="mdi-arrow-left"
                    variant="tonal"
                    rounded
                    @click="prevPage"
                  ></v-btn>

                  <div class="mx-2 ">
                    {{ page }} из {{ pageCount }}
                  </div>

                  <v-btn
                    :disabled="page >= pageCount"
                    density="comfortable"
                    icon="mdi-arrow-right"
                    variant="tonal"
                    rounded
                    @click="nextPage"
                  ></v-btn>
                </div>
              </template >

            </v-data-iterator >
          </v-container>
        </div>
        </template>

        <template v-slot:[`item.2`]>
          <v-container>
            <div class="d-flex text-light-emphasis justify-content-between">
              <v-select
              density="compact"
              v-model="selectedVariant"
              :items="['Болезнь', 'Рапорт', 'Иная причина']"
              variant="outlined"
              @input="handleVariantChange"
              class="w-25"
            ></v-select>

            <div v-if="selectedVariant==='Болезнь' || selectedVariant==='Рапорт'" class="d-flex justify-content-end gap-1">
              <div>

              </div>
              <VueDatePicker
                  v-model="startDate"
                  locale="ru"
                  :enable-time-picker="false"
                  placeholder="Начальная дата"
                  auto-apply
                  class="w-25"
                  style="min-width:155px"
                  :min-date="new Date(selectedDutyData['date'])"
                ></VueDatePicker>
              <div v-if="show_end_date">
                <VueDatePicker
                  v-model="endDate"
                  locale="ru"
                  :enable-time-picker="false"
                  placeholder="Конечная дата"
                  auto-apply
                  class="w-25"
                  style="min-width:155px"
                  :min-date="new Date().setDate(new Date(selectedDutyData['date']).getDate() + 1)"
                ></VueDatePicker>
              </div>
              <v-btn
                  @click="show_end_date = !show_end_date"
                  variant="outlined"
                  color="grey-lighten-1"
                  class="rounded-3"
                  >{{ show_end_date ? 'Скрыть' : 'По...' }}
              </v-btn>
            </div>

          </div>

            <!--v-date-picker
              v-model="date"
              range
              scrollable
              locale="ru-RU"
              first-day-of-week=1
            ></v-date-picker-->
            <v-textarea
                v-model="commentaryContents"
                label="Комментарий"
                placeholder="Распишите информацию, если нужно"
                variant="outlined"
                rows="10"
            >
            </v-textarea>
          </v-container>
        </template>

        <!--v-stepper-item
          :rules="[() => isUpdated]"
          subtitle="Сожалеем об этом"
          title="Ошибка при обновлении"
          value="2"
        >
          <v-container class="text-medium-emphasis text-center">
              <h5>Упс! Возникла ошибка во время </h5>
              <h5>обновления суток. Попробуйте попозже.</h5>
          </v-container>
        </v-stepper-item-->

        <template v-slot:[`item.3`]>
          <v-container class="text-medium-emphasis text-center">
            <div v-if="isUpdated">
              <h3>Все сделано!</h3>
              <h3>Уведомления придут в Telegram.</h3>
              <h5>(но не забудьте напомнить и лично)</h5>
            </div>
            <div v-else>
              <h5>Упс! Возникла ошибка во время </h5>
              <h5>обновления суток. Попробуйте позже.</h5>
            </div>
          </v-container>
        </template>
      </v-stepper>
      </div>

    </v-card>
  </v-dialog>
</template>


<script>
import CadetCard from "@/components/CadetCard";
import DutyDataService from "@/services/DutyDataService";
//import { ref } from 'vue';

export default {
  name: "EditRoleDialog",
  components: {CadetCard},
  props:{
    selectedCadetData:{
      type: Object,
      required: true
    },
    selectedDutyId:{
      type: Number,
      required: true
    },
    selectedDutyData:{
      type: Object,
      required: true
    },
    dialog:{
      type: Boolean,
      required: true
    }
  },
  data() {
    return{
      search: '',
      loading: false,
      suitableCadets: [],
      reserveCadets: [],
      //isConfirmed: false,
      step: 1,
      confirmedCadet: null,
      isUpdated: false,

      startDate: new Date(),
      endDate: null,
      show_end_date: false,

      items: [
        'Выбрать замену',
        'Указать причину',
        'Готово!',
      ],
      selectedVariant: 'Болезнь',
      commentaryContents: ''
      //this.selectedDocType = ???
    }
  },
  mounted() {
    /*this.startDate = Date.now()
    this.endDate = this.startDate + 7;*/
    //this.dp = this.$refs.dp;
    // await this.fetchSuitableCadets(this.selectedCadetData['role']['id']);
  },
  methods: {
    handleNextClick() {
      switch(this.step){
        /*case 1: {
          this.step++;
          break;
        }*/
        case 2:{
          //confirm('Вы уверены?')
          this.updateDuty()
          setTimeout(()=>this.step++, 800)
          //this.updateDutyLayout();
          //this.step++;
          break;
        }
        case 3: {
          this.closeDialog()
          break;
        }
        default: this.step++;
      }
    },
    handlePrevClick() {
      if (this.step === 1) {
        // Perform the action here
        //this.confirmAction();
        this.closeDialog()
      } else if (this.step === 2){
        this.confirmedCadet = null
        this.step--;
      }
      else {
        this.step--;
      }
    },
    confirmAction() {
      if (confirm('Are you sure you want to perform this action?')) {
        setTimeout(()=>{}, 1000)
      }
    },

    handleVariantChange(variant) {
      if (variant === 'Болезнь') {
        this.diseaseDescription = '';
      } else if (variant === 'Рапорт') {
        this.reportDescription = '';
      } else if (variant === 'Иная причина') {
        this.otherReasonDescription = '';
      }
    },
    confirmCadet (cadetData) {
      this.confirmedCadet = cadetData;
      //this.isConfirmed = true;
      this.step++;
    },
    closeDialog() {
      this.$emit('update', this.isUpdated)
      this.clearDialogData();
      this.$emit('close');
    },
    clearDialogData(){
      this.step = 1; // Reset step to 1 when dialog is closed
      this.isUpdated = false;
      this.confirmedCadet=null;
      this.commentaryContents = '';
      this.startDate = new Date()
      this.endDate = null
      this.selectedVariant = 'Болезнь'
      /*this.suitableCadets=[]
      this.reserveCadets=[]*/
    },

    async fetchReservesAndSuitableCadets() {
      try {
        console.log('FETCHING SUITABLES IN EDITrOLEdIaLOG')
        console.log('for duty id:', this.selectedDutyId)
        console.log('and the role', this.selectedCadetData['role']['id'])
        console.log('and the cadet id:', this.selectedCadetData['cadet']['id'])

        const params = new URLSearchParams();
        params.append('role_id', this.selectedCadetData['role']['id']);

        const response = await DutyDataService.getSuitableReserves(this.selectedDutyId, this.selectedCadetData['role']['id'])
        this.suitableCadets = await response['suitable_cadets']
        this.reserveCadets = await response['reserves']
        console.log('SUITABLES: ', await response)
        //this.suitableCadets = await response
      } catch (error) {
        console.error(error);
      } finally {
        console.log('Disabling loading...')
        this.loading = false;
        console.log('Complete loading!')
    }
  },
    async updateDuty() {
      try {
        // console.log(JSON.stringify(this.selectedCadetData['cadet']['id']))
        // console.log(JSON.stringify(this.confirmedCadet['id']))
        console.log(this.startDate, this.endDate)
        if (this.selectedDocType === 1 || this.selectedDocType === 2) {
          let startDate =  this.startDate ? this.startDate.toISOString().slice(0, 10) : ''  // Convert to ISO 8601 format or use default date
          //let endDate = this.endDate && this.show_end_date? this.endDate.toISOString().slice(0, 10) : ''
          let replacementDoc = {  // Variable declaration
            'start_date': startDate,
            //'end_date': endDate
          }
          if (this.endDate && this.show_end_date){
            replacementDoc['end_date'] = this.endDate.toISOString().slice(0, 10)
          }
          replacementDoc['contents'] = this.commentaryContents ||
              (this.selectedDocType===2? 'Рапорт на спание. Освобожмдён от трудовой деятелбности.' :
                  'Очемнь при очемнб болен. Лежатб до новаво гомда.')

          await DutyDataService.updateDuty(this.selectedDutyId, this.selectedCadetData['cadet']['id'],
              this.confirmedCadet['id'], null, replacementDoc)
        } else if (this.selectedDocType === 3) {
          let commentary = this.commentaryContents
          await DutyDataService.updateDuty(this.selectedDutyId, this.selectedCadetData['cadet']['id'],
              this.confirmedCadet['id'], commentary, null)
        }
        this.isUpdated = true;
      } catch (error) {
        console.error('Error:', error);
      }
    }
  },
  computed:{
    datepicker1State(){
      return this.startDate
    },
    datepicker2State(){
      return !this.endDate && this.show_end_date ? true: null
    },
    formSubTitle(){
      switch (this.step){
        case 1: return "Позиция –– " + this.selectedCadetData['role']['name'];
        case 2: return this.selectedCadetData['cadet']['surname'] + ' (' + this.selectedCadetData['cadet']['group'] +
             ')' + ' ⟶ ' +  this.confirmedCadet['surname'] + ' (' + this.confirmedCadet['group'] + ')'
        case 3: {
          if (this.isUpdated){
            return this.selectedCadetData['cadet']['surname'] + ' (' + this.selectedCadetData['cadet']['group'] +
             ')' + ' ⟶ ' +  this.confirmedCadet['surname'] + ' (' + this.confirmedCadet['group'] + ')' + '✅☑'
          }
          else {
            return this.selectedCadetData['cadet']['surname'] + ' (' + this.selectedCadetData['cadet']['group'] +
             ')' + ' ⟶ ' +  this.confirmedCadet['surname'] + ' (' + this.confirmedCadet['group'] + ')' + '❌⚠'
          }
        }
        default: return "Замена курсанта"
      }
    },
    localDialog: {
      get() {
        return this.dialog;
      },
      set(value) {
        this.$emit('update:dialog', value);
      }
    },
    confirmButtonLabel() {
      return this.step === 1 ? 'Дальше' : this.step === 2 ? 'Подтвердить' : (this.isUpdated ? 'Отлично!' : 'Понятно');
    },
    // TODO: actually fetch the docTypes and display them
    selectedDocType(){
      return this.selectedVariant === 'Болезнь' ? 1 : this.selectedVariant === 'Рапорт' ? 2 : 3    }
  },
  watch: {
    selectedCadetData: {
      async handler() {
        if(this.selectedCadetData['role']){
          console.log('Selected Cadet data in the Dialog:')
          console.log(this.selectedCadetData)
          await this.fetchReservesAndSuitableCadets(this.selectedCadetData['role']['id']);
        }
        else{
          console.log('UUUUHHHH((((')
        }
      },
      immediate: true
    },
    // TODO: reserves are updated only when another cadet is chosen
    // to update them each time the dialog opens consider using the dialog prop handler
    // instead of the selectedCadetData one and clearing arrays with reserves in clearDialogData

    /*dialog: {
        async handler() {
          if (this.dialog === true){
            if(this.selectedCadetData['role']){
              console.log('Selected Cadet data in the Dialog:')
              console.log(this.selectedCadetData)
              await this.fetchReservesAndSuitableCadets(this.selectedCadetData['role']['id']);
            }
            else{
              console.log('UUUUHHHH((((')
            }
          }
        }
    }*/
  }
}
</script>

<style scoped>
  .dp__theme_light {
    --dp-border-radius: 12px;
    --dp-cell-border-radius: 20%;
  }
  .custom-select {
      cursor: pointer;
      color: darkcyan;
      margin: 0;
      display: inline-block;
    }
</style>
