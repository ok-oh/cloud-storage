import { createPinia } from 'pinia'
import piniaPersist from 'pinia-plugin-persistedstate'

const store = createPinia()
store.use(piniaPersist)

export default store