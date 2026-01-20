<script lang="ts" setup>
import { ref } from 'vue';

const props = defineProps(["online", "registered"]);

</script>

<template>
  <header class="topbar">
    <div>
      <div class="brand">CHATTEX - CHATTUJ DO WOLI</div>
      <div class="sub">Public chat • Prywatne wiadomości • Forum</div>
    </div>
    <div class="status">
      <div>🟢 {{ props.online }} online</div>
      <div>⚫ {{ props.registered }} zarejestrowanych</div>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
  /* color: #e5e7eb;
  text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.9); */
  background: rgba(255, 255, 255, 0.72);
  border-radius: 14px;
  padding: 9px;
  box-shadow: 0 18px 60px rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(6px);
  display: flex;
}

.status {
  margin: 4px 4px 4px auto;
}

.status > div {
  font-weight: 800;
}

.brand {
  font-size: 28px;
  font-weight: 800;
}

.sub {
  margin-top: 4px;
  font-size: 13px;
}
</style>