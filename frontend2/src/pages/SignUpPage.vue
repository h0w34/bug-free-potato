<template>
  <v-app>
    <v-main class="align-center align-content-center justify-content-center">
      <v-form @submit.prevent>
        <v-row class="justify-content-center">
          <v-card
            class="rounded-5 px-5 py-4"
            min-height="400"
            min-width="460"
            max-width="480"
            :elevation="4"
          >
          <v-card-title class=" text-center text-emphasis-medium">
            <div class="text-h5 text-light-emphasis">Мои утки 🐣</div>
          </v-card-title>
          <v-container>
            <div class="mb-3 text-h5 font-weight-medium text-medium-emphasis"  >Зарегистрироваться</div>

            <div class="text-subtitle-1 text-medium-emphasis">
              Юзернейм
            </div>
            <v-text-field
              placeholder="beanpotato33"
              density="compact"
              variant="outlined"
              class="rounded-xl"
              v-model="firstname"
              :rules="nameRules"
            ></v-text-field>
            <div class="text-subtitle-1 text-medium-emphasis">
              Почта
            </div>
            <v-text-field
              placeholder="Ваша почта"
              density="compact"
              variant="outlined"
              class="rounded-xl"
              v-model="firstname"
              :rules="nameRules"
            ></v-text-field>

            <div class="text-subtitle-1 text-medium-emphasis">
              Пароль
            </div>
            <v-text-field
              :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible ? 'text' : 'password'"
              density="compact"
              variant="outlined"
              class="rounded-xl"
              v-model="firstname"
              :counter="10"
              :rules="passwordRules"
              clearable
              @click:append-inner="visible = !visible"
            ></v-text-field>

            <div class="text-subtitle-1 text-medium-emphasis">
              Повторите пароль еще раз
            </div>
            <v-text-field
              :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible ? 'text' : 'password'"
              density="compact"
              variant="outlined"
              class="rounded-xl mb-3"
              v-model="firstname"
              :counter="10"
              :rules="passwordRules"
              clearable
              @click:append-inner="visible = !visible"
            ></v-text-field>

            <v-btn
              class="mb-2"
              variant="flat"
              color="grey-darken-2"
              min-height="50"
              width="100%"
              density="default"
            >
              Войти
            </v-btn>
          </v-container>
          <v-card-text class="text-center py-1 text-medium-emphasis">
            Уже есть аккаунт?
        <a
          class="text-blue text-decoration-none ml-2"
          href="/login"
          rel="noopener noreferrer"
        >
          Войти <v-icon  icon="mdi-chevron-right"></v-icon>
        </a>
      </v-card-text>
          </v-card>
        </v-row>
      </v-form>

    </v-main>
  </v-app>
</template>



<script>
export default {
  data() {
    return {
      password:"",
      userLoggedIn: false,
      username:""
    };

  },
  method: {
changeStep(){
  this.$emit("nextStep", "signinfr");
}
}
};

</script>

<style scoped>

</style>


