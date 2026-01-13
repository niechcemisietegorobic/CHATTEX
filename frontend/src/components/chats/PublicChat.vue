<script lang="ts" setup>
import { API_URL, tokenHeader, SOCKET_URL } from '@/constants';
import { ref, type Ref, onUnmounted, nextTick } from 'vue';
import ChatMessage from './ChatMessage.vue';
import { io } from 'socket.io-client';

const messages: Ref<any, any> = ref([])
const typed_message = ref('')
const chat_box: Ref<any> = ref(null);

const socket = io(SOCKET_URL, {
  auth: {
    token: tokenHeader().Authorization
  }
});

onUnmounted(() => {
  socket.close();
});

socket.on("public_message", (msg) => {
  messages.value.push(msg);
  scrollChatBox();
});

async function refreshPublic() {
  const r = await fetch(`${API_URL}/api/public/messages`, {
    headers: tokenHeader(),
  });
  const list = await r.json();

  messages.value = list;
  scrollChatBox();
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

refreshPublic();
</script>

<template>
  <!-- PUBLICZNE -->
  <section class="tabpane" id="tab-public">
    <div class="panel">
      <div class="panel-title">Publiczny czat</div>
      <div ref="chat_box" id="public-messages" class="box">
        <ChatMessage v-for="message in messages" :isPrivate="false" :message />
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
</style>