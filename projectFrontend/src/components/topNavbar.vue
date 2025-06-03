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
        <router-link to="/data" class="nav-link">Records</router-link>
      </div>
  
      <!-- Right: Avatar, Name, Dropdown -->
      <div class="navbar-right">
        <img :src="userAvatar" alt="Avatar" class="avatar" />
        <span class="user-name">{{ userName }}</span>
        <div class="dropdown" ref="dropdownRef">
          <button class="dropdown-btn" @click="toggleDropdown">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          <div v-show="dropdownOpen" class="dropdown-menu">
            <a @click="handleAccountSettings" class="dropdown-item">Account Settings</a>
            <a @click="handlePreferences" class="dropdown-item">Preferences</a>
            <hr class="dropdown-divider" />
            <a @click="handleLogout" class="dropdown-item logout">Logout</a>
          </div>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const dropdownOpen = ref(false)
  const dropdownRef = ref(null)
  
  const userEmail = computed(() => {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    return user.email || 'User'
  })
  
  const userAvatar = ref('https://randomuser.me/api/portraits/men/32.jpg')
  
  // Toggle dropdown
  const toggleDropdown = () => {
    dropdownOpen.value = !dropdownOpen.value
  }
  
  // Close dropdown when clicking outside
  const closeDropdownOnClickOutside = (event) => {
    if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
      dropdownOpen.value = false
    }
  }
  
  // Handle dropdown menu items
  const handleAccountSettings = () => {
    dropdownOpen.value = false
    // Add account settings logic here
  }
  
  const handlePreferences = () => {
    dropdownOpen.value = false
    // Add preferences logic here
  }
  
  const handleLogout = () => {
    // Clear user data from localStorage
    localStorage.removeItem('user')
    // Close dropdown
    dropdownOpen.value = false
    // Redirect to login page
    router.push('/login')
  }
  
  // Lifecycle hooks for click outside listener
  onMounted(() => {
    document.addEventListener('click', closeDropdownOnClickOutside)
  })
  
  onUnmounted(() => {
    document.removeEventListener('click', closeDropdownOnClickOutside)
  })
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
    z-index: 100;
    font-family: 'Poppins', sans-serif;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
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
    z-index: 1000;
  }
  
  .dropdown-btn {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.3s ease;
  }
  
  .dropdown-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  .dropdown-btn svg {
    transition: transform 0.3s ease;
  }
  
  .dropdown[data-open="true"] .dropdown-btn svg {
    transform: rotate(180deg);
  }
  
  .dropdown-menu {
    position: absolute;
    right: 0;
    top: 100%;
    background-color: var(--bg-dropdown);
    border-radius: 8px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    min-width: 200px;
    padding: 0.5rem 0;
    margin-top: 0.5rem;
    z-index: 1000;
  }
  
  .dropdown-item {
    color: var(--text-secondary);
    padding: 0.75rem 1.5rem;
    display: block;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .dropdown-item:hover {
    background-color: var(--hover-accent);
    color: white;
    padding-left: 2rem;
  }
  
  .dropdown-item.logout:hover {
    background-color: #e74c3c;
  }
  
  .dropdown-divider {
    margin: 0.5rem 0;
    border: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
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