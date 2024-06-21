<template>
  <v-app>
    <v-main class="align-center align-content-center justify-content-center">
      <v-form ref="form">
        <v-row class="justify-content-center">
          <v-card
            class="rounded-5 px-5 py-4 mb-5 justify-content-center"
            height="468"
            min-height="400"
            min-width="460"
            max-width="480"
            :elevation="4"
          >
          <v-card-title class=" text-center text-emphasis-medium">
            <div class="text-h5 text-light-emphasis">Мои утки 🐣</div>
          </v-card-title>
          <v-container>
            <div class="mb-3 text-h5 font-weight-medium text-medium-emphasis"  >Вход по почте или нику</div>
            <div class="text-subtitle-1 text-medium-emphasis">
              Email/username

            </div>
            <v-text-field
              name="login"
              density="compact"
              variant="outlined"
              class="rounded-xl"
              v-model="login_input"
              :rules="usernameEmailRules"
              :counter="40"
            ></v-text-field>
            <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
              Пароль
              <a
                class="text-caption text-decoration-none text-blue"
                href="#"
                rel="noopener noreferrer"
                target="_blank"
              >
                Забыли пароль?
              </a>
            </div>
            <v-text-field
              :append-inner-icon="passwordVisible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="passwordVisible ? 'text' : 'password'"
              density="compact"
              variant="outlined"
              class="rounded-xl mb-3"
              v-model="password"
              :rules="passwordRules"
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
              @click.prevent="validateAndLogin"
            >
              Войти
            </v-btn>
          </v-container>
          <v-card-text class="text-center py-2 pb-2 text-medium-emphasis">
            Еще не с нами?
        <a
          class="text-blue text-decoration-none ml-2"
          href="/signup"
          rel="noopener noreferrer"
        >
          Зарегистрироваться <v-icon  icon="mdi-chevron-right"></v-icon>
        </a>
      </v-card-text>
          </v-card>
        </v-row>
      </v-form>

    </v-main>
  </v-app>
</template>


<script>
/*import AuthService from "@/services/auth.service";
import { mapActions } from 'vuex';
import store from '../store';*/


export default {
  data() {
    return {
      loading:false,
      password:"",
      passwordVisible: false,
      userLoggedIn: false,
      login_input:"",
      passwordRules: [
        value => {
          if (value?.length >= 8) return true
            return 'Пароль не может содержать менее 8 символов.'
        },
      ],
      usernameEmailRules: [
        v => !!v || 'Введите почту/юзернейм',
        v => {
          if (v.includes('@')) {
            return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(v) || 'Недопустимый email.';
          } else {
            if (v.length < 5) return 'Не менее 5 символов на юзернейм.'
            return /^[a-zA-Z0-9_]+$/.test(v) || 'Недопустимый юзернейм.';
          }
        },
      ]
    };
  },

  methods: {
    async validateAndLogin() {
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
          alert('Invalid username or password');
        }
      } catch (error) {
        alert('Invalid username or password');
      } finally {
        this.loading = false;
      }
    }
  }
    /*async validateAndLogin() {
      if (!this.$refs.form.validate()) {
        return;
      }
      await this.login();
    },*/
    /*async login() {
      this.loading = true;
      try {
        //await new Promise(resolve => setTimeout(resolve, 1000));
        const response = await AuthService.login(this.login_input, this.password);
        alert(JSON.stringify(response))
          localStorage.setItem('jwt_access', response['access_token']);
          localStorage.setItem('jwt_refresh', response['refresh_token']);
          this.userLoggedIn = true;
          this.loading = false;
      } catch (error) {
        alert('Invalid username or password');
        /!*alert('Не удалось войти');*!/
        this.loading = false;
      }
    },
  }*/
}

</script>

<style scoped>
  .unselectable {
    -webkit-user-select: none;
    -webkit-touch-callout: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
</style>


