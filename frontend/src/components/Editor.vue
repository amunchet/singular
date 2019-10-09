<template>
	<b-container class='main'>
		<b-button class='mb-3' @click="save" variant="success" >Submit</b-button>&nbsp;&nbsp;
		<b-button class='mb-3' @click="save" variant="primary" >Restart Server</b-button>
		<b-row>
		<b-col class='left'>
			<b-card class='m-2'>
				<h2><font-awesome-icon class='pb-2 mr-2' icon='sort-down' />RSS Feeds</h2>
<b-container>
				<b-row v-for="item,idx in json.rss_feed" >
					<b-input class='m-1 'style='width:80%; float:left;'
						 v-model="json.rss_feed[idx]">
					</b-input>
					<b-button class='m-1' variant='danger' @click="drop_rss(idx)"><b>X</b></b-button>
				</b-row>
				<b-row class='left'>
					<b-button class='mt-2' variant="primary" @click="add_rss">+ Add RSS Feed</b-button>
				</b-row>
				</b-container>

			</b-card>
			<b-card class='m-2'>
				<b-modal id="modal-1" title="Add/Edit Show">
					<AddShow />
				</b-modal>
				<h2>Shows<h2 class='left'><b-button v-b-modal.modal-1 @click="add_show()" variant='primary'>+ Add Show</b-button>&nbsp;&nbsp;<b-button>Print View (Google Doc)</b-button></h2></h2>
<b-container>
				<b-card-group deck>
				<b-card no-body class='overflow-hidden m-3 bg-primary p-2' style='min-width:250px;max-width:350px;text-align:center;' v-for="items,idx in json.shows" >
					<b-row no-gutters>
						<b-col>

					<b-card-title class='p-1 overflow-hidden text-light' style='height: 30px;text-align:center;'>{{items[0]}}</b-card-title>
<img :src="items[1]" height=300px />
						<b-button class='mt-2 mb-2' style='width:100%' variant='primary'><font-awesome-icon icon="edit" />&nbsp;Edit</b-button><br />
					<b-button class='mt-1 half_width tall_button' variant='danger'><font-awesome-icon icon="times" size="1x" />&nbsp;&nbsp;Dropped</b-button>
					<b-button class='mt-1 half_width float_right tall_button' variant='success' @click='complete_show(idx)'><font-awesome-icon icon="check" size="1x" />  Completed</b-button>
						</b-col>

					</b-row>
				</b-card>
				</b-card-group>				

				</b-container>

	
			
			</b-card><b-card>
				<h2>Removed RSS Feeds</h2>
				<b-button>Clear Old RSS Feeds</b-button>
				{{json.removed_rss_feeds}}
			</b-card>
			<b-card>
				<h2>Completed Shows</h2>
			<b-button>Clear Old RSS Feeds</b-button>
			{{json.completed_shows}}
			</b-card>


			<b-card>
				<h2>Dropped Shows</h2>
<b-button>Clear Old RSS Feeds</b-button>
<b-container>
				<b-card-group deck>
				<b-card no-body class='overflow-hidden m-3 bg-secondary p-2' style='min-width:250px;max-width:350px;text-align:center;' v-for="items in json.dropped" >
					<b-row no-gutters>
						<b-col>

					<b-card-title class='p-1 overflow-hidden text-light' style='height: 30px;text-align:center;'>{{items[0]}}</b-card-title>
<img :src="items[1]" height=300px />
				<b-form-textarea class='mt-3' placeholder='Preview' />
				<b-form-textarea class='mt-2' placeholder='Dropped Reason...'/>
						</b-col>

					</b-row>
				</b-card>
				</b-card-group>				

				</b-container>


			</b-card>
		</b-col>
		</b-row>
		<b-row>
		<b-col class='left'>
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
import AddShow from '@/components/AddShow'
import axios from 'axios'
export default {
	name: 'Editor',
	components: {
		VJsoneditor,
		AddShow

	},
	mounted: function(){
		this.init()
	},
	methods: {
		init: function(){

		axios.get("http://" + window.location.hostname + ":5000/get").then(data=>{
			this.json = data.data
		})
		},
		add_show: function(){
			this.show_add = true 
		},
		add_rss: function(){
			this.json.rss_feed.push("")
		},
		save: function(){
			axios.post("http://" + window.location.hostname + ":5000/save", this.json).then(resp=>{
				this.init()
			})
		},
		drop_rss: function(idx){
			if(this.json.removed_rss_feeds == undefined){
				this.json["removed_rss_feeds"] = []
			}
			this.json["removed_rss_feeds"].push(this.json.rss_feed[idx])
			this.json.rss_feed.splice(idx,1)
		},
		complete_show: function(idx){
			console.log("Completing " + idx)
			if(this.json.completed_shows == undefined){
				this.json.completed_shows = []
			}
			this.json['completed_shows'].push(this.json.shows[idx])
			this.json.shows.splice(idx,1)

		}
	},
	data() {
		return {
			show_add: false,
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
.full_width{
width: 100%;
}
.tall_button{
	height: 40px;
	
}
.half_width{
	float: left;
	margin-right: 2%;
	width: 47%;
}
.float_right{
	margin-right:0;
	float: right;
}
.dark-bg{

}
</style>
