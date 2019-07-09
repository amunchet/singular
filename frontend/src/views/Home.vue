<template>
  <div class="home">
	  <div class='header'>
	  <img class='header' src="@/../public/img/Logo.png" />
	  </div>
    <HelloWorld />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
	data () {
		return {
		}
	},
  components: {
    HelloWorld
  }
}
</script>
<style scoped>
*{
	margin: 0;
	padding: 0;
}
div.header{
	background-color: #45454b;
	overflow: hidden;
}
img.header{
	height: 80px;
	margin: auto;

}
div.home{
	background-color: #ebebed;
	min-height: 800px;
}
</style>
