<script lang="ts" setup>
import { API_URL, tokenHeader } from '@/constants';
import { ref, type Ref } from 'vue';
import ChatMessage from './ChatMessage.vue';

const messages: Ref<any, any> = ref([])
const typed_message = ref('')

async function refreshPublic() {
    const r = await fetch(`${API_URL}/api/public/messages`);
    const list = await r.json();

    messages.value = list;
}

async function sendMessage() {
  const r = await fetch(`${API_URL}/api/public/messages`, {
    method: 'POST',
    headers: tokenHeader(),
    body: JSON.stringify({ content: typed_message.value })
  });
  const data = await r.json();
  if (r.status !== 201) alert(data.error || 'Błąd');
  else {
    messages.value.push({
        timestamp: Date.now(),
        username: ">(You)",
        content: typed_message.value
    })
    typed_message.value = "";
  }
}

refreshPublic();
</script>

<template>
    <!-- PUBLICZNE -->
    <section class="tabpane" id="tab-public">
        <div class="panel">
            <div class="panel-title">Publiczny czat</div>
            <div id="public-messages" class="box">
                <ChatMessage v-for="message in messages" :message/>
            </div>
            <form id="public-form" class="row">
                <input v-model="typed_message" type="text" id="public-input" placeholder="Napisz publicznie..." required />
                <button type="submit" @click.prevent="sendMessage">Wyślij</button>
            </form>
        </div>
    </section>
</template>
