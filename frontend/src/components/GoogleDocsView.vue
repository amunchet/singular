<template>
  <div>
    <div class='header'>
      This is the view to copy and paste notes about the given shows into a Google Document repository (or whatever word processor you would like).  Storing all shows will clutter the JSON file, so I recommend moving to more permanent storage, such as Google Docs.
    </div>
    <pre>
    {{print_json}}
  
    </pre>

    <div v-for="season in print_json" v-if="season">
      <h2>{{season.season}} {{season.year}}</h2>
    <table>
      <tr><th>Name</th><th>Grade</th><th>Note</th></tr>
      <tr v-for="shows in season.shows" v-if="shows">
        <td>
          <img :src="shows.thumbnail" />
          {{shows.name}}</td>
        <td>{{shows.grade}}</td>
        <td><b>Preview</b><br />
          {{shows.preview}}
          <br />
          <b>First Episode</b><br />
          {{shows.first_episode}}
          <br />
          <b>Final Thoughts</b><br />
          {{shows.final_thoughts}}
        </td>
      </tr>
    </table>
    </div>

  </div>
</template>

<script>
export default{
  name: "GoogleDocsView",
  props: ["json"],
  data(){
    return{
      print_json: 
      [{
        "season" : "Winter",
        "year" : 2020,
        "shows": [
          {
            "name" : "Show A",
            "preview" : "PV looked pretty good",
            "first_episode" : "Strong star, we'll see if it lasts",
            "final_thoughts" : "Overall decent, but fell off to the end",
            "grade" : "C+",
            "thumbnail" : "http://google.com/img.url",
          },
          {
            "name" : "Show B",
            "preview" : "PV looked pretty bad",
            "first_episode" : "Not good start",
            "grade" : "F",
            "final_thoughts" : "Dropped like a hot rock",
            "thumbnail" : "http://google.com/bad.jpg"  
          }
        ]


      },
        {
          "season" : "Summer",
          "year" : 2019,
          "shows": [
            {
              "name" : "Show G",
              "preview" : "bad start",
              "first_episode" : "mediocre start",
              "grade" : "F",
              "final_thoughts" : "Dropped like a hot rock",
              "thumbnail" : "http://google.com/bad.jpg"  
            }

          ],
        }
      ]

    }
  },
}
</script>

<style scoped lang="scss">
</style>
