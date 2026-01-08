<script lang="ts" setup>

    const props = defineProps(["message"])
</script>

<template>
    <div class="msg">
        {{ `${props.message.timestamp} - ${props.message.username}: ${props.message.content}` }}
    </div>
</template>