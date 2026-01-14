<script lang="ts" setup>
import { API_URL, tokenHeader, SOCKET_URL } from '@/constants';
import { ref, type Ref, onUnmounted, nextTick } from 'vue';
import { io } from 'socket.io-client';
import ChatMessage from './ChatMessage.vue';

const props = defineProps(["username"]);

const users: Ref<any> = ref([]);
const selected_user = ref('');
const dm: Ref<any> = ref([]);
const typed_message = ref('');
const chat_box: Ref<any> = ref(null);

async function refreshDM() {
    dm.value = [];
    const r = await fetch(`${API_URL}/api/private/messages?with=${selected_user.value}`, {
        headers: tokenHeader()
    });
    const data = await r.json();

    if (r.status !== 200) {
        return;
    }
    dm.value = data;
    scrollChatBox();
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

async function refreshUsers() {
    const r = await fetch(`${API_URL}/api/users`);
    const list: any[] = await r.json();

    //w dm pokazuje kazdego opocz mnie
    users.value = list.filter(u => u !== props.username);
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

socket.on("private_message", (msg) => {
    if (msg.from == selected_user.value) {
        dm.value.push(msg);
        scrollChatBox();
    }
});

refreshUsers();
</script>

<template>
    <!-- PRYWATNE -->
    <section class="tabpane" id="tab-private">
        <div class="panel">
            <div class="panel-title">Prywatne wiadomości</div>

            <div class="row">
                <select v-model="selected_user" id="dm-user" @change="refreshDM">
                    <option v-for="(user, index) in users" :key="index" :value="user">{{ user }}</option>
                </select>
                <button id="dm-refresh" type="button" class="ghost" @click="refreshUsers">Odśwież</button>
            </div>

            <div ref="chat_box" id="dm-messages" class="box">
                <div v-if="dm.length == 0">Brak wiadomości do wyświetlenia</div>
                <ChatMessage v-else v-for="message in dm" :isPrivate="true" :message/>
            </div>

            <form id="dm-form" class="row">
                <input v-model="typed_message" type="text" id="dm-input" placeholder="Napisz prywatnie..." required />
                <button type="submit" @click.prevent="sendDM">Wyślij</button>
            </form>
        </div>
    </section>
</template>

<style scoped>
.panel-title{
  font-weight: 800;
  margin-bottom: 8px;
}
</style>
