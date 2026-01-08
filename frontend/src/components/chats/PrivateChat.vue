<script lang="ts" setup>
import { API_URL, tokenHeader } from '@/constants';
import { ref, type Ref } from 'vue';

const users: Ref<any> = ref([]);
const selected_user = ref('');
const dm: Ref<any> = ref([]);
const typed_message = ref('');

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
    }
}

async function refreshUsers() {
    const r = await fetch(`${API_URL}/api/users`);
    const list: any[] = await r.json();
    const me = localStorage.getItem('username');

    //w dm pokazuje kazdego opocz mnie
    users.value = list.filter(u => u !== me);
}

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

            <div id="dm-messages" class="box">
                <div class="msg" v-if="dm.length == 0">Brak wiadomości do wyświetlenia</div>
                <div class="msg" v-else v-for="m in dm">{{ m.timestamp }} - {{ m.from }}: {{ m.content }}</div>
            </div>

            <form id="dm-form" class="row">
                <input v-model="typed_message" type="text" id="dm-input" placeholder="Napisz prywatnie..." required />
                <button type="submit" @click.prevent="sendDM">Wyślij</button>
            </form>
        </div>
    </section>
</template>
