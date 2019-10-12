<template>
	<b-container>
		<b-row class='m-1 p-1'>
			<b-input v-model="newshow[0]" placeholder='Show Name?' />
		</b-row>
		</b-row>
		<b-row class='m-1 p-1'>
			<b-input v-model="newshow[1]" placeholder='Image' />
		</b-row>
		<b-row class='m-1 p-1' >
			<b-form-checkbox v-model="newshow[2].thumbnail" value="1" unchecked-value="0"/> Generate Thumbnails?
		</b-row>
		<b-row class='m-1 p-1'>
			<b-form-textarea v-model="newshow[2].preview" placeholder='Preview' />
		</b-row>
		<b-row class='m-1 p-1'>
			<b-form-textarea v-model="newshow[2].first_episode" placeholder="First episode thoughts" />
		</b-row>
    <img class='m-2' :src="newshow[1]" width=200px /> <br />
	</b-container>

</template>

<script>
export default{
  name: 'AddShow',
    data(){
    return {
      newshow: {
        0: "",
        1: "",
        2 : {
          "thumbnail" : "",
          "preview" : "",
          "first_episode" : "",
          "first_impressions": "",
          "final_thoughts" : "",
          "grade" : ""
        }
      }
    }
  },
watch: {
  "newshow": {
    handler(newVal, oldVal){

      this.$emit("updateNew", newVal)
    },
    deep: true
  },
},
  created: function(){
  },
  methods:{
  },
}
</script>

<style scoped lang='scss'>
</style>
