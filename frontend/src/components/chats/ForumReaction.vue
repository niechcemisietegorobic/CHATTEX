<script lang="ts" setup>
import { API_URL, tokenHeader } from '@/constants';
const props = defineProps(["icon", "count", "post_id"]);
const emit = defineEmits(["updateReactions"]);

async function toggleReaction() {
    const r = await fetch(`${API_URL}/api/forum/reactions`, {
        method: 'POST',
        headers: tokenHeader(),
        body: JSON.stringify({ post_id: props.post_id, emoji: props.icon })
    });
    const data = await r.json();
    if (r.status !== 200) alert(data.error || 'Błąd reakcji');
    else {
        emit("updateReactions", props.post_id, data);
    }
}
</script>

<template>
    <button class="emoji" @click="toggleReaction">{{ props.icon }} {{ props.count }}</button>
</template>

<style scoped>
button.emoji {
    background: #f3f4f6;
    color: #111;
    border: 1px solid #e5e7eb;
    padding: 6px 10px;
    border-radius: 999px;
}
</style>
