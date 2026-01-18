<script lang="ts" setup>
import { API_URL, tokenHeader } from '@/constants';
import { ref } from 'vue';

const props = defineProps(["username", "message", "isPrivate"]);
const emit = defineEmits(["removeMessage"]);

const hovered = ref(false);

async function removeMessage() {
    const r = await fetch(`${API_URL}/api/${props.isPrivate ? 'private' : 'public'}/messages/${props.message.id}`, {
        method: 'DELETE',
        headers: tokenHeader(),
    });
    const data = await r.json();
    if (r.status !== 200) alert(data.error || 'Błąd');
    else {
        emit("removeMessage", data.id);
    }
}
</script>

<template>
    <div class="msg" @mouseenter="hovered = true" @mouseleave="hovered = false">
        <span class="muted">{{ `${props.message.timestamp} ` }}</span>
        <span>{{ `${isPrivate ? props.message.from : props.message.username}: ${props.message.content}` }}</span>
        <button v-show="hovered && props.username == (isPrivate ? props.message.from : props.message.username)"
            @click="removeMessage">Usuń wiadomość</button>
    </div>
</template>

<style scoped>
.msg {
    display: flex;
    padding: 6px 8px;
    border-bottom: 1px solid #eef2f7;
    font-size: 14px;
    white-space: pre-wrap;
}

.muted {
    color: #4b5563;
}

button {
    background-color: crimson;
    padding: 0px 5px 0px 5px;
    margin-left: auto;
}
</style>