import {createStore} from 'vuex'

export interface State {
    deviceStatus: DeviceStatus,
    device: number,
    deviceName:string

}

export enum DeviceStatus {
    CONNECTED,
    NOT_CONNECTED,
    UNAVAILABLE
}

export default createStore<State>({
    state: {
        deviceStatus: DeviceStatus.NOT_CONNECTED,
        device: 0,
        deviceName:""
    },
    mutations: {
        setDevice(state, payload) {
            state.device = payload
            state.deviceName="Device "+(payload+1)
            state.deviceStatus = DeviceStatus.CONNECTED
        },
        disconnect(state){
            state.deviceName=""
            state.device=-1
            state.deviceStatus=DeviceStatus.NOT_CONNECTED
        }
    },
    actions: {
        selectDevice({commit}, device) {
            commit("setDevice", device)
        },
        disconnect({commit}){
            commit("disconnect")
        }
    },
    modules: {},
    getters: {
        device(state) {
            return state.deviceName
        },
        status(state) {
            return state.deviceStatus
        }
    }
})
