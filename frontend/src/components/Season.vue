<template>
    <div class='main p-3'>
        <b-row>
            <b-col>
                Season
                <b-select v-model="season" :options="seasons">
                </b-select>
            </b-col>
            <b-col>
                Year
                <b-input v-model="year" />
            </b-col>
        </b-row>
    </div>
</template>

<script>
    export default {
        name: "Season",
        props: ["inp_season", "inp_year"],
        watch: {
            "season": function (newval) {
                this.$emit("season", newval)
            },
            "year": function (newval) {
                this.$emit("year", newval)
            },
        },
        data() {
            return {
                season: "",
                year: "",
                seasons: [{
                        "text": "Spring",
                        "value": "spring"
                    },
                    {
                        "text": "Summer",
                        "value": "summer"
                    },
                    {
                        "text": "Fall",
                        "value": "fall"
                    },
                    {
                        "text": "Winter",
                        "value": "winter"
                    }
                ],
            }
        },
        methods: {
            calculateSeason: function () {
                // Parse the current month and return approparite season best guess
                var d = new Date();
                var n = d.getMonth() + 1;
                if (n > 0 && n <= 3) {
                    this.season = "spring"
                } else if (n > 3 && n <= 6) {
                    this.season = "summer"
                } else if (n > 6 && n <= 9) {
                    this.season = "fall"
                } else {
                    this.season = "winter"
                }

                this.year = d.getFullYear()
                this.$forceUpdate()
            }
        },
        mounted: function () {
            if ((this.inp_season == "" && this.inp_year == "") || (this.inp_season == undefined && this.inp_year ==
                    undefined)) {
                this.calculateSeason()
            } else {
                this.year = this.inp_year
                this.season = this.inp_season
            }
        }
    }
</script>

<style scoped lang="scss">
    .main {
        background-color: #ebebef;
        width: 100%;
    }
</style>