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
        <!-- Add more links as needed -->
        <router-link to="/settings" class="nav-link">Settings</router-link>
      </div>
  
      <!-- Right: Avatar, Name, Dropdown -->
      <div class="navbar-right">
        <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Avatar" class="avatar" />
        <span class="user-name">John Doe</span>
        <div class="dropdown" @click="toggleDropdown" :class="{ 'open': dropdownOpen }">
          <button class="dropdown-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          <transition name="dropdown-fade">
            <div v-if="dropdownOpen" class="dropdown-menu">
              <a href="#" class="dropdown-item">Account Settings</a>
              <a href="#" class="dropdown-item">Preferences</a>
              <hr class="dropdown-divider" />
              <a href="#" class="dropdown-item logout">Logout</a>
            </div>
          </transition>
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
  
  // Optional: Close dropdown when clicking outside
  // import { onMounted, onUnmounted } from 'vue'
  // const closeDropdownOnClickOutside = (event) => {
  //   if (dropdownOpen.value && !event.target.closest('.dropdown')) {
  //     dropdownOpen.value = false;
  //   }
  // }
  // onMounted(() => document.addEventListener('click', closeDropdownOnClickOutside))
  // onUnmounted(() => document.removeEventListener('click', closeDropdownOnClickOutside))
  </script>
  
  <style scoped>
  /* Import Poppins Font */
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
  
  :root {
    --navbar-height: 70px;
    --primary-glow: #a29bfe; /* A soft lavender for glow effects */
    --text-primary: #f0f0f0;
    --text-secondary: #d1d8e0;
    --bg-dropdown: #2c303a; /* Darker, slightly desaturated */
    --hover-accent: #8e44ad; /* A nice purple for accents */
  }
  
  .navbar {
    width: 100%;
    height: var(--navbar-height);
    background: linear-gradient(90deg, #5a63b1, #643e9a);
    color: var(--text-primary);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2.5rem;
    box-sizing: border-box;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    font-family: 'Poppins', sans-serif;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: background 0.3s ease;
  }
  
  /* --- Left Section --- */
  .navbar-left {
    display: flex;
    align-items: center;
    gap: 1rem; /* Consistent gap */
  }
  
  .navbar-logo {
    width: 38px; /* Slightly smaller for sleekness */
    height: 38px;
    transition: transform 0.3s ease;
  }
  .navbar-left:hover .navbar-logo {
    transform: scale(1.1) rotate(-5deg);
  }
  
  .navbar-title {
    font-size: 1.25rem; /* Adjusted size */
    font-weight: 600; /* Semibold for Poppins */
    letter-spacing: 0.5px;
    transition: color 0.3s ease;
  }
  .navbar-left:hover .navbar-title {
    color: #fff;
  }
  
  /* --- Center Section --- */
  .navbar-center {
    display: flex;
    gap: 2.5rem; /* Increased gap for better spacing */
  }
  
  .nav-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 1rem;
    font-weight: 500; /* Medium weight */
    padding: 8px 0; /* Padding for hover effect */
    position: relative;
    transition: color 0.3s ease, transform 0.3s ease;
  }
  
  .nav-link::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    background: var(--primary-glow);
    transition: width 0.3s ease-in-out;
    border-radius: 1px;
  }
  
  .nav-link:hover,
  .nav-link.router-link-exact-active { /* Style for active link */
    color: #ffffff; /* Brighter white for active */
    font-weight: 600; /* Bolder */
    transform: translateY(-2px);
  }
  
  .nav-link:hover::after,
  .nav-link.router-link-exact-active::after {
    width: 70%;
    background: #ffffff; /* Make underline more prominent for active link */
  }
  
  /* --- Right Section --- */
  .navbar-right {
    display: flex;
    align-items: center;
    gap: 1.2rem; /* Consistent gap */
  }
  
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.3);
    transition: border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  }
  .navbar-right:hover .avatar {
    transform: scale(1.05);
    border-color: var(--primary-glow);
    box-shadow: 0 0 10px var(--primary-glow);
  }
  
  .user-name {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-secondary);
    transition: color 0.3s ease;
  }
  .navbar-right:hover .user-name {
    color: var(--text-primary);
  }
  
  /* --- Dropdown --- */
  .dropdown {
    position: relative;
  }
  
  .dropdown-btn {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 6px; /* Added padding for easier click */
    display: flex; /* For aligning SVG */
    align-items: center;
    justify-content: center;
    border-radius: 50%; /* Make it circular */
    transition: background-color 0.3s ease, color 0.3s ease, transform 0.3s ease;
  }
  
  .dropdown-btn svg {
    transition: transform 0.3s ease-in-out;
  }
  
  .dropdown.open .dropdown-btn svg {
    transform: rotate(180deg);
  }
  
  .dropdown-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: var(--text-primary);
  }
  
  .dropdown-menu {
    position: absolute;
    right: 0;
    top: calc(100% + 10px); /* A bit more spacing */
    background-color: var(--bg-dropdown);
    border-radius: 8px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25); /* Enhanced shadow */
    min-width: 200px; /* Wider dropdown */
    display: flex;
    flex-direction: column;
    z-index: 10;
    overflow: hidden; /* For border-radius on items */
    border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle border */
  }
  
  .dropdown-item {
    color: var(--text-secondary);
    padding: 12px 20px; /* More padding */
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 400;
    transition: background-color 0.2s ease, color 0.2s ease, padding-left 0.2s ease;
    cursor: pointer;
    display: block; /* Ensure full width clickable */
  }
  
  .dropdown-item:hover {
    background-color: var(--hover-accent);
    color: #fff;
    padding-left: 25px; /* Slight indent on hover */
  }
  
  .dropdown-item.logout:hover {
    background-color: #e74c3c; /* Red accent for logout */
    color: #fff;
  }
  
  .dropdown-divider {
    height: 1px;
    margin: 8px 0;
    overflow: hidden;
    background-color: rgba(255, 255, 255, 0.1);
    border: 0;
  }
  
  /* Dropdown Transition */
  .dropdown-fade-enter-active,
  .dropdown-fade-leave-active {
    transition: opacity 0.25s ease, transform 0.25s ease;
  }
  
  .dropdown-fade-enter-from,
  .dropdown-fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }
  </style>