<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
    </div>
    <router-view/>

  </div>
</template>
<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

export default{
	name: 'app'
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0 !important;
  padding: 0 !important;
}
body{
	margin: 0 !important;
	padding: 0 !important;
}
#nav {
	display: none;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
