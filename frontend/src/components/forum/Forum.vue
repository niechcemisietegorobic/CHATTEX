<script lang="ts" setup>
import { API_URL, tokenHeader, SOCKET_URL } from '@/constants';
import { ref, type Ref, onUnmounted } from 'vue';
import ForumPost from './ForumPost.vue';
import { io } from 'socket.io-client';

const emit = defineEmits(["publicNotif", "privateNotif"]);

const posts: Ref<any[], any[]> = ref([]);
const typed_title = ref('');
const typed_body = ref('');

async function refreshPosts() {
  const r = await fetch(`${API_URL}/api/forum/posts`);
  const list = await r.json();

  posts.value = list;
}

async function addPost() {
  const r = await fetch(`${API_URL}/api/forum/posts`, {
    method: 'POST',
    headers: tokenHeader(),
    body: JSON.stringify({ title: typed_title.value, body: typed_body.value })
  });
  typed_title.value = "";
  typed_body.value = "";
  const data = await r.json();
  if (r.status !== 201) alert(data.error || 'Błąd dodania posta');
  else {
    posts.value.unshift(data);
  }
}

function updateComment(post_id: number, comment: any) {
  let i = posts.value.findIndex(post => post.id == post_id);
  if (i != -1) {
    posts.value[i].comments.push(comment);
  }
}

function updateReactions(post_id: number, reactions: any) {
  let i = posts.value.findIndex(post => post.id == post_id);
  if (i != -1) {
    posts.value[i].reactions = reactions;
  }
}

const socket = io(SOCKET_URL, {
  auth: {
    token: tokenHeader().Authorization
  }
});

onUnmounted(() => {
  socket.close();
});

socket.on("forum_post", (post) => {
  posts.value.unshift(post);
});

socket.on("forum_comment", (comment_response) => {
  let i = posts.value.findIndex(post => post.id == comment_response.post_id);
  if (i != -1) {
    posts.value[i].comments.push(comment_response.comment);
  }
});

socket.on("forum_reactions", (reactions_response) => {
  let i = posts.value.findIndex(post => post.id == reactions_response.post_id);
  if (i != -1) {
    posts.value[i].reactions = (reactions_response.reactions);
  }
});

socket.on("public_message", () => {
  emit("publicNotif");
});


socket.on("private_message", () => {
  emit("privateNotif");
});

refreshPosts();
</script>

<template>
  <!-- FORUM i wszystko wokol -->
  <section class="tabpane" id="tab-forum">
    <div class="panel">
      <div class="panel-title">Forum - posty</div>

      <form id="post-form" class="stack">
        <input v-model="typed_title" type="text" id="post-title" placeholder="Tytuł posta" required />
        <textarea v-model="typed_body" id="post-body" placeholder="Treść posta..." rows="4" required></textarea>
        <button type="submit" @click.prevent="addPost">Dodaj post</button>
      </form>

      <div id="posts" class="posts">
        <ForumPost v-for="post in posts" :post @updateComment="updateComment" @updateReactions="updateReactions" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.panel-title {
  font-weight: 800;
  margin-bottom: 8px;
}

.posts {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>