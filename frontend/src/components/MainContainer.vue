<script setup lang="ts">
import AuthSection from './AuthSection.vue';
import AppSection from './AppSection.vue';
import { ref } from 'vue';

const is_logged = ref(false);
const username = ref('');

function updateUsername(val: string) {
    username.value = val;
}

function updateIsLogged(val: boolean) {
    is_logged.value = val;
}
</script>

<template>
    <main class="card">

        <AuthSection v-if="!is_logged" @updateIsLogged="updateIsLogged" @updateUsername="updateUsername" :is_logged="is_logged" :username="username" />

        <AppSection v-else :username="username" @updateIsLogged="updateIsLogged" />

    </main>
</template>