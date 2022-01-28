<template>
  <div class="tw-flex tw-flex-col tw-m-2">
    <div v-if="status===FingerPrintScanStates.SCANNING" style="height: 300px" class="tw-flex tw-justify-center">
      <div>
        <n-h3 prefix="bar" align-text type="warning" >
          Please place tour finger on scanner
        </n-h3>
        <lottie
            :file="scanLoading"
        />
      </div>
    </div>
    <div v-if="status===FingerPrintScanStates.SCAN_SUCCESS" style="height: 300px" class="tw-flex tw-justify-center">
      <div>
        <n-h3 prefix="bar" type="success" align-text>
          Scan Successful
        </n-h3>
        <lottie
            :loop="false"
            :file="scanSuccess"
        />
      </div>
    </div>
    <div v-if="status===FingerPrintScanStates.SCAN_FAILED" style="height: 300px" class="tw-flex tw-justify-center">
      <div>
        <n-h3  prefix="bar" align-text type="error">
          Scan Failed
        </n-h3>
        <lottie
            :loop="false"
            :file="scanFailed"
        />
      </div>
    </div>
    <div v-if="status===FingerPrintScanStates.IDLE" style="height: 300px" class="tw-flex tw-justify-center">
      <div>
        <n-h3  prefix="bar" align-text type="primary">
          No pending scan requests
        </n-h3>
        <lottie
            :file="scanIdle"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import Lottie from "./Lottie.vue";
import scan_progress from "@/assets/finger-print.json"
import scan_failed from "@/assets/fingerprint-error.json"
import scan_success from "@/assets/fingerprint-success.json"
import scan_idle from "@/assets/waiting.json"
import {FingerPrintScanStates} from "@/utils/enums";


@Options({
  props:{
    status:{
      required:true
    }
  },
  components:{
    Lottie
  },
})
export default class FingerPrint extends Vue{
  FingerPrintScanStates=FingerPrintScanStates
  scanLoading=scan_progress
  scanSuccess=scan_success
  scanFailed=scan_failed
  scanIdle=scan_idle
  scanStatus:FingerPrintScanStates=FingerPrintScanStates.IDLE
}
</script>

<style scoped>

</style>
