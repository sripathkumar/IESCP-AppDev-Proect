<template>
  <div class="add-campaign">
    <div class="header-buttons">
      <button @click="goBack">Back</button>
      <button @click="logout">Logout</button>
    </div>
    <h2 class="page-title">Edit Ad {{this.ad.name}}</h2>
    <div class="form-container">
      <form @submit.prevent="submitAd">
        <div class="form-group">
          <label for="name">Ad Name:</label>
          <input type="text" id="name" v-model="name" required placeholder="Enter ad name">
        </div>
        <div class="form-group">
          <label for="content">Content:</label>
          <textarea id="content" v-model="content" required placeholder="Enter ad content"></textarea>
        </div>
        <div class="form-group">
          <label for="start-date">Start Date:</label>
          <input type="date" id="start-date" v-model="start_date" required>
        </div>
        <div class="form-group">
          <label for="budget">Budget:</label>
          <input type="number" id="budget" v-model="budget" required placeholder="Enter budget">
        </div>
        <div class="form-group">
          <label for="requirements">Requirements:</label>
          <input type="text" id="requirements" v-model="requirements" required placeholder="Enter requirements">
        </div>
        <button type="submit" @click="updatead(this.id)" class="btn-submit">Update Ad</button>
      </form>
    </div>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AddingAd',
  data() {
    return {
      sponsor_id: localStorage.getItem('sponsor_id'),
      name: '',
      content: '',
      start_date: '',
      budget: '',
      requirements: '',
      message: '',
      token: '',
      id: null,
      ad: [],
    };
  },
  created() {
    this.id = this.$route.params.id;
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/login');
    }
    this.fetchad(this.id);
  },
  methods: {
    goBack() {
      const role = localStorage.getItem('role');
      if (role === 'sponsor') {
        this.$router.push('/sponsor-dashboard');  // Redirect to sponsor dashboard
      } else if (role === 'admin') {
        this.$router.push('/admin-dashboard');  // Redirect to admin dashboard
      } else {
        this.$router.push('/');  // Redirect to home if no valid role is found
      }
    },
    fetchad(id) {
      const authToken = localStorage.getItem('authToken');
      axios.get(`http://127.0.0.1:5000/api/Ad/${id}`, {
        headers: {
          'Authorization': authToken,
        },
      })
      .then(response => {
        this.ad = response.data.data;
        this.name = response.data.data.name;
        this.content = response.data.data.content;
        this.start_date = response.data.data.start_date;
        this.budget = response.data.data.budget;
        this.requirements = response.data.data.requirements;
      })
      .catch(error => {
        console.error('An error occurred while fetching the campaigns:', error);
      });
    },
    updatead(id) {
      const authToken = localStorage.getItem('authToken');
      if (localStorage.getItem('role') === 'sponsor' || 'admin') {
        axios.put(`http://127.0.0.1:5000/api/Ad/${id}`, 
        {
            name: this.name,
            sponsor_id: this.sponsor_id,
            content: this.content,
            start_date: this.start_date,
            budget: this.budget,
            requirements: this.requirements
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': authToken,
          },
        })
        .then(response => {
          this.message = 'Ad updated successfully';
          this.$router.push('/sponsor-dashboard');
        })
        .catch(error => {
          console.error(error);
          this.message = error.response ? error.response.data.message : 'An error occurred. Please try again.';
        });
      } else {
        this.message = 'You are not authorized to update a campaign';
      }
    },
  },
};
</script>

<style scoped>
/* General Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: #f4f7fb;
  color: #333;
  padding: 20px;
}

/* Main Wrapper */
.add-campaign {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 950px;
  margin: 40px auto;
}

/* Header Buttons */
.header-buttons {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.header-buttons button {
  background-color: #48cae4;
  color: white;
  border: none;
  padding: 12px 18px;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.3s;
}

.header-buttons button:hover {
  background-color: #369cb3;
}

/* Page Title */
.page-title {
  color: #2b2d42;
  font-weight: 600;
  font-size: 30px;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

/* Form Container */
.form-container {
  background-color: #f9f9fb;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #555;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #48cae4;
  outline: none;
}

.form-group textarea {
  resize: vertical;
  height: 150px;
}

/* Submit Button */
.btn-submit {
  background-color: #48cae4;
  color: white;
  padding: 14px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s;
}

.btn-submit:hover {
  background-color: #369cb3;
}

/* Message */
.message {
  text-align: center;
  color: #f44336;
  font-size: 16px;
  margin-top: 20px;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
  .add-campaign {
    padding: 20px;
  }

  .page-title {
    font-size: 24px;
  }

  .form-group label {
    font-size: 14px;
  }

  .form-group input,
  .form-group textarea {
    font-size: 14px;
  }

  .btn-submit {
    padding: 12px 16px;
    font-size: 14px;
  }
}
</style>

