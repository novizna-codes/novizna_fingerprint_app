<template>
  <div class="tw-p-4">
    <n-page-header subtitle="">
      <template #title>
        Available Devices
      </template>
      <template #header>
        <n-breadcrumb>
          <n-breadcrumb-item>FingerSense</n-breadcrumb-item>
          <n-breadcrumb-item>Devices</n-breadcrumb-item>
        </n-breadcrumb>
      </template>

      <template #extra>
        <n-space>
          <n-button @click="checkDevices"  secondary type="primary" >
            <template #icon>
              <n-icon>
                <Refresh />
              </n-icon>
            </template>
            Refresh
          </n-button>

        </n-space>
      </template>
      <div v-if="loadingDevice" class="tw-flex tw-col tw-h-full tw-align-center tw-justify-center">
        <n-spin description="Checking available devices" size="large"/>

      </div>
      <div v-else-if="deviceError" class="tw-flex tw-h-full tw-flex-col tw-px-4 tw-align-center tw-justify-center">
        <n-alert type="error"> {{ errorMessage }}</n-alert>
        <n-divider/>
        <n-button @click="checkDevices"  secondary type="primary" >
          <template #icon>
            <n-icon>
              <Refresh />
            </n-icon>
          </template>
          Refresh
        </n-button>
      </div>
      <div v-else class="tw-flex tw-flex-col ">
        <n-h2 prefix="bar"><n-text type="primary">Please select your device</n-text></n-h2>

        <n-select v-model:value="selectedDevice" :options="options">

        </n-select>
        <span class="tw-m-4 tw-block">

        </span>
        <n-button  @click="selectDevice" type="primary">Select</n-button>
      </div>
      <!--      <template #footer>As of April 3, 2021</template>-->
    </n-page-header>
    <n-modal
        v-model:show="connectionLoading"
        :mask-closable="false"
        :closable="false"
        :bordered="false"
        preset="dialog"
        size="small"
    >
      <template #header>
        <n-h3 prefix="bar"  >Connecting</n-h3>
<!--        <n-h3 v-elif="connectionSuccessful" prefix="bar" type="success">Connected successfully</n-h3>-->
<!--        <n-h3 v-else prefix="bar" type="error" >Connection error</n-h3>-->
      </template>
      <div class="tw-flex tw-justify-center">
        <n-spin size="large"/>
      </div>
    </n-modal>
    <n-modal
        v-model:show="connectionSuccessful"
        :mask-closable="false"
        :closable="false"
        :bordered="false"
        preset="dialog"
        size="small"
        @positive-click="onSuccess"
        positive-text="Ok"
    >
      <template #header>
                <n-h3  prefix="bar" type="success">Connected successfully</n-h3>
        <!--        <n-h3 v-else prefix="bar" type="error" >Connection error</n-h3>-->
      </template>
    </n-modal>
    <n-modal
        v-model:show="connectionError"
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
        <n-h3 prefix="bar" type="error" >Connection error</n-h3>
      </template>
    </n-modal>
  </div>
</template>

<script lang="ts">
import {Options, Vue,setup} from 'vue-class-component';
import {client} from "@/utils/api";
import { Refresh,CashOutline } from '@vicons/ionicons5'
import {useDialog} from "naive-ui";

@Options({
  components: {
    Refresh,
    CashOutline
  },
})
export default class SetupView extends Vue {
  loadingDevice = true
  deviceError = false
  errorMessage = ""
  availableDevice = 0
  selectedDevice = 0
  options = []
  connectionDialog=false
  connectionSuccessful=false
  connectionLoading=false
  connectionError=false
  // dialog=setup(()=>useDialog())

  fetchingSettings(){
    return client.get("/settings")
  }

  checkDevices() {
    this.loadingDevice=true
    client.get<DevicesResponse>("/devices").then(response => {
      const data= response.data
      if (!data.success) {
        this.deviceError = true
        this.errorMessage = data.message
      } else {
        this.availableDevice = data.devices
        this.errorMessage = ""
        this.deviceError = false
        this.options = []
        for (let i = 1; i < this.availableDevice + 1; i++) {
          this.options.push({
            label: 'Device ' + i,
            value: i - 1
          })
        }
      }
    }).catch((error) => {

    }).finally(() => {
      this.loadingDevice = false
    })
  }
  selectDevice(){
    this.connectionLoading=true
    this.connectionSuccessful=false
    this.connectionError=false
    client.get("/connect/"+this.selectedDevice).then(response=>{
      const data=response.data
      if (data.success){
        this.connectionSuccessful=true
        this.$store.dispatch("selectDevice",this.selectedDevice)
      }else {
        this.connectionError=true
      }
    }).finally(()=>{
      this.connectionLoading=false
    })
  }
  onSuccess(){
    this.$router.push({name:'home'})
  }

  onError(){}

  mounted() {
    this.fetchingSettings().then(response=>{
      const data=response.data
      if(data.connected){
        this.$store.dispatch("selectDevice",data.device)
        this.$router.push({name:'home'})
      }
      this.checkDevices()
    })
  }

}
</script>

<style scoped>

</style>
