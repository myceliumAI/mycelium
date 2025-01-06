<template>
  <div class="silent-check-sso"></div>
</template>

<script>
import { defineComponent, onMounted } from 'vue';

export default defineComponent({
  name: 'SilentCheckSso',
  setup() {
    onMounted(() => {
      window.parent.postMessage(location.href, location.origin);
    });
  }
});
</script> 