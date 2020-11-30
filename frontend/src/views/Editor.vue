<template>
    <b-container class='main'>
        <b-button class='mb-3' variant="warning" @click="restart_server()">
            <font-awesome-icon class='mr-2' icon="play" />
            Run Singular Downloader</b-button>

        <b-card class='dark-bg p-2 m-2 left' v-show="show_docker_output">
            <b-button @click="show_docker_output = false" class='mt-0 mr-0 ' variant="danger">
                <font-awesome-icon icon="times" />
            </b-button>
            <br /><br />
            <div id='dockerinfo' class='maxheight' v-html="docker_output"></div>
        </b-card>
        <b-row>
            <b-col class='left'>
                <b-card class='m-2'>
                    <h2>
                        <font-awesome-icon class='pb-2 mr-2 hover_hand' icon='sort-down' v-show="show_rss"
                            @click="show_rss=false" />
                        <font-awesome-icon v-show="!show_rss" @click="show_rss=true" class='pt-2 mb-1  mr-2 hover_hand'
                            icon='caret-right' />
                        RSS Feeds</h2>
                    <b-container>
                        <b-row v-show="show_rss" v-for="item,idx in json.rss_feed">
                            <b-col style='width:75%;'>

                                <b-button class='m-1' variant='danger' @click="drop_rss(idx)"><b>
                                        <font-awesome-icon icon="times" /></b></b-button>
                                <b-input @blur="save()" class='m-1 ' style='width:80%; float:left;'
                                    v-model.lazy="json.rss_feed[idx]">
                                </b-input>
                            </b-col>
                            <b-col>
                                <b-list-group horizontal>
                                    <b-list-group-item variant="dark" small v-for="listed, idxx in rss[item]"
                                        v-if="listed">
                                        {{listed}}
                                    </b-list-group-item>
                                </b-list-group>
                            </b-col>

                        </b-row>
                        <b-row class='left'>
                            <b-button class='mt-2' variant="primary" @click="add_rss">+ Add RSS Feed</b-button>
                        </b-row>
                    </b-container>

                </b-card>
                <b-card class="m-2">

                    <h2>Direct Shows</h2>
                    <b-button variant="success" @click="()=>{
                    if(json.direct == undefined){
                    json.direct = []
                    }
                    json.direct.push('')
                    $forceUpdate()
                    }
                    ">+Add Direct Download</b-button>

                    <b-row v-if="json.direct != undefined" v-for="(url, idx) in json.direct" v-bind:key="idx" class="m-2">
                      <b-col cols="1">
                        <b-button variant="danger" @click="()=>{
                        json.direct.splice(idx, 1)
                        save()
                        $forceUpdate()
                        }"
                        >
                        <font-awesome-icon icon="times" size="1x" />
                      </b-button>
                      </b-col>
                      <b-col>
                      <b-input v-model="json.direct[idx]" @blur="save()"/>
                      </b-col>
                    </b-row>

                </b-card>

                <b-card class='m-2'>
                    <b-modal id="modal-add" title="Add/Edit Show" @ok="handleAddOk()">
                        <AddShow v-on:updateNew="handleAddUpdate" />
                    </b-modal>
                    <div class='float-right'>
                        <font-awesome-icon class='pt-1 mt-2 mr-3 text-muted' icon="th-large" size=2x />
                        <toggle-button :width="50" :height="30" color="green" v-model="showPrint" />
                        <font-awesome-icon icon="print" class='pt-1 mt-2 ml-3 text-muted' size=2x />
                    </div>
                    <h2>

                        <font-awesome-icon class='pb-2 mr-2 hover_hand' icon='sort-down' v-show="show_shows"
                            @click="show_shows=false" />
                        <font-awesome-icon v-show="!show_shows" @click="show_shows=true"
                            class='pt-2 mb-1  mr-2 hover_hand' icon='caret-right' />


                        Shows<h2 class='left'>
                            <b-button class='mt-2' v-if="!showPrint" v-b-modal.modal-add @click="add_show()"
                                variant='primary'>+ Add Show</b-button>
                        </h2>
                    </h2>

                    <b-button variant="danger" v-if="showPrint" class='mb-2' @click="clear_completed()">Clear Completed
                        and Dropped</b-button>
                    <GoogleDocsView v-show="showPrint" :json="json" />


                    <b-card-group v-show="show_shows" deck>
                        <b-card no-body class='overflow-hidden m-3 bg-primary p-2'
                            style='min-width:250px;max-width:350px;text-align:center;' v-for="items,idx in json.shows">
                            <b-row no-gutters>
                                <b-col>

                                    <b-card-title class='p-1 overflow-hidden text-light'
                                        style='height: 30px;text-align:center;'>{{items[0]}}</b-card-title>
                                    <img :src="items[1]" height=300px />
                                    <b-modal :id="'modal-current-' + idx" title="Add/Edit Show" @ok="editShow()">
                                        <AddShow v-on:updateNew="handleAddUpdate" :edit="items" />
                                    </b-modal>

                                    <b-button v-b-modal="'modal-current-' + idx" class='mt-2 mb-2' style='width:100%'
                                        variant='primary'>
                                        <font-awesome-icon icon="edit" />&nbsp;Edit</b-button><br />
                                    <b-button @click="drop_show(idx)" class='mt-1 half_width tall_button'
                                        variant='danger'>
                                        <font-awesome-icon icon="times" />&nbsp;&nbsp;Dropped</b-button>
                                    <b-button class='mt-1 half_width float_right tall_button' variant='success'
                                        @click='complete_show(idx)'>
                                        <font-awesome-icon icon="check" /> Completed</b-button>
                                </b-col>

                            </b-row>
                        </b-card>
                    </b-card-group>




                </b-card>
                <b-card v-show="!showPrint" class='m-2'>
                    <h2>


                        <font-awesome-icon class='pb-2 mr-2 hover_hand' icon='sort-down' v-show="show_completed"
                            @click="show_completed=false" />
                        <font-awesome-icon v-show="!show_completed" @click="show_completed=true"
                            class='pt-2 mb-1  mr-2 hover_hand' icon='caret-right' />

                        Completed Shows</h2>
                    <b-card-group v-show="show_completed" deck>
                        <b-card no-body class='overflow-hidden m-3 bg-success p-2'
                            style='min-width:250px;max-width:350px;text-align:center;'
                            v-for="items,idx in json.completed_shows"
                            v-if="items != undefined && items[2] != undefined">
                            <b-row no-gutters v-if="items">
                                <b-col>

                                    <b-card-title class='p-1 text-light' style='height: 30px;text-align:center;'>
                                        {{items[0]}}<div class='hover_hand float_right' variant="link"
                                            @click="restore_show(idx, 'completed')">
                                            <font-awesome-icon icon="undo" class='text-white' />
                                        </div>
                                    </b-card-title>
                                    <img :src="items[1]" height=300px />

                                    <b-modal :id="'modal-completed-' + idx" title="Add/Edit Show" @ok="editShow()">
                                        <AddShow v-on:updateNew="handleAddUpdate" :edit="items" />
                                    </b-modal>

                                    <b-button v-b-modal="'modal-completed-' + idx" class='mt-2 mb-2' style='width:100%'
                                        variant='primary'>
                                        <font-awesome-icon icon="edit" />&nbsp;Edit</b-button><br />


                                    <b-form-input @blur="save()" class="mt-3" v-model="items[2].grade"
                                        placeholder='Final Grade' />
                                    <b-form-text>Show Grade</b-form-text>
                                    <b-form-textarea :ref="'text-' + idx"
                                        @blur="items[2].final_thoughts = saveTextarea('text-', idx)" class='mt-2'
                                        :value="items[2].final_thoughts" placeholder='Final Thoughts'>
                                    </b-form-textarea>
                                    <b-form-text>Final Thoughts</b-form-text>
                                </b-col>

                            </b-row>
                        </b-card>
                    </b-card-group>




                </b-card>


                <b-card v-show="!showPrint" class='m-2'>
                    <h2>


                        <font-awesome-icon class='pb-2 mr-2 hover_hand' icon='sort-down' v-show="show_dropped"
                            @click="show_dropped=false" />
                        <font-awesome-icon v-show="!show_dropped" @click="show_dropped=true"
                            class='pt-2 mb-1  mr-2 hover_hand' icon='caret-right' />

                        Dropped Shows</h2>
                    <b-card-group v-show="show_dropped" deck>
                        <b-card no-body class='overflow-hidden m-3 bg-secondary p-2'
                            style='min-width:250px;max-width:350px;text-align:center;' v-for="items,idx in json.dropped"
                            v-if="items != undefined && items[2] != undefined">
                            <b-row no-gutters v-if="items">
                                <b-col>

                                    <b-card-title class='p-1 text-light' style='height: 30px;text-align:center;'>
                                        {{items[0]}}<div @click="restore_show(idx, 'dropped')"
                                            class='float_right hover_hand'>
                                            <font-awesome-icon icon="undo" class='text-white' />
                                        </div>
                                    </b-card-title>
                                    <img :src="items[1]" height=300px />
                                    <b-modal :id="'modal-dropped-' + idx" title="Add/Edit Show" @ok="editShow()">
                                        <AddShow v-on:updateNew="handleAddUpdate" :edit="items" />
                                    </b-modal>

                                    <b-button v-b-modal="'modal-dropped-' + idx" class='mt-2 mb-2' style='width:100%'
                                        variant='primary'>
                                        <font-awesome-icon icon="edit" />&nbsp;Edit</b-button><br />



                                    <b-form-textarea :ref="'dropped-preview-' + idx"
                                        @blur="items[2].preview = saveTextarea('dropped-preview-', idx)" class='mt-2'
                                        :value="items[2].preview" placeholder='Preview'>
                                    </b-form-textarea>

                                    <b-form-text>Preview Thoughts</b-form-text>


                                    <b-form-textarea :ref="'dropped-' + idx"
                                        @blur="items[2].final_thoughts = saveTextarea('dropped-', idx)" class='mt-2'
                                        :value="items[2].final_thoughts" placeholder='Dropped Reason...'>
                                    </b-form-textarea>


                                    <b-form-text>Dropped Reason</b-form-text>
                                </b-col>

                            </b-row>
                        </b-card>
                    </b-card-group>



                </b-card>
                <b-card class='m-2'>
                    <h2>

                        <font-awesome-icon class='pb-2 mr-2 hover_hand' icon='sort-down' v-show="show_dropped_rss"
                            @click="show_dropped_rss=false" />
                        <font-awesome-icon v-show="!show_dropped_rss" @click="show_dropped_rss=true"
                            class='pt-2 mb-1  mr-2 hover_hand' icon='caret-right' />


                        Removed RSS Feeds</h2>
                    <b-button @click="clear_removed_rss()">Clear Old RSS Feeds</b-button>
                    <b-container v-show="show_dropped_rss">
                        <b-table class='mt-3' small striped :items="removed_rss_feeds()" />
                    </b-container>
                </b-card>

            </b-col>
        </b-row>
        <b-row>
            <b-col class='left'>
                <v-jsoneditor v-model="json" class="editor m-2">
                </v-jsoneditor>
            </b-col>

        </b-row>
    </b-container>
