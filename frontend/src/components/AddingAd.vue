<template>
  <div class="add-ad-container">
    <div class="header-buttons">
      <button @click="navigateTo('/sponsor-dashboard')">Back</button>
      <button @click="logout">Logout</button>
    </div>
    <h3 class="page-title">Add New Ad to "{{ this.campname }}"</h3>
    <form @submit.prevent="submitAd" class="ad-form">
      <div class="form-group">
        <label for="name">Ad Name</label>
        <input type="text" v-model="name" required placeholder="Enter Ad name">
      </div>

      <div class="form-group">
        <label for="content">Ad Content</label>
        <textarea v-model="content" required placeholder="Describe the ad content"></textarea>
      </div>

      <div class="form-group">
        <label for="start_date">Start Date</label>
        <input type="date" v-model="start_date" required>
      </div>

      <div class="form-group">
        <label for="requirements">Requirements</label>
        <textarea v-model="requirements" required placeholder="List requirements for the ad"></textarea>
      </div>

      <div class="form-group">
        <label for="budget">Budget</label>
        <input type="number" v-model="budget" required placeholder="Enter ad budget">
      </div>

      <button type="submit" class="submit-button">Submit Ad</button>
    </form>
    <p class="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      name: '',
      content: '',
      campaign_id: '',
      sponsor_id: localStorage.getItem('sponsor_id'),
      start_date: '',
      requirements: '',
      budget: '',
      status: true,
      message: '',
      id: null,
      campname: ''
    };
  },
  created() {
    this.id = this.$route.params.id;
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/login');
    }
    this.fetchCampaigns(this.id);
  },
  methods: {
    navigateTo(path) {
    this.$router.push(path);
  },
    fetchCampaigns(id) {
      const authToken = localStorage.getItem('authToken');
      axios.get(`http://127.0.0.1:5000/api/campaign/${id}`, {
        headers: {
          'Authorization': authToken
        }
      })
      .then(response => {
        this.campaigns = response.data.data;
        this.campaign_id = response.data.data.id;
        this.campname = response.data.data.name;
      })
      .catch(error => {
        console.error('Error fetching campaigns:', error);
      });
    },
    submitAd() {
      const formData = new FormData();
      formData.append('name', this.name);
      formData.append('content', this.content);
      formData.append('campaign_id', this.campaign_id);
      formData.append('sponsor_id', this.sponsor_id);
      formData.append('start_date', this.start_date);
      formData.append('requirements', this.requirements);
      formData.append('budget', this.budget);
      formData.append('status', this.status === true ? 'true' : 'false');

      const authToken = localStorage.getItem('authToken');
      axios.post('http://127.0.0.1:5000/api/Ad', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': authToken
        }
      })
      .then(response => {
        this.message = 'Ad added successfully';
        this.$router.push('/sponsor-dashboard');
      })
      .catch(error => {
        console.error('Error adding ad:', error);
        this.message = 'An error occurred. Please try again.';
      });
    }
  }
};
</script>

<style scoped>
.add-ad-container {
  background-color: #f8f8f8;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 40px auto;
}

.header-buttons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.header-buttons button {
  background-color: #1d3557;
  color: #fff;
  border: none;
  padding: 12px 20px;
  border-radius: 30px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.header-buttons button:hover {
  background-color: #457b9d;
}

.page-title {
  text-align: center;
  color: #1d3557;
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 30px;
  text-transform: uppercase;
}

.ad-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 16px;
  color: #333;
}

.form-group input,
.form-group textarea {
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #1d3557;
  outline: none;
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.submit-button {
  background-color: #1d3557;
  color: white;
  padding: 15px 25px;
  font-size: 18px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #457b9d;
}

.message {
  margin-top: 20px;
  text-align: center;
  color: #1d3557;
  font-size: 18px;
}
</style>
