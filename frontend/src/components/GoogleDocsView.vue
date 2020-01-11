<template>
  <div>
    <div class='header'>
      This is the view to copy and paste notes about the given shows into a Google Document repository (or whatever word processor you would like).  Storing all shows will clutter the JSON file, so I recommend moving to more permanent storage, such as Google Docs.
    </div>
    <pre>
    {{json}}
    </pre>
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
            "name" : "",
            "preview" : "",
            "first_episode" : "",
            "review" : "",
            "grade" : "",
            "dropped" : "",
            "url" : "",
          }
        ]

      },
        {
          "season" : "Summer",
          "year" : 2019
        }
      ]

    }
  },
}
</script>

<style scoped lang="scss">
</style>
