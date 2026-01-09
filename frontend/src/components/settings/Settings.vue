<script lang="ts" setup>
const props = defineProps(["username"]);

const bg = new URL('@/assets/background.png', import.meta.url).href
</script>

<template>
    <section class="tabpane" id="tab-settings">
        <div class="panel">
            <div class="panel-title">Ustawienia</div>

            <div class="row setting">
                Nazwa użytkownika: {{ props.username }}
            </div>

            <div class="row setting">
                <span>Tło aplikacji <button>Zmień</button></span>
                <img :src="bg" />
            </div>

        </div>
    </section>
</template>

<style scoped>
.panel-title {
    font-weight: 800;
    margin-bottom: 8px;
}

.setting {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 6px 6px;
    font-weight: 200;
}

img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
</style>