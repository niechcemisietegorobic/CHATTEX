<script lang="ts" setup>
import { API_URL, tokenHeader, SOCKET_URL } from '@/constants';
import { ref, type Ref, onUnmounted, nextTick } from 'vue';
import { io } from 'socket.io-client';
import ChatMessage from './ChatMessage.vue';

const props = defineProps(["username"]);
const emit = defineEmits(["publicNotif", "forumNotif", "updateOnline"]);

const users: Ref<any> = ref([]);
const selected_user = ref('');
const dm: Ref<Array<any>> = ref([]);
const typed_message = ref('');
const chat_box: Ref<any> = ref(null);

async function fetchDM(scroll: boolean = true, skip: number = 0, limit: number = 30) {
    const r = await fetch(`${API_URL}/api/private/messages?with=${selected_user.value}&skip=${skip}&limit=${limit}`, {
        method: 'GET',
        headers: tokenHeader()
    });
    const list = await r.json();

    if (r.status !== 200) {
        return;
    }
    dm.value = list.concat(dm.value);
    if (scroll) scrollChatBox();
}

async function sendDM() {
    const r = await fetch(`${API_URL}/api/private/messages`, {
        method: 'POST',
        headers: tokenHeader(),
        body: JSON.stringify({ to: selected_user.value, content: typed_message.value })
    });
    typed_message.value = "";
    const data = await r.json();
    if (r.status !== 201) alert(data.error || 'Błąd wysyłania');
    else {
        dm.value.push(data);
        scrollChatBox();
    }
}

async function fetchUsers(skip: number = 0, limit: number = 10) {
    const r = await fetch(`${API_URL}/api/users?skip=${skip}&limit=${limit}`, {
        method: 'GET',
        headers: tokenHeader(),
    });
    const list: any[] = await r.json();

    users.value = users.value.concat(list);//.filter(u => u !== props.username));
}

function scrollChatBox() {
    nextTick(() => {
        if (chat_box.value) {
            chat_box.value.scrollTop = chat_box.value.scrollHeight;
        }
    });
}

const socket = io(SOCKET_URL, {
    auth: {
        token: tokenHeader().Authorization
    }
});

onUnmounted(() => {
    socket.close();
});

function removeMessage(id: number) {
    dm.value = dm.value.filter(e => e.id != id);
}

socket.on("private_message", (msg) => {
    if (msg.from == selected_user.value) {
        dm.value.push(msg);
        scrollChatBox();
    }
});

socket.on("private_message_delete", (msg) => {
    removeMessage(msg.id);
});

socket.on("public_message", () => {
    emit("publicNotif");
});

socket.on("forum_post", () => {
    emit("forumNotif");
});

socket.on("forum_comment", () => {
    emit("forumNotif");
});

socket.on("stats", () => {
    emit("updateOnline");
});

function selectUser(user: string) {
    selected_user.value = user;
    dm.value = [];
    fetchDM();
}

fetchUsers();
</script>

<template>
    <!-- PRYWATNE -->
    <section class="tabpane" id="tab-private">
        <div class="panel">
            <div class="panel-title">Prywatne wiadomości</div>

            <div class="column">
                <div class="users-box">
                    <div class="panel-title">Lista użytkowników</div>
                    <div class="users-list">
                        <button v-for="(user) in users" :key="user" class="ghost expand"
                            :class="{ active: user == selected_user }" @click="selectUser(user)">{{
                                user }}</button>
                        <button id="dm-refresh" type="button" class="expand"
                            @click="fetchUsers(users.length)">Więcej</button>
                    </div>
                </div>

                <div class="dm-box">
                    <div ref="chat_box" class="box">
                        <div v-if="dm.length == 0">Brak wiadomości do wyświetlenia</div>
                        <div v-else>
                            <button class="ghost more-button" @click="fetchDM(false, dm.length)">Wczytaj
                                poprzednie</button>
                            <ChatMessage v-for="message in dm" :username="props.username"
                                :isPrivate="true" :message @removeMessage="removeMessage" />
                        </div>
                    </div>

                    <form id="dm-form" class="row">
                        <input v-model="typed_message" type="text" id="dm-input" placeholder="Napisz prywatnie..."
                            required />
                        <button type="submit" @click.prevent="sendDM">Wyślij</button>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.panel-title {
    font-weight: 800;
    margin-bottom: 8px;
}

.column {
    display: flex;
    flex-flow: row;
    gap: 10px;
}

.dm-box {
    width: 100%;
    flex: 1 1 auto;
}

.users-box {
    padding: 5px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
}

.users-list {
    margin: 10px 0;
    overflow-y: scroll;
    min-height: 0;
    height: max(260px, 40vh);
}

.users-list > button {
    margin-top: 3px;
}

.users-list::-webkit-scrollbar {
  display: none;
}

.expand {
    width: 100%;
}

.ghost.active {
    background: linear-gradient(90deg, rgb(138, 138, 138) 1%, rgba(190, 190, 190, 0) 40%);
    border: 2px solid black;
}

.more-button {
    padding: 4px;
    border-radius: 4px;
    font-weight: 500;
}
</style>
