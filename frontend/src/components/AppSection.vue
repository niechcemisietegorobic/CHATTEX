<script lang="ts" setup>
import PublicChat from './chats/PublicChat.vue';
import PrivateChat from './chats/PrivateChat.vue';
import Forum from './forum/Forum.vue';
import { ref } from 'vue';
import Settings from './settings/Settings.vue';

const props = defineProps(["username", "background"]);
const emit = defineEmits(["updateIsLogged", "updateUsername", "updateBackground"]);
const active_tab = ref("public");
const forum_notifs = ref(0);
const public_notifs = ref(0);
const private_notifs = ref(0);

function activatePublicChat() {
    active_tab.value = "public";
    public_notifs.value = 0;
}

function activatePrivateChat() {
    active_tab.value = "private";
    private_notifs.value = 0;
}

function activateForum() {
    active_tab.value = "forum";
    forum_notifs.value = 0;
}

function publicNotif() {
    public_notifs.value++;
}

function privateNotif() {
    private_notifs.value++;
}

function forumNotif() {
    forum_notifs.value++;
}

function updateUsername(val: string) {
    emit("updateUsername", val);
}

function updateBackground(val: string) {
    emit("updateBackground", val);
}
</script>

<template>
    <section id="app-section">
        <div class="welcome-row">
            <div id="welcome" class="welcome">Witaj, {{ username }}</div>
            <button id="logout-btn" class="ghost" @click="emit('updateIsLogged', false)">Wyloguj</button>
        </div>

        <nav class="tabs">
            <button class="tab" :class="{ active: active_tab === 'public' }" data-tab="public"
                @click="activatePublicChat">Publiczny czat<span v-if="public_notifs > 0" class="notif">{{ public_notifs
                    }}</span></button>
            <button class="tab" :class="{ active: active_tab === 'private' }" data-tab="private"
                @click="activatePrivateChat">Prywatne<span v-if="private_notifs > 0" class="notif">{{ private_notifs
                    }}</span></button>
            <button class="tab" :class="{ active: active_tab === 'forum' }" data-tab="forum"
                @click="activateForum">Forum<span v-if="forum_notifs > 0" class="notif">{{ forum_notifs
                    }}</span></button>
            <button class="tab last-button" :class="{ active: active_tab === 'settings' }" data-tab="settings"
                @click="active_tab = 'settings'">Ustawienia</button>
        </nav>

        <PublicChat v-if="active_tab == 'public'" :username="props.username" @privateNotif="privateNotif" @forumNotif="forumNotif" />

        <PrivateChat v-else-if="active_tab == 'private'" :username="props.username" @publicNotif="publicNotif"
            @forumNotif="forumNotif" />

        <Forum v-else-if="active_tab == 'forum'" :username="props.username" />

        <Settings v-else :username="props.username" :background="props.background" @updateUsername="updateUsername"
            @updateBackground="updateBackground" @publicNotif="publicNotif" @privateNotif="privateNotif" />

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

.notif {
    background-color: crimson;
    color: white;
    padding: 5px;
    border-radius: 100%;
    width: 1.5em;
    height: 1.5em;
    display: inline-flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    transform: translateY(-50%) translateX(20%);
}
</style>