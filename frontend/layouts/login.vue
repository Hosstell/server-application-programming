<template>
  <v-content>
    <notifications group="dataValid" position="top center" width="300px"/>
    <v-app>
      <v-container fluid fill-height>
        <nuxt />
      </v-container>
    </v-app>
  </v-content>
</template>

<script>
  export default {
    name: "login",
    middleware: 'auth-middleware'
  }
</script>

<style scoped>

</style>