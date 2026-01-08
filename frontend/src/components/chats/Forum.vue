<script lang="ts" setup>
import { API_URL, tokenHeader } from '@/constants';
import { ref, type Ref } from 'vue';
import ForumPost from './ForumPost.vue';

const posts: Ref<any, any> = ref([]);
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
    body: JSON.stringify({title: typed_title.value, body: typed_body.value})
  });
  const data = await r.json();
  if (r.status !== 201) alert(data.error || 'Błąd dodania posta');
  else {
    // posts.value.push()
  }
}

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
                <ForumPost v-for="post in posts" :post/>
            </div>
        </div>
    </section>
</template>
