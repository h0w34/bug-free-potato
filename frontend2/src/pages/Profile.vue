<template>
  <EditDutyDialog
      :dialog="dutyDialog"
      :selected-duty="selectedDuty"
      :selected-duty-id="selectedDuty['id']"
      @close="closeDutyDialogLocal()"
  />
  <div class="d-flex justify-content-center p-5">
    <!-- v-skeleton-loader type="paragraph@3"/-->
    <v-row class="justify-content-center gap-lg-3">
      <v-col cols="auto">
          <div v-if="error">
            <v-container class="text-medium-emphasis text-center">
                <h5>Упс! Не удалось статистику!.</h5>
                <h5>Скорее всего у этого юзера нету <br>
                  привязанного курсанта.</h5>
              </v-container>
          </div>
          <v-skeleton-loader
            v-else
            :loading="loading"
            width="470"
            type="article@4"
          >
            <v-card class="mb-2 rounded-xl py-5 px-4 pt-2"
              min-height="400"
              max-width="480"
              :elevation="2"
            >
              <div class="text-h5 mt-2">
                Статистика 📈
              </div>
            <v-divider/>
              <h4 class="m-1 mb-3 text-light-emphasis">За месяц:</h4>
                <v-row>
                  <v-col cols="auto">
                    <stats-chip
                      emoji="🗓️️"
                      text="Суток за месяц"
                      :num="cadetStatistics['stats']['current_month']['duties_count']"
                    />
                  </v-col>
                  <v-col cols="auto">
                    <stats-chip
                      emoji="💤"
                      text="Суток на сб/вс"
                      :num="cadetStatistics['stats']['current_month']['weekend_duties_count']"
                    />
                  </v-col>
                </v-row>
                <v-row class="mb-2">
                  <v-col cols="auto">
                    <stats-chip
                      emoji="💫️"
                      text="Заменил"
                      :num="cadetStatistics['stats']['current_month']['replaced_count']"
                    />
                  </v-col>
                  <v-col cols="auto">
                    <stats-chip
                      emoji="💀"
                      text="Заменён"
                      :num="cadetStatistics['stats']['current_month']['was_replaced_count']"
                    />
                  </v-col>
                </v-row>
              <h4 class="m-1 mb-3 text-light-emphasis">За текущий год:</h4>
                <v-row>
                  <v-col cols="auto">
                    <stats-chip
                      emoji="🗓"
                      text="Суток за год"
                      :num="cadetStatistics['stats']['current_year']['duties_count']"
                    />
                  </v-col>
                  <v-col cols="auto">
                    <stats-chip
                      emoji="🛏️️"
                      text="Суток на сб/вс"
                      :num="cadetStatistics['stats']['current_year']['weekend_duties_count']"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="auto">
                    <stats-chip
                      emoji="🪃️"
                      text="Заменил"
                      :num="cadetStatistics['stats']['current_year']['replaced_count']"
                    />
                  </v-col>
                  <v-col cols="auto">
                    <stats-chip
                      emoji="🪦"
                      text="Заменён"
                      :num="cadetStatistics['stats']['current_year']['was_replaced_count']"
                    />
                  </v-col>
                </v-row>
              </v-card>
          </v-skeleton-loader>
        <!--v-skeleton-loader type="paragraph@3"/-->
      </v-col>

      <v-col cols="auto">
        <v-skeleton-loader
          :loading="loading"
          height="500"
          width="350"
          type="card, paragraph, paragraph"
        >
          <v-card class="py-3 rounded-xl"
            min-width="330"
            :elevation="2"
          >
            <div class="text-center px-4">
              <v-avatar
                class="ma-3"
                size="150"
              >
<!--                <v-img
                  alt="doggy"
                  :src="require('../../public/default_avatar.gif')"
                ></v-img>-->
