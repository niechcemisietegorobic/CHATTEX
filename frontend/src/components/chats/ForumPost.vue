<script lang="ts" setup>
import ForumReaction from './ForumReaction.vue';
import ForumComment from './ForumComment.vue';
import { ref } from 'vue';
import { API_URL, tokenHeader } from '@/constants';

const props = defineProps(["post"])
const typed_comment = ref('');

const REACTIONS = ["👍", "❤️", "😂", "😮", "😡"];

async function addComment() {
  const r = await fetch(`${API_URL}/api/forum/comments`, {
    method: 'POST',
    headers: tokenHeader(),
    body: JSON.stringify({post_id: props.post.id, body: typed_comment})
  });
  const data = await r.json();
  if (r.status !== 201) alert(data.error || 'Błąd komentarza');
  else {
    props.post.comments.push({})
  }
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
            <ForumReaction v-for="reaction in REACTIONS" :icon="reaction" />
        </div>
        <div class="comm-title">
            Komentarze:
        </div>
        <div class="comments">
            <ForumComment v-for="comment in props.post.comments" :comment />
        </div>
        <form class="row">
            <input v-model="typed_comment" type="text" class="comment-input" placeholder="Dodaj komentarz..." required />
            <button type="submit" @click.prevent="addComment">Dodaj</button>
        </form>
    </div>
</template>