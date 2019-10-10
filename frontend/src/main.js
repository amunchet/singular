import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'


import { library } from '@fortawesome/fontawesome-svg-core'

//Add the fontawesome icons here
import { faEdit, faTimes, faCheck, faSortUp, faSortDown} from '@fortawesome/free-solid-svg-icons'

library.add(faEdit)
library.add(faTimes)
library.add(faCheck)
library.add(faSortUp)
library.add(faSortDown)

// Define the backend port
Vue.prototype.$port = 7500




//End of Font awesome icon adds
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'


Vue.component('font-awesome-icon', FontAwesomeIcon)


import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
