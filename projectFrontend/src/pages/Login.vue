<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email:</label>
          <input type="email" v-model="email" required>
        </div>
        <div class="form-group">
          <label>Password:</label>
          <input type="password" v-model="password" required>
        </div>
        <div class="error" v-if="error">{{ error }}</div>
        <button type="submit">Login</button>
      </form>
      <p>Don't have an account? <router-link to="/register">Register here</router-link></p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:8000/api/login/', {
          email: this.email,
          password: this.password
        });
        
        if (response.data && response.data.user) {
          // Store user info
          const userData = {
            email: response.data.user.email,
            name: response.data.user.name,
            isAuthenticated: true
          };
          localStorage.setItem('user', JSON.stringify(userData));
          this.$router.push('/home');
        } else {
          this.error = 'Login failed. Please try again.';
        }
      } catch (err) {
        if (err.response && err.response.status === 401) {
          this.error = 'Invalid email or password';
        } else if (err.response && err.response.data && err.response.data.error) {
          this.error = err.response.data.error;
        } else {
          this.error = 'An error occurred. Please try again.';
        }
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - var(--navbar-height));
  width: 100%;
}

.login-form {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
  margin: 2rem;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: var(--hover-accent);
}

button {
  width: 100%;
  padding: 0.875rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 1rem;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: #e74c3c;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

p {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

a {
  color: var(--hover-accent);
  text-decoration: none;
  font-weight: 500;
}

a:hover {
  text-decoration: underline;
}
</style>