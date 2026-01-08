<script lang="ts" setup>
import PublicChat from './chats/PublicChat.vue';
import PrivateChat from './chats/PrivateChat.vue';
import Forum from './chats/Forum.vue';
import { ref } from 'vue';

const props = defineProps(["username"])
const emit = defineEmits(["updateIsLogged"])
const active_chat = ref("public")
</script>

<template>
    <section id="app-section">
        <div class="welcome-row">
            <div id="welcome" class="welcome">Witaj, {{ username }}</div>
            <button id="logout-btn" class="ghost" @click="emit('updateIsLogged', false)">Wyloguj</button>
        </div>

        <nav class="tabs">
            <button class="tab" :class="{ active: active_chat === 'public' }" data-tab="public"
                @click="active_chat = 'public'">Publiczny czat</button>
            <button class="tab" :class="{ active: active_chat === 'private' }" data-tab="private"
                @click="active_chat = 'private'">Prywatne</button>
            <button class="tab" :class="{ active: active_chat === 'forum' }" data-tab="forum"
                @click="active_chat = 'forum'">Forum</button>
        </nav>

        <PublicChat v-if="active_chat == 'public'" />

        <PrivateChat v-else-if="active_chat == 'private'" />

        <Forum v-else />

    </section>
</template>