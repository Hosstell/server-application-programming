import Vue from 'vue'
import Notifications from 'vue-notification'

if (process.client) {
  Vue.use(Notifications)
}
