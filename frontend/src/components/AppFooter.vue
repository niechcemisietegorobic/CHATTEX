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
  color: #e5e7eb;
  text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.9);
}
</style>