<template>
  <nav class="navbar">
    <!-- Left: Logo and System Name -->
    <div class="navbar-left">
      <img src="../assets/vue.svg" alt="Logo" class="navbar-logo" />
      <span class="navbar-title">Student Records System</span>
    </div>
    <!-- Center: Navigation Links -->
    <div class="navbar-center">
      <router-link to="/home" class="nav-link">Home</router-link>
      <router-link to="/records" class="nav-link">Records</router-link>
    </div>
    <!-- Right: Avatar, Name, Dropdown -->
    <div class="navbar-right">
      <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Avatar" class="avatar" />
      <span class="user-name">John Doe</span>
      <div class="dropdown" @click="toggleDropdown">
        <button class="dropdown-btn">▼</button>
        <div v-if="dropdownOpen" class="dropdown-menu">
          <a href="#" class="dropdown-item">Account Settings</a>
          <a href="#" class="dropdown-item">Logout</a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
const dropdownOpen = ref(false)
const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}
</script>

<style scoped>
.navbar {
  width: 100vw;
  height: 64px;
  background: #1a1a1a;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}
.navbar-left {
  display: flex;
  align-items: center;
}
.navbar-logo {
  width: 40px;
  height: 40px;
  margin-right: 12px;
}
.navbar-title {
  font-size: 1.3rem;
  font-weight: bold;
  letter-spacing: 1px;
}
.navbar-center {
  display: flex;
  gap: 2rem;
}
.nav-link {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  transition: color 0.2s;
}
.nav-link:hover {
  color: #646cff;
}
.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}
.avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #646cff;
}
.user-name {
  font-size: 1rem;
  font-weight: 500;
}
.dropdown {
  position: relative;
}
.dropdown-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 8px;
}
.dropdown-menu {
  position: absolute;
  right: 0;
  top: 120%;
  background: #232323;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  min-width: 160px;
  display: flex;
  flex-direction: column;
  z-index: 10;
}
.dropdown-item {
  color: #fff;
  padding: 12px 16px;
  text-decoration: none;
  transition: background 0.2s;
  cursor: pointer;
}
.dropdown-item:hover {
  background: #646cff;
  color: #fff;
}
</style>
