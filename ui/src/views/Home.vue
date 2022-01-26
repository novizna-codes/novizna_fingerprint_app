<template>
  <div class="tw-p-4">
    <n-page-header subtitle="">
      <template #title>
        {{device}}
      </template>
      <template #header>
        <n-breadcrumb>
          <n-breadcrumb-item>FingerSense</n-breadcrumb-item>
          <n-breadcrumb-item>{{ device }}</n-breadcrumb-item>
        </n-breadcrumb>
      </template>
      <div>
        <n-divider/>
        <n-button @click="disconnectDevice" block type="error">Disconnect</n-button>
      </div>
    </n-page-header>
    <n-modal
        v-model:show="disconnecting"
        :mask-closable="false"
        :closable="false"
        :bordered="false"
        preset="dialog"
        size="small"
    >
      <template #header>
        <n-h3 prefix="bar"  >Disconnecting</n-h3>
        <!--        <n-h3 v-elif="connectionSuccessful" prefix="bar" type="success">Connected successfully</n-h3>-->
        <!--        <n-h3 v-else prefix="bar" type="error" >Connection error</n-h3>-->
      </template>
      <div class="tw-flex tw-justify-center">
        <n-spin size="large"/>
      </div>
    </n-modal>
    <n-modal
        v-model:show="disconnectingSuccessful"
        :mask-closable="false"
        :closable="false"
        :bordered="false"
        preset="dialog"
        size="small"
        @positive-click="onSuccess"
        positive-text="Ok"
    >
      <template #header>
        <n-h3  prefix="bar" type="success">DisConnected successfully</n-h3>
        <!--        <n-h3 v-else prefix="bar" type="error" >Connection error</n-h3>-->
      </template>
    </n-modal>
    <n-modal
        v-model:show="disconnectingError"
        :mask-closable="false"
        :closable="false"
        :bordered="false"
        type="error"
        @negative-click="onError"
        positive-text="Ok"
        preset="dialog"
        size="small"
    >
      <template #header>
        <n-h3 prefix="bar" type="error" >DisConnection error</n-h3>
      </template>
    </n-modal>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import {client} from "@/utils/api";

export default class Home extends Vue {
  get device(){
    return this.$store.getters['device']
  }
  disconnecting=false
  disconnectingSuccessful=false
  disconnectingError=false
  disconnectDevice(){
    this.disconnecting=true
    this.disconnectingSuccessful=false
    client.post("disconnect").then(response=>{
      const data=response.data
      if(data.success){
        this.disconnectingSuccessful=true
        this.$store.dispatch("disconnect")
      }else {
        this.disconnectingError=true
      }
    }).finally(()=>{
      this.disconnecting=false
    })
  }
  onSuccess(){
    this.$router.back()
  }
  onError(){

  }
}
</script>
