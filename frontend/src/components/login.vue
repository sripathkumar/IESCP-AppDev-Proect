<template>
  <div class="login">
    <div class="navbar-container">
      <Navbar />
    </div>
    <div class="content">
      <!-- Forms Container -->
      <div class="forms-container">
        <!-- User Login Form -->
        <div class="form-card">
          <div class="card-body">
            <h5 class="card-title">User Login</h5>
            <form @submit.prevent="login">
              <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" v-model="username" class="form-control" id="username" required>
              </div>
              <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" v-model="password" class="form-control" id="password" required>
              </div>
              <button type="submit" class="btn btn-primary">Login</button>
            </form>
          </div>
        </div>

        <!-- Admin Login Form -->
        <div class="form-card">
          <div class="card-body">
            <h5 class="card-title">Admin Login</h5>
            <form @submit.prevent="adminLogin">
              <div class="form-group">
                <label for="admin-username">Username:</label>
                <input type="text" v-model="adminUsername" class="form-control" id="admin-username" required>
              </div>
              <div class="form-group">
                <label for="admin-password">Password:</label>
                <input type="password" v-model="adminPassword" class="form-control" id="admin-password" required>
              </div>
              <button type="submit" class="btn btn-primary">Login</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'Login',
  components: {
    Navbar,
  },
  data() {
    return {
      username: '',
      password: '',
      adminUsername: '',
      adminPassword: '',
      errorMessage: '',
    };
  },
  methods: {
    login() {
      axios
        .post('http://127.0.0.1:5000/api/login', {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          if (response.status === 200) {
            localStorage.setItem('authToken', response.data.token);
            localStorage.setItem('username', response.data.username);
            localStorage.setItem('user_id', response.data.user_id);
            localStorage.setItem('role', response.data.role);

            const role = response.data.role;
            if (role === 'sponsor' && response.data.status === 'approved') {
              localStorage.setItem('Company_name', response.data.Company_name);
              localStorage.setItem('sponsor_id', response.data.sponsor_id);
              localStorage.setItem('Industry', response.data.Industry);
              localStorage.setItem('budget', response.data.budget);
              localStorage.setItem('status', response.data.status);
              this.$router.push('/sponsor-dashboard');
            } else if(role === 'influencer'){
              localStorage.setItem('category', response.data.category);
              localStorage.setItem('influencer_id', response.data.influencer_id);
              localStorage.setItem('niche', response.data.niche);
              localStorage.setItem('reach', response.data.reach);
              this.$router.push('/influencer-dashboard');
            } else{alert('cannot login until admin approves!!');
            this.$router.push('/login');
          }
        }
        })
        .catch((error) => {
          if (error.response) {
            if (error.response.status === 401) {
              this.errorMessage = 'Password is incorrect';
            } else if (error.response.status === 404) {
              this.errorMessage = 'Username does not exist';
            } else {
              this.errorMessage = 'An error occurred. Please try again.';
            }
          } else {
            this.errorMessage = 'Network error. Please try again.';
          }
        });
    },
    adminLogin() {
      if (this.adminUsername === 'admin' && this.adminPassword === '123456') {
        axios
          .post('http://127.0.0.1:5000/api/login', {
            username: this.adminUsername,
            password: this.adminPassword,
          })
          .then((response) => {
            if (response.data.role === 'admin') {
              localStorage.setItem('username', this.adminUsername);
              localStorage.setItem('role', response.data.role);
              localStorage.setItem('authToken', response.data.token);
              this.$router.push('/Admin-dashboard');
            } else {
              this.errorMessage = 'Invalid admin credentials';
            }
          })
          .catch((error) => {
            console.error('Login error:', error);
            this.errorMessage = 'An error occurred during login';
          });
      } else {
        this.errorMessage = 'Invalid admin credentials';
      }
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
.login {
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

/* Forms Container */
.forms-container {
  display: flex;
  gap: 2rem;
  justify-content: center;
  align-items: center;
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

.alert {
  margin-top: 20px;
}
</style>
