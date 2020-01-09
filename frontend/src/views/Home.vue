<template>
  <div class="home">
	  <div class='header'>
	  <img class='header' src="@/../public/img/Logo.png" />
	  </div>
    <Editor />
  </div>
</template>

<script>
// @ is an alias to /src
import Editor from '@/views/Editor.vue'

export default {
  name: 'home',
	data () {
		return {
		}
	},
  components: {
  	Editor 
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
