<script lang="ts" setup>
import { API_URL } from '@/constants';
import { ref, type Ref } from 'vue';

const users: Ref<any> = ref([]);

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
                <select id="dm-user">
                    <option v-for="(user, index) in users" :key="index" :value="user">{{ user }}</option>
                </select>
                <button id="dm-refresh" type="button" class="ghost" @click="refreshUsers">Odśwież</button>
            </div>

            <div id="dm-messages" class="box"></div>

            <form id="dm-form" class="row">
                <input type="text" id="dm-input" placeholder="Napisz prywatnie..." required />
                <button type="submit">Wyślij</button>
            </form>
        </div>
    </section>
</template>
