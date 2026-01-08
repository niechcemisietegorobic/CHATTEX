<script lang="ts" setup>
import { API_URL } from '@/constants';
import { ref, type Ref } from 'vue';
import ForumPost from './ForumPost.vue';

const posts: Ref<any, any> = ref([]);

async function refreshPosts() {
    const r = await fetch(`${API_URL}/api/forum/posts`);
    const list = await r.json();

    posts.value = list;
}

refreshPosts();
</script>

<template>
    <!-- FORUM i wszystko wokol -->
    <section class="tabpane" id="tab-forum">
        <div class="panel">
            <div class="panel-title">Forum - posty</div>

            <form id="post-form" class="stack">
                <input type="text" id="post-title" placeholder="Tytuł posta" required />
                <textarea id="post-body" placeholder="Treść posta..." rows="4" required></textarea>
                <button type="submit">Dodaj post</button>
            </form>

            <div id="posts" class="posts">
                <ForumPost v-for="post in posts" :post/>
            </div>
        </div>
    </section>
</template>
