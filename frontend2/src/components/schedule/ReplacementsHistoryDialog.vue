<template>
  <v-card
    class="rounded-xl pb-2"
    color="grey-lighten-5"
  >
      <v-card-title class="d-flex justify-space-between align-center">
        <div class="text-h5 text-medium-emphasis ps-3">
          История замен
        </div>
        <div>
        <v-btn icon="mdi-close" variant="text" @click="closeDialog"/>
        </div>
      </v-card-title>

      <v-divider class="mx-8 my-0"></v-divider>
      <v-card-text>
        <v-container class="text-medium-emphasis text-center pb-0">
          <div v-if="error">
              <!--h5>Ой! Возникла ошибка во время <br>
              загрузки замен. Попробуйте позже.</h5-->
              <h5>В этих сутках еще не было замен. <br>
              Чтобы начать, выберите одного из везунчиков.</h5>
          </div>
          <div v-else-if="loading">
            <v-list v-for="index in 2" :key="index">
              <v-skeleton-loader type="paragraph" />
              <v-divider/>
            </v-list>
          </div>
          <div v-else>
              <v-expansion-panels
                v-for="(replacement, i) in replacementsData"
                :key="i"
              >
                <v-expansion-panel class="rounded-3 mb-3">
                  <v-expansion-panel-title>
                    <v-container class="pa-0 d-flex justify-content-between align-center">
                      <div> {{ formPanelTitle(replacement) }}</div>
                      <div class="d-inline-flex align-center">
                        <div>
                          {{formatDate(replacement['date'])}}
                        </div>
                        <v-chip
                          color="secondary"
                          variant="tonal"
                          label
                          class="mx-2"
                        >
                          {{replacement['duty_role']['name'] }}
                        </v-chip>
                      </div>
                    </v-container>
                  </v-expansion-panel-title>

                  <v-expansion-panel-text>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
          </div>
        </v-container>

          <!--v-expansion-panels class="mb-6">
            <v-expansion-panel
              v-for="i in 3"
              :key="i"
            >
              <v-expansion-panel-title expand-icon="mdi-menu-down">
                Item
              </v-expansion-panel-title>
              <v-expansion-panel-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-title collapse-icon="mdi-minus" expand-icon="mdi-plus">
                Item
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
              </v-expansion-panel-text>
            </v-expansion-panel>

            <v-expansion-panel>
              <v-expansion-panel-title>
                Item
                <template v-slot:actions="{ expanded }">
                  <v-icon :color="!expanded ? 'teal' : ''" :icon="expanded ? 'mdi-pencil' : 'mdi-check'"></v-icon>
                </template>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
              </v-expansion-panel-text>
            </v-expansion-panel>

            <v-expansion-panel>
              <v-expansion-panel-title disable-icon-rotate>
                Item
                <template v-slot:actions>
                  <v-icon color="error" icon="mdi-alert-circle">
                  </v-icon>
                </template>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels-->
      </v-card-text>
      <v-divider class="mx-8 mt-0 mb-4"/>
  </v-card>

</template>

<script>
import moment from 'moment';
import DutyDataService from "@/services/DutyDataService";
moment.locale('ru');
moment.updateLocale('ru', {
  weekdaysShort: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
});


export default {
  name: "ReplacementsHistoryDialog",
  props:{
    selectedDutyId:{
      type: Object,
      required: true
    }
  },
  data(){
    return {
      replacementsData: null,
      error: false,
      loading: true
    }
  },
  methods:{
    formPanelTitle(replacementData){
      return replacementData['replaced_cadet']['surname'] +
          ' (' + replacementData['replaced_cadet']['group'] + ')' +
          ' ⟶ ' +  replacementData['replacing_cadet']['surname']
          + ' (' + replacementData['replacing_cadet']['group'] + ')'
    },
    formatDate(dateString){
      return moment(dateString).format('ddd, D MMM YYYY HH:mm');
    },
    closeDialog(){
      //this.clearDialogData()
      this.$emit('close')
    },
    async fetchReplacements(){
      try {
          this.replacementsData = await DutyDataService.getReplacements(this.selectedDutyId);
        } catch (error) {
          this.error = true;
          console.error(error);
        }
    },
    initDialogData(){
      this.error = false;
      this.loading = true;
      this.replacementsData = null;
    }

  },
  async mounted() {
    await this.fetchReplacements();
  },
  watch:{
    selectedDutyId: {
      async handler(){
        if(this.selectedDutyId){
          this.initDialogData()
          await this.fetchReplacements();
          console.log('replacements data: ', JSON.stringify(this.replacementsData))
          this.loading = false
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>

</style>