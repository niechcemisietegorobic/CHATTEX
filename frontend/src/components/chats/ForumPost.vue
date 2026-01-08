<script lang="ts" setup>
import ForumReaction from './ForumReaction.vue';
import ForumComment from './ForumComment.vue';
import { ref } from 'vue';
import { API_URL, tokenHeader } from '@/constants';

const props = defineProps(["post"])
const emit = defineEmits(["updateComment", "updateReactions"])
const typed_comment = ref('');

const REACTIONS = ["👍", "❤️", "😂", "😮", "😡"];

async function addComment() {
    const r = await fetch(`${API_URL}/api/forum/comments`, {
        method: 'POST',
        headers: tokenHeader(),
        body: JSON.stringify({ post_id: props.post.id, body: typed_comment.value })
    });
    typed_comment.value = "";
    const data = await r.json();
    if (r.status !== 201) alert(data.error || 'Błąd komentarza');
    else {
        emit("updateComment", props.post.id, data);
    }
}

function updateReactions(post_id: number, reactions: any) {
    emit("updateReactions", post_id, reactions);
}
</script>

<template>
    <div class="post">
        <div class="post-title">
            {{ props.post.title }}
        </div>
        <div class="post-meta">
            {{ props.post.timestamp + " • " + props.post.author }}
        </div>
        <div class="post-body">
            {{ props.post.body }}
        </div>
        <div class="react-row">
            <ForumReaction v-for="reaction in REACTIONS" :icon="reaction" :post_id="props.post.id"
                :count="(props.post.reactions && props.post.reactions[reaction]) ? props.post.reactions[reaction] : 0"
                @updateReactions="updateReactions" />
        </div>
        <div class="comm-title">
            Komentarze:
        </div>
        <div class="comments">
            <ForumComment v-for="comment in props.post.comments" :comment />
        </div>
        <form class="row">
            <input v-model="typed_comment" type="text" class="comment-input" placeholder="Dodaj komentarz..."
                required />
            <button type="submit" @click.prevent="addComment">Dodaj</button>
        </form>
    </div>
</template>

<style scoped>
.post {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 12px;
    background: #fff;
}

.post-title {
    font-weight: 900;
    font-size: 16px;
}

.post-meta {
    font-size: 12px;
    color: #6b7280;
    margin-top: 2px;
}

.post-body {
    margin-top: 10px;
    white-space: pre-wrap;
}

.react-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin: 10px 0 8px;
}

.comm-title {
    font-weight: 800;
    margin-top: 6px;
}

.comments {
    background: #f9fafb;
    border: 1px solid #eef2f7;
    border-radius: 10px;
    padding: 8px;
    margin: 8px 0;
}
</style>