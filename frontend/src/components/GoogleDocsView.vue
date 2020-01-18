<template>
    <div>
        <div class='header'>
            This is the view to copy and paste notes about the given shows into a Google Document repository (or
            whatever word processor you would like). Storing all shows will clutter the JSON file, so I recommend moving
            to more permanent storage, such as Google Docs.
        </div>


        <div v-for="season in print_json" v-if="season">
            <h2>{{season.season}} {{season.year}}</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Note</th>
                </tr>
                <tr v-for="shows in season.shows" v-if="shows">
                    <td style='width:25%'>
                        <img height=100px :src="shows.thumbnail_url" />
                        {{shows.name}}</td>
                    <td style="text-align: center;width:10%;" :class="returnGradeColor(shows.grade)">{{shows.grade}}
                    </td>
                    <td>
                        <h4>Preview</h4>
                        {{shows.preview}}
                        <br /><br />
                        <h4>First Episode</h4>
                        {{shows.first_episode}}
                        <br /><br />
                        <h4>Final Thoughts</h4>
                        {{shows.final_thoughts}}
                    </td>
                </tr>
            </table>
        </div>

    </div>
</template>

<script>
    export default {
        name: "GoogleDocsView",
        props: ["json"],
        watch: {
            json: function () {
                try {
                    this.processJSON()
                } catch (e) {
                    console.log(e)
                }
            }
        },
        methods: {
            returnGradeColor: function (grade) {
                try {
                    if (grade != "undefined" && grade[0] != undefined) {
                        return "grade" + grade[0].toUpperCase()
                    }
                    return "grade"
                } catch (e) {
                    return "grade"
                }
            },
            processJSON: function () {
                /* Processes the JSON into Google Doc format */

                var found_seasons = [{
                    "season": "Unknown",
                    "year": "Unknown",
                    "shows": []
                }]

                this.json.dropped.forEach(val => {
                    if (val[2] != undefined) {
                        val[2].grade = "F"
                    }
                })

                var all_shows = [...this.json.dropped, ...this.json.completed_shows]

                all_shows.forEach(val => {
                    var created_show = {
                        "name": val[0],
                        "thumbnail_url": val[1],
                        ...val[2]
                    }


                    if (val[2] != undefined && val[2].season != undefined && val[2].year != undefined) {
                        var found = found_seasons.filter(x => x.year != undefined && x.season !=
                            undefined && x.year == val[2].year && x.season == val[2].season).length
                        if (found < 1) {
                            found_seasons.push({
                                "season": val[2].season,
                                "year": val[2].year,
                                "shows": [created_show]
                            })
                        } else {
                            found_seasons.forEach(found_val => {
                                if (found_val.season == val[2].season && found_val.year == val[2]
                                    .year) {
                                    found_val.shows.push(created_show)
                                }
                            })
                        }
                    } else if (val[2] != undefined && (val[2].season == undefined || val[2].year ==
                            undefined)) {
                        found_seasons.forEach(found_val => {
                            if (found_val.season == "Unknown" && found_val.year == "Unknown") {
                                found_val.shows.push(created_show)
                            }
                        })
                    }
                })

                if (found_seasons[0].shows.length == 0) {
                    found_seasons.splice(0, 1)
                }
                this.print_json = found_seasons.sort((first, sec) => {
                    var seasons = {
                        "spring": 1,
                        "summer": 2,
                        "fall": 3,
                        "winter": 4
                    }
                    if (first['year'] > sec['year']) {
                        return -1
                    } else if (first['year'] < sec['year']) {
                        return 1
                    } else {
                        if (seasons[first['season'].toLowerCase()] > seasons[sec['season'].toLowerCase()]) {
                            return -1
                        } else {
                            return 1
                        }
                    }
                })
            }
        },
        mounted: function () {},
        data() {
            return {
                print_json: [{
                        "season": "Winter",
                        "year": 2020,
                        "shows": [{
                                "name": "Show A",
                                "preview": "PV looked pretty good",
                                "first_episode": "Strong star, we'll see if it lasts",
                                "final_thoughts": "Overall decent, but fell off to the end",
                                "grade": "C+",
                                "thumbnail": "http://google.com/img.url",
                            },
                            {
                                "name": "Show B",
                                "preview": "PV looked pretty bad",
                                "first_episode": "Not good start",
                                "grade": "F",
                                "final_thoughts": "Dropped like a hot rock",
                                "thumbnail": "http://google.com/bad.jpg"
                            }
                        ]


                    },
                    {
                        "season": "Summer",
                        "year": 2019,
                        "shows": [{
                                "name": "Show G",
                                "preview": "bad start",
                                "first_episode": "mediocre start",
                                "grade": "F",
                                "final_thoughts": "Dropped like a hot rock",
                                "thumbnail": "http://google.com/bad.jpg"
                            }

                        ],
                    }
                ]

            }
        },
    }
</script>

<style scoped lang="scss">
    h2 {
        text-transform: uppercase;
        margin-top: 20px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    table,
    tr,
    th,
    td {
        border: 1px solid black;
        padding-left: 10px;
        padding-right: 10px;
    }

    table tbody tr {
        border: 1px solid black;
    }

    /* Grades Styling */
    .gradeA {
        background-color: green;
    }

    .gradeB {
        background-color: darkgreen;
    }

    .gradeC {
        background-color: yellow;
    }

    .gradeD {
        background-color: darkorange;
    }

    .grade,
    .gradeF {
        background-color: grey;
    }
</style>