<!--                <v-img
                  alt="doggy"
                  :src="require('../../public/default_avatar.gif')"
                ></v-img>-->
                <v-img
                  alt="doggy"
                  :src="getUserAvatarUrl(userData['user']['username']/*['avatar']['url']*/)"
                ></v-img>
              </v-avatar>
              <v-card-title class="px-0">
                <div>
                <h3 class="mb-0">
                  {{user['cadet']['name'] + ' ' + user['cadet']['surname']}}
                </h3>
                <div class="text-medium-emphasis" @click="navigateToUserPage">
                 {{'@'+username}}
                </div>
              </div>
              </v-card-title>
            </div>
            <v-divider class="mx-10 my-2"/>
            <div class="px-3 mx-0">
                <div>
                  <v-list class="d-flex justify-content-start">
                    <v-list-item>
                      <h6 class="mb-1"
                      >{{ '🎖️ '+ user['cadet']['rank']['name']+' полиции' }}</h6>
                      <h6 class="mb-1">{{'🫂 '+ user['cadet']['group']['name'] +' взвод'}}</h6>
                      <h6 class="mb-1">{{'⚓ '+ user['cadet']['course']['name'] +'-й курс'}}</h6>
                      <h6 class="mb-3">{{ '👨‍💻 ' + user['cadet']['faculty']['name'] }}</h6>
                      <div class="gap-1 d-flex">
                        <div><v-chip color="danger">старожил</v-chip></div>
                        <div><v-chip color="secondary">пожилой</v-chip></div>
                      </div>
                    </v-list-item>
                  </v-list>
                </div>
              </div>
          </v-card>

<!--          <CadetCard :cadet-data="user['cadet']"/>-->
        </v-skeleton-loader>

      </v-col>

      <v-col cols="auto">
        <v-skeleton-loader
          :loading="loading"
          width="470"
          type="paragraph@8"
        >
          <v-card
            class="rounded-xl px-3 py-0"
            width="490"
            :elevation="2"
          >
            <div class="p-3">
              <span class="text-h5">Ближайшие сутки</span>
              <v-divider/>
              <div v-if="cadetStatistics['future_duties'].length > 0">
                <v-expansion-panels
                    v-for="(dutyData, i) in cadetStatistics['future_duties']"
                    :key="i"
                    :readonly="true"
                  >
                    <v-expansion-panel class="rounded-3 mb-3"
                      @click="openDutyDialogLocal(dutyData)"
                    >
                      <v-expansion-panel-title class="pl-5 pr-4" disable-icon-rotate>
                        <template v-slot:actions>
                          <!--v-icon
                              color="grey"
                              icon="mdi-information"
                              class="mx-0 px-0"
                          >
                          </v-icon-->
                        </template>
                        <v-container class="pa-0 d-flex justify-content-between align-center">
                          <div class="d-flex text-truncate align-center">
                            <v-chip
                              color="secondary"
                              variant="outlined"
                                label
                              density="compact"
                              class="d-flex mr-2 py-3 justify-content-start"
                            >
                              <div class="mr-2 text-h6 font-weight-light">{{formattedDate(dutyData['duty']['date'])['day']}}</div>
                              <div >{{ formattedDate(dutyData['duty']['date'])['month']}}</div>
                            </v-chip>

                            <div class="ml-1 mr-2"> | </div>
                            <div>{{ dutyData['duty']['location']['name']}}</div>
                          </div>
                          <div class="d-flex align-center">
                            <v-chip
                              color="secondary"
                              variant="tonal"
                              label
                              class="mx-2 d-flex justify-content-center"
                              style="min-width: 100px"
                            >
                              {{ dutyData['role']['name'] }}
                            </v-chip>
                          </div>
                        </v-container>
                      </v-expansion-panel-title>

                    </v-expansion-panel>
                  </v-expansion-panels>
              </div>
              <v-container v-else fluid class="font-weight-regular text-light-emphasis text-center mb-4 p-4">
                Поздравляем! У этого везунчика <br/>
                нет запланированных суток.
              </v-container>

              <v-divider/>

              <span class="text-h5">Текущие резервы</span>
              <v-divider/>
              <div v-if="cadetStatistics['future_reserves'].length > 0">
                <v-expansion-panels
                    v-for="(reserveData, i) in cadetStatistics['future_reserves']"
                    :key="i"
                  >
                    <v-expansion-panel class="rounded-3 mb-3">
                      <v-expansion-panel-title class="pl-5">
                        <v-container class="pa-0 d-flex justify-content-between align-center">
                          <div class="d-flex text-truncate align-center">
                            <v-chip
                              color="secondary"
                              variant="outlined"
                                label
                              density="compact"
                              class="d-flex mr-2 py-3 justify-content-start"
                            >
                              <div class="mr-2 text-h6 font-weight-light">{{formattedDate(reserveData['duty']['date'])['day']}}</div>
                              <div >{{ formattedDate(reserveData['duty']['date'])['month']}}</div>
                            </v-chip>

                            <div class="ml-1 mr-2"> | </div>
                            <div>{{ reserveData['duty']['location']['name']}}</div>
                          </div>
                          <div class="d-flex align-center">
                            <v-chip
                              color="secondary"
                              variant="tonal"
                              label
                              class="mx-2 d-flex justify-content-center"
                              style="min-width: 100px"
                            >
                              {{ reserveData['role']['name'] }}
                            </v-chip>
                          </div>
                        </v-container>
                      </v-expansion-panel-title>

                      <v-expansion-panel-text>
                        <CadetCardSmall
                          :cadet-data="reserveData['backed_up_cadet']"
                        />

                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
              </div>
              <v-container v-else-if="cadetStatistics['future_duties'].length === 0" fluid class="font-weight-regular text-light-emphasis text-center mb-4 p-4">
                Замечательно! Этот курсант <br/>
                не состоит в резервах в том числе.
              </v-container>
              <v-container v-else fluid class="font-weight-regular text-light-emphasis text-center mb-4 p-4">
                У этого курсанта <br/>
                нет запланированных замен.
              </v-container>
            </div>
          </v-card>
        </v-skeleton-loader>
      </v-col>
      <!--v-skeleton-loader type="paragraph@3"/-->

    </v-row>
  </div>
  <!--div class="container">
    <div class="profile-card">
      <div class="profile-card__avatar">
        <img src="`" alt="User Avatar" />
      </div>
      <div class="profile-card__description">
        <h2>John Doe</h2>
        <p>Software Engineer</p>
        <p>john.doe@example.com</p>
        <p>123-456-7890</p>
      </div>
    </div>
  </div-->
