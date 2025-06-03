<script setup>
import TopNavbar from './components/topNavbar.vue'
</script>

<template>
  <div id="app">
    <TopNavbar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style>
/* Import Poppins Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
  --navbar-height: 70px;
  --primary-glow: #a29bfe;
  --text-primary: #f0f0f0;
  --text-secondary: #d1d8e0;
  --bg-dropdown: #2c303a;
  --hover-accent: #8e44ad;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  font-family: 'Poppins', sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.main-content {
  padding-top: var(--navbar-height);
  flex: 1;
  width: 100%;
}
</style>
