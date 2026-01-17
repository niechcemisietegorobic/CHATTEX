<script lang="ts" setup>
import { API_URL, tokenHeader } from '@/constants';
import { ref, type Ref } from 'vue';

const props = defineProps(["username"]);
const emit = defineEmits(["updateUsername"]);

const backgroundInput: Ref<any> = ref(null);
const is_changing_username = ref(false);
const changed_username = ref(props.username);
const invite_code = ref('');
const bg = new URL('@/assets/background.png', import.meta.url).href

function openBackgroundInput() {
    backgroundInput.value.click();
}

async function change_background(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    const r = await fetch(`${API_URL}/api/user/background`, {
        method: 'POST',
        headers: tokenHeader(),
        body: formData
    });
    const data = await r.json();
    if (r.status !== 200) {
        alert(data.error || 'Zmiana tła aplikacji zakończona niepowodzeniem.');
        return;
    }
    alert("[DEV] success");
}

async function change_username() {
    is_changing_username.value = false;

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
    emit("updateUsername", changed_username.value);
}

async function fetch_invite_code() {
    const r = await fetch(`${API_URL}/api/user/invite`, {
        headers: tokenHeader()
    });
    const data = await r.json();
    if (r.status !== 200) {
        alert(data.error || 'Nie udało się uzyskać kodu zaproszenia.');
        return;
    }

    invite_code.value = data.code;
}

async function refresh_invite_code() {
    const r = await fetch(`${API_URL}/api/user/invite`, {
        method: "POST",
        headers: tokenHeader()
    });
    const data = await r.json();
    if (r.status !== 200) {
        alert(data.error || 'Nie udało się odświeżyć kodu zaproszenia.');
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
                Nowa nazwa użytkownika: <input v-model="changed_username" type="text" placeholder="Nazwa użytkownika" />
                <button @click="is_changing_username = false">Anuluj</button>
                <button @click="change_username">Zapisz</button>
            </div>
            <div v-else class="row setting">
                Nazwa użytkownika: {{ props.username }} <button @click="is_changing_username = true">Zmień</button>
            </div>

            <div class="row setting">
                <span>Twój kod zaproszenia: {{ invite_code }} <button
                        @click="refresh_invite_code">Odśwież</button></span>
            </div>

            <div class="row setting">
                <span>Tło aplikacji: </span>
                <div class="img-container">
                    <img :src="bg" />
                    <button class="img-button" @click="openBackgroundInput">Zmień</button>
                </div>
                <input class="file-input" type="file" ref="backgroundInput" @change="change_background" />
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

.img-container {
    position: relative;
}

.img-button {
    position: absolute;
    top: 50%;
    left: min(25%, 256px);
    transform: translate(-50%, -50%);
}

img {
    width: min(50%, 512px);
    height: 100%;
    object-fit: contain;
    border-radius: 14px;
    border: 3px solid black;
    filter: contrast(50%);
}

.file-input {
    display: none;
}
</style>