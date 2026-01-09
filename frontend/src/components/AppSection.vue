<script lang="ts" setup>
import PublicChat from './chats/PublicChat.vue';
import PrivateChat from './chats/PrivateChat.vue';
import Forum from './forum/Forum.vue';
import { ref } from 'vue';
import Settings from './settings/Settings.vue';

const props = defineProps(["username"])
const emit = defineEmits(["updateIsLogged"])
const active_tab = ref("public")
</script>

<template>
    <section id="app-section">
        <div class="welcome-row">
            <div id="welcome" class="welcome">Witaj, {{ username }}</div>
            <button id="logout-btn" class="ghost" @click="emit('updateIsLogged', false)">Wyloguj</button>
        </div>

        <nav class="tabs">
            <button class="tab" :class="{ active: active_tab === 'public' }" data-tab="public"
                @click="active_tab = 'public'">Publiczny czat</button>
            <button class="tab" :class="{ active: active_tab === 'private' }" data-tab="private"
                @click="active_tab = 'private'">Prywatne</button>
            <button class="tab" :class="{ active: active_tab === 'forum' }" data-tab="forum"
                @click="active_tab = 'forum'">Forum</button>
            <button class="tab last-button" :class="{ active: active_tab === 'settings' }" data-tab="settings"
                @click="active_tab = 'settings'">Ustawienia</button>
        </nav>

        <PublicChat v-if="active_tab == 'public'" />

        <PrivateChat v-else-if="active_tab == 'private'" />

        <Forum v-else-if="active_tab == 'forum'" />

        <Settings v-else :username="props.username" />

    </section>
</template>

<style scoped>
.welcome-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}

.last-button {
    margin-left: auto;
}

.welcome {
    font-weight: 800;
}
</style>