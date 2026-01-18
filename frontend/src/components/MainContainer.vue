<script setup lang="ts">
import AuthSection from './AuthSection.vue';
import AppSection from './AppSection.vue';
import { ref } from 'vue';
import { API_URL, tokenHeader } from '@/constants';

const is_logged = ref(false);
const background = ref('');
const username = ref('');

function updateUsername(val: string) {
    username.value = val;
}

function updateBackground(val: string) {
    background.value = val;
    document.body.style.backgroundImage = `url("${val}")`;
}

function updateIsLogged(val: boolean) {
    is_logged.value = val;
    if (!val) {
        fetchDefaultBackground();
    } else {
        fetchBackground();
    }
}

async function fetchDefaultBackground() {
    const r = await fetch(`${API_URL}/api/background`);
    const data = await r.json();
    if (r.status !== 200) {
        alert(data.error || 'Nie udało się uzyskać adresu tła.');
        return;
    }
    updateBackground(data.url);
}

async function fetchBackground() {
    const r = await fetch(`${API_URL}/api/user/background`, {
        headers: tokenHeader()
    });
    const data = await r.json();
    if (r.status !== 200) {
        alert(data.error || 'Nie udało się uzyskać adresu tła.');
        return;
    }

    updateBackground(data.url);
}

fetchDefaultBackground();
</script>

<template>
    <main class="card">

        <AuthSection v-if="!is_logged" @updateIsLogged="updateIsLogged" @updateUsername="updateUsername"
            :is_logged="is_logged" :username="username" />

        <AppSection v-else :username="username" :background="background" @updateUsername="updateUsername"
            @updateBackground="updateBackground" @updateIsLogged="updateIsLogged" />

    </main>
</template>