<template>
  <div>
    Season
    {{season}}
    <b-select>
    </b-select>

    Year
    <b-input v-model="year"/>
  </div>
</template>

<script>
export default{
  name: "Season",
  props: ["season", "year"],
  data(){
    return {
    }
  },
  methods: {
    calculateSeason: function(){
      // Parse the current month and return approparite season best guess
      
    }
  },
  mounted: {
  }
}
</script>

<style scoped lang="scss">
</style>