</template>

<script>
/*import router from "@/router";*/
import UserDataService from "@/services/user-data.service";
import ResourcesService from "@/services/resources-data.service";
import StatsChip from "@/components/user/StatsChip";
import dateToString from "@/utils/date_utils";
import CadetCardSmall from "@/components/cadet/CadetCardSmall";
import EditDutyDialog from "@/components/schedule/DutyDialog";
import StaticDataService from "@/services/static-data.service";
import {mapActions} from "vuex";
/*import CadetCard from "@/components/cadet/CadetCard";*/

export default {
  name: "ProfilePage",
  components: {/*CadetCard,*/ EditDutyDialog, CadetCardSmall, StatsChip},
  data(){
    return {
      dutyDialog: false,
      selectedDuty: {},
      error: false,
      userData: null,
      cadetStatistics: null,
      loading: true
    }
  },
  props: {
      username: {
          type: String,
          required: true
      }
    },

    methods: {
      ...mapActions('layoutStore', ['openDutyDialog']),
      ...mapActions('layoutStore', ['closeDutyDialog']),

      getUserAvatarUrl(username) {
        return StaticDataService.getUserAvatarUrl(username);
      },
      openDutyDialogLocal(dutyData){
        this.selectedDuty = dutyData['duty'];
        this.openDutyDialog()
        this.dutyDialog = true;
      },
      closeDutyDialogLocal(){
        console.log('closing dialog in profile..')
        this.dutyDialog = false;
        this.closeDutyDialog()
        this.selectedDuty = {};
      },
      formattedDate(date) {
        return dateToString(new Date(date));
      },
      navigateToUserPage() {
        this.loading
        this.$router.push({ name: 'home', params: { username: 'johndoe' } });
        this.closeDutyDialog()
      },
      async fetchUserData() {
        if (this.username) {
          try {
            this.userData = await UserDataService.getUserByUsername(this.username)
            //this.loading = false
          } catch (error) {
             this.error = true;
          }
        }
      },
      async fetchCadetStatistics() {
          if (this.userData) {
            try {
              this.cadetStatistics = await ResourcesService.getCadetStatistics(this.userData['cadet']['id'])
            } catch (error) {
               this.error = true;
            }
          }
      }
    },
    computed:{
      user(){
        return this.userData ? this.userData : {}
      }
    },
    watch: {
      username: {
        async handler(){
          this.loading = true;
          await this.fetchUserData()
          await this.fetchCadetStatistics()
          this.loading = false
          console.log('selectedDutyId:', JSON.stringify(this.selectedDutyId ))
        } ,
        immediate: true
      }
    }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f7f7f7;
}

.profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-card__avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 20px;
}

.profile-card__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-card__description {
  text-align: center;
}

.profile-card__description h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.profile-card__description p {
  font-size: 16px;
  margin-bottom: 10px;
}


</style>
