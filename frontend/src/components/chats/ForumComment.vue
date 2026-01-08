<script lang="ts" setup>
const props = defineProps(["comment"]);
</script>

<template>
    <div class="comment">
        {{ props.comment.timestamp }} - {{ props.comment.author }}: {{ props.comment.body }}
    </div>
</template>

<style scoped>
.comment {
    padding: 6px 6px;
    border-bottom: 1px solid #eef2f7;
    font-size: 13px;
}
</style>