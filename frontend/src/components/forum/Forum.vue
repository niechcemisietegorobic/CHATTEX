<script lang="ts" setup>
import { API_URL, tokenHeader, SOCKET_URL } from '@/constants';
import { ref, type Ref, onUnmounted } from 'vue';
import ForumPost from './ForumPost.vue';
import { io } from 'socket.io-client';

const POSTS_PER_PAGE = 5;

const props = defineProps(["username"]);
const emit = defineEmits(["publicNotif", "privateNotif", "updateOnline"]);

const posts: Ref<Array<any>> = ref([]);
const typed_title = ref('');
const typed_body = ref('');
const selected_post: Ref<any> = ref({});
const is_browsing = ref(true);
const skip_count = ref(0);
const is_writing = ref(false);

async function refreshPosts() {
  const r = await fetch(`${API_URL}/api/forum/posts?limit=${POSTS_PER_PAGE}&skip=${skip_count.value}`, {
    method: 'GET',
    headers: tokenHeader()
  });
  const list = await r.json();
  if (r.status !== 200) alert(list.error || 'Błąd dodania posta');
  else {
    posts.value = list;
  }
}

async function selectPost(post_id: number) {
  const r = await fetch(`${API_URL}/api/forum/posts/${post_id}`, {
    method: 'GET',
    headers: tokenHeader()
  });
  const post = await r.json();
  if (r.status !== 200) alert(post.error || 'Błąd dodania posta');
  else {
    selected_post.value = post;
    is_browsing.value = false;
  }
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
    is_writing.value = false;
    await refreshPosts();
  }
}

function updateComment(post_id: number, comment: any) {
  if (selected_post.value.id == post_id) {
    selected_post.value.comments.push(comment);
  }
}

function removeComment(post_id: number, comment_id: number) {
  if (selected_post.value.id == post_id) {
    let j = (selected_post.value.comments as Array<any>).findIndex(c => c.id == comment_id);
    if (j != -1) {
      selected_post.value.comments.pop(j);
    }
  }
}

function updateReactions(post_id: number, reactions: any) {
  if (selected_post.value.id == post_id) {
    selected_post.value.reactions = reactions;
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
  refreshPosts();
});

socket.on("forum_comment", (comment_response) => {
  if (selected_post.value.id == comment_response.post_id) {
    selected_post.value.comments.push(comment_response.comment);
  }
});

socket.on("forum_reactions", (reactions_response) => {
  if (selected_post.value.id == reactions_response.post_id) {
    selected_post.value.reactions = (reactions_response.reactions);
  }
});

function removePost(id: number) {
  is_browsing.value = true;
  posts.value = posts.value.filter(e => e.id != id);
}

socket.on("public_message", () => {
  emit("publicNotif");
});

socket.on("private_message", () => {
  emit("privateNotif");
});

socket.on("forum_post_delete", (post) => {
  removePost(post.id);
});

socket.on("forum_comment_delete", (comment) => {
  removeComment(comment.post_id, comment.id);
});

socket.on("stats", () => {
  emit("updateOnline");
});

function nextPosts() {
  if (posts.value.length > 0) {
    skip_count.value += POSTS_PER_PAGE;
    refreshPosts();
  }
}

function previousPosts() {
  if (POSTS_PER_PAGE <= skip_count.value) {
    skip_count.value -= POSTS_PER_PAGE;
    refreshPosts();
  }
}

refreshPosts();
</script>

<template>
  <section class="tabpane" id="tab-forum">
    <div class="panel">
      <div class="panel-title">Forum - posty</div>

      <form id="post-form" class="stack" v-if="is_writing">
        <input v-model="typed_title" type="text" id="post-title" placeholder="Tytuł posta" required />
        <textarea v-model="typed_body" id="post-body" placeholder="Treść posta..." rows="4" required></textarea>
        <button @click="is_writing = false">Anuluj</button>
        <button type="submit" @click.prevent="addPost">Dodaj post</button>
      </form>

      <div class="row" v-if="!is_writing">
        <button v-if="!is_browsing" @click="is_browsing = true">Wróć</button>
        <button v-if="is_browsing" @click="is_writing = true">Nowy post</button>
        <div v-if="is_browsing" class="navigation-buttons">
          <button @click="previousPosts">Poprzednia</button>
          Strona: {{ 1 + Math.floor(skip_count / POSTS_PER_PAGE) }}
          <button @click="nextPosts">Następna</button>
        </div>
      </div>

      <div id="posts" class="posts" v-if="!is_writing">
        <ForumPost v-if="!is_browsing" :summary="false" :post="selected_post" :username="props.username"
          @updateComment="updateComment" @updateReactions="updateReactions" @removePost="removePost"
          @removeComment="removeComment" />

        <ForumPost v-if="is_browsing" @click="selectPost(post.id)" v-for="post in posts" :summary="true" :post
          :username="props.username" @updateComment="updateComment" @updateReactions="updateReactions"
          @removePost="removePost" @removeComment="removeComment" class="clickable" />
        <div v-if="is_browsing && posts.length == 0">Brak postów na stronie {{ 1 + Math.floor(skip_count /
          POSTS_PER_PAGE) }}</div>
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

.navigation-buttons {
  margin-left: auto;
  margin-right: auto;
}

.clickable {
  cursor: pointer;
}
</style>