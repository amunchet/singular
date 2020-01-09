<template>
	<b-container class='main'>
    {{json}}
		<b-button class='mb-3' variant="primary" @click="restart_server()">Restart Server</b-button>

    <b-card class='dark-bg p-2 m-2 left' v-show="show_docker_output">
      <b-button @click="show_docker_output = false" class='mt-0 mr-0 ' variant="danger"><font-awesome-icon icon="times" /></b-button>
	<br /><br />
      <div id='dockerinfo' class='maxheight' v-html="docker_output"></div>
    </b-card>
		<b-row>
		<b-col class='left'>
			<b-card class='m-2'>
				<h2><font-awesome-icon class='pb-2 mr-2' icon='sort-down' />RSS Feeds</h2>
<b-container>
				<b-row v-for="item,idx in json.rss_feed" >
					<b-input class='m-1 'style='width:80%; float:left;' 
						 v-model="json.rss_feed[idx]">
					</b-input>
          <b-button class='m-1' variant='danger' @click="drop_rss(idx)"><b><font-awesome-icon icon="times" /></b></b-button>
				</b-row>
				<b-row class='left'>
					<b-button class='mt-2' variant="primary" @click="add_rss">+ Add RSS Feed</b-button>
				</b-row>
				</b-container>

			</b-card>
			<b-card class='m-2'>
				<b-modal id="modal-1" title="Add/Edit Show" @ok="handleAddOk()">
					<AddShow v-on:updateNew="handleAddUpdate" />
				</b-modal>
        <h2>Shows<h2 class='left'><b-button v-b-modal.modal-1 @click="add_show()" variant='primary'>+ Add Show</b-button>&nbsp;&nbsp;<b-button>Print View (Google Doc)</b-button><b-button>Return to Normal View</b-button></h2></h2>
				<b-card-group deck>
				<b-card no-body class='overflow-hidden m-3 bg-primary p-2' style='min-width:250px;max-width:350px;text-align:center;' v-for="items,idx in json.shows" >
					<b-row no-gutters>
						<b-col>

					<b-card-title class='p-1 overflow-hidden text-light' style='height: 30px;text-align:center;'>{{items[0]}}</b-card-title>
<img :src="items[1]" height=300px />
<b-modal :id="'modal-' + idx" title="Add/Edit Show" @ok="editShow()">
					<AddShow v-on:updateNew="handleAddUpdate" :edit="items" />
				</b-modal>

						<b-button v-b-modal="'modal-' + idx" class='mt-2 mb-2' style='width:100%' variant='primary'><font-awesome-icon icon="edit"  />&nbsp;Edit</b-button><br />
					<b-button @click="drop_show(idx)" class='mt-1 half_width tall_button' variant='danger'><font-awesome-icon icon="times" size="1x" />&nbsp;&nbsp;Dropped</b-button>
					<b-button class='mt-1 half_width float_right tall_button' variant='success' @click='complete_show(idx)'><font-awesome-icon icon="check" size="1x" />  Completed</b-button>
						</b-col>

					</b-row>
				</b-card>
				</b-card-group>				


	
			
			</b-card><b-card>
				<h2>Removed RSS Feeds</h2>
				<b-button>Clear Old RSS Feeds</b-button>
				{{json.removed_rss_feeds}}
			</b-card>
			<b-card>
				<h2>Completed Shows</h2>
				(Need to have grade in here as well as final thoughts)

      <b-card-group deck>
        <b-card no-body class='overflow-hidden m-3 bg-success p-2' style='min-width:250px;max-width:350px;text-align:center;' v-for="items,idx in json.completed_shows" >
          <b-row no-gutters v-if="items">
            <b-col>

              <b-card-title class='p-1 overflow-hidden text-light' style='height: 30px;text-align:center;'>{{items[0]}}<b-button class='float_right' @click="restore_show(idx, 'completed')" >Restore</b-button></b-card-title>
          <img :src="items[1]" height=300px />
          <b-form-input class="mt-3" v-model="items[2].grade" placeholder='Final Grade' />
            <b-form-text>Show Grade</b-form-text>
            <b-form-textarea  v-model="items[2].final_thoughts" class='mt-2' placeholder='Final Thoughts' />
              <b-form-text>Final Thoughts</b-form-text>
            </b-col>

					</b-row>
				</b-card>
				</b-card-group>				




			</b-card>


			<b-card>
				<h2>Dropped Shows</h2>
				<b-card-group deck>
				<b-card no-body class='overflow-hidden m-3 bg-secondary p-2' style='min-width:250px;max-width:350px;text-align:center;' v-for="items,idx in json.dropped" >
          <b-row no-gutters v-if="items">
						<b-col>

					<b-card-title class='p-1 overflow-hidden text-light' style='height: 30px;text-align:center;'>{{items[0]}}<b-button @click="restore_show(idx, 'dropped')" class='float_right'>Restore</b-button></b-card-title>
