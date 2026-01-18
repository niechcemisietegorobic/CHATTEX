<script lang="ts" setup>

const props = defineProps(["message", "isPrivate"])
</script>

<template>
    <div class="msg">
        <span class="muted">{{ `${props.message.timestamp} ` }}</span>
        <span>{{ `${isPrivate ? props.message.from : props.message.username}: ${props.message.content}` }}</span>
    </div>
</template>

<style scoped>
.msg {
    padding: 6px 8px;
    border-bottom: 1px solid #eef2f7;
    font-size: 14px;
    white-space: pre-wrap;
}

.muted {
  color: #4b5563;
}
</style>