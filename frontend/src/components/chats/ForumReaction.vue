<script lang="ts" setup>
    const props = defineProps(["icon", "count"])
</script>

<template>
    <button class="emoji">{{ props.icon }} {{ props.count }}</button>
</template>
