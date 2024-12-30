<template>
  <div class="register-brand">
    <div class="navbar-container">
      <Navbar />
    </div>
    <div class="content">
      <div class="form-card">
        <div class="card-body">
          <h5 class="card-title">Register as Sponsor</h5>
          <form @submit.prevent="register">
            <div class="form-group">
              <label for="username">Username:</label>
              <input type="text" v-model="username" class="form-control" id="username" required>
            </div>
            <div class="form-group">
              <label for="email">Email:</label>
              <input type="email" v-model="email" class="form-control" id="email" required>
            </div>
            <div class="form-group">
              <label for="password">Password:</label>
              <input type="password" v-model="password" class="form-control" id="password" required>
            </div>
            <div class="form-group">
              <label for="company_name">Company Name:</label>
              <input type="text" v-model="company_name" class="form-control" id="company_name" required>
            </div>
            <div class="form-group">
              <label for="industry">Industry:</label>
              <input type="text" v-model="industry" class="form-control" id="industry" required>
            </div>
            <div class="form-group">
              <label for="budget">Budget:</label>
              <input type="number" v-model="budget" class="form-control" id="budget" required>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
            <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'RegisterBrand',
  components: {
    Navbar,
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      company_name: '',
      industry: '',
      budget: '',
      role: 'sponsor',
      errorMessage: '',
    };
  },
  methods: {
    register() {
      if (this.password.length < 5 || this.password.length > 10) {
        this.errorMessage = 'Password must be between 5 and 10 characters long';
        return;
      }

      axios
        .post('http://127.0.0.1:5000/api/register', {
          username: this.username,
          email: this.email,
          password: this.password,
          sponsor_details: {
            company_name: this.company_name,
            industry: this.industry,
            budget: this.budget,
            status: 'pending',
          },
          role: this.role,
        })
        .then((response) => {
          if (response.status === 201) {
            alert('Your request has been sent to admin. Once approved, you can login.');
            this.$router.push('/login');
          }
        })
        .catch((error) => {
          console.log(error);
          this.errorMessage = 'Registration failed. Please try again.';
        });
    },
  },
};
</script>

<style scoped>
/* Navbar Container */
.navbar-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px;
  height: 100vh;
  background-color: #31572c;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
}

/* Navbar Styles */
.navbar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.navbar a {
  text-decoration: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  text-align: center;
  width: 100%;
}

.navbar a:hover {
  background-color: #99582a;
}

/* Page Layout */
.register-brand {
  display: flex;
  height: 100vh;
  background-color: #f5ebe0;
}

.content {
  margin-left: 220px;
  display: flex;
  justify-content: center;
  align-items: center;
  width: calc(100% - 220px);
}

/* Form Card */
.form-card {
  background-color: #9f7e69;
  color: white;
  width: 400px;
  padding: 20px;
  border-radius: 18px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-primary {
  background-color: #31572c;
  border: none;
  border-radius: 10px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #99582a;
}
</style>
