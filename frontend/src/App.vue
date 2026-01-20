<script setup lang="ts">

import AppHeader from './components/AppHeader.vue';
import MainContainer from './components/MainContainer.vue';
import AppFooter from './components/AppFooter.vue';
import { IS_DEV, API_URL } from './constants';
import { ref } from 'vue';

const online = ref(0);
const registered = ref(0);

async function stats() {
  const r = await fetch(`${API_URL}/api/stats`);
  const data = await r.json();
  if (r.status == 200) {
    online.value = data.online;
    registered.value = data.registered;
  }
}

function updateOnline() {
  stats();
}

if (IS_DEV) {
  document.body.style.backgroundBlendMode = "multiply";
  document.body.style.backgroundColor = "#FAA99B";
}

stats();
</script>

<template>
  <div class="app-shell">
    <AppHeader :online :registered />
    <MainContainer @updateOnline="updateOnline" />
    <AppFooter />
  </div>
</template>

<style scoped>
.app-shell {
  max-width: max(90%, 920px);
  margin: 0 auto;
  padding: 28px 16px 18px;
}
</style>
