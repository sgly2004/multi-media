<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: "Ma Ying Hei", Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background: #f9f4e6;
  color: #2c3e50;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.scroll-container {
  position: relative;
  margin: 40px auto;
  max-width: 1200px;
  background: linear-gradient(
    to right,
    rgba(244, 236, 218, 0.8),
    rgba(244, 236, 218, 0.95),
    rgba(244, 236, 218, 0.8)
  );
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.scroll-container::before,
.scroll-container::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 40px;
  background: #8b4513;
  opacity: 0.1;
}
</style>
