import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import VueSocketIO from 'vue-socket.io'

import {
    library
} from '@fortawesome/fontawesome-svg-core'

//Add the fontawesome icons here
import {
    faCaretRight,
    faPrint,
    faThLarge,
    faUndo,
    faPlay,
    faEdit,
    faTimes,
    faCheck,
    faSortUp,
    faSortDown
} from '@fortawesome/free-solid-svg-icons'

library.add(faThLarge)
library.add(faCaretRight)
library.add(faPrint)
library.add(faEdit)
library.add(faUndo)
library.add(faPlay)
library.add(faTimes)
library.add(faCheck)
library.add(faSortUp)
library.add(faSortDown)

// Define the backend port
Vue.prototype.$port = 7500




//End of Font awesome icon adds
import {
    FontAwesomeIcon
} from '@fortawesome/vue-fontawesome'


Vue.component('font-awesome-icon', FontAwesomeIcon)


import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)


Vue.config.productionTip = false

// Toggle Button
import ToggleButton from 'vue-js-toggle-button'
Vue.use(ToggleButton)

// Socket IO library

const options = {}; //Options object to pass into SocketIO

var url = window.location.href
var url_arr = url.split("/")
var socket_url = url_arr[0] + "//" + url_arr[2]


Vue.use(new VueSocketIO({
    debug: true,
    connection: socket_url,
    vuex: {
        store,
        actionPrefix: 'SOCKET_',
        mutationPrefix: 'SOCKET_'
    },
    options: {} //Optional options
}))

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')