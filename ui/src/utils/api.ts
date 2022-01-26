import axios, { AxiosInstance } from "axios";

export const client: AxiosInstance = axios.create({
    baseURL: "http://localhost:8000",
    headers: {
        "Content-type": "application/json",
    },
});

export default {
    install: (app:any, options:any[]) => {
        app.config.globalProperties.$api = client
    }
}