<img :src="items[1]" height=300px />
				<b-form-textarea v-model="items[2].preview" class='mt-3' placeholder='Preview' />
          <b-form-text>Preview Thoughts</b-form-text>
				<b-form-textarea v-model="items[2].final_thoughts" class='mt-2' placeholder='Dropped Reason...'/>
          <b-form-text>Dropped Reason</b-form-text>
						</b-col>

					</b-row>
				</b-card>
				</b-card-group>				



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

    const self = this;          
	},
	sockets: {
		connect: function(){
			console.log("Socket connected")
		},
		response: function(data){
			this.show_docker_output = true
			this.docker_output += data + "<br />"
			this.$nextTick(()=>{
				var container = this.$el.querySelector("#dockerinfo")
				container.scrollTop = container.scrollHeight
			})
		},
	},
  watch:{
    json: {
      deep: true,

      handler: async function(){
      this.save()
    }
    }
  },
	methods: {
		init: function(){

		axios.get("http://" + window.location.hostname + ":" + this.$port + "/get").then(data=>{
			this.json = data.data
		})
		},
		add_show: function(){
			this.show_add = true 
		},
		add_rss: function(){
      console.log(this.json)
			this.json.rss_feed.push("")
		},
		save: async function(){
      if (this.json.success == undefined){ 
			axios.post("http://" + window.location.hostname + ":" + this.$port + "/save", this.json).then(resp=>{
				//this.init()
        console.log("Saved!")
			})
      }
		},
		drop_rss: function(idx){
			if(this.json.removed_rss_feeds == undefined){
				this.json["removed_rss_feeds"] = []
			}
			this.json["removed_rss_feeds"].push(this.json.rss_feed[idx])
			this.json.rss_feed.splice(idx,1)
		},
    get_docker_status: function(){
      axios.get("http://" + window.location.hostname + ":" + this.$port + "/docker/status").then(resp => {
        this.docker_output = resp.data.replace("\n", "<br />")
      }).catch(resp=>{
        this.docker_output = "ERROR : <div style='color: red'>" + resp.response.data + "</div>"
      })
    },
    restart_server: function(){
	this.$socket.emit("restart")
    },
  drop_show: function(idx){
			console.log("Dropping " + idx)
			if(this.json.dropped == undefined){
				this.json.dropped = []
			}
			this.json['dropped'].push(this.json.shows[idx])
			this.json.shows.splice(idx,1)

		},
		complete_show: function(idx){
			console.log("Completing " + idx)
			if(this.json.completed_shows == undefined){
				this.json.completed_shows = []
			}
			this.json['completed_shows'].push(this.json.shows[idx])
			this.json.shows.splice(idx,1)
		},
    restore_show: function(idx, type){
      console.log("Restoring show of " + type + ": " + idx)
      if(this.json.shows == undefined){
          this.json.shows = []
        }

      if (type == "completed"){
        this.json['shows'].push(this.json.completed_shows[idx])
        this.json.completed_shows.splice(idx, 1)
      }
      if(type == "dropped"){

        this.json['shows'].push(this.json.dropped[idx])
        this.json.dropped.splice(idx, 1)
      }
    },
    handleAddUpdate: function(val){
      this.temp_add = val
    },
    handleAddOk: function(){
      console.log(this.temp_add)
      if (this.json.shows == undefined){
        this.json.shows = []
      }
      this.json.shows.unshift(JSON.parse(JSON.stringify(this.temp_add)))
    },
    editShow: function(idx){
      this.json.shows[idx] = JSON.parse(JSON.stringify(this.temp_add))
    }
	},
	data() {
		return {
      temp_add: "",
			show_add: false,
      docker_output: "",
      show_docker_output: false,
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
.selected{
  background-color: lightblue !important;
  border: 3px solid #efefee !important;
}
.float_left{
	float: left;
}
.form-text{
  color: black !important;
  width: 100%;
  text-align: left;
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
  background-color: #43434e;
  color: white;
}
.red{
  color: red !important;
}
.maxheight{
	min-height: 150px;
	max-height: 300px;
	overflow-y: scroll;
}
.maxheight::-webkit-scrollbar { width: 0 !important }
.maxheight{ overflow: -moz-scrollbars-none; }
.maxheight{ -ms-overflow-style: none; }

</style>
