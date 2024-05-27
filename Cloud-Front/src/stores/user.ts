import { defineStore } from 'pinia'

export const useUserStore = defineStore('user',
    {
    state: () => {
        return {
            username: ''
        }
    },
    actions: {
        update(username: string){
            this.username = username
        },
        reset(){
            this.username = ''
        }
    },
    persist: {
        enabled: true
    }
})