<script setup lang="ts">
import AuthSection from './AuthSection.vue';
import AppSection from './AppSection.vue';
import { ref } from 'vue';
import { API_URL } from '@/constants';

const is_logged = ref(false);
const background = ref('');
const username = ref('');

function updateUsername(val: string) {
    username.value = val;
}

function updatedBackground(val: string) {
    background.value = val;
    document.body.style.backgroundImage = `url("${val}")`;
}

function updateIsLogged(val: boolean) {
    is_logged.value = val;
    if (!val) {
        fetchDefaultBackground();
    }
}

async function fetchDefaultBackground() {
    const r = await fetch(`${API_URL}/api/background`);
    const data = await r.json();
    if (r.status !== 200) {
        alert(data.error || 'Nie udało się uzyskać adresu tła.');
        return;
    }
    updatedBackground(data.url);
}

fetchDefaultBackground();
</script>

<template>
    <main class="card">

        <AuthSection v-if="!is_logged" @updateIsLogged="updateIsLogged" @updateUsername="updateUsername" 
            :is_logged="is_logged" :username="username" />

        <AppSection v-else :username="username" @updateUsername="updateUsername" @updateIsLogged="updateIsLogged" />

    </main>
</template>