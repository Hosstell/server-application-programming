<template>
  <v-layout align-center justify-center>
    <v-spacer/>
    <v-flex xs12 sm8 md4>
      <v-form ref="form" v-model="valid" @submit.prevent="submit">
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Вход</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>

            <v-text-field
              label="Email*"
              v-model="email"
              required
              :rules="[required, emailRul]"
              autocomplete="off"
            />

            <v-text-field
              id="password"
              v-model="password"
              name="password"
              label="Пароль"
              :rules="[required]"
              type="password"
              autocomplete="off"
            />

          </v-card-text>
          <v-card-actions>
            <v-btn text outlined to="/registration">Регистрация </v-btn>
            <v-spacer></v-spacer>
            <v-btn text outlined color="green" :disabled="!valid" @click="login">Войти</v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-flex>
    <v-spacer/>
  </v-layout>
</template>

<script>
  import gql from 'graphql-tag'

  import DatePicker from "../components/common/DatePicker";
  export default {
    name: "login",
    layout: "login",
    components: {DatePicker},
    data() {
      return {
        email: null,
        password: null,
        valid: false,
        required: value => !!value || 'Поле не может быть пустым',
        emailRul: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Неверный формат email'
        }

      }
    },
    methods: {
      login() {
        this.$apollo.mutate({
          mutation: gql`
          mutation ($email: String!, $password: String!) {
            login(email: $email, password: $password) {
              success
            }
          }`,
          variables: {
            email: this.email,
            password: this.password,
          }
        }).then(data => {
          let success =data.data.login.success

          if (success) {
            this.$router.push({ path: '/my_pictures' })
          } else {
            console.log(this)
            this.$notify({
              type: 'error',
              group: 'dataValid',
              title: 'Ошибка авторизации',
              text: 'Проверьте  введенный email и пароль.',
              duration: 2000,
            });

          }
        })
      }
    }
  }
</script>

<style scoped>

</style>
