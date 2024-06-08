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
           <template v-slot:prev="{ on, attrs}">
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
                :disabled="step === 1 && !confirmedCadet"
                :key="step === items.length - 1 ? 'confirm' : 'next'"
              >
               {{ step === 1 ? 'Дальше' : step === 2 ? 'Подтвердить' : 'Отлично!' }}
              </v-btn>
            </template>

          <template v-slot:[`item.1`]>

          <div class="text-h6 text-medium-emphasis font-weight-regular">
            Из резерва:
          </div>

          <div v-if="selectedCadetData['reserve'].length === 0 || selectedCadetData['reserve'] === undefined" >
            <v-container class=" text-center">
              <div class="text-h8 font-weight-regular text-medium-emphasis">
                Ой! Для этого курсанта нет резервов.<br>
                Попросите администратора их добавить.
              </div>
            </v-container>
          </div>
          <div v-else>
            <v-container>
              <v-row>
                <v-col
                  v-for="(reserve_cadet_data, i) in selectedCadetData['reserve']"
                  :key="i"
                  cols="12"
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
            <v-combobox
              v-model="selectedVariant"
              :items="['Болезнь', 'Рапорт', 'Иная причина']"
              variant="outlined"
              @input="handleVariantChange"
            ></v-combobox>

            <v-text-field
              v-if="selectedVariant === 'Болезнь'"
              v-model="diseaseDescription"
              placeholder="Описание болезни"
              variant="outlined"
            ></v-text-field>

            <v-text-field
              v-if="selectedVariant === 'Рапорт'"
              v-model="reportDescription"
              placeholder="Описание рапорта"
              variant="outlined"
            ></v-text-field>
            <v-textarea label="Label" variant="solo-filled"></v-textarea>
            <v-text-field
              v-if="selectedVariant === 'Иная причина'"
              v-model="otherReasonDescription"
              placeholder="Описание иной причины"
              variant="outlined"
            ></v-text-field>

          </v-container>



        </template>

        <template v-slot:[`item.3`]>
          <v-container class="text-medium-emphasis text-center">
            <h3>Все сделано!</h3>
            <h3>Уведомления придут в Telegram.</h3>
            <h5>(но не забудьте напомнить и лично)</h5>
          </v-container>
        </template>
      </v-stepper>

      </div>

    </v-card>
  </v-dialog>
</template>

<script>

import CadetCard from "@/components/CadetCard";

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
    dialog:{
      type: Boolean,
      required: true
    }
  },
  data() {
    return{
      search: '',
      loading: 0,
      suitableCadets: null,
      isConfirmed: false,
      shipping: 0,
      step: 1,
      confirmedCadet: null,
      isUpdated: false,
      items: [
        'Выбрать замену',
        'Указать причину',
        'Готово!',
      ],
      selectedVariant: '',
      diseaseDescription: '',
      reportDescription: '',
      otherReasonDescription: '',
    }
  },
  async mounted() {
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
      } else {
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
      this.isConfirmed = true;
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
        this.confirmedCadet=null
    },

    async fetchSuitableCadets() {
  try {
    console.log('FETCHING SUITABLES IN EDITrOLEdIaLOG')
    console.log('for duty id:', this.selectedDutyId)
    console.log('and the role', this.selectedCadetData['role']['id'])
    console.log('and the cadet id:', this.selectedCadetData['cadet']['id'])

    const params = new URLSearchParams();
    params.append('role_id', this.selectedCadetData['role']['id']);

    const response = await fetch(
      `http://localhost:8080/api/duties/${this.selectedDutyId}/reserves?${params.toString()}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error status: ${response.status}`);
    }
    this.suitableCadets = await response.json();
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
        const response = await fetch(`http://localhost:8080/api/duties/${this.selectedDutyId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'replaced_id': this.selectedCadetData['cadet']['id'],
            'replacing_id': this.confirmedCadet['id'],
            'reason': {
              'type': 'sick',
              'start_date': '2024-04-03',
              'end_date': '2024-04-13'
            }
          })
        });
        //confirm('Ответ сервера:' + response.json());
        if (!response.ok) {
          throw new Error(`Error updating duty: ${response.status} - ${response.statusText}`);
        }
          //this.$emit('update', 1);
          this.isUpdated=true;
      } catch (error) {
        console.error('Error:', error);
      }
    },

  },
  computed:{
    formSubTitle(){
      switch (this.step){
        case 1: return "Позиция –– " + this.selectedCadetData['role']['name'];
        case 2: return this.selectedCadetData['cadet']['surname'] + ' (' + this.selectedCadetData['cadet']['group'] +
             ')' + ' ⟶ ' +  this.confirmedCadet['surname'] + ' (' + this.confirmedCadet['group'] + ')'
        case 3: return null
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
  },
  watch: {
    selectedCadetData: {
      async handler() {
        if(this.selectedCadetData['role']){
          console.log('Selected Cadet data in the Dialog:')
          console.log(this.selectedCadetData)
          await this.fetchSuitableCadets(this.selectedCadetData['role']['id']);
        }
        else{
          console.log('UUUUHHHH((((')
        }
      },
      immediate: true
    },
  }

}
</script>

<style scoped>

</style>
