<script lang="ts" setup>
import { API_URL, tokenHeader, SOCKET_URL } from '@/constants';
import { ref, type Ref, onUnmounted, nextTick } from 'vue';
import ChatMessage from './ChatMessage.vue';
import { io } from 'socket.io-client';

const props = defineProps(["username"]);
const emit = defineEmits(["privateNotif", "forumNotif", "updateOnline"]);
const messages: Ref<Array<any>> = ref([]);
const typed_message = ref('');
const chat_box: Ref<any> = ref(null);

const socket = io(SOCKET_URL, {
  auth: {
    token: tokenHeader().Authorization
  }
});

onUnmounted(() => {
  socket.close();
});

function removeMessage(id: number) {
  messages.value = messages.value.filter(e => e.id != id);
}

socket.on("public_message", (msg) => {
  messages.value.push(msg);
  scrollChatBox();
});

socket.on("public_message_delete", (msg) => {
  removeMessage(msg.id);
});

socket.on("private_message", () => {
  emit("privateNotif");
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

async function fetchPublic(scroll: boolean = true, skip: number = 0, limit: number = 30) {
  const r = await fetch(`${API_URL}/api/public/messages?skip=${skip}&limit=${limit}`, {
    method: 'GET',
    headers: tokenHeader(),
  });
  const list = await r.json();

  if (r.status !== 200) {
      return;
  }
  messages.value = list.concat(messages.value);
  if (scroll) scrollChatBox();
}

async function sendMessage() {
  const r = await fetch(`${API_URL}/api/public/messages`, {
    method: 'POST',
    headers: tokenHeader(),
    body: JSON.stringify({ content: typed_message.value })
  });
  typed_message.value = "";
  const data = await r.json();
  if (r.status !== 201) alert(data.error || 'Błąd');
  else {
    messages.value.push(data);
    scrollChatBox();
  }
}

function scrollChatBox() {
  nextTick(() => {
    if (chat_box.value) {
      chat_box.value.scrollTop = chat_box.value.scrollHeight;
    }
  });
}

fetchPublic();
</script>

<template>
  <section class="tabpane" id="tab-public">
    <div class="panel">
      <div class="panel-title">Publiczny czat</div>
      <div ref="chat_box" id="public-messages" class="box">
        <button class="ghost more-button" @click="fetchPublic(false, messages.length)">Wczytaj poprzednie</button>
        <ChatMessage v-for="message in messages" :username="props.username" :isPrivate="false" :message @removeMessage="removeMessage" />
      </div>
      <form id="public-form" class="row">
        <input v-model="typed_message" type="text" id="public-input" placeholder="Napisz publicznie..." required />
        <button type="submit" @click.prevent="sendMessage">Wyślij</button>
      </form>
    </div>
  </section>
</template>

<style scoped>
.panel-title {
  font-weight: 800;
  margin-bottom: 8px;
}

.more-button {
  padding: 4px;
  border-radius: 4px;
  font-weight: 500;
}
</style>