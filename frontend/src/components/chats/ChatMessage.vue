<script lang="ts" setup>

    const props = defineProps(["message", "isPrivate"])
</script>

<template>
    <div class="msg">
        {{ `${props.message.timestamp} - ${isPrivate ? props.message.from : props.message.username}: ${props.message.content}` }}
    </div>
</template>

<style scoped>
.msg {
    padding: 6px 8px;
    border-bottom: 1px solid #eef2f7;
    font-size: 14px;
    white-space: pre-wrap;
}
</style>