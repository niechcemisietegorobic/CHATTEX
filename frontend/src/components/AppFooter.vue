<script lang="ts" setup>
  import { IS_DEV, BUILD_NUMBER } from '@/constants';
</script>

<template>
  <footer class="foot">
    {{ `${IS_DEV ? "Dev" : "Prod"} build ${IS_DEV ? BUILD_NUMBER : "" } • Backend: Flask • Frontend: vue + ts` }}
  </footer>
</template>

<style scoped>
.foot {
  margin-top: 14px;
  text-align: center;
  /* color: #e5e7eb; */
  /* text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.9); */
  background: rgba(255,255,255,0.72);
  border-radius: 14px;
  padding: 9px;
  box-shadow: 0 18px 60px rgba(0,0,0,0.45);
  backdrop-filter: blur(6px);
}
</style>
