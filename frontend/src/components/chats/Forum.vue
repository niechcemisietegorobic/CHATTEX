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

            <div id="posts" class="posts"></div>
        </div>
    </section>
</template>
