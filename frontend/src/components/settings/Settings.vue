<script lang="ts" setup>
import { API_URL, tokenHeader } from '@/constants';
import { ref } from 'vue';

const props = defineProps(["username"]);

const is_changing_username = ref(false);
const changed_username = ref(props.username);
const invite_code = ref('');
const bg = new URL('@/assets/background.png', import.meta.url).href

async function change_username() {
    const r = await fetch(`${API_URL}/api/user/username`, {
        method: 'POST',
        headers: tokenHeader(),
        body: JSON.stringify({ username: changed_username.value })
    });
    const data = await r.json();
    if (r.status !== 200) {
        alert(data.error || 'Zmiana nazwy użytkownika zakończona niepowodzeniem.');
        return;
    }

    is_changing_username.value = false;
}

async function fetch_invite_code() {
    const r = await fetch(`${API_URL}/api/user/invite`, {
        headers: tokenHeader()
    });
    const data = await r.json();
    if (r.status !== 200) {
        alert(data.error || 'Zmiana nazwy użytkownika zakończona niepowodzeniem.');
        return;
    }

    invite_code.value = data.code;
}

fetch_invite_code();
</script>

<template>
    <section class="tabpane" id="tab-settings">
        <div class="panel">
            <div class="panel-title">Ustawienia</div>

            <div v-if="is_changing_username" class="row setting">
                Nowa nazwa użytkownika: <input v-model="changed_username" type="text" placeholder="Nazwa użytkownika"/> 
                <button @click="change_username">Zapisz</button>
            </div>
            <div v-else class="row setting">
                Nazwa użytkownika: {{ props.username }} <button @click="is_changing_username = true">Zmień</button>
            </div>

            <div class="row setting">
                <span>Twój kod zaproszenia: {{ invite_code }} <button>Odśwież</button></span>
                <img :src="bg" />
            </div>

            <div class="row setting">
                <span>Tło aplikacji <button>Zmień</button></span>
                <img :src="bg" />
            </div>

        </div>
    </section>
</template>

<style scoped>
.panel-title {
    font-weight: 800;
    margin-bottom: 8px;
}

.setting {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 6px 6px;
    font-weight: 200;
}

img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
</style>