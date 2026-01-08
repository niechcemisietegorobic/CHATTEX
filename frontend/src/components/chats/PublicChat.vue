<script lang="ts" setup>
import { API_URL } from '@/constants';
import { ref } from 'vue';
import ChatMessage from './ChatMessage.vue';

const messages = ref([])

async function refreshPublic() {
    const r = await fetch(`${API_URL}/api/public/messages`);
    const list = await r.json();

    messages.value = list;
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
                <input type="text" id="public-input" placeholder="Napisz publicznie..." required />
                <button type="submit">Wyślij</button>
            </form>
        </div>
    </section>
</template>
