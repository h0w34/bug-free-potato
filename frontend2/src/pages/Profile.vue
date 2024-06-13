<template>
  <div class="d-flex justify-content-center p-5">
    <!-- v-skeleton-loader type="paragraph@3"/-->
    <v-row class="justify-content-center gap-3">
      <v-col cols="auto" >
          <v-card class="mb-2 rounded-xl py-5 px-4 pt-2"
            min-width="500"
            min-height="400"
            max-width="470"
          >
            <div class="text-h5 mt-2">
              Статистика 📈
            </div>
          <v-divider/>
            <h4 class="m-1 mb-3 text-light-emphasis">За месяц:</h4>
              <v-row>
                <v-col cols="6">
                  <div
                    style="border: 3px solid #eaebf1"
                    class="rounded-xl pa-3 pb-2 text-truncate gap-2 align-center text-wrap d-flex"
                  >
                    <h4>🗓️️</h4>
                    <h5 style="font-size: 1.2rem" class="align-self-center">Суток за месяц:</h5>
                    <h3 class="mr-2 align-self-center">3</h3>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div
                        style="border: 3px solid #eaebf1;"
                        class="rounded-xl pa-3 pb-2 text-truncate gap-2 align-center text-wrap d-flex"
                    >
                      <h4>💤️</h4>
                      <h5 style="font-size: 1.2rem" class="align-self-center">Суток на сб/вс:</h5>
                      <h4 class="mr-2 align-self-center">15</h4>
                  </div>
                </v-col>
              </v-row>
              <v-row class="mb-2">
                <v-col cols="6">
                  <div
                        style="border: 3px solid #eaebf1; "
                        class="rounded-xl pa-3 pb-2 text-truncate gap-2 align-center text-wrap d-flex"

                    >
                      <h4>💫️</h4>
                      <h5  style="font-size: 1.2rem" class="align-self-center">Заменил:</h5>
                      <h4 class="mr-2">15</h4>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div
                        style="border: 3px solid #eaebf1; "
                        class="rounded-xl pa-3 pb-2 text-truncate gap-2 align-center text-wrap d-flex"
                    >
                      <h4>💀️</h4>
                      <h5 style="font-size: 1.2rem" class="align-self-center">Заменён:</h5>
                      <h4 class="mr-2">15</h4>
                  </div>
                </v-col>
              </v-row>


            <h4 class="m-1 mb-3 text-light-emphasis">За текущий год:</h4>
              <v-row>
                <v-col cols="6">
                  <div
                    style="border: 3px solid #eaebf1"
                    class="rounded-xl pa-3 pb-2 text-truncate gap-2 align-center text-wrap d-flex"
                  >
                    <h4>🗓️️</h4>
                    <h5 style="font-size: 1.2rem" class="align-self-center">Суток в 2024:</h5>
                    <h4 class="mr-2">3</h4>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div
                        style="border: 3px solid #eaebf1;"
                        class="rounded-xl pa-3 pb-2 text-truncate gap-2 align-center text-wrap d-flex"
                    >
                      <h4>🛏️️</h4>
                      <h5 style="font-size: 1.2rem" class="align-self-center">Суток на сб/вс:</h5>
                      <h4 class="mr-2">15</h4>
                  </div>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <div
                        style="border: 3px solid #eaebf1; "
                        class="rounded-xl pa-3 pb-2 text-truncate gap-2 align-center text-wrap d-flex"
                    >
                      <h4>🪃</h4>
                      <h5 style="font-size: 1.2rem" class="align-self-center">Заменил:</h5>
                      <h4 class="mr-2">15</h4>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div
                        style="border: 3px solid #eaebf1;"
                        class="rounded-xl pa-3 pb-2 text-truncate gap-2 align-center text-wrap d-flex"
                    >
                      <h4>⚰</h4>
                      <h5 style="font-size: 1.2rem" class="align-self-center">Заменён:</h5>
                      <h4 class="mr-2">15</h4>
                  </div>
                </v-col>
              </v-row>
            </v-card>

        <!--v-skeleton-loader type="paragraph@3"/-->
      </v-col>
      <v-col cols="auto">
        <v-card class="py-3 rounded-xl" >
          <div class="text-center px-5">
            <v-avatar
              class="ma-3"
              size="150"
            >
              <v-img
                alt="doggy"
                src="https://i.ytimg.com/vi/4tlzDBFEg8c/maxresdefault.jpg"
              ></v-img>
            </v-avatar>
            <v-card-title>
              <div>
              <h2 class="mb-0">Иван Иванов</h2>
              <div class="text-medium-emphasis" @click="navigateToUserPage">
               @somenickname
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
                    >🎖️ Рядовой полиции</h6>
                    <h6 class="mb-1">🫂 913 взвод</h6>
                    <h6 class="mb-3">👨‍💻 ФПСОИБ</h6>

                    <div class="gap-1 d-flex">
                      <div><v-chip color="danger">старожил</v-chip></div>
                      <div><v-chip color="secondary">пожилой</v-chip></div>
                    </div>
                  </v-list-item>
                </v-list>
              </div>
            </div>
        </v-card>
      </v-col>

      <v-col cols="auto">
        <v-card
        class="rounded-xl px-3 py-0"
        min-width="500"
        >
        <div class="p-3">
          <span class="text-h5">Ближайшие сутки</span>
          <v-divider/>
          <v-expansion-panels
                v-for="i in 3"
                :key="i"
              >
                <v-expansion-panel class="rounded-3 mb-3">
                  <v-expansion-panel-title>
                    <v-container class="pa-0 d-flex justify-content-between align-center">

                      <div class="d-flex text-truncate">
                        <div>05 Мая, </div>
                        <div>Волгина 12</div>
                      </div>
                      <div class="d-flex align-center">

                        <v-chip
                          color="secondary"
                          variant="tonal"
                          label
                          class="mx-2"
                        >
                          Помдеж
                        </v-chip>
                      </div>
                    </v-container>
                  </v-expansion-panel-title>

                  <v-expansion-panel-text>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
          <v-divider/>
          <span class="text-h5">Текущие замены</span>
          <v-divider/>
          <v-expansion-panels
                v-for="i in 3"
                :key="i"
              >
                <v-expansion-panel class="rounded-3 mb-3">
                  <v-expansion-panel-title>
                    <v-container class="pa-0 d-flex justify-content-between align-center">

                      <div class="d-flex ">
                        <div>05 Мая, </div>
                        <div>Волгина 12</div>
                      </div>
                      <div class="d-flex align-center">

                        <v-chip
                          color="secondary"
                          variant="tonal"
                          label
                          class="mx-2"
                        >
                          Помдеж
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
      </v-card>
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
import router from "@/routers";

export default {
  name: "ProfilePage",
  props: {
        username: {
            type: String,
            required: true
        }
    },

    methods: {
      navigateToUserPage() {
         router.push({ name: 'not', params: { username: 'johndoe' } });
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
