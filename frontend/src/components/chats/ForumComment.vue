<script lang="ts" setup>
const props = defineProps(["comment"]);
</script>

<template>
    <div class="comment">
        {{ props.comment.timestamp }} - {{ props.comment.author }}: {{ props.comment.body }}
    </div>
</template>
