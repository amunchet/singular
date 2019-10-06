<template>
	<b-container class='main'>
		<b-row>
		<b-col class='left'>
			<b-card>
			<h2>RSS Feeds</h2>
<b-container>
				<b-row v-for="items in json.rss_feed">
					<b-input class='m-1 'style='width:80%; float:left;'
						:value="items">
					</b-input>
					<b-button class='m-1' variant='danger'><b>X</b></b-button>
				</b-row>
				<b-row class='left'>
					<b-button variant="primary">+ Add RSS Feed</b-button>
				</b-row>
				</b-container>

			</b-card>

			<b-card>
				<h2>Shows</h2>
<b-container>
				<b-row v-for="items in json.shows" class='m-3'>
					<b-col style='width:10%;'>
						<img :src="items[1]" width=100%/><br />
						<b-button class='mt-2' style='width:100%;' variant='primary'>Change</b-button>
					</b-col>
					<b-col style='width:90%'>
					<b-input class='m-1 '
						:value="items[0]">
					</b-input>
					<b-button class='m-1 float_left' variant='danger'><b>Dropped</b></b-button>
					<b-button class='m-1 float_left' variant='success'><b>Completed</b></b-button>
					</b-col>
				</b-row>
				<b-row class='left'>
					<b-button variant="primary">+ Add RSS Feed</b-button>
				</b-row>
				</b-container>

	
			
			</b-card><b-card>
				<h2>Removed RSS Feeds</h2></b-card>
			<b-card>
				<h2>Dropped Shows</h2></b-card>
		</b-col>
		<b-col class='left'>
			<b-button class='mb-3' variant="success" >Submit</b-button>
		<v-jsoneditor v-model="json"
			      class="editor"
			      >
		</v-jsoneditor>
		</b-col>

		</b-row>
	</b-container>
</template>

<script>

import VJsoneditor from 'vue-jsoneditor';
import axios from 'axios'
export default {
	name: 'Editor',
	components: {
		VJsoneditor
	},
	mounted: function(){
		axios.get("http://localhost:5000/get").then(data=>{
			this.json = data.data
		})

	},
	methods: {
	},
	data() {
		return {
			json: {
				success: true
			}
		}
	},
	props: {
		msg: String
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.float_left{
	float: left;
}
h3 {
	margin: 40px 0 0;
}
ul {
	list-style-type: none;
	padding: 0;
}
li {
	display: inline-block;
	margin: 0 10px;
}
a {
	color: #42b983;
}
.left{ text-align: left !important; }
.main{
	margin: auto;
	margin-top: 20px;
}
.editor{
	height: 500px !important;
}
</style>
