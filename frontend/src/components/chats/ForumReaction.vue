<script lang="ts" setup>
    const props = defineProps(["icon"])
</script>

<template>
    <button class="emoji">{{ props.icon }}</button>
</template>
