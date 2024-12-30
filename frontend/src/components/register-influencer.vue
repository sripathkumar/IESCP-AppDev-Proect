<template>
  <div class="register-influencer">
    <div class="layout">
      <div class="sidebar">
        <Navbar />
      </div>
      <div class="main-content">
        <div class="form-card">
          <div class="card-body">
            <h5 class="card-title">Register as Influencer</h5>
            <form @submit.prevent="register">
              <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" v-model="username" class="form-control" id="username" required />
              </div>
              <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" v-model="email" class="form-control" id="email" required />
              </div>
              <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" v-model="password" class="form-control" id="password" required />
              </div>
              <div class="form-group">
                <label for="category">Category:</label>
                <input type="text" v-model="category" class="form-control" id="category" required />
              </div>
              <div class="form-group">
                <label for="niche">Niche:</label>
                <input type="text" v-model="niche" class="form-control" id="niche" required />
              </div>
              <div class="form-group">
                <label for="reach">Reach:</label>
                <input type="number" v-model="reach" class="form-control" id="reach" required />
              </div>
              <button type="submit" class="btn btn-primary">Register</button>
              <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/Navbar.vue";

export default {
  name: "RegisterInfluencer",
  components: {
    Navbar,
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      category: "",
      niche: "",
      reach: "",
      role: "influencer",
      errorMessage: "",
    };
  },
  methods: {
    register() {
      if (this.password.length < 5 || this.password.length > 10) {
        this.errorMessage = "Password must be between 5 and 10 characters long";
        return;
      }

      axios
        .post("http://127.0.0.1:5000/api/register", {
          username: this.username,
          email: this.email,
          password: this.password,
          influencer_details: {
            category: this.category,
            niche: this.niche,
            reach: this.reach,
          },
          role: this.role,
        })
        .then((response) => {
          if (response.status === 201) {
            localStorage.setItem("authToken", response.data.token);
            localStorage.setItem("email", response.data.email);
            localStorage.setItem("user_id", response.data.user_id);
            localStorage.setItem("influencer_id", response.data.influencer_id);
            localStorage.setItem("username", response.data.username);
            localStorage.setItem("category", response.data.category);
            localStorage.setItem("niche", response.data.niche);
            localStorage.setItem("reach", response.data.reach);
            localStorage.setItem("role", response.data.role);
            this.$router.push("/influencer-dashboard");
          }
        })
        .catch((error) => {
          console.log(error);
          this.errorMessage = "Registration failed. Please try again.";
        });
    },
  },
};
</script>

<style scoped>
.register-influencer {
  display: flex;
  min-height: 100vh;
  background-color: #f5ebe0;
}

.layout {
  display: flex;
  width: 100%;
}

.sidebar {
  width: 250px;
  background-color: #31572c;
  color: white;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.form-card {
  background-color: #9f7e69;
  color: white;
  width: 30rem;
  padding: 20px;
  border-radius: 18px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}
</style>
