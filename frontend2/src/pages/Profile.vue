<template>
  <v-container flex class="py-5 d-flex  justify-space-between">
    <!-- v-skeleton-loader type="paragraph@3"/-->
    <v-card
      variant="flat"
      max-width="450"
      height="100%"
    >
      <v-card-title class="px-2 pb-0">
        <div class="text-h5">
          Статистика 📈
        </div>
      </v-card-title>
      <v-container
          class="rounded-xl  align-center px-1"
          min-width="500"
          min-height="400"
      >
            <v-row>
              <v-col>
                <div
                  style="border: 3px solid #eaebf1;"
                  class="rounded-xl pa-3 pb-2 d-flex align-center gap-2"
                >
                  <h3>🗓️️</h3>
                  <h5 class="align-self-center">Суток за месяц:</h5>
                  <h3 class="mr-2">3</h3>
                </div>
              </v-col>
              <v-col>
                <div
                      style="border: 3px solid #eaebf1; max-width: 100%"
                      class="rounded-xl pa-3 d-flex pb-2 align-center gap-2 justify-space-between"
                  >
                    <h3>🗓️️</h3>
                    <h5 class="align-self-center">Суток за год:</h5>
                    <h3 class="mr-2">15</h3>
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="7">
                <div
                      style="border: 3px solid #eaebf1; max-width: 100%"
                      class="rounded-xl pa-3 d-flex pb-2 align-center gap-2 justify-space-between"
                  >
                    <h3>🗓️️</h3>
                    <h5 class="align-self-center">Праздников и выходных:</h5>
                    <h3 class="mr-2">15</h3>
                </div>
              </v-col>
              <v-col cols="6">
                <div
                      style="border: 3px solid #eaebf1; max-width: 100%"
                      class="rounded-xl pa-3 d-flex pb-2 align-center gap-2 justify-space-between"
                  >
                    <h3>🗓️️</h3>
                    <h5 class="align-self-center">Суток за год:</h5>
                    <h3 class="mr-2">15</h3>
                </div>
              </v-col>
            </v-row>
        </v-container>
      <v-skeleton-loader type="paragraph@3"/>
    </v-card>

    <v-card class="py-3 rounded-xl "  height="100%" >
      <div class="text-center px-5 ">
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
          <div class="text-medium-emphasis">
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
                <div class="text-medium-emphasis">

                </div>
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
    <!--v-skeleton-loader type="paragraph@3"/-->
    <v-card>
      <v-card-title>Ближайшие сутки</v-card-title>
      <v-card-title>Мои резервы</v-card-title>
    </v-card>
  </v-container>
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
export default {
  name: "ProfilePage"
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
