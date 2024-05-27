import {defineStore} from "pinia";
import axios from "axios";
import {SERVER_ADDR} from "@/config";
import {ElNotification} from "element-plus";

const updateUrl = SERVER_ADDR + "/list/"

export const useFilesStore = defineStore('fileList',
    {
        state: () => {
            return {
                files: []
            }
        },
        actions: {
            update(username){
                axios.get(updateUrl+username)
                    .then(response => {
                        this.$reset()
                        for(let i = 0;i < response.data.length;i++){
                            this.files.push({'name': response.data[i]})
                        }
                    })
                    .catch(error => {
                        console.log(error)
                        ElNotification({
                            offset: 70,
                            title: '更新文件列表错误'
                        })
                        return
                    })
            },
            reset(){
                this.files = []
            }
        }
    })