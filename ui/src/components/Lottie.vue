<template>
  <lottie-player :src="JSON.stringify(file)" ref="player" autoplay :loop="loop" debug mode="normal" style="width: 300px">
  </lottie-player>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import "@lottiefiles/lottie-player";


@Options({
  props:{
    file: {
      required: true
    },
    loop:{
      required:false,
      default:true,
      type:Boolean
    }
  },
  watch:{
    file: function(newVal, oldVal) {
      this.init();
    }
  }
})
export default class Lottie extends Vue {

  mounted(){
    this.init();
  }
  beforeCreate(){
    // this.init()
  }
  async init() {
    console.log(this.$refs.player)
    this.$refs.player.load(''+JSON.stringify(this.file))
  }
}
</script>

<style scoped>

</style>