</template>

<script>
    import VJsoneditor from 'vue-jsoneditor';
    import AddShow from '@/components/AddShow'
    import GoogleDocsView from '@/components/GoogleDocsView'
    import axios from 'axios'
    export default {
        name: 'Editor',
        components: {
            VJsoneditor,
            AddShow,
            GoogleDocsView

        },
        mounted: function () {
            this.init()

            const self = this;
        },
        sockets: {
            connect: function () {
                console.log("Socket connected")
            },
            response: function (data) {
                this.show_docker_output = true
                this.docker_output += data + "<br />"
                this.$nextTick(() => {
                    var container = this.$el.querySelector("#dockerinfo")
                    container.scrollTop = container.scrollHeight
                })
            },
        },
        methods: {

            init: function () {

                axios.get("/get").then(data => {
                    this.json = data.data
                    axios.get("/rss").then(
                    res => {
                        this.rss = res.data

                    })
                })
            },
            clear_completed: function () {
                this.$bvModal.msgBoxConfirm(
                        'Are you sure you wish to remove the completed and dropped shows?  This action cannot be undone.'
                        )
                    .then(value => {
                        if (value) {
                            this.json.completed_shows = []
                            this.json.dropped = []
                            this.save()
                        }
                    })
            },
            clear_removed_rss: function () {
                this.$bvModal.msgBoxConfirm(
                        'Are you sure you wish to remove the old rss feeds?  This action cannot be undone.')
                    .then(value => {
                        if (value) {
                            this.json.removed_rss_feeds = []
                            this.save()
                        }
                    })
            },
            saveTextarea: function (nm, idx, sv) {
                // Returns the value and bypasses the update until the blur is called
                this.save()
                return "" + this.$refs[nm + idx][0].$el.value
            },
            removed_rss_feeds: function () {
                if (this.json != undefined && this.json.removed_rss_feeds != undefined) {
                    return this.json.removed_rss_feeds.map(x => {
                        return {
                            "Removed RSS URL": x
                        }
                    })
                }
                this.save()
            },
            add_show: function () {
                this.show_add = true
                this.save()
            },
            add_rss: function () {
                this.json.rss_feed.push("")
            },
            save: async function () {
                if (this.json.success == undefined) {
                    axios.post("//" + window.location.hostname + ":" + this.$port + "/save", this.json).then(
                        resp => {
                            //this.init()
                            console.log("Saved!")
                        })
                }
            },
            drop_rss: function (idx) {
                if (this.json.removed_rss_feeds == undefined) {
                    this.json["removed_rss_feeds"] = []
                }
                this.json["removed_rss_feeds"].push(this.json.rss_feed[idx])
                this.json.rss_feed.splice(idx, 1)
                this.save()
            },
            get_docker_status: function () {
                axios.get("/docker/status").then(resp => {
                    this.docker_output = resp.data.replace("\n", "<br />")
                }).catch(resp => {
                    this.docker_output = "ERROR : <div style='color: red'>" + resp.response.data + "</div>"
                })
            },
            restart_server: function () {
                this.$socket.emit("restart")
            },
            drop_show: function (idx) {
                console.log("Dropping " + idx)
                if (this.json.dropped == undefined) {
                    this.json.dropped = []
                }
                this.json['dropped'].push(this.json.shows[idx])
                this.json.shows.splice(idx, 1)
                this.save()
            },
            complete_show: function (idx) {
                console.log("Completing " + idx)
                if (this.json.completed_shows == undefined) {
                    this.json.completed_shows = []
                }
                this.json['completed_shows'].push(this.json.shows[idx])
                this.json.shows.splice(idx, 1)
                this.save()
            },
            restore_show: function (idx, type) {
                console.log("Restoring show of " + type + ": " + idx)
                if (this.json.shows == undefined) {
                    this.json.shows = []
                }

                if (type == "completed") {
                    this.json['shows'].push(this.json.completed_shows[idx])
                    this.json.completed_shows.splice(idx, 1)
                }
                if (type == "dropped") {

                    this.json['shows'].push(this.json.dropped[idx])
                    this.json.dropped.splice(idx, 1)
                }
                this.save()
            },
            handleAddUpdate: function (val) {
                this.temp_add = val
                this.save()
            },
            handleAddOk: function () {
                console.log(this.temp_add)
                if (this.json.shows == undefined) {
                    this.json.shows = []
                }
                this.json.shows.unshift(JSON.parse(JSON.stringify(this.temp_add)))
                this.save()
            },
            editShow: function (idx) {
                this.json.shows[idx] = JSON.parse(JSON.stringify(this.temp_add))
                this.save()
            }
        },
        data() {
            return {
                show_rss: true,
                show_shows: true,
                show_completed: true,
                show_dropped: true,
                show_dropped_rss: false,
                showPrint: false,
                temp_add: "",
                show_add: false,
                rss: [],
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
    .selected {
        background-color: lightblue !important;
        border: 3px solid #efefee !important;
    }

    .float_left {
        float: left;
    }

    .form-text {
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

    .left {
        text-align: left !important;
    }

    .main {
        margin: auto;
        margin-top: 20px;
    }

    .editor {
        height: 500px !important;
    }

    .full_width {
        width: 100%;
    }

    .tall_button {
        height: 40px;

    }

    .half_width {
        float: left;
        margin-right: 2%;
        width: 47%;
    }

    .float_right {
        margin-right: 0;
        float: right;
    }

    .dark-bg {
        background-color: #43434e;
        color: white;
    }

    .red {
        color: red !important;
    }

    .maxheight {
        min-height: 150px;
        max-height: 300px;
        overflow-y: scroll;
    }

    .maxheight::-webkit-scrollbar {
        width: 0 !important
    }

    .maxheight {
        overflow: -moz-scrollbars-none;
    }

    .maxheight {
        -ms-overflow-style: none;
    }

    /deep/ .list-group-item {
        padding: .33rem .5rem;
    }

    .hover_hand {
        cursor: pointer;
    }
</style>
