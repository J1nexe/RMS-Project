<template>
  <div class="register-container">  <div class="register-form">
      <h2>Register</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Name:</label>
          <input type="text" v-model="name" required>
        </div>
        <div class="form-group">
          <label>Email:</label>
          <input type="email" v-model="email" required>
        </div>
        <div class="form-group">
          <label>Password:</label>
          <input type="password" v-model="password" required minlength="6">
        </div>
        <div class="form-group">
          <label>Confirm Password:</label>
          <input type="password" v-model="confirmPassword" required minlength="6">
        </div>
        <div class="error" v-if="error">{{ error }}</div>
        <button type="submit">Register</button>
      </form>
      <p>Already have an account? <router-link to="/login">Login here</router-link></p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      error: ''
    }
  },
  methods: {
    async handleRegister() {
      try {
        if (this.password !== this.confirmPassword) {
          this.error = 'Passwords do not match';
          return;
        }

        if (this.password.length < 6) {
          this.error = 'Password must be at least 6 characters long';
          return;
        }        const response = await axios.post('http://localhost:8000/api/users/', {
          name: this.name,
          email: this.email,
          password: this.password
        });
        
        if (response.data) {
          this.$router.push('/login');
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          this.error = err.response.data.error;
        } else if (err.response && err.response.status === 400) {
          this.error = 'Invalid email or password format';
        } else {
          this.error = 'Registration failed. Please try again.';
        }
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - var(--navbar-height));
  width: 100%;
}

.register-form {
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