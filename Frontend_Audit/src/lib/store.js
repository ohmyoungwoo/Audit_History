import { writable } from "svelte/store";

const persisi_storage = (key, initValue) => {
    const storeedValueStr = localStorage.getItem(key)
    const store = writable(storeedValueStr != null ? JSON.parse(storeedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persisi_storage("page", 0)