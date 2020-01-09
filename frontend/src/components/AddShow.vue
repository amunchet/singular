<template>
	<b-container>
		<b-row class='m-1 p-1'>

			<b-input v-model="newshow[0]" aria-describedby="name_help" placeholder='Show Name' />
        <b-form-text id='name_help'>Name of the Show</b-form-text>
		</b-row>
		</b-row>
		<b-row class='m-1 p-1'>
			<b-input aria-describedby="url_help" v-model="newshow[1]" placeholder='URL (http(s)://XXX.jpg)' />
        <b-form-text id='url_help'>URL of Show Cover</b-form-text>
		</b-row>
		</b-row>
		<b-row class='m-1 p-1' >
			<b-form-checkbox v-model="newshow[2].thumbnail" value="1" unchecked-value="0"/> Generate Thumbnails?
		</b-row>
		<b-row class='m-1 p-1'>
			<b-form-textarea aria-describedby="preview_help" v-model="newshow[2].preview" placeholder='Preview Thoughts' />
        <b-form-text id='preview_help'>Preview Thoughts (before the first episode is seen.)</b-form-text>

		</b-row>
		<b-row class='m-1 p-1'>
			<b-form-textarea aria-describedby="first_help" v-model="newshow[2].first_episode" placeholder="First Episode Thoughts" />
        <b-form-text id='first_help'>Thoughts on the First Episode.</b-form-text>
		</b-row>
    <img class='m-2' :src="newshow[1]" width=200px /> <br />
    <b-form-text id='name_help'>Image Preview</b-form-text>
	</b-container>
</template>

<script>
export default{
  name: 'AddShow',
    data(){
    return {
      newshow: [
        "",
        "",
        {
          "thumbnail" : "",
          "preview" : "",
          "first_episode" : "",
          "first_impressions": "",
          "final_thoughts" : "",
          "grade" : ""
        }
        ]
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
    if(this.edit != undefined && this.edit != ""){
      this.newshow = this.edit
    }
  },
  methods:{
  },
  props: ['edit']
}
</script>

<style scoped lang='scss'>
/deep/ .form-text{
  width: 100%;
  text-align: right;
}
</style>
