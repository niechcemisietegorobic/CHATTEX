<script lang="ts" setup>
import { API_URL, tokenHeader } from '@/constants';
import { ref } from 'vue';

const props = defineProps(["comment", "username"]);
const emit = defineEmits(["removeComment"]);

async function removeComment() {
    const r = await fetch(`${API_URL}/api/forum/comments/${props.comment.id}`, {
        method: 'DELETE',
        headers: tokenHeader(),
    });
    const data = await r.json();
    if (r.status !== 200) alert(data.error || 'Błąd');
    else {
        emit("removeComment", data.post_id, data.id);
    }
}

const hovered = ref(false);
</script>

<template>
    <div class="comment" @mouseenter="hovered = true" @mouseleave="hovered = false">
        {{ props.comment.timestamp }} - {{ props.comment.author }}: {{ props.comment.body }}
        <button v-show="hovered && props.username == props.comment.author"
            @click="removeComment">Usuń</button>
    </div>
</template>

<style scoped>
.comment {
    display: flex;
    padding: 6px 6px;
    border-bottom: 1px solid #eef2f7;
    font-size: 13px;
}

button {
    padding: 0px 5px 0px 5px;
    margin-left: auto;
    margin-top: 0;
    margin-bottom: 0;
    font-weight: bold;
}
</style>