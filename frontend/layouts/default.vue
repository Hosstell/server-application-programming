<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      absolute
      temporary
    >
      <v-list>
        <v-list-item>
          Вы вошли как {{ $$user.username }}
        </v-list-item>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
          @click="closeNavigator"
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <app-bar @changeMenuState="drawer = !drawer"/>

    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import AppBar from "./AppBar";

export default {
  components: {AppBar},
  middleware: 'auth-middleware',
  data () {
    return {
      clipped: true,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-numeric',
          title: 'Распознать',
          to: '/recognize'
        },
        {
          icon: 'mdi-image-multiple',
          title: 'Мои изображения',
          to: '/my_pictures'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Vuetify.js'
    }
  },
  methods: {
    closeNavigator() {
      this.drawer = false
    }
  }
}
</script>
