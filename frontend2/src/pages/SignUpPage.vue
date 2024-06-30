<template>
  <v-app>
    <v-main class="align-center align-content-center justify-content-center">
      <v-form @submit.prevent ref="form">
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

<!--            <div class="text-subtitle-1 text-medium-emphasis">
              Юзернейм
            </div>
            <v-text-field
              placeholder="beanpotato33"
              density="compact"
              variant="outlined"
              class="rounded-xl"
              v-model="firstname"
              :rules="nameRules"
            ></v-text-field>-->
            <div class="text-subtitle-1 text-medium-emphasis">
              Почта
            </div>
            <v-text-field
              density="compact"
              variant="outlined"
              class="rounded-xl"
              v-model="email"
              :rules="emailRules"
              :counter="40"
            ></v-text-field>

            <div class="text-subtitle-1 text-medium-emphasis">
              Пароль
            </div>
            <v-text-field
              :append-inner-icon="passwordVisible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="passwordVisible ? 'text' : 'password'"
              density="compact"
              variant="outlined"
              class="rounded-xl"
              v-model="password"
              :rules="password1Rules"
              clearable
              @click:append-inner="passwordVisible = !passwordVisible"
            ></v-text-field>

            <div class="text-subtitle-1 text-medium-emphasis">
              Повторите пароль еще раз
            </div>
            <v-text-field
              :append-inner-icon="passwordVisible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="passwordVisible ? 'text' : 'password'"
              density="compact"
              variant="outlined"
              class="rounded-xl mb-3"
              v-model="password2"
              :rules="password2Rules"
              clearable
              @click:append-inner="passwordVisible = !passwordVisible"
            ></v-text-field>

            <v-btn
              type="submit"
              :loading="loading"
              class="mb-2"
              variant="flat"
              color="grey-darken-2"
              min-height="50"
              width="100%"
              density="default"
              @click.prevent="validateAndSignIn"
            >
              Поехали!
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
      passwordVisible: false,
      loading: false,

      password:'',
      password2:'',
      email:'',
      signupFailure: false,

      password1Rules: [
        value => {
          if (value?.length >= 8) return true
            return 'Пароль не может содержать менее 8 символов'
        },
        () => {
          if (this.password !== this.password2) return 'Пароли не совпадают'
          else return true
        }
      ],
      password2Rules: [
        () => {
          if (this.password !== this.password2) return 'Пароли не совпадают'
          else return true
        }
      ],
      emailRules: [
        v => !!v || 'Введите вашу почту',
        v => {
          return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(v) || 'Недопустимый email';
        },
        () => this.signupFailure ? 'Эта почта уже кем-то используется' : true
      ]
    };

  },
  methods: {
    async validateAndSignIn(){
      this.loginFailure = false;
      const loadingStartTime = performance.now();

      if (!this.$refs.form.validate()) {
        return;
      }
      try {
        this.loading = true;
        const response = await this.$store.dispatch('authStore/login', {
          login_input: this.login_input,
          password: this.password,
        });
        if (response) {
          // Handle the response
          // For example, you can redirect to a protected route
          this.$nextTick(() => {
            this.$router.push(this.returnUrl || '/');
          });
        } else {
          await new Promise(resolve => setTimeout(resolve, Math.max(800 - (performance.now() - loadingStartTime), 0)));
          this.loginFailure = true;
          alert('Invalid username or password');
        }
      } catch (error) {
        this.loginFailure = true;
        await new Promise(resolve => setTimeout(resolve, Math.max(800 - (performance.now() - loadingStartTime), 0)));
        this.loginFailure = true;
        /*if (error.response.message === 'login_error'){

        } else if (error.response.message === 'password_error')*/
        /*alert('Invalid username or password');*/
      } finally {
        this.loading = false;
      }
    },
    changeStep(){
      this.$emit("nextStep", "signinfr");
  }
}
};

</script>

<style scoped>

</style>


