<script setup lang="ts">

import AppHeader from './components/AppHeader.vue';
import MainContainer from './components/MainContainer.vue';
import AppFooter from './components/AppFooter.vue';
</script>

<template>
  <div class="app-shell">
    <AppHeader />
    <MainContainer />
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